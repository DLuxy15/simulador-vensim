# Vensim Lab

Sistema web **local** en Python para explorar y simular modelos Vensim con PySD.
Interfaz en español, modo oscuro, acentos azules y tipografía legible.

**Versión 2** (noviembre 2026): los gráficos son más altos, con una proporción
cercana a 4:3 sin reducir el ancho, y la pestaña Gráficos incluye un control
**Tamaño** para ajustar su alto en pantalla.

## 1. Qué necesitas

- Python **3.10, 3.11 o 3.12**, de 64 bits. Recomendado: **3.11**.
  Comprueba tu versión con `python --version` (Windows) o `python3 --version` (macOS/Linux).
  No se ha probado con Python 3.13 o versiones posteriores.
- VS Code y un navegador moderno (Chrome, Edge o Firefox).
- Internet para instalar las dependencias la primera vez. Después, la interfaz,
  las simulaciones y los gráficos funcionan sin internet. No usa un CDN.
- No necesitas tener Vensim instalado.

El proyecto se ha probado con Python 3.10.12 en Linux. Se incluyen instrucciones
para Windows, macOS y Linux, pero no se ha ejecutado en una PC Windows o Mac.
No se incluye una carpeta .venv precreada: los entornos virtuales no son portables.
Los comandos de abajo crean un venv real en tu propia PC.

## 2. Extraer y abrir

1. Extrae **todo** el contenido recibido en una carpeta, por ejemplo `Documentos/vensim-lab`.
2. En VS Code: **Archivo > Abrir carpeta**, elige la carpeta extraída (la que contiene `run.py`).
3. Abre **Terminal > Nueva terminal**. Todos los comandos siguientes se ejecutan allí.

## 3. Crear el venv, instalar y ejecutar

### Windows (PowerShell o CMD)

Ejecuta cada línea por separado:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run.py
```

Si no tienes el comando `py`, pero `python --version` muestra Python 3.10 a 3.12,
usa `python -m venv .venv` como primera línea. Si tienes Python 3.10 o 3.12 con
el lanzador `py`, cambia `-3.11` por tu versión.

No es obligatorio activar el venv: estos comandos usan directamente su Python,
por lo que funcionan aunque PowerShell bloquee `Activate.ps1`. No necesitas
cambiar la política de seguridad de PowerShell.

Activación opcional, si prefieres usar después `python run.py`:
- PowerShell: `.\.venv\Scripts\Activate.ps1`
- CMD: `.venv\Scripts\activate.bat`

### macOS / Linux (bash o zsh)

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run.py
```

Usa un `python3` de la versión indicada. En Linux puede ser necesario instalar
el paquete `python3-venv` de tu distribución. Activación opcional:
`source .venv/bin/activate`.

### Abrir la aplicación

Con el servidor encendido, abre **http://127.0.0.1:5000** en tu navegador.
Mantén la terminal abierta. Para detenerlo: **Ctrl+C**.

En VS Code, puedes instalar la extensión oficial Python de Microsoft, abrir
la paleta (**Ctrl+Shift+P**, o **Cmd+Shift+P** en Mac), elegir **Python: Select
Interpreter** y seleccionar el Python dentro de `.venv`.

### Volver a abrirlo otro día

Abre esta carpeta en VS Code y ejecuta solo la última línea de tu sistema:
` .\.venv\Scripts\python.exe run.py` en Windows, o `.venv/bin/python run.py`
en macOS/Linux. No hace falta reinstalar cada vez.

## 4. Probar sin tener un modelo a mano

1. Pulsa **Probar ejemplo**. Carga `examples/poblacion.mdl`, creado para este proyecto.
2. En **Variables** verás un stock llamado Poblacion, nacimientos, defunciones,
   tasas y los controles de tiempo.
3. Abre **Tabla**. Poblacion ya estará seleccionada. Puedes marcar también
   Nacimientos y Defunciones. Pulsa **Ejecutar simulación**.
4. Con la configuración original: inicio 0, fin 50, paso e intervalo 0.25,
   obtendrás 201 filas. La población inicial es 1000 y la final es
   aproximadamente **2711.517123** (integración de Euler).
5. Abre **Gráficos**. Puedes superponer series o ver una por variable, hacer
   zoom, ocultar series y descargar una imagen desde la barra del gráfico.
   Los gráficos usan un alto cercano a la proporción 4:3; ajústalo con el
   control **Tamaño** de esa pestaña (solo cambia la vista, no los datos).
6. En **Tabla**, **Descargar CSV** exporta todas las filas. La pantalla muestra
   50 filas por página y hasta 6 decimales; el CSV no usa ese redondeo visual.
7. En **Mapa del modelo**, verás un mapa automático de dependencias. Enfoca
   una variable para ver solo su entorno directo.

## 5. Usar tu modelo Vensim

- Exporta o guarda un archivo de texto **.mdl** desde Vensim. No sirve un .vpm,
  una captura ni un PDF. Carga el archivo con **Cargar archivo**.
- El inventario muestra el nombre original, tipo, unidades y descripción.
  Los stocks se reconocen por el subtipo **Integ** de PySD. Los “flujos
  asociados” se infieren por su dependencia de un stock: puede haber
  auxiliares en ese grupo. No es una clasificación perfecta de los símbolos
  del dibujo original. Otros elementos con memoria aparecen como Estado.
- Selecciona hasta 30 variables y configura tiempo final, paso e intervalo.
  El inicio se toma del modelo. Cada ejecución parte de las condiciones
  originales, no de la ejecución anterior.
- Tabla y gráficos comparten la última ejecución. Si cambias la selección o
  los tiempos, vuelve a ejecutar. El CSV queda deshabilitado hasta hacerlo.
