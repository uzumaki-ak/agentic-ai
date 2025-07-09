// import { useEffect, useState } from 'react'

// export function useSSE(url: string, options: { onMessage: (event: MessageEvent) => void }) {
//   const [status, setStatus] = useState<'connecting' | 'open' | 'closed'>('connecting')
  
//   useEffect(() => {
//     const eventSource = new EventSource(url)
    
//     eventSource.onopen = () => setStatus('open')
//     eventSource.onerror = () => setStatus('closed')
//     eventSource.onmessage = options.onMessage
    
//     return () => {
//       eventSource.close()
//       setStatus('closed')
//     }
//   }, [url, options.onMessage])
  
//   return { status }
// }


// firebae 



"use client"

import { useEffect, useRef, useState } from "react"

interface UseSSEOptions {
  onMessage?: (event: MessageEvent) => void
  onError?: (error: Event) => void
  onOpen?: (event: Event) => void
}

export function useSSE(url: string, options: UseSSEOptions = {}) {
  const eventSourceRef = useRef<EventSource | null>(null)
  const [status, setStatus] = useState<'connecting' | 'open' | 'closed'>('connecting')

  useEffect(() => {
    if (typeof window === "undefined") return

    const eventSource = new EventSource(url)
    eventSourceRef.current = eventSource
    setStatus('connecting')

    eventSource.onopen = (event) => {
      console.log("SSE connection opened")
      setStatus('open')
      options.onOpen?.(event)
    }

    eventSource.onmessage = (event) => {
      try {
        options.onMessage?.(event)
      } catch (error) {
        console.error("SSE message processing error:", error)
      }
    }

    eventSource.onerror = (error) => {
      console.error("SSE error:", error)
      setStatus('closed')
      options.onError?.(error)
    }

    return () => {
      eventSource.close()
      eventSourceRef.current = null
      setStatus('closed')
    }
  }, [url])

  return {
    status,
    close: () => {
      eventSourceRef.current?.close()
      eventSourceRef.current = null
      setStatus('closed')
    },
  }
}
