#-*- coding:utf-8 -*-
#传教士(野人)的数量，船的载重
num,boat_load=0,0

class State:
    '''m,c表示起始岸传教士和野人数量,b表示船的状态,1在起始岸0在目标岸'''
    def __init__(self,m,c,b):
        self.m=m
        self.c=c
        self.b=b
    def __eq__(self,other):
        if self.m==other.m and self.c==other.c and self.b==other.b:
            return True
        else:
            return False

class Node:
    '''搜索节点'''
    def __init__(self,state,step,parent):
        self.state=state
        self.step=step
        self.parent=parent

    def __lt__(self,node):
        return self.estimate(self)<self.estimate(node)

    def __str__(self):
        #便于输出节点状态
        out_str='第%2d步:   '%(self.step)
        out_str+='m:%2d-c:%2d   '%(self.state.m,self.state.c)+'B'*self.state.b
        out_str+='-'*6
        out_str+='B'*(1-self.state.b)+'   m:%2d-c:%2d'%(num-self.state.m,num-self.state.c)
        return out_str

    def estimate(self,node):
        #估价函数f*(n)=g*(n)+h*(n)
        #起始岸 f = step + 2*(m + c - b)/(boat_load-1) + 1
        #目标岸 f = step + 2*(m + c + 1 - b)/(boat_load-1) + 2
        if node.state.b == 1:
            return node.step+2*(node.state.m+node.state.c-boat_load)/(boat_load-1)+1
        else:
            return node.step+2*(node.state.m+node.state.c+1-boat_load)/(boat_load-1)+2

    def is_safe(self):
        #是否是合法状态
        if self.state.m==self.state.c:
            return True
        elif self.state.m==0 or self.state.m==num:
            return True
        else:
            return False

    def is_exist(self,open,close):
        #是否已经有这个状态
        for node in open:
            if self.state == node.state:
                return False
        for node in close:
            if self.state == node.state:
                return False
        return True

    def in_boat(self,node):
        #用于测试，输出船上的认识和方向
        boat_m=self.state.m-node.state.m
        boat_c=self.state.c-node.state.c
        if boat_m>=0 and boat_c>=0:
            return '<--(m:%d,c:%d)'%(boat_m,boat_c)
        else:
            return '-->(m:%d,c:%d)'%(abs(boat_m),abs(boat_c))

def solution(num,boat_load):
    start_node=Node(State(num,num,1),0,None)
    open=[start_node]
    goal_state=State(0,0,0)
    close=[]
    #循环直到找到目标状态或者open表为空
    while True:
        if not open:
            print('失败')
            break
        node=open.pop(0)
        close.append(node)
        state=node.state
        if node.state==goal_state:
            #success
            output_steps(node)
            break
        elif state.b==1:
            #如果船在起始岸
            #船上全是野人
            for c in range(1,min(boat_load,state.c)+1):
                new_node=Node(State(state.m,state.c-c,1-state.b),node.step+1,node)
                if new_node.is_safe() and new_node.is_exist(open,close):
                    open.append(new_node)
            #船上全是传教士或者既有传教士又有野人
            for m in range(1,min(boat_load,state.m)+1):
                for c in range(0,min(m,state.c)+1):
                    if m+c>boat_load :
                        break
                    new_node=Node(State(state.m-m,state.c-c,1-state.b),node.step+1,node)
                    if new_node.is_safe() and new_node.is_exist(open,close):
                        open.append(new_node)
        elif node.state.b==0:
            #如果船在目标岸
            #船上全是野人
            for c in range(1,min(boat_load,num-state.c)+1):
                new_node=Node(State(state.m,state.c+c,1-state.b),node.step+1,node)
                if new_node.is_safe() and new_node.is_exist(open,close):
                    open.append(new_node)
            #船上全是传教士或者既有传教士又有野人
            for m in range(1,min(boat_load,num-state.m)+1):
                for c in range(0,min(m,num-state.c)+1):
                    if(m+c>boat_load):
                        break
                    new_node=Node(State(state.m+m,state.c+c,1-state.b),node.step+1,node)
                    if new_node.is_safe() and new_node.is_exist(open,close):
                        open.append(new_node)
        #根据估价函数进行排序
        open.sort()
        
def output_steps(node):
    '''输出转移过程'''
    print('共进行了%d步'%(node.step))
    print('-步数---+---起始岸--+---河流---+--目标岸---+-----船只---')
    steps=[]
    while node.parent!=None:
        steps.append(node)
        node=node.parent
    steps.append(node)
    last_step=None
    for step in steps[::-1]:
        if last_step:
            print(str(step)+' '*3+step.in_boat(last_step))
            last_step=step
        else:
            last_step=step
            print(str(step))

if __name__=='__main__':
    num=int(input("输入传教士和野人的总数："))
    while num%2 != 0:
        print("ERROR:因为野人和传教士人数相同，所以总数一定是正偶数")
        num=int(input("输入传教士和野人的总数："))
    num=int(num/2)
    boat_load=int(input("输入船的满载人数："))
    solution(num,boat_load)

