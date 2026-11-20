"""Punto de entrada. Arranca con: python run.py"""
import os
from vensimlab.presentacion.web import crear_app

app = crear_app()

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', '5000'))
    print(f'Abre http://127.0.0.1:{puerto} en tu navegador. Ctrl+C para cerrar.')
    app.run(host='127.0.0.1', port=puerto, debug=False)
