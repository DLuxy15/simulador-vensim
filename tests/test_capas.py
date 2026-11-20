"""Pruebas por capa: datos y negocio se prueban sin servidor web."""
from pathlib import Path
import sys
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vensimlab.datos.repositorio import RepositorioModelos
from vensimlab.negocio.servicio import ErrorNegocio, ServicioModelos

def test_datos_guarda_y_elimina():
    repo = RepositorioModelos()
    k = repo.nuevo_espacio()
    assert not repo.existe(k)
    repo.guardar_ejemplo(k)
    assert repo.existe(k)
    repo.eliminar(k)
    assert not repo.existe(k)

def test_negocio_sin_web():
    s = ServicioModelos(RepositorioModelos())
    k, inv, nombre = s.cargar()
    assert nombre == 'poblacion.mdl' and len(inv['variables']) == 10
    r = s.simular(k, {'columns': ['Poblacion'], 'final': 10, 'step': 1, 'saveper': 1})
    assert len(r['rows']) == 11
    with pytest.raises(ErrorNegocio):
        s.simular(k, {'columns': []})
    with pytest.raises(ErrorNegocio):
        s.simular('x', {'columns': ['Poblacion']})
