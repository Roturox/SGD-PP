import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("inventario_colegio.db")
cursor = conn.cursor()

# Consultar usuarios registrados
cursor.execute("SELECT * FROM Usuarios")
usuarios = cursor.fetchall()

# Mostrar los datos en consola
for usuario in usuarios:
    print(usuario)

conn.close()