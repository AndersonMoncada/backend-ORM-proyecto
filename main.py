"""
Punto de entrada del sistema de gestión del Parque de Atracciones.
Maneja login, creación de usuario inicial y menú CRUD completo.
"""

import sys
from datetime import datetime
from typing import Optional
from uuid import UUID

sys.path.insert(0, ".")

"Esto es para la prueba del pull request ya que no me quiere subir a Github"

from src.crud import UsuarioCrud as crud_usuario
from src.crud import TitularCrud as crud_titular
from src.crud import VisitanteCrud as crud_visitante
from src.crud import EntradaCrud as crud_entrada
from src.crud import SedeCrud as crud_sede
from src.crud import AtraccionesCrud as crud_atraccion
from src.crud.MicroEntidadesCrud import (
    crear_acuatica,
    obtener_todas_acuaticas,
    obtener_acuatica_por_id,
    actualizar_acuatica,
    eliminar_acuatica,
    crear_electronica,
    obtener_todas_electronicas,
    obtener_electronica_por_id,
    actualizar_electronica,
    eliminar_electronica,
    crear_mecanica,
    obtener_todas_mecanicas,
    obtener_mecanica_por_id,
    eliminar_mecanica,
    crear_fisica,
    obtener_todas_fisicas,
    obtener_fisica_por_id,
    eliminar_fisica,
)
from src.database.config import crear_tablas
from src.Entities.Usuario import Usuario


def leer_texto(mensaje: str) -> str:
    return input(mensaje).strip()


