"""CAPA DE NEGOCIO (proceso aparte): usa PySD. Es un limite de tiempo, NO una caja de seguridad."""
import json
import math
import sys
from pathlib import Path
import pysd

CONTROL = {'initial_time', 'final_time', 'time_step', 'saveper', 'time'}

def describe(model):
    rows = model.doc.fillna('').to_dict('records')
    names = {r['Py Name']: r['Real Name'] for r in rows}
    deps = model.dependencies
    def public_dependencies(key, seen=None):
        seen = set() if seen is None else seen
        if key in seen:
            return set()
        seen.add(key)
        value = deps.get(key, {})
        found = set()
        for dep, inner in value.items():
            if dep in ('initial', 'step') and isinstance(inner, dict):
                for sub in inner:
                    found |= {sub} if sub in names else public_dependencies(sub, seen)
            elif dep in names:
                found.add(dep)
            elif dep.startswith('_'):
                found |= public_dependencies(dep, seen)
        return found
    stocks = {r['Py Name'] for r in rows if r['Subtype'] == 'Integ'}
    flows = set()
    for stock in stocks:
        flows |= public_dependencies(stock) - CONTROL - stocks
    variables = []
    edges = []
    for r in rows:
        py = r['Py Name']
        if py in CONTROL:
            kind = 'Control'
        elif py in stocks:
            kind = 'Stock'
        elif r['Type'] == 'Constant':
            kind = 'Constante'
        elif py in flows:
            kind = 'Flujo asociado'
        elif r['Type'] == 'Stateful':
            kind = 'Estado'
        else:
            kind = 'Auxiliar'
        variables.append({'name': r['Real Name'], 'py': py, 'kind': kind,
                          'units': str(r['Units']), 'description': str(r['Comment']),
                          'subtype': str(r['Subtype'])})
        for dep in public_dependencies(py):
            if dep != py and dep not in CONTROL and py not in CONTROL:
                edges.append({'source': names[dep], 'target': names[py]})
    return {'variables': variables, 'edges': edges,
            'defaults': {'initial': float(model.time.initial_time()),
                         'final': float(model.time.final_time()),
                         'step': float(model.time.time_step()),
                         'saveper': float(model.time.saveper())}}

def execute(job):
    model = pysd.read_vensim(str(Path(job['model']).resolve()))
    info = describe(model)
    if job['action'] == 'inspect':
        return info
    columns = job.get('columns', [])
    allowed = {v['name'] for v in info['variables']}
    if not columns or len(columns) > 30 or any(v not in allowed for v in columns):
        raise ValueError('Selecciona entre 1 y 30 variables del modelo.')
    start = info['defaults']['initial']
    final = float(job.get('final', info['defaults']['final']))
    step = float(job.get('step', info['defaults']['step']))
    saveper = float(job.get('saveper', info['defaults']['saveper']))
    if not all(math.isfinite(v) for v in (start, final, step, saveper)):
        raise ValueError('Los tiempos deben ser numeros finitos.')
    if final <= start or step <= 0 or saveper < step:
        raise ValueError('El fin debe superar al inicio; el paso debe ser positivo y el intervalo de salida no menor que el paso.')
    if (final-start)/step > 100000 or (final-start)/saveper > 10000:
        raise ValueError('Limite: 100 000 pasos y 10 001 filas. Reduce el horizonte o aumenta el paso/intervalo.')
    frame = model.run(return_columns=columns, final_time=final, time_step=step, saveper=saveper, flatten_output=True)
    if len(frame.columns) > 200 or len(frame)*len(frame.columns) > 300000:
        raise ValueError('La salida es demasiado grande. Selecciona menos variables o aumenta el intervalo.')
    frame.index.name = 'Tiempo'
    # pandas serializes missing and infinite values as null, valid JSON.
    data = json.loads(frame.reset_index().to_json(orient='split', double_precision=10))
    return {'columns': data['columns'], 'rows': data['data'], 'csv': frame.to_csv(),
            'settings': {'initial': start, 'final': final, 'step': step, 'saveper': saveper}}

if __name__ == '__main__':
    target = Path(sys.argv[2])
    try:
        result = execute(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')))
        payload = {'ok': True, 'result': result}
    except Exception as exc:
        payload = {'ok': False, 'error': f'{type(exc).__name__}: {str(exc)[:1200]}'}
    target.write_text(json.dumps(payload, ensure_ascii=False, allow_nan=False), encoding='utf-8')
