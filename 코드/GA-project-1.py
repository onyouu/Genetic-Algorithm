# 유전 알고리즘 첫 시도(숫자 찾기)
# 변이율 10%
# 엘리트 보존 O -> 훨씬 빠르게 목표에 도달(평균적으로 256세대에 도달, 도달 실패 비율 0%) s=350, g=10000000, lim=100, test=500
# 엘리트 보존 X -> 보다 느리게 목표에 도달(평균적으로 1360세대에 도달, 도달 실패 비율 0%) s=350, g=10000000, lim=100, test=500
# 엘리트 보존 O -> 훨씬 빠르게 목표에 도달(평균적으로 192세대에 도달, 도달 실패 비율 3.8%) s=350, g=1000, lim=100, test=500
# 엘리트 보존 X -> 보다 느리게 목표에 도달(평균적으로 430세대에 도달, 도달 실패 비율 39.4%) s=350, g=1000, lim=100, test=500
# 문제점 
# 1. 도달하지 못한 경우는 포함시키지 않아서 원래 결과보다 낮은 값이 나올 가능성이 존재함
# 2. 랜덤한 수라 절대적으로 옳다고 보기 어려움
# 변이율이 높아질수록 더 빨리 목표에 도달함
# 돌연변이가 많으면 목표하는 개체에 도달을 빠르게 해서 유지 가능?(엘리트 보존 O)

import random
import numpy as np
from matplotlib import pyplot as plt

def ruleret(gene,target):
    p=[1/(abs(sum(x)-target)+1) for x in gene]
    pick=random.uniform(0,sum(p))
    num=0
    for ge,se in zip(gene,p):
        num+=se
        if num>pick:
            return ge[:]

s=350 #목표
g=1000 #세대
lim=100 #한계
test=500
fake=10 #변이율(%)
avg=[]
avg2=[]

for fake in range(1,101):
    elit=0 #도달 세대 총합
    elit2=0
    reached=0 #도달 세대 개수
    reached2=0
    for _ in range(test):
        genom1 = [[random.randint(1,lim) for _ in range(4)] for _ in range(4)]
        genom=[x[:] for x in genom1]
        ab=[]
        for i in range(g):
            genom.sort(key= lambda x:abs(sum(x)-s))
            ab.append(sum(genom[0]))
            if sum(genom[0])>=s:
                elit2+=i
                reached2+=1
                # print(sum(genom[0]))
                break
            new_genom=[]
            for _ in range(2): #엘리트 보존시 2,아닐 시 4
                mom=ruleret(genom,s)
                dad=ruleret(genom,s)
                if random.randint(1,2)==1: # 하나의 유전자만 교체
                    change=random.randint(0,3)
                    mom[change]=dad[change]
                    child=mom[:]
                else: # 연속된 두개의 유전자 교체
                    change=random.randint(0,2)
                    mom[change:change+2]=dad[change:change+2]
                    child=mom[:]
                if random.randint(1,100) <= fake:
                    child[random.randint(0,3)]=random.randint(1,lim)
                new_genom.append(child)
            genom=[x[:] for x in genom[:2]]+[x[:] for x in new_genom] #엘리트 보존 O
            #genom=[x[:] for x in new_genom] #엘리트 보존 X
        genom=[x[:] for x in genom1]
        for i in range(g):
            genom.sort(key= lambda x:abs(sum(x)-s))
            ab.append(sum(genom[0]))
            if sum(genom[0])>=s:
                elit+=i
                reached+=1
                # print(sum(genom[0]))
                break
            new_genom=[]
            for _ in range(4): #엘리트 보존시 2,아닐 시 4
                mom=ruleret(genom,s)
                dad=ruleret(genom,s)
                if random.randint(1,2)==1: # 하나의 유전자만 교체
                    change=random.randint(0,3)
                    mom[change]=dad[change]
                    child=mom[:]
                else: # 연속된 두개의 유전자 교체
                    change=random.randint(0,2)
                    mom[change:change+2]=dad[change:change+2]
                    child=mom[:]
                if random.randint(1,100) <= fake:
                    child[random.randint(0,3)]=random.randint(1,lim)
                new_genom.append(child)
            #genom=[x[:] for x in genom[:2]]+[x[:] for x in new_genom] #엘리트 보존 O
            genom=[x[:] for x in new_genom] #엘리트 보존 X

        #그래프
        # for x in genom:print(sum(x),x)
        # plt.figure(figsize=(10,5))
        # plt.plot(ab, label="Best sum per generation", color='blue')
        # plt.axhline(y=s, color='red', linestyle='--', label=f"Target = {s}")
        # plt.xlabel("Generation")
        # plt.ylabel("Best Genome Sum")
        # plt.title("GA Fitness Convergence")
        # plt.legend()
        # plt.grid(True)
        # plt.show()
    # if reached > 0:
    #     print("평균 도달 세대:", elit // reached)
    #     print("도달 실패 비율:", (test - reached) // test * 100,'%')
    # else:
    #     print("목표에 도달한 케이스 없음")
    avg.append(elit // reached)
    avg2.append(elit2 // reached2)

#그래프
plt.figure(figsize=(10,5))
plt.plot(np.arange(1,101),avg, color='blue') # 엘리트 보존 O 
plt.plot(np.arange(1,101),avg2, color='red') # 엘리트 보존 X
plt.legend()
plt.grid(True)
plt.show()