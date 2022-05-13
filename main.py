import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp

cap = cv2.VideoCapture(0)
handDetector = HandDetector(detectionCon=0.9)
col = (255, 0, 255, 0.8)



class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor

rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150, 150]))

cx, cy, w, h = 100, 100, 200, 200

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = handDetector.findHands(img)
    lmList, _ = handDetector.findPosition(img)

    if lmList:

        l, _, _, = handDetector.findDistance(4, 8, img)
        print(l)

        if l < 30:
            cursor = lmList[8]
            for rect in rectList:
                rect.update(cursor)

    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), col, cv2.FILLED)

    cv2.imshow("frame", img)
    cv2.waitKey(1)

