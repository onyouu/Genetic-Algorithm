# 진화와 변이율의 상관관계를 알아보기 위한 자연을 단순화 시킬 프로그램 아이디어 생각해보기(숫자 합 좀 뻔하고 노잼)

import random
import numpy as np
from matplotlib import pyplot as plt

s=350 #목표
g=500 #세대
lim=100 #한계
fake=10 #변이율(%)
genom1 = [[random.randint(1,lim) for _ in range(4)] for _ in range(4)]
genom=[x[:] for x in genom1]
ab=[]
ac=[]

def ruleret(gene,target):
    p=[1/(abs(sum(x)-target)+1) for x in gene]
    pick=random.uniform(0,sum(p))
    num=0
    for ge,se in zip(gene,p):
        num+=se
        if num>pick:
            return ge[:]
        
# 유전자 교체 방식 1(랜덤 교차)       
for i in range(g):
        genom.sort(key= lambda x:abs(sum(x)-s))
        ac.append(sum(genom[0]))
        new_genom=[]
        for _ in range(4): #엘리트 보존시 2,아닐 시 4
            mom=ruleret(genom, s)
            dad=ruleret(genom, s)
            if random.randint(1,2)==1: # 하나의 유전자만 교체
                change=random.randint(0,3)
                mom[change]=dad[change]
                child=mom[:]
            else: # 연속된 두개의 유전자 교체
                cp = random.randint(0,1)
                ep = random.randint(1,3)
                mom[cp:cp+ep] = dad[cp:cp+ep][:]
                child=mom[:]
            if random.randint(1,100) <= fake:
                child[random.randint(0,3)]=random.randint(1,lim)
            new_genom.append(child)
        # genom=[x[:] for x in genom[:2]]+[x[:] for x in new_genom] #엘리트 보존 O
        genom=[x[:] for x in new_genom] #엘리트 보존 X
        
# 유전자 교체 방식 2(두 점 교차) - 이게 더 좋은 듯 
genom=[x[:] for x in genom1]
for i in range(g):
    genom.sort(key= lambda x:abs(sum(x)-s)) #적합도 평가
    ab.append(sum(genom[0]))
    new_genom=[]
    for _ in range(4): #엘리트 보존시 2,아닐 시 4
        #교차 연산
        mom=ruleret(genom, s)
        dad=ruleret(genom, s)
        cp = random.randint(0,1)
        ep = random.randint(1,3)
        mom[cp:cp+ep] = dad[cp:cp+ep][:]
        child=mom[:]
        #돌연변이 연산
        if random.randint(1,100) <= fake:
            child[random.randint(0,3)]=random.randint(1,lim)
        new_genom.append(child)
    genom=[x[:] for x in new_genom] #엘리트 보존 X

print(ab[0],ac[0])
plt.plot(ab, label="Best sum per generation(two croos)", color='blue')
plt.plot(ac, label="Best sum per generation(two and one croos)", color='green')
plt.axhline(y=s, color='red', linestyle='--', label=f"Target = {s}")
plt.xlabel("Generation")
plt.ylabel("Best Genome Sum")
plt.title("The sum of generations")
plt.legend()
plt.grid(True)
plt.show()