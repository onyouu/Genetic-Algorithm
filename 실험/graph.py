#ACG = Average Continuous Generation
#APG = Average Persistent Generation
import matplotlib.pyplot as plt


g100 = [3.5,3.7,3.4,4.5,4.7,4.5,5.0,4.5,5.1,4.3,5.1]
g500 = [3.0,8.8,10.2,13.1,10.9,11.9,11.1,10.9,9.3,10.4,11.4]
gp = [-0.5,5.1,6.8,8.6,6.2,7.4,6.1,6.4,4.2,6.1,6.3]
fake = [i for i in range(0,101,10)]

l=[[] for _ in range(11)]
for i in range(11):
    l[i].append(g100[i])
    l[i].append(g500[i])
    l[i].append(gp[i])
    l[i].append(i)
l.sort(key = lambda x:(x[2],x[1]), reverse=True)
for i in l:print(i[3]*10)

plt.figure(figsize=(10,6))
# plt.plot(fake,g100, label='100 ACG')
# plt.plot(fake,g500, label='500 ACG',color='orange')
plt.plot(fake,gp, label='100~500 APG',color='green')

plt.xticks(range(0, 101, 10))
plt.grid(axis='x', linestyle=':', color='gray', alpha=0.7)
plt.xlabel("Mutation Percent(%)")
plt.ylabel("Generation")
plt.legend()
plt.show()