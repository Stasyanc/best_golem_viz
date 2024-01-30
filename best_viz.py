import matplotlib.pyplot as plt
from Intersect import SweepIntersector
import networkx as nx
import math
import random
def count_intersect(G,pos):
    segList = []
    back_dict={}
    for i in G.edges:
        vs = (pos[i[0]][0],pos[i[0]][1])
        ve = (pos[i[1]][0],pos[i[1]][1])
        segList.append( (vs,ve) )
        back_dict[(vs,ve)]=i
    isector = SweepIntersector()
    isecDic = isector.findIntersections(segList)
    back_isecDic={}
    colper=0
    for i,v in isecDic.items():
        back_isecDic[back_dict[i]]=v
        colper+=len(v)-2
    return colper

def distance_proportion(pos):
    R_min=math.inf
    R_max=0
    for i,v in pos.items():
        for j,w in pos.items():
            if i!=j:
                R=(v[0]-w[0])**2+(v[1]-w[1])**2
                R_min=min(R,R_min)
                R_max=max(R,R_max)
    return math.sqrt(R_min/R_max)

def vis_quality(G,pos):
    return count_intersect(G,pos)+1-distance_proportion(pos)

def generate_best_viz(G,pos=None,seed=10,iterations=100,pop_size=6,num_gen=8):
    if pos == None:
        new_pos = nx.spring_layout(G,seed,iterations) #Передаем конкретное значение параметра seed, чтобы всегда получалось одно и то же размещение вершин
    else:
        new_pos=pos
    best_pos=new_pos
    best_fit=vis_quality(G,new_pos)
    pop=[]
    fit_table={}
    #Генерация начальной популяции
    for i in range(pop_size):
        p=(seed+i,iterations)
        pop.append(p)
        if p not in fit_table:
            new_pos = nx.spring_layout(G,seed=p[0],iterations=p[1])
            fit_table[p]=vis_quality(G,new_pos)
            if fit_table[p]<best_fit:
                best_fit=fit_table[p]
                best_pos=new_pos
    #Перебор поколений
    for gen in range(num_gen):
        #Мутации
        new_ind =[]
        for i,j in pop:
            p=(i,random.randint(j//2,j*2))
            new_ind.append(p)
            if p not in fit_table:
                new_pos = nx.spring_layout(G,seed=p[0],iterations=p[1])
                fit_table[p]=vis_quality(G,new_pos)
                if fit_table[p]<best_fit:
                    best_fit=fit_table[p]
                    best_pos=new_pos
        #Селекция
        pop=sorted(pop+new_ind,key=lambda p: fit_table[p],reverse=True)[:pop_size]
    return best_pos,best_fit,len(fit_table)
