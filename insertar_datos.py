import sqlite3

# Conectar a la base de datos
def conectar_bd():
    return sqlite3.connect("inventario_colegio.db")

# Función para insertar un usuario
def agregar_usuario(nombre, apellido, dni, rol):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Usuarios (nombre, apellido, dni, rol) VALUES (?, ?, ?, ?)", 
                       (nombre, apellido, dni, rol))
        conn.commit()
        print("✅ Usuario agregado correctamente.")
    except sqlite3.IntegrityError:
        print("⚠️ Error: DNI duplicado.")
    finally:
        conn.close()

# Función para insertar un producto en el inventario
def agregar_producto(nombre, codigo_barras, cantidad, ubicacion):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Inventario (nombre, codigo_barras, cantidad, ubicacion) VALUES (?, ?, ?, ?)",
                       (nombre, codigo_barras, cantidad, ubicacion))
        conn.commit()
        print("✅ Producto agregado correctamente.")
    except sqlite3.IntegrityError:
        print("⚠️ Error: Código de barras duplicado.")
    finally:
        conn.close()

# Ejecutar funciones de prueba
agregar_usuario("Carlos", "López", "11223344", "administrador")
agregar_producto("Proyector", "987654321", 2, "Sala de Conferencias")
