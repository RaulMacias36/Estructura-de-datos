import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class GrafoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TDA Grafo - Control por Coordenadas")
        self.root.geometry("1100x800")
        
        self.G = nx.DiGraph()
        self.pos = {}  # Diccionario de posiciones {nodo: [x, y]}
        
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel de Control (Izquierda)
        control_panel = tk.Frame(main_frame, width=280, bg="#2c3e50")
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        btn_style = {'font': ('Arial', 9), 'pady': 5, 'bg': '#ecf0f1', 'fg': '#2c3e50', 'cursor': 'hand2'}
        lbl_style = {'font': ('Arial', 10, 'bold'), 'bg': '#2c3e50', 'fg': 'white', 'pady': 8}

        # --- SECCIONES ---
        sections = [
            ("🛠️ ACTUALIZACIÓN", [
                ("➕ Insertar Vértice", self.ui_insertar_vertice),
                ("📍 Mover Nodo (x, y)", self.ui_mover_nodo),
                ("🔵 Arista No Dirigida", lambda: self.ui_insertar_arista(False)),
                ("🔴 Arista Dirigida", lambda: self.ui_insertar_arista(True)),
                ("🗑️ Eliminar Vértice", self.ui_eliminar_vertice),
                ("✂️ Eliminar Arista", self.ui_eliminar_arista),
            ]),
            ("🔍 CONSULTAS", [
                ("📊 Información G", self.ui_info_basica),
                ("degree(v)", self.ui_grado),
                ("Adyacentes(v)", self.ui_adyacentes),
            ])
        ]

        for title, btns in sections:
            tk.Label(control_panel, text=title, **lbl_style).pack(fill=tk.X)
            for txt, cmd in btns:
                tk.Button(control_panel, text=txt, command=cmd, **btn_style).pack(fill=tk.X, padx=10, pady=2)

        # Guía de Coordenadas
        tk.Label(control_panel, text="\n📍 PLANO CARTESIANO:\nUsa valores de 0 a 100\nEjemplo: (50, 50) es el centro.", 
                 bg="#2c3e50", fg="#f1c40f", font=("Arial", 9, "italic")).pack(pady=20)

        # Panel Visual
        self.viz_frame = tk.Frame(main_frame, bg="white")
        self.viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.viz_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.actualizar_dibujo()

    # --- NUEVA FUNCIÓN DE MOVIMIENTO POR COORDENADAS ---
    def ui_mover_nodo(self):
        v = simpledialog.askstring("Mover", "Nombre del vértice a mover:", parent=self.root)
        if v in self.G:
            try:
                x = simpledialog.askfloat("Coordenada X", "Ingresa X (0-100):", parent=self.root)
                y = simpledialog.askfloat("Coordenada Y", "Ingresa Y (0-100):", parent=self.root)
                if x is not None and y is not None:
                    self.pos[v] = [x, y]
                    self.actualizar_dibujo()
            except ValueError:
                messagebox.showerror("Error", "Debes ingresar números válidos.")
        else:
            messagebox.showwarning("Error", f"El vértice '{v}' no existe.")

    def ui_insertar_vertice(self):
        v = simpledialog.askstring("Nuevo Vértice", "Nombre:", parent=self.root)
        if v:
            self.G.add_node(v)
            if v not in self.pos:
                # Se inserta en una posición aleatoria inicial dentro del rango 0-100
                import random
                self.pos[v] = [random.randint(10, 90), random.randint(10, 90)]
            self.actualizar_dibujo()

    def ui_insertar_arista(self, dirigida):
        v = simpledialog.askstring("Origen", "De:", parent=self.root)
        w = simpledialog.askstring("Destino", "A:", parent=self.root)
        o = simpledialog.askstring("Etiqueta", "Info de arista (o):", parent=self.root)
        if v in self.G and w in self.G:
            self.G.add_edge(v, w, label=o, directed=dirigida)
            if not dirigida: self.G.add_edge(w, v, label=o, directed=dirigida)
            self.actualizar_dibujo()
        else:
            messagebox.showerror("Error", "Los vértices deben existir.", parent=self.root)

    # --- RESTO DE OPERACIONES ---
    def ui_info_basica(self): messagebox.showinfo("G", f"Nodos: {list(self.G.nodes())}\nAristas: {self.G.number_of_edges()}", parent=self.root)
    def ui_grado(self): 
        v = simpledialog.askstring("Grado", "Vértice:", parent=self.root)
        if v in self.G: messagebox.showinfo("Info", f"grado({v}) = {self.G.degree(v)}", parent=self.root)
    def ui_adyacentes(self):
        v = simpledialog.askstring("Ady", "Vértice:", parent=self.root)
        if v in self.G: messagebox.showinfo("Info", f"Adyacentes: {list(self.G.neighbors(v))}", parent=self.root)
    def ui_eliminar_vertice(self):
        v = simpledialog.askstring("Del", "Vértice:", parent=self.root)
        if v in self.G: self.G.remove_node(v); self.pos.pop(v, None); self.actualizar_dibujo()
    def ui_eliminar_arista(self):
        v = simpledialog.askstring("Del", "Origen:", parent=self.root); w = simpledialog.askstring("Del", "Destino:", parent=self.root)
        if self.G.has_edge(v,w): self.G.remove_edge(v,w); self.actualizar_dibujo()

    def actualizar_dibujo(self):
        self.ax.clear()
        if self.G.number_of_nodes() > 0:
            # Asegurar que todos tengan posición
            for n in self.G.nodes():
                if n not in self.pos: self.pos[n] = [50, 50]

            # Listas de aristas por tipo
            e_dir = [(u, v) for u, v, d in self.G.edges(data=True) if d.get('directed')]
            e_undir = [(u, v) for u, v, d in self.G.edges(data=True) if not d.get('directed')]

            # Dibujar Nodos
            nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color='#3498db', node_size=800, edgecolors='black')
            nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_color='white', font_weight='bold')

            # Dibujar Aristas (Rojo=Dirigida, Azul=NoDirigida)
            if e_dir:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=e_dir, ax=self.ax, 
                                       edge_color='red', width=2, arrows=True, arrowsize=20, 
                                       connectionstyle="arc3,rad=0.1")
            if e_undir:
                nx.draw_networkx_edges(self.G, self.pos, edgelist=e_undir, ax=self.ax, 
                                       edge_color='blue', width=2, arrows=False)

            # Etiquetas de aristas
            labels = nx.get_edge_attributes(self.G, 'label')
            nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=labels, ax=self.ax)

        # Configurar límites del plano para que no "baile" al mover nodos
        self.ax.set_xlim(-5, 105)
        self.ax.set_ylim(-5, 105)
        self.ax.set_axis_off()
        self.canvas.draw()
        self.toolbar.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = GrafoApp(root)
    root.mainloop()