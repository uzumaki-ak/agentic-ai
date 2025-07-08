import { Badge } from '@/components/ui/badge'
import { Loader2 } from 'lucide-react'

export function StatusBadge({ status }: { status: string }) {
  return (
    <Badge 
      variant={status === 'searching' ? 'default' : 'destructive'}
      className="px-3 py-1 text-sm font-medium"
    >
      {status === 'searching' ? (
        <div className="flex items-center">
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Active Search
        </div>
      ) : status === 'found' ? (
        'Match Found!'
      ) : (
        'Idle'
      )}
    </Badge>
  )
}