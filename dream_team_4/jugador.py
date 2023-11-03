from colorama import Fore, Style
from estadisticas import Estadisticas

class Jugador:
    def __init__(self, nombre, posicion, estadisticas, logros,nombre_equipo):
        self._nombre = nombre
        self._posicion = posicion
        self._estadisticas:Estadisticas = estadisticas
        self._logros = logros
        self._nombre_equipo = nombre_equipo
    @property
    def nombre(self):
        return self._nombre

    @property
    def posicion(self):
        return self._posicion

    @property
    def estadisticas(self):
        return self._estadisticas

    @property
    def logros(self):
        return self._logros

    
    @property
    def nombre_equipo(self):
        return self._nombre_equipo
    #permite ser printeable
    def __str__(self):
        return f"Nombre: {self.nombre}, Posición: {self.posicion}, Estadísticas: {self.estadisticas}, Logros: {self.logros}, Equipo: {self.nombre_equipo}"
    
    def mostrar_logros(self):
        for logro in self.logros:
            print(Fore.YELLOW+logro+Style.RESET_ALL)