# Importacion de Librerias

from Utiles import leer_int
from Equipos import menu_equipos
from Jugadores import menu_jugadores
from partidos import menu_partidos
from resultados import menu_resultados

# Definicion de funciones del Menu principal conectados con el resto de los menus y el resto de los archivos
def main():
    opcion = None
    while opcion != 5:
        print("\n PRIMERA DIVISÓN DE LA LIGA ESPAÑOLA")
        print("\n PATROCINADO POR CAMPUSFP")
        print("1. Gestión de equipos")
        print("2. Gestión de jugadores")
        print("3. Calendario de partidos")
        print("4. Resultados y clasificación")
        print("5. Salir")
        opcion = leer_int("Elige una opción:", minimo=1)

        if opcion == 1:
            menu_equipos()
        elif opcion == 2:
            menu_jugadores()
        elif opcion == 3:
            menu_partidos()
        elif opcion == 4:
            menu_resultados()
        elif opcion == 5:
            print("Vuelva pronto a consultar la mejor liga del mundo")
        else:
            print("Opción incorrecta. Vuelve a intentarlo otra vez por favor.")