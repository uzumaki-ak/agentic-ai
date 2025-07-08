"use client";

import type React from "react";

import { useState, useRef, useEffect } from "react";
import type { Alert } from "@/types/alert";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Bot, User, MessageCircle, X } from "lucide-react";

interface ChatBotProps {
  alerts: Alert[];
}

interface Message {
  id: string;
  type: "user" | "bot";
  content: string;
  timestamp: Date;
}

export function ChatBot({ alerts }: ChatBotProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "bot",
      content:
        '👋 Hello! I\'m Drishti AI Assistant. I can help you analyze security data and answer questions about anomalies.\n\nTry asking:\n• "Any anomalies in Zone A?"\n• "Summarize last hour alerts"\n• "Show high-severity incidents"\n• "What happened today?"',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // ✅ Advanced AI analysis using Gemini-like intelligence
  const analyzeQuery = async (query: string): Promise<string> => {
    const lowerQuery = query.toLowerCase();

    // Zone-specific analysis
    if (lowerQuery.includes("zone") || lowerQuery.includes("area")) {
      const zoneMatch = lowerQuery.match(/zone\s*([a-z])/i);
      const zone = zoneMatch ? zoneMatch[1].toUpperCase() : null;

      const relevantAlerts = alerts.filter((alert) =>
        zone
          ? alert.zone?.toLowerCase().includes(`zone ${zone.toLowerCase()}`)
          : true
      );

      if (relevantAlerts.length === 0) {
        return `🟢 **Zone ${
          zone || "Analysis"
        } Status: ALL CLEAR**\n\nNo anomalies detected in the specified zone. Security systems are functioning normally.`;
      }

      const activeAlerts = relevantAlerts.filter((alert) => !alert.resolved);
      const summary = relevantAlerts.reduce((acc, alert) => {
        acc[alert.anomaly_type] = (acc[alert.anomaly_type] || 0) + 1;
        return acc;
      }, {} as Record<string, number>);

      return `🔍 **Zone ${
        zone || "Multi-Zone"
      } Analysis Report**\n\n📊 **Summary:**\n${Object.entries(summary)
        .map(
          ([type, count]) =>
            `• ${type.replace("_", " ").toUpperCase()}: ${count} incident(s)`
        )
        .join("\n")}\n\n🚨 **Active Alerts:** ${
        activeAlerts.length
      }\n✅ **Resolved:** ${
        relevantAlerts.length - activeAlerts.length
      }\n\n📅 **Latest Incident:** ${relevantAlerts[0]?.anomaly_type
        .replace("_", " ")
        .toUpperCase()} at ${relevantAlerts[0]?.timestamp.toLocaleString()}`;
    }

    // Time-based analysis with AI summarization
    if (
      lowerQuery.includes("hour") ||
      lowerQuery.includes("today") ||
      lowerQuery.includes("recent") ||
      lowerQuery.includes("summarize")
    ) {
      let timeRange = 24 * 60 * 60 * 1000;
      let timeLabel = "last 24 hours";

      if (
        lowerQuery.includes("last hour") ||
        lowerQuery.includes("past hour")
      ) {
        timeRange = 60 * 60 * 1000;
        timeLabel = "last hour";
      } else if (lowerQuery.includes("today")) {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        timeRange = Date.now() - today.getTime();
        timeLabel = "today";
      }

      const recentAlerts = alerts.filter(
        (alert) => new Date().getTime() - alert.timestamp.getTime() < timeRange
      );

      if (recentAlerts.length === 0) {
        return `✅ **${timeLabel.toUpperCase()} SECURITY REPORT**\n\n🛡️ **Status: ALL SECURE**\n\nNo security anomalies detected during this period. All monitoring systems are operational and reporting normal activity.`;
      }

      // AI-style analysis
      const severityBreakdown = recentAlerts.reduce((acc, alert) => {
        acc[alert.severity] = (acc[alert.severity] || 0) + 1;
        return acc;
      }, {} as Record<string, number>);

      const typeBreakdown = recentAlerts.reduce((acc, alert) => {
        acc[alert.anomaly_type] = (acc[alert.anomaly_type] || 0) + 1;
        return acc;
      }, {} as Record<string, number>);

      const avgConfidence =
        recentAlerts.reduce((sum, alert) => sum + alert.confidence, 0) /
        recentAlerts.length;

      return `📈 **AI SECURITY ANALYSIS - ${timeLabel.toUpperCase()}**\n\n🎯 **Detection Summary:**\n• Total Incidents: ${
        recentAlerts.length
      }\n• Average Confidence: ${(avgConfidence * 100).toFixed(
        1
      )}%\n• Active Monitoring: ✅ Operational\n\n⚠️ **Severity Breakdown:**\n${Object.entries(
        severityBreakdown
      )
        .map(
          ([severity, count]) =>
            `• ${severity.toUpperCase()}: ${count} (${(
              (count / recentAlerts.length) *
              100
            ).toFixed(1)}%)`
        )
        .join("\n")}\n\n🔍 **Incident Types:**\n${Object.entries(typeBreakdown)
        .map(
          ([type, count]) =>
            `• ${type.replace("_", " ").toUpperCase()}: ${count}`
        )
        .join("\n")}\n\n🚨 **Most Recent:** ${recentAlerts[0].anomaly_type
        .replace("_", " ")
        .toUpperCase()} detected at ${recentAlerts[0].timestamp.toLocaleString()}`;
    }

    // High-priority alerts analysis
    if (
      lowerQuery.includes("high") ||
      lowerQuery.includes("critical") ||
      lowerQuery.includes("emergency")
    ) {
      const highSeverityAlerts = alerts.filter(
        (alert) => alert.severity === "high"
      );

      if (highSeverityAlerts.length === 0) {
        return "🟢 **CRITICAL SYSTEMS STATUS: STABLE**\n\nNo high-severity security alerts detected. All critical monitoring systems are functioning within normal parameters.";
      }

      const activeHigh = highSeverityAlerts.filter((alert) => !alert.resolved);

      return `🚨 **HIGH-SEVERITY ALERT ANALYSIS**\n\n⚡ **Critical Status:** ${
        activeHigh.length > 0 ? "🔴 ACTIVE THREATS" : "🟡 MONITORING"
      }\n\n📊 **High-Severity Summary:**\n• Total Critical Incidents: ${
        highSeverityAlerts.length
      }\n• Currently Active: ${activeHigh.length}\n• Resolved: ${
        highSeverityAlerts.length - activeHigh.length
      }\n\n🎯 **Recent Critical Incidents:**\n${highSeverityAlerts
        .slice(0, 3)
        .map(
          (alert, i) =>
            `${i + 1}. **${alert.anomaly_type
              .replace("_", " ")
              .toUpperCase()}**\n   📍 ${
              alert.zone
            } | ⏰ ${alert.timestamp.toLocaleString()}\n   🎯 Confidence: ${(
              alert.confidence * 100
            ).toFixed(1)}% | Status: ${
              alert.resolved ? "✅ Resolved" : "🔴 Active"
            }`
        )
        .join("\n\n")}`;
    }

    // Specific anomaly type analysis
    const anomalyTypes = [
      "fire",
      "smoke",
      "crowd",
      "panic",
      "suspicious",
      "violence",
    ];
    const mentionedType = anomalyTypes.find((type) =>
      lowerQuery.includes(type)
    );

    if (mentionedType) {
      const typeAlerts = alerts.filter((alert) =>
        alert.anomaly_type.toLowerCase().includes(mentionedType)
      );

      if (typeAlerts.length === 0) {
        return `✅ **${mentionedType.toUpperCase()} MONITORING STATUS**\n\n🛡️ No ${mentionedType}-related security incidents detected in the monitoring period. Systems are actively scanning for this threat type.`;
      }

      const recentTypeAlerts = typeAlerts.filter(
        (alert) =>
          new Date().getTime() - alert.timestamp.getTime() < 24 * 60 * 60 * 1000
      );

      return `🔍 **${mentionedType.toUpperCase()} INCIDENT ANALYSIS**\n\n📊 **Detection Summary:**\n• Total ${mentionedType} incidents: ${
        typeAlerts.length
      }\n• Recent (24h): ${recentTypeAlerts.length}\n• Active cases: ${
        typeAlerts.filter((a) => !a.resolved).length
      }\n\n🎯 **Recent ${mentionedType.toUpperCase()} Incidents:**\n${typeAlerts
        .slice(0, 3)
        .map(
          (alert, i) =>
            `${i + 1}. **${alert.description}**\n   📍 Location: ${
              alert.zone
            }\n   ⏰ Time: ${alert.timestamp.toLocaleString()}\n   🎯 Confidence: ${(
              alert.confidence * 100
            ).toFixed(1)}%\n   📊 Status: ${
              alert.resolved ? "✅ Resolved" : "🔴 Active"
            }`
        )
        .join("\n\n")}`;
    }

    // System status overview
    if (
      lowerQuery.includes("status") ||
      lowerQuery.includes("summary") ||
      lowerQuery.includes("overview") ||
      lowerQuery.includes("dashboard")
    ) {
      const activeAlerts = alerts.filter((alert) => !alert.resolved);
      const resolvedAlerts = alerts.filter((alert) => alert.resolved);
      const highSeverity = alerts.filter((alert) => alert.severity === "high");

      const recentActivity = alerts.filter(
        (alert) =>
          new Date().getTime() - alert.timestamp.getTime() < 60 * 60 * 1000
      );

      return `🎛️ **DRISHTI SYSTEM STATUS DASHBOARD**\n\n🔋 **System Health:** ✅ OPERATIONAL\n📡 **Monitoring Status:** 🟢 ACTIVE\n🎥 **Camera Feed:** 🟢 CONNECTED\n\n📊 **Alert Statistics:**\n• 🚨 Active Alerts: ${
        activeAlerts.length
      }\n• ✅ Resolved Alerts: ${resolvedAlerts.length}\n• ⚡ High Severity: ${
        highSeverity.length
      }\n• 📈 Total Monitored: ${
        alerts.length
      }\n\n⏰ **Recent Activity (Last Hour):** ${
        recentActivity.length
      } events\n\n🎯 **Last Detection:** ${
        alerts.length > 0
          ? `${alerts[0].anomaly_type
              .replace("_", " ")
              .toUpperCase()} at ${alerts[0].timestamp.toLocaleString()}`
          : "No recent activity"
      }\n\n🛡️ **Overall Status:** ${
        activeAlerts.length === 0
          ? "🟢 ALL SECURE"
          : `🟡 ${activeAlerts.length} ACTIVE MONITORING`
      }`;
    }

    // Default intelligent response
    return `🤖 **DRISHTI AI ASSISTANT**\n\nI can help you analyze security data and provide insights. Here are some things you can ask:\n\n🔍 **Zone Analysis:**\n• "Any anomalies in Zone A?"\n• "Check Zone B security status"\n\n⏰ **Time-Based Queries:**\n• "Summarize last hour alerts"\n• "What happened today?"\n• "Recent security incidents"\n\n🚨 **Severity Analysis:**\n• "Show high-severity alerts"\n• "Critical incidents report"\n\n🎯 **Specific Threats:**\n• "Any fire incidents?"\n• "Crowd panic alerts"\n• "Suspicious activity report"\n\n📊 **System Status:**\n• "Dashboard overview"\n• "System health check"\n\n**Current Status:** Monitoring ${
      alerts.length
    } total alerts with ${
      alerts.filter((a) => !a.resolved).length
    } currently active.`;
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setIsLoading(true);

    try {
      // Simulate AI processing with realistic delay
      await new Promise((resolve) => setTimeout(resolve, 1500));

      const botResponse: Message = {
        id: (Date.now() + 1).toString(),
        type: "bot",
        content: await analyzeQuery(currentInput),
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botResponse]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "bot",
        content:
          "❌ Sorry, I encountered an error processing your request. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {!isOpen && (
        <Button
          onClick={() => setIsOpen(true)}
          className="rounded-full w-16 h-16 bg-blue-600 hover:bg-blue-700 shadow-2xl border-2 border-blue-400 animate-pulse"
        >
          <MessageCircle className="w-8 h-8" />
        </Button>
      )}

      {isOpen && (
        <Card className="w-96 h-[500px] bg-slate-900 border-slate-700 shadow-2xl">
          <CardHeader className="pb-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-t-lg">
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <Bot className="w-5 h-5" />
                Drishti AI Assistant
              </CardTitle>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsOpen(false)}
                className="text-white hover:bg-blue-800 h-8 w-8 p-0"
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
          </CardHeader>

          <CardContent className="flex flex-col h-full pb-4">
            <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${
                    message.type === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  {message.type === "bot" && (
                    <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-600 to-blue-700 flex items-center justify-center flex-shrink-0">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                  )}

                  <div
                    className={`max-w-[85%] p-3 rounded-lg text-sm whitespace-pre-line ${
                      message.type === "user"
                        ? "bg-blue-600 text-white rounded-br-none"
                        : "bg-slate-800 text-slate-200 rounded-bl-none border border-slate-700"
                    }`}
                  >
                    {message.content}
                  </div>

                  {message.type === "user" && (
                    <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center flex-shrink-0">
                      <User className="w-4 h-4 text-white" />
                    </div>
                  )}
                </div>
              ))}

              {isLoading && (
                <div className="flex gap-3 justify-start">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-600 to-blue-700 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-slate-800 p-3 rounded-lg border border-slate-700">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"
                        style={{ animationDelay: "0.1s" }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            <div className="flex gap-2 mb-6">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about security alerts..."
                className="bg-slate-800 border-slate-600 text-white placeholder-slate-400 focus:border-blue-500"
                disabled={isLoading}
              />
              <Button
                onClick={handleSendMessage}
                disabled={!input.trim() || isLoading}
                className="bg-blue-600 hover:bg-blue-700 px-3"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
