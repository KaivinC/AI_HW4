import random
import copy
import math
import time
import matplotlib.pyplot as plt

ATTRIBUTE_NUM=32
CLASS_INDEX=1
RATIO=0.7
TREE_NUM=500

def DisbuteAllData(dataSet,trainData,testData):
    datas=copy.deepcopy(dataSet)

    for _ in range(math.floor(len(dataSet)*RATIO)):
        index=random.randint(0,len(datas)-1)
        trainData.append(datas[index])
        del datas[index]
    
    for i in range(len(datas)):
        testData.append(datas[i])

def TreeBagging(trainData,subData):
    datas=copy.deepcopy(trainData)

    for _ in range(math.floor(len(dataSet))):
        index=random.randint(0,len(datas)-1)
        subData.append(datas[index])



def CalGini(current,left,right):
    totalDC=0
    for i in current.values():
        totalDC+=i
    Dc=1
    for i in current.values():
        Dc=Dc-(i/totalDC)*(i/totalDC)
    
    totalDl=0
    for i in left.values():
        totalDl+=i
    Dl=1
    for i in left.values():
        Dl=Dl-(i/totalDl)*(i/totalDl)

    totalDr=0
    for i in right.values():
        totalDr+=i
    Dr=1
    for i in right.values():
        Dr=Dr-(i/totalDr)*(i/totalDr)

    D=Dc-(totalDl/totalDC)*Dl-(totalDr/totalDC)*Dr

    # if(D==0):
    #     print(left.values(),"and",right.values(),"and",i,interval)
    return D

def CalTree(currentNode,mode,ratio):
    global ATTRIBUTE_NUM
    global CLASS_INDEX
    if(mode==0):
        ATTRIBUTE_NUM=4
        CLASS_INDEX=4
    elif(mode==1):
        ATTRIBUTE_NUM=32
        CLASS_INDEX=1
    elif(mode==2):
        ATTRIBUTE_NUM=10
        CLASS_INDEX=10
    elif(mode==3):
        ATTRIBUTE_NUM=13
        CLASS_INDEX=0

    best_choice=[0,0]
    best_value=0
    current={}
    for k in range(len(currentNode.datas)):
        if(current.get(currentNode.datas[k][CLASS_INDEX])==None):
            current[currentNode.datas[k][CLASS_INDEX]]=1
        else:
            current[currentNode.datas[k][CLASS_INDEX]]+=1

    recordAttribute=[]
    # for i in range(2,ATTRIBUTE_NUM):
    ATTRIBUTE=math.floor(math.sqrt(ATTRIBUTE_NUM))
    #ATTRIBUTE=ratio
    for _ in range(ATTRIBUTE):
        if(mode==0):
            i=random.randint(0,ATTRIBUTE_NUM-1)
            while(i in recordAttribute):
                i=random.randint(0,ATTRIBUTE_NUM-1)
            recordAttribute.append(i)
        elif(mode==1):
            i=random.randint(2,ATTRIBUTE_NUM-1)
            while(i in recordAttribute):
                i=random.randint(2,ATTRIBUTE_NUM-1)
            recordAttribute.append(i)
        elif(mode==2):
            i=random.randint(1,ATTRIBUTE_NUM-1)
            while(i in recordAttribute):
                i=random.randint(1,ATTRIBUTE_NUM-1)
            recordAttribute.append(i)
        elif(mode==3):
            i=random.randint(1,ATTRIBUTE_NUM-1)
            while(i in recordAttribute):
                i=random.randint(1,ATTRIBUTE_NUM-1)
            recordAttribute.append(i)

        sorted(currentNode.datas,key=lambda l:l[i], reverse=True)
        for j in range(len(currentNode.datas)-1):
            interval=((float(currentNode.datas[j][i])+float(currentNode.datas[j+1][i]))/2)
            left={}
            right={}
            for k in range(len(currentNode.datas)):
                if(float(currentNode.datas[k][i])<interval):
                    if(left.get(currentNode.datas[k][CLASS_INDEX])==None):
                        left[currentNode.datas[k][CLASS_INDEX]]=1
                    else:
                        left[currentNode.datas[k][CLASS_INDEX]]+=1

                else:
                    if(right.get(currentNode.datas[k][CLASS_INDEX])==None):
                        right[currentNode.datas[k][CLASS_INDEX]]=1
                    else:
                        right[currentNode.datas[k][CLASS_INDEX]]+=1


            value=CalGini(current,left,right)
            
            if(best_value<value):
                best_value=value
                best_choice=[i,interval]
    
    currentNode.condition=best_choice

    leftDatas=[]
    rightDatas=[]
    
    left={}
    right={}
    leftNum=0
    rightNum=0
    for i in range(len(currentNode.datas)):
        if(float(currentNode.datas[i][best_choice[0]])<best_choice[1]):
            leftNum+=1
            leftDatas.append(currentNode.datas[i])
            if(left.get(currentNode.datas[i][CLASS_INDEX])==None):
                left[currentNode.datas[i][CLASS_INDEX]]=1
            else:
                left[currentNode.datas[i][CLASS_INDEX]]+=1
        else:
            rightNum+=1
            rightDatas.append(currentNode.datas[i])
            if(right.get(currentNode.datas[i][CLASS_INDEX])==None):
                right[currentNode.datas[i][CLASS_INDEX]]=1
            else:
                right[currentNode.datas[i][CLASS_INDEX]]+=1

    currentNode.leftNode=node()
    currentNode.leftNode.datas=leftDatas[:]
    currentNode.rightNode=node()
    currentNode.rightNode.datas=rightDatas[:]


    if(len(left)>1):
        CalTree(currentNode.leftNode,mode,ratio)
    elif(len(left)==1):
        currentNode.leftNode.answer=list(left.keys())[0]

    if(len(right)>1):
        CalTree(currentNode.rightNode,mode,ratio)  
    elif(len(right)==1):
        currentNode.rightNode.answer=list(right.keys())[0]

