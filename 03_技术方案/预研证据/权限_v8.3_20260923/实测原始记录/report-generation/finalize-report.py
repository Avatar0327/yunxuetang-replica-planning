"""Controller report rendering after all frozen reference windows; no application changes."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,hashlib,re,subprocess,gzip
ROOT=Path.cwd(); TECH=Path('/Users/peng/Library/Mobile Documents/com~apple~CloudDocs/Agent复刻项目/云学堂复刻规划/03_技术方案')
CAMP=ROOT/'evidence/raw/reference-final-eb3fb3e-20260923'
assert (CAMP/'campaign-exit.txt').exists(),'Do not finalize a running reference campaign'
ps=json.loads((ROOT/'evidence/performance-summary.json').read_text()); windows=ps['windows']
assert len(windows)==4 and all(not w.get('incomplete') for w in windows)
for w in windows:
 a=w['audit'];assert not a['audit_errors'] and a['actual_wall_ms']>=600000 and a['observed_client_count']==50
 assert w['runtime']['resource_gate'] and w['runtime']['data_scale_gate']
 assert not a['categories'].get('authorization_error',0) and not a.get('raw_correctness_mismatches'), 'Unexpected authorization result requires explicit adjudication'
# A passing candidate changes the ADR/ruling: never hard-code No-Go across a successful implementation.
assert not any(all(w['gate']['all_measured_windows_pass'] for w in windows if w['candidate']==c) for c in ['native','casbin'])
now=datetime.now().astimezone().isoformat(timespec='seconds')
mapdoc=json.loads((ROOT/'output/functional-coverage-map.json').read_text()); review=json.loads((ROOT/'output/functional-semantic-review.json').read_text())
byid={i['id']:i for i in mapdoc['items']}
gates={'09':('hot','permission',None),'10':('cold','permission',None),'11':('hot','success','list-'),'12':('cold','success','list-'),'13':(None,'success','history-')}
for tail,(cache,metric,prefix) in gates.items():
 selected=[w for w in windows if cache is None or w['cache']==cache]
 measures=[(w,t,s) for w in selected for s,t in w['audit']['threshold_observations'].items() if prefix is None or s.startswith(prefix)]
 assert any(not t[metric+'_met'] for _,t,_ in measures)
 item=byid['AUTH-T18-'+tail];item['status']='fail'
 item['actualResult']='完整参考窗口实测未达04门槛：'+'；'.join(f"{w['candidate']}/{w['cache']}/{s} p95={t[metric+'_p95_ms']:.2f}ms，门槛{t[metric+'_limit_ms']}ms" for w,t,s in measures)+'。只使用成功样本；失败请求独立计数。'
for tail in ['19','20']:
 item=byid['AUTH-T18-'+tail];item['status']='pass';item['actualResult']='四个窗口均实际观测50客户端、持续至少600秒、访问A/B；每窗Docker限配、源码镜像标签、PG参数和实际50k/1M数据核验通过。此行仅确认测量基准执行，不代表延迟通过。'
for tail in [*gates,'19','20']:
 item=byid['AUTH-T18-'+tail]
 for w in windows:
  item['evidence'].append({'kind':'benchmark','candidate':w['candidate'],'path':w['path']+'/independent-audit.json'})
  item['evidence'].append({'kind':'benchmark','candidate':w['candidate'],'path':w['path']+'/runtime-check.json'})
 item['evidence'].append({'kind':'benchmark','candidate':'shared','path':'evidence/performance-summary.json'})
counts=dict(Counter(i['status'] for i in mapdoc['items'])); assert counts=={'pass':163,'fail':5},counts
mapdoc.update(updatedAt=now,controllerSemanticReviewCompleted=True,boundary='All168 requirements have explicit controller semantic/evidence judgments.163pass/5performancefail;overallNO_GO. Historical and final source provenance retained; product53AC and independent deployment are not thereby passed.')
(ROOT/'evidence/coverage-map.json').write_text(json.dumps(mapdoc,ensure_ascii=False,indent=2)+'\n')
review.update(reviewed_at=now,mapping_sha256=hashlib.sha256((ROOT/'evidence/coverage-map.json').read_bytes()).hexdigest(),scope='全部168点由控制器逐项裁定；功能/边界163通过，5性能项失败。结合独立代码审查，无整体Go。',overall_go_inferred=False,overall_gate='NO_GO')
review['group_review']['AUTH-T18']='四窗实际50客户端×600秒，资源/数据/源码一致；每个200真值独立核对，授权错误与真值差异0。权限、列表/count、历史聚合5个性能核对点不达标，163通过/5失败，完整统计与错误率单列。'
for r in review['items']:r['controller_semantic_state']='reviewed_'+byid[r['id']]['status']
(ROOT/'evidence/controller-semantic-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
num=lambda x:f'{x:.2f}'
rng=lambda arr:f'{min(arr):.2f}～{max(arr):.2f}'
lines=['单位均为毫秒；p95仅来自成功请求。权限门槛50、列表500、历史聚合2000。','','| 候选/缓存 | 成功/总请求 | 非成功率 | 权限p95范围（四场景） | 列表p95范围 | 宽/复杂历史p95 | 结论 |','|---|---:|---:|---|---|---|---|']
total=success=auth_errors=measurement_errors=0;failure_statuses=Counter()
for w in windows:
 a=w['audit'];t=a['threshold_observations'];c=a['categories'];n=a['sample_count'];s=c.get('success',0);total+=n;success+=s;auth_errors+=c.get('authorization_error',0);measurement_errors+=c.get('measurement_error',0)
 lines.append(f"| {w['candidate']}/{w['cache']} | {s}/{n} | {(n-s)/n*100:.2f}% | {rng([v['permission_p95_ms'] for v in t.values()])} | {rng([v['success_p95_ms'] for k,v in t.items() if k.startswith('list-')])} | {num(t['history-broad']['success_p95_ms'])}/{num(t['history-constrained']['success_p95_ms'])} | 未通过 |")
 with gzip.open(ROOT/w['path']/'measurement/samples.jsonl.gz','rt') as f:
  for record in f:
   r=json.loads(record)
   if r['classification']!='success':failure_statuses[str(r['status']) if r.get('status') is not None else 'transport_exception']+=1
perf_table='\n'.join(lines)
findings=f'四个参考窗口合计 {total:,} 次请求，成功 {success:,} 次，非成功 {total-success:,} 次；非成功HTTP/传输分类为 {dict(failure_statuses)}。成功结果真值差异与记录到的授权错误均为 {auth_errors}，测量错误 {measurement_errors}；各窗口均未满足原性能门槛，不能凭语义正确放行。'
end=json.loads((CAMP/'casbin-cold/measurement/summary.json').read_text())['endAt']
replacement={
'VERDICT':'No-Go',
'OUTCOME':'本轮性能门禁未通过，两套候选均不能按当前实现进入正式权限开发。',
'GATE_SUMMARY':'**163 个核对点通过，5 个性能核对点未通过，0 个未完成。** 失败项为 AUTH-T18-09/10（冷热权限开销）、11/12（冷热列表/count）和13（历史聚合）。四个50客户端×600秒参考窗口已完成；不放宽任何延迟门槛，不将失败请求计入成功性能。功能、故障和浏览器的限定结果见下文。',
'EXECUTION_END':f'最后一个参考窗口结束于 {end}（UTC，北京时间加8小时），报告编制于 {now}',
'PERFORMANCE_TABLE':perf_table,
'PERFORMANCE_FINDING':findings,
'PERFORMANCE_CAUSALITY':'实测确认权限段和数据段均有显著开销；尚未完成CPU、事件循环、连接池等待与具体SQL之间的组件级归因。大集合/JSON表示是明确可见的成本候选，不能仅凭本次总时延宣布唯一根因。下一轮须补分段观测并验证新的范围/上限查询表示，随后在相同资源重跑，不能只调高超时或放宽门槛。',
'ESTIMATE_RESULT':'两候选共同的权限/查询路径在正式参考条件下均未达门槛。建议先做有界性能整改预研，再据通过的方案修订正式实施；当前不把任何未验证的优化当成已完成工作。下表是新增大集合技术工作发生时的条件重估，保留已审A作比较。',
'SIGNED_AT':now,
'SIGNOFF_REASON':'两候选冷热权限、列表/count和历史聚合参考性能不达标，且正常负载存在非成功请求（具体分类以上表为准）',
'NEXT_ACTION':'下一步应先评审本报告、ADR及2～4人天整改预研建议，验证大集合许可关系/版本绑定计划与SQL方案，再完整复测；未获新一轮门禁通过前，正式B1保持不启动。本次交付的是有失败结论的完整预研报告，不是以报告齐全替代通过。'}
text=(ROOT/'output/final-report-draft.md').read_text()
for k,v in replacement.items():text=text.replace('{{'+k+'}}',v)
assert not re.search(r'\{\{[A-Z_]+\}\}',text)
# Preserve full historical execution draft before replacing the controller-owned report.
old=TECH/'12_权限预研报告.md';backup=ROOT/'evidence/raw/12-执行中历史快照.md'
if not backup.exists():backup.write_bytes(old.read_bytes())
old.write_text(text)
adr=(ROOT/'output/final-adr-draft.md').read_text()
ars={'ADR_STATUS':'技术建议形成，当前门禁No-Go；待业务/项目负责人评审','ADR_GATE':'两套候选参考性能均未达标，当前不能放行正式开发。','ADR_PERFORMANCE':perf_table,'ADR_INTERPRETATION':findings+' 两候选共用大部分权限/查询路径，因此本次结果首先说明当前方案整体需要整改。','ADR_REMEDIATION':'下一轮先增加权限构建、序列化/解析、事件循环、池等待和数据SQL的分段观测；比较版本绑定的许可关系/计划与直接关系查询，避免每请求搬运大人员/公司数组。允许提出索引或表示优化，但必须保存原真值、来源字段和版本边界，使用同资源完整冷热窗口及撤权/故障回归证明。未实际验证前不选定某个新Schema为正式实现。'}
for k,v in ars.items():adr=adr.replace('{{'+k+'}}',v)
assert not re.search(r'\{\{[A-Z_]+\}\}',adr)
(TECH/'13_Native与Casbin取舍ADR.md').write_text(adr)
est=json.loads((ROOT/'output/post-spike-estimate-draft.json').read_text());est.update(created_at=now,reference_evidence=str(CAMP.relative_to(ROOT)),current_gate='NO_GO',basis='Both candidate hot/cold reference windows failed; proposed large-set core work is conditional until a remedial feasibility spike succeeds.')
(TECH/'核验记录/预研后条件工期核算.json').write_text(json.dumps(est,ensure_ascii=False,indent=2)+'\n')
(ROOT/'evidence/final-verdict.json').write_text(json.dumps({'at':now,'gate':'NO_GO','functional_matrix':counts,'failed_ids':[i['id'] for i in mapdoc['items'] if i['status']=='fail'],'reference_source':ps['sourceCommit'],'application_source':mapdoc['sourceCommit'],'requests':total,'successful_requests':success,'non_success_statuses':dict(failure_statuses),'authorization_errors':auth_errors,'measurement_errors':measurement_errors,'formal_B1_started':False,'prototype_reuse_credit':0,'human_signature':None},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'gate':'NO_GO','counts':counts,'requests':total,'success':success,'failures':dict(failure_statuses)},ensure_ascii=False))
