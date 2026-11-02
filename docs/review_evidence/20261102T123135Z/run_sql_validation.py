"""Run repository SQL in a private SCRAM cluster; never connect to existing DBs."""
from pathlib import Path
import subprocess, tempfile, socket, secrets, os, json, datetime, time
R=Path(r'C:\Users\Quynh\Documents\csdlnc\CSDL_Nangcao'); PG=Path(r'C:\Program Files\PostgreSQL\16\bin')
OUT=R/'docs/review_evidence'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
OUT.mkdir(parents=True,exist_ok=False)
results=[];env=os.environ.copy();env.update(PGCLIENTENCODING='UTF8',PGCONNECT_TIMEOUT='10',PGPASSWORD=secrets.token_urlsafe(32),PGUSER='report_validator',PGDATABASE='postgres',PGHOST='127.0.0.1')
with socket.socket() as s:s.bind(('127.0.0.1',0));env['PGPORT']=str(s.getsockname()[1])
def run(args,log,input=None,strict=True):
 r=subprocess.run([str(x) for x in args],input=input,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=600,creationflags=subprocess.CREATE_NO_WINDOW)
 (OUT/log).write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
 if strict and r.returncode:raise RuntimeError(f'{log}: exit {r.returncode}')
 return r
def sql(text,log,strict=True):return run([PG/'psql.exe','-X','-w','-v','ON_ERROR_STOP=1','-qAt'],log,text,strict)
def file(rel,log,strict=True,extra=()):return run([PG/'psql.exe','-X','-w','-v','ON_ERROR_STOP=1',*extra,'-f',R/rel],log,strict=strict)
def test(name,fn):
 try:fn();results.append({'name':name,'status':'passed'});print('PASS',name,flush=True)
 except Exception as e:results.append({'name':name,'status':'failed','error':str(e)});print('FAIL',name,str(e),flush=True)
