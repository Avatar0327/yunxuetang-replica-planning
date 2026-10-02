from pathlib import Path
import json,hashlib,subprocess,tarfile,datetime,re
repo=Path.cwd();tech=Path('/Users/peng/Library/Mobile Documents/com~apple~CloudDocs/Agent复刻项目/云学堂复刻规划/03_技术方案');planning=tech.parent;dest=tech/'预研证据/Native性能整改_v8.3_20260923/最终交付';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def check(n,b):
 checks.append({'name':n,'pass':bool(b)})
 if not b:raise AssertionError(n)
f=json.loads((tech/'核验记录/输入文件指纹.json').read_text());expected={x['path']:x['sha256'] for x in f['files']};actual={str(p.relative_to(planning)):sha(p) for p in planning.rglob('*') if p.is_file() and p.name!='.DS_Store' and tech not in p.parents};check('65 v8.3 inputs unchanged',len(actual)==65 and actual==expected)
m=json.loads((dest/'交付证据指纹.json').read_text());check('report digest',sha(tech/m['report']['path'])==m['report']['sha256'])
for x in m['artifacts']:check('outer digest '+x['path'],sha(dest/x['path'])==x['sha256'] and (dest/x['path']).stat().st_size==x['bytes'])
check('member hashes read back by packager',m['raw_files_verified']==json.loads((dest/'原始证据文件指纹.json').read_text())['count']>0)
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();check('frozen delivered source',head==m['source_commit']=='817256bf1e1fc722aaa5f0c21878e84fe8df1306');check('clean source',not subprocess.check_output(['git','status','--porcelain'],text=True).strip())
check('application unchanged since final qualified candidate',not subprocess.check_output(['git','diff','dfa6341',head,'--','src','sql','web','scripts/benchmark.ts','scripts/benchmark-truth.ts'],text=True))
archive=next(dest/a['path'] for a in m['artifacts'] if a['path'].startswith('Native整改源码'))
with tarfile.open(archive,'r:gz') as t:
 blobs={x.name:t.extractfile(x).read() for x in t if x.isfile()};names=subprocess.check_output(['git','ls-tree','-r','--name-only','-z',head],text=True).split('\0')[:-1];check('source archive exact tracked file set',set(blobs)==set(names))
 for name,data in blobs.items():check('source exact '+name,data==subprocess.check_output(['git','show',head+':'+name]))
summary=json.loads((repo/'evidence/raw/native-remediation-final-summary/windows.json').read_text());check('6 complete windows all NoGo',len(summary['windows'])==6 and len(summary['scenarios'])==24 and all(not x['gate'] and x['auditIssues']==0 and x['seconds']>=600 for x in summary['windows']))
for i in [1,2]:
 p=repo/f'evidence/raw/native-remediation-candidate{i}';r=json.loads((p/('regression-summary-verified' if i==1 else 'regression-summary')/'regression-summary.json').read_text());check('candidate regression '+str(i),r['complete'] and r['observations']==456 and len(r['phases'])==10 and all(x['count']==16 and x['allChecks'] for x in r['phases']) and all(x['allChecks'] for x in r['timeline']))
c=json.loads((repo/'evidence/raw/native-remediation-cost-drivers/independent-results-audit.json').read_text());check('cost640/32/16 audited',c['trials']==640 and len(c['cells'])==32 and len(c['fullAudits'])==16 and c['allFullAuditsComplete'] and c['failures']==0 and not c['issues'])
r=(tech/'15_Native权限性能整改报告.md').read_text();check('discipline retained',all(x in r for x in ['G-01','G-02','G-04','G-05','G-06','D-42 由我方定义','T-10 由我方定义','AC-N-03','AC-E-01','AC-E-02','AC-E-03','AC-E-22','AC-N-11','AC-E-25','固定表单','单级固定审批','课程无审核','北森','站内通知','人工维护','B4-16','B4-14','265～417','267～421','273～433','待用户实际评审签署，未代签','折抵：0']))
result={'at':datetime.datetime.now().astimezone().isoformat(),'delivery_verified':True,'permission_gate':'NO_GO','checks':checks,'scope':'Fresh artifact integrity, exact source readback, inputs and measured gate records; no new runtime test or Go inference.'}
(dest/'最终核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'delivery_verified':True,'checks':len(checks),'source':head,'permission_gate':'NO_GO'},ensure_ascii=False))
