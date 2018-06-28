# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import imutils
import cv2

def bubbleChecker(img,x,y,w,h):
    #1. blob size limit-------------------
    #frame size = ( width / 6 ) * (height * 8 )
    #blob_size = ( width / 10 ) * ( height * 8 )

    row = int(img.shape[1] / 60)  #minimal size limit
    col = int(img.shape[0] / 64)
    if (w < row) or (h < col) :
        return 0
    if h * 1.5 < w :
        return 0

    #2. white pixel rate limit----------------------
    img_trim = img[y:y + h, x:x + w]
    n_white_pix = cv2.countNonZero(img_trim)
    whiterate =(  n_white_pix / (w*h) ) * 100
    if whiterate < 45 :
        return 0

    #3. two line
    edges = cv2.Canny(img_trim, 0, 0, apertureSize=3)

    minLineLength = (h * 70) / 100  # 크기제한 : 이미지 size 70%이상
    lines = cv2.HoughLinesP(image=edges, rho=0.02, theta=np.pi / 500, threshold=19,
                            lines=np.array([]), minLineLength=minLineLength, maxLineGap=50)
    if lines is None:
        print(0)
        return 0
    a, b, c = lines.shape
    count = 0
    for n in range(a):
        x1 = lines[n][0][0]
        x2 = lines[n][0][2]
        if (x2 - x1) == 0:
            count += 1

    print(count)

    if count < 2:
        return 0

    return 1

def areaCirculator2(list1,list2):       #사각형 좌표 2개를 받아서 겹치는 넓이를 계산함
                                        #( 겹치는 넓이/ 내가 찾은 사각형 넓이 ) -> 점수 환산
    if len(list1) ==0:
        return 0
    if len(list2) ==0:
        return 0

    point = []

    point = [list1[0], list1[1],
             list1[0] + list1[2], list1[1] + list1[3],
             list2[0], list2[1],
             list2[0] + list2[2], list2[1] + list2[3]
             ]
    num = len(point) // 4
    point = np.array(point).reshape(num, 4)
    point = point.astype(int)
    field = np.zeros((int(max(point[:, 2])), int(max(point[:, 3]))))
    for i in range(num):
        field[point[i, 0]:point[i, 2], point[i, 1]:point[i, 3]] = 1
    #print("면적:%0.2f" % (field.sum() ))

    result = field.sum() - ( field.sum() - list1[2]*list1[3] ) - ( field.sum() - list2[2]*list2[3] )
    #print("면적:%d" %result )

    score =int ( ( result / (list1[2]*list1[3]) ) * 100)

    #print("점수:%d" %score)
    #print("---------------------------------")
    return score


# load the image, convert it to grayscale, and blur it
image = cv2.imread("003.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


#blurred = cv2.GaussianBlur(gray, (11, 11), 0)
thresh = cv2.threshold(gray, 224, 250, cv2.THRESH_BINARY)[1]

# threshold the image to reveal light regions in the
# blurred image

# perform a series of erosions and dilations to remove
# any small blobs of noise from the thresholded image

kernel = np.ones((5,5),np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
thresh = cv2.erode(thresh,kernel,iterations = 1)
cv2.imshow("th", thresh)

#thresh = cv2.erode(thresh, None, iterations=2)
#thresh = cv2.dilate(thresh, None, iterations=4)

# perform a connected component analysis on the thresholded
# image, then initialize a mask to store only the "large"
# components
labels = measure.label(thresh, neighbors=4)
mask = np.zeros(thresh.shape, dtype="uint8")

# loop over the unique components
for label in np.unique(labels):
    # if this is the background label, ignore it
    if label == 0:
        continue

    # otherwise, construct the label mask and count the
    # number of pixels
    labelMask = np.zeros(thresh.shape, dtype="uint8")
    labelMask[labels == label] = 255
    numPixels = cv2.countNonZero(labelMask)

    # if the number of pixels in the component is sufficiently
    # large, then add it to our mask of "large blobs"
    #row = int(image.shape[1] / 60)
    #col = int(image.shape[0] / 64)
    if numPixels > 2000:
        mask = cv2.add(mask, labelMask)


# find the contours in the mask, then sort them from left to
# right
cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
cnts = contours.sort_contours(cnts)[0]

data=[]
# loop over the contours
for (i, c) in enumerate(cnts):
    # draw the bright spot on the image
    (x, y, w, h) = cv2.boundingRect(c)
    # ((cX, cY), radius) = cv2.minEnclosingCircle(c)
    #cv2.circle(image, (int(cX), int(cY)), int(radius),(0, 0, 255), 3)
    if bubbleChecker(thresh,x,y,w,h) == 1 :
        data.append([x,y,w,h])
        #cv2.rectangle(image, (x,y),(x+w,y+h),(30, 0, 255), 3)
        #cv2.putText(image, "#{}".format(i + 1), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

'''
    for [x1,y1,w1,h1] in data:
        l1 = [x1,y1,w1,h1]
        for [x2, y2, w2, h2] in data:
            l2 = [x2, y2, w2, h2]
            if (x1 != x2) and (y1 != y2) :

                if areaCirculator2(l1,l2) >= 80 :
                    if (w1*h1) > (w2*h2) :
                        data.remove([x2,y2,w2,h2])
                    else:
                        data.remove([x1,y1,w1,h1])
'''

    for [x,y,w,h] in data:
        cv2.rectangle(image, (x, y), (x + w, y + h), (30, 0, 255), 3)
        cv2.putText(image, "#{}".format(i + 1), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)




# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)



