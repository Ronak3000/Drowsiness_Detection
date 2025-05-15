import React from 'react'
import { View, Text, StyleSheet } from 'react-native'

export default function StatusOverlay({ status }) {
  const bg = status === 'drowsy'
    ? 'rgba(255,0,0,0.6)'
    : 'rgba(0,128,0,0.6)'

  return (
    <View style={[styles.overlay, { backgroundColor: bg }]}>
      <Text style={styles.text}>{status.toUpperCase()}</Text>
    </View>
  )
}

const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    bottom: 50,
    left: 0,
    right: 0,
    alignItems: 'center',
    padding: 10
  },
  text: {
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold'
  }
})
