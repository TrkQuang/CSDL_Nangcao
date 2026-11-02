"""Run Cypher only in a new disposable official Neo4j container."""
from pathlib import Path
import subprocess, os, secrets, socket, json, datetime, urllib.request, urllib.error, base64, time
R=Path(r'C:\Users\Quynh\Documents\csdlnc\CSDL_Nangcao')
OUT=R/'docs/review_evidence'/('neo4j_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
OUT.mkdir(parents=True)
name='detai17-validation-'+secrets.token_hex(5)
password=secrets.token_urlsafe(30)
env=os.environ.copy();env['NEO4J_AUTH']='neo4j/'+password
with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
def command(args):
 p=subprocess.run(args,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=600)
 if p.returncode:raise RuntimeError(p.stderr.replace(password,'[REDACTED]'))
 return p.stdout
url=f'http://127.0.0.1:{port}/db/neo4j/tx/commit'
def query(statements):
 data=json.dumps({'statements':[{'statement':s} for s in statements]}).encode()
 req=urllib.request.Request(url,data,{'Content-Type':'application/json','Authorization':'Basic '+base64.b64encode(('neo4j:'+password).encode()).decode()})
 with urllib.request.urlopen(req,timeout=30) as response:result=json.load(response)
 if result['errors']:raise RuntimeError(json.dumps(result['errors']))
 return result
started=False
try:
 command(['docker','pull','neo4j:5.18-community'])
 command(['docker','run','-d','--name',name,'-p',f'127.0.0.1:{port}:7474','-e','NEO4J_AUTH','-e','NEO4J_server_memory_heap_initial__size=256m','-e','NEO4J_server_memory_heap_max__size=512m','-e','NEO4J_server_memory_pagecache_size=256m','neo4j:5.18-community']);started=True
 deadline=time.monotonic()+180
 while True:
  try:query(['RETURN 1']);break
  except (urllib.error.URLError,TimeoutError,ConnectionError):
   if time.monotonic()>deadline:raise
   time.sleep(2)
 def statements(path):
  text='\n'.join(line for line in path.read_text(encoding='utf-8-sig').splitlines() if not line.strip().startswith('//'))
  return [s.strip() for s in text.split(';') if s.strip()]
 # Import starts with DETACH DELETE; container above is fresh and exclusively owned.
 for stmt in statements(R/'neo4j/import/import_nodes_edges.cypher'):query([stmt])
 counts=query(['MATCH (u:User) RETURN count(u)','MATCH ()-[r:FRIEND]->() RETURN count(r)','MATCH ()-[r:FOLLOWS]->() RETURN count(r)'])
 assert [x['data'][0]['row'][0] for x in counts['results']]==[6,6,4]
 results={}
 for case in ['friends_of_friends','shortest_path','cycle_detection','recommendation']:
  result=query(statements(R/f'neo4j/cypher/{case}.cypher'))
  (OUT/(case+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
  rows=[r['row'] for r in result['results'][0]['data']]
  if case=='friends_of_friends':assert [r[0] for r in rows]==[4,5],rows
  if case=='shortest_path':assert rows==[[[1,3,5],['An','Chi','Em'],2]],rows
  if case=='cycle_detection':assert [r[0] for r in rows]==[[1,2,3,1],[2,3,5,4,2],[1,2,4,5,3,1]],rows
  if case=='recommendation':assert [(r[0],r[2]) for r in rows]==[(4,1),(5,1)],rows
  results[case]='passed';print('PASS',case,flush=True)
 version=query(['CALL dbms.components() YIELD name, versions, edition RETURN name, versions, edition'])
 (OUT/'summary.json').write_text(json.dumps({'status':'passed','tests':results,'counts':[6,6,4],'version':version,'image':'neo4j:5.18-community','isolation':'new disposable container; loopback HTTP only'},ensure_ascii=False,indent=2),encoding='utf-8')
 print('EVIDENCE',OUT,flush=True)
finally:
 if started:command(['docker','rm','-f','-v',name])
