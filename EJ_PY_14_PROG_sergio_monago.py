# Importacion de librerias

import random
import numpy as np

# Definicion de variables

FICHERO = "partida_comenzada.txt"
TAM = 20
BARCOS = [2, 3, 4]

def crear_tablero_vacio():
    tablero = np.zeros((20, 20), dtype=int)
    print("Tablero vacío creado (20x20):")
    print(tablero)
    return tablero

# Definicion de funciones: Funciones del archivo (Parte que mas ha costado y la investigacion ha sido extensa, ya que me lo queria currar)

# Funciones Dificiles (Investigacion en diferentes fuentes)

def estado_a_texto(estado):
    linea1 = str(estado["tam"])
    partes_barcos = []
    for b in estado["ships"]:
        pares = []
        for p in b:
            pares.append(str(p[0]) + "," + str(p[1]))
        partes_barcos.append(";".join(pares))
    linea2 = "|".join(partes_barcos)
    if estado["shots"]:
        linea3 = ";".join(str(s[0]) + "," + str(s[1]) for s in estado["shots"])
    else:
        linea3 = ""
    return linea1 + "\n" + linea2 + "\n" + linea3

def texto_a_estado(texto):
    texto = texto.strip()
    if texto == "":
        return None
    lineas = texto.splitlines()
    if len(lineas) < 2:
        return None
    try:
        tam = int(lineas[0].strip())
    except Exception:
        return None
    ships = []
    if lineas[1].strip() != "":
        barcos = lineas[1].split("|")
        for b in barcos:
            coords = []
            for par in b.split(";"):
                if par.strip() == "":
                    pass
                else:
                    r_s, c_s = par.split(",")
                    coords.append([int(r_s), int(c_s)])
            if coords:
                ships.append(coords)
    shots = []
    if len(lineas) >= 3 and lineas[2].strip() != "":
        for par in lineas[2].split(";"):
            if par.strip() == "":
                pass
            else:
                r_s, c_s = par.split(",")
                shots.append([int(r_s), int(c_s)])
    return {"tam": tam, "ships": ships, "shots": shots}


# Funciones mas faciles

def guardar(estado):
    texto = estado_a_texto(estado)
    with open(FICHERO, "w", encoding="utf-8") as f:
        f.write(texto)


def cargar_si_hay():
    try:
        with open(FICHERO, "r", encoding="utf-8") as f:
            contenido = f.read()
            if contenido.strip() == "":
                return None
            return texto_a_estado(contenido)
    except FileNotFoundError:
        return None
    except Exception:
        return None

def vaciar_fichero():
    with open(FICHERO, "w", encoding="utf-8") as f:
        f.write("")


# Definicion de funciones: Colocación de los barcos (Hacemos uso de la liberia Random para que todas las partidas no sean iguales)
def colocar_barco(ocupadas, largo, tam):
    intentos = 0
    while intentos < 1000:
        intentos += 1
        orient = random.choice(["H", "V"])
        if orient == "H":
            r = random.randint(0, tam - 1)
            c = random.randint(0, tam - largo)
            coords = [[r, c + i] for i in range(largo)]
        else:
            r = random.randint(0, tam - largo)
            c = random.randint(0, tam - 1)
            coords = [[r + i, c] for i in range(largo)]
        solapa = False
        for p in coords:
            if (p[0], p[1]) in ocupadas:
                solapa = True
        if not solapa:
            for p in coords:
                ocupadas.add((p[0], p[1]))
            return coords
    raise RuntimeError("No se pudo colocar barco")

def nueva_partida():
    ocupadas = set()
    ships = []
    for l in BARCOS:
        ships.append(colocar_barco(ocupadas, l, TAM))
    return {"tam": TAM, "ships": ships, "shots": []}


# Definicion de funciones: Utilidades dentro del juego

def mostrar_tablero(estado, revelar=False):
    tam = estado["tam"]
    mat = np.full((tam, tam), ".", dtype=str)
    for s in estado["shots"]:
        if 0 <= s[0] < tam and 0 <= s[1] < tam:
            mat[s[0], s[1]] = "o"
    for ship in estado["ships"]:
        for p in ship:
            if [p[0], p[1]] in estado["shots"]:
                mat[p[0], p[1]] = "X"
            elif revelar:
                mat[p[0], p[1]] = "B"
    for fila in mat:
        print(" ".join(fila))


def hundido(barco, shots):
    shots_set = {(s[0], s[1]) for s in shots}
    todo = True
    for p in barco:
        if (p[0], p[1]) not in shots_set:
            todo = False
    return todo


def todos_hundidos(estado):
    ok = True
    for b in estado["ships"]:
        if not hundido(b, estado["shots"]):
            ok = False
    return ok


# Definicion de funciones: Función principal con definiciones creadas anteriormente

def main():
    crear_tablero_vacio()
    estado = cargar_si_hay()
    if estado is None:
        estado = nueva_partida()
        print("Nueva partida creada (No se guarda automáticamente)")
    else:
        print("Partida cargada desde el fichero")

    jugando = True
    while jugando:
        print("\nTablero (o = agua, X = tocado). Coordenadas 0..{}".format(TAM - 1))
        mostrar_tablero(estado, revelar=False)
        entrada = input("Introduce 'fila,col' o 111 para menú: ").strip()

        if entrada == "111":
            print("1. Guardar\n 2. Salir sin guardar")
            opcion = input("Elige 1 o 2: ").strip()
            if opcion == "1":
                try:
                    guardar(estado)
                    print("Partida guardada en", FICHERO)
                except Exception:
                    print("Error al guardar la partida")
            else:
                print("Saliendo sin guardar los cambios")
                jugando = False
        else:
            valido = True
            partes = entrada.split(",")
            if len(partes) != 2:
                print("Formato no valido. Debe ser fila,col")
                valido = False
            else:
                try:
                    r = int(partes[0].strip())
                    c = int(partes[1].strip())
                    if not (0 <= r < TAM and 0 <= c < TAM):
                        print("Coordenada fuera del rango.")
                        valido = False
                except Exception:
                    print("Entrada no numérica válida.")
                    valido = False

            if valido:
                repetido = False
                for s in estado["shots"]:
                    if s[0] == r and s[1] == c:
                        repetido = True
                if repetido:
                    print("Ya has disparado en esa coordenada.")
                else:
                    estado["shots"].append([r, c])
                    impacto = False
                    for ship in estado["ships"]:
                        encontrado = False
                        for p in ship:
                            if p[0] == r and p[1] == c:
                                encontrado = True
                        if encontrado:
                            impacto = True
                    if impacto:
                        print("Tocado")
                    else:
                        print("Agua.")

                    for ship in estado["ships"]:
                        if hundido(ship, estado["shots"]):
                            print("Barco hundido de longitud", len(ship))

                    if todos_hundidos(estado):
                        print("Has hundido todos los barcos ¡Felicidades!")
                        try:
                            vaciar_fichero()
                            print("La partida guardada (si existía) ha sido eliminada.")
                        except Exception:
                            print("No se ha podido eliminar la partida guardada.")
                        jugando = False

    print("Fin del juego.")
main()