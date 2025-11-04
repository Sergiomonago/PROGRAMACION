# Importacion de Librerias

from tabulate import tabulate


# Definiciones de funciones de uso general (para importar)
def leer_int(mensaje, minimo=None):
    while True:
        try:
            valor = int(input(mensaje + " "))
            if minimo is not None and valor < minimo:
                print(f"Introduce un número mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Por favor introduce un número entero.")

def leer_texto(mensaje):
    while True:
        texto = input(mensaje + " ").strip()
        if texto == "":
            print("El campo no se puede quedar vacío. Inténtalo de nuevo.")
        else:
            return texto

def imprimir_tabla(filas, columnas, encabezado=True):
    if not filas:
        print("(Sin registros)")
        return
    print(tabulate(filas, headers=columnas, tablefmt="grid"))

def generar_ID(lista):
    id = 0
    id = len(lista)+1
    return id