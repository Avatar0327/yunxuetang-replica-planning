"""Controller synthetic browser fixture operations; no production credentials/data."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,subprocess,urllib.request
ROOT=Path(__file__).resolve().parents[2]
label,mode=sys.argv[1:3]
target=ROOT/'output/playwright'/label
if target.exists():raise SystemExit('Refuse to overwrite existing control evidence')
now=lambda:datetime.now(timezone.utc).isoformat()
record={'startedAt':now(),'mode':mode,'synthetic':True}
if mode=='appointment':
 person,project,active=sys.argv[3:6]
 assert person in ['L','M'] and project in ['P','Q'] and active in ['true','false']
 body={'personId':person,'projectId':project,'active':active=='true'}
 url='http://127.0.0.1:4311/appointments'
 r=urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(body).encode(),headers={'Authorization':'Bearer spike-Z','Content-Type':'application/json'},method='POST'))
 record.update(request={'method':'POST','url':url,'body':body},status=r.status,response=json.loads(r.read()))
 assert r.status==200
elif mode=='independent-role':
 member={'id':'browser-independent-L','tenantId':'T1','personId':'L','roleId':'role-9','level':3,'active':True,'provenance':'system_origin','policies':[{'nodeId':'personal-learning','navigation':True,'actions':['report.personal-learning.view'],'scope':{'kind':'self'},'rawFields':[],'delegableActions':[]}]}
 sql="INSERT INTO authz.membership(tenant_id,id,person_id,role_id,data) VALUES('T1','browser-independent-L','L','role-9','"+json.dumps(member).replace("'","''")+"');"
 cmd=['docker','--context','colima-yxt-permission','exec','-i','yxt-pg','psql','-U','spike','-d','permission_spike','-X','-v','ON_ERROR_STOP=1']
 r=subprocess.run(cmd,input=sql,text=True,capture_output=True)
 record.update(fixture='Explicit system-origin synthetic membership, not a test of role-grant UI',sql=sql,exitCode=r.returncode,stdout=r.stdout,stderr=r.stderr)
 if r.returncode:raise RuntimeError(r.stderr)
else:raise SystemExit('unknown fixture mode')
record['finishedAt']=now();target.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'file':str(target.relative_to(ROOT)),'status':record.get('status',record.get('exitCode'))},ensure_ascii=False))
