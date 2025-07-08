"use client";

import { useEffect, useRef } from "react";
import type { Alert } from "@/types/alert";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface MapViewProps {
  alerts: Alert[];
}

export function MapView({ alerts }: MapViewProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);

  useEffect(() => {
    if (
      typeof window !== "undefined" &&
      mapRef.current &&
      !mapInstanceRef.current
    ) {
      import("leaflet").then((L) => {
        const map = L.map(mapRef.current!).setView(
          [
            Number.parseFloat(process.env.NEXT_PUBLIC_DEFAULT_LAT || "28.6139"),
            Number.parseFloat(process.env.NEXT_PUBLIC_DEFAULT_LNG || "77.2090"),
          ],
          13
        );

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          attribution: "© OpenStreetMap contributors",
        }).addTo(map);

        mapInstanceRef.current = map;
      });
    }
  }, []);

  // ✅ Color-coded severity markers on map
  useEffect(() => {
    if (mapInstanceRef.current && typeof window !== "undefined") {
      import("leaflet").then((L) => {
        // Clear existing markers
        markersRef.current.forEach((marker) => {
          mapInstanceRef.current.removeLayer(marker);
        });
        markersRef.current = [];

        // Create custom icons based on severity
        const createCustomIcon = (severity: string, anomalyType: string) => {
          const colors = {
            low: "#22c55e",
            medium: "#f59e0b",
            high: "#ef4444",
          };

          const icons = {
            fire: "🔥",
            smoke: "💨",
            crowd_panic: "👥",
            suspicious_activity: "👁️",
            violence: "⚡",
          };

          return L.divIcon({
            html: `
              <div style="
                background-color: ${
                  colors[severity as keyof typeof colors] || "#6b7280"
                }; 
                width: 30px; 
                height: 30px; 
                border-radius: 50%; 
                border: 3px solid white; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.4);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
              ">
                ${icons[anomalyType as keyof typeof icons] || "⚠️"}
              </div>
            `,
            iconSize: [30, 30],
            className: "custom-marker",
          });
        };

        // Add markers for each alert
        alerts.forEach((alert) => {
          if (alert.location) {
            const marker = L.marker([alert.location.lat, alert.location.lng], {
              icon: createCustomIcon(alert.severity, alert.anomaly_type),
            }).addTo(mapInstanceRef.current);

            marker.bindPopup(`
              <div style="padding: 12px; min-width: 200px;">
                <h3 style="font-weight: bold; font-size: 16px; margin-bottom: 8px; color: #1e293b;">
                  ${alert.anomaly_type.replace("_", " ").toUpperCase()}
                </h3>
                <p style="font-size: 14px; color: #475569; margin-bottom: 8px;">
                  ${alert.description}
                </p>
                <div style="font-size: 12px; color: #64748b;">
                  <strong>Confidence:</strong> ${(
                    alert.confidence * 100
                  ).toFixed(1)}%<br>
                  <strong>Severity:</strong> <span style="color: ${
                    alert.severity === "high"
                      ? "#ef4444"
                      : alert.severity === "medium"
                      ? "#f59e0b"
                      : "#22c55e"
                  }">${alert.severity.toUpperCase()}</span><br>
                  <strong>Zone:</strong> ${alert.zone}<br>
                  <strong>Time:</strong> ${alert.timestamp.toLocaleString()}<br>
                  <strong>Status:</strong> ${
                    alert.resolved ? "✅ Resolved" : "🔴 Active"
                  }
                </div>
                ${
                  alert.snapshot_url
                    ? `
                  <a href="${alert.snapshot_url}" target="_blank" 
                     style="display: inline-block; margin-top: 8px; padding: 4px 8px; 
                            background: #3b82f6; color: white; text-decoration: none; 
                            border-radius: 4px; font-size: 12px;">
                    📸 View Snapshot
                  </a>
                `
                    : ""
                }
              </div>
            `);

            markersRef.current.push(marker);
          }
        });
      });
    }
  }, [alerts]);

  return (
    <Card className="bg-slate-900 border-slate-700">
      <CardHeader>
        <CardTitle className="text-blue-400 flex items-center gap-2">
          🗺️ Live Security Map
          <span className="text-sm font-normal text-slate-400">
            ({alerts.length} alerts)
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div
          ref={mapRef}
          className="w-full h-96 rounded-lg border border-slate-700"
          style={{ minHeight: "400px" }}
        />
        <div className="flex items-center gap-6 mt-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-green-500 rounded-full border-2 border-white shadow"></div>
            <span>Low Severity</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-yellow-500 rounded-full border-2 border-white shadow"></div>
            <span>Medium Severity</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-red-500 rounded-full border-2 border-white shadow"></div>
            <span>High Severity</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
