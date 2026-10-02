from pathlib import Path
from datetime import datetime
import json
ROOT=Path.cwd(); TECH=Path('/Users/peng/Library/Mobile Documents/com~apple~CloudDocs/Agent复刻项目/云学堂复刻规划/03_技术方案')
v=json.loads((ROOT/'evidence/final-verdict.json').read_text());assert v['gate']=='NO_GO'
now=datetime.now().astimezone().isoformat(timespec='seconds')
def modify(name,replacements=(),append=None):
 p=TECH/name;s=p.read_text()
 for a,b in replacements:
  if a in s:s=s.replace(a,b)
  elif b not in s:raise ValueError('Expected source not found: '+name+' / '+a[:80])
 if append and append[0] not in s:s+='\n\n'+append[1]+'\n'
 p.write_text(s)
modify('00_技术方案索引与决策.md',[
 ('| [12 权限预研报告](12_权限预研报告.md) | 执行中：原始证据、独立审查、后续矩阵/故障/性能及Go/No-Go；当前无整体通过结论 |','| [12 权限预研报告](12_权限预研报告.md) | 已交付No-Go：168点实际矩阵、故障、四窗性能、审查、风险与签字页 |\n| [13 Native与Casbin取舍ADR](13_Native与Casbin取舍ADR.md) | 建议Native作为整改候选；两候选当前性能均未通过，不放行正式B1 |'),
 ('本包覆盖完整Path A的技术设计，不只前三批。Schema和接口是设计规格，未创建应用、数据库、迁移脚本或预研原型。11重估已通过业务审核，用户已放行三天权限预研；须先完成v8.3输入重新基线化；三天报告另行交付，不能把计划当结果。','本包覆盖完整Path A的技术设计，不只前三批。正式Schema和接口仍为设计规格；已另建本地隔离权限原型。v8.3重新基线化、A业务审核及B执行授权均已完成；交付物B现为No-Go，实际结果见12，不将计划或原型视为正式B1完成。'),
 ('权限预研已在隔离原型中执行，当前尚无整体Go结论；局部测试与独立审查的实际结果见[12预研报告](12_权限预研报告.md)。浏览器、完整矩阵和性能证据仍须逐项核验，万人同时在学容量尚未验证。11保留“预研前估算，非承诺工期”的核算基线，不能将文件齐全视为可以绕过门禁。','权限预研已完成本轮证据交付，结论为**No-Go**：163/168核对点通过、5项性能失败。浏览器、故障及四个50客户端×600秒参考窗口均已执行，详见[12](12_权限预研报告.md)和[13](13_Native与Casbin取舍ADR.md)；万人同时在学容量尚未验证。11保留已审A的265～417基线，另列预研后条件建议；正式B1不启动，原型折抵0。')])
modify('04_权限模型与三天预研.md',[
 ('**预研已获用户授权并在v8.3输入门禁通过后开始执行，当前无整体Go结论，正式B1权限开发未开始。**','**本轮预研已完成证据交付，结论No-Go：163点通过、5项性能失败，正式B1权限开发未开始。**'),
 ('### 9.5 性能指标提议（均未实测）','### 9.5 启动前冻结的性能指标（实际结果见12）')],('## 11. 本轮预研结果索引','''## 11. 本轮预研结果索引

2026-09-23：原计划按三阶段执行，未声称三个日历日已过去。24组/168点逐项复核，163通过、AUTH-T18-09/10/11/12/13五项性能失败；四个资源匹配的50客户端×600秒窗口已完成，判定**No-Go**。T-05/T-06/T-07、双实例下一媒体请求撤权、Redis/DB故障与Pub/Sub缺失均有实测；未将功能正确替代性能门禁。

本节及9.5保留原已批准阈值，不改成实测较慢的值。矩阵、原始证据、故障时间线、性能、模块边界、工期条件和真实签字状态见[12](12_权限预研报告.md)；引擎取舍见[13](13_Native与Casbin取舍ADR.md)。原型折抵0；正式B1未放行。'''))
modify('06_前三批实施与验收计划.md',[
 ('已确认决定不重复索要；预研和实现仍未执行。','已确认决定不重复索要；预研已交付No-Go，实际矩阵与性能见12，正式B1实现仍未开始。')])