def CalTree_CON(currentNode,mode,currentNum,maxLimit):
    if(currentNum<=maxLimit):
        global ATTRIBUTE_NUM
        global CLASS_INDEX
        if(mode==0):
            ATTRIBUTE_NUM=4
            CLASS_INDEX=4
        elif(mode==1):
            ATTRIBUTE_NUM=32
            CLASS_INDEX=1
        elif(mode==2):
            ATTRIBUTE_NUM=10
            CLASS_INDEX=10
        elif(mode==3):
            ATTRIBUTE_NUM=13
            CLASS_INDEX=0

        best_choice=[0,0]
        best_value=0
        current={}
        for k in range(len(currentNode.datas)):
            if(current.get(currentNode.datas[k][CLASS_INDEX])==None):
                current[currentNode.datas[k][CLASS_INDEX]]=1
            else:
                current[currentNode.datas[k][CLASS_INDEX]]+=1

        recordAttribute=[]
        # for i in range(2,ATTRIBUTE_NUM):
        ATTRIBUTE=math.floor(math.sqrt(ATTRIBUTE_NUM))

        for _ in range(ATTRIBUTE):
            if(mode==0):
                i=random.randint(0,ATTRIBUTE_NUM-1)
                while(i in recordAttribute):
                    i=random.randint(0,ATTRIBUTE_NUM-1)
                recordAttribute.append(i)
            elif(mode==1):
                i=random.randint(2,ATTRIBUTE_NUM-1)
                while(i in recordAttribute):
                    i=random.randint(2,ATTRIBUTE_NUM-1)
                recordAttribute.append(i)
            elif(mode==2):
                i=random.randint(1,ATTRIBUTE_NUM-1)
                while(i in recordAttribute):
                    i=random.randint(1,ATTRIBUTE_NUM-1)
                recordAttribute.append(i)
            elif(mode==3):
                i=random.randint(1,ATTRIBUTE_NUM-1)
                while(i in recordAttribute):
                    i=random.randint(1,ATTRIBUTE_NUM-1)
                recordAttribute.append(i)

            sorted(currentNode.datas,key=lambda l:l[i], reverse=True)
            for j in range(len(currentNode.datas)-1):
                interval=((float(currentNode.datas[j][i])+float(currentNode.datas[j+1][i]))/2)
                left={}
                right={}
                for k in range(len(currentNode.datas)):
                    if(float(currentNode.datas[k][i])<interval):
                        if(left.get(currentNode.datas[k][CLASS_INDEX])==None):
                            left[currentNode.datas[k][CLASS_INDEX]]=1
                        else:
                            left[currentNode.datas[k][CLASS_INDEX]]+=1

                    else:
                        if(right.get(currentNode.datas[k][CLASS_INDEX])==None):
                            right[currentNode.datas[k][CLASS_INDEX]]=1
                        else:
                            right[currentNode.datas[k][CLASS_INDEX]]+=1


                value=CalGini(current,left,right)

                if(best_value<value):
                    best_value=value
                    best_choice=[i,interval]

        currentNode.condition=best_choice

        leftDatas=[]
        rightDatas=[]

        left={}
        right={}
        leftNum=0
        rightNum=0
        for i in range(len(currentNode.datas)):
            if(float(currentNode.datas[i][best_choice[0]])<best_choice[1]):
                leftNum+=1
                leftDatas.append(currentNode.datas[i])
                if(left.get(currentNode.datas[i][CLASS_INDEX])==None):
                    left[currentNode.datas[i][CLASS_INDEX]]=1
                else:
                    left[currentNode.datas[i][CLASS_INDEX]]+=1
            else:
                rightNum+=1
                rightDatas.append(currentNode.datas[i])
                if(right.get(currentNode.datas[i][CLASS_INDEX])==None):
                    right[currentNode.datas[i][CLASS_INDEX]]=1
                else:
                    right[currentNode.datas[i][CLASS_INDEX]]+=1

        currentNode.leftNode=node()
        currentNode.leftNode.datas=leftDatas[:]
        currentNode.rightNode=node()
        currentNode.rightNode.datas=rightDatas[:]


        if(len(left)>1):
            if(currentNum+1<=maxLimit):
                return CalTree_CON(currentNode.leftNode,mode,currentNum+1,maxLimit)
            else:
                tmp=0
                for key in left.keys():
                    if(left[key]>tmp):
                        tmp=left[key]
                        currentNode.leftNode.answer=key
        elif(len(left)==1):
            currentNode.leftNode.answer=list(left.keys())[0]

        if(len(right)>1):
            if(currentNum+1<=maxLimit):
                return CalTree_CON(currentNode.rightNode,mode,currentNum+1,maxLimit)
                
            else:
                tmp=0
                for key in right.keys():
                    if(right[key]>tmp):
                        tmp=right[key]
                        currentNode.rightNode.answer=key
        elif(len(right)==1):
            currentNode.rightNode.answer=list(right.keys())[0]



