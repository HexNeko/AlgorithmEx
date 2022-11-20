#-*- coding:utf-8 -*-

#目标状态
goal=None

class Node:
    '''搜索节点'''
    def __init__(self,code,zero_pos,step,parent):
        self.code=code #八数码内容
        self.x,self.y=zero_pos #空位坐标
        self.step=step
        self.parent=parent
    
    def __eq__(self,other):
        if other!=None and self.code==other.code:
            return True
        else:
            return False
        
    def __lt__(self,node):
        return estimate(self)<estimate(node)

    def __str__(self):
        #便于输出节点状态
        out_str='**第%d步**\n'%(self.step)
        out_str+=str(self.code[0])+'\n'+str(self.code[1])+'\n'+str(self.code[2])+'\n'
        return out_str

    def possible_child(self):
        #可能的子节点状态
        res=[]
        for x,y in [(0,1),(0,-1),(1,0),(-1,0)]:
            if self.x+x>=0 and self.x+x<3 and self.y+y>=0 and self.y+y<3:
                new_code=[[i for i in j] for j in self.code]
                #交换数字位置
                new_code[self.x][self.y]=new_code[self.x+x][self.y+y]
                new_code[self.x+x][self.y+y]=0
                #创建新节点
                new_node=Node(new_code,(self.x+x,self.y+y),self.step+1,self)
                res.append(new_node)
        return res

def estimate(node):
    '''估价函数f*(n)=g*(n)+h*(n)
    已走步数加错误位置数字个数'''
    unsame_nums=0
    for i in range(0,3):
        for j in range(0,3):
            if node.code[i][j]!=goal[i][j] and node.code[i][j]!=0:
                unsame_nums+=1
    return node.step+unsame_nums

def solution(start):
    '''开始求解'''
    #首先找到空位置
    x,y=0,0
    for i in range(0,3):
        for j in range(0,3):
            if start[i][j]==0:
                x,y=i,j
                break
    start_node=Node(start,(x,y),0,None)
    open=[start_node]
    close=[]
    #循环直到找到目标状态或者open表为空
    while True:
        if not open:
            print('失败')
            break
        node=open.pop(0)
        close.append(node)
        if node.code==goal:
            #success
            output_steps(node)
            break
        else:
            for next in node.possible_child():
                if not (next in open or next in close):
                    open.append(next)
        open.sort()
        
def output_steps(node):
    '''输出转移过程'''
    print('共进行了%d步\n'%(node.step))
    steps=[]
    while node.parent!=None:
        steps.append(node)
        node=node.parent
    steps.append(node)
    for step in steps[::-1]:
        print(step)

if __name__=='__main__':
    start,end=[],[]
    print('输入初始状态，分三行输入：')
    for i in range(0,3):
        start.append([int(i) for i in input().split()])
    print('输入目标状态，分三行输入：')
    for i in range(0,3):
        end.append([int(i) for i in input().split()])
    goal=end
    solution(start)

