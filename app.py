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
        contraseña = request.form["contraseña"]

        cursor.execute("SELECT id, rol, contraseña FROM Usuarios WHERE dni = ?", (dni,))
        usuario = cursor.fetchone()

        if usuario and contraseña == usuario[2]:  # ⚠️ Sustituir por hashed passwords
            session["user_id"] = usuario[0]
            session["rol"] = usuario[1]
            return redirect("/dashboard")
        return "Credenciales incorrectas", 401

    conn.close()
    return render_template("login.html")

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
        contraseña = generate_password_hash(request.form["contraseña"])

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

    if request.method == "POST":
        nombre = request.form["nombre"]
        codigo_barras = request.form["codigo_barras"]
        tipo = request.form["tipo"]
        estado = request.form["estado"]
        contacto = request.form["contacto"]
        fecha_hora = request.form["fecha_hora"]

        cursor.execute("INSERT INTO Inventario (nombre, codigo_barras, cantidad, ubicacion) VALUES (?, ?, 1, 'Depósito')")
        cursor.execute("INSERT INTO Movimientos (usuario, codigo_barras, accion, fecha) VALUES (?, ?, 'ingreso', ?)",
                       (contacto, codigo_barras, fecha_hora))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("depositar.html")
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
def retirar():
    return render_template("retirar.html")
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
