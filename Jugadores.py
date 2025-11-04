#Importacion de Librerias
from Utiles import leer_texto, leer_int, imprimir_tabla, generar_ID

#Definicion de variables
jugadores = []

# Definicion de funciones del menu de jugadores 
def menu_jugadores():
    opcion = None
    while opcion != 0:
        print("\n Gestión de jugadores")
        print("1. Listar todos los jugadores activos")
        print("2. Listar todos (incluye inactivos)")
        print("3. Listar jugadores por equipo")
        print("4. Buscar jugador por ID")
        print("5. Alta de jugador")
        print("6. Actualizar jugador")
        print("7. Eliminar (marcar inactivo)")
        print("0. Volver al menú principal")
        opcion = leer_int("Elige una opción:", minimo=0)

        if opcion == 1:
            listar_jugadores(solo_activos=True)
        elif opcion == 2:
            listar_jugadores(solo_activos=False)
        elif opcion == 3:
            eid = leer_int("ID del equipo:", minimo=1)
            listar_jugadores(filtrar_por_equipo_id=eid, solo_activos=True)
        elif opcion == 4:
            jid = leer_int("ID del jugador a buscar:", minimo=1)
            j = buscar_jugador_por_id(jid)
            if j:
                try:
                    from Equipos import buscar_por_id
                    equipo = buscar_por_id(j.get("equipo_id"))
                    nombre_equipo = equipo["nombre"] if equipo else "(Sin equipo)"
                except ImportError:
                    nombre_equipo = "(Equipo no disponible)"
                imprimir_tabla([[j["id"], j["nombre"], j["posicion"], j["equipo_id"], nombre_equipo, "Sí" if j.get("activo", True) else "No"]],
                               ["ID", "Nombre", "Posición", "Equipo ID", "Equipo", "Activo"])
            else:
                print("Jugador no encontrado.")
        elif opcion == 5:
            alta_jugador()
        elif opcion == 6:
            actualizar_jugador()
        elif opcion == 7:
            eliminar_jugador()
        elif opcion == 0:
            print("Saliendo del menú de jugadores...")
        else:
            print("Opción no válida. Intentalo de nuevo.")



def listar_jugadores(filtrar_por_equipo_id=None, solo_activos=True):
    try:
        from Equipos import buscar_por_id
    except ImportError:
        buscar_por_id = lambda x: None

    lista = list(jugadores)
    if solo_activos:
        lista = [j for j in lista if j.get("activo", True)]
    if filtrar_por_equipo_id is not None:
        lista = [j for j in lista if j.get("equipo_id") == filtrar_por_equipo_id]

    filas = []
    for j in lista:
        equipo = buscar_por_id(j.get("equipo_id"))
        nombre_equipo = equipo["nombre"] if equipo else "(Sin equipo)"
        filas.append([j["id"], j["nombre"], j["posicion"], j["equipo_id"], nombre_equipo, "Sí" if j.get("activo", True) else "No"])

    imprimir_tabla(filas, ["ID", "Nombre", "Posición", "Equipo ID", "Equipo", "Activo"])


def validar_equipo(equipo_id):
    try:
        from Equipos import buscar_por_id
    except ImportError:
        return False, "Módulo equipos no disponible."

    equipo = buscar_por_id(equipo_id)
    if not equipo:
        return False, "Equipo no encontrado."
    if not equipo.get("activo", True):
        return False, "El equipo está inactivo."
    return True, equipo


def buscar_jugador_por_id(jugador_id):
    for j in jugadores:
        if j["id"] == jugador_id:
            return j
        return None


def alta_jugador():
    print("\n--- Alta de jugador ---")
    nombre = leer_texto("Nombre del jugador:")
    posicion = leer_texto("Posición (Portero, Defensa, Centrocampista, Delantero):")
    equipo_id = leer_int("ID del equipo al que pertenece:", minimo=1)

    valido, info = validar_equipo(equipo_id)
    if not valido:
        print("No se puede crear el jugador:", info)
        return

    nuevo_id = generar_ID(jugadores)
    jugador = {
        "id": nuevo_id,
        "nombre": nombre,
        "posicion": posicion,
        "equipo_id": equipo_id,
        "activo": True
    }
    jugadores.append(jugador)
    print(f"Jugador creado con ID {nuevo_id}.")


def actualizar_jugador():
    print("\n--- Actualizar jugador ---")
    jid = leer_int("ID del jugador a actualizar:", minimo=1)
    j = buscar_jugador_por_id(jid)
    if not j:
        print("Jugador no encontrado.")
        return

    print("Ficha actual:")
    listar = [[j["id"], j["nombre"], j["posicion"], j["equipo_id"], "Sí" if j.get("activo", True) else "No"]]
    imprimir_tabla(listar, ["ID", "Nombre", "Posición", "Equipo ID", "Activo"])

    nuevo_nombre = input(f"Nuevo nombre (ENTER para mantener '{j['nombre']}'): ").strip()
    nueva_posicion = input(f"Nueva posición (ENTER para mantener '{j['posicion']}'): ").strip()
    cambio_equipo = input("¿Cambiar equipo? (s/n): ").strip().lower()

    if nuevo_nombre:
        j["nombre"] = nuevo_nombre
    if nueva_posicion:
        j["posicion"] = nueva_posicion
    if cambio_equipo.startswith('s'):
        nuevo_eid = leer_int("Nuevo ID de equipo:", minimo=1)
        valido, info = validar_equipo(nuevo_eid)
        if not valido:
            print("No se puede cambiar el equipo:", info)
        else:
            j["equipo_id"] = nuevo_eid

    print("Jugador actualizado.")


def eliminar_jugador():
    print("\n Eliminar jugador (marcar inactivo) ")
    jid = leer_int("ID del jugador a eliminar:", minimo=1)
    j = buscar_jugador_por_id(jid)
    if not j:
        print("Jugador no encontrado.")
        return

    confirmar = input(f"¿Confirmas desactivar al jugador '{j['nombre']}'? (s/n): ").strip().lower()
    if confirmar.startswith('s'):
        j["activo"] = False
        print("Jugador desactivado.")
    else:
        print("Operación cancelada.")