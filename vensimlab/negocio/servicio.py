"""CAPA DE NEGOCIO: reglas de la aplicacion. Valida pedidos, llama a PySD
(en un proceso aparte, ver worker.py) y devuelve datos simples.
No conoce Flask ni sabe donde se guardan los archivos."""
import json
from pathlib import Path
import subprocess
import sys
import uuid

WORKER = Path(__file__).resolve().parent / 'worker.py'


class ErrorNegocio(ValueError):
    """Error con mensaje claro para mostrar al usuario."""


class ServicioModelos:
    def __init__(self, repositorio):
        self.repo = repositorio

    def cargar(self, subida=None, nombre=None):
        """Carga el ejemplo (subida=None) o un archivo subido. Devuelve (clave, inventario, nombre)."""
        if subida is None:
            nombre = 'poblacion.mdl'
        else:
            if not nombre or not nombre.lower().endswith('.mdl'):
                raise ErrorNegocio('Elige un archivo Vensim con extension .mdl (no .vpm).')
            nombre = Path(nombre.replace('\\', '/')).name
        clave = self.repo.nuevo_espacio()
        try:
            if subida is None:
                self.repo.guardar_ejemplo(clave)
            else:
                self.repo.guardar_subida(clave, subida)
            inventario = self._worker(clave, 'inspect')
        except (ErrorNegocio, OSError):
            self.repo.eliminar(clave)
            raise
        return clave, inventario, nombre

    def reemplazar(self, anterior):
        self.repo.eliminar(anterior)

    def simular(self, clave, pedido):
        if not self.repo.existe(clave):
            raise ErrorNegocio('Carga primero un modelo .mdl.')
        if not isinstance(pedido, dict):
            raise ErrorNegocio('Solicitud invalida.')
        datos = {k: pedido[k] for k in ('columns', 'final', 'step', 'saveper') if k in pedido}
        return self._worker(clave, 'run', **datos)

    def _worker(self, clave, accion, **kwargs):
        carpeta = self.repo.carpeta(clave)
        trabajo = uuid.uuid4().hex
        entrada, salida = carpeta / f'{trabajo}.json', carpeta / f'{trabajo}.out.json'
        entrada.write_text(json.dumps({'model': str(self.repo.ruta_modelo(clave)), 'action': accion, **kwargs}), encoding='utf-8')
        try:
            proceso = subprocess.run([sys.executable, str(WORKER), str(entrada), str(salida)], cwd=carpeta,
                                     capture_output=True, text=True, timeout=90)
            if proceso.returncode or not salida.exists():
                raise ErrorNegocio('PySD no pudo procesar el modelo. Revisa que sea compatible y no necesite archivos externos.')
            resultado = json.loads(salida.read_text(encoding='utf-8'))
            if not resultado['ok']:
                raise ErrorNegocio(resultado['error'])
            return resultado['result']
        except subprocess.TimeoutExpired:
            raise ErrorNegocio('Se alcanzo el limite de 90 segundos. Prueba un modelo u horizonte mas pequeno.') from None
        finally:
            entrada.unlink(missing_ok=True)
            salida.unlink(missing_ok=True)
