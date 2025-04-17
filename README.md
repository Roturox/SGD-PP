# 🏗️ Sistema de Gestión de Depósito

Este proyecto es un sistema de gestión de inventario desarrollado con **Python, Flask y SQLite** para administrar materiales en un depósito escolar. Permite registrar insumos y herramientas, gestionar préstamos y controlar el stock de forma eficiente.

## 🚀 Tecnologías utilizadas
- **Python** 🐍 → Lenguaje principal del backend.
- **Flask** 🌐 → Framework para crear la aplicación web.
- **SQLite** 🗄️ → Base de datos ligera para almacenar materiales y usuarios.
- **HTML + CSS** 🎨 → Diseño de las páginas web.
- **Bootstrap** 📏 → Estilos y componentes responsivos.

## 📌 Funcionalidades principales
✅ **Login y gestión de usuarios** → Diferenciación entre **Rectora** y **Administradores**, cada uno con permisos específicos.  
✅ **Registro de materiales** → Agregar herramientas e insumos con código de barras y estado actual.  
✅ **Gestión de préstamos** → Control de materiales prestados y fechas de devolución.  
✅ **Stock crítico** → Identificación de materiales con baja disponibilidad.  
✅ **Reportes y estadísticas** → Análisis del uso de los materiales en el depósito.  

2️⃣ Crear un entorno virtual y activarlo
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate  # En Windows


3️⃣ Instalar las dependencias
pip install -r requirements.txt


4️⃣ Ejecutar el archivo de configuración de la base de datos
python setup_db.py


5️⃣ Iniciar la aplicación
python app.py


6️⃣ Acceder a la aplicación desde el navegador
Abre http://127.0.0.1:5000 para comenzar a usar el sistema.
📂 Estructura del proyecto
📂 PP-SGD_byRoturo
 ├── app.py                  # Código principal de la aplicación Flask
 ├── setup_db.py             # Script para configurar la base de datos
 ├── inventario_colegio.db   # Base de datos SQLite
 ├── requirements.txt        # Dependencias del proyecto
 ├── templates               # Archivos HTML
 │    ├── layout.html
 │    ├── login.html
 │    ├── dashboard.html
 │    ├── usuarios.html
 ├── static                  # Archivos CSS y JavaScript
 │    ├── styles.css
 ├── README.md               # Documentación del proyecto


💡 Contribuir al proyecto
Si deseas colaborar:
- Haz un fork del repositorio.
- Crea una nueva rama para tu mejora:git checkout -b mi-mejora

- Haz tus cambios y súbelos:git add .
git commit -m "Mejora en la gestión de usuarios"
git push origin mi-mejora

- Haz un Pull Request para revisión.


📩 Contacto
Si tienes dudas o sugerencias, puedes abrir un Issue en GitHub o contactar a los desarrolladores. ¡Toda ayuda es bienvenida! 😃🎉

---

### **✅ Últimos pasos**
1️⃣ **Copia este contenido y guárdalo en tu archivo `README.md` dentro del repositorio.**  
2️⃣ **Sube los cambios a GitHub:**  
   ```sh
   git add README.md
   git commit -m "Agregado README.md"
   git push origin main
