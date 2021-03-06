import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands (self.mode, self.maxHands, self.detectionCon, self.trackCon)

        # Function to draw line between 2 points
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                # pass the original img / below line shoud give me point on hand
                # mpDraw.draw_landmarks(img, handLms)
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)

        return img
    
    def findPostion(self,img,handNo = 0 ,draw= True):

        lmList= []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
         # this will give you the x,y cordnation by ratio so multiple it by width and height / print(id,lm)
                h, w, c = img.shape
                cx, cy = int (lm.x * w), int (lm.y * h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle (img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                    
        return lmList

# to check if it is detecting any thing print(results.multi_hand_landmarks)


def main():
    pTime = 0
    cTime = 0
    
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPostion(img)
            
        # Capturing FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        
        # showing as in the screen
        cv2.putText (img, str (int (fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        
        cv2.imshow ("img", img)
        cv2.waitKey (1)


if __name__ == "__main__":
    main()
