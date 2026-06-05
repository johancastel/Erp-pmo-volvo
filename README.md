# Volvo Group Colombia - ERP PMO (Control de Flota y Novedades)

Este es el módulo de control operativo, registro de novedades y seguimiento de mantenimiento de la flota de vehículos de **Volvo Group Colombia**. La aplicación está construida sobre **Streamlit** y soporta un motor de base de datos híbrido (MySQL local con fallback automático a SQLite).

El sistema cuenta con un diseño visual corporativo premium de Volvo en modo oscuro y se encuentra completamente estructurado bajo una arquitectura modular y escalable.

---

## 📁 Estructura del Proyecto (Arquitectura Modular)

El código del proyecto se encuentra estructurado en capas para separar la interfaz de usuario, la persistencia, la lógica de negocio y las configuraciones del sistema:

```text
02_Proyecto_ERP_PMO/
├── .streamlit/
│   └── config.toml             # Configuración nativa del tema y puerto de Streamlit
├── src/
│   ├── __init__.py             # Inicializador de paquete de Python
│   ├── app.py                  # Flujo de ejecución principal e inyección de JS
│   ├── styles.py               # Inyección de CSS premium corporativo de Volvo
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Mapeos de patios (flota real) y credenciales por defecto
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py       # Manager de conexión híbrida (MySQL y SQLite fallback)
│   │   ├── queries/
│   │   │   ├── __init__.py
│   │   │   └── sql_templates.py # Plantillas de sentencias SQL y esquemas de tablas
│   │   └── repositories/
│   │       ├── __init__.py
│   │       └── novedades_repository.py # Repositorio CRUD y migración automática
│   ├── services/
│   │   ├── __init__.py
│   │   ├── cache_service.py    # Inicialización del estado de sesión en Streamlit
│   │   ├── export_service.py   # Lógica de generación y empaquetado Excel/CSV/ZIP
│   │   ├── mantenimiento_service.py # Procesamiento de datos de mantenimientos
│   │   └── validation_service.py # Validación de inputs y reglas de negocio
│   └── ui/
│       ├── __init__.py
│       ├── components/
│       │   ├── __init__.py
│       │   ├── header.py       # Banner corporativo superior dinámico
│       │   └── navigation.py   # Menú lateral, filtros y formulario de conexión
│       ├── forms/
│       │   ├── __init__.py
│       │   ├── electrical_form.py  # Formulario del área eléctrica
│       │   ├── levels_form.py      # Formulario del área de niveles
│       │   └── mechanical_form.py  # Formulario del área mecánica
│       ├── pages/
│       │   ├── __init__.py
│       │   ├── atender_novedades.py # Panel de visualización y respuesta a novedades
│       │   ├── exportar_datos.py    # Filtros y zona de descarga de reportes
│       │   └── ingreso_novedades.py # Selector de vehículos y orquestador de formularios
│       └── tables/
│           ├── __init__.py
│           └── desktop_grid.py # Grid/Tabla interactiva avanzada con paginación
├── 01_Modulo_Noveades.py       # Punto de entrada de la aplicación (Orquestador de arranque)
├── erp_pmo.db                  # Base de datos SQLite (Generada automáticamente en contingencia)
└── README.md                   # Documentación y manual del proyecto (este archivo)
```

---

## ✨ Características Clave e Innovaciones

### 🗄️ 1. Persistencia de Datos Híbrida (Robusta y con Fallback)
* **Modo MySQL Local (BI Ready)**: Intenta conectarse a un servidor local MySQL en `127.0.0.1:3306`. Permite integrar los registros de auditoría directamente en Power BI u otros tableros corporativos.
* **Fallback SQLite (Respaldo en Contingencia)**: Si no detecta MySQL activo, la aplicación conmuta automáticamente al archivo de base de datos local `erp_pmo.db`, asegurando el funcionamiento ininterrumpido sin pérdida de registros.
* **Control Remoto**: Los técnicos y administradores pueden modificar y verificar las credenciales de conexión en tiempo real en la barra lateral en la sección **⚙️ Conexión MySQL Local**.

