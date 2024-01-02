import matplotlib.pyplot as plt
from Intersect import SweepIntersector
import networkx as nx
import best_viz
from examples.synthetic_graph_evolution.generators import generate_labeled_graph
from utils import draw_graphs_subplots
from gui import Graph_gui
import tkinter as tk

def test_viz(size=16,type=None):
    node_types = ('a', 'b')
    target_graph = generate_labeled_graph('tree', size, node_labels=node_types)
    pos=nx.spring_layout(target_graph)
    fit = best_viz.vis_quality(target_graph,pos)
    best_pos,best_fit = best_viz.generate_best_viz(target_graph,pos)
    if type!=None:
        draw_graphs_subplots(target_graph, target_graph, titles=['Old Graph: '+str(fit), 'Best Graph: '+str(best_fit)],poses=[pos,best_pos])
    else:
        root = tk.Tk()
        app = Graph_gui(root,target_graph,fit,best_fit,poses=[pos,best_pos])
        app.window()
        root.geometry("1200x700")
        root.mainloop()
    return target_graph


if __name__ == '__main__':
    test_viz()
