'use client'

import { useState } from 'react'
import { PreferencesLayout } from '../../components/preferences-layout'
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { useRouter } from 'next/navigation'

const technologies = [
  "Web Development", "Mobile Development", "API Development", "Cloud Computing",
  "DevOps", "Machine Learning", "Data Science", "Blockchain",
  "Internet of Things (IoT)", "Cybersecurity", "Game Development GD", "AR/VR Development"
]

export default function TechnologyPreferences() {
  const [selectedTech, setSelectedTech] = useState<string[]>([])
  const router = useRouter()

  const handleTechChange = (tech: string) => {
    setSelectedTech(prev => 
      prev.includes(tech) ? prev.filter(t => t !== tech) : [...prev, tech]
    )
  }

  const handleNext = () => {
    // Here you would typically save the preferences
    console.log("Selected technologies:", selectedTech)
    router.push('/preferences/language')
  }

  const handleBack = () => {
    router.back()
  }

  return (
    <PreferencesLayout currentStep={1} totalSteps={3}>
      <div className="space-y-6">
        <h3 className="text-xl font-semibold text-foreground">Select Your Technology Skills</h3>
        <div className="grid grid-cols-2 gap-4">
          {technologies.map(tech => (
            <div key={tech} className="flex items-center space-x-2">
              <Checkbox 
                id={tech} 
                checked={selectedTech.includes(tech)}
                onCheckedChange={() => handleTechChange(tech)}
              />
              <label htmlFor={tech} className="text-sm font-medium text-muted-foreground leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                {tech}
              </label>
            </div>
          ))}
        </div>
        <div className="flex justify-between">
          <Button onClick={handleBack} variant="outline" className="border-border text-muted-foreground hover:bg-secondary">Back</Button>
          <Button onClick={handleNext} className="bg-primary text-primary-foreground hover:bg-primary/90">Next</Button>
        </div>
      </div>
    </PreferencesLayout>
  )
}

