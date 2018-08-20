import random

import cv2
import sys
import numpy as np
import os
import time

# HOW TO USE--------------------------
# python imageSynthesizer.py [text component folder] [target image] [target mask]
# EX ) python imageSynthesizer.py textcomp sampleorg.jpg samplemask.png
#
# 1. image folder = origin manga images + mask images
# 2. mask must be WHITE
#-----------------------------------------

#compLocation ='textcomp'
compLocation = sys.argv[1]
targetorg = sys.argv[2]
targetmask = sys.argv[3]

#testorg = cv2.imread('sampleorg.jpg')
testorg = cv2.imread(targetorg)
testmask = cv2.imread(targetmask)
def compSynth(comp,compmask,origin,originmask):

    rows, cols, channels = comp.shape
    org_rows, org_cols, org_channels = origin.shape
    count=0

    while True:
        count+=1
        if (count>20):
            print("Synth fail...")
            return 0
        x = random.randrange(0, org_rows - rows)
        y = random.randrange(0, org_cols - cols)

        std = np.std(originmask[x:x + rows, y:y + cols].ravel())
        if (std ==0):

            break;


    roi = origin[x:x+rows, y:y+cols]


    img2gray = cv2.cvtColor(comp, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img1_fg = cv2.bitwise_and(comp, comp, mask=mask)
    img2_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    #cv2.imshow("Image2", img1_fg)
    #cv2.waitKey(0)

    dst = cv2.add(img1_fg, img2_bg)

    origin[x:x+rows, y:y+cols] = dst
    originmask[x:x+rows, y:y+cols] = compmask

    return 1



filelist=[]
complist=[]
compmasklist=[]

for root, dirs, files in os.walk(compLocation):
    for file in files:
        filelist.append(file)

print(filelist)

i=1
for data in filelist:
    if (data.find('_') != -1):
        compmasklist.append(data)
    if (data.find('_') == -1):
        complist.append(data)
    i+=1

compmasklist.sort()
complist.sort()

print(complist)
print(compmasklist)
print(len(complist))
print(len(compmasklist))





#comp1 = cv2.imread(compLocation + '/' + '2.png')
#comp1_mask = cv2.imread(compLocation + '/' + '2_.png')




for i in range(0,3):
    index = random.randrange(0, len(complist))
    mask_target = compmasklist.pop(index)

    comp_mask = cv2.imread(compLocation + '/' + mask_target )
    org_index = complist.index(mask_target[0:mask_target.index("_")] + '.png')

    org_target = complist.pop(org_index)



    comp = cv2.imread(compLocation + '/' + org_target)
    compSynth(comp, comp_mask, testorg, testmask)



row = testorg.shape[1]
col = testorg.shape[0]

cv2.imshow('res', testorg[0:(int)((col*2)/3), 0:row])
cv2.waitKey(0)
cv2.imshow('res', testorg[(int)(col/3):col, 0:col])
cv2.waitKey(0)
cv2.imshow('res', testmask)
cv2.waitKey(0)

now = time.localtime()
s = "%04d%02d%02d_%02d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


cv2.imwrite('segdata/' + s + '_org.png', testorg)
cv2.imwrite('segdata/' + s + '_mask.png', testmask)

cv2.destroyAllWindows()