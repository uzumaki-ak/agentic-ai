"use client"

import type { Alert } from "@/types/alert"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertTriangle, CheckCircle, Shield, Zap } from "lucide-react"

interface StatsCardsProps {
  alerts: Alert[]
}

export function StatsCards({ alerts }: StatsCardsProps) {
  const activeAlerts = alerts.filter((alert) => !alert.resolved)
  const resolvedAlerts = alerts.filter((alert) => alert.resolved)
  const highSeverityAlerts = alerts.filter((alert) => alert.severity === "high")

  const recentAlerts = alerts.filter((alert) => new Date().getTime() - alert.timestamp.getTime() < 24 * 60 * 60 * 1000)

  const avgConfidence = alerts.length > 0 ? alerts.reduce((sum, alert) => sum + alert.confidence, 0) / alerts.length : 0

  const stats = [
    {
      title: "Active Alerts",
      value: activeAlerts.length,
      icon: AlertTriangle,
      color: activeAlerts.length > 0 ? "text-red-400" : "text-green-400",
      bgColor: activeAlerts.length > 0 ? "bg-red-500/10" : "bg-green-500/10",
      borderColor: activeAlerts.length > 0 ? "border-red-500/20" : "border-green-500/20",
      subtitle: activeAlerts.length > 0 ? "Requires attention" : "All clear",
    },
    {
      title: "Resolved Today",
      value: resolvedAlerts.length,
      icon: CheckCircle,
      color: "text-green-400",
      bgColor: "bg-green-500/10",
      borderColor: "border-green-500/20",
      subtitle: "Successfully handled",
    },
    {
      title: "High Priority",
      value: highSeverityAlerts.length,
      icon: Zap,
      color: highSeverityAlerts.length > 0 ? "text-red-400" : "text-orange-400",
      bgColor: highSeverityAlerts.length > 0 ? "bg-red-500/10" : "bg-orange-500/10",
      borderColor: highSeverityAlerts.length > 0 ? "border-red-500/20" : "border-orange-500/20",
      subtitle: "Critical incidents",
    },
    {
      title: "Detection Rate",
      value: `${(avgConfidence * 100).toFixed(1)}%`,
      icon: Shield,
      color: "text-blue-400",
      bgColor: "bg-blue-500/10",
      borderColor: "border-blue-500/20",
      subtitle: "Average confidence",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      {stats.map((stat, index) => (
        <Card
          key={index}
          className={`bg-slate-900 border-slate-700 ${stat.borderColor} hover:shadow-lg transition-all`}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-400">{stat.title}</CardTitle>
            <div className={`p-2 rounded-lg ${stat.bgColor}`}>
              <stat.icon className={`w-4 h-4 ${stat.color}`} />
            </div>
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${stat.color} mb-1`}>{stat.value}</div>
            <p className="text-xs text-slate-500">{stat.subtitle}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
