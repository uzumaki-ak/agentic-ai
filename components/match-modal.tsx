'use client'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import Image from 'next/image'
import { Badge } from '@/components/ui/badge'
import { Alert } from '@/types/alert'


export function MatchModal({ 
  alert,
  open,
  onClose
}: {
  alert: Alert | null
  open: boolean
  onClose: () => void
}) {
  if (!alert) return null

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle>Person Found!</DialogTitle>
          <p className="text-sm text-muted-foreground">
            {alert.name} detected at {alert.location.lat}, {alert.location.lng}
          </p>
        </DialogHeader>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="relative aspect-square rounded-lg overflow-hidden border">
            <Image
              src={alert.snapshotUrl ?? '/placeholder.png'}
              alt={`${alert.name} detected`}
              fill
              className="object-cover"
            />
          </div>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <h3 className="text-xs font-medium text-muted-foreground">Name</h3>
                <p className="font-medium">{alert.name}</p>
              </div>
              <div>
                <h3 className="text-xs font-medium text-muted-foreground">Confidence</h3>
                <p>
                  <Badge variant="outline">{alert.confidence}%</Badge>
                </p>
              </div>
              <div>
                <h3 className="text-xs font-medium text-muted-foreground">Time Detected</h3>
                <p>{new Date(alert.timestamp).toLocaleTimeString()}</p>
              </div>
              <div>
                <h3 className="text-xs font-medium text-muted-foreground">Date</h3>
                <p>{new Date(alert.timestamp).toLocaleDateString()}</p>
              </div>
              <div className="col-span-2">
                <h3 className="text-xs font-medium text-muted-foreground">Location</h3>
                <p>
                  {alert.location.lat}, {alert.location.lng}
                </p>
              </div>
            </div>
            
            {alert.aiDescription && (
              <div className="bg-muted/50 p-4 rounded-lg">
                <h3 className="text-sm font-medium mb-2">AI Analysis</h3>
                <p className="text-sm">{alert.aiDescription}</p>
              </div>
            )}
          </div>
        </div>
        
        <div className="mt-4 h-64 rounded-lg overflow-hidden">
          {/* Map component would go here */}
        </div>
      </DialogContent>
    </Dialog>
  )
}