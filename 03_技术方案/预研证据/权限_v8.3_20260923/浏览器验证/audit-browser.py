from pathlib import Path
from datetime import datetime,timezone
import json,re,shutil,hashlib
ROOT=Path.cwd(); checks=[]; copied=[]
files={
'native':{'learner':'02-learner.txt','P-only':'05-P-only.txt','P-detail':'08-P-detail.txt','Q-denied':'10-Q-denied.txt','module-denied':'14-module-denied.txt','Q-retained':'18-Q-retained.txt','P-revoked':'21-revoked-P-denied.txt','backend-closed':'25-backend-closed.txt','combined':'44-combined-valid.txt','independent':'47-independent-valid.txt','return':'50-return-snapshot.txt'},
'casbin':{'learner':'02-learner.txt','P-only':'06-P-only.txt','P-detail':'09-P-detail.txt','Q-denied':'11-Q-denied.txt','module-denied':'14-module-denied.txt','Q-retained':'18-Q-only.txt','P-revoked':'20-revoked-P.txt','backend-closed':'23-backend-closed.txt','combined':'27-combined.txt','independent':'30-independent.txt','return':'33-return-snapshot.txt'}}
for c,paths in files.items():
 d=Path('output/playwright')/('final-'+c)
 for name,file in paths.items():
  p=d/file;s=p.read_text();criteria={}
  if name in ['learner','backend-closed','return']:
   criteria={'learning-heading':'heading "学习中心"' in s,'no-admin-heading':'heading "管理后台"' not in s,'no-admin-navigation':'navigation [' not in s}
  elif name=='P-only':criteria={'admin':'heading "管理后台"' in s,'only-training':'button "培训中心"' in s and 'button "个人学习报表"' not in s,'P-only':'cell "共享项目 P"' in s and 'cell "项目 Q"' not in s}
  elif name=='P-detail':criteria={'allowed-P':'heading "共享项目 P"' in s and '已获得此项目的访问权限' in s}
  elif name in ['Q-denied','module-denied','P-revoked']:criteria={'safe-denial':'你暂时不能查看或操作这项内容，请联系管理员确认权限' in s,'no-resource-details':'cell "共享项目 P"' not in s and 'heading "共享项目 P"' not in s and 'cell "项目 Q"' not in s,'no-internals':all(x not in s for x in ['TypeError','SELECT ','stacktrace','compiler-30'])}
  elif name=='Q-retained':criteria={'Q-only':'cell "项目 Q"' in s and 'cell "共享项目 P"' not in s}
  elif name=='combined':criteria={'both-sources':'button "培训中心"' in s and 'button "个人学习报表"' in s and 'cell "共享项目 P"' in s}
  elif name=='independent':criteria={'admin-retained':'heading "管理后台"' in s,'report-only':'button "个人学习报表"' in s and 'button "培训中心"' not in s,'self-count-one':'当前可见记录：1' in s}
  checks.append({'candidate':c,'step':name,'path':str(p),'criteria':criteria,'pass':all(criteria.values()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 # Copy CLI-generated snapshots, console, trace and resources referenced in logs, preserving source paths.
 for p in d.glob('*.txt'):
  for rel in re.findall(r'\.playwright-cli/[\w./-]+',p.read_text()):
   src=Path(rel)
   if src.is_dir():
    sources=[x for x in src.rglob('*') if x.is_file()]
   elif src.is_file():sources=[src]
   else:continue
   for f in sources:
    dest=d/'cli-artifacts'/f
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest);copied.append(str(dest))
result={'at':datetime.now(timezone.utc).isoformat(),'applicationSource':'cb72484ed8e7547146920fd4312dd24f8c9e2402','sourceCommit':'d6e2d66','checks':checks,'allPassed':all(c['pass'] for c in checks),'artifactFiles':len(set(copied)),'excludedEvidence':[{'paths':['output/playwright/final-native/Q-denied.png','output/playwright/final-native/11-Q-network.txt'],'reason':'Controller mistakenly overlapped two CLI command sequences; ambiguous capture state. Retain but not denial proof. Use exact10 snapshot and sequential21/22 instead.'},{'paths':['output/playwright/final-native/26-independent-role.json','output/playwright/final-native/29-combined.txt','output/playwright/final-native/32-independent.txt','output/playwright/final-native/34-independent-refreshed.txt','output/playwright/final-native/36-self-report.txt','output/playwright/final-native/41-combined.txt','output/playwright/final-native/independent-report.png'],'reason':'Malformed controller fixture omitted navigation/delegableActions. Correctly denied or503, not valid independent-role acceptance. Correction SQL38/42; valid44/47/50 used.'}],'limits':['Controller inspected real DOM plus screenshots for both candidates, with actual button navigation.','Synthetic fixture admin setup is not role configuration UI acceptance. Host Node processes are not resource-capped reference windows.','Console retains expected403, favicon404 and Native malformed-fixture503; no compiler error.','Native trace begins at revokedP; earlier real snapshots/control records remain separate. Casbin trace covers full grant/revoke flow.','Browser flow covers AUTH-T06/T10 business shell only, not formal product AC completion or whole Go.']}
Path('evidence/browser-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'passed':sum(c['pass'] for c in checks),'copied':len(set(copied))}));assert result['allPassed']
