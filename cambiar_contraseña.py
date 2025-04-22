from werkzeug.security import generate_password_hash
import sqlite3

conn = sqlite3.connect("inventario_colegio.db")
cursor = conn.cursor()

nueva_contraseña = generate_password_hash("a")  # 🔐 Cifrar nueva contraseña

cursor.execute("UPDATE Usuarios SET contraseña = ? WHERE dni = '4720375'", (nueva_contraseña,))
conn.commit()
conn.close()

print("✅ Contraseña actualizada correctamente.")