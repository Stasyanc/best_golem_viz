import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from utils import draw_graphs_subplots
from examples.synthetic_graph_evolution.generators import generate_labeled_graph
import networkx as nx
import best_viz

class Graph_gui:
    def __init__(self,master,target_graph,fit,best_fit,poses=[None,None]):
        self.master=master
        self.master.title("Best_Golem_Viz")
        self.target_graph=target_graph
        self.titles=['Old Graph: '+str(fit), 'Best Graph: '+str(best_fit)]
        self.poses=poses
        draw_graphs_subplots(self.target_graph,self.target_graph,titles=self.titles,show=False,poses=self.poses)
        figure = plt.gcf() 
        self.canvas = FigureCanvasTkAgg(figure)
        self.canvas.draw()
        self.textbox=tk.Text(width=5,height=1)
        self.update_button=tk.Button(self.master,text="Запустить",command=self.update)
        self.graph_frame = tk.Frame(self.master)
        self.quit_button = tk.Button(self.master, text="Выход", command=self.master.quit)

    def window(self):
        self.textbox.pack(side=tk.TOP)
        self.update_button.pack(side=tk.TOP)
        self.quit_button.pack(side=tk.TOP)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update(self):
        self.canvas.get_tk_widget().destroy()
        s=self.textbox.get('1.0',tk.END)
        node_types = ('a', 'b')
        target_graph = generate_labeled_graph('tree', int(s), node_labels=node_types)
        pos=nx.spring_layout(target_graph)
        fit = best_viz.vis_quality(target_graph,pos)
        best_pos,best_fit = best_viz.generate_best_viz(target_graph,pos)
        self.target_graph=target_graph
        self.titles=['Old Graph: '+str(fit), 'Best Graph: '+str(best_fit)]
        self.poses=[pos,best_pos]
        draw_graphs_subplots(self.target_graph,self.target_graph,titles=self.titles,show=False,poses=self.poses)
        figure = plt.gcf() 
        self.canvas = FigureCanvasTkAgg(figure)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)