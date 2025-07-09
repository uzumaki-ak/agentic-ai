// "use client"

// import { useState } from "react"
// import { doc, updateDoc } from "firebase/firestore"
// import { db } from "@/lib/firebase"
// import type { Alert } from "@/types/alert"
// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
// import { Button } from "@/components/ui/button"
// import { Badge } from "@/components/ui/badge"
// import { CheckCircle, ExternalLink, AlertTriangle, Flame, Users, Eye, Shield, Zap } from "lucide-react"


// export interface AlertsListProps {
//   alerts: Alert[]
//   onSelect?: (alert: Alert) => void
// }

// export function AlertsList({ alerts,onSelect }: AlertsListProps) {
//   const [resolvingAlerts, setResolvingAlerts] = useState<Set<string>>(new Set())

//   const handleResolveAlert = async (alertId: string) => {
//     setResolvingAlerts((prev) => new Set(prev).add(alertId))

//     try {
//       await updateDoc(doc(db, "alerts", alertId), {
//         resolved: true,
//         resolvedAt: new Date(),
//       })
//     } catch (error) {
//       console.error("Error resolving alert:", error)
//     } finally {
//       setResolvingAlerts((prev) => {
//         const newSet = new Set(prev)
//         newSet.delete(alertId)
//         return newSet
//       })
//     }
//   }

//   const getAnomalyIcon = (type: string) => {
//     switch (type) {
//       case "fire":
//         return <Flame className="w-4 h-4 text-red-400" />
//       case "smoke":
//         return <AlertTriangle className="w-4 h-4 text-yellow-400" />
//       case "crowd_panic":
//         return <Users className="w-4 h-4 text-orange-400" />
//       case "suspicious_activity":
//         return <Eye className="w-4 h-4 text-purple-400" />
//       case "violence":
//         return <Zap className="w-4 h-4 text-red-500" />
//       default:
//         return <Shield className="w-4 h-4 text-blue-400" />
//     }
//   }

//   const getSeverityColor = (severity: string) => {
//     switch (severity) {
//       case "low":
//         return "bg-green-500/20 text-green-400 border-green-500/30"
//       case "medium":
//         return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
//       case "high":
//         return "bg-red-500/20 text-red-400 border-red-500/30"
//       default:
//         return "bg-gray-500/20 text-gray-400 border-gray-500/30"
//     }
//   }

//   const getTimeAgo = (timestamp: Date) => {
//     const now = new Date()
//     const diff = now.getTime() - timestamp.getTime()
//     const minutes = Math.floor(diff / 60000)
//     const hours = Math.floor(diff / 3600000)
//     const days = Math.floor(diff / 86400000)

//     if (days > 0) return `${days}d ago`
//     if (hours > 0) return `${hours}h ago`
//     if (minutes > 0) return `${minutes}m ago`
//     return "Just now"
//   }

//   return (
//     <Card className="bg-slate-900 border-slate-700">
//       <CardHeader>
//         <CardTitle className="text-blue-400 flex items-center gap-2">
//           🚨 Recent Alerts
//           <Badge variant="secondary" className="bg-blue-500/20 text-blue-400 border-blue-500/30">
//             {alerts.filter((a) => !a.resolved).length} Active
//           </Badge>
//         </CardTitle>
//       </CardHeader>
//       <CardContent>
//         <div className="space-y-3 max-h-96 overflow-y-auto">
//           {alerts.length === 0 ? (
//             <div className="text-center py-8 text-slate-400">
//               <CheckCircle className="w-12 h-12 mx-auto mb-3 opacity-50" />
//               <p className="font-medium">No alerts detected</p>
//               <p className="text-sm">System is monitoring...</p>
//             </div>
//           ) : (
//             alerts.map((alert) => (
//               <div
//                 key={alert.id}
//                  onClick={() => onSelect && onSelect(alert)}
//           style={{ cursor: onSelect ? 'pointer' : 'default' }}
//                 className={`p-4 rounded-lg border transition-all hover:shadow-lg ${
//                   alert.resolved
//                     ? "bg-slate-800/50 border-slate-600 opacity-70"
//                     : "bg-slate-800 border-slate-600 hover:border-slate-500 hover:bg-slate-750"
//                 }`}
//               >
//                 <div className="flex items-start justify-between mb-3">
//                   <div className="flex items-center gap-3">
//                     {getAnomalyIcon(alert.anomaly_type)}
//                     <div>
//                       <h3 className="font-semibold text-white text-sm">
//                         {alert.anomaly_type.replace("_", " ").toUpperCase()}
//                       </h3>
//                       <p className="text-xs text-slate-400">
//                         📍 {alert.zone} • ⏰ {getTimeAgo(alert.timestamp)}
//                       </p>
//                     </div>
//                   </div>
//                   <div className="flex items-center gap-2">
//                     <Badge className={getSeverityColor(alert.severity)}>{alert.severity}</Badge>
//                     {alert.resolved && <CheckCircle className="w-4 h-4 text-green-400" />}
//                   </div>
//                 </div>

