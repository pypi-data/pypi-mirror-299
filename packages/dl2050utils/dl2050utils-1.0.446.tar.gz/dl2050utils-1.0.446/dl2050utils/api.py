# ####################################################################################################
# api.py
#
# API server, API_Worker server
#
# Responses are allwways JSON, both for GET/POST of the form {status_code:<int>, message:<str>, result:<dict>}
#
# Example API:
#   api = API_Server(cfg)
#   api.run()
#
# cfg = {
#   'apiserver': {'servive':<service>, 'wkey':<wkey>}
#   'gcloud': {'gs_key':<gs_key_struct>}}
#   }
#
# Example API_Client:
#   api_cli = API_Client(key=key, url='http://ju:9000')
#   res = api_cli.req({'url':'www.xxx.com'})
#   req_id = res['result']['req_id']
#   api_cli.check(req_id)
#
# Example Worker:
#
#   w = API_Worker('kardio', wkey, 'http://ju:9000')
#   def proc(task, start_cb, done_cb, error_cb):
#       start_cb(task['id'], 10)
#       time.sleep(10)
#       done_cb(task['id'], {'ml':42}, used_credits=1.)
#       return 0
#   w.run(proc)
#
# ####################################################################################################
import time
import datetime
import secrets
import string
import sqlite3
import uvicorn
import json
import uuid
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from dl2050utils.core import oget, now, date_to_srt, str_to_date_2
from dl2050utils.env import config_load
from dl2050utils.log import AppLog
from dl2050utils.sqlite import Sqlite
from dl2050utils.restutils import get_param, sync_request
from dl2050utils.fs import GS

TASK_STATUS = ['REQUESTED', 'DISPATCHED', 'START', 'DONE', 'ERROR']

# ####################################################################################################
# REST
# ####################################################################################################

def raise_error(status_code=500, msg='', LOG=None):
    """Generic function to raise HTTPException and optionally log the error (used in the API)"""
    if LOG is not None: LOG(4, 0, label='HTTPException', msg=msg)
    raise HTTPException(status_code=status_code, detail=msg)

def rest_ok(result=None, message=''):
    return JSONResponse(status_code=200, content={'status':200, 'message':message, 'result':result})

async def http_exception(request, exc):
    return JSONResponse(status_code=exc.status_code, content={'status':exc.status_code, 'message': exc.detail or "HTTP error"})
    # 'error_code': exc.__class__.__name__

async def server_error_exception(request, exc):
    return JSONResponse(status_code=500, content={'status': 500, 'message': "Internal server error",})

# ####################################################################################################
# Utility functions
# ####################################################################################################

def db_create(db):
    Q1 = '''
        CREATE TABLE IF NOT EXISTS api_keys (
            key CHAR(256) PRIMARY KEY,
            email VARCHAR(128),
            name VARCHAR(128),
            created_at DATETIME,
            reset_calls_at DATETIME,
            active BOOLEAN,
            rate_limit INTEGER,
            calls INTEGER DEFAULT 0,
            calls_total INTEGER DEFAULT 0,
            credits REAL DEFAULT 0 -- current credits total
        )
    '''
    Q2 = '''
        CREATE TABLE IF NOT EXISTS api_tasks (
            id INTEGER PRIMARY KEY,
            created_at DATETIME,
            key CHAR(256),
            status CHAR(32),
            payload TEXT,
            result TEXT,
            eta DATETIME,
            credits REAL DEFAULT 0 -- credits used by task
        );
    '''
    db.execute(Q1)
    db.execute(Q2)

def get_new_key(n=256): return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(n))
def get_reset_time(): return date_to_srt(now()+datetime.timedelta(hours=1))
def to_json(o): return None if o is None else json.dumps(o)
def from_json(s): return None if s is None else json.loads(s)

# ####################################################################################################
# Transactions
# ####################################################################################################

