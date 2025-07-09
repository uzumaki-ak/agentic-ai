// import { SearchIcon } from "lucide-react";
// import { Button } from "./ui/button";
// import { Input } from "./ui/input";
// import { Label } from "./ui/label";

// export default function UploadForm() {
//   return (
//     <div className="border rounded-lg p-6">
//       <h2 className="text-xl font-bold mb-4">Report Missing Person</h2>
//       <form action="/api/upload" method="POST" encType="multipart/form-data">
//         <div className="mb-4">
//           <Label>Full Name</Label>
//           <Input name="name" required />
//         </div>
        
//         <div className="mb-4">
//           <Label>Primary Photo (Front-facing)</Label>
//           <Input 
//             type="file" 
//             name="primaryPhoto" 
//             accept="image/*" 
//             required
//           />
//         </div>
        
//         <div className="grid grid-cols-2 gap-4 mb-4">
//           <div>
//             <Label>Additional Photo (Profile)</Label>
//             <Input type="file" name="profilePhoto" accept="image/*" />
//           </div>
//           <div>
//             <Label>Alternative Appearance</Label>
//             <Input type="file" name="altPhoto" accept="image/*" />
//           </div>
//         </div>
        
//         <div className="mb-4">
//           <Label>Last Known Location</Label>
//           <Input name="lastLocation" placeholder="Near main entrance" />
//         </div>
        
//         <Button type="submit" className="w-full">
//           <SearchIcon className="mr-2" />
//           Start Search
//         </Button>
//       </form>
//     </div>
//   )
// }


// firebase 



"use client"

import type React from "react"

import { useState } from "react"
import { SearchIcon, Loader2 } from "lucide-react"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Label } from "./ui/label"
import { useToast } from "@/hooks/use-toast"

export default function UploadForm() {
  const [isUploading, setIsUploading] = useState(false)
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsUploading(true)

    try {
      const formData = new FormData(e.currentTarget)

      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      })

      const result = await response.json()

      if (response.ok) {
        toast({
          title: "Success!",
          description: "Missing person report submitted. Detection started.",
        })

        // Reset form
        e.currentTarget.reset()

        // Broadcast status update
        await fetch("/api/stream/broadcast", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            type: "STATUS_UPDATE",
            status: "searching",
          }),
        })
      } else {
        throw new Error(result.error || "Upload failed")
      }
    } catch (error) {
      console.error("Upload error:", error)
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to submit report",
        variant: "destructive",
      })
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="border rounded-lg p-6">
      <h2 className="text-xl font-bold mb-4">Report Missing Person</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <Label htmlFor="name">Full Name</Label>
          <Input id="name" name="name" required disabled={isUploading} placeholder="Enter full name" />
        </div>

        <div className="mb-4">
          <Label htmlFor="primaryPhoto">Primary Photo (Front-facing)</Label>
          <Input id="primaryPhoto" type="file" name="primaryPhoto" accept="image/*" required disabled={isUploading} />
          <p className="text-xs text-muted-foreground mt-1">Clear, front-facing photo works best</p>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <Label htmlFor="profilePhoto">Additional Photo (Profile)</Label>
            <Input id="profilePhoto" type="file" name="profilePhoto" accept="image/*" disabled={isUploading} />
          </div>
          <div>
            <Label htmlFor="altPhoto">Alternative Appearance</Label>
            <Input id="altPhoto" type="file" name="altPhoto" accept="image/*" disabled={isUploading} />
          </div>
        </div>

        <div className="mb-4">
          <Label htmlFor="lastLocation">Last Known Location</Label>
          <Input id="lastLocation" name="lastLocation" placeholder="Near main entrance" disabled={isUploading} />
        </div>

        <Button type="submit" className="w-full" disabled={isUploading}>
          {isUploading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <SearchIcon className="mr-2" />
              Start Search
            </>
          )}
        </Button>
      </form>
    </div>
  )
}
