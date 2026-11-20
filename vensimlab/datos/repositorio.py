"""CAPA DE DATOS: guarda y recupera archivos .mdl en una carpeta temporal.
No conoce Flask ni PySD. Solo maneja archivos."""
import atexit
from pathlib import Path
import shutil
import tempfile
import uuid

EJEMPLO = Path(__file__).resolve().parent / 'ejemplos' / 'poblacion.mdl'


class RepositorioModelos:
    def __init__(self):
        self._temp = tempfile.TemporaryDirectory(prefix='vensim_lab_')
        atexit.register(self._temp.cleanup)
        self.raiz = Path(self._temp.name)

    def nuevo_espacio(self):
        """Crea una carpeta nueva para un modelo y devuelve su id."""
        clave = uuid.uuid4().hex
        (self.raiz / clave).mkdir()
        return clave

    def carpeta(self, clave):
        return self.raiz / clave

    def ruta_modelo(self, clave):
        return self.raiz / clave / 'modelo.mdl'

    def existe(self, clave):
        return isinstance(clave, str) and len(clave) == 32 and self.ruta_modelo(clave).is_file()

    def guardar_ejemplo(self, clave):
        shutil.copyfile(EJEMPLO, self.ruta_modelo(clave))

    def guardar_subida(self, clave, archivo):
        archivo.save(self.ruta_modelo(clave))

    def eliminar(self, clave):
        if isinstance(clave, str) and len(clave) == 32:
            shutil.rmtree(self.raiz / clave, ignore_errors=True)
