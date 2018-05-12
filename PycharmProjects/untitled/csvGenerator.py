import cv2
import csv
import numpy as np

drawing = False #Mouse가 클릭된 상태 확인용
ix,iy = -1,-1
index=0

data=[]
# Mouse Callback함수
# NOTICE! 항상 좌상단에서 우하단으로 그릴것!
def draw_rect(event, x,y, flags, param):
    global ix,iy, drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN: #마우스를 누른 상태
        drawing = True
        ix, iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
        if drawing == True:            # 마우스를 누른 상태 일경우
            cv2.rectangle(img,(ix,iy),(x,y),(255,0,0),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False;             # 마우스를 때면 상태 변경
        cv2.rectangle(img,(ix,iy),(x,y),(255,0,0),-1)
        print(ix,iy,x-ix,y-iy)   # 중심좌표, 너비, 높이 형태로 표현

        data.append([ix,iy,x-ix,y-iy])


def num_generator(current_num):
    result = "failed"
    if 0<=current_num<=9 :
        result =  "00" + str(current_num)
    elif 10<=current_num<=99 :
        result = "0" + str(current_num)
    elif current_num>=100 :
        result = str(current_num)

    return result

def tester_ui(bg): # bg is standardized image(img / 255)

    not_mask = np.ones(bg.shape, np.float32)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rect)

    screen = np.empty(bg.shape)
    while(1):
        screen = bg.astype(np.float32) * not_mask
        color_mask = np.logical_not(not_mask).astype(np.float32)
        color_mask *= (0,0,1) # red mask
        screen += color_mask
        cv2.imshow('image',screen)
        k = cv2.waitKey(1) & 0xFF
        if k == 13: #ESC = 27, CarriageReturn(enter) = 13
            break

    mask = np.logical_not(not_mask).astype(np.float32)
    return mask

if __name__ == '__main__':

    while True:
        #-------------------------------------
        jfname = num_generator(index) + ".jpg"
        csvname = num_generator(index) + ".csv"
        img = cv2.imread(jfname)
        if img is None :
            print ("That was last image")
            break
        else:
            img = cv2.imread(jfname) / 255

        f = open(csvname, 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)

        not_mask = np.ones(img.shape, np.float32)

        cv2.namedWindow(num_generator(index))
        cv2.setMouseCallback(num_generator(index), draw_rect)

        screen = np.empty(img.shape)
        while (1):
            screen = img.astype(np.float32) * not_mask
            color_mask = np.logical_not(not_mask).astype(np.float32)
            color_mask *= (0, 0, 1)  # red mask
            screen += color_mask
            cv2.imshow(num_generator(index), screen)
            k = cv2.waitKey(1) & 0xFF
            if k == 13:  # ESC = 27, CarriageReturn(enter) = 13
                cv2.destroyWindow(num_generator(index))
                wr.writerow(data)
                data=[]
                index = index + 1
                print(num_generator(index))
                break

        wr.writerow(data) # for last data
        f.close()

