# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import imutils
import cv2


location = 'manga/Chapter 067 - raw/006.jpg'
#location = '000.jpg'


def bubbleChecker(img,i,x,y,w,h):
    #1. blob size limit-------------------

    rowMin = int(img.shape[1] / 35)  #minimal size limit
    colMin = int(img.shape[0] / 35)
    rowMax = int(img.shape[1] / 2)
    colMax = int(img.shape[0] / 2)
    if (w < rowMin) or (h < colMin) :
        print('%d is deleted by size'%i)
        return 0

    if (w > rowMax) or (h > colMax) :
        print('%d is deleted by size' % i)
        return 0

    if h * 1.5 < w :
        print('%d is deleted by sizerate' % i)
        return 0

    #2. white pixel rate limit----------------------
    img_trim = img[y:y + h, x:x + w]

    n_white_pix = cv2.countNonZero(img_trim)
    whiterate =(  n_white_pix / (w*h) ) * 100
    if whiterate < 45 :
        print('%d is deleted by whiterate' % i)
        return 0

    #3. two line
    edges = cv2.Canny(img_trim, 0, 0, apertureSize=3)

    minLineLength = (h * 20) / 100  # 크기제한 : 이미지 size 70%이상
    maxLineGap = w/5
    lines = cv2.HoughLinesP(image=edges, rho=0.02, theta=np.pi / 500, threshold=20,
                            lines=np.array([]), minLineLength=minLineLength, maxLineGap=maxLineGap)

    vcount = 0

    # For DEBUG --------------------------------------------
    if i==-1 :
        if lines is not None :
            for i in range(len(lines)):
                for x1, y1, x2, y2 in lines[i]:
                    if (x1-x2) == 0 :
                        vcount +=1
                    cv2.line(img_trim, (x1, y1), (x2, y2), (0, 0, 255), 3)


        print('vertical line : %d'%vcount)
        cv2.imshow('%d'%i, img_trim)
        cv2.waitKey(0)
    #-----------------------------------------------------------


    if lines is None:
        img_trim = cv2.erode(img_trim, kernel, iterations=1)
        edges = cv2.Canny(img_trim, 0, 0, apertureSize=3)
        lines = cv2.HoughLinesP(image=edges, rho=0.02, theta=np.pi / 500, threshold=20,
                                lines=np.array([]), minLineLength=minLineLength, maxLineGap=maxLineGap)
        if lines is None:
            print(0)
            print('%d is deleted by line' % i)
            return 0


    a, b, c = lines.shape
    hcount = 0
    vcount = 0
    dcount =0
    for n in range(a):
        x1 = lines[n][0][0]
        x2 = lines[n][0][2]
        y1 = lines[n][0][1]
        y2 = lines[n][0][3]
        if (x2 - x1) == 0:
            vcount += 1
        if (y2 - y1) == 0:
            hcount += 1
        if ((x2 - x1) != 0 ) and ((y2 - y1) != 0 ) :
            dcount+=1


    if vcount < 2:
        print('%d is deleted by line' % i)
        return 0

    #if vcount > 30:
    #    print('%d is deleted by TOO MANY vertical line:%d' % (i,vcount))
    #    return 0

    if hcount > 10:
        print('%d is deleted by TOO MANY horizen line:%d' % (i,hcount))
        return 0

    if dcount > 5 :
        print('%d is deleted by diagonal line:%d' % (i, dcount))
        return 0



    print('---------%d is selected! v:%d h:%d d:%d----------' %(i,vcount,hcount,dcount))
    return 1



def bubbleFinder(image):
    # load the image, convert it to grayscale, and blur it
    #location = '003.jpg'
    #image = cv2.imread(location)
    #image2 = cv2.imread(location)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    #blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    thresh = cv2.threshold(gray, 224, 250, cv2.THRESH_BINARY)[1]

    # threshold the image to reveal light regions in the
    # blurred image

    # perform a series of erosions and dilations to remove
    # any small blobs of noise from the thresholded image

    #kernel = np.ones((5,5),np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.erode(thresh,kernel,iterations = 1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.erode(thresh,kernel,iterations = 1)

    #cv2.imshow("th", thresh)




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
        #cv2.rectangle(image, (x, y), (x + w, y + h), (30, 0, 255), 3)
        #cv2.putText(image, "#{}".format(i + 1), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2)
        print(i+1,x,y,w,h)
        if bubbleChecker(thresh,i+1,x,y,w,h) == 1 :
            data.append([x,y,w,h])

            #cv2.rectangle(image, (x,y),(x+w,y+h),(30, 0, 255), 3)
            #cv2.putText(image, "#{}".format(i + 1), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)


        for [x,y,w,h] in data:
            #cv2.rectangle(image2, (x, y), (x + w, y + h), (30, 0, 255), 3)
            #cv2.putText(image2, "#{}".format(i + 1), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)




    # show the output image
    #cv2.imshow("Image", image)
    #cv2.imshow("Image2", image2)

    #cv2.waitKey(0)
    
    retrun data