//                 <p className="text-sm text-slate-300 mb-3 leading-relaxed">{alert.description}</p>

//                 <div className="flex items-center justify-between text-xs text-slate-400 mb-3">
//                   <span className="flex items-center gap-1">
//                     🎯 Confidence:{" "}
//                     <span className="text-blue-400 font-medium">{(alert.confidence * 100).toFixed(1)}%</span>
//                   </span>
//                   <span>{alert.timestamp.toLocaleString()}</span>
//                 </div>

//                 <div className="flex items-center gap-2">
//                   {alert.snapshot_url && (
//                     <Button
//                       size="sm"
//                       variant="outline"
//                       className="text-xs border-slate-600 hover:border-slate-500 hover:bg-slate-700 bg-transparent"
//                       onClick={() => window.open(alert.snapshot_url, "_blank")}
//                     >
//                       <ExternalLink className="w-3 h-3 mr-1" />
//                       View Image
//                     </Button>
//                   )}

//                   {!alert.resolved && (
//                     <Button
//                       size="sm"
//                       variant="outline"
//                       className="text-xs border-green-600 hover:border-green-500 text-green-400 hover:bg-green-500/10 bg-transparent"
//                       onClick={() => handleResolveAlert(alert.id)}
//                       disabled={resolvingAlerts.has(alert.id)}
//                     >
//                       <CheckCircle className="w-3 h-3 mr-1" />
//                       {resolvingAlerts.has(alert.id) ? "Resolving..." : "Resolve"}
//                     </Button>
//                   )}
//                 </div>
//               </div>
//             ))
//           )}
//         </div>
//       </CardContent>
//     </Card>
//   )
// }




// firebase \\\


"use client"

import { useState } from "react"
import { doc, updateDoc } from "firebase/firestore"
import { db } from "@/lib/firebase"
import type { Alert } from "@/types/alert"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { CheckCircle, ExternalLink, AlertTriangle, Flame, Users, Eye, Shield, Zap, User } from "lucide-react"

export interface AlertsListProps {
  alerts: Alert[]
  onSelect?: (alert: Alert) => void
}

