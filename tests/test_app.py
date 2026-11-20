import io
import math
from pathlib import Path
import sys
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        c.get('/')
        with c.session_transaction() as s:
            c.environ_base['HTTP_X_LOCAL_TOKEN'] = s['token']
        yield c

def load(client):
    r=client.post('/api/load',data={'demo':'true'})
    assert r.status_code==200,r.json
    return r.json

def test_example_metadata_and_dependencies(client):
    data=load(client)
    assert len(data['variables'])==10
    assert [v['name'] for v in data['variables'] if v['kind']=='Stock']==['Poblacion']
    assert {'source':'Nacimientos','target':'Poblacion'} in data['edges']
    assert {'source':'Poblacion','target':'Nacimientos'} in data['edges']
    assert len(data['edges'])==6

def test_simulation_numeric_and_csv(client):
    load(client)
    r=client.post('/api/run',json={'columns':['Poblacion','Nacimientos','Defunciones'],'final':50,'step':.25,'saveper':.25})
    assert r.status_code==200,r.json
    data=r.json
    assert len(data['rows'])==201
    assert data['rows'][0]==[0,1000,30,10]
    assert math.isclose(data['rows'][-1][1],1000*(1+.02*.25)**200,rel_tol=1e-9)
    assert len(data['csv'].strip().splitlines())==202

def test_custom_times_and_repeated_run_starts_original(client):
    load(client)
    for _ in range(2):
        r=client.post('/api/run',json={'columns':['Poblacion'],'final':10,'step':.5,'saveper':1})
        assert r.status_code==200,r.json
        assert len(r.json['rows'])==11
        assert r.json['rows'][0][1]==1000

def test_user_upload_and_invalid_extension(client):
    path=Path(__file__).resolve().parents[1]/'vensimlab/datos/ejemplos/poblacion.mdl'
    r=client.post('/api/load',data={'model':(io.BytesIO(path.read_bytes()),'mi_modelo.mdl')})
    assert r.status_code==200
    assert r.json['filename']=='mi_modelo.mdl'
    assert client.post('/api/load',data={'model':(io.BytesIO(b'abc'),'test.py')}).status_code==400

def test_bad_model_keeps_previous(client):
    load(client)
    assert client.post('/api/load',data={'model':(io.BytesIO(b'not a model'),'bad.mdl')}).status_code==400
    assert client.post('/api/run',json={'columns':['Poblacion']}).status_code==200

def test_missing_model(client):
    assert client.post('/api/run',json={'columns':['Poblacion']}).status_code==400

@pytest.mark.parametrize('body',[
    {'columns':[]}, {'columns':['No existe']}, {'columns':['Poblacion'],'step':0},
    {'columns':['Poblacion'],'saveper':.01}, {'columns':['Poblacion'],'final':-1},
    {'columns':['Poblacion'],'step':.000001}, {'columns':['Poblacion'],'final':'nan'}])
def test_invalid_settings(client,body):
    load(client)
    r=client.post('/api/run',json=body)
    assert r.status_code==400,r.json
    assert r.json['error']

def test_csrf_host_and_oversize(client):
    assert client.post('/api/load',data={'demo':'true'},headers={'X-Local-Token':'wrong'}).status_code==403
    assert client.get('/',headers={'Host':'untrusted.example'}).status_code==403
    assert client.post('/api/load',data={'model':(io.BytesIO(b'x'*(5*1024*1024+1)),'big.mdl')}).status_code==413

def test_local_plotly(client):
    r=client.get('/static/plotly-local.js')
    assert r.status_code==200
    assert b'plotly.js' in r.data[:500]
