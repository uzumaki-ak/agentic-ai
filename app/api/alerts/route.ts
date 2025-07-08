import { Alert } from '@/types/alert'
import { NextResponse } from 'next/server'

// In-memory storage for demo (replace with DB in production)
let alerts: Alert[] = []

export async function GET() {
  return NextResponse.json(alerts)
}

export async function POST(req: Request) {
  try {
    const data: Alert = await req.json()
    
    // Add timestamp if not present
    if (!data.timestamp) {
      data.timestamp = new Date()
    }
    
    // Add unique ID if not present
    if (!data.id) {
      data.id = Date.now().toString()
    }
    
    alerts = [data, ...alerts]
    
    console.log('New alert received:', {
      id: data.id,
      timestamp: data.timestamp,
      location: data.location || 'Unknown'
    })
    
    // Keep only last 100 alerts to prevent memory issues
    if (alerts.length > 100) {
      alerts = alerts.slice(0, 100)
    }
    
    return NextResponse.json(data, { status: 201 })
    
  } catch (error) {
    console.error('Alert processing error:', error)
    return NextResponse.json(
      { error: 'Failed to process alert' },
      { status: 500 }
    )
  }
}