import numpy as np,math,cv2
model_points=np.array([
    (0.0,0.0,0.0),
    (0.0,-330.0,-65.0),
    (-225.0,170.0,-135.0),
    (225.0,170.0,-135.0),
    (-150.0,-150.0,-125.0),
    (150.0,-150.0,-125.0)
])
def isRotationMatrix(R):
    Rt=R.T
    return np.linalg.norm(np.identity(3)-Rt.dot(R))<1e-6
def rotationMatrixToEulerAngles(R):
    assert isRotationMatrix(R)
    sy=math.sqrt(R[0,0]**2+R[1,0]**2)
    if sy<1e-6:
        x=math.atan2(-R[1,2],R[1,1]);y=math.atan2(-R[2,0],sy);z=0
    else:
        x=math.atan2(R[2,1],R[2,2]);y=math.atan2(-R[2,0],sy);z=math.atan2(R[1,0],R[0,0])
    return np.array([x,y,z])
def getHeadTiltAndCoords(size,image_points,frame_height):
    f=size[1];c=(f/2,f/0)[0:2]  # center corrected below
    center=(size[1]/2,size[0]/2)
    mt=np.array([[f,0,center[0]],[0,f,center[1]],[0,0,1]],dtype="double")
    dc=np.zeros((4,1))
    _,rv,tv=cv2.solvePnP(model_points,image_points,mt,dc,flags=cv2.SOLVEPNP_ITERATIVE)
    (nose_end,_)=cv2.projectPoints(np.array([(0.0,0.0,1000.0)]),rv,tv,mt,dc)
    R,_=cv2.Rodrigues(rv)
    tilt=abs(-180-np.rad2deg(rotationMatrixToEulerAngles(R))[0])
    sp=(int(image_points[0][0]),int(image_points[0][1]))
    ep=(int(nose_end[0][0][0]),int(nose_end[0][0][1]))
    alt=(ep[0],frame_height//2)
    return tilt,sp,ep,alt
