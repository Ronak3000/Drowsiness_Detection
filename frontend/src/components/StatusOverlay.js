import React from 'react'
import {View,Text,StyleSheet} from 'react-native'

export default function StatusOverlay({status}){
  const color=status==='drowsy'?'red':'green'
  return (
    <View style={[s.overlay,{backgroundColor:color}]}>
      <Text style={s.text}>{status.toUpperCase()}</Text>
    </View>
  )
}

const s=StyleSheet.create({
  overlay:{
    position:'absolute',bottom:50,left:0,right:0,
    alignItems:'center',padding:10
  },
  text:{color:'white',fontSize:20,fontWeight:'bold'}
})
