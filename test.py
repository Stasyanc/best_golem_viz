import matplotlib.pyplot as plt
from Intersect import SweepIntersector
import networkx as nx
import best_viz
from examples.synthetic_graph_evolution.generators import generate_labeled_graph
from utils import draw_graphs_subplots
import time

def test_viz(seed,iteration,pop_size,num_gen,size):
    test_table_f.write(str(j) + '\t')
    test_table_f.write(str(N)+'\t')
    test_table_f.write(str(pop_size)+'\t')
    test_table_f.write(str(num_gen)+'\t')
    test_table_f.write(str(iteration)+'\t')
    test_table_f.write(str(seed)+'\t')
    node_types = ('a', 'b')
    target_graph = generate_labeled_graph('tree', size,node_labels=1)
    mv=max(len(target_graph._succ[i])+len(target_graph._pred[i]) for i in range(size))
    start_t1=time.time()
    pos=nx.spring_layout(target_graph)
    end_t1=time.time()
    fit = best_viz.vis_quality(target_graph,pos)
    test_table_f.write(str(fit)+'\t')
    start_t2=time.time()
    best_pos,best_fit,len_fit_table = best_viz.generate_best_viz(target_graph,pos,seed=seed,iterations=iteration,pop_size=pop_size,num_gen=num_gen)
    end_t2=time.time()
    test_table_f.write(str(best_fit)+'\t')
    test_table_f.write(str(end_t1-start_t1)+'\t')
    test_table_f.write(str(end_t2-start_t2)+'\t')
    test_table_f.write(str(mv)+'\t')
    test_table_f.write(str(len_fit_table)+'\n')
    plt.close()
    s=str(j)
    s="0"*(4-len(s))+s
    draw_graphs_subplots(target_graph, target_graph,poses=[pos,best_pos],show=False,path_to_save="test/pic/"+str(size)+"_"+s+".png",titles=["Было:"+str(fit),"Стало:"+str(best_fit)])
    print(str(j)+" граф:\t",file=test_max_v_f)
    print(target_graph._adj,file=test_max_v_f)
    return target_graph


if __name__ == '__main__':
    print("Введите количество вершин")
    N=int(input()) #Размер графа
    print("Введите количество графов")
    count=int(input()) #Количество запусков
    seed=10 #Затравка
    iteration=100 #Количество итераций
    pop_size=20 #Размер популяции
    num_gen=2 #Количество поколений
    test_table_f=open('test/test_table.txt','w')
    test_max_v_f=open('test/test_max_vertex.txt','w')
    test_table_f.write("Номер теста\tКол верш\tРазм поп\tКол пок\tКол ит\tЗатравка\tФитнес было\tФитнес стало\tВремя было\tВремя стало\tМакс степень вершины\tВсего размещений\n")
    for j in range(1,count+1):
        test_viz(size=N,seed=seed,iteration=iteration,pop_size=pop_size,num_gen=num_gen)
    test_table_f.close()
    test_max_v_f.close()
