

import copy
import csv
import json
import os
import re

from colorama import Fore,Style
from estadisticas import Estadisticas
from jugador import Jugador
#from parcial import guardar_csv


class Equipo:
    def __init__(self):
        self.jugadores: list[Jugador] = []
        self._nombre = ""
    @property
    def nombre(self):
        return self._nombre
    @nombre.setter#agrega el nombre en una clase variable privada
    def nombre(self,new):
        self._nombre=new
    #1)



    def cargar_desde_json(self, archivo_json):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as file:
                dream_team = json.load(file)
                jugadores_data = dream_team['jugadores']
                nombre_de_equipo = dream_team['equipo']
                for jugador_data in jugadores_data:
                    estadisticas = Estadisticas(**jugador_data['estadisticas'])  # desempaqueta el diccionario
                    jugador = Jugador(jugador_data['nombre'], jugador_data['posicion'], estadisticas, jugador_data['logros'], nombre_de_equipo)
                    self.jugadores.append(jugador)
        except FileNotFoundError:
            print("El archivo no se encontró.")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar el JSON: {e}")
        except KeyError as e:
            print(f"Error de clave en el JSON: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

            
                

    def mostrar_jugadores(self,solo_nombre:bool):
        """print nombre / posicion de los jugadores en clase jugadres
        si es True solo nombres
        si es False nombres y posicion"""        
        for jugador in self.jugadores:
            if solo_nombre:
                print(Fore.GREEN+jugador.nombre+Style.RESET_ALL)
            else:
                print(Fore.GREEN+jugador.nombre +" - "+jugador.posicion+Style.RESET_ALL  )
                
    #2)
    def mostrar_estadisticas_jugador(equipo,es_guardar:bool):
        """recibe la clase
        si True ademas guarda en csv
        print jugadores enumerados //consulta indice // lo valida si es un numero // si esta entre 0 y jugadores enumerados print a estadisticas
            """
        #muestro las opciones/jugadores        
        for numero, jugador in enumerate(equipo.jugadores):
            print(Fore.GREEN+f"{numero}: Nombre: {jugador.nombre}, Posición: {jugador.posicion}"+Style.RESET_ALL)
        indice = input(Fore.YELLOW+"\nSeleccione el índice del jugador para ver sus estadísticas: \n"+Style.RESET_ALL)
        
        while True:
            try:
                #equipo.jugadores es equivalente a una lista con todos los diccionarios 1 por jugador
                if 0 <= int(indice) < len(equipo.jugadores):
                    jugador_seleccionado = equipo.jugadores[int(indice)]
                    mensaje = f"""
Estadísticas completas de {jugador_seleccionado.nombre}:
    Puntos:
        Temporadas jugadas: {jugador_seleccionado.estadisticas.temporadas_jugadas}
        Puntos totales: {jugador_seleccionado.estadisticas.puntos_totales}
        Promedio de Puntos p/Partido: {jugador_seleccionado.estadisticas.promedio_puntos_por_partido}
    Rebotes:
        Rebotes totales: {jugador_seleccionado.estadisticas.rebotes_totales}
        Promedio de Rebotes p/Partido: {jugador_seleccionado.estadisticas.promedio_rebotes_por_partido}
    Asistencias:
        Asistencias Totales: {jugador_seleccionado.estadisticas.asistencias_totales}
        Promedio de Asistencias p/Partido: {jugador_seleccionado.estadisticas.promedio_asistencias_por_partido}
    Robos y Bloqueos:
        Robos Totales: {jugador_seleccionado.estadisticas.robos_totales}
        Bloqueos Totales: {jugador_seleccionado.estadisticas.bloqueos_totales}
    Porcentajes de Tiros:
        Porcentaje de Tiros de Campo: {jugador_seleccionado.estadisticas.porcentaje_tiros_de_campo}
        Porcentaje de Tiros Libres: {jugador_seleccionado.estadisticas.porcentaje_tiros_libres}
        Porcentaje de Tiros Triples: {jugador_seleccionado.estadisticas.porcentaje_tiros_triples}
"""
                    print(Fore.GREEN+mensaje+Style.RESET_ALL)
                    #ENCABEZADO
                    
                    
                    #True
                    if es_guardar:
                       equipo.guardar_estadisticas_como_csv(jugador_seleccionado)
                    #   equipo.guardar_csv(jugador_seleccionado)                        
                    break
                else:
                    print(Fore.RED+"Índice fuera de rango. Ingrese un índice válido, reinicio"+Style.RESET_ALL)
                    break
            except ValueError:
                print(Fore.RED+"Entrada inválida. Ingrese un número válido para el índice del jugador, reinicio"+Style.RESET_ALL)
                break
                
                
        
    #3 mejora

    def guardar_estadisticas_como_csv(self,jugador_seleccionado:Jugador):
        
        estadisticas = [
            jugador_seleccionado.nombre,
            jugador_seleccionado.estadisticas.temporadas_jugadas,
            jugador_seleccionado.estadisticas.puntos_totales,
            jugador_seleccionado.estadisticas.promedio_puntos_por_partido,
            jugador_seleccionado.estadisticas.rebotes_totales,
            jugador_seleccionado.estadisticas.promedio_rebotes_por_partido,
            jugador_seleccionado.estadisticas.asistencias_totales,
            jugador_seleccionado.estadisticas.promedio_asistencias_por_partido,
            jugador_seleccionado.estadisticas.robos_totales,
            jugador_seleccionado.estadisticas.bloqueos_totales,
            jugador_seleccionado.estadisticas.porcentaje_tiros_de_campo,
            jugador_seleccionado.estadisticas.porcentaje_tiros_libres,
            jugador_seleccionado.estadisticas.porcentaje_tiros_triples
        ]

        nombre_archivo = 'estadisticas_jugador.csv'
        #nombre_jugaor = jugador_seleccionado.nombre   #hay que sumarlo al texto y se va generando un csv por cada jugador con el encabezado
        modo_apertura = 'a' if os.path.exists(nombre_archivo) else 'w'
        try:
            with open(nombre_archivo, mode=modo_apertura, newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if file.tell() == 0:#primera vuelta del encabezado
                    writer.writerow([
                        "Jugador", "Temporadas", "Puntos totales", "Promedios pt por partido",
                        "Rebotes totales", "Promedio rebotes", "Asistencias totales", "Promedio asistencias",
                        "Robos totales", "Bloqueos totales", "Tiros campo pct", "Tiros libres pct", "Tiros triples pct"
                    ])
                writer.writerow(estadisticas)
            print(Fore.GREEN+"Estadísticas del jugador guardadas en estadisticas_jugador.csv"+Style.RESET_ALL)
        except IOError as e:
            print(Fore.RED+f"Error al guardar las estadísticas, : {e}(reinicio)"+Style.RESET_ALL)

    #4
    def seleccion_jugador(equipo):
        """valide la seleccion"""
        print(Fore.YELLOW+"La lista de jugadores por equipo para seleccionar es:"+Style.RESET_ALL) 
        equipo.mostrar_jugadores(True)
        seleccion = input("Selecciona el nombre de un jugador en la lista para ver sus logros(mientras mas especifico el tipeo del nombre mas unica es la coincidencia)\n")
        flag=True
        for index,jugador in enumerate(equipo.jugadores):
            if re.search(seleccion,jugador.nombre,re.IGNORECASE) :
            
                    flag=False
                    print(Fore.GREEN+f"El numero N°{index} jugador encontrado es: {jugador.nombre} y sun logros son:"+Style.RESET_ALL)
                    jugador.mostrar_logros()
        if flag:
            print(Fore.RED+"No se encontro ningun resultado"+Style.RESET_ALL)
            
            

    #5


    def mostrar_promedio_puntos(self, jugadores: list[Jugador]):
        """Calcular y mostrar el promedio de puntos por partido de todo el equipo del Dream Team, ordenado por nombre de manera ascendente."""
        suma_promedio = 0
        jugadores_ordenados = sorted(jugadores, key=lambda jugador: jugador.nombre)

        cantidad_jugadores_validos = 0  # Contador para jugadores con valores válidos

        for jugador in jugadores_ordenados:
            promedio_puntos = jugador.estadisticas.promedio_puntos_por_partido

            if promedio_puntos is not None and promedio_puntos != 0:
                print(Fore.GREEN + f"Nombre: {jugador.nombre} - Promedio de puntos: {promedio_puntos}" + Style.RESET_ALL)
                suma_promedio += promedio_puntos
                cantidad_jugadores_validos += 1

        if cantidad_jugadores_validos > 0:
            promedio_equipo = suma_promedio / cantidad_jugadores_validos
            print(Fore.BLUE + f"Promedio de todo el equipo es de: {promedio_equipo}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "No hay datos válidos para calcular el promedio del equipo." + Style.RESET_ALL)

        
    #6
    def verificar_salon_fama(self,jugadores:list[Jugador]):
        flag_jugador_no_encontrado = True
           
        nombre_seleccionado = input("\nEscribe un nombre o apellido completo de un jugador para chekear que este en el Salon de la Fama\n")
        
        for jugador in jugadores:
            if re.search(nombre_seleccionado,jugador.nombre,re.IGNORECASE):
                jugador_encontrado=jugador
                flag_jugador_no_encontrado = False
                break
        if flag_jugador_no_encontrado:
            print(Fore.RED+"jugador no identificado"+Style.RESET_ALL)
        else:
            if Equipo.buscar_si_esta_en_fama_logros(jugador_encontrado.logros):
                print(Fore.GREEN+"El jugador  se encuentra en el Salon de la Fama del Baloncesto"+Style.RESET_ALL)
            else:
                print(Fore.RED + " El jugador no se encuentra en el Salon de la Fama del Baloncesto"+Style.RESET_ALL)
                    
                
        
    
    def buscar_si_esta_en_fama_logros(logros:list[str]) -> bool:
        patron = r'^'+"Miembro del Salon de la Fama del Baloncesto"+ r'$' 
        #texto_sin_despues_baloncesto = re.sub(patron, "Baloncesto")
        for logro in logros:
            if re.search(patron,logro,):
                return True
        return False
        
    #7  Calcular y mostrar el jugador con la mayor cantidad de rebotes totales
    def calcular_rebotes_totales_mayor(self,jugadores:list[Jugador]):
        jugador_max_rebotes = max(jugadores,key=lambda jugador:jugador.estadisticas.rebotes_totales)
        print(Fore.GREEN+f"El jugador con mayor cantidad de rebotes totales es: {jugador_max_rebotes.nombre} con {jugador_max_rebotes.estadisticas.rebotes_totales} rebotes"+Style.RESET_ALL)
    #8  
    def ordernar_listado_robos_totales(self):
        
        n = len(self.jugadores)

        for i in range(n):
            for j in range(0, n-i-1):
                if self.jugadores[j].estadisticas.robos_totales < self.jugadores[j+1].estadisticas.robos_totales:
                    self.jugadores[j], self.jugadores[j+1] = self.jugadores[j+1], self.jugadores[j]
        for i in self.jugadores:
            print(i.nombre+" - "+ str(i._estadisticas.robos_totales))
        self.guardar_jugadores_csv()
        
        
    def guardar_jugadores_csv(self):
        estadisticas = []
        for jugador_seleccionado in self.jugadores:
            estadisticas.append ([
                jugador_seleccionado.nombre,
                jugador_seleccionado.estadisticas.temporadas_jugadas,
                jugador_seleccionado.estadisticas.puntos_totales,
                jugador_seleccionado.estadisticas.promedio_puntos_por_partido,
                jugador_seleccionado.estadisticas.rebotes_totales,
                jugador_seleccionado.estadisticas.promedio_rebotes_por_partido,
                jugador_seleccionado.estadisticas.asistencias_totales,
                jugador_seleccionado.estadisticas.promedio_asistencias_por_partido,
                jugador_seleccionado.estadisticas.robos_totales,
                jugador_seleccionado.estadisticas.bloqueos_totales,
                jugador_seleccionado.estadisticas.porcentaje_tiros_de_campo,
                jugador_seleccionado.estadisticas.porcentaje_tiros_libres,
                jugador_seleccionado.estadisticas.porcentaje_tiros_triples
            ])

        nombre_archivo = 'stadelman.csv'
        #nombre_jugaor = jugador_seleccionado.nombre   #hay que sumarlo al texto y se va generando un csv por cada jugador con el encabezado
        modo_apertura = 'a' if os.path.exists(nombre_archivo) else 'w'
        try:
            with open(nombre_archivo, mode=modo_apertura, newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if file.tell() == 0:#primera vuelta del encabezado
                    writer.writerow([
                        "Jugador", "Temporadas", "Puntos totales", "Promedios pt por partido",
                        "Rebotes totales", "Promedio rebotes", "Asistencias totales", "Promedio asistencias",
                        "Robos totales", "Bloqueos totales", "Tiros campo pct", "Tiros libres pct", "Tiros triples pct"
                    ])
                for i in range(len(estadisticas)):
                    writer.writerow(estadisticas[i])
                    
            print(Fore.GREEN+"Estadísticas del jugador guardadas en estadisticas_jugador.csv"+Style.RESET_ALL)
        except IOError as e:
            print(Fore.RED+f"Error al guardar las estadísticas, : {e}(reinicio)"+Style.RESET_ALL)
        
        self.guardar_jugadores_json()
        
    

    def guardar_jugadores_json(self):
        nombre_archivo = input("Ingrese un nombre valido par un archivo")
        patron_nombre_archivo = r'^[a-zA-Z0-9_-]'
        if re.match(patron_nombre_archivo, nombre_archivo):
        
            datos_jugadores = []
            for jugador_seleccionado in self.jugadores:
                datos_jugadores.append({
                    "Jugador": jugador_seleccionado.nombre,
                    "Temporadas": jugador_seleccionado.estadisticas.temporadas_jugadas,
                    "Puntos totales": jugador_seleccionado.estadisticas.puntos_totales,
                    "Promedios pt por partido": jugador_seleccionado.estadisticas.promedio_puntos_por_partido,
                    "Rebotes totales": jugador_seleccionado.estadisticas.rebotes_totales,
                    "Promedio rebotes": jugador_seleccionado.estadisticas.promedio_rebotes_por_partido,
                    "Asistencias totales": jugador_seleccionado.estadisticas.asistencias_totales,
                    "Promedio asistencias": jugador_seleccionado.estadisticas.promedio_asistencias_por_partido,
                    "Robos totales": jugador_seleccionado.estadisticas.robos_totales,
                    "Bloqueos totales": jugador_seleccionado.estadisticas.bloqueos_totales,
                    "Tiros campo pct": jugador_seleccionado.estadisticas.porcentaje_tiros_de_campo,
                    "Tiros libres pct": jugador_seleccionado.estadisticas.porcentaje_tiros_libres,
                    "Tiros triples pct": jugador_seleccionado.estadisticas.porcentaje_tiros_triples
                })

            nombre_archivo+=".json"
            try:
                with open(nombre_archivo, 'w') as file:
                    json.dump(datos_jugadores, file, indent=4)
                print(f"Estadísticas de los jugadores guardadas en {nombre_archivo}.json")
            except IOError as e:
                print(f"Error al guardar las estadísticas: {e}")
                
    #9           
    def ordenar_por_suma_robos_y_bloqueos1(self):
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

        for jugador in self.jugadores:
            suma_robos_bloqueos = jugador.estadisticas.robos_totales + jugador.estadisticas.bloqueos_totales
            
            print(f"{jugador.nombre} - Suma de Robos y Bloqueos: {suma_robos_bloqueos}")
        
          
        opcion_b = input("Quiere continuar con la parte B")
        if opcion_b=="s":
            for jugador in self.jugadores:
                suma_robos_bloqueos = jugador.estadisticas.robos_totales + jugador.estadisticas.bloqueos_totales
                porcentaje = (suma_robos_bloqueos / max_suma_robos_bloqueos) * 100
                print(f"{jugador.nombre} - Suma de Robos y Bloqueos: {suma_robos_bloqueos} : {porcentaje:.2f}%")
        cantidad_a_mostrar = input("cuantos jugadores quiere mostrar")
        for idx, jugador in enumerate(self.jugadores):
            if idx < (len(self.jugadores) - cantidad_a_mostrar):
                continue
            
            suma_robos_bloqueos = jugador.estadisticas.robos_totales + jugador.estadisticas.bloqueos_totales
            porcentaje = (suma_robos_bloqueos / max_suma_robos_bloqueos) * 100
            print(f"{idx + 1}. {jugador.nombre} - Suma de Robos y Bloqueos: {suma_robos_bloqueos} - Porcentaje: {porcentaje:.2f}%")
        
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

        cantidad_a_mostrar = int(input("Ingrese la cantidad de jugadores a mostrar: "))  # Convertir a entero

        for idx, jugador in enumerate(self.jugadores):
            if idx < (len(self.jugadores) - cantidad_a_mostrar):
                continue
            
            suma_robos_bloqueos = jugador.estadisticas.robos_totales + jugador.estadisticas.bloqueos_totales
            porcentaje = (suma_robos_bloqueos / max_suma_robos_bloqueos) * 100
            print(f"{idx + 1}. {jugador.nombre} - Suma de Robos y Bloqueos: {suma_robos_bloqueos} - Porcentaje: {porcentaje:.2f}%")
        


     

        
        
        


        
        
        
        
    
        
                    
