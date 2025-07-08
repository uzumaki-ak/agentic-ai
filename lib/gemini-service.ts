import { GEMINI_API_URL } from "./constants"
import { GEMINI_API_KEY } from "./constants"



export async function generatePersonDescription(imageUrl: string): Promise<string> {
  if (!GEMINI_API_KEY) {
    console.warn('Gemini API key not configured')
    return ''
  }

  try {
    const response = await fetch(`${GEMINI_API_URL}/generateContent`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GEMINI_API_KEY}`
      },
      body: JSON.stringify({
        contents: [{
          parts: [{
            text: "Describe this person's appearance including clothing, accessories, and any distinctive features. Be concise and factual."
          }, {
            image: {
              url: imageUrl
            }
          }]
        }],
        generationConfig: {
          maxOutputTokens: 256,
          temperature: 0.4
        }
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error?.message || 'Gemini API error')
    }

    const data = await response.json()
    return data.candidates?.[0]?.content?.parts?.[0]?.text || ''
  } catch (error) {
    console.error('Gemini API error:', error)
    return ''
  }
}