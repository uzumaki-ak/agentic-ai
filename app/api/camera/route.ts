import { NextResponse } from 'next/server'
import { exec } from 'child_process'
import path from 'path'

export async function POST(req: Request) {
  const { action } = await req.json()
  
  try {
    const pythonScript = path.join(process.cwd(), 'python', 'detector', 'main.py')
    
    if (action === 'start') {
      exec(`python ${pythonScript} start`, (error) => {
        if (error) console.error(`Error starting detection: ${error.message}`)
      })
      return NextResponse.json({ message: 'Detection started' })
    }
    
    if (action === 'stop') {
      exec(`pkill -f ${pythonScript}`, (error) => {
        if (error) console.error(`Error stopping detection: ${error.message}`)
      })
      return NextResponse.json({ message: 'Detection stopped' })
    }
    
    return NextResponse.json({ error: 'Invalid action' }, { status: 400 })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to control camera' },
      { status: 500 }
    )
  }
}