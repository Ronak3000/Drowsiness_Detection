export const API_URL = 'https://drowsiness-detection-3-4yld.onrender.com'

export async function analyzeFrame(uri) {
  const form = new FormData()
  form.append('frame', { uri, type: 'image/jpeg', name: 'frame.jpg' })
  const res = await fetch(API_URL, { method: 'POST', body: form })
  return res.json()
}
