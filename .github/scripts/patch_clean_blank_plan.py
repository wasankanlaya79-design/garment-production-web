from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

changes=[]

old='''while(PLAN_MASTER.length<33){\n  PLAN_MASTER.push({seq:PLAN_MASTER.length+1,jobId:"",masterFo:"",productionFo:"",fo:"",style:"",color:"",process:"Sewing",size:"",line:"",jobQty:"",sam:"",eff:"40",orderQty:""});\n}'''
new='''while(PLAN_MASTER.length<33){\n  PLAN_MASTER.push({seq:PLAN_MASTER.length+1,jobId:"",masterFo:"",productionFo:"",fo:"",style:"",color:"",process:"",size:"",line:"",jobQty:"",sam:"",eff:"",orderQty:""});\n}'''
if old not in s:
    raise SystemExit('ERROR startup blank rows marker not found')
s=s.replace(old,new,1); changes.append('startup blanks')

old='''function blankPlanRow(){\n  return {seq:0,jobId:"",masterFo:"",productionFo:"",fo:"",style:"",color:"",process:"Sewing",size:"",line:"",jobQty:"",sam:"",eff:"40",orderQty:""};\n}'''
new='''function blankPlanRow(){\n  return {seq:0,jobId:"",masterFo:"",productionFo:"",fo:"",style:"",color:"",process:"",size:"",line:"",jobQty:"",sam:"",eff:"",orderQty:""};\n}'''
if old not in s:
    raise SystemExit('ERROR blankPlanRow marker not found')
s=s.replace(old,new,1); changes.append('blankPlanRow')

old='''  PLAN_MASTER.forEach((r,i)=>ensurePlanJobId(r,i+1));'''
new='''  PLAN_MASTER.forEach((r,i)=>{\n    const hasRealPlanData=[r.jobId,r.masterFo,r.productionFo,r.fo,r.style,r.color,r.line,r.jobQty,r.sam,r.orderQty]\n      .some(v=>cellText(v)!=="");\n    if(hasRealPlanData) ensurePlanJobId(r,i+1);\n  });'''
if old not in s:
    raise SystemExit('ERROR render ensurePlanJobId marker not found')
s=s.replace(old,new,1); changes.append('conditional job id')

old='''      <td><input data-i="${i}" data-k="process" value="${esc(r.process||"Sewing")}" ${PLANNER_EDIT?"":"readonly"}></td>'''
new='''      <td><input data-i="${i}" data-k="process" value="${esc(r.process||"")}" ${PLANNER_EDIT?"":"readonly"}></td>'''
if old not in s:
    raise SystemExit('ERROR process display marker not found')
s=s.replace(old,new,1); changes.append('blank process display')

# Safety checks
required=[
  '<title>Production Control V1.35 — JOB ID</title>',
  'เลือกจากทั้งหมด 18 Line',
  'Production Plan Master',
  'id="clearPlanFoBtn"',
  'function blankPlanRow()',
  'const hasRealPlanData=',
  'prod-ok','prod-repair','prod-ng','</html>'
]
for token in required:
    if token not in s:
        raise SystemExit('ERROR missing required token: '+token)
if len(s.encode('utf-8'))<200000:
    raise SystemExit('ERROR file unexpectedly small')

p.write_text(s,encoding='utf-8')
print('PATCH_OK',changes,len(s.encode('utf-8')))
