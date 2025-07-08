// import { NextRequest } from 'next/server'

// // Store connected clients
// const clients = new Set<{ id: number; controller: ReadableStreamDefaultController }>()
// let clientId = 0

// export async function GET(req: NextRequest) {
//   const stream = new ReadableStream({
//     start(controller) {
//       const id = ++clientId
//       clients.add({ id, controller })
      
//       // Send initial message to keep connection open
//       controller.enqueue(`id: ${id}\n`)
//       controller.enqueue(`event: connected\n`)
//       controller.enqueue(`data: ${JSON.stringify({ type: 'CONNECTED', id })}\n\n`)
      
//       // Handle client disconnect
//       req.signal.onabort = () => {
//         clients.delete({ id, controller })
//         controller.close()
//       }
//     }
//   })

//   return new Response(stream, {
//     headers: {
//       'Content-Type': 'text/event-stream',
//       'Connection': 'keep-alive',
//       'Cache-Control': 'no-cache, no-transform',
//     },
//   })
// }

// // Function to broadcast to all clients
// export function broadcast(data: object) {
//   const message = `data: ${JSON.stringify(data)}\n\n`
//   clients.forEach(({ controller }) => {
//     try {
//       controller.enqueue(message)
//     } catch (error) {
//       console.error('Failed to send SSE:', error)
//     }
//   })
// }



import { NextRequest } from 'next/server'

const clients = new Set<{ id: number; controller: ReadableStreamDefaultController }>()
let clientId = 0

export async function GET(req: NextRequest) {
  const stream = new ReadableStream({
    start(controller) {
      const id = ++clientId
      clients.add({ id, controller })
      
      // Send heartbeat every 25 seconds to keep connection alive
      const heartbeat = setInterval(() => {
        controller.enqueue(`: heartbeat\n\n`)
      }, 25000)

      req.signal.onabort = () => {
        clearInterval(heartbeat)
        clients.delete({ id, controller })
        controller.close()
      }
    }
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Connection': 'keep-alive',
      'Cache-Control': 'no-cache, no-transform',
    },
  })
}

export function broadcast(data: object) {
  const message = `data: ${JSON.stringify(data)}\n\n`
  clients.forEach(({ controller }) => {
    try {
      controller.enqueue(message)
    } catch (error) {
      console.error('SSE send error:', error)
    }
  })
}