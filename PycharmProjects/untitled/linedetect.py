import numpy as np
import cv2

img = cv2.imread('ttt.jpg')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(gray, 224, 250, cv2.THRESH_BINARY)[1]
kernel = np.ones((5,5),np.uint8)
gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
gray = cv2.erode(gray,kernel,iterations = 1)
cv2.imshow('origin',gray)

edges = cv2.Canny(gray,0,0,apertureSize = 3)

minLineLength= (img.shape[0] * 70) / 100       #허프변환
lines = cv2.HoughLinesP(image=edges,rho=0.02,theta=np.pi/500, threshold=10,lines=np.array([]), minLineLength=minLineLength,maxLineGap=100)

a,b,c = lines.shape
for i in range(a):
    cv2.line(gray, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)


print(len(lines))
cv2.imshow('houghlines5.jpg',gray)
cv2.waitKey(0)
