t cv2
import mediapipe as mp
import time

# class
class handDetector():
    def __init__(self,mode=False,maxHands=2,modelComplexity=1,detectionConf=0.7,trackingConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionConf = detectionConf
        self.trackingConf = trackingConf

        # detecting landmarks and connections
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,modelComplexity,detectionConf,trackingConf)
        self.mpdraw = mp.solutions.drawing_utils


    #-------------findhands----------------
    def findhands(self,img,draw=True):
        self.RGBimg = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(self.RGBimg)

        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img,handlms,self.mpHands.HAND_CONNECTIONS)

        return img

    # finding position=====================
    def findPosition(self, img, handNo=0, draw=True):

        lmlist = []

        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

        return lmlist

#-------------main--------------------------
def main():
    cTime=0
    pTime=0
    cap = cv2.VideoCapture(0)
    while True:
        success,img = cap.read()
        # class object
        detector = handDetector()
        img = detector.findhands(img)
        position = detector.findPosition(img)

        if len(position)!=0:
            print(position)


        # calculating time
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),1)

        cv2.imshow('img',img)
        if cv2.waitKey(20) & 0xFF == ord('d'):
            break

#-----------------python main---------------
if __name__=="__main__":
    main()