modify('07_需求与验收追踪.md',append=('## 5. 权限预研实际结果','''## 5. 权限预研实际结果（独立AUTH命名空间）

交付物B见[12预研报告](12_权限预研报告.md)与[完整168点矩阵](预研证据/权限_v8.3_20260923/矩阵与摘要/coverage-matrix.md)。24组全保留，163点通过、5点失败、0未完成；失败为AUTH-T18-09/10权限冷热开销、11/12列表/count、13历史聚合。四窗各50客户端×600秒及资源/数据核验已实际执行，当前门禁**No-Go**，正式B1不启动。

T-05多角色覆盖、T-06任命后台、T-07客户甲/乙/内部公司边界、两实例撤权含媒体及Redis/PubSub故障均有原型证据。它们支持相关REQ/AC/TD的技术可行性判断，**不把本表94REQ、53AC或13TD自动改为产品验收通过**。53场景保持原编号/标题和范围，B6仍按52适用/7宣读/33差异；五项永久缺口不销项。'''))
modify('08_设计审查记录.md',append=('### 7.4 本轮预研终审与No-Go交付',f'''### 7.4 本轮预研终审与No-Go交付

{now}：65正本指纹保持v8.3，未再次重新基线化，也未修改业务输入。最终全分支审查四项Important已按一次集中修复及一次限定复审关闭：任命键碰撞、合法混合ID排序误拒、分类403/503存在性差异、Vue空白页。源码cb72484，限定复审d6e2d66，参考窗口eb3fb3e；src/sql/web一致。保留1项可读性Minor。

控制器独立核对35对归档SHA、最终Task3/4/5共1228条字面观察零差异；8条核心记录仅约定业务字段相等，保留动态revision差异说明。317/317 Node条目不是168点或产品AC计数。真实Chrome双候选22个命名状态完成；交错采集及无效角色夹具不计通过证据，原件保留。

Casbin冷窗建数先有两次10秒SQL超时；仅宿主建数会话改60秒后按原SQL完成，失败原件与补跑履历保留，API和性能门槛未改。四窗各50客户端×600秒，实际限配与50k/1M数据核验均通过。168点逐项裁定为163通过/5性能失败，整体**No-Go**；成功请求{v['successful_requests']}/{v['requests']}，非成功分类{v['non_success_statuses']}，授权错误{v['authorization_errors']}。完整原始统计、错误率、故障/撤权时间线、独立审查、ADR、风险重估和待人工签字页已交付12/13。未用快速拒绝计入正常查询p95。

同步了索引、04、06、07、11的当前状态；较早阶段审查与执行报告作为历史保留。统计报告脚本曾按fault取失败计时字段，控制器修为实际failure并用8组既有数据核对；未改原测量或应用逻辑。A已审265～417保持，正式核心净增6～12和新增整改预研2～4仅为条件建议，非追加批准。原型折抵0、正式B1未开始，五永久缺口、七宣读、四最简、两已承担风险继续保留。'''))
modify('11_范围与工期重估.md',[
 ('**04的24项AUTH测试正在执行，当前没有整体Go签字；完整矩阵和实测结论见12。**','**04的24项AUTH已完成本轮实际矩阵，当前结论No-Go；163点通过、5项性能失败，完整实测见12。**')],('## 9. 预研后条件重估','''## 9. 预研后条件重估（交付物B附录，未批准追加）

本轮四个完整参考窗口均未达04的性能门槛，结论No-Go，详见[12](12_权限预研报告.md)及[ADR](13_Native与Casbin取舍ADR.md)。**以上A的分列表、265～417总量和原271～429条件情形保持为已审比较基线，不反写已审估计。**

若下一轮证实需要改造大集合许可关系/版本绑定计划与SQL表示，建议B1-05由5～8改6～10（增1～2），B1-07由3～5改8～15（增5～10），合计8～13替换为14～25，净增6～12；B1-08仍为2～3单列。B1由41～70变47～82，完整含原预研3天的条件总量为271～429。它是原条件包的具体工作展开，不再加一次6～12，不因选择Native自动收费，也不重算已含的T-05/T-07/T-16、公司与工程增量。

尚未执行的性能整改预研建议2～4人天另列，先分段诊断、验证表示和查询，再按同资源完整冷热/撤权/故障复测。若正式核心变化和新增预研两者均被采用，总量才为273～433。均为条件估算、非承诺工期、非已批准追加，且不构成未知风险上限。可复用文件已在12配套清单列出，但当前被替代正式工作项仍为空、折抵0；未来同一片段不可同时按原型和正式工作重复记工。

主要不确定度为许可集合基数、SQL计划、序列化/池等待、冻结/重验频率、真实媒体网关和单人复核节奏。框架语义承载可行不等于当前性能通过。具体算式见[预研后条件核算](核验记录/预研后条件工期核算.json)，它不替换原[范围工期计算底稿](核验记录/范围工期计算底稿.json)。'''))
state_path=TECH/'预研证据/权限_v8.3_20260923/执行状态.json';state=json.loads(state_path.read_text());state.update(updated_at=now,permission_gate='NO_GO',phase='交付物B已交付；163点通过/5性能失败；正式B1不放行',task6='complete_evidence_delivery_NO_GO',domain_integration_complete=True,benchmark_reference_complete=True,browser_complete=True,known_open_findings=['AUTH-T18-09/10/11/12/13性能未达门槛','正常参考负载出现非成功请求'],open_findings=['Performance remediation required before formalB1'],final_application_source=v['application_source'],reference_source=v['reference_source'],final_matrix=v['functional_matrix'],final_reference_requests=v['requests'],final_reference_success=v['successful_requests'],permission_spike_go=False,overall_go=False,formal_B1_started=False,prototype_reuse_credit_person_days=0,human_signature=None)
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
# Prototype active status; phase reports remain historical rather than rewritten evidence.
p=ROOT/'README.md';s=p.read_text().replace('Full168 semantic acceptance, real browser and capped reference performance remain incomplete; formal B1 is not authorized.','Final controller audit records163passed/5performancefailed out of168, with real browser and four capped50-client600-second windows complete. OverallNO_GO; formalB1 is not authorized. See evidence/coverage-matrix.md,performance-statistics.md and final-verdict.json.').replace('Actual browser/capped reference windows and independent168 acceptance remain incomplete; formalB1 remains prohibited.','Actual browser, four capped reference windows and independent168 audit are complete; five performance requirements failed and formalB1 remains prohibited.');p.write_text(s)
for name in ['task2-follow-up.md','task3-ports.md','task4-ports.md','task5-ports.md','controller-acceptance-audit-notes.md','decision-evidence.md','post-spike-estimate-notes.md']:
 p=ROOT/'docs'/name;s=p.read_text();note='> 历史阶段底稿：下文的待执行/未完成指当时交接时点；2026-09-23最终实测为163通过/5性能失败、整体No-Go，见evidence/coverage-matrix.md和performance-statistics.md及03/12、13。原规则与阶段证据保留。\n\n'
 if not s.startswith('> 历史阶段底稿'):p.write_text(note+s)
print(json.dumps({'technical_status_synchronized':True,'formal_B1_started':False,'human_signature':None},ensure_ascii=False))
