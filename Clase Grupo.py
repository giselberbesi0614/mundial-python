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