def grab_task(db):
    """Gets the oldest task with status REQUESTED and updates the status to PROCESSING with atomiticity"""
    tbl = 'api_tasks'
    d = None
    try:
        # Begin a transaction to lock the row and ensure atomicity
        db.conn.execute('BEGIN IMMEDIATE')
        cursor = db.conn.cursor()
        Q = f"SELECT * FROM {tbl} WHERE status == 'REQUESTED' ORDER BY id LIMIT 1"
        cursor.execute(Q)
        task = cursor.fetchone()
        if not task:
            db.conn.rollback()
            return None
        # Fetch the column names and convert the row to a dictionary
        column_names = [description[0] for description in cursor.description]
        d = dict(zip(column_names, task))
        cursor.execute(f"UPDATE {tbl} SET status = ? WHERE id = ?", ('PROCESSING', d['id']))
        db.conn.commit()
        return d
    except sqlite3.DatabaseError as exc:
        print(f'grab_task EXCEPTION: {exc}')
        db.conn.rollback()
    
def update_credits(db, key, value):
    """DB transaction to update key credits value"""
    try:
        db.conn.execute('BEGIN IMMEDIATE')
        cursor = db.conn.cursor()
        cursor.execute("""UPDATE api_keys SET credits = credits + ? WHERE key = ?""", (value, key))
        db.conn.commit()
    except Exception as exc:
        print(f'update_credits EXCEPTION: {exc}')
        db.conn.rollback()
        raise exc

# ####################################################################################################
# API_Server
# ####################################################################################################

