import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

import { Button } from '@/components/ui/button'
import { format } from 'date-fns'
import { Alert } from '@/types/alert'

interface DetectionAlertProps {
  alert: Alert
  onSelect: (alert: Alert) => void
}

export function DetectionAlert({ alert, onSelect }: DetectionAlertProps) {
  return (
    <Card className="hover:shadow-md transition-shadow cursor-pointer">
      <CardHeader className="flex flex-row items-center justify-between p-4">
        <CardTitle className="text-sm font-medium">{alert.name}</CardTitle>
        <span className="text-xs text-muted-foreground">
          {format(new Date(alert.timestamp), 'HH:mm:ss')}
        </span>
      </CardHeader>
      <CardContent className="p-4 pt-0">
        <div className="flex justify-between items-center">
          <div>
            <p className="text-xs text-muted-foreground">
              {`Lat: ${alert.location.lat}, Lng: ${alert.location.lng}`}
            </p>
            <div className="flex items-center mt-1">
              <span className="text-xs mr-2">Confidence:</span>
              <span className="text-xs font-medium text-primary">
                {alert.confidence}%
              </span>
            </div>
          </div>
          <Button 
            variant="outline" 
            size="sm"
            onClick={() => onSelect(alert)}
          >
            View
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}