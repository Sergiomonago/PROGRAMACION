# Importacion de librerias

from Utiles import leer_int, leer_texto, imprimir_tabla

# Definicion de funciones

def menu_resultados():
    opcion = None
    while opcion != 0:
        print("\n Resultados y Clasificación")
        print("1. Registrar resultado de partido pendiente")
        print("2. Ver la clasificación")
        print("3. Ver estadísticas de un equipo")
        print("4. Volver al menú principal")
        opcion = leer_int("Elige una opción:", minimo=0)

        if opcion == 1:
            registrar_resultado()
        elif opcion == 2:
            ver_clasificacion()
        elif opcion == 3:
            estadisticas_equipo()
        elif opcion == 4:
            print("Volviendo al menú principal")
        else:
            print("Opción no válida. Intenta de nuevo.")

# Definicion de funciones del menu

def elegir_partido_pendiente():
    try:
        from partidos import partidos
        from Equipos import buscar_por_id
    except ImportError:
        print("Partidos necesarios no disponibles.")
        return None

    no_jugados = [p for p in partidos if not p.get("jugado", False)]
    if not no_jugados:
        print("No hay partidos pendientes de jugar.")
        return None

    filas = []
    for p in no_jugados:
        local = buscar_por_id(p["local_id"])
        visit = buscar_por_id(p["visitante_id"])
        filas.append([p["id"], p["jornada"], p["fecha"], p["hora"],
                     p["local_id"], local["nombre"] if local else f"(ID {p['local_id']})",
                     p["visitante_id"], visit["nombre"] if visit else f"(ID {p['visitante_id']})"])
    imprimir_tabla(filas, ["ID","Jornada","Fecha","Hora","Local ID","Local","Visitante ID","Visitante"])

    pid = leer_int("Introduce el ID del partido a registrar (0 para cancelar):", minimo=0)
    if pid == 0:
        return None

    for p in no_jugados:
        if p["id"] == pid:
            return p

    print("ID no válido o no pertenece a partidos pendientes.")
    return None

def registrar_resultado():
    print("\n--- Registrar resultado ---")
    p = elegir_partido_pendiente()
    if not p:
        return

    valid_input = False
    while not valid_input:
        try:
            g_local = int(input("Goles del equipo local: ").strip())
            g_visit = int(input("Goles del equipo visitante: ").strip())
            if g_local < 0 or g_visit < 0:
                print("Los goles deben ser enteros >= 0.")
            else:
                valid_input = True
        except ValueError:
            print("Introduce números enteros válidos para los goles.")

    p["resultado"] = (g_local, g_visit)
    p["jugado"] = True
    print(f"Resultado guardado: {g_local} - {g_visit} (Partido ID {p['id']})")

def calcular_clasificacion():
    try:
        from Equipos import equipos
        from partidos import partidos
    except ImportError:
        print("Módulos necesarios no disponibles.")
        return []

    tabla = {}
    for e in equipos:
        if not e.get("activo", True):
            continue
        tabla[e["id"]] = {
            "id": e["id"],
            "nombre": e["nombre"],
            "PJ": 0,
            "G": 0,
            "E": 0,
            "P": 0,
            "GF": 0,
            "GC": 0,
            "DG": 0,
            "PTS": 0
        }

    # Recorremos partidos jugados y sumamos estadísticas (solo si ambos equipos están en la tabla)
    for p in partidos:
        if not p.get("jugado", False):
            continue
        res = p.get("resultado")
        if not res or not isinstance(res, (list, tuple)) or len(res) != 2:
            # partido marcado como jugado pero sin resultado válido: saltar
            continue
        gl, gv = int(res[0]), int(res[1])
        id_local = p["local_id"]
        id_visit = p["visitante_id"]

        if id_local not in tabla or id_visit not in tabla:
            continue
            # si alguno de los equipos no está activo/registrado en tabla no lo contabilizamos para mantener consistencia.

        # Actualizar PJ, GF, GC 
        tabla[id_local]["PJ"] += 1
        tabla[id_visit]["PJ"] += 1
        tabla[id_local]["GF"] += gl
        tabla[id_local]["GC"] += gv
        tabla[id_visit]["GF"] += gv
        tabla[id_visit]["GC"] += gl

        # Resultados (G/E/P) y PTS
        if gl > gv:
            tabla[id_local]["G"] += 1
            tabla[id_local]["PTS"] += 3
            tabla[id_visit]["P"] += 1
        elif gl < gv:
            tabla[id_visit]["G"] += 1
            tabla[id_visit]["PTS"] += 3
            tabla[id_local]["P"] += 1
        else:
            tabla[id_local]["E"] += 1
            tabla[id_visit]["E"] += 1
            tabla[id_local]["PTS"] += 1
            tabla[id_visit]["PTS"] += 1

    # Calcular DG y preparar lista
    lista = []
    for tid, datos in tabla.items():
        datos["DG"] = datos["GF"] - datos["GC"]
        lista.append(datos)

    # Ordenar por PTS desc, luego DG desc, luego GF desc, luego nombre asc
    lista.sort(key=lambda x: (-x["PTS"], -x["DG"], -x["GF"], x["nombre"]))
    return lista

def ver_clasificacion():
    print("\n Clasificación")
    clasif = calcular_clasificacion()
    if not clasif:
        print("(No hay datos para mostrar la clasificación.)")
        return

    filas = []
    posicion = 1
    for c in clasif:
        filas.append([posicion, c["id"], c["nombre"], c["PJ"], c["G"], c["E"], c["P"], c["GF"], c["GC"], c["DG"], c["PTS"]])
        posicion += 1

    imprimir_tabla(filas, ["Pos", "ID", "Equipo", "PJ", "G", "E", "P", "GF", "GC", "DG", "PTS"])

def estadisticas_equipo():
    try:
        from Equipos import buscar_por_id
    except ImportError:
        print("Módulo equipos no disponible.")
        return

    eid = leer_int("ID del equipo:", minimo=1)
    equipo = buscar_por_id(eid)
    if not equipo or not equipo.get("activo", True):
        print("Equipo no encontrado o inactivo.")
        return

    clasif = calcular_clasificacion()
    datos = next((c for c in clasif if c["id"] == eid), None)

    if not datos:
        print("El equipo no tiene partidos contabilizados aún.")
        return

    filas = [[datos["id"], datos["nombre"], datos["PJ"], datos["GF"], datos["GC"], datos["DG"], datos["PTS"]]]
    imprimir_tabla(filas, ["ID", "Equipo", "PJ", "GF", "GC", "DG", "PTS"])


