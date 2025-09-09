# Clonar el repositorio

```bash
git clone https://github.com/JuanDavidZabalaTapiero/examen-prix.git
```

# Crear entorno virtual

```bash
python -m venv .venv

# Activación (Windows)
.venv\Scripts\activate

# Activación (Linux/Mac)
source .venv/bin/activate
```

# Instalar dependencias

```bash
pip install -r requirements.txt # producción
pip install -r requirements-dev.txt # desarrollo
```

# Crear variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
SECRET_KEY=tu_clave_secreta
DATABASE_URL=mysql://usuario:contraseña@host:3306/nombre_bd
```

# Base de datos (migraciones)

Si no está la carpeta migrations/ (iniciar por primera vez):
```bash
flask db init
```

Si hay cambios en los modelos:
```bash
flask db migrate -m "mensaje describiendo el cambio"
```

Actualizar la BD
```bash
flask db upgrade
```

# Ejecutar la app
```bash
python run.py
```