def EXCalTree(currentNode,mode):
    global ATTRIBUTE_NUM
    global CLASS_INDEX
    if(mode==0):
        ATTRIBUTE_NUM=4
        CLASS_INDEX=4
    elif(mode==1):
        ATTRIBUTE_NUM=32
        CLASS_INDEX=1
    elif(mode==2):
        ATTRIBUTE_NUM=10
        CLASS_INDEX=10
    elif(mode==3):
        ATTRIBUTE_NUM=13
        CLASS_INDEX=0

    best_choice=[0,0]
    current={}
    for k in range(len(currentNode.datas)):
        if(current.get(currentNode.datas[k][CLASS_INDEX])==None):
            current[currentNode.datas[k][CLASS_INDEX]]=1
        else:
            current[currentNode.datas[k][CLASS_INDEX]]+=1


    if(mode==0):
        y=random.randint(0,ATTRIBUTE_NUM-1)
    elif(mode==1):
        y=random.randint(2,ATTRIBUTE_NUM-1)
    elif(mode==2):
        y=random.randint(1,ATTRIBUTE_NUM-1)
    elif(mode==3):
        y=random.randint(1,ATTRIBUTE_NUM-1)

    sorted(currentNode.datas,key=lambda l:l[y], reverse=True)
    x=random.randint(0,len(currentNode.datas)-2)
    interval=((float(currentNode.datas[x][y])+float(currentNode.datas[x+1][y]))/2)

    best_choice=[y,interval]
    currentNode.condition=best_choice
    leftDatas=[]
    rightDatas=[]
 
    left={}
    right={}
 
    leftNum=0
    rightNum=0
    record=[]
    for i in range(len(currentNode.datas)):
        if(float(currentNode.datas[i][best_choice[0]])==best_choice[1]):
            record.append(i)
        if(float(currentNode.datas[i][best_choice[0]])<best_choice[1]):
            leftNum+=1
            leftDatas.append(currentNode.datas[i])
            if(left.get(currentNode.datas[i][CLASS_INDEX])==None):
                left[currentNode.datas[i][CLASS_INDEX]]=1
            else:
                left[currentNode.datas[i][CLASS_INDEX]]+=1
        else:
            rightNum+=1
            rightDatas.append(currentNode.datas[i])
            if(right.get(currentNode.datas[i][CLASS_INDEX])==None):
                right[currentNode.datas[i][CLASS_INDEX]]=1
            else:
                right[currentNode.datas[i][CLASS_INDEX]]+=1


    currentNode.leftNode=node()
    currentNode.leftNode.datas=leftDatas[:]
    currentNode.rightNode=node()
    currentNode.rightNode.datas=rightDatas[:]


    if(len(left)>1):
        currentNode.leftNode.datas=leftDatas[:]
        EXCalTree(currentNode.leftNode,mode)
    elif(len(left)==1):
        currentNode.leftNode.answer=list(left.keys())[0]
    elif(len(left)==0):
        currentNode.leftNode.answer=currentNode.datas[record[0]][best_choice[0]]
        

    if(len(right)>1):
        EXCalTree(currentNode.rightNode,mode)  
    elif(len(right)==1):
        currentNode.rightNode.answer=list(right.keys())[0]
    elif(len(right)==0):
        currentNode.leftNode.answer=currentNode.datas[record[0]][best_choice[0]]