class API_Server:
    def __init__(self, service, cfg=None):
        if service is None: raise('service must be defined')
        if cfg is not None: cfg = config_load('kardio')
        self.port = 9000
        self.db = Sqlite(f'/data/{service}/apiserver/api-db')
        self.wkey = oget(cfg,['apiserver','wkey'])
        if self.wkey is None: raise('Worker key not defined')
        self.gs = GS(service) if oget(cfg,['gcloud','gs_key']) is not None else None
        self.LOG = AppLog(cfg, service=f'{service}-apis')
        self.LOG(2, 0, label='READY')
    
    # ####################################################################################################
    # Admin
    # ####################################################################################################

    def new_key(self, email, rate_limit=100):
        key = get_new_key()
        self.db.insert('api_keys',{'key':key, 'email':email, 'active':True, 'rate_limit':rate_limit,
                                   'reset_calls_at':get_reset_time()})
        return key
    def revoke_key(self, key): return self.select_and_update('api_keys', 'key', key, {'active':False})
    def get_key(self, key): return self.db.select_one('api_keys', 'key', key)
    def get_keys(self): return self.db.select('api_keys')
    def get_tasks(self): return self.db.select('api_tasks')
    def get_task(self, task_id): return self.db.select_one('api_tasks', 'id', task_id)
    def remove_all_tasks(self): self.db.delete_all('api_tasks')
    def add_credits(self, key, value): update_credits(self.db, key, value)
    def remove_credits(self, key, value): update_credits(self.db, key, -value)
    def db_create(self): db_create(self.db)
    
    # ####################################################################################################
    # Access control
    # ####################################################################################################

    def check_access(self, key):
        d = self.db.select_one('api_keys', 'key', key)
        if d is None: raise_error(403, 'Invalid API key', self.LOG)
        if d['active']==0: raise_error(403, 'Inactive API key', self.LOG)
        if d['calls'] > d['rate_limit']: raise_error(403, 'Rate limit exceded', self.LOG)
        if d['credits'] < 0: raise_error(403, 'Out of credits', self.LOG)
        for c in ['calls','calls_total']: d[c] += 1
        ts1,ts2 = now(),str_to_date_2(d['reset_calls_at'])
        # Update time window limit if needed
        if ts1 > ts2: d['calls'],d['reset_calls_at'] = 0,ts2+datetime.timedelta(hours=1)
        self.db.update( 'api_keys', 'key', d)
        return d
    
    def check_worker_access(self, key):
        if len(key)>256: raise_error(self.LOG, err_msg='Invalid Worker key', status_code=400)
        if key!=self.wkey: raise_error(self.LOG, err_msg='Unauthorized Worker key', status_code=403)
    
    def reset_rate_limit(self, key):
        return self.db.select_and_update('api_keys', 'key', key, {'calls':0, 'reset_calls_at':now()+datetime.timedelta(hours=1)})
    
    # ####################################################################################################
    # API Entrypoints
    # ####################################################################################################
    
    async def req(self, request):
        data = await request.json()
        key = get_param(request, 'key', str, max_length=256, data=data) # POST
        payload = get_param(request, 'payload', dict, max_length=256, data=data)
        self.check_access(key)
        task = {'created_at':now(), 'key':key, 'status':'REQUESTED', 'payload':to_json(payload)}
        req_id = self.db.insert('api_tasks', task)
        self.LOG(2, 0, label='API', label2='/apiserver/req', msg=f"req_id={req_id}")
        return rest_ok(result={'req_id':req_id})
    
    async def check(self, request):
        key = get_param(request, 'key', str, max_length=256)
        req_id = get_param(request, 'req_id', int)
        self.check_access(key)
        task = self.db.select_one('api_tasks', 'id', req_id)
        res = None
        if task is not None:
            res = {'status':task['status']}
            if res['status']!='DONE':
                res['eta'] = task['eta']
            else:
                res['result'],res['credits'] = from_json(task['result']),task['credits']
        return rest_ok(result=res)
    
    async def get_upload_url(self, request):
        key = get_param(request, 'key', str, max_length=256)
        self.check_access(key)
        if self.gs is None: raise_error(self.LOG, err_msg='Upload links not available', status_code=400)
        upload_url,download_url = self.gs.urls('kardio', str(uuid.uuid4()))
        return rest_ok(result={'upload_url':upload_url, 'download_url':download_url})
    
    # ####################################################################################################
    # Worker Entrypoints
    # ####################################################################################################
    
    async def grab(self, request):
        data = await request.json()
        key = get_param(request, 'key', str, max_length=256, data=data)
        self.check_worker_access(key)
        task = grab_task(self.db)
        if task is not None: self.db.select_and_update('api_tasks', 'id', task['id'], {'status':'DISPATCHED'})
        if task is not None: self.LOG(2, 0, label='API', label2='/worker/grab', msg=f"id={task['id']}")
        return rest_ok(result=task)

    async def start(self, request):
        data = await request.json()
        key = get_param(request, 'key', str, max_length=256, data=data)
        task_id = get_param(request, 'id', int, data=data)
        eta = get_param(request, 'eta', int, data=data)
        self.check_worker_access(key)
        self.db.select_and_update('api_tasks', 'id', task_id, {'status':'START', 'eta':eta})
        return rest_ok()

    async def done(self, request):
        data = await request.json()
        key = get_param(request, 'key', str, max_length=256, data=data)
        task_id = get_param(request, 'id', int, data=data)
        result = to_json(get_param(request, 'result', dict, data=data))
        used_credits = get_param(request, 'credits', float, data=data)
        self.check_worker_access(key)
        self.db.select_and_update('api_tasks', 'id', task_id, {'status':'DONE', 'result':result, 'credits':used_credits, 'eta':None})
        task = self.get_task(task_id)
        self.remove_credits(task['key'], used_credits)
        return rest_ok()

    async def error(self, request):
        data = await request.json()
        key = get_param(request, 'key', str, max_length=256, data=data)
        task_id = get_param(request, 'id', int, max_length=256, data=data)
        self.check_worker_access(key)
        self.db.select_and_update('api_tasks', 'id', task_id, {'status':'ERROR', 'eta':None})
        return rest_ok()

    # ####################################################################################################
    # Run
    # ####################################################################################################
    
    def run(self, port=None):
        port = port or self.port
        self.LOG(2, 0, label='RUN', msg=f'Listening in port {port}')
        routes = [
            Route('/apiserver/req', endpoint=self.req, methods=['POST']),
            Route('/apiserver/check', endpoint=self.check, methods=['GET']),
            Route('/apiserver/get_upload_url', endpoint=self.get_upload_url, methods=['GET']),
            Route('/worker/grab', endpoint=self.grab, methods=['POST']),
            Route('/worker/start', endpoint=self.start, methods=['POST']),
            Route('/worker/done', endpoint=self.done, methods=['POST']),
            Route('/worker/error', endpoint=self.error, methods=['POST']),
        ]
        exception_handlers = {
            HTTPException: http_exception,
            Exception: server_error_exception,
        }
        app = Starlette(
            debug=True,
            routes=routes,
            exception_handlers=exception_handlers,
            # middleware=self.middleware,
        )
        uvicorn.run(app, port=port, host='0.0.0.0', log_level='critical')

