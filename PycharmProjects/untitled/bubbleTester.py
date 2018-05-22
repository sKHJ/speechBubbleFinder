import cv2
import csv
import numpy as np
import re

score=100

def csvReader2(name, list1):         #csv파일이 string 형태라서 이를 int list로 바꿔주는 과정
    with open(name, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)

    for i in range(0, len(your_list[0])):
        l = csvInterpreter(your_list[0][i])
        list1.append(l)

def csvInterpreter(list):  #csv파일이 string 형태라서 이를 int list로 바꿔주는 과정
    newList=[]
    a = ''
    flag = 0
    for k in list:
        #print(k)
        if k.isdigit():
            flag = 1
            a = a + k
        elif flag == 1:
            #print(a)
            flag = 0
            newList.append(int(a))
            a = ''
    return newList

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
    print("면적:%d" %result )

    score =int ( ( result / (list1[2]*list1[3]) ) * 100)


    print("점수:%d" %score)
    print("---------------------------------")
    return score



def csvComparison(list1,list2,score):           #내가 찾은 사각형 list1과 기계가 찾은 사각형 list2를 비교해
    listSize1 = len(list1)                      #최종점수 산출
    #if listSize1 > 10 :
    #    listSize1 = len(list1)
    listSize2 = len(list2)
    print("list1사이즈 : %d" %listSize1)
    print("list2사이즈 : %d" %listSize2)

    if listSize1 <= 0 :
        return score
    if listSize2 <= 0 :
        return score

    area = 0
    current = 0
    currenti= 0
    currentj= -1
    removeJ = 1
    currentScore = score

    newList1=[]
    newList2=[]

    for j in range(0,listSize2):
        print ("list2의 %d 번째 좌표와 비교" %j)

        area = areaCirculator2(list1[0],list2[j])
        if area > current :               # 어떤 조합이 가장 높은 점수를 얻을수 있을까?
            current=area
            currentj = j

        print("현재 최고점 %d"%current)

    if current < 80 or currentj == -1 :
        currentScore = currentScore - 10
        removeJ = 0

    print ("list2의 %d번째와"%currentj + "%d 퍼센트 일치" %current)

    print (list1)
    print (list2)

    newList1 = list1
    newList1.pop(0)
    newList2 = list2

    if removeJ == 1 :
        newList2.pop(currentj)

    print (newList1)
    print (newList2)

    return csvComparison(newList1,newList2,currentScore)
    #return 0


if __name__ == '__main__':
    list1 = []
    list2 = []
    csvReader2('output1.csv',list1)  # 내가 찾은 list
    csvReader2('output2.csv',list2)  # 기계가 찾은 list

    listSize1 = len(list1)
    listSize2 = len(list2)

    print(listSize1)
    print(listSize2)

    current = 0
    currenti= -1
    currentj= -1

    a = csvComparison(list1,list2,100)

    print(a)

