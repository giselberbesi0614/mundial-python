class Equipo:
    def __init__(self, nombre, victorias=0, empates=0, derrotas=0):
        self.nombre = nombre
        self.victorias = victorias
        self.empates = empates
        self.derrotas = derrotas

    def mostrar_info(self):
        return f"Equipo: {self.nombre}\nVictorias: {self.victorias}\nEmpates: {self.empates}\nDerrotas: {self.derrotas}"
