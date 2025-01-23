import customtkinter as ctk
import threading
import random
import time

class ProcessManager:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Gestor de Procesos")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.processes = []
        
        self.setup_ui()

    def setup_ui(self):
        # Program name frame
        name_frame = ctk.CTkFrame(self.root)
        name_frame.grid(row=0, column=0, columnspan=6, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(name_frame, text="Nombre del programa").grid(row=0, column=0, padx=5)
        self.program_name = ctk.CTkEntry(name_frame, width=300)
        self.program_name.grid(row=0, column=1, padx=5)
        self.program_name.bind('<Return>', lambda e: self.add_program())
        
        ctk.CTkButton(name_frame, text="Agregar", command=self.add_program).grid(row=0, column=2, padx=5)

        # Process frame
        process_frame = ctk.CTkFrame(self.root)
        process_frame.grid(row=1, column=0, columnspan=6, padx=10, pady=5, sticky="ew")
        
        self.process_entries = {}
        process_names = ['A', 'B', 'C', 'D', 'E', 'F']
        
        for i, name in enumerate(process_names):
            ctk.CTkLabel(process_frame, text=f"Proceso {name}").grid(row=0, column=i, padx=5)
            entry = ctk.CTkEntry(process_frame, width=100, justify='center')
            entry.grid(row=1, column=i, padx=5, pady=5)
            self.process_entries[name] = entry

        # Progress frame
        progress_frame = ctk.CTkFrame(self.root)
        progress_frame.grid(row=2, column=0, columnspan=6, padx=10, pady=5, sticky="ew")
        
        self.progress_bars = {}
        for i, name in enumerate(process_names):
            ctk.CTkLabel(progress_frame, text=f"Proceso {name}").grid(row=i, column=0, padx=5, sticky="e")
            progress = ctk.CTkProgressBar(progress_frame, width=400)
            progress.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            progress.set(0)
            self.progress_bars[name] = progress

        # Button frame
        button_frame = ctk.CTkFrame(self.root)
        button_frame.grid(row=3, column=0, columnspan=6, padx=10, pady=5, sticky="ew")
        
        ctk.CTkButton(button_frame, text="Multiprogramación", 
                     command=self.show_multiprogramming).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Lotes", 
                     command=self.show_batches).grid(row=0, column=1, padx=5, pady=5)

    def add_program(self):
        name = self.program_name.get()
        if name:
            self.processes.append(name)
            for i, process_name in enumerate(self.process_entries.keys()):
                if i < len(self.processes):
                    self.process_entries[process_name].delete(0, ctk.END)
                    self.process_entries[process_name].insert(0, self.processes[i])
            self.program_name.delete(0, ctk.END)
            print(f"Programa agregado: {name}")

    def simulate_process(self, progress_bar, duration, callback=None):
        def run():
            progress_bar.set(0)
            for i in range(101):
                time.sleep(duration/100)
                progress_bar.set(i/100)
                self.root.update_idletasks()
            if callback:
                callback()
        return run

    def show_multiprogramming(self):
        print("Mostrando multiprogramación")
        for bar in self.progress_bars.values():
            bar.set(0)
            
        for name, bar in self.progress_bars.items():
            if self.process_entries[name].get():
                duration = random.uniform(1, 5)
                thread = threading.Thread(target=self.simulate_process(bar, duration))
                thread.daemon = True
                thread.start()

    def show_batches(self):
        print("Mostrando lotes")
        def process_next(index=0):
            if index >= len(self.progress_bars):
                return
                
            name = list(self.progress_bars.keys())[index]
            if self.process_entries[name].get():
                bar = self.progress_bars[name]
                thread = threading.Thread(
                    target=self.simulate_process(bar, 2, 
                    lambda: self.root.after(100, process_next, index + 1)))
                thread.daemon = True
                thread.start()
                
        for bar in self.progress_bars.values():
            bar.set(0)
            
        process_next()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ProcessManager()
    app.run()