### 🎨 2. Experiencia de Usuario y Diseño Corporativo Volvo
* **Tema Oscuro Premium**: Diseñado con paletas de color HSL exclusivas (`#0b1320` como fondo, `#122135` en cabeceras y `#152232` en tarjetas de métricas).
* **Adaptabilidad (Responsive Layout)**: Se redimensiona automáticamente de forma elegante en pantallas móviles y computadoras.
* **Mejoras UX mediante Javascript Inyectado**:
  1. **Solución al bug de Streamlit (Input Focus)**: Fuerza un evento `blur()` en las cajas de texto al hacer clic en cualquier botón. Esto previene que se omitan los cambios no guardados.
  2. **Limpieza del Prefijo "Add "**: Elimina de forma dinámica las etiquetas de Streamlit en selecciones interactivas.
  3. **Auto-colapso en Celular**: Contrae de manera automática el menú lateral cuando un técnico selecciona un formulario en pantallas móviles, optimizando el área útil de trabajo.

### 📋 3. Formularios Técnicos Especializados
Las novedades están estructuradas y segmentadas en tres tipos de cuestionarios:
* **Eléctrico**: Luces, baterías, tableros de instrumentos, cableados y fusibles.
* **Mecánico**: Motor, caja de cambios, embragues, frenos, dirección, suspensión y llantas.
* **Niveles**: Aceites (motor/transmisión), refrigerante, líquido de dirección y frenos, y niveles de AdBlue (Urea).

### 📊 4. Panel de Seguimiento (Atender Novedades)
Permite visualizar la lista histórica de novedades registradas en una grilla interactiva, filtrar de forma rápida y responder a los problemas indicando:
* Estado de la atención (Abierta, En Proceso, Cerrada).
* Severidad real.
* Diagnóstico técnico y repuestos/insumos utilizados.

---

## 📊 Distribución Real de la Flota (451 Móviles)

La flota total consta de **451 vehículos** con sus identificaciones reales de operación, distribuidos en **7 patios** específicos:

* **20 DE JULIO**: 203 vehículos (ej. `D500`, `N635`)
* **CALLE 191**: 48 vehículos (ej. `N0850`, `Z10-7329`)
* **CONEJERA**: 59 vehículos (ej. `Z10-7125`, `Z10-7331`)
* **EEMB**: 50 vehículos (ej. `CO-0617`, `CO-0666` - Flota Eléctrica)
* **ENGATIVA**: 20 vehículos (ej. `Z10-7258`, `Z10-7330`)
* **GAVIOTAS**: 60 vehículos (ej. `Z15-7034`, `Z15-7123`)
* **SUBA**: 11 vehículos (ej. `Z10-7267`, `Z10-7333`)

---

## 🛠️ Requisitos e Instalación

Para ejecutar este proyecto de forma local, necesitarás tener instalado **Python 3.8 o superior**.

### 1. Clonar e Instalar dependencias necesarias:
Ejecuta el siguiente comando para instalar las librerías necesarias:
```bash
pip install streamlit pandas pymysql pillow openpyxl
```
*(Nota: `sqlite3` viene incorporado de forma nativa en la instalación estándar de Python).*

### 2. Arrancar la aplicación con Streamlit:
Dado que el comando global `streamlit` podría no estar mapeado en el `PATH` de Windows en todos los entornos, la forma más recomendada y segura de correr el proyecto es mediante el módulo de python:
```bash
python -m streamlit run 01_Modulo_Noveades.py
```

La terminal desplegará los enlaces locales para ver el aplicativo:
* **Local:** `http://localhost:8501`
* **Red:** `http://<TU_IP_LOCAL>:8501`

---

## 🔒 Privacidad y Soporte
Este sistema es propiedad exclusiva de **Volvo Group Colombia**. El acceso y modificación de datos de la flota está restringido a personal técnico autorizado y auditores PMO de patio.
