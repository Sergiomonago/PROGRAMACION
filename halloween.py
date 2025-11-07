# Importacion de librerias

import random

# Definicion de variables

monstruos = { 'vampiro': 3, 'momia': 2, 'bruja': 4, 'esqueleto': 1, 'fantasma': 5 } 
objetos = ['estaca', 'poción mágica', 'hechizo']

captura = False
intentos = 3

# Definicion de funciones

def elegir_mounstruo(mounstruos):
    mounstruo = random.choice(list(mounstruos.keys))
    dificultad = mounstruos(mounstruo)
    return mounstruo, dificultad

def intento_captura(dificultad, objeto):
    if objeto == "poción mágica":
        probabilidad_captura = 0.7
    elif objeto == "estaca":
        probabilidad_captura = 0.6
    elif objeto == "hechizo":
        probabilidad_captura = 0.5
    else:
        probabilidad_captura = 0.3

    probabilidad_final = probabilidad_captura - (dificultad * 0.1)
    suerte = random.random()
    return suerte < probabilidad_final

# Logica de programacion

print("¡Bienvenido a la caza de monstruos de Halloween!")
mounstruo, dificultad = elegir_mounstruo(monstruos) 

print("Un {mounstruo} ha aparecido con una dificultad {dificultad}")

while intentos > 0 and not captura:
    print("Tienes {intentos} intentos restantes")
    print("Elige un objeto para intentar capturar al {mounstruo}")

for objetos in objetos:
    print(objetos)
    seleccion = input("escribe el nombre del objeto que quieras")
    capturado = intento_captura(dificultad, seleccion)

    if capturado:
        print("Has capturado al {mounstruo} con un {seleccion}")
    else:
        print("Fallaste al intentar capturar el {mounstruo} con un {objetos}")
        intentos = intentos - 1
    if not captura:
        print("El {mounstruo}, ha escapado.")
        print("fin del Juego")
    