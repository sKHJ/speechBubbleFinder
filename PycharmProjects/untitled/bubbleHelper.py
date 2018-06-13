import cv2
import csv
import numpy as np

drawing = False #Mouse가 클릭된 상태 확인용
ix,iy = -1,-1
index=48

imageFlag=0
data=[]
row = 0
col = 0

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
        drawing = False            # 마우스를 때면 상태 변경
        cv2.rectangle(img,(ix,iy),(x,y),(255,0,0),-1)

        if imageFlag == 1 :     # 1/3
            print(ix,iy,x-ix,y-iy)   # 중심좌표, 너비, 높이 형태로 표현
            data.append([ix,iy,x-ix,y-iy])
        if imageFlag == 2 :     # 2/3
            a = x-ix
            b = y-iy
            iy = iy + (int)(col/6)
            print(ix, iy, a, b)
            data.append([ix, iy, a, b])
        if imageFlag == 0 :     # 3
            a = x - ix
            b = y - iy
            iy = iy + (int)(col/3)
            print(ix, iy, a, b)
            data.append([ix, iy, a, b])



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
        if imageFlag == 0:
            jfname = num_generator(index) + ".jpg"
            csvname = num_generator(index) + ".csv"
            oriimg = cv2.imread(jfname)
            print("file open : %s"%jfname)


            f = open(csvname, 'w', encoding='utf-8', newline='')
            wr = csv.writer(f)

        if oriimg is None :
            print ("That was last image")
            break
        else:
            row = oriimg.shape[1]
            col = oriimg.shape[0]
            #img = cv2.imread(jfname) / 255

            if imageFlag == 0 :
                img = oriimg[0:(int)((col*2)/3), 0:row] / 255
                imageFlag+=1
            elif imageFlag == 1 :
                img = oriimg[(int)(col/6) : (int)((col*5)/6), 0:col] / 255
                imageFlag+=1
            elif imageFlag == 2 :
                img = oriimg[(int)(col/3):col, 0:col] / 255
                imageFlag=0




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
                if imageFlag != 0:
                    print(1)
                    break
                else:
                    cv2.destroyWindow(num_generator(index))
                    wr.writerow(data)
                    data=[]
                    index = index + 1
                    print(num_generator(index))
                    break

        if imageFlag == 0:
            wr.writerow(data) # for last data
            f.close()

