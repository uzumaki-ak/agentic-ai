'use client'
import { useState, useEffect } from 'react'
import UploadForm from '@/components/upload-form'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useSSE } from '@/hooks/use-sse'
import { Alert } from '@/types/alert'
import { StatusBadge } from '@/components/status-badge'
import { AlertsList } from '@/components/alerts-list'
import { MapView } from '@/components/map-view'
import { LiveFeedView } from '@/components/live-feed'
import { MatchModal } from '@/components/match-modal'

export default function DashboardPage() {
  const [status, setStatus] = useState<'idle' | 'searching' | 'found'>('idle')
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  // Real-time alert streaming
  useSSE('/api/stream', {
    onMessage: (event) => {
      const data = JSON.parse(event.data)
      
      if (data.type === 'STATUS_UPDATE') {
        setStatus(data.status)
      }
      
      if (data.type === 'NEW_ALERT') {
        setAlerts(prev => [data.alert, ...prev])
        setStatus('found')
        setIsModalOpen(true)
        setSelectedAlert(data.alert)
        
        // Play notification sound
        new Audio('/sounds/alert.mp3').play().catch(console.error)
      }
    }
  })

  // Load initial alerts
  useEffect(() => {
    const fetchAlerts = async () => {
      const response = await fetch('/api/alerts')
      const data = await response.json()
      setAlerts(data)
    }
    fetchAlerts()
  }, [])

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Drishti - Lost Person Finder</h1>
        <StatusBadge status={status} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column */}
        <div className="lg:col-span-1 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Report Missing Person</CardTitle>
            </CardHeader>
            <CardContent>
              <UploadForm />
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Recent Alerts</CardTitle>
            </CardHeader>
            <CardContent>
              <AlertsList 
                alerts={alerts} 
                onSelect={(alert) => {
                  setSelectedAlert(alert)
                  setIsModalOpen(true)
                }} 
              />
            </CardContent>
          </Card>
        </div>
        
        {/* Right Column */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Detection Map</CardTitle>
            </CardHeader>
            <CardContent className="p-0 h-[500px]">
              <MapView alerts={alerts} />
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle>Live Camera Feed</CardTitle>
                <Button variant="outline" size="sm">
                  Switch Camera
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <LiveFeedView />
            </CardContent>
          </Card>
        </div>
      </div>
      
      <MatchModal 
        alert={selectedAlert} 
        open={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
      />
    </div>
  )
}