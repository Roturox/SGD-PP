from flask import Flask, render_template, request, redirect, session
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = "clave-secreta"  # Clave para manejar sesiones

# 🔗 Conexión a la base de datos
def conectar_bd():
    return sqlite3.connect("inventario_colegio.db")

# 💡 Decorador: Verificar inicio de sesión
def requiere_login(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    return decorador

# 💡 Decorador: Verificar roles específicos
def requiere_rol(rol):
    def decorador(func):
        @wraps(func)
        def verificacion(*args, **kwargs):
            if "rol" not in session or session["rol"] != rol:
                return "Acceso denegado", 403
            return func(*args, **kwargs)
        return verificacion
    return decorador

# 🏠 Página inicial: Redirige según la sesión
@app.route('/')
def inicio():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")

# 🔓 Login
@app.route('/login', methods=["GET", "POST"])
def login():
    conn = conectar_bd()
    cursor = conn.cursor()

    if request.method == "POST":
        dni = request.form["dni"]
        contraseña_ingresada = request.form["contraseña"]

        cursor.execute("SELECT id, rol, contraseña FROM Usuarios WHERE dni = ?", (dni,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario[2], contraseña_ingresada):  # 🔒 Comparar contraseña cifrada
            session["user_id"] = usuario[0]
            session["rol"] = usuario[1]
            conn.close()
            return redirect("/dashboard")

        conn.close()
        return "❌ Credenciales incorrectas", 401  # 🔴 Bloquear acceso con datos incorrectos

    return render_template("login.html")
# Fin de Login

@app.route('/resetear_contraseña', methods=["POST"])
@requiere_rol("rectora")  # 🔒 Solo la rectora puede hacerlo
def resetear_contraseña():
    conn = conectar_bd()
    cursor = conn.cursor()

    dni = request.form["dni"]
    nueva_contraseña = generate_password_hash("temporal123")  # 🔐 Nueva contraseña temporal

    cursor.execute("UPDATE Usuarios SET contraseña = ? WHERE dni = ?", (nueva_contraseña, dni))
    conn.commit()
    conn.close()

    return redirect("/usuarios")  # Redirigir de nuevo a la lista de usuarios




# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

# 📊 Dashboard (Protegido)
@app.route('/dashboard')
@requiere_login
def dashboard():
    conn = conectar_bd()
    cursor = conn.cursor()

    # Consultar datos dinámicos (ejemplo)
    cursor.execute("SELECT id, nombre, cantidad FROM Inventario WHERE cantidad < 10")
    stock_critico = cursor.fetchall()

    conn.close()
    return render_template("layout.html", stock_critico=stock_critico)

# 🧑‍🎓 Usuarios (Solo accesible por la rectora)
@app.route('/usuarios')
@requiere_rol("rectora")
def listar_usuarios():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre, apellido, dni, rol FROM Usuarios")
    usuarios = cursor.fetchall()

    conn.close()
    return render_template("usuarios.html", usuarios=usuarios)



#Inicio de Invenario--
@app.route('/inventario')
def mostrar_inventario():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Inventario")
    productos = cursor.fetchall()
    conn.close()
    return render_template("inventario.html", productos=productos)
#Fin de Inventario--


#Inicio de Agregar Usuario--
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/agregar_usuario', methods=["GET", "POST"])
@requiere_rol("rectora")
def agregar_usuario():
    conn = conectar_bd()
    cursor = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        dni = request.form["dni"]
        rol = request.form["rol"]
        contraseña = generate_password_hash(request.form["contraseña"])  # 🔐 Cifrar contraseña

        cursor.execute("INSERT INTO Usuarios (nombre, apellido, dni, rol, contraseña) VALUES (?, ?, ?, ?, ?)",
                       (nombre, apellido, dni, rol, contraseña))
        conn.commit()
        conn.close()

        return redirect("/usuarios")

    return render_template("agregar_usuario.html")

#Fin de Agregar Usuario--


#Inicio de Depositar--
@app.route('/depositar', methods=["GET", "POST"])
def depositar():
    conn = conectar_bd()  # 🛠️ Conectar a la base de datos
    cursor = conn.cursor()  # 🛠️ Definir el cursor para ejecutar SQL

    if request.method == "POST":
        nombre = request.form["nombre"]
        codigo_barras = request.form["codigo_barras"]

        cursor.execute("INSERT INTO Inventario (nombre, codigo_barras, cantidad, ubicacion) VALUES (?, ?, 1, 'Depósito')", (nombre, codigo_barras))
        
        conn.commit()  # 🛠️ Guardar los cambios en la base de datos
        conn.close()  # 🛠️ Cerrar la conexión

        return redirect("/dashboard")  # 🔄 Redirigir después del registro

    return render_template("depositar.html")  # Mostrar el formulario

#Fin de Depositar--


#Inicio de Prestamos--
@app.route('/prestamo', methods=["GET", "POST"])
def prestamos():
    conn = conectar_bd()
    cursor = conn.cursor()

    if request.method == "POST":
        material = request.form["material"]
        responsable = request.form["responsable"]
        fecha_devolucion = request.form["fecha_devolucion"]
        cursor.execute("INSERT INTO Movimientos (usuario, codigo_barras, accion, fecha) VALUES (?, ?, 'retiro', ?)",
                       (responsable, material, fecha_devolucion))
        conn.commit()

    cursor.execute("SELECT * FROM Movimientos WHERE accion='retiro'")
    prestamos = cursor.fetchall()
    conn.close()
    return render_template("prestamos.html", prestamos=prestamos)
#Fin de Prestamos--


#Inicio de Retirar--
@app.route('/retirar', methods=["GET", "POST"])
@requiere_login
def retirar():
    conn = conectar_bd()
    cursor = conn.cursor()

    # 📌 Obtener materiales del inventario
    cursor.execute("SELECT nombre, cantidad FROM Inventario")
    inventario = cursor.fetchall()

    if request.method == "POST":
        material = request.form["material"]
        cantidad = int(request.form["cantidad"])

        # 📌 Verificar si el material tiene stock suficiente
        cursor.execute("SELECT cantidad FROM Inventario WHERE nombre = ?", (material,))
        stock = cursor.fetchone()

        if not stock:
            conn.close()
            return "❌ Error: Material no encontrado en el inventario.", 400

        if stock[0] < cantidad:
            conn.close()
            return "⚠️ Error: No hay suficiente stock disponible.", 400

        # ✅ Actualizar el inventario tras el retiro
        cursor.execute("UPDATE Inventario SET cantidad = cantidad - ? WHERE nombre = ?", (cantidad, material))

        # 📌 Registrar el retiro en la tabla `Movimientos`
        cursor.execute("INSERT INTO Movimientos (usuario, codigo_barras, accion, fecha) VALUES (?, ?, 'retiro', CURRENT_TIMESTAMP)",
                       (session["user_id"], material))

        conn.commit()
        conn.close()
        return redirect("/dashboard")  # 🔄 Redirigir después del retiro

    conn.close()
    return render_template("retirar.html", inventario=inventario)
#Inicio de Retirar--


#Inicio de Pedidos--
@app.route('/pedido', methods=["GET", "POST"])
def pedido():
    return render_template("pedido.html")
#Fin de Pedidos--


#Inicio de Estadisticas--
@app.route('/estadisticas')
def estadisticas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, COUNT(*) FROM Inventario GROUP BY nombre ORDER BY COUNT(*) DESC")
    estadisticas = cursor.fetchall()
    conn.close()
    return render_template("estadisticas.html", estadisticas=estadisticas)
#Fin de Estadisticas--

if __name__ == "__main__":
    app.run(debug=True)
