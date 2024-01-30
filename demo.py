import matplotlib.pyplot as plt
from Intersect import SweepIntersector
import networkx as nx
import best_viz
from examples.synthetic_graph_evolution.generators import generate_labeled_graph
from utils import draw_graphs_subplots
import time

def test_viz(size=16):
    start_t=time.time()
    node_types = ('a', 'b')
    target_graph = generate_labeled_graph('tree', size, node_labels=node_types)
    pos=nx.spring_layout(target_graph)
    fit = best_viz.vis_quality(target_graph,pos)
    best_pos,best_fit,len_fit_table = best_viz.generate_best_viz(target_graph,pos)
    end_t=time.time()
    print("Всего размещений",len_fit_table)
    print(f"Время работы программы {(end_t-start_t):.03f}s")
    draw_graphs_subplots(target_graph, target_graph, titles=['Old Graph: '+str(fit), 'Best Graph: '+str(best_fit)],poses=[pos,best_pos])
    return target_graph


if __name__ == '__main__':
    print("Введите кол-во вершин")
    test_viz(int(input()))
