from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old='''    PLAN_MASTER.length=0;\n    if(typeof ensurePlanMinRows==='function') ensurePlanMinRows();\n    if(typeof renderPlanTable==='function') renderPlanTable();'''
new='''    PLAN_MASTER.length=0;\n    if(typeof renderPlanTable==='function') renderPlanTable();'''

if old not in s:
    raise SystemExit('ERROR clear FO block not found; index unchanged')

s=s.replace(old,new,1)

required=[
  '<title>Production Control V1.35 — JOB ID</title>',
  'เลือกจากทั้งหมด 18 Line',
  'Production Plan Master',
  'id="clearPlanFoBtn"',
  'CLEAR PLAN FO PATCH V1',
  'PLAN_MASTER.length=0;',
  'prod-ok','prod-repair','prod-ng','</html>'
]
for token in required:
    if token not in s:
        raise SystemExit('ERROR missing required token: '+token)
if len(s.encode('utf-8'))<200000:
    raise SystemExit('ERROR file unexpectedly small')

p.write_text(s,encoding='utf-8')
print('PATCH_OK clear FO leaves zero plan rows',len(s.encode('utf-8')))
