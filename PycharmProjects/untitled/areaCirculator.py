import cv2
import csv
import numpy as np
import re

score=100

def areaCirculator2(list1,list2):

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

def csvReader(name, list): #csv 파일 'name'을 프로그램 내 'list'에 저장

    f = open(name, 'r', encoding='utf-8', newline='')
    r = csv.reader(f)

    for i in r:
        list.append(i)

    f.close()

def csvInterpreter(list):
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

def csvComparison(list1,list2,score):
    listSize1 = len(list1)
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
    currentScore = score

    for j in range(0,listSize2):
        print ("list2의 %d 번째 좌표와 비교" %j)
        cList1 = csvInterpreter(list1[0][0])
        cList2 = csvInterpreter(list2[0][j])
        print (cList1)
        print (cList2)

        area = areaCirculator2(cList1,cList2)
        if area > current :               # 어떤 조합이 가장 높은 점수를 얻을수 있을까?
            current=area
            currentj = j

    if current < 80:
        currentScore = currentScore - 10

    print ("list2의 %d번째와"%currentj + "%d 퍼센트 일치" %current)

    print (list1)
    print (list2)

    newList1 = list1.pop(0)
    newList1.pop(0)
    newList2 = list2.pop(0)
    newList2.pop(currentj)

    print (newList1)
    print (newList2)

    return csvComparison(newList1,newList2,currentScore)
    #return 0



if __name__ == '__main__':
    list1 = []
    list2 = []
    csvReader('output1.csv',list1)  # 내가 찾은 list
    csvReader('output2.csv',list2)  # 기계가 찾은 list

    listSize1 = len(list1) -1
    listSize2 = len(list2) -1

    print(listSize1)
    print(listSize2)

    current = 0
    currenti= -1
    currentj= -1

    #ToDo : list의 요소를 어떻게 읽을것인가
    print(list1[0][0])
    print(list2[0][0])

    cList1 = csvInterpreter(list1[0][0])
    cList2 = csvInterpreter(list2[0][0])
    #areaCirculator2(cList1,cList2)
    a = csvComparison(list1,list2,100)
    #a = csvInterpreter(list2[0][0])
    print(a)



