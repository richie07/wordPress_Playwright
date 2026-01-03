# WordPress Login Automation Framework

Este proyecto es un framework de pruebas automatizadas para validar el login de WordPress utilizando **Playwright**, **Python** y **Cucumber (pytest-bdd)**.

Sigue el patrón **Page Object Model (POM)** e incluye una clase `BasePage` (Wrapper) para centralizar las interacciones con Playwright.

## 🛠️ Tecnologías
- **Python 3.x**
- **Playwright**: Automatización del navegador.
- **pytest**: Runner de pruebas.
- **pytest-bdd**: Implementación de BDD (Gherkin) para pytest.

## 🚀 Instalación y Configuración

### 1. Clonar o descagar el proyecto
Asegúrate de estar en la carpeta raíz del proyecto.

### 2. Crear entorno virtual (Recomendado)
```bash
python3 -m venv venv
source venv/bin/activate  # En Mac/Linux
# venv\Scripts\activate   # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
*Si tienes problemas con `pip`, prueba usando `python3 -m pip install -r requirements.txt`.*

### 4. Instalar navegadores de Playwright
Es necesario instalar los binarios de los navegadores para que Playwright funcione.
```bash
playwright install
```

## 🏃‍♂️ Ejecución de Pruebas

Para ejecutar todos los escenarios definidos en los archivos `.feature`:

```bash
python3 -m pytest
```

### Opciones útiles:
- **Ver el navegador (Headed)**: Por defecto los tests corren en modo "Headless" (sin ventana). Para ver el navegador, usa `--headed`:
  ```bash
  python3 -m pytest --headed
  ```
- **Modo lento (Slowmo)**: Configurado a 500ms en `pytest.ini` para poder observar las acciones si usas `--headed`.

### Ejecución por etiquetas (Tags)
Puedes filtrar qué tests ejecutar usando etiquetas (`@login`, `@user`).

**Ejecutar solo Login:**
```bash
python3 -m pytest -m login
```

**Ejecutar solo Usuarios:**
```bash
python3 -m pytest -m user
```

**Ejecutar Login O Usuarios:**
```bash
python3 -m pytest -m "login or user"
```

### Ejecución en Paralelo (Nuevo)
Para ejecutar los tests más rápido usando múltiples núcleos de tu CPU, usa el flag `-n auto`:

```bash
# Ejecutar usando todos los núcleos disponibles
python3 -m pytest -n auto

# Ejecutar usando 3 procesos paralelos
python3 -m pytest -n 3
```

### Configuración de Ambientes (Environments)
El proyecto soporta múltiples ambientes (dev, staging, prod) controlados por la variable de entorno `ENV`.
Por defecto usa `dev`.

Para ejecutar en **staging**:
```bash
ENV=staging python3 -m pytest
```

Para ejecutar en **prod**:
```bash
ENV=prod python3 -m pytest
```

Los URLs se gestionan en `utils/config.py`.

### Reportes y CI/CD
**Reporte HTML**:
Al ejecutar los tests, se genera automáticamente un archivo `report.html` con los resultados.
Abrir en el navegador:
```bash
open report.html
```

**CI/CD (GitHub Actions)**:
Se ha configurado un pipeline en `.github/workflows/ci.yml`.
Cada vez que hagas push a `main`:
1. Instala dependencias y browsers.
2. Ejecuta los tests en modo Headless.
3. Sube dos artefactos descargables: `test-report` (HTML) y `automation-logs`.

### Logging
El framework genera logs automáticos de todas las interacciones con el navegador (clicks, navegación, etc).
- **Consola**: Se muestran mientras corren los tests.
- **Archivo**: Se guardan en `automation.log` en la raíz del proyecto.
- **Seguridad**: Los campos de contraseña se ocultan automáticamente (`*****`).

### Debugging
Para aprender y seguir el flujo paso a paso, tienes dos opciones:

**1. Playwright Inspector**
Muestra una ventana visual paso a paso.
```bash
PWDEBUG=1 python3 -m pytest -m user
```

**2. Python Debugger (PDB)**
Detiene la ejecución donde pongas el breakpoint `import pdb; pdb.set_trace()`.
Usa el flag `-s` para poder interactuar con la consola.
```bash
python3 -m pytest -m user -s
```

## 📂 Estructura del Proyecto

```text
/
├── features/               # Archivos .feature (Gherkin)
│   └── login.feature       # Escenarios de prueba de Login
├── pages/                  # Page Objects
│   ├── base_page.py        # Wrapper de Playwright (click, fill, etc.)
│   └── login_page.py       # Lógica específica de la página de Login
├── tests/                  # Step Definitions (Código de prueba)
│   ├── test_login.py       # Vincula los pasos Gherkin con el código Python
│   └── __init__.py
├── pytest.ini              # Configuración de Pytest (opciones slowmo, headed)
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```

## 📝 Notas
- La URL base está configurada en `pages/login_page.py` apuntando a `http://localhost:8080/wp-login.php`.
- Si tu entorno de WordPress tiene una URL diferente, actualízala en ese archivo.