- Si hay variables con subíndices, PySD las convierte en columnas por serie.
  En las tablas/gráficos verás sus nombres expandidos.
- No cambia ecuaciones, no edita parámetros y no guarda escenarios.

### El mapa gráfico que sí se incluye

Está probado con el ejemplo. Es un **mapa de dependencias**, no una reproducción
exacta del boceto/sketch de Vensim ni un editor de stock-flujo. Flecha A → B:
B utiliza A. No incluye polaridades (+/−), coordenadas ni símbolos del dibujo.
Organiza constantes, auxiliares/flujos y stocks en columnas. Muestra hasta
80 nodos; con modelos grandes usa el selector de enfoque. Los nombres largos
se acortan en pantalla y se ven completos al pasar el cursor. Es una vista de
ayuda, no sustituye validar el modelo en Vensim.

## 6. Seguridad, privacidad y límites

- **Solo modelos propios o de confianza.** PySD traduce el .mdl a Python y
  ejecuta ese código en tu PC con tus permisos. El subproceso y el tiempo
  límite evitan algunos bloqueos, pero **NO son una caja de seguridad**.
- Servidor solo en `127.0.0.1`, sin modo debug. No lo publiques en internet,
  no cambies a `0.0.0.0` y no lo uses como un servicio multiusuario.
- La carga y la simulación no envían el modelo a un servicio externo.
  Un modelo que haga referencia a recursos externos no queda garantizado
  por esa afirmación: usa modelos autocontenidos y de confianza.
- Hasta 5 MB por carga, 90 segundos por traducción/ejecución, 100 000 pasos,
  10 001 filas y 300 000 celdas de salida. Hasta 200 series expandidas.
- Los archivos se procesan en una carpeta temporal del sistema. Al sustituir
  un modelo en la misma sesión se elimina el anterior; al cerrar normalmente
  el servidor se elimina la carpeta temporal. Un cierre forzado podría dejar
  restos en temporales. No se borran tus .mdl originales.
- El navegador pierde los resultados al recargar. Descarga el CSV antes.
- Se admite un .mdl autocontenido. Esta versión no sube Excel/CSV/VDF ni otras
  dependencias; modelos con datos externos, funciones no soportadas,
  macros especiales o errores pueden fallar. PySD no es equivalente a todo
  Vensim. El mensaje de error muestra el motivo que devuelve PySD.
- Revisa unidades, método numérico y resultados antes de usarlo en un trabajo.
  No se ha probado tu modelo particular, porque todavía no se proporcionó uno.

## 7. Problemas frecuentes

**No abre la página:** comprueba que la terminal esté ejecutando `run.py` y
que uses `http`, no `https`. El navegador y el servidor deben estar en la misma PC.

**Puerto ocupado:** cierra la otra aplicación o cambia el puerto:
- PowerShell: `$env:PORT="5001"; .\.venv\Scripts\python.exe run.py`
- CMD: `set PORT=5001` y luego `.venv\Scripts\python.exe run.py`
- macOS/Linux: `PORT=5001 .venv/bin/python run.py`
Entonces abre `http://127.0.0.1:5001`.

**No se instala:** comprueba versión y arquitectura de Python, conexión,
espacio disponible y que ejecutas el pip del venv. No hace falta Graphviz.
Si tu conexión corporativa bloquea PyPI, usa otra red autorizada.

**Error de modelo:** prueba primero el ejemplo. Si funciona, revisa la
compatibilidad de tu .mdl con PySD y si requiere datos externos. No renombres
un .vpm a .mdl. El inventario no aparecerá si la inicialización del modelo falla.

**No hay datos / curvas interrumpidas:** los valores no finitos se muestran
como “Sin dato” y las curvas dejan huecos; revisa las ecuaciones y el paso.

**Gráficos con unidades diferentes:** elige “Un gráfico por variable”.

## 8. Arquitectura por capas

```
run.py                         punto de entrada (arranca el servidor)
vensimlab/
  presentacion/                CAPA 1: interfaz web
    web.py                     rutas Flask, seguridad local, JSON
    templates/ static/         HTML, CSS y JavaScript (modo oscuro azul)
  negocio/                     CAPA 2: logica de la aplicacion
    servicio.py                ServicioModelos: validaciones y reglas
    worker.py                  PySD: traduce, inventaria y simula (proceso aparte)
  datos/                       CAPA 3: acceso a archivos
    repositorio.py             guarda/borra los .mdl en una carpeta temporal
    ejemplos/poblacion.mdl     modelo de demostracion
tests/                         pruebas por capa y de extremo a extremo
requirements.txt               dependencias
```

Regla: cada capa solo usa la de abajo. Presentacion llama a Negocio; Negocio
llama a Datos. Datos no conoce Flask ni PySD, y Negocio no conoce Flask.
Si quieres cambiar algo: la apariencia va en `presentacion/`, las reglas o
limites de simulacion en `negocio/`, y donde se guardan los archivos en `datos/`.

## 9. Pruebas automáticas (opcional)

Instala pytest dentro del venv y ejecuta:

```bash
python -m pip install pytest==9.0.1
python -m pytest -q
```

Sustituye `python` por la ruta completa del Python del venv si no está activado.
Las pruebas visuales realizadas se describen en `tests/PRUEBAS.md`.

## Documentación de referencia

- PySD, inicio: https://pysd.readthedocs.io/en/latest/getting_started.html
- Carga de modelos: https://pysd.readthedocs.io/en/stable/python_api/model_loading.html
- API de simulación: https://pysd.readthedocs.io/en/latest/python_api/model_class.html

Los componentes de terceros conservan sus licencias. Este proyecto es un
prototipo local para explorar y probar modelos, no un reemplazo de Vensim.
