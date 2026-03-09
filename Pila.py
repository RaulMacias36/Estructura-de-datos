import tkinter as tk
from tkinter import messagebox

class PilaVisualMaestra:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Pila - Secuencia Automática y Manual")
        self.root.geometry("1100x750")
        self.root.configure(bg="#1a1b26")

        self.pilas = {"Principal": []}
        self.capacidad = 8
        self.temporales = [] 
        
        # Secuencia exacta de la imagen: I=Insertar, E=Eliminar
        self.secuencia = [
            ('I', 'X'), ('I', 'Y'), ('E', 'Z'), ('E', 'T'), ('E', 'U'),
            ('I', 'V'), ('I', 'W'), ('E', 'P'), ('I', 'R')
        ]
        self.indice_auto = 0
        
        self.setup_ui()

    def setup_ui(self):
        # --- PANEL DE CONTROL ---
        header = tk.Frame(self.root, bg="#24283b", pady=20)
        header.pack(side=tk.TOP, fill=tk.X)

        tk.Label(header, text="VALOR:", fg="#c0caf5", bg="#24283b", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=15)
        self.entry_val = tk.Entry(header, font=("Arial", 14), width=8, bg="#414868", fg="white", justify='center', insertbackground="white")
        self.entry_val.pack(side=tk.LEFT, padx=5)

        tk.Button(header, text="PUSH", command=self.push, bg="#9ece6a", fg="#1a1b26", font=("Arial", 9, "bold"), width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(header, text="POP SMART", command=self.smart_pop, bg="#f7768e", fg="#1a1b26", font=("Arial", 9, "bold"), width=12).pack(side=tk.LEFT, padx=5)
        
        # BOTÓN DE SECUENCIA AUTOMÁTICA
        self.btn_auto = tk.Button(header, text="EJECUTAR SECUENCIA (Auto)", command=self.iniciar_secuencia, 
                                  bg="#7aa2f7", fg="#1a1b26", font=("Arial", 10, "bold"), padx=10)
        self.btn_auto.pack(side=tk.RIGHT, padx=20)

        # --- ÁREA DE PILAS ---
        self.container = tk.Frame(self.root, bg="#1a1b26")
        self.container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # --- CONSOLA LOG ---
        log_frame = tk.Frame(self.root, bg="#16161e")
        log_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        tk.Label(log_frame, text=" HISTORIAL DE OPERACIONES", fg="#7aa2f7", bg="#16161e", font=("Arial", 9, "bold")).pack(anchor="w", padx=10)
        
        self.log = tk.Text(log_frame, height=12, bg="#16161e", fg="#a9b1d6", font=("Consolas", 11), bd=0, padx=15, pady=10)
        self.log.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        scrollbar = tk.Scrollbar(log_frame, command=self.log.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log.config(yscrollcommand=scrollbar.set)
        
        self.render()

    def render(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        for nombre, items in self.pilas.items():
            f = tk.Frame(self.container, bg="#24283b", bd=2, relief="flat", padx=15, pady=15)
            f.pack(side=tk.LEFT, padx=25, fill=tk.Y)
            
            tk.Label(f, text=nombre.upper(), bg="#24283b", fg="#7aa2f7", font=("Arial", 12, "bold")).pack(pady=10)
            
            c = tk.Canvas(f, width=130, height=400, bg="#1a1b26", highlightthickness=1, highlightbackground="#414868")
            c.pack()
            
            for i in range(self.capacidad):
                y_t, y_b = 400 - (i+1)*45, 400 - i*45
                color_celda = "#3d59a1" 
                if i < len(items) and items[i] in self.temporales:
                    color_celda = "#e0af68" # Dorado
                
                if i >= len(items): color_celda = "#24283b"
                c.create_rectangle(10, y_t, 120, y_b, fill=color_celda, outline="#565f89", width=2)
                
                if i < len(items):
                    c.create_text(65, y_t+22, text=items[i], fill="white", font=("Arial", 14, "bold"))
            
            if items:
                y_tp = 400 - (len(items)*45)
                c.create_text(65, y_tp-15, text="TOPE ⬇", fill="#f7768e", font=("Arial", 10, "bold"))

    def write_log(self, msg, tipo="INFO"):
        self.log.config(state='normal')
        tag = tipo.lower()
        self.log.insert(tk.END, f"[{tipo}] ", tag)
        self.log.insert(tk.END, f"{msg}\n")
        self.log.tag_config("aviso", foreground="#e0af68")
        self.log.tag_config("ok", foreground="#9ece6a")
        self.log.tag_config("aux", foreground="#bb9af7")
        self.log.tag_config("auto", foreground="#7aa2f7")
        self.log.see(tk.END)
        self.log.config(state='disabled')
        self.root.update_idletasks()

    # --- LÓGICA AUTOMÁTICA ---
    def iniciar_secuencia(self):
        if self.indice_auto < len(self.secuencia):
            tipo, valor = self.secuencia[self.indice_auto]
            self.write_log(f"EJECUTANDO PASO {self.indice_auto + 1}: {tipo}({valor})", "AUTO")
            self.btn_auto.config(state='disabled', text="PROCESANDO...")
            
            if tipo == 'I':
                self.entry_val.delete(0, tk.END)
                self.entry_val.insert(0, valor)
                self.push()
                self.indice_auto += 1
                self.root.after(1500, self.iniciar_secuencia)
            else:
                self.entry_val.delete(0, tk.END)
                self.entry_val.insert(0, valor)
                self.smart_pop()
                # El smart_pop tiene sus propios callbacks .after, 
                # así que necesitamos esperar a que terminen antes del siguiente paso
                tiempo_espera = 2500 if valor not in self.pilas["Principal"] else 4000
                self.indice_auto += 1
                self.root.after(tiempo_espera, self.iniciar_secuencia)
        else:
            self.write_log("SECUENCIA COMPLETA FINALIZADA.", "OK")
            self.btn_auto.config(state='normal', text="REINICIAR SECUENCIA")
            self.indice_auto = 0

    # --- LÓGICA MANUAL (MANTENIDA) ---
    def push(self):
        val = self.entry_val.get().upper().strip()
        if val and len(self.pilas["Principal"]) < self.capacidad:
            self.pilas["Principal"].append(val)
            self.write_log(f"PUSH: {val} en Principal.", "OK")
            self.render()
            if not self.btn_auto['state'] == 'disabled': self.entry_val.delete(0, tk.END)

    def smart_pop(self):
        obj = self.entry_val.get().upper().strip()
        if not obj: return
        p_main = self.pilas["Principal"]

        if obj not in p_main:
            self.write_log(f"ELIMINAR {obj}: No existe. Iniciando creación visual.", "AVISO")
            self.temporales.append(obj)
            p_main.append(obj)
            self.render()
            self.root.after(1500, lambda: self.finish_fake_pop(obj))
            return

        if p_main[-1] != obj:
            self.write_log(f"ELIMINAR {obj}: Atrapado. Usando Auxiliar.", "AUX")
            self.pilas["Auxiliar"] = []
            self.render()
            self.root.after(800, lambda: self.move_to_aux(obj))
        else:
            p_main.pop()
            self.write_log(f"POP: {obj} eliminado del tope.", "OK")
            self.render()
            if not self.btn_auto['state'] == 'disabled': self.entry_val.delete(0, tk.END)

    def finish_fake_pop(self, obj):
        if obj in self.pilas["Principal"]:
            self.pilas["Principal"].pop()
            if obj in self.temporales: self.temporales.remove(obj)
            self.write_log(f"ÉXITO: {obj} eliminado tras creación visual.", "OK")
            self.render()
            if not self.btn_auto['state'] == 'disabled': self.entry_val.delete(0, tk.END)

    def move_to_aux(self, obj):
        p_main, p_aux = self.pilas["Principal"], self.pilas.get("Auxiliar", [])
        if p_main and p_main[-1] != obj:
            temp = p_main.pop()
            p_aux.append(temp)
            self.write_log(f"MOVIENDO: {temp} a Auxiliar.", "AUX")
            self.render()
            self.root.after(600, lambda: self.move_to_aux(obj))
        elif p_main:
            p_main.pop()
            self.write_log(f"ÉXITO: {obj} eliminado.", "OK")
            self.render()
            self.root.after(1000, self.return_to_main)

    def return_to_main(self):
        if self.pilas.get("Auxiliar"):
            temp = self.pilas["Auxiliar"].pop()
            self.pilas["Principal"].append(temp)
            self.write_log(f"REGRESANDO: {temp} a Principal.", "AUX")
            self.render()
            self.root.after(600, self.return_to_main)
        else:
            if "Auxiliar" in self.pilas: del self.pilas["Auxiliar"]
            self.write_log("ESTRUCTURA RESTAURADA.", "OK")
            self.render()
            if not self.btn_auto['state'] == 'disabled': self.entry_val.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PilaVisualMaestra(root)
    root.mainloop()