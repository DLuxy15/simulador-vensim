"""CAPA DE PRESENTACION: servidor web Flask, rutas, plantillas y estilos.
Solo traduce entre HTTP y el servicio de negocio."""
import hmac
import secrets
from flask import Flask, Response, jsonify, render_template, request, session
from plotly.offline import get_plotlyjs
from ..datos.repositorio import RepositorioModelos
from ..negocio.servicio import ErrorNegocio, ServicioModelos


def crear_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)
    app.config.update(MAX_CONTENT_LENGTH=5*1024*1024, SESSION_COOKIE_SAMESITE='Strict', SESSION_COOKIE_HTTPONLY=True)
    servicio = ServicioModelos(RepositorioModelos())

    @app.before_request
    def solo_local():
        if request.method == 'POST' and (not session.get('token') or not hmac.compare_digest(request.headers.get('X-Local-Token', ''), session['token'])):
            return jsonify(error='Recarga la pagina para iniciar una sesion local.'), 403

    @app.after_request
    def cabeceras(respuesta):
        respuesta.headers['X-Content-Type-Options'] = 'nosniff'
        respuesta.headers['X-Frame-Options'] = 'DENY'
        respuesta.headers['Cache-Control'] = 'no-store'
        return respuesta

    @app.errorhandler(413)
    def muy_grande(error):
        return jsonify(error='El archivo supera el limite de 5 MB.'), 413

    @app.get('/')
    def inicio():
        session.setdefault('token', secrets.token_hex(32))
        return render_template('index.html', token=session['token'])

    @app.get('/static/plotly-local.js')
    def plotly_local():
        return Response(get_plotlyjs(), mimetype='application/javascript')

    @app.post('/api/load')
    def cargar():
        try:
            if request.form.get('demo') == 'true':
                clave, inventario, nombre = servicio.cargar()
            else:
                archivo = request.files.get('model')
                if not archivo:
                    raise ErrorNegocio('Elige un archivo Vensim con extension .mdl (no .vpm).')
                clave, inventario, nombre = servicio.cargar(archivo, archivo.filename)
            anterior = session.get('model_id')
            session['model_id'] = clave
            if anterior:
                servicio.reemplazar(anterior)
            return jsonify(**inventario, filename=nombre)
        except (ErrorNegocio, OSError) as exc:
            return jsonify(error=str(exc)), 400

    @app.post('/api/run')
    def simular():
        try:
            pedido = request.get_json(silent=True) or {}
            return jsonify(servicio.simular(session.get('model_id', ''), pedido))
        except (ErrorNegocio, TypeError, OSError) as exc:
            return jsonify(error=str(exc)), 400

    return app
