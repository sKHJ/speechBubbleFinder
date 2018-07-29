#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;

# Read image
#im = cv2.imread("ttt4.jpg", cv2.IMREAD_GRAYSCALE)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200

# Filter by Area.
params.filterByArea = True
params.minArea = 15

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

detector = cv2.SimpleBlobDetector_create(params)
sift = cv2.xfeatures2d.SIFT_create()

# Detect blobs.
#keypoints = detector.detect(im)

def blobDetect(im):
    keypoints = detector.detect(im)
    return len(keypoints)

def siftDetect(im):
    kps = sift.detectAndCompute(im, None)
    return len(kps)

def cornerDetect(im):
    image = np.float32(im)
    dst = cv2.cornerHarris(image, 2, 3, 0.04)
    return len(dst)

def connectedComponentDetect(im):
    output = cv2.connectedComponentsWithStats(im, 4, cv2.CV_32S)
    return output[0]

def imgResizer(im):
    height = 250
    width = 250
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed((255,255,255)))
    # Fill image with color
    image[:] = color

    if (im.shape[1] > width) and (im.shape[0] > height):
        r_width = im.shape[1]
        r_height = im.shape[0]
        parm = 0.95
        while True:
            r_width = int(im.shape[1] * parm)
            r_height = int(im.shape[0] * parm)
            if(r_width < width) and (r_height < height):
                break
            else:
                parm-=0.05

        r_img = cv2.resize(im, (r_width, r_height), interpolation=cv2.INTER_AREA)
    else:
        r_img = im

    image[0:r_img.shape[0],0:r_img.shape[1]] = r_img

    cv2.imshow('af',image)
    cv2.waitKey(0)
    #cv2.imwrite('red.jpg', image)

    return image
