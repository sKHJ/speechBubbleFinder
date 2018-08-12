import cv2
import sys
import csv

# HOW TO USE--------------------------
# python image_classifier.py [imagefolder]
# EX ) python image_classifier.py answers
#-----------------------------------------


imageLocation = sys.argv[1]
#imageLocation ='seg_answers'
import os

def stateprinter(f1,f2,f3):
    lang ='JPN'
    if f1==0:
        lang='JPN'
    if f1==1:
        lang='ENG'

    margin='YES'
    if f2==0:
        margin='YES'
    if f2==1:
        margin='NO'

    cali='YES'
    if f3==0:
        cali='YES'
    if f3==1:
        cali='NO'

    print("language : %s, margintext : %s, Calibrated : %s "%(lang,margin,cali))


filelist=[]
originimglist=[]
maskimglist=[]

for root, dirs, files in os.walk(imageLocation):
    for file in files:
        filelist.append(file)

if 'img_feature.csv' in filelist:
    filelist.remove('img_feature.csv')

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

f = open(imageLocation+ '/' + 'img_feature.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

data=[]
for index in range(0,len(originimglist)):

    targetimg = cv2.imread(imageLocation + '/' + originimglist[index])
    cv2.imshow("Look at this image!", targetimg)
    print("What is language? JPN-(push q) / ENG- (push w)")
    print("Is there margin text? YES-(push a) / NO - (push s)")
    print("is calibrated? YES-(push z) / NO - (push x)")
    print("----------------------------------------")
    print("Is classifying finished?, push ESC")
    feature1,feature2,feature3=0,0,0

    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            feature1=0
            stateprinter(feature1,feature2,feature3)
        if k == ord('w'):
            feature1=1
            stateprinter(feature1, feature2, feature3)
        if k == ord('a'):
            feature2=0
            stateprinter(feature1,feature2,feature3)
        if k == ord('s'):
            feature2=1
            stateprinter(feature1, feature2, feature3)
        if k == ord('z'):
            feature3=0
            stateprinter(feature1,feature2,feature3)
        if k == ord('x'):
            feature3=1
            stateprinter(feature1, feature2, feature3)
        if k == 27:
            cv2.destroyAllWindows()
            break

    data.append([originimglist[index],feature1,feature2,feature3])


for i in range(0, len(data)):
    print(data[i])
    wr.writerow(data[i])
f.close()
