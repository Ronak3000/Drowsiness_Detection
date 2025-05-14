from flask import Flask,request,jsonify
import cv2,mediapipe as mp,numpy as np
from deepface import DeepFace
from model.EAR import eye_aspect_ratio
from model.MAR import mouth_aspect_ratio
from model.HeadPose import getHeadTiltAndCoords

app=Flask(__name__)
mpf=mp.solutions.face_mesh.FaceMesh(static_image_mode=True,
    max_num_faces=1,refine_landmarks=True)

@app.route('/predict',methods=['POST'])
def predict():
    data=request.files['frame'].read()
    npimg=np.frombuffer(data,np.uint8)
    frame=cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    faces=DeepFace.extract_faces(frame,detector_backend='mtcnn',
        enforce_detection=False,align=False)
    mesh=mpf.process(rgb).multi_face_landmarks
    if not mesh or not faces:
        return jsonify(status='no_face')
    lm=mesh[0].landmark
    h,w=frame.shape[:2]
    coords=np.array([[int(p.x*w),int(p.y*h)] for p in lm])
    LEFT=[33,160,158,133,153,144];RIGHT=[362,385,387,263,373,380]
    MOUTH=[61,291,0,17,13,14,87,317]
    ear=(eye_aspect_ratio(coords[LEFT])+eye_aspect_ratio(coords[RIGHT]))/2
    mar=mouth_aspect_ratio(coords[MOUTH])
    pts=np.zeros((6,2),dtype='double')
    pts[0]=coords[1];pts[1]=coords[199]
    pts[2]=coords[LEFT[0]];pts[3]=coords[RIGHT[3]]
    pts[4]=coords[MOUTH[0]];pts[5]=coords[MOUTH[1]]
    tilt,_,_,_=getHeadTiltAndCoords(frame.shape[:2],pts,h)
    status=('drowsy' if ear<0.25 or mar>0.79 or tilt>15 else 'alert')
    return jsonify(ear=round(float(ear),2),
                   mar=round(float(mar),2),
                   tilt=round(float(tilt),2),
                   status=status)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)
