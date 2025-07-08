import { SearchIcon } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";

export default function UploadForm() {
  return (
    <div className="border rounded-lg p-6">
      <h2 className="text-xl font-bold mb-4">Report Missing Person</h2>
      <form action="/api/upload" method="POST" encType="multipart/form-data">
        <div className="mb-4">
          <Label>Full Name</Label>
          <Input name="name" required />
        </div>
        
        <div className="mb-4">
          <Label>Primary Photo (Front-facing)</Label>
          <Input 
            type="file" 
            name="primaryPhoto" 
            accept="image/*" 
            required
          />
        </div>
        
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <Label>Additional Photo (Profile)</Label>
            <Input type="file" name="profilePhoto" accept="image/*" />
          </div>
          <div>
            <Label>Alternative Appearance</Label>
            <Input type="file" name="altPhoto" accept="image/*" />
          </div>
        </div>
        
        <div className="mb-4">
          <Label>Last Known Location</Label>
          <Input name="lastLocation" placeholder="Near main entrance" />
        </div>
        
        <Button type="submit" className="w-full">
          <SearchIcon className="mr-2" />
          Start Search
        </Button>
      </form>
    </div>
  )
}