def leer_float(mensaje: str, default: float = 0.0) -> float:
    try:
        return float(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_int(mensaje: str, default: int = 0) -> int:
    try:
        return int(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_uuid(mensaje: str) -> Optional[UUID]:
    s = input(mensaje).strip()
    if not s:
        return None
    try:
        return UUID(s)
    except ValueError:
        return None


def ingresar_o_crear_usuario() -> Optional[Usuario]:
    if not crud_usuario.hay_usuarios():
        print("\nNo hay usuarios en el sistema. Crea el primero :).")
        nombre = leer_texto("Nombre de usuario: ")
        contra = leer_texto("Contraseña: ")
        rol = leer_texto("Rol (admin/usuario): ") or "admin"
        if not nombre or not contra:
            print("Nombre y contraseña son obligatorios.")
            return None
        try:
            crud_usuario.crear(nombre, contra, rol)
            print(f"Usuario '{nombre}' creado. Inicia sesión.\n")
        except Exception as e:
            print("Error al crear usuario:", e)
            return None

    while True:
        print("Inicio de sesión ✨✨")
        nombre = leer_texto("Usuario: ")
        contra = leer_texto("Contraseña: ")
        if not nombre or not contra:
            print("Usuario y contraseña obligatorios.\n")
            continue
        usuario = crud_usuario.login(nombre, contra)
        if usuario:
            print(f"\nBienvenido, {usuario.nombre_usuario} ({usuario.rol}).\n")
            return usuario
        print("Usuario o contraseña incorrectos.\n")


def menu_usuarios(usuario_id: UUID) -> None:
    while True:
        print("\n- Usuarios -")
        print("1. Lista  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for u in crud_usuario.obtener_todos():
                print(
                    f"  {u.id_usuario} | {u.nombre_usuario} | {u.rol} | activo={u.activo}"
                )
        elif op == "2":
            nombre = leer_texto("Nombre de usuario: ")
            contra = leer_texto("Contraseña: ")
            rol = leer_texto("Rol (admin/usuario): ") or "usuario"
            if nombre and contra:
                try:
                    crud_usuario.crear(nombre, contra, rol)
                    print("Usuario creado.")
                except Exception as e:
                    print("Error:", e)
        elif op == "3":
            id_u = leer_uuid("ID usuario a actualizar: ")
            if not id_u:
                print("ID inválido.")
                continue
            u = crud_usuario.obtener_por_id(id_u)
            if not u:
                print("No existe ese usuario.")
                continue
            nombre = (
                leer_texto(f"Nuevo nombre (actual: {u.nombre_usuario}): ")
                or u.nombre_usuario
            )
            rol = leer_texto(f"Nuevo rol (actual: {u.rol}): ") or u.rol
            crud_usuario.actualizar(id_u, usuario_id, nombre_usuario=nombre, rol=rol)
            print("Actualizado.")
        elif op == "4":
            id_u = leer_uuid("ID usuario a eliminar: ")
            if id_u and crud_usuario.eliminar(id_u):
                print("Eliminado correctamente 🥳🥳.")
            else:
                print("No se pudo eliminar ✖️.")


def menu_titulares(usuario_id: UUID) -> None:
    while True:
        print("\n- Titulares -")
        print("1. Lista  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for t in crud_titular.obtener_todos():
                print(
                    f"  {t.id_titular} | {t.nombre} | {t.cedula} | {t.telefono or '-'}"
                )
        elif op == "2":
            nombre = leer_texto("Nombre: ")
            cedula = leer_texto("Cédula: ")
            telefono = leer_texto("Teléfono (opcional): ")
            if nombre and cedula:
                try:
                    crud_titular.crear(nombre, cedula, usuario_id, telefono or None)
                    print("Titular creado.")
                except Exception as e:
                    print("Error:", e)
        elif op == "3":
            id_t = leer_uuid("ID titular a actualizar: ")
            if not id_t:
                print("ID inválido X.")
                continue
            t = crud_titular.obtener_por_id(id_t)
            if not t:
                print("No existe ese titular.")
                continue
            nombre = leer_texto(f"Nuevo nombre (actual: {t.nombre}): ") or t.nombre
            telefono = (
                leer_texto(f"Nuevo teléfono (actual: {t.telefono or '-'}): ")
                or t.telefono
            )
            crud_titular.actualizar(id_t, usuario_id, nombre=nombre, telefono=telefono)
            print("Actualizado.")
        elif op == "4":
            id_t = leer_uuid("ID titular a eliminar: ")
            if id_t and crud_titular.eliminar(id_t):
                print("Eliminado. 🥳🥳")
            else:
                print("No se pudo eliminar. ✖️")


def menu_visitantes(usuario_id: UUID) -> None:
    while True:
        print("\n- Visitantes -")
        print(
            "1. Listar todos  2. Listar por titular  3. Crear  4. Actualizar  5. Eliminar  0. Volver"
        )
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for v in crud_visitante.obtener_todos():
                print(
                    f"  {v.id_visitante} | {v.nombre_visitante} | edad={v.edad} | estatura={v.estatura}"
                )
        elif op == "2":
            id_t = leer_uuid("ID titular: ")
            if id_t:
                for v in crud_visitante.obtener_por_titular(id_t):
                    print(
                        f"  {v.id_visitante} | {v.nombre_visitante} | edad={v.edad} | estatura={v.estatura}"
                    )
        elif op == "3":
            nombre = leer_texto("Nombre visitante: ")
            edad = leer_int("Edad: ")
            estatura = leer_float("Estatura (metros): ")
            id_t = leer_uuid("ID titular: ")
            if nombre and id_t:
                try:
                    crud_visitante.crear(nombre, edad, estatura, id_t, usuario_id)
                    print("Visitante creado.")
                except Exception as e:
                    print("Error:", e)
        elif op == "4":
            id_v = leer_uuid("ID visitante a actualizar: ")
            if not id_v:
                print("ID inválido.")
                continue
            v = crud_visitante.obtener_por_id(id_v)
            if not v:
                print("No existe ese visitante.")
                continue
            nombre = (
                leer_texto(f"Nuevo nombre (actual: {v.nombre_visitante}): ")
                or v.nombre_visitante
            )
            edad = leer_int(f"Nueva edad (actual: {v.edad}): ") or v.edad
            estatura = (
                leer_float(f"Nueva estatura (actual: {v.estatura}): ") or v.estatura
            )
            crud_visitante.actualizar(
                id_v, usuario_id, nombre_visitante=nombre, edad=edad, estatura=estatura
            )
            print("Actualizado.")
        elif op == "5":
            id_v = leer_uuid("ID visitante a eliminar: ")
            if id_v and crud_visitante.eliminar(id_v):
                print("Eliminado. 🥳🥳")
            else:
                print("No se pudo eliminar. ✖️")


def menu_entradas(usuario_id: UUID) -> None:
    while True:
        print("\n- Entradas -")
        print(
            "1. Listar todas  2. Listar por titular  3. Crear  4. Actualizar  5. Eliminar  0. Volver"
        )
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for e in crud_entrada.obtener_todos():
                print(
                    f"  {e.id_entrada} | {e.codigo} | precio={e.precio} | fecha={e.fecha}"
                )
        elif op == "2":
            id_t = leer_uuid("ID titular: ")
            if id_t:
                for e in crud_entrada.obtener_por_titular(id_t):
                    print(f"  {e.id_entrada} | {e.codigo} | precio={e.precio}")
        elif op == "3":
            codigo = leer_texto("Código de entrada: ")
            precio = leer_float("Precio: ")
            fecha_str = leer_texto("Fecha (YYYY-MM-DD): ")
            reingreso = leer_texto("Reingreso (si/no, opcional): ")
            id_t = leer_uuid("ID titular: ")
            if codigo and id_t:
                try:
                    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                    crud_entrada.crear(
                        codigo, precio, fecha, id_t, usuario_id, reingreso or None
                    )
                    print("Entrada creada.")
                except Exception as e:
                    print("Error:", e)
        elif op == "4":
            id_e = leer_uuid("ID entrada a actualizar: ")
            if not id_e:
                print("ID inválido.")
                continue
            e = crud_entrada.obtener_por_id(id_e)
            if not e:
                print("No existe esa entrada.")
                continue
            precio = leer_float(f"Nuevo precio (actual: {e.precio}): ") or e.precio
            reingreso = (
                leer_texto(f"Nuevo reingreso (actual: {e.reingreso or '-'}): ")
                or e.reingreso
            )
            crud_entrada.actualizar(
                id_e, usuario_id, precio=precio, reingreso=reingreso
            )
            print("Actualizado.")
        elif op == "5":
            id_e = leer_uuid("ID entrada a eliminar: ")
            if id_e and crud_entrada.eliminar(id_e):
                print("Eliminado. 🥳🥳")
            else:
                print("No se pudo eliminar. ✖️")


def menu_sedes(usuario_id: UUID) -> None:
    while True:
        print("\n- Sedes -")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for s in crud_sede.obtener_todos():
                print(f"  {s.id_sede} | {s.nombre} | {s.ubicacion}")
        elif op == "2":
            nombre = leer_texto("Nombre sede: ")
            ubicacion = leer_texto("Ubicación: ")
            if nombre and ubicacion:
                crud_sede.crear(nombre, ubicacion)
                print("Sede creada.")
        elif op == "3":
            id_s = leer_uuid("ID sede a actualizar: ")
            if not id_s:
                print("ID inválido.")
                continue
            s = crud_sede.obtener_por_id(id_s)
            if not s:
                print("No existe esa sede.")
                continue
            nombre = leer_texto(f"Nuevo nombre (actual: {s.nombre}): ") or s.nombre
            ubicacion = (
                leer_texto(f"Nueva ubicación (actual: {s.ubicacion}): ") or s.ubicacion
            )
            crud_sede.actualizar(id_s, nombre=nombre, ubicacion=ubicacion)
            print("Actualizado.")
        elif op == "4":
            id_s = leer_uuid("ID sede a eliminar: ")
            if id_s and crud_sede.eliminar(id_s):
                print("Eliminado. 🥳🥳")
            else:
                print("No se pudo eliminar. ✖️")


def menu_atracciones(usuario_id: UUID) -> None:
    while True:
        print("\n- Atracciones -")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for a in crud_atraccion.obtener_todos():
                print(
                    f"  {a.id_atraccion} | {a.nombre} | edad_min={a.edad_minima} | estatura_min={a.estatura_minima} | sede={a.id_sede}"
                )
        elif op == "2":
            nombre = leer_texto("Nombre atracción: ")
            edad_minima = leer_int("Edad mínima: ")
            estatura_minima = leer_float("Estatura mínima (metros): ")
            id_s = leer_uuid("ID sede: ")
            if nombre and id_s:
                crud_atraccion.crear(nombre, edad_minima, estatura_minima, id_s)
                print("Atracción creada.")
        elif op == "3":
            id_a = leer_uuid("ID atracción a actualizar: ")
            if not id_a:
                print("ID inválido.")
                continue
            a = crud_atraccion.obtener_por_id(id_a)
            if not a:
                print("No existe esa atracción.")
                continue
            nombre = leer_texto(f"Nuevo nombre (actual: {a.nombre}): ") or a.nombre
            edad_minima = (
                leer_int(f"Nueva edad mínima (actual: {a.edad_minima}): ")
                or a.edad_minima
            )
            estatura_minima = (
                leer_float(f"Nueva estatura mínima (actual: {a.estatura_minima}): ")
                or a.estatura_minima
            )
            crud_atraccion.actualizar(
                id_a,
                nombre=nombre,
                edad_minima=edad_minima,
                estatura_minima=estatura_minima,
            )
            print("Actualizado.")
        elif op == "4":
            id_a = leer_uuid("ID atracción a eliminar: ")
            if id_a and crud_atraccion.eliminar(id_a):
                print("Eliminado. 🥳🥳")
            else:
                print("No se pudo eliminar. ✖️")


def menu_microentidades(usuario_id: UUID) -> None:
    while True:
        print("\n--- Subentidades ---")
        print("1. Acuáticas  2. Electrónicas  3. Mecánicas  4. Físicas  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        elif op == "1":
            menu_acuaticas()
        elif op == "2":
            menu_electronicas()
        elif op == "3":
            menu_mecanicas()
        elif op == "4":
            menu_fisicas()


def menu_acuaticas() -> None:
    while True:
        print("\n- Acuáticas -")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for a in obtener_todas_acuaticas():
                print(
                    f"  {a.id_acuatica} | profundidad={a.profundidad} | capacidad={a.capacidad} | propulsion={a.propulsion}"
                )
        elif op == "2":
            id_a = leer_uuid("ID atracción base: ")
            profundidad = leer_float("Profundidad (metros): ")
            capacidad = leer_int("Capacidad: ")
            propulsion = leer_texto("Propulsión: ")
            if id_a and propulsion:
                crear_acuatica(id_a, profundidad, capacidad, propulsion)
                print("Acuática creada.")
        elif op == "3":
            id_a = leer_uuid("ID acuática a actualizar: ")
            if not id_a:
                print("ID inválido.")
                continue
            a = obtener_acuatica_por_id(id_a)
            if not a:
                print("No existe.")
                continue
            profundidad = (
                leer_float(f"Nueva profundidad (actual: {a.profundidad}): ")
                or a.profundidad
            )
            capacidad = (
                leer_int(f"Nueva capacidad (actual: {a.capacidad}): ") or a.capacidad
            )
            actualizar_acuatica(id_a, profundidad=profundidad, capacidad=capacidad)
            print("Actualizado.")
        elif op == "4":
            id_a = leer_uuid("ID acuática a eliminar: ")
            if id_a and eliminar_acuatica(id_a):
                print("Eliminado. 😁")
            else:
                print("No se pudo eliminar. 🚫")


def menu_electronicas() -> None:
    while True:
        print("\n--- Electrónicas ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for e in obtener_todas_electronicas():
                print(
                    f"  {e.id_electronica} | experiencia={e.experiencia} | equipamiento={e.equipamiento or '-'}"
                )
        elif op == "2":
            id_a = leer_uuid("ID atracción base: ")
            experiencia = leer_texto("Experiencia: ")
            equipamiento = leer_texto("Equipamiento (opcional): ")
            if id_a and experiencia:
                crear_electronica(id_a, experiencia, equipamiento or None)
                print("Electrónica creada.")
        elif op == "3":
            id_e = leer_uuid("ID electrónica a actualizar: ")
            if not id_e:
                print("ID inválido.")
                continue
            e = obtener_electronica_por_id(id_e)
            if not e:
                print("No existe.")
                continue
            experiencia = (
                leer_texto(f"Nueva experiencia (actual: {e.experiencia}): ")
                or e.experiencia
            )
            equipamiento = (
                leer_texto(f"Nuevo equipamiento (actual: {e.equipamiento or '-'}): ")
                or e.equipamiento
            )
            actualizar_electronica(
                id_e, experiencia=experiencia, equipamiento=equipamiento
            )
            print("Actualizado.")
        elif op == "4":
            id_e = leer_uuid("ID electrónica a eliminar: ")
            if id_e and eliminar_electronica(id_e):
                print("Eliminado. 😁")
            else:
                print("No se pudo eliminar. 🚫")


def menu_mecanicas() -> None:
    while True:
        print("\n- Mecánicas -")
        print("1. Listar  2. Crear  3. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for m in obtener_todas_mecanicas():
                print(f"  {m.id_mecanica} | atraccion={m.id_atraccion}")
        elif op == "2":
            id_a = leer_uuid("ID atracción base: ")
            if id_a:
                crear_mecanica(id_a)
                print("Mecánica creada.")
        elif op == "3":
            id_m = leer_uuid("ID mecánica a eliminar: ")
            if id_m and eliminar_mecanica(id_m):
                print("Eliminado. 🥳🥳")
            else:
                print("No se pudo eliminar. X")


def menu_fisicas() -> None:
    while True:
        print("\n- Físicas -")
        print("1. Listar  2. Crear  3. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for f in obtener_todas_fisicas():
                print(f"  {f.id_fisica} | atraccion={f.id_atraccion}")
        elif op == "2":
            id_a = leer_uuid("ID atracción base: ")
            if id_a:
                crear_fisica(id_a)
                print("Física creada.")
        elif op == "3":
            id_f = leer_uuid("ID física a eliminar: ")
            if id_f and eliminar_fisica(id_f):
                print("Eliminado. 😁")
            else:
                print("No se pudo eliminar. 🚫")


def menu_principal(usuario: Usuario) -> None:
    while True:
        print("\n====== Menú principal ======")
        print("1. Usuarios")
        print("2. Titulares")
        print("3. Visitantes")
        print("4. Entradas")
        print("5. Sedes")
        print("6. Atracciones")
        print("7. Subentidades (Acuática, Electrónica, Mecánica, Física)")
        print("0. Salir")

        op = leer_texto("Opción: ")

        if op == "0":
            print(f"Hasta luego, {usuario.nombre_usuario}!")
            break
        elif op == "1":
            menu_usuarios(usuario.id_usuario)
        elif op == "2":
            menu_titulares(usuario.id_usuario)
        elif op == "3":
            menu_visitantes(usuario.id_usuario)
        elif op == "4":
            menu_entradas(usuario.id_usuario)
        elif op == "5":
            menu_sedes(usuario.id_usuario)
        elif op == "6":
            menu_atracciones(usuario.id_usuario)
        elif op == "7":
            menu_microentidades(usuario.id_usuario)
        else:
            print("Opción no válida.")


def main() -> None:
    crear_tablas()
    usuario = ingresar_o_crear_usuario()
    if not usuario:
        print("No se pudo iniciar sesión. Saliendo.")
        return
    menu_principal(usuario)


if __name__ == "__main__":
    main()
