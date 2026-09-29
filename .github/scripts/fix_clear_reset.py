from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Rename button so the action is clear.
s = s.replace(
    '<button id="clearPlanFoBtn" type="button" style="background:#dc2626;color:#fff">เคลียร์ FO ทั้งหมด 🔒</button>',
    '<button id="clearPlanFoBtn" type="button" style="background:#dc2626;color:#fff">Reset / เคลียร์ FO 🔒</button>',
    1
)

# 2) Reset must leave PLAN_MASTER at zero rows; never recreate placeholders here.
s = s.replace(
    "    PLAN_MASTER.length=0;\n    if(typeof ensurePlanMinRows==='function') ensurePlanMinRows();\n    if(typeof renderPlanTable==='function') renderPlanTable();",
    "    PLAN_MASTER.length=0;\n    if(typeof renderPlanTable==='function') renderPlanTable();",
    1
)

# 3) Never generate JOBxxx-NS-LNA for a truly empty placeholder row.
old_ensure = '''function ensurePlanJobId(row,seq=1){
  row.masterFo=cellText(row.masterFo||row.fo||row.productionFo);
  row.productionFo=cellText(row.productionFo||row.fo||row.masterFo);
  row.fo=row.productionFo;
  row.process=cellText(row.process)||"Sewing";
  row.size=cellText(row.size)||"ไม่มี Size";
  row.jobQty=cellText(row.jobQty||row.qty||row.orderQty);
  row.jobId=cellText(row.jobId)||generateJobId(row,seq);
  return row;
}'''
new_ensure = '''function ensurePlanJobId(row,seq=1){
  row.masterFo=cellText(row.masterFo||row.fo||row.productionFo);
  row.productionFo=cellText(row.productionFo||row.fo||row.masterFo);
  row.fo=row.productionFo;
  row.process=cellText(row.process)||"Sewing";
  row.size=cellText(row.size)||"ไม่มี Size";
  row.jobQty=cellText(row.jobQty||row.qty||row.orderQty);

  const hasRealPlanData=[
    row.masterFo,row.productionFo,row.fo,row.style,row.color,row.line,
    row.jobQty,row.sam,row.orderQty,cellText(row.jobId)
  ].some(v=>cellText(v)!=="");

  row.jobId=hasRealPlanData
    ? (cellText(row.jobId)||generateJobId(row,seq))
    : "";
  return row;
}'''

if old_ensure in s:
    s = s.replace(old_ensure, new_ensure, 1)
elif 'const hasRealPlanData=[' not in s:
    raise SystemExit('ERROR: ensurePlanJobId block not found; index left unchanged')

# Safety checks before write.
required = [
    '<title>Production Control V1.35 — JOB ID</title>',
    'เลือกจากทั้งหมด 18 Line',
    'Production Plan Master',
    'prod-ok', 'prod-repair', 'prod-ng',
    'Reset / เคลียร์ FO 🔒',
    'CLEAR PLAN FO PATCH V1',
    'const hasRealPlanData=[',
    '</html>'
]
for token in required:
    if token not in s:
        raise SystemExit(f'ERROR: required token missing: {token}')

clear_tail=s[s.rfind('/* CLEAR PLAN FO PATCH V1 */'):]
if "ensurePlanMinRows" in clear_tail:
    raise SystemExit('ERROR: Clear FO still recreates placeholder rows')

if len(s.encode('utf-8')) < 200000:
    raise SystemExit('ERROR: index unexpectedly small; refusing to write')

p.write_text(s, encoding='utf-8')
print('FIX_CLEAR_RESET_OK', len(s.encode('utf-8')))
