#Importación de Librerias
from Utiles import leer_int, leer_texto, imprimir_tabla, generar_ID
from datetime import datetime

#Definción de variables

partidos = [
]

# Definicion de funciones solo del (menú)

def menu_partidos():
    opcion = None
    while opcion != 0:
        print("\n Calendario de los partidos")
        print("1. Listar todos los partidos")
        print("2. Listar por jornada")
        print("3. Listar solo los no jugados")
        print("4. Crear un partido")
        print("5. Reprogramar un partido")
        print("6. Eliminar un partido")
        print("7. Volver al menú principal")
        opcion = leer_int("Elige una opción:", minimo=0)

        if opcion == 1:
            listar_partidos()
        elif opcion == 2:
            j = leer_int("Número de jornada:", minimo=1)
            listar_partidos(filtrar_jornada=j)
        elif opcion == 3:
            listar_partidos(solo_no_jugados=True)
        elif opcion == 4:
            crear_partido()
        elif opcion == 5:
            reprogramar_partido()
        elif opcion == 6:
            eliminar_partido()
        elif opcion == 7:
            print("Volviendo al menu principal")
        else:
            print("Opción no válida. Intentalo de nuevo.")


#Definicion de funciones de validaciones diferentes

def validar_equipos_disponibles(local_id, visitante_id):
    if local_id == visitante_id:
        return False, "Un equipo no puede jugar contra sí mismo."
    try:
        from Equipos import buscar_por_id
    except ImportError:
        return False, "Módulo equipos no disponible."

    local = buscar_partido_por_id(local_id)
    visit = buscar_partido_por_id(visitante_id)

    if not local:
        return False, f"Equipo local (ID {local_id}) no encontrado."
    if not visit:
        return False, f"Equipo visitante (ID {visitante_id}) no encontrado."
    if not local.get("activo", True):
        return False, f"Equipo local (ID {local_id}) está inactivo."
    if not visit.get("activo", True):
        return False, f"Equipo visitante (ID {visitante_id}) está inactivo."

    return True, None

def validar_fecha_hora(fecha_str, hora_str):
    try:
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return False, "Formato de fecha inválido. Usa YYYY-MM-DD."
    try:
        hora_obj = datetime.strptime(hora_str, "%H:%M").time()
    except ValueError:
        return False, "Formato de hora inválido. Usa HH:MM en formato 24h."

    return True, (fecha_obj, hora_obj)

def enfrentamiento_duplicado_en_jornada(jornada, local_id, visitante_id):
    for p in partidos:
        if p.get("jornada") == jornada:
            a, b = p.get("local_id"), p.get("visitante_id")
            if (a == local_id and b == visitante_id) or (a == visitante_id and b == local_id): # Comparo sin importar el orden del Local o del Visitante
                return True
    return False

def buscar_partido_por_id(pid):
    for p in partidos:
        if p["id"] == pid:
            return p
    return None

# Definicion de funciones de este menu

# Si "filtrar_jornada" es None muestra todos , si no se filtra.
# Si "solo_no_jugados" es True, muestra solo aquellos con jugado == False.

def listar_partidos(filtrar_jornada=None, solo_no_jugados=False):
    try:
        from Equipos import buscar_por_id
    except ImportError:
        buscar_partido_por_id = lambda x: None

    lista = list(partidos)
    if filtrar_jornada is not None:
        lista = [p for p in lista if p.get("jornada") == filtrar_jornada]
    if solo_no_jugados:
        lista = [p for p in lista if not p.get("jugado", False)]

    filas = []
    for p in lista:
        local = buscar_partido_por_id(p.get("local_id"))
        visit = buscar_partido_por_id(p.get("visitante_id"))
        nombre_local = local["nombre"] if local else f"(ID {p.get('local_id')})"
        nombre_visit = visit["nombre"] if visit else f"(ID {p.get('visitante_id')})"
        resultado = "-"
        if p.get("jugado"):
            res = p.get("resultado")
            if res:
                resultado = f"{res[0]} - {res[1]}"
            else:
                resultado = "JUGADO (sin resultado)"
        filas.append([
            p["id"], p["jornada"], p["fecha"], p["hora"],
            p["local_id"], nombre_local,
            p["visitante_id"], nombre_visit,
            "Sí" if p.get("jugado", False) else "No",
            resultado
        ])

    imprimir_tabla(filas, ["ID", "Jornada", "Fecha", "Hora", "Local ID", "Local", "Visitante ID", "Visitante", "Jugado", "Resultado"])


def crear_partido():
    print("\n--- Crear partido ---")
    jornada = leer_int("Número de jornada (>=1):", minimo=1)
    local_id = leer_int("ID del equipo local:", minimo=1)
    visitante_id = leer_int("ID del equipo visitante:", minimo=1)

    valido, msg = validar_equipos_disponibles(local_id, visitante_id)
    if not valido:
        print("No se puede crear el partido:", msg)
        return

    if enfrentamiento_duplicado_en_jornada(jornada, local_id, visitante_id):
        print("Ya existe ese enfrentamiento en la misma jornada. No se permite duplicar.")
        return

    fecha = leer_texto("Fecha (YYYY-MM-DD):")
    hora = leer_texto("Hora (HH:MM, 24h):")

    valido_dt, info_dt = validar_fecha_hora(fecha, hora)
    if not valido_dt:
        print("Fecha/hora inválida:", info_dt)
        return

    nuevo_id = generar_ID(partidos)
    partido = {
        "id": nuevo_id,
        "jornada": jornada,
        "local_id": local_id,
        "visitante_id": visitante_id,
        "fecha": fecha,
        "hora": hora,
        "jugado": False,
        "resultado": None  #(golesLocal, golesVisitante) cuando se juegue el partido
    }
    partidos.append(partido)
    print(f"Partido creado con ID {nuevo_id}.")


def reprogramar_partido():
    print("\n--- Reprogramar partido ---")
    pid = leer_int("ID del partido a reprogramar:", minimo=1)
    p = buscar_partido_por_id(pid)
    if not p:
        print("Partido no encontrado.")
        return
    if p.get("jugado", False):
        print("No se puede reprogramar: el partido ya ha sido jugado.")
        return
    
    print("Ficha actual:")
    listar_partidos(filtrar_jornada=None)
    fecha = leer_texto("Nueva fecha (YYYY-MM-DD):")
    hora = leer_texto("Nueva hora (HH:MM):")
    valido_dt, info_dt = validar_fecha_hora(fecha, hora)

    if not valido_dt:
        print("Fecha/hora inválida:", info_dt)
        return

    p["fecha"] = fecha
    p["hora"] = hora
    print("Partido reprogramado perfectamente.")


def eliminar_partido():
    print("\n--- Eliminar partido ---")
    pid = leer_int("ID del partido a eliminar:", minimo=1)
    p = buscar_partido_por_id(pid)
    if not p:
        print("Partido no encontrado.")
        return
    if p.get("jugado", False):
        print("No se puede eliminar: el partido ya ha sido jugado.")
        return

    confirmar = leer_texto(f"Confirmar eliminación del partido ID {pid} (S/N):").lower()
    if confirmar.startswith('s'):
        partidos.remove(p)
        print("Partido eliminado.")
    else:
        print("Operación cancelada.")



