import cv2
import time
import numpy as np
import mediapipe as mp
import handDetection as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#####################
wCam,hCam=640,480
###################

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0

detector=htm.handDetector()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]
vol=0
volBAR=400
volPERC=0
while True:
    success,img=cap.read()
    img=detector.findhands(img)
    #getting position
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        #4-->Thumb, 8-->Index finger
        #print(lmlist[4],lmlist[8])

        #creating circles around thumb and index
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        #create a line between them
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)
        #print(length)

        #hand range-50-300
        #vol range--65-0

        vol=np.interp(length,[50,300],[minVol,maxVol])
        volBAR = np.interp(length,[50,300],[400,150])
        volPERC=np.interp(length,[50,300],[0,100])

        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            #changed the colour of our central button if both fingers came too close(giving it a button effect)
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
        cv2.rectangle(img,(50,int(volBAR)),(85,400),(255,0,0),cv2.FILLED)
        cv2.putText(img, f'{int(volPERC)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255,0,0), 3)


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'FPS:{int(fps)}',(50,70),cv2.FONT_HERSHEY_COMPLEX,
                1,(255,0,0),3)


    cv2.imshow("Img",img)
    cv2.waitKey(1)
