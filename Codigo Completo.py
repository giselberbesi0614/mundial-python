import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import random
import threading
import time


class Estadio:
    def __init__(self, nombre, ciudad, capacidad):
        self.nombre = nombre
        self.ciudad = ciudad
        self.capacidad = capacidad

    def mostrar_info(self):
        return f"Estadio: {self.nombre}, Ciudad: {self.ciudad}, Capacidad: {self.capacidad}"


class Grupo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.equipos = []

    def agregar_equipo(self, equipo):
        self.equipos.append(equipo)

    def mostrar_info(self):
        info = f"Grupo: {self.nombre}\n"
        for equipo in self.equipos:
            info += equipo.mostrar_info() + "\n"
        return info


class Jugador:
    def __init__(self, nombre, edad, posicion):
        self.nombre = nombre
        self.edad = edad
        self.posicion = posicion
        self.goles = 0

    def mostrar_info(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Posición: {self.posicion}, Goles: {self.goles}"


class Equipo:
    def __init__(self, nombre, victorias=0, empates=0, derrotas=0):
        self.nombre = nombre
        self.victorias = victorias
        self.empates = empates
        self.derrotas = derrotas
        self.jugadores = []

    def agregar_jugador(self, jugador):
        self.jugadores.append(jugador)

    def mostrar_info(self):
        return f"Equipo: {self.nombre}\nVictorias: {self.victorias}\nEmpates: {self.empates}\nDerrotas: {self.derrotas}"


class Partido:
    def __init__(self, equipo_local, equipo_visitante, estadio, dia, hora):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.estadio = estadio
        self.dia = dia
        self.hora = hora
        self.resultado = None

    def jugar_partido(self, resultado):
        self.resultado = resultado

    def mostrar_resultado(self):
        if self.resultado:
            return f"Partido en {self.estadio.nombre} - {self.equipo_local.nombre} vs {self.equipo_visitante.nombre}: {self.resultado}"
        else:
            return f"Partido en {self.estadio.nombre} - {self.equipo_local.nombre} vs {self.equipo_visitante.nombre}: Aún no jugado"

    def mostrar_info(self):
        return f"Partido: {self.equipo_local.nombre} vs {self.equipo_visitante.nombre}\n" \
               f"Estadio: {self.estadio.nombre}\nCiudad: {self.estadio.ciudad}\nCapacidad: {self.estadio.capacidad}\n" \
               f"Día: {self.dia}\nHora: {self.hora}"


class MundialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mundial App")
        self.bg_color = "#2c3e50"
        self.fg_color = "#ecf0f1"
        self.root.configure(bg=self.bg_color)

        self.equipos = []
        self.grupos = {}
        self.partidos = []

        self.frame_left = tk.Frame(self.root, bg=self.bg_color)
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y)

        self.frame_right = tk.Frame(self.root, bg=self.bg_color)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.label_img = tk.Label(self.frame_left, bg=self.bg_color)
        self.label_img.pack()

        self.img = Image.open("trofeo.png")
        self.img = self.img.resize((200, 200), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img)
        self.label_img.config(image=self.img)

        self.combo = ttk.Combobox(self.frame_left, state="readonly", font=("Helvetica", 12))
        self.combo.pack(pady=20)
        self.combo.bind('<<ComboboxSelected>>', self.mostrar_info_equipo)

        self.info_text = tk.Text(self.frame_right, height=20, width=50, bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 12))
        self.info_text.pack(fill=tk.BOTH, expand=True)

        self.crear_menu()

        self.btn_admin_jugadores = tk.Button(self.frame_left, text="Administrar Jugadores", command=self.administrar_jugadores)
        self.btn_admin_jugadores.pack(pady=10)

        
        self.lbl_estadisticas = tk.Label(self.frame_right, bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 12))
        self.lbl_estadisticas.pack(fill=tk.X, padx=20, pady=10)

        self.actualizar_estadisticas_en_tiempo_real()

    def crear_menu(self):
        main_menu = tk.Menu(self.root)
        self.root.config(menu=main_menu)

        data_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Datos", menu=data_menu)
        data_menu.add_command(label="Cargar Datos", command=self.load_data)

        partido_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Partidos", menu=partido_menu)
        partido_menu.add_command(label="Mostrar Partidos", command=self.mostrar_partidos)

    def load_data(self):
        grupo_a = Grupo("Grupo A")
        grupo_a.agregar_equipo(Equipo("Argentina", 3, 1, 1))
        grupo_a.agregar_equipo(Equipo("Brazil", 2, 2, 1))

        grupo_b = Grupo("Grupo B")
        grupo_b.agregar_equipo(Equipo("Colombia", 2, 0, 1))

        grupo_c = Grupo("Grupo C")
        grupo_c.agregar_equipo(Equipo("Ecuador", 2, 1, 0))
        grupo_c.agregar_equipo(Equipo("Venezuela", 1, 1, 1))

        self.grupos = {"Grupo A": grupo_a, "Grupo B": grupo_b, "Grupo C": grupo_c}

        estadio1 = Estadio("Estadio Monumental", "Buenos Aires", 50000)
        estadio2 = Estadio("Maracaná", "Río de Janeiro", 70000)

        self.partidos = [
            Partido(grupo_a.equipos[0], grupo_a.equipos[1], estadio1, "2024-06-15", "18:00"),
            Partido(grupo_b.equipos[0], grupo_c.equipos[0], estadio2, "2024-06-16", "20:00")
        ]

        self.equipos = []
        for grupo in self.grupos.values():
            for equipo in grupo.equipos:
                self.equipos.append(equipo)

        self.combo['values'] = [equipo.nombre for equipo in self.equipos]
        self.combo.set("Seleccionar Equipo")

        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "Datos de ejemplo cargados.\n\n")

    def mostrar_info_equipo(self, event):
        equipo_nombre = self.combo.get()
        equipo = next((equipo for equipo in self.equipos if equipo.nombre == equipo_nombre), None)
        if equipo:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Nombre del Equipo: {equipo.nombre}\n\n")

            self.info_text.insert(tk.END, "Partidos:\n\n")
            for partido in self.partidos:
                if partido.equipo_local == equipo or partido.equipo_visitante == equipo:
                    self.info_text.insert(tk.END, partido.mostrar_info() + "\n\n")

    def mostrar_partidos(self):
        self.info_text.delete(1.0, tk.END)
        for partido in self.partidos:
            self.info_text.insert(tk.END, partido.mostrar_info() + "\n")
            self.info_text.insert(tk.END, "-" * 30 + "\n")

    def administrar_jugadores(self):
        top_admin_jugadores = tk.Toplevel(self.root)
        top_admin_jugadores.title("Administrar Jugadores")

        equipo_nombre = self.combo.get()
        equipo = next((equipo for equipo in self.equipos if equipo.nombre == equipo_nombre), None)

        if equipo:
            frame_jugadores = tk.Frame(top_admin_jugadores, bg=self.bg_color)
            frame_jugadores.pack(padx=20, pady=10)

            label_titulo = tk.Label(frame_jugadores, text=f"Jugadores de {equipo.nombre}", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 14, "bold"))
            label_titulo.pack(pady=10)

           
            for jugador in equipo.jugadores:
                label_jugador = tk.Label(frame_jugadores, text=f"{jugador.mostrar_info()}", bg=self.bg_color, fg=self.fg_color)
                label_jugador.pack()

            
            label_agregar = tk.Label(top_admin_jugadores, text="Agregar Nuevo Jugador:", bg=self.bg_color, fg=self.fg_color)
            label_agregar.pack(pady=10)

            frame_formulario = tk.Frame(top_admin_jugadores, bg=self.bg_color)
            frame_formulario.pack(padx=20, pady=10)

            label_nombre = tk.Label(frame_formulario, text="Nombre:", bg=self.bg_color, fg=self.fg_color)
            label_nombre.grid(row=0, column=0, padx=5, pady=5)
            entry_nombre = tk.Entry(frame_formulario)
            entry_nombre.grid(row=0, column=1, padx=5, pady=5)

            label_edad = tk.Label(frame_formulario, text="Edad:", bg=self.bg_color, fg=self.fg_color)
            label_edad.grid(row=1, column=0, padx=5, pady=5)
            entry_edad = tk.Entry(frame_formulario)
            entry_edad.grid(row=1, column=1, padx=5, pady=5)

            label_posicion = tk.Label(frame_formulario, text="Posición:", bg=self.bg_color, fg=self.fg_color)
            label_posicion.grid(row=2, column=0, padx=5, pady=5)
            entry_posicion = tk.Entry(frame_formulario)
            entry_posicion.grid(row=2, column=1, padx=5, pady=5)

            def agregar_nuevo_jugador():
                nombre = entry_nombre.get()
                edad = int(entry_edad.get())
                posicion = entry_posicion.get()

                nuevo_jugador = Jugador(nombre, edad, posicion)
                equipo.agregar_jugador(nuevo_jugador)

               
                label_jugador = tk.Label(frame_jugadores, text=f"{nuevo_jugador.mostrar_info()}", bg=self.bg_color, fg=self.fg_color)
                label_jugador.pack()

            btn_agregar = tk.Button(frame_formulario, text="Agregar Jugador", command=agregar_nuevo_jugador)
            btn_agregar.grid(row=3, columnspan=2, pady=10)

            def cerrar_ventana():
                top_admin_jugadores.destroy()

            btn_cerrar = tk.Button(top_admin_jugadores, text="Cerrar", command=cerrar_ventana)
            btn_cerrar.pack(pady=10)

    def actualizar_estadisticas_en_tiempo_real(self):
        def actualizar():
            while True:
                if self.partidos:
                    partido_actual = random.choice(self.partidos)
                    goles_local = random.randint(0, 3)
                    goles_visitante = random.randint(0, 2)
                    resultado = f"{partido_actual.equipo_local.nombre} {goles_local} - {goles_visitante} {partido_actual.equipo_visitante.nombre}"
                    self.lbl_estadisticas.config(text=f"Último partido: {resultado}")
                time.sleep(5)  

        threading.Thread(target=actualizar, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = MundialApp(root)
    root.mainloop()
