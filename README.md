# 🎡 Parque de Atracciones — ORM con Trazabilidad

Sistema de gestión para un parque de atracciones desarrollado en Python con SQLAlchemy y PostgreSQL (Neon). Permite administrar visitantes, titulares, entradas, atracciones y sedes mediante operaciones CRUD completas con trazabilidad de usuarios.

---

## Estructura del proyecto

```
Parque-de-Atracciones-ORM/
├── .env.example          # Plantilla de variables de entorno
├── .gitignore
├── README.md
├── main.py               # Punto de entrada del programa
├── requirements.txt
└── src/
    ├── database/
    │   ├── __init__.py
    │   └── config.py     # Conexión a Neon (PostgreSQL)
    ├── entities/         # Modelos ORM con SQLAlchemy
    │   ├── __init__.py
    │   ├── usuario.py
    │   ├── titular.py
    │   ├── visitante.py
    │   ├── entrada.py
    │   ├── atraccion.py
    │   └── sede.py
    └── crud/             # Operaciones CRUD por entidad
        ├── __init__.py
        ├── usuario.py
        ├── titular.py
        ├── visitante.py
        ├── entrada.py
        ├── atraccion.py
        └── sede.py
```

---

## Entidades

| Entidad | Descripción | Trazabilidad |
|---------|-------------|--------------|
| `Usuario` | Gestiona el acceso al sistema. Base de trazabilidad para las demás entidades. | No aplica |
| `Titular` | Persona responsable del grupo de visitantes. Referencia a Usuario para auditoría. | ✅ |
| `Visitante` | Integrantes del grupo registrado por el titular. | ✅ |
| `Entrada` | Registro de compra de entrada con precio, fecha y código. | ✅ |
| `Atraccion` | Atracciones del parque con restricciones de edad y estatura. | No aplica |
| `Sede` | Sedes del parque con su ubicación. | No aplica |

Las entidades `Titular`, `Visitante` y `Entrada` incluyen las 4 columnas de auditoría:
- `fecha_creacion` — se registra automáticamente al crear.
- `fecha_edicion` — se actualiza automáticamente al modificar.
- `id_usuario_creacion` — referencia al usuario que creó el registro.
- `id_usuario_edita` — referencia al usuario que realizó la última edición.

---

## Requisitos

- Python 3.10 o superior
- Cuenta en [Neon](https://neon.tech) o cualquier instancia PostgreSQL

---

## Instalación

1. Clona el repositorio y crea un entorno virtual:

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
   - Copia `.env.example` y renómbralo a `.env`
   - Define tu cadena de conexión:

```
DATABASE_URL=postgresql://usuario:password@host:5432/nombre_bd
```

4. Ejecuta el programa:

```bash
python main.py
```

---

## Funcionalidades CRUD

El sistema permite realizar las siguientes operaciones desde el menú principal:

- **Usuarios** — Registro, login con contraseña hasheada, actualización y eliminación.
- **Titulares** — Crear titular del grupo, consultar, actualizar y eliminar.
- **Visitantes** — Registrar integrantes del grupo asociados a un titular.
- **Entradas** — Compra, consulta de vigencia, historial y eliminación.
- **Atracciones** — Gestión de atracciones con validación de restricciones.
- **Sedes** — Administración de sedes y su ubicación.

---

## Flujo de trabajo Git

```
feat/nombre-rama → dev → qa → prod
```

Cada funcionalidad se desarrolla en una rama `feat`, se integra a `dev` mediante Pull Request, pasa por revisión en `qa` y finalmente llega a `prod` cuando está estable.

---

## Video demostrativo

[🎥 URL del video]([https://drive.google.com/file/d/1PtMPPrprwsYymXXANvvDEfEM6OVbRduf/view?usp=sharing](https://drive.google.com/file/d/1isdCwVwVNezH1xewpH5JUO_7Z0-OyOD6/view?usp=sharing))

---

## Notas

- El archivo `.env` **no debe subirse** al repositorio (está en `.gitignore`).
- Las tablas se crean automáticamente al ejecutar `main.py` si no existen en Neon.
- Las contraseñas se almacenan con hash SHA-256, nunca en texto plano.
