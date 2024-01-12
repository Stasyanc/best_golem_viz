import matplotlib.pyplot as plt
from Intersect import SweepIntersector
import networkx as nx
import best_viz
from examples.synthetic_graph_evolution.generators import generate_labeled_graph
from utils import draw_graphs_subplots
from gui import create_window
import tkinter as tk

def test_viz_gui(size=16):
    tr=create_window(size)
    return tr


if __name__ == '__main__':
    test_viz_gui()
