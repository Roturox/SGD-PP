from werkzeug.security import generate_password_hash
import sqlite3

conn = sqlite3.connect("inventario_colegio.db")
cursor = conn.cursor()

nueva_contraseña = generate_password_hash("Fr1j0l3r0.")  # 🔐 Cifrar nueva contraseña

cursor.execute("UPDATE Usuarios SET contraseña = ? WHERE dni = '4720375'", (nueva_contraseña,))
conn.commit()
conn.close()

print("✅ Contraseña actualizada correctamente.")