def SearchTree(currentNode,value):
    if(currentNode.leftNode!=None or currentNode.rightNode!=None):
        if(currentNode.leftNode!=None and float(value[currentNode.condition[0]])<currentNode.condition[1]):
            return SearchTree(currentNode.leftNode,value)
        else:
            return SearchTree(currentNode.rightNode,value)
    else:
        if(currentNode.answer==value[CLASS_INDEX]):
            return 1
        else:
            return 0

class node():
    def __init__(self):
        self.leftNode=None
        self.rightNode=None
        self.datas=[]
        self.condition=[0,0]
        self.answer=""







####read file#####
dataSet=[]
fp=open("iris.txt","r")
line=fp.readline()

while line:
    line=line[0:-1]
    data=line.split(',')
    dataSet.append(data)
    line=fp.readline()
dataSet.pop()
fp.close()
#####
dataSet2=[]
fp2=open("wdbc.txt","r")
line=fp2.readline()

while line:
    line=line[0:-1]
    data=line.split(',')
    dataSet2.append(data)
    line=fp2.readline()
    
dataSet2.pop()
fp2.close()
#####
dataSet3=[]
fp3=open("glass.txt","r")
line=fp3.readline()

while line:
    line=line[0:-1]
    data=line.split(',')
    dataSet3.append(data)
    line=fp3.readline()
    
dataSet3.pop()
fp3.close()

dataSet4=[]
fp4=open("wine.txt","r")
line=fp4.readline()

