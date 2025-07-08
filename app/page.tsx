"use client"

import { useState, useEffect } from "react"
import { collection, onSnapshot, query, orderBy } from "firebase/firestore"
import { db } from "@/lib/firebase"
import { MapView } from "@/components/map-view"
import { AlertsList } from "@/components/alerts-list"
import { ChatBot } from "@/components/chat-bot"
import { StatsCards } from "@/components/stats-cards"
import { FilterControls } from "@/components/filter-controls"
import type { Alert } from "@/types/alert"

export default function Dashboard() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [filteredAlerts, setFilteredAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    severity: "all",
    type: "all",
    resolved: "all",
    timeRange: "24h",
  })

  // ✅ Real-time Firestore listener (not polling)
  useEffect(() => {
    const alertsQuery = query(collection(db, "alerts"), orderBy("timestamp", "desc"))

    const unsubscribe = onSnapshot(
      alertsQuery,
      (snapshot) => {
        const alertsData = snapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data(),
          timestamp: doc.data().timestamp?.toDate() || new Date(),
        })) as Alert[]

        setAlerts(alertsData)
        setLoading(false)
      },
      (error) => {
        console.error("Firestore listener error:", error)
        setLoading(false)
      },
    )

    return () => unsubscribe()
  }, [])

  useEffect(() => {
    let filtered = alerts

    if (filters.severity !== "all") {
      filtered = filtered.filter((alert) => alert.severity === filters.severity)
    }

    if (filters.type !== "all") {
      filtered = filtered.filter((alert) => alert.anomaly_type === filters.type)
    }

    if (filters.resolved !== "all") {
      const isResolved = filters.resolved === "resolved"
      filtered = filtered.filter((alert) => alert.resolved === isResolved)
    }

    if (filters.timeRange !== "all") {
      const now = new Date()
      const timeRanges = {
        "1h": 1 * 60 * 60 * 1000,
        "24h": 24 * 60 * 60 * 1000,
        "7d": 7 * 24 * 60 * 60 * 1000,
        "30d": 30 * 24 * 60 * 60 * 1000,
      }

      const cutoff = new Date(now.getTime() - timeRanges[filters.timeRange as keyof typeof timeRanges])
      filtered = filtered.filter((alert) => alert.timestamp >= cutoff)
    }

    setFilteredAlerts(filtered)
  }, [alerts, filters])

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-blue-400 text-xl animate-pulse">Loading Drishti Dashboard...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="container mx-auto p-6">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-blue-400 mb-2">🔍 Project Drishti</h1>
          <p className="text-slate-400">Real-time Video Anomaly Detection & Security Monitoring System</p>
        </div>

        <StatsCards alerts={alerts} />
        <FilterControls filters={filters} onFiltersChange={setFilters} />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-2">
            <MapView alerts={filteredAlerts} />
          </div>
          <div className="lg:col-span-1">
            <AlertsList alerts={filteredAlerts} />
          </div>
        </div>

       <div className="mb-9 h-[600px]"> 
  <ChatBot alerts={alerts} />
</div>

      </div>
    </div>
  )
}
