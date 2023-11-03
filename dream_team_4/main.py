

import os
import re

from colorama import Fore, Style
from equipo import Equipo


def imprimir_menu() -> str:
    menu =\
    """
    Menú de opciones Dream Team:
            1. Mostrar la lista de jugadores del Dream Team.
            2. Mostrar estadísticas de un jugador por índice.
            3. Guardar estadísticas de un jugador en archivo CSV.
            4. Buscar un jugador por nombre y mostrar sus logros.
            5. Calcular y mostrar promedio de puntos por partido 
            de todo el equipo, forma ascendente alfabeticamente.
            6. Comprobar si un jugador es miembro del Salón de la Fama.
            7. Encontrar al jugador con más rebotes totales."
            8. guarda en csv de manera desendente y guarda un json con el nombre elegido por el usuario
            9. ordena la lista de jugadores segun la suma de rebotes y robos
    """
    print(Fore.YELLOW+menu+Style.RESET_ALL)
    # menu = Texttable()
    # texto_menu=\
    #    [ ["Menú"," de opciones Dream Team:"],
    #     ["1.", "Mostrar la lista de jugadores del Dream Team."],
    #     ["2.", "Mostrar estadísticas de un jugador por índice."],
    #     ["3.", "Guardar estadísticas de un jugador en archivo CSV."],
    #     ["4.", "Buscar un jugador por nombre y mostrar sus logros."],
    #     ["5.", "Calcular y mostrar promedio de puntos por partido de todo el equipo, forma ascendente."],
    #     ["6.", "Comprobar si un jugador es miembro del Salón de la Fama."],
    #     ["7.", "Encontrar al jugador con más rebotes totales."],
    #     ["8.", "Salir"]]
    # menu.add_rows(texto_menu)

    # print(menu.draw())
        


def menu_principal() -> str | int:
    imprimir_menu()
    opcion = input('\nSeleccione una opción: ')
    return opcion if re.match('[1-9]$', opcion) else -1

def limpiar_consola() -> None:
        '''
        Imprime un mensaje indicando que limpiará la consola al presionar una tecla.
        Recibe: nada
        Retorna: nada
        '''
        _ = input('\nPresione una tecla para continuar...')
        os.system('cls') if os.name in ['ce', 'nt', 'dos'] else os.system('clear')

if __name__ == "__main__":#tester
   
    equipo = Equipo()
    equipo.cargar_desde_json('dream_team.json')#carga los datos del json
    while True:
        opcion = menu_principal()
        match opcion:
            case "1":
                equipo.mostrar_jugadores(False)
            case "2":
                equipo.mostrar_estadisticas_jugador(False)
            case "3":
                equipo.mostrar_estadisticas_jugador(True)
            case "4":
                equipo.seleccion_jugador()
            case "5":
                equipo.mostrar_promedio_puntos(equipo.jugadores)
            case "6":
                equipo.mostrar_jugadores(True)
                equipo.verificar_salon_fama(equipo.jugadores)
            case "7":
                equipo.calcular_rebotes_totales_mayor(equipo.jugadores)
            case "8":
                equipo.ordernar_listado_robos_totales()
            case "9":
                equipo.ordenar_por_suma_robos_y_bloqueos()
            case _:
                print(Fore.RED+"Opción incorrecta... vuelva a intentarlo"+Style.RESET_ALL)
        limpiar_consola()
    
    