while line:
    line=line[0:-1]
    data=line.split(',')
    dataSet4.append(data)
    line=fp4.readline()
    
dataSet4.pop()
fp4.close()

####################first####################
# begin=time.time()

# avgCorrectRate=0
# for i in range(TREE_NUM):
#     print(i)
#     trainData=[]
#     testData=[]
#     subData=[]
#     DisbuteAllData(dataSet,trainData,testData)
#     TreeBagging(trainData,subData)
#     root=node()
#     root.datas=subData[:]

#     CalTree(root)

#     total=0
#     correct=0
#     for value in testData:
#         total+=1
#         correct+=SearchTree(root,value)

#     avgCorrectRate+=(correct/total)

# end= time.time()
# # print(avgCorrectRate/TREE_NUM)
# print("The Time with Attribute Begging : ",end-begin)
# print("The CorrectRate with Attribute Begging : ",avgCorrectRate/TREE_NUM)
####################first####################

####################second####################
# ratioCorrect=[]
# ratioNum=[1,2,3,4,5,6,7,8,9]

# for n in range(1,10):
#     print(n)
#     RATIO=0.1*n

#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet4,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree(root,3,0)
#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     ratioCorrect.append(avgCorrectRate/TREE_NUM)
 
# plt.title('wine_Ratio')
# plt.xlabel('ratioNum')
# plt.ylabel('ratioCorrect')
# plt.plot(ratioNum,ratioCorrect)
# plt.show()
####################second####################

####################third####################
# irisCorrect=[]
# wdbcCorrect=[]
# glassCorrect=[]
# wineCorrect=[]
# treeNum=[]

# for n in range(1,70):
#     print(n)
#     TREE_NUM=n
#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree(root,0,0)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     irisCorrect.append(avgCorrectRate/TREE_NUM)

#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet2,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree(root,1,n)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     wdbcCorrect.append(avgCorrectRate/TREE_NUM)

#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet3,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree(root,2,n)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     glassCorrect.append(avgCorrectRate/TREE_NUM)

#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet4,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree(root,3,n)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     wineCorrect.append(avgCorrectRate/TREE_NUM)
#     treeNum.append(n)

# plt.title('Number of trees in the forest')
# plt.xlabel('TreeNum')
# plt.ylabel('Correct')


# plt.plot(treeNum,irisCorrect,label='iris', color='red')
# plt.plot(treeNum,wdbcCorrect,label='wdbc', color='blue')
# plt.plot(treeNum,glassCorrect,label='glass', color='orange')
# plt.plot(treeNum,wineCorrect,label='wine', color='green')
# plt.legend(loc='best')
# plt.show()
# plt.close()
####################third####################

####################fourth####################
# irisCorrect=[]
# wdbcCorrect=[]
# glassCorrect=[]
# wineCorrect=[]
# treeNum1=[]
# treeNum2=[]
# treeNum3=[]
# treeNum4=[]

# for n in range(1,5):
#     print(n)
#     TREE_NUM=10
#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree(root,0,n)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     irisCorrect.append(avgCorrectRate/TREE_NUM)
#     treeNum1.append(n)
# plt.title('Number of attributes at each node splitting')
# plt.xlabel('attributeNum')
# plt.ylabel('Correct')
# plt.plot(treeNum1,irisCorrect,label='iris', color='red')
# plt.legend(loc='best')
# plt.show()
# plt.close()


# for n in range(1,31):
#     TREE_NUM=10
#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet2,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree(root,1,n)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     wdbcCorrect.append(avgCorrectRate/TREE_NUM)
#     treeNum2.append(n)
# plt.title('Number of attributes at each node splitting')
# plt.xlabel('attributeNum')
# plt.ylabel('Correct')
# plt.plot(treeNum2,wdbcCorrect,label='wdbc', color='blue')
# plt.legend(loc='best')
# plt.show()
# plt.close()

