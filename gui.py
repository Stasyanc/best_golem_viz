import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from utils import draw_graphs_subplots
from examples.synthetic_graph_evolution.generators import generate_labeled_graph
import networkx as nx
import best_viz
import time

class Graph_gui:
    def __init__(self,master,target_graph,fit,best_fit,poses=[None,None]):
        self.master=master
        self.master.title("Best_Golem_Viz")
        self.target_graph=target_graph
        self.titles=['Old Graph: '+str(fit), 'Best Graph: '+str(best_fit)]
        self.poses=poses
        self.graph_frame = tk.Frame(self.master)
        draw_graphs_subplots(self.target_graph,self.target_graph,titles=self.titles,show=False,poses=self.poses)
        figure = plt.gcf() 
        self.canvas = FigureCanvasTkAgg(figure,self.graph_frame)
        self.canvas.draw()
        self.first_str=tk.Frame(self.master)
        self.fits=tk.Text(self.first_str,width=10,height=1)
        self.fits.insert("1.0",fit)
        self.fits_l=tk.Label(self.first_str,text="Old graph fits")
        self.best_fits=tk.Text(self.first_str,width=10,height=1)
        self.best_fits.insert("1.0",best_fit)
        self.best_fits_l=tk.Label(self.first_str,text="New graph fits")
        self.count_v_t=tk.Text(self.first_str,width=5,height=1)
        self.count_v_t.insert("1.0",16)
        self.count_v=tk.Label(self.first_str,text="Введите количество вершин")
        self.update_button=tk.Button(self.first_str,text="Запустить",command=self.update)
        self.quit_button = tk.Button(self.first_str, text="Выход", command=self.master.quit)
        self.second_str=tk.Frame(self.master)
        self.count_p=tk.Label(self.second_str,text="Количество поколений")
        self.size_p=tk.Label(self.second_str,text="Размер популяции")
        self.start_z=tk.Label(self.second_str,text="Начальная затравка")
        self.count_it=tk.Label(self.second_str,text="Количество итераций")
        self.count_p_t=tk.Text(self.second_str, width=5,height=1)
        self.count_p_t.insert("1.0",8)
        self.size_p_t=tk.Text(self.second_str, width=5,height=1)
        self.size_p_t.insert("1.0",6)
        self.start_z_t=tk.Text(self.second_str, width=5,height=1)
        self.start_z_t.insert("1.0",10)
        self.count_it_t=tk.Text(self.second_str, width=5,height=1)
        self.count_it_t.insert("1.0",100)
        self.third_str=tk.Frame(self.master)
        self.fit_old=tk.Label(self.third_str,text="Old Graph")
        self.fit_old_t=tk.Text(self.third_str,width=10,height=1)
        self.fit_old_t.insert("1.0",fit)
        self.fit_old=tk.Label(self.third_str,text="New Graph")
        self.fit_new_t=tk.Text(self.third_str,width=10,height=1)
        self.fit_new_t.insert("1.0",fit)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def window(self):   
        self.first_str.pack(side=tk.TOP,fill=tk.BOTH)
        self.second_str.pack(side=tk.TOP,fill=tk.BOTH)
        self.graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.count_v.pack(side=tk.LEFT)
        self.count_v_t.pack(side=tk.LEFT)
        self.update_button.pack(side=tk.LEFT)
        self.best_fits.pack(side=tk.RIGHT)
        self.best_fits_l.pack(side=tk.RIGHT)
        self.fits.pack(side=tk.RIGHT)
        self.fits_l.pack(side=tk.RIGHT)
        #self.quit_button.pack(side=tk.LEFT)
        self.count_p.pack(side=tk.LEFT)
        self.count_p_t.pack(side=tk.LEFT)
        self.size_p.pack(side=tk.LEFT)
        self.size_p_t.pack(side=tk.LEFT)
        self.start_z.pack(side=tk.LEFT)
        self.start_z_t.pack(side=tk.LEFT)
        self.count_it.pack(side=tk.LEFT)
        self.count_it_t.pack(side=tk.LEFT)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

    def update(self):
        count_v=int(self.count_v_t.get('1.0',tk.END))
        count_p=int(self.count_p_t.get('1.0',tk.END))
        size_p=int(self.size_p_t.get('1.0',tk.END))
        start_z=int(self.start_z_t.get('1.0',tk.END))
        count_it=int(self.count_it_t.get('1.0',tk.END))
        if count_v!='\n':
            node_types = ('a', 'b')
            target_graph = generate_labeled_graph('tree', int(count_v), node_labels=node_types)
            pos=nx.spring_layout(target_graph)
            fit = best_viz.vis_quality(target_graph,pos)
            best_pos,best_fit = best_viz.generate_best_viz(target_graph,pos,seed=start_z,iterations=count_it,pop_size=size_p,num_gen=count_p)
            self.target_graph=target_graph
            self.fits.insert("1.0",fit)
            self.best_fits.insert("1.0",best_fit)
            self.titles=['Old Graph: '+str(fit), 'Best Graph: '+str(best_fit)]
            self.poses=[pos,best_pos]
            draw_graphs_subplots(self.target_graph,self.target_graph,titles=self.titles,show=False,poses=self.poses)
            self.canvas.get_tk_widget().destroy()
            figure = plt.gcf() 
            self.canvas = FigureCanvasTkAgg(figure,self.graph_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    def on_closing(self):
        self.master.quit()

        
def create_window(target_graph,fit,best_fit,poses=[None,None]):
    start_t=time.time()
    root = tk.Tk()
    app = Graph_gui(root,target_graph,fit,best_fit,poses)
    app.window()
    root.geometry("1200x700")
    start_t=time.time()
    app.master.mainloop()

    return 1