import cv2
import sys
import numpy as np
import os

# HOW TO USE--------------------------
# python textcompExtracter.py [imagefolder]
# EX ) python textcompExtracter.py ext_test
#
# 1. image folder = origin manga images + mask images
# 2. mask must be WHITE
#-----------------------------------------


def imgsynth(img1, img2):
    # img1 = cv2.imread('textcomp/1_.png')
    # img2 = cv2.imread('textcomp/1.png')

    # 삽입할 이미지의 row, col, channel정보
    rows, cols, channels = img1.shape

    # 대상 이미지에서 삽입할 이미지의 영역을 추출
    roi = img2[0:rows, 0:cols]

    # mask를 만들기 위해서 img1을 gray로 변경후 binary image로 전환
    # mask는 logo부분이 흰색(255), 바탕은 검은색(0)
    # mask_inv는 logo부분이 검은색(0), 바탕은 흰색(255)

    img2gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # bitwise_and 연산자는 둘다 0이 아닌 경우만 값을 통과 시킴.
    # 즉 mask가 검정색이 아닌 경우만 통과가 되기때문에 mask영역 이외는 모두 제거됨.
    # 아래 img1_fg의 경우는 bg가 제거 되고 fg(logo부분)만 남게 됨.
    # img2_bg는 roi영역에서 logo부분이 제거되고 bg만 남게 됨.
    img1_fg = cv2.bitwise_and(img1, img1, mask=mask_inv)
    img1_bg = cv2.bitwise_and(img1, img1, mask=mask)
    img2_bg = cv2.bitwise_and(roi, roi, mask=mask)
    #cv2.imshow("Image2", img1_bg)
    #cv2.waitKey(0)

    # 2개의 이미지를 합치면 바탕은 제거되고 logo부분만 합쳐짐.
    dst = cv2.add(img1_fg, img2_bg)

    # 합쳐진 이미지를 원본 이미지에 추가.
    img2[0:rows, 0:cols] = dst

    image = np.zeros((rows, cols, 3), np.uint8)
    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed((0,0,0)))
    # Fill image with color
    image[:] = color

    image[0:rows, 0:cols] = dst
    return image


imageLocation = sys.argv[1]
#imageLocation ='ext_test'


filelist=[]
originimglist=[]
maskimglist=[]

for root, dirs, files in os.walk(imageLocation):
    for file in files:
        filelist.append(file)

print(filelist)

i=1
for data in filelist:
    if ( i % 2 == 0):
        maskimglist.append(data)
    if (i% 2 == 1):
        originimglist.append(data)
    i+=1

print(maskimglist)
print(originimglist)
print(len(maskimglist))
print(len(originimglist))


i=1
for index in range(0,len(originimglist)):
    maskimg = cv2.imread(imageLocation + '/' + maskimglist[index])
    oriimg = cv2.imread(imageLocation + '/' + originimglist[index])



    connectivity = 4
    # Perform the operation
    output = cv2.connectedComponentsWithStats(maskimg[:, :, 0], connectivity, cv2.CV_32S)
    stats = output[2]


    for data in stats:

        x = data[0]
        y = data[1]
        w = data[2]
        h = data[3]
        #cv2.rectangle(maskimg, (x, y), (x + w, y + h), (30, 0, 255), 3)
        if x!=0 and y!=0:
            print(maskimglist[index])

            resultimg = imgsynth(maskimg[y:y + h, x:x + w],oriimg[y:y + h, x:x + w])
            img2gray = cv2.cvtColor(maskimg[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
            img1_bg = cv2.bitwise_and(maskimg[y:y + h, x:x + w], maskimg[y:y + h, x:x + w], mask=mask)
            cv2.imwrite('textcomp/' + str(i) + '_.png', img1_bg)
            cv2.imwrite('textcomp/' + str(i) + '.png', resultimg)
            i+=1


