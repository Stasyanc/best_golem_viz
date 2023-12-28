import matplotlib.pyplot as plt
from Intersect import SweepIntersector
import networkx as nx
import best_viz
from examples.synthetic_graph_evolution.generators import generate_labeled_graph
from utils import draw_graphs_subplots

def test_viz(size=16):
    # Generate target graph that will be sought by optimizer
    node_types = ('a', 'b')
    target_graph = generate_labeled_graph('tree', size, node_labels=node_types)
    pos=nx.spring_layout(target_graph)
    fit = best_viz.vis_quality(target_graph,pos)
    best_pos,best_fit = best_viz.generate_best_viz(target_graph,pos)
    draw_graphs_subplots(target_graph, target_graph, titles=['Old Graph: '+str(fit), 'Best Graph: '+str(best_fit)],poses=[pos,best_pos])
    return target_graph


if __name__ == '__main__':
    """
    In this example Optimizer is expected to find the target graph
    using Tree Edit Distance metric and a random tree (nx.random_tree) as target.
    The convergence can be seen from achieved metrics and visually from graph plots.
    """
    print("Введите кол-во вершин")
    test_viz(size=int(input()))
