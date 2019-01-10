import numpy as np
import random
import math

genmax=500
probability=60
mutation_step=0.0005
indiv_per_group=50
group_num=100
LEFT=-1
RIGHT=2
PI=3.1415926

class Individual():
    def __init__(self,x=0,fx=0,live=True):
        self.x=x
        self.fx=fx
        self.live=live

class Group():
    def __init__(self):
        self.best=Individual()
        self.best_gen=0
        self.cur_gen=0
        individiuals=[]
        for i in range(group_num):
            x=Individual() 
            individiuals.append(x)
        self.individiuals=individiuals
     
    def fx(self,x):
       # return x * math.sin(10 * PI * x) + 2.0
       return math.sin(PI*x)
    #------------------------------
    #总的启动函数，用于对进化过程的启动
    #------------------------------ 
    def sovel(self):
        self.init()
        for i in range(genmax):
            self.cur_gen=i
            self.assess()
            self.choose(self.cur_gen)
            self.cross()
            self.mutation()

    def init(self):
        self.best.fx=-0xffffffff
        self.best_gen=0
        self.cur_gen=0
        for i in range(indiv_per_group):
            t=np.random.randint(3001)
            x=(t/1000)-1
            self.individiuals[i].x=x
            self.individiuals[i].live=True
    
    def assess(self):
        for i in range(indiv_per_group):
            self.individiuals[i].fx=self.fx(self.individiuals[i].x)
            

    def choose(self,gen):
        totalFxvalue=0
        for i in range(indiv_per_group):
            totalFxvalue+=self.individiuals[i].fx
        self.best.fx=self.individiuals[0].fx
        self.best.x=self.individiuals[0].x
        tmp_add=0
        for i in range(indiv_per_group):
            t=random.random()
            tmp_add+=self.individiuals[i].fx
            tmp=tmp_add/totalFxvalue
            if tmp>=t:
                if self.individiuals[i].fx>self.best.fx:
                    self.best.fx=self.individiuals[i].fx
                    self.best.x=self.individiuals[i].x
                continue
            else :
                self.individiuals[i].live=False
        if self.best.fx >self.individiuals[0].fx:
            self.best_gen=gen


    def cross(self): 
        first=0
        second=0
        for i in range(indiv_per_group):
            if self.individiuals[i].live == False:
                while True:
                    first=random.randint(0,100)%indiv_per_group
                    if self.individiuals[first].live == True:
                        break
                    second=random.randint(0,100)%indiv_per_group
                    if  self.individiuals[second].live == True:
                       break
                diff=0
                tmp_x=0
                if self.individiuals[first].x >self.individiuals[second].x:
                   diff=self.individiuals[first].x-self.individiuals[second].x
                   tmp_x=random.random()*diff
                   tmp_x+=self.individiuals[second].x
                else:
                   diff=self.individiuals[second].x-self.individiuals[first].x
                   tmp_x=random.random()*diff
                   tmp_x+=self.individiuals[first].x
        
                tmp_fx=self.fx(tmp_x)
                if tmp_fx > self.individiuals[first].fx and tmp_fx > self.individiuals[second].fx:
                  self.individiuals[i].x=self.individiuals[first].x
                  self.individiuals[i].fx=self.individiuals[first].fx
                else:
                   if self.individiuals[first].fx > self.individiuals[second].fx:
                       self.individiuals[i].x=self.individiuals[first].x
                       self.individiuals[i].fx=self.individiuals[first].fx
                   else:
                       self.individiuals[i].x=self.individiuals[second].x
                       self.individiuals[i].fx=self.individiuals[second].fx
                self.individiuals[i].live=True
    
    def mutation(self):
        for i in range(indiv_per_group):
            if self.individiuals[i].live ==True:
                pro=random.randint(0,100)
                if pro>probability:
                     return
                t=random.random()
                if t>0.5:
                    self.individiuals[i].x+=mutation_step
                    if self.individiuals[i].x >RIGHT:
                         self.individiuals[i].x=LEFT
                    self.individiuals[i].fx=self.fx(self.individiuals[i].x)
                    if self.individiuals[i].fx > self.best.fx:
                         self.best.fx=self.individiuals[i].fx
                         self.best.x=self.individiuals[i].x
                else:
                    self.individiuals[i].x-=mutation_step
                    if self.individiuals[i].x <LEFT:
                         self.individiuals[i].x=RIGHT
                    self.individiuals[i].fx=self.fx(self.individiuals[i].x)
                    if self.individiuals[i].fx > self.best.fx:
                         self.best.fx=self.individiuals[i].fx
                         self.best.x=self.individiuals[i].x
                


if __name__ =="__main__":
    group=Group()
    bestsovel=[]
    for i in range(group_num):
       group.sovel()
       bestsovel.append([group.best.x,group.best.fx])
    print("输出每个种群的最优解：\n")
    for i in range(group_num):
        print(str(i)+"th:x="+str(bestsovel[i][0])+"  fx="+str(bestsovel[i][1]))
    max_fx = bestsovel[0][1]
    max_x=bestsovel[0][0]
    for i in range(group_num):
        if bestsovel[i][1]>max_fx:
            max_x=bestsovel[i][0]
            max_fx=bestsovel[i][1]

    print("所有种群的最优解：")
    print("x="+str(max_x)+"  fx="+str(max_fx))

       