# ####################################################################################################
# API_Client
# ####################################################################################################

class API_Client:
    def __init__(self, key, url): self.key,self.url = key,url
    def do_request(self, route, payload):
        method = 'GET' if route=='apiserver/check' else 'POST'
        return sync_request(f'{self.url}{route}', method=method, payload=payload)
    def check(self, req_id): return self.do_request('/apiserver/check', {'key':self.key, 'req_id':req_id})
    def req(self, payload): return self.do_request('/apiserver/req',  {'key':self.key, 'payload':payload})

# ####################################################################################################
# API_Worker
# ####################################################################################################

class API_Worker:

    def __init__(self, service, cfg=None, url=None, LOG=None):
        if service is None: raise('service must be defined')
        if cfg is not None: cfg = config_load('kardio')
        self.wkey = oget(cfg,['apiserver','wkey'])
        if self.wkey is None: raise('worker key not defined')
        self.url = url or 'http://localhost:9000'
        self.LOG = AppLog(cfg, service=f'{service}-ws')
        self.LOG(2, 0, label='READY', label2='STARTUP', msg=f'API Server at {self.url}')

    def request(self, path, payload):
        res = sync_request(f'{self.url}/{path}', method='POST', payload=payload, LOG=self.LOG)
        if oget(res,['status']!=200):
            self.LOG(4, 0, label='API_Worker', label2=path)
            return None
        return res

    def grab(self):
        res = self.request('worker/grab', {'key':self.wkey})
        return oget(res,['result'])

    def start(self, task_id, eta):
        return self.request('worker/start', {'key':self.wkey, 'id':task_id, 'eta':eta})

    def done(self, task_id, result, used_credits=0.):
        return self.request('worker/done', {'key':self.wkey, 'id':task_id, 'result':result, 'credits':used_credits})

    def error(self, task_id):
        return self.request('worker/error', {'key':self.wkey, 'id':task_id})
    
    def run(self, cb):
        try:
            while True:
                task = self.grab()
                if task is None:
                    time.sleep(1)
                    continue
                try:
                    if not cb(task, self.start, self.done, self.error):
                        self.LOG(2, 0, label='API_Worker', label2='DONE', msg=f"{task['id']}")
                    else:
                        self.LOG(3, 0, label='API_Worker', label2='ABORTED', msg=f"{task['id']}")
                except Exception as exc:
                    self.error(task['id'])
                    self.LOG(4, 0, label='API_Worker', label2='Callback EXCEPTION', msg=f"{task['id']}, exc={exc}")
        except KeyboardInterrupt:
            self.LOG(2, 0, label='API_Worker', label2='SHUTDOWN')
        except Exception as exc:
            self.error(task['id'])
            self.LOG(4, 0, label='API_Worker', label2='Server EXCEPTION', msg=f'exc={exc}')
