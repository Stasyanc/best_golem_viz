import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt
from examples.synthetic_graph_evolution.generators import generate_labeled_graph
from utils import draw_graphs_subplots

class Graph_gui:
    def __init__(self,master,target_graph,fit,best_fit,poses=[None,None]):
        self.master=master
        self.master.title("Best_Golem_Viz")
        
        draw_graphs_subplots(target_graph, target_graph,show=False, titles=['Old Graph: '+str(fit), 'Best Graph: '+str(best_fit)],poses=poses)
        figure = plt.gcf()
        self.canvas = FigureCanvasTkAgg(figure)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        ss=tk.Text(width=5,height=1)
        self.graph_frame = tk.Frame(self.master)
        self.graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
       # self.contents = tk.StringVar()
        quit_button = tk.Button(self.master, text="Выход", command=self.master.quit)
        quit_button.pack(side=tk.BOTTOM)
      #  ss.pack(side=tk.BOTTOM)