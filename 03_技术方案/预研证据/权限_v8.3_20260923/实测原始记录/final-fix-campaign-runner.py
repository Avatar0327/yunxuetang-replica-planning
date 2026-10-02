from pathlib import Path
import subprocess,os,json,time
root=Path('/Users/peng/Agent本地开发/云学堂权限预研');cwd=root/'output/final-fix-campaign';raw=cwd/'evidence/raw';env=os.environ.copy();env['PATH']='/opt/homebrew/opt/node@24/bin:'+env['PATH'];env['FINAL_FIX_SOURCE']='cb72484ed8e7547146920fd4312dd24f8c9e2402'
results=[]
def run(name,args,extra=None):
 e=env.copy();e.update(extra or {});start=time.time()
 with (raw/(name+'.txt')).open('w') as f:r=subprocess.run(args,cwd=cwd,env=e,stdout=f,stderr=subprocess.STDOUT)
 results.append(dict(name=name,command=args,cwd=str(cwd),environment={k:v for k,v in e.items() if k in ['FINAL_FIX_SOURCE','TASK3_OBSERVATIONS','SEMANTIC_EVIDENCE','RACE_EVIDENCE','HTTP_OBSERVATIONS','TASK5_TIMELINE','CANDIDATE']},exit=r.returncode,seconds=time.time()-start));(raw/'commands.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(name,r.returncode,flush=True)
 if r.returncode:raise SystemExit(r.returncode)
run('core-seed',['npm','run','seed'])
run('core',['node','--import','tsx','--test','--test-concurrency=1','test/semantic.test.ts','test/cache.test.ts','test/integration.test.ts','test/races.test.ts','test/review-regressions.test.ts','test/module-boundaries.test.ts'],{'SEMANTIC_EVIDENCE':'evidence/raw/core-semantic.jsonl','RACE_EVIDENCE':'evidence/raw/core-races.jsonl'})
for candidate in ['native','casbin']:
 run('http-'+candidate+'-seed',['npm','run','seed'])
 apiEnv=env.copy();apiEnv.update(CANDIDATE=candidate,PORT='4311')
 with (raw/('http-'+candidate+'-api.txt')).open('w') as f:
  child=subprocess.Popen(['node','--import','tsx','src/bootstrap.ts'],cwd=cwd,env=apiEnv,stdout=f,stderr=subprocess.STDOUT)
  try:
   for i in range(200):
    if '"ready":true' in (raw/('http-'+candidate+'-api.txt')).read_text():break
    if child.poll() is not None:raise RuntimeError('API failed')
    time.sleep(.03)
   run('http-'+candidate,['node','--import','tsx','--test','test/http.test.ts'],{'CANDIDATE':candidate,'HTTP_OBSERVATIONS':'evidence/raw/http-'+candidate+'.jsonl'})
  finally:child.terminate();child.wait(timeout=10)
for domain in ['task3','task4','task5']:
 run(domain+'-seed',['npm','run','seed'])
 run(domain,['npm','run','test:'+domain],{'TASK3_OBSERVATIONS':'evidence/raw/'+domain+'.jsonl','HTTP_OBSERVATIONS':'evidence/raw/'+domain+'-http.jsonl','TASK5_TIMELINE':'evidence/raw/task5-commit-timeline.jsonl'})
