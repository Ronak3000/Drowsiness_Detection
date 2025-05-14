export const API_URL='https://<your-render-service>.onrender.com/predict'
export async function analyzeFrame(data){
  const form=new FormData()
  form.append('frame',{uri:data, type:'image/jpeg', name:'frame.jpg'})
  const res=await fetch(API_URL,{method:'POST',body:form})
  return res.json()
}
