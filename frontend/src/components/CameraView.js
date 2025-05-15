import React, { useState, useEffect, useRef } from 'react'
import { View, StyleSheet, Text, Platform } from 'react-native'
import { Camera, useCameraPermissions } from 'expo-camera'
import * as FaceDetector from 'expo-face-detector'

export default function CameraView() {
  const [permission, requestPermission] = useCameraPermissions()
  const cameraRef = useRef(null)
  const [faces, setFaces] = useState([])

  useEffect(() => {
    if (Platform.OS !== 'web') {
      requestPermission()
    }
  }, [])

  const handleFacesDetected = ({ faces }) => {
    setFaces(faces)
  }

  if (Platform.OS === 'web') {
    return (
      <View style={styles.container}>
        <Text>Camera not supported on web</Text>
      </View>
    )
  }

  if (!permission) return <View style={styles.container}/>
  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text>No camera access</Text>
      </View>
    )
  }

  return (
    <View style={styles.container}>
      <Camera
        ref={cameraRef}
        style={styles.camera}
        type={Camera.Constants.Type.front}
        onFacesDetected={handleFacesDetected}
        faceDetectorSettings={{
          mode: FaceDetector.FaceDetectorMode.fast,
          detectLandmarks: FaceDetector.FaceDetectorLandmarks.none,
          runClassifications: FaceDetector.FaceDetectorClassifications.none,
        }}
      />
      <View style={styles.faceInfo}>
        <Text style={styles.faceText}>
          {faces.length > 0 ? `Faces detected: ${faces.length}` : 'No faces detected'}
        </Text>
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  camera: {
    flex: 1,
  },
  faceInfo: {
    position: 'absolute',
    bottom: 50,
    alignSelf: 'center',
    backgroundColor: 'rgba(0,0,0,0.6)',
    padding: 10,
    borderRadius: 10,
  },
  faceText: {
    color: '#fff',
    fontSize: 16,
  },
})