export function AlertsList({ alerts, onSelect }: AlertsListProps) {
  const [resolvingAlerts, setResolvingAlerts] = useState<Set<string>>(new Set())

  const handleResolveAlert = async (alertId: string) => {
    setResolvingAlerts((prev) => new Set(prev).add(alertId))
    try {
      await updateDoc(doc(db, "alerts", alertId), {
        resolved: true,
        resolvedAt: new Date(),
      })
    } catch (error) {
      console.error("Error resolving alert:", error)
    } finally {
      setResolvingAlerts((prev) => {
        const newSet = new Set(prev)
        newSet.delete(alertId)
        return newSet
      })
    }
  }

  const getAnomalyIcon = (type: string) => {
    switch (type) {
      case "person_found":
        return <User className="w-4 h-4 text-green-400" />
      case "fire":
        return <Flame className="w-4 h-4 text-red-400" />
      case "smoke":
        return <AlertTriangle className="w-4 h-4 text-yellow-400" />
      case "crowd_panic":
        return <Users className="w-4 h-4 text-orange-400" />
      case "suspicious_activity":
        return <Eye className="w-4 h-4 text-purple-400" />
      case "violence":
        return <Zap className="w-4 h-4 text-red-500" />
      default:
        return <Shield className="w-4 h-4 text-blue-400" />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "low":
        return "bg-green-500/20 text-green-400 border-green-500/30"
      case "medium":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
      case "high":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30"
    }
  }

  const getTimeAgo = (timestamp: Date | any) => {
    try {
      // Convert Firebase Timestamp to Date if needed
      let date: Date
      if (timestamp && typeof timestamp.toDate === "function") {
        // Firebase Timestamp
        date = timestamp.toDate()
      } else if (timestamp instanceof Date) {
        // Already a Date object
        date = timestamp
      } else if (typeof timestamp === "string") {
        // String timestamp
        date = new Date(timestamp)
      } else {
        // Fallback
        return "Unknown"
      }

      const now = new Date()
      const diff = now.getTime() - date.getTime()
      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(diff / 3600000)
      const days = Math.floor(diff / 86400000)

      if (days > 0) return `${days}d ago`
      if (hours > 0) return `${hours}h ago`
      if (minutes > 0) return `${minutes}m ago`
      return "Just now"
    } catch (error) {
      console.error("Error formatting time:", error)
      return "Unknown"
    }
  }

  const formatTimestamp = (timestamp: Date | any) => {
    try {
      // Convert Firebase Timestamp to Date if needed
      let date: Date
      if (timestamp && typeof timestamp.toDate === "function") {
        // Firebase Timestamp
        date = timestamp.toDate()
      } else if (timestamp instanceof Date) {
        // Already a Date object
        date = timestamp
      } else if (typeof timestamp === "string") {
        // String timestamp
        date = new Date(timestamp)
      } else {
        // Fallback
        return "Unknown time"
      }

      return date.toLocaleString()
    } catch (error) {
      console.error("Error formatting timestamp:", error)
      return "Unknown time"
    }
  }

  return (
    <Card className="bg-slate-900 border-slate-700">
      <CardHeader>
        <CardTitle className="text-blue-400 flex items-center gap-2">
          🚨 Recent Alerts
          <Badge variant="secondary" className="bg-blue-500/20 text-blue-400 border-blue-500/30">
            {alerts.filter((a) => !a.resolved).length} Active
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {alerts.length === 0 ? (
            <div className="text-center py-8 text-slate-400">
              <CheckCircle className="w-12 h-12 mx-auto mb-3 opacity-50" />
              <p className="font-medium">No alerts detected</p>
              <p className="text-sm">System is monitoring...</p>
            </div>
          ) : (
            alerts.map((alert) => (
              <div
                key={alert.id}
                onClick={() => onSelect && onSelect(alert)}
                style={{ cursor: onSelect ? "pointer" : "default" }}
                className={`p-4 rounded-lg border transition-all hover:shadow-lg ${
                  alert.resolved
                    ? "bg-slate-800/50 border-slate-600 opacity-70"
                    : "bg-slate-800 border-slate-600 hover:border-slate-500 hover:bg-slate-750"
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    {getAnomalyIcon(alert.anomaly_type)}
                    <div>
                      <h3 className="font-semibold text-white text-sm">
                        {alert.name || alert.anomaly_type.replace("_", " ").toUpperCase()}
                      </h3>
                      <p className="text-xs text-slate-400">
                        📍 {alert.zone} • ⏰ {getTimeAgo(alert.timestamp)}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge className={getSeverityColor(alert.severity)}>{alert.severity}</Badge>
                    {alert.resolved && <CheckCircle className="w-4 h-4 text-green-400" />}
                  </div>
                </div>

                <p className="text-sm text-slate-300 mb-3 leading-relaxed">{alert.description}</p>

                <div className="flex items-center justify-between text-xs text-slate-400 mb-3">
                  <span className="flex items-center gap-1">
                    🎯 Confidence: <span className="text-blue-400 font-medium">{alert.confidence}%</span>
                  </span>
                  <span>{formatTimestamp(alert.timestamp)}</span>
                </div>

                <div className="flex items-center gap-2">
                  {(alert.snapshotUrl || alert.snapshot_url) && (
                    <Button
                      size="sm"
                      variant="outline"
                      className="text-xs border-slate-600 hover:border-slate-500 hover:bg-slate-700 bg-transparent"
                      onClick={(e) => {
                        e.stopPropagation()
                        window.open(alert.snapshotUrl || alert.snapshot_url, "_blank")
                      }}
                    >
                      <ExternalLink className="w-3 h-3 mr-1" />
                      View Image
                    </Button>
                  )}
                  {!alert.resolved && (
                    <Button
                      size="sm"
                      variant="outline"
                      className="text-xs border-green-600 hover:border-green-500 text-green-400 hover:bg-green-500/10 bg-transparent"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleResolveAlert(alert.id)
                      }}
                      disabled={resolvingAlerts.has(alert.id)}
                    >
                      <CheckCircle className="w-3 h-3 mr-1" />
                      {resolvingAlerts.has(alert.id) ? "Resolving..." : "Resolve"}
                    </Button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  )
}
