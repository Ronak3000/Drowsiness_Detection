import {React,useState,useRef} from 'react'
import {View,Text,StyleSheet,Alert} from 'react-native'
import {RNCamera} from 'react-native-camera'
import {analyzeFrame} from '../api'
import StatusOverlay from './StatusOverlay'

export default function CameraView(){
  const [status,setStatus]=useState('loading')
  const cameraRef=useRef(null)
  const onReady=async()=>{
    if(cameraRef.current){
      const options={quality:0.5,base64:false}
      const data=await cameraRef.current.takePictureAsync(options)
      const result=await analyzeFrame(data.uri)
      setStatus(result.status)
    }
    setTimeout(onReady,2000)
  }
  return (
    <View style={s.container}>
      <RNCamera
        ref={cameraRef}
        style={s.preview}
        type={RNCamera.Constants.Type.front}
        onCameraReady={onReady}
      />
      <StatusOverlay status={status}/>
    </View>
  )
}

const s=StyleSheet.create({
  container:{flex:1},
  preview:{flex:1}
})
