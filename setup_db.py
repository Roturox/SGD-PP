import sqlite3

# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect("inventario_colegio.db")
cursor = conn.cursor()

# Crear la tabla de Usuarios primero
cursor.execute("""
CREATE TABLE IF NOT EXISTS Usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni TEXT UNIQUE NOT NULL,
    rol TEXT NOT NULL CHECK(rol IN ('rectora', 'administrador')),
    contraseña TEXT NOT NULL
)
""")

# Crear la tabla de Inventario
cursor.execute("""
CREATE TABLE IF NOT EXISTS Inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    codigo_barras TEXT UNIQUE NOT NULL,
    cantidad INTEGER NOT NULL,
    ubicacion TEXT NOT NULL
)
""")

# Crear la tabla de Movimientos
cursor.execute("""
CREATE TABLE IF NOT EXISTS Movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    codigo_barras TEXT NOT NULL,
    accion TEXT NOT NULL CHECK(accion IN ('ingreso', 'retiro')),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(codigo_barras) REFERENCES Inventario(codigo_barras)
)
""")

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("✅ Base de datos creada exitosamente.")
