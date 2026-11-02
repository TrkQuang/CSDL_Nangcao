"""Assert PostgreSQL isolation and run embedded example in a private cluster."""
from pathlib import Path
import tempfile, subprocess, secrets, socket, os, json, datetime, importlib.util, io, contextlib
import psycopg2
R=Path(r'C:\Users\Quynh\Documents\csdlnc\CSDL_Nangcao'); PG=Path(r'C:\Program Files\PostgreSQL\16\bin')
OUT=R/'docs/review_evidence'/('isolation_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')); OUT.mkdir(parents=True)
env=os.environ.copy();env.update(PGUSER='isolated_validator',PGPASSWORD=secrets.token_urlsafe(32),PGHOST='127.0.0.1',PGDATABASE='postgres',PGCLIENTENCODING='UTF8')
with socket.socket() as s:s.bind(('127.0.0.1',0));env['PGPORT']=str(s.getsockname()[1])
def cmd(args,log):
 with (OUT/log).open('a',encoding='utf-8') as f:
  p=subprocess.run([str(x) for x in args],env=env,stdout=f,stderr=subprocess.STDOUT,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW,timeout=120)
 assert p.returncode==0,log
with tempfile.TemporaryDirectory(prefix='detai17_isolation_') as tmp:
 tmp=Path(tmp);pw=tmp/'password';pw.write_text(env['PGPASSWORD'],encoding='utf-8');started=False
 try:
  cmd([PG/'initdb.exe','-D',tmp/'cluster','-U',env['PGUSER'],'--auth=scram-sha-256',f'--pwfile={pw}','--encoding=UTF8','--locale=C'],'setup.txt');pw.unlink()
  cmd([PG/'pg_ctl.exe','-D',tmp/'cluster','-l',tmp/'server.txt','-o',f"-h 127.0.0.1 -p {env['PGPORT']}",'-w','start'],'setup.txt');started=True
  for file in ['database/schema.sql','database/constraints.sql','database/seed_test.sql']:
   cmd([PG/'psql.exe','-X','-w','-v','ON_ERROR_STOP=1','-f',R/file],'seed.txt')
  def connect():return psycopg2.connect(host=env['PGHOST'],port=env['PGPORT'],user=env['PGUSER'],password=env['PGPASSWORD'],dbname='postgres',options='-c statement_timeout=10000')
  a=connect();b=connect();b.autocommit=True
  def scalar(c,s):
   with c.cursor() as cur:cur.execute(s);return cur.fetchone()[0] if cur.description else None
  results={}
  for level in ['READ COMMITTED','REPEATABLE READ']:
   scalar(b,'UPDATE users SET friend_count=2 WHERE user_id=1')
   a.set_session(isolation_level=level)
   first=scalar(a,'SELECT friend_count FROM users WHERE user_id=1')
   scalar(b,'UPDATE users SET friend_count=3 WHERE user_id=1')
   second=scalar(a,'SELECT friend_count FROM users WHERE user_id=1')
   assert (first,second)==((2,3) if level=='READ COMMITTED' else (2,2))
   results[level]={'first':first,'second':second,'status':'passed'};a.rollback()
  b.autocommit=False;a.set_session(isolation_level='SERIALIZABLE');b.set_session(isolation_level='SERIALIZABLE')
  scalar(a,'SELECT SUM(friend_count) FROM users');scalar(b,'SELECT SUM(friend_count) FROM users')
  scalar(a,'UPDATE users SET friend_count=friend_count+1 WHERE user_id=1')
  scalar(b,'UPDATE users SET friend_count=friend_count+1 WHERE user_id=2');a.commit()
  try:b.commit();raise AssertionError('SSI did not abort write skew')
  except psycopg2.Error as e:
   assert e.pgcode=='40001',e.pgcode;results['SERIALIZABLE']={'status':'passed','sqlstate':e.pgcode,'error':e.pgerror};b.rollback()
  a.close();b.close()
  for key,pg in [('DB_HOST','PGHOST'),('DB_PORT','PGPORT'),('DB_USER','PGUSER'),('DB_PASS','PGPASSWORD'),('DB_NAME','PGDATABASE')]:os.environ[key]=env[pg]
  spec=importlib.util.spec_from_file_location('embedded_demo',R/'sql_advanced/embedded/psycopg2_cursor.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  output=io.StringIO()
  with contextlib.redirect_stdout(output):mod.demo_embedded_query(1)
  text=output.getvalue();assert '- ID: 2,' in text and '- ID: 3,' in text and '[LỖI' not in text
  (OUT/'embedded.txt').write_text(text,encoding='utf-8');results['embedded Python']={'status':'passed','friend_ids':[2,3]}
  (OUT/'summary.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(results,ensure_ascii=True));print('EVIDENCE',OUT)
 finally:
  if started:cmd([PG/'pg_ctl.exe','-D',tmp/'cluster','-m','fast','-w','stop'],'setup.txt')
