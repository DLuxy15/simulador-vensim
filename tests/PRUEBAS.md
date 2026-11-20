# Validación realizada

Entorno de prueba: Python 3.10.12, Linux, PySD 3.14.3, Flask 3.1.2 y Plotly 6.5.0.
Navegador: Chromium 141, escritorio 1440 × 1050 y pantalla estrecha 390 × 844.

## Pruebas automáticas del servidor

15 pruebas aprobadas (`python -m pytest -q`):

- Carga del ejemplo, inventario de 10 variables, identificación del stock y
  6 dependencias, incluidos los bucles de realimentación.
- Carga por archivo adjunto .mdl, además del botón de ejemplo.
- Simulación de 201 instantes y comparación numérica con la solución discreta
  esperada: `1000 * (1 + 0.02 * 0.25) ** 200`.
- CSV completo y tiempos personalizados. Dos ejecuciones consecutivas parten
  de las condiciones originales.
- Rechazo de extensión incorrecta y modelo inválido. Una carga fallida no
  sustituye el modelo que ya estaba activo.
- Errores al simular sin modelo, sin variables, con variable inexistente,
  paso cero, intervalo menor al paso, final anterior al inicio, demasiados
  pasos o tiempo no finito.
- Límite de carga de 5 MB, verificación de sesión local y host, Plotly servido
  desde la instalación local.

## Prueba de interfaz real

- Carga del ejemplo desde la página.
- Inventario y filtro por nombre.
- Selección simultánea de Poblacion, Nacimientos y Defunciones.
- Simulación desde la interfaz, 50 filas visibles por página.
- Descarga real del CSV con 201 filas de datos.
- Gráfico con 3 series y cambio a 3 gráficos separados.
- Mapa SVG con 5 variables y enfoque de una variable (2 nodos en su entorno).
- Sin errores JavaScript durante ese recorrido.
- Capturas inspeccionadas del inicio, inventario, tabla, gráfico, mapa y
  pantalla estrecha. Contraste oscuro/azul, etiquetas y distribución legibles;
  la página no desborda horizontalmente. Las tablas y el mapa tienen su propio
  desplazamiento horizontal cuando lo necesitan.

Las capturas se usan como evidencia de validación, no como una promesa de
compatibilidad con cualquier modelo. El usuario no facilitó un modelo propio.
No se ejecutó en Windows ni macOS. El mapa es una reconstrucción de
**dependencias**, no del sketch original de Vensim.

## Actualización de la versión 2 (20 nov 2026)

Cambio solo en la capa de presentación: alto inicial del gráfico cercano a la
proporción 4:3 según el ancho disponible (420 a 950 px) y control **Tamaño**
(deslizador de 320 a 1100 px) que ajusta el alto de todos los gráficos sin
volver a simular. No cambió la API, la simulación ni las demás vistas.

- 17 pruebas automáticas aprobadas (`python -m pytest -q`), mismas 17 de la
  versión por capas.
- Verificación visual con Chromium real, 1440 × 1050: ejemplo cargado,
  3 series superpuestas a 947 px de alto, deslizador aplicado a 400, 500 y
  950 px con redibujado correcto, y 3 gráficos separados que toman la misma
  altura. Sin errores JavaScript durante el recorrido.
