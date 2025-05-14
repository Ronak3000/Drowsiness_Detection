export const API_URL='https://drowsiness-detection-9l65.onrender.com'
export async function analyzeFrame(data){
  const form=new FormData()
  form.append('frame',{uri:data, type:'image/jpeg', name:'frame.jpg'})
  const res=await fetch(API_URL,{method:'POST',body:form})
  return res.json()
}
