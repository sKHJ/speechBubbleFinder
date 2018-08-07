import cv2
import sys
import csv

#imageLocation = sys.argv[1]
imageLocation ='seg_answers'
import os


filelist=[]
originimglist=[]
maskimglist=[]

for root, dirs, files in os.walk(imageLocation):
    for file in files:
        filelist.append(file)

print(filelist)

i=1
for data in filelist:
    if ( i % 3 == 1):
       originimglist.append(data)
    if (i% 3 == 0):
        maskimglist.append(data)
    i+=1

print(originimglist)
print(maskimglist)
print(len(originimglist))
print(len(maskimglist))

if (len(originimglist)!=len(maskimglist)):
    print(" i think... something wrong here... ")

f = open('img_feature.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

data=[]
for index in range(0,len(originimglist)):
    targetimg = cv2.imread(imageLocation + '/' + originimglist[index])
    cv2.imshow("Look at this image!", targetimg)
    cv2.waitKey(0)
    feature1 = input("Language? ENG(0),JPN(1) : ")
    feature2 = input("is there margin-text? YES(1), NO(0) : ")
    feature3 = input("is image calibrated? YES(1),NO(0)" )

    data.append([originimglist[index],feature1,feature2,feature3])



print(data)