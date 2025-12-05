# Hackathon Backend

Backend desarrollado con Python, FastAPI, MongoDB y Gemini API.

## 🏗️ Estructura del Proyecto

```
hackathon-backend/
├── app/
│   ├── __init__.py          # Inicialización del módulo
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── config.py            # Configuración de la aplicación
│   ├── database.py          # Conexión a MongoDB
│   ├── models/              # Modelos de datos para MongoDB
│   ├── schemas/             # Schemas de Pydantic para validación
│   ├── routes/              # Rutas/endpoints de la API
│   ├── services/            # Lógica de negocio y servicios externos
│   │   └── gemini_service.py # Servicio para interactuar con Gemini API
│   └── utils/               # Utilidades y funciones auxiliares
├── .env.example             # Ejemplo de variables de entorno
├── .gitignore              # Archivos a ignorar en Git
├── requirements.txt        # Dependencias del proyecto
├── server.py               # Archivo para iniciar el servidor
├── start.sh                # Script de inicio automatizado
└── README.md              # Este archivo
```

## 🚀 Inicio Rápido

El proyecto incluye un script `start.sh` que automatiza el proceso:

1. **Configurar variables de entorno:**
```bash
cp .env.example .env
```

2. **Editar el archivo `.env`** con tus credenciales:
   - `MONGODB_URL`: URL de conexión a MongoDB (obligatorio)
   - `GEMINI_API_KEY`: Tu API key de Gemini (obligatorio)
   - Otras configuraciones opcionales (ver sección de Configuración)

3. **Activar entorno virtual (si usas uno):**
```bash
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

4. **Ejecutar el script:**
```bash
./start.sh
```

El script automáticamente:
- ✅ Verifica que existe el archivo `.env`
- ✅ Detecta Python (`python3` o `python`)
- ✅ Verifica e instala dependencias solo si es necesario
- ✅ Inicia el servidor usando `server.py`

El archivo `server.py` carga automáticamente las variables de entorno desde `.env` y configura el servidor según la configuración.

## 🌐 Acceso a la aplicación

Una vez iniciada, la aplicación estará disponible en:
- **API**: http://localhost:8000
- **Documentación interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## 📁 Organización del Código

### `app/models/`
Modelos de datos para MongoDB. Define la estructura de los documentos que se almacenarán en la base de datos.

### `app/schemas/`
Schemas de Pydantic para validación de datos de entrada y salida en los endpoints.

### `app/routes/`
Rutas/endpoints de la API. Cada archivo de rutas debe ser importado y registrado en `app/routes/__init__.py`.

### `app/services/`
Lógica de negocio y servicios externos:
- `gemini_service.py`: Maneja todas las interacciones con la API de Gemini

### `app/utils/`
Funciones auxiliares y utilidades reutilizables.

## 🔧 Configuración

Todas las configuraciones se manejan a través de variables de entorno en el archivo `.env`.

### Variables Obligatorias:
- `MONGODB_URL`: URL de conexión a MongoDB
- `GEMINI_API_KEY`: Tu API key de Gemini

### Variables Opcionales:
- `HOST`: Host del servidor (default: `0.0.0.0`)
- `PORT`: Puerto del servidor (default: `8000`)
- `DEBUG`: Modo debug - activa auto-reload (default: `False`)
- `MONGODB_DB_NAME`: Nombre de la base de datos (default: `hackathon_db`)
- `GEMINI_MODEL`: Modelo de Gemini a usar (default: `gemini-pro`)
- `CORS_ORIGINS`: Orígenes permitidos para CORS (default: `["*"]`)
- `APP_NAME`: Nombre de la aplicación (default: `Hackathon Backend`)
- `APP_VERSION`: Versión de la aplicación (default: `0.1.0`)

Ver `.env.example` para un ejemplo completo.

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **MongoDB**: Base de datos NoSQL
- **Motor**: Driver asíncrono para MongoDB
- **Gemini API**: API de Google para generación de texto
- **Pydantic**: Validación de datos
