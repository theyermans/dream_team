def ordenar_por_suma_robos_y_bloqueos(self):
    n = len(self.jugadores)
    max_suma_robos_bloqueos = max(
        jugador.estadisticas.robos_totales + jugador.estadisticas.bloqueos_totales
        for jugador in self.jugadores
    )

    for i in range(n):
        for j in range(0, n - i - 1):
            suma_robos_bloqueos_j = self.jugadores[j].estadisticas.robos_totales + self.jugadores[j].estadisticas.bloqueos_totales
            suma_robos_bloqueos_j1 = self.jugadores[j + 1].estadisticas.robos_totales + self.jugadores[j + 1].estadisticas.bloqueos_totales

            if suma_robos_bloqueos_j < suma_robos_bloqueos_j1:
                self.jugadores[j], self.jugadores[j + 1] = self.jugadores[j + 1], self.jugadores[j]

    cantidad_a_mostrar = int(input("Ingrese la cantidad de jugadores a mostrar: "))

    for idx, jugador in enumerate(self.jugadores[:cantidad_a_mostrar]):
        suma_robos_bloqueos = jugador.estadisticas.robos_totales + jugador.estadisticas.bloqueos_totales
        porcentaje = (suma_robos_bloqueos / max_suma_robos_bloqueos) * 100
        print(f"{idx + 1}. {jugador.nombre} - Suma de Robos y Bloqueos: {suma_robos_bloqueos} - Porcentaje: {porcentaje:.2f}%")
