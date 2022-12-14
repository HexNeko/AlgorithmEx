import numpy as np
import copy
import random

#城市距离矩阵
city_num = 5
city_dist_mat = np.zeros([city_num, city_num])
city_dist_mat[0][1] = city_dist_mat[1][0] = 1165
city_dist_mat[0][2] = city_dist_mat[2][0] = 1462
city_dist_mat[0][3] = city_dist_mat[3][0] = 3179
city_dist_mat[0][4] = city_dist_mat[4][0] = 1967
city_dist_mat[1][2] = city_dist_mat[2][1] = 1511
city_dist_mat[1][3] = city_dist_mat[3][1] = 1942
city_dist_mat[1][4] = city_dist_mat[4][1] = 2129
city_dist_mat[2][3] = city_dist_mat[3][2] = 2677
city_dist_mat[2][4] = city_dist_mat[4][2] = 1181
city_dist_mat[3][4] = city_dist_mat[4][3] = 2216

#定义个体类，包括基因（城市路线）和适应度
class Individual:
    def __init__(self, genes = None):
        self.genes = genes
        self.fitness = None

        global city_num
        #基因用城市序列表示，必从0开始
        if self.genes == None:
            #如果初始没有基因，则随机产生
            temp = [i for i in range(1,city_num)]
            random.shuffle(temp)
            genes = [0] + temp[:]
            self.genes = genes
        #个体适应度
        self.fitness = self.evaluate_fitness()

    #定义小于比较，用于实现锦标赛算法选择种群
    def __lt__(self,other):
        return self.fitness < other.fitness

    #计算个体的适应度 也就是距离的总和
    def evaluate_fitness(self):
        dis = 0
        for i in range(city_num):
            if i == city_num - 1:
                dis += city_dist_mat[self.genes[i]][0]#回到0
            else:
                dis += city_dist_mat[self.genes[i]][self.genes[i+1]]
        return dis

#定义GeneticAlgorithm类 
#3交叉、变异、更新种群，全部在Ga类中实现
class GeneticAlgorithm:
    #input_为城市间的距离矩阵
    def __init__(self):
        self.best = Individual(None)
        #种群
        self.individual_list = []
        
    #交叉
    #交叉规则：对于parent1,parnet2分别从中抽取连续的长度为num_cross的基因作为子代的同位置基因
    #剩余部分则选择另一个父辈的基因，按顺序填入
    def cross(self):
        new_gen = []
        #随机选取一段，含有num_cross个数字（城市）
        num_cross = 3
        for i in range(0, len(self.individual_list) - 1, 2):
            #将上一代根据奇偶数分为两个种群
            parent_gen1 = self.individual_list[i].genes[:]
            parent_gen2 = self.individual_list[i+1].genes[:]
            #随机从两个父代中抽取num_cross长度的基因
            index_random = [i for i in range(1,city_num - num_cross + 1)]
            start_index1 = random.choice(index_random)
            end_index1 = start_index1+num_cross
            start_index2 = random.choice(index_random)
            end_index2 = start_index2+num_cross
            choice_list1 = parent_gen1[start_index1:end_index1]
            choice_list2 = parent_gen2[start_index2:end_index2]
            #利用这一段生成两个子代
            #用于复制对应段后的补全
            temp1=[i for i in parent_gen2 if i not in choice_list1]
            temp2=[i for i in parent_gen1 if i not in choice_list2]
            #生成子代
            son_gen1 = temp1[:start_index1]+choice_list1+temp1[start_index1:]
            son_gen2 = temp2[:start_index1]+choice_list2+temp2[start_index1:]
            #将这两个子代放入种群
            new_gen.append(Individual(son_gen1))
            new_gen.append(Individual(son_gen2))
        return new_gen
        
    #变异
    #变异规则：随机挑选两个位置然后交换位置
    def mutate(self, new_gen):
        change = 0
        mutate_p = 0.05 #变异个体的比例
        index_1 = 1
        index_2 = 1
        index_list = [i + 1 for i in range(city_num - 1)]
        for individual in new_gen:
            if random.random() < mutate_p:
                change += 1
                #如果变异，采用基于位置的变异,方便起见，直接使用上面定义的index列表
                index_l = random.choice(index_list)
                index_2 = random.choice(index_list)
                while index_1 == index_2:
                    index_2 = random.choice(index_list)
                #交换
                temp = individual.genes[index_1]
                individual.genes[index_1] = individual.genes[index_2]
                individual.genes[index_2] = temp
        #变异结束，与老一代的进行合并
        self.individual_list += new_gen
        print("变异个数:%d"%(change))

    #采用锦标赛算法选择
    def select(self):
        #在此选用锦标赛算法
        group_num = 30
        group_size = 4
        win_num = 2
        #锦标赛的胜者列表
        winners = []
        for i in range(group_num):
            group = []
            for j in range(group_size):
                group.append(random.choice(self.individual_list))
            #存储完一组之后选出适应度最大的前2个
            group.sort()
            winners += group[: win_num]
        #将胜者作为新的种群
        self.individual_list = winners

    #更新种群
    def next_gen(self):
        #交叉
        new_gene = self.cross()
        #变异
        self.mutate(new_gene)
        #选择
        self.select()
        #获得这一代的最佳个体
        print('best genens = ', self.best.genes)
        print('best fitness = ', self.best.fitness)
        for individual in self.individual_list:
            if individual.fitness < self.best.fitness:
                self.best = individual
    #开始训练
    def train(self):
        #随机出初代种群#
        individual_num = 60
        self.individual_list = [Individual() for i in range(individual_num)]
        #迭代次数
        gen_num = 100
        result,fitness=0,0
        for i in range(gen_num):
            #从当代种群中交叉、变异、选择出适应度最佳的个体，获得子代产生新的种群
            print('************迭代第%d次************'%(i))
            self.next_gen()
        print('\n\n最终结果是：',self.best.genes+[self.best.genes[0]])
        print('距离总和是：', self.best.fitness)

if __name__ == '__main__':
    route = GeneticAlgorithm()
    route.train()