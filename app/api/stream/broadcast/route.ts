import { NextRequest } from 'next/server'
import { broadcast } from '../route'

export async function POST(req: NextRequest) {
  try {
    const data = await req.json()
    broadcast(data)
    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: 'Broadcast failed' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}