# for n in range(1,10):
#     print(n)
#     TREE_NUM=10
#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet3,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree(root,2,n)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     glassCorrect.append(avgCorrectRate/TREE_NUM)
#     treeNum3.append(n)
# plt.title('Number of attributes at each node splitting')
# plt.xlabel('attributeNum')
# plt.ylabel('Correct')
# plt.plot(treeNum3,glassCorrect,label='glass', color='orange')
# plt.legend(loc='best')
# plt.show()
# plt.close()

    

# for n in range(1,13):
#     print(n)
#     TREE_NUM=10
#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet4,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree(root,3,n)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     wineCorrect.append(avgCorrectRate/TREE_NUM)
#     treeNum4.append(n)
# plt.title('Number of attributes at each node splitting')
# plt.xlabel('attributeNum')
# plt.ylabel('Correct')
# plt.plot(treeNum4,wineCorrect,label='wine', color='green')
# plt.legend(loc='best')
# plt.show()
# plt.close()

####################fourth####################

####################fifth####################
# irisCorrect=[]
# wdbcCorrect=[]
# glassCorrect=[]
# wineCorrect=[]
# treeNum=[]

# for n in range(1,15):
#     print(n)
#     TREE_NUM=10
#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree_CON(root,0,0,n)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     irisCorrect.append(avgCorrectRate/TREE_NUM)

#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet2,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree_CON(root,1,0,n)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     wdbcCorrect.append(avgCorrectRate/TREE_NUM)

#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet3,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree_CON(root,2,0,n)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     glassCorrect.append(avgCorrectRate/TREE_NUM)

#     avgCorrectRate=0
#     for i in range(TREE_NUM):
#         trainData=[]
#         testData=[]
#         subData=[]
#         DisbuteAllData(dataSet4,trainData,testData)
#         TreeBagging(trainData,subData)
#         root=node()
#         root.datas=subData[:]

#         CalTree_CON(root,3,0,n)

#         total=0
#         correct=0
#         for value in testData:
#             total+=1
#             correct+=SearchTree(root,value)

#         avgCorrectRate+=(correct/total)

#     wineCorrect.append(avgCorrectRate/TREE_NUM)
#     treeNum.append(n)

# plt.title('The maximize depth of tree')
# plt.xlabel('maximize depth')
# plt.ylabel('Correct')


# plt.plot(treeNum,irisCorrect,label='iris', color='red')
# plt.plot(treeNum,wdbcCorrect,label='wdbc', color='blue')
# plt.plot(treeNum,glassCorrect,label='glass', color='orange')
# plt.plot(treeNum,wineCorrect,label='wine', color='green')
# plt.legend(loc='best')
# plt.show()
# plt.close()
####################fifth####################

####################sixth####################

begin1=time.time()
avgCorrectRate1=0
for i in range(TREE_NUM):
    print(i)
    trainData=[]
    testData=[]
    subData=[]
    DisbuteAllData(dataSet4,trainData,testData)
    TreeBagging(trainData,subData)
    root=node()
    root.datas=subData[:]

    EXCalTree(root,3)

    total=0
    correct=0
    for value in testData:
        total+=1
        correct+=SearchTree(root,value)

    avgCorrectRate1+=(correct/total)
end1=time.time()

begin=time.time()
avgCorrectRate=0
for i in range(TREE_NUM):
    print(i)
    trainData=[]
    testData=[]
    subData=[]
    DisbuteAllData(dataSet4,trainData,testData)
    TreeBagging(trainData,subData)
    root=node()
    root.datas=subData[:]

    CalTree(root,3,0)

    total=0
    correct=0
    for value in testData:
        total+=1
        correct+=SearchTree(root,value)

    avgCorrectRate+=(correct/total)
end=time.time()
print("The CorrectRate of iris with random forest: ",avgCorrectRate/TREE_NUM)
print("The Time with random forest: ",end-begin)
print("The CorrectRate of iris with extremely random forest: ",avgCorrectRate1/TREE_NUM)
print("The Time with extremely random forest: ",end1-begin1)
####################sixth####################