def seed():file('database/seed_test.sql','seed_latest.txt')
with tempfile.TemporaryDirectory(prefix='detai17_report_validation_') as tmp:
 tmp=Path(tmp);cluster=tmp/'cluster';pw=tmp/'password';pw.write_text(env['PGPASSWORD'],encoding='utf-8');started=False
 try:
  run([PG/'initdb.exe','-D',cluster,'-U',env['PGUSER'],'--auth=scram-sha-256',f'--pwfile={pw}','--encoding=UTF8','--locale=C'],'cluster_init.txt');pw.unlink()
  with (OUT/'cluster_start.txt').open('w',encoding='utf-8') as handle:
   subprocess.run([str(PG/'pg_ctl.exe'),'-D',str(cluster),'-l',str(tmp/'server.log'),'-o',f"-h 127.0.0.1 -p {env['PGPORT']}",'-w','start'],env=env,stdout=handle,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW,timeout=60,check=True)
  started=True
  for rel in ['database/schema.sql','database/constraints.sql','database/seed_test.sql']+[f'sql_advanced/q{i:02}_{suffix}.sql' for i,suffix in [(9,'trigger'),(10,'procedure'),(11,'function'),(12,'dynamic')]]:
   file(rel,Path(rel).stem+'.txt')
  meta=sql("SELECT json_build_object('version',version(),'host',inet_server_addr(),'port',inet_server_port(),'users',(SELECT count(*) FROM users));",'environment_query.txt').stdout.strip()
  (OUT/'environment.json').write_text(meta,encoding='utf-8')
  test('Task 3 regression Q9-Q12',lambda:file('sql_advanced/validate_task3.sql','task3.txt'))
  test('Advanced SELECT Q1-Q8',lambda:file('sql_advanced/q01_q08_select.sql','advanced_queries.txt'))
  test('FD source checks',lambda:file('normalization/fd_check.sql','fd_checks.txt'))
  test('MVD 4NF demonstration',lambda:file('normalization/mvd_4nf.sql','mvd_4nf.txt'))
  for model in ['adjacency_list','path_enumeration','nested_set','closure_table']:
   seed()
   test(model+' CRUD definitions',lambda m=model:file(f'tree_models/{m}/crud.sql',m+'_crud.txt'))
   test(model+' Q1-Q10',lambda m=model:file(f'tree_models/{m}/queries_q1_q10.sql',m+'_queries.txt'))
   test(model+' tree invariants',lambda m=model:file('benchmark/validate_dataset.sql',m+'_invariants.txt'))
  seed()
  for query in ['friends_of_friends','shortest_path','cycle_detection','recommendation']:
   test('Graph '+query,lambda q=query:file('recursive_sql/'+q+'.sql',q+'.txt'))
  test('Graph expected shortest path and recommendations',lambda:sql("""DO $$ BEGIN
  IF NOT EXISTS(SELECT 1 FROM friend_edge WHERE a=1 AND b=3) OR NOT EXISTS(SELECT 1 FROM friend_edge WHERE a=3 AND b=5) OR EXISTS(SELECT 1 FROM friend_edge WHERE a=1 AND b=5) THEN RAISE EXCEPTION 'shortest path seed mismatch'; END IF;
  IF (SELECT array_agg(b ORDER BY b) FROM (SELECT DISTINCT second.b FROM friend_edge first JOIN friend_edge second ON first.b=second.a WHERE first.a=1 AND second.b<>1 AND second.b NOT IN(SELECT b FROM friend_edge WHERE a=1)) x)<>ARRAY[4,5] THEN RAISE EXCEPTION 'recommendation seed mismatch'; END IF;
  END $$;""",'graph_assertions.txt'))
  seed();test('T1 transaction',lambda:file('transactions/t1_success.sql','t1.txt'))
  seed()
  # T2 deliberately raises two CHECK errors; psql must continue to rollback/savepoint.
  def t2():
   r=run([PG/'psql.exe','-X','-w','-v','ON_ERROR_STOP=0','-f',R/'transactions/t2_rollback_savepoint.sql'],'t2.txt');assert r.stderr.count('ERROR:')==2,r.stderr
   sql("DO $$ BEGIN IF NOT EXISTS(SELECT 1 FROM post WHERE post_id=100) THEN RAISE EXCEPTION 'savepoint post missing'; END IF; IF EXISTS(SELECT 1 FROM friendship WHERE user_a>=user_b) THEN RAISE EXCEPTION 'invalid friendship persisted'; END IF; END $$;",'t2_assertions.txt')
  test('T2 expected errors and SAVEPOINT persistence',t2)
  seed()
  def deadlock():
   # Interactive pipes synchronize after each session acquires its first lock.
   cmd=[str(PG/'psql.exe'),'-X','-w','-qAt','-v','ON_ERROR_STOP=1','-v','VERBOSITY=verbose']
   a=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',env=env)
   b=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',env=env)
   for proc,node in [(a,1),(b,2)]:
    proc.stdin.write(f"BEGIN; SET LOCAL statement_timeout='15s'; SELECT user_id FROM users WHERE user_id={node} FOR UPDATE;\n");proc.stdin.flush();assert proc.stdout.readline().strip()==str(node)
   a.stdin.write('SELECT user_id FROM users WHERE user_id=2 FOR UPDATE; COMMIT;\n');a.stdin.flush()
   b.stdin.write('SELECT user_id FROM users WHERE user_id=1 FOR UPDATE; COMMIT;\n');b.stdin.flush()
   oa,ea=a.communicate(timeout=30);ob,eb=b.communicate(timeout=30)
   (OUT/'deadlock.txt').write_text('A\n'+oa+ea+'\nB\n'+ob+eb,encoding='utf-8');assert '40P01' in ea+eb;assert sorted([a.returncode,b.returncode])==[0,3]
  test('T3 synchronized deadlock SQLSTATE 40P01',deadlock)
  for clients in [5,10,20]:
   seed()
   test(f'pgbench {clients} clients',lambda c=clients:run([PG/'pgbench.exe','-n','-c',c,'-j','2','-t','100','-f',R/'transactions/pgbench/add_friend.sql'],'pgbench_'+str(c)+'.txt'))
   test(f'pgbench {clients} counters',lambda c=clients:sql("DO $$ BEGIN IF EXISTS(SELECT 1 FROM users WHERE friend_count<>(SELECT count(*) FROM friend_edge WHERE a=users.user_id)) THEN RAISE EXCEPTION 'counter mismatch'; END IF; END $$;",'pgbench_'+str(c)+'_assertions.txt'))
  (OUT/'summary.json').write_text(json.dumps({'results':results,'cluster':'private SCRAM loopback; no existing database touched','neo4j':'blocked: Docker engine not running','python_benchmark':'blocked: psycopg2/matplotlib missing'},ensure_ascii=False,indent=2),encoding='utf-8')
 finally:
  if started:run([PG/'pg_ctl.exe','-D',cluster,'-m','fast','-w','stop'],'cluster_stop.txt')
print('EVIDENCE',OUT,flush=True)
print('RESULT',sum(x['status']=='passed' for x in results),'passed;',sum(x['status']=='failed' for x in results),'failed',flush=True)
