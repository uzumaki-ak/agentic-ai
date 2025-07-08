import { useEffect, useState } from 'react'

export function useSSE(url: string, options: { onMessage: (event: MessageEvent) => void }) {
  const [status, setStatus] = useState<'connecting' | 'open' | 'closed'>('connecting')
  
  useEffect(() => {
    const eventSource = new EventSource(url)
    
    eventSource.onopen = () => setStatus('open')
    eventSource.onerror = () => setStatus('closed')
    eventSource.onmessage = options.onMessage
    
    return () => {
      eventSource.close()
      setStatus('closed')
    }
  }, [url, options.onMessage])
  
  return { status }
}