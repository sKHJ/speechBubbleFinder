import cv2
import csv
import numpy as np

drawing = False #Mouse가 클릭된 상태 확인용
ix,iy = -1,-1
index=0

# Mouse Callback함수
# NOTICE! 항상 좌상단에서 우하단으로 그릴것!
def draw_rect(event, x,y, flags, param):
    global ix,iy, drawing, mode
    #global data

    if event == cv2.EVENT_LBUTTONDOWN: #마우스를 누른 상태
        drawing = True
        ix, iy = x,y
    elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
        if drawing == True:            # 마우스를 누른 상태 일경우

            cv2.rectangle(img,(ix,iy),(x,y),(255,0,0),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False;             # 마우스를 때면 상태 변경

        cv2.rectangle(img,(ix,iy),(x,y),(255,0,0),-1)
        #print(ix,iy,x,y)
        print(ix,iy,x-ix,y-iy)   # 중심좌표, 너비, 높이 형태로 표현

        f = open(csvname, 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        data = np.array([ix,iy,x-ix,y-iy])
        wr.writerow(data)

        # ToDo : 파일에 누적해서 저장하는방법 ?? array로 저장해놧다가 프로그램 종료때 저장한다?
        f.close()

def num_generator(current_num):
    result = "failed"
    if 0<=current_num<=9 :
        result =  "00" + str(current_num)
    elif 10<=current_num<=99 :
        result = "0" + str(current_num)
    elif current_num>=100 :
        result = str(current_num)

    return result





#img = np.zeros((512,512,3), np.uint8)
#fname = "landscape"



    #jfname = num_generator(index) + ".jpg"
    #csvname = num_generator(index) + ".csv"
    #img = cv2.imread(jfname)
    #cv2.namedWindow(num_generator(index))
    #cv2.setMouseCallback(num_generator(index), draw_rect)

while True:
    #-------------------------------------
    jfname = num_generator(index) + ".jpg"
    csvname = num_generator(index) + ".csv"
    img = cv2.imread(jfname)
    cv2.namedWindow(num_generator(index))
    cv2.setMouseCallback(num_generator(index), draw_rect)
    #--------------------------------------
    cv2.imshow(num_generator(index) , img)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:    # esc를 누르면 종료
        break
    elif k == ord('n'):
       index = index + 1
       print(num_generator(index))


cv2.destroyAllWindows()
