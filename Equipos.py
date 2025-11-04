# Importacion de Librerias

from Utiles import leer_texto, leer_int, imprimir_tabla, generar_ID

# Definición de Variables
equipos = []


# Definición de Funcione principal (Menú)

def menu_equipos():
    opcion = None
    while opcion != 7:
        print("\n Gestión de los equipos")
        print("1. Listar los equipos activos")
        print("2. Listar todos (incluye inactivos)")
        print("3. Buscar equipo por ID")
        print("4. Crear equipos")
        print("5. Actualizar un equipo")
        print("6. Eliminar (marcar inactivo)")
        print("7. Volver al menú principal")
        opcion = leer_int("Elige una opción:", minimo=0)

        if opcion == 1:
            listar_equipos(activos_solo=True)
        elif opcion == 2:
            listar_equipos(activos_solo=False)
        elif opcion == 3:
            eid = leer_int("ID a buscar:", minimo=1)
            e = buscar_por_id(eid)
            if e:
                imprimir_tabla([[e["id"], e["nombre"], e["ciudad"], "Sí" if e.get("activo", True) else "No"]],
                               ["ID", "Nombre", "Ciudad", "Activo"])
            else:
                print("Equipo no encontrado.")
        elif opcion == 4:
            crear_equipo()
        elif opcion == 5:
            actualizar_equipo()
        elif opcion == 6:
            eliminar_equipo()
        elif opcion == 7:
            print("Volviendo al menú principal")
        else:
            print("Opción no válida. Intentalo de nuevo.")


# Definición de Funciones

def listar_equipos(activos_solo=True):
    if activos_solo:
        lista = [e for e in equipos if e.get("activo", True)]
    else:
        lista = list(equipos)
    filas = []
    for e in lista:
        filas.append([e["id"], e["nombre"], e["ciudad"], "Sí" if e.get("activo", True) else "No"])
    imprimir_tabla(filas, ["ID", "Nombre", "Ciudad", "Activo"])


def buscar_por_id(equipo_id):
    for e in equipos:
        if e["id"] == equipo_id:
            return e
    return None


def crear_equipo():
    print("Crear equipo")
    nombre = leer_texto("Nombre del equipo:")
    ciudad = leer_texto("Ciudad:")
    nuevo_id = generar_ID(equipos)
    equipo = {"id": nuevo_id, "nombre": nombre, "ciudad": ciudad, "activo": True}
    equipos.append(equipo)
    print(f"Equipo creado con ID {nuevo_id}.")


def actualizar_equipo():
    print("Actualizar un equipo")
    eid = leer_int("ID del equipo a actualizar:", minimo=1)
    e = buscar_por_id(eid)
    if not e:
        print("Equipo no encontrado.")
        return
    print("Ficha actual:")
    imprimir_tabla([[e["id"], e["nombre"], e["ciudad"], "Sí" if e.get("activo", True) else "No"]],
                   ["ID", "Nombre", "Ciudad", "Activo"])
    nuevo_nombre = leer_texto(f"Nuevo nombre (enter para mantener '{e['nombre']}'):")
    nuevo_ciudad = leer_texto(f"Nueva ciudad (enter para mantener '{e['ciudad']}'):")

    if nuevo_nombre:
        e['nombre'] = nuevo_nombre
    if nuevo_ciudad:
        e['ciudad'] = nuevo_ciudad

    print("Equipo actualizado.")


def eliminar_equipo():
    print("\n Eliminar equipo (marcar inactivo) ")
    eid = leer_int("ID del equipo a eliminar:", minimo=1)
    e = buscar_por_id(eid)
    if not e:
        print("Equipo no encontrado.")
        return

    if has_jugadores(eid):
        print("No se puede eliminar el equipo porque tiene jugadores asignados.")
        return

    confirmar = leer_texto(f"¿Confirmas que quieres desactivar el equipo? '{e['nombre']}'? (s/n)").lower()
    if confirmar.startswith('s'):
        e['activo'] = False
        print("Equipo desactivado.")
    else:
        print("Operación cancelada.")


def has_jugadores(equipo_id):
    try:
        from Jugadores import jugadores as lista_jugadores
    except ImportError:
        return False

    return any(j for j in lista_jugadores if j.get("equipo_id") == equipo_id and j.get("activo", True))
    return False