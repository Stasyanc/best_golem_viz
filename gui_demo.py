import matplotlib.pyplot as plt
from Intersect import SweepIntersector
import networkx as nx
import best_viz
from examples.synthetic_graph_evolution.generators import generate_labeled_graph
from utils import draw_graphs_subplots
from gui import create_window
import tkinter as tk

def test_viz_gui(size=16):
    node_types = ('a', 'b')
    target_graph = generate_labeled_graph('tree', size, node_labels=node_types)
    pos=nx.spring_layout(target_graph)
    fit = best_viz.vis_quality(target_graph,pos)
    best_pos,best_fit = best_viz.generate_best_viz(target_graph,pos)
    create_window(target_graph,fit,best_fit,poses=[pos,best_pos])
    return target_graph


if __name__ == '__main__':
    test_viz_gui()
