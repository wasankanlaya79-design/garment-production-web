from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

BUTTON = 'id="clearPlanFoBtn"'
MARKER = '/* CLEAR PLAN FO PATCH V1 */'

old_toolbar = '''          <button id="importPlanExcelBtn" class="export-excel">โหลดแผนจาก Excel 🔒</button>
          <button id="downloadPlanTemplateBtn" class="secondary">ดาวน์โหลด Template Excel</button>
          <button id="unlockPlannerBtn" class="primary">เพิ่ม / แก้ไขแผน 🔒</button>'''

new_toolbar = '''          <button id="importPlanExcelBtn" class="export-excel">โหลดแผนจาก Excel 🔒</button>
          <button id="downloadPlanTemplateBtn" class="secondary">ดาวน์โหลด Template Excel</button>
          <button id="clearPlanFoBtn" type="button" style="background:#dc2626;color:#fff">เคลียร์ FO ทั้งหมด 🔒</button>
          <button id="unlockPlannerBtn" class="primary">เพิ่ม / แก้ไขแผน 🔒</button>'''

patch = r'''
<script>
/* CLEAR PLAN FO PATCH V1 */
(function(){
  function clearAllPlanFo(){
    const pin=prompt("กรอกรหัส Planner เพื่อเคลียร์ FO ทั้งหมด");
    if(pin===null) return;
    if(pin!==PLANNER_PIN){
      alert("รหัสไม่ถูกต้อง");
      return;
    }

    const realRows=PLAN_MASTER.filter(rowHasPlanContent).length;
    if(!confirm(
      `ยืนยันเคลียร์ FO ทั้งหมด ${realRows} รายการ?\n\n`+
      `• ล้างเฉพาะ Production Plan Master\n`+
      `• ไม่ลบ Production Log / ประวัติการผลิต\n`+
      `• หลังเคลียร์สามารถโหลดแผนใหม่ได้ทันที`
    )) return;

    PLAN_MASTER.length=0;
    if(typeof ensurePlanMinRows==='function') ensurePlanMinRows();
    if(typeof renderPlanTable==='function') renderPlanTable();
    if(typeof refreshFoOptions==='function') refreshFoOptions();

    const foSelect=document.getElementById('foSelect');
    if(foSelect) foSelect.value='';

    if(typeof recordAudit==='function'){
      recordAudit('CLEAR_PLAN_FO',`เคลียร์ Production Plan Master ${realRows} รายการ`);
    }
    if(typeof setPlanImportStatus==='function'){
      setPlanImportStatus(`เคลียร์ FO สำเร็จ ${realRows} รายการ • Production Log ยังอยู่`,'success');
    }

    alert(`เคลียร์ FO สำเร็จ ${realRows} รายการ\nProduction Log ยังอยู่`);
  }

  function bindClearFo(){
    const btn=document.getElementById('clearPlanFoBtn');
    if(btn && !btn.dataset.boundClearFo){
      btn.dataset.boundClearFo='1';
      btn.addEventListener('click',clearAllPlanFo);
    }
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',bindClearFo);
  }else{
    bindClearFo();
  }
})();
</script>
'''

# Ensure the button exists exactly once in the planner toolbar.
if BUTTON not in s:
    if old_toolbar not in s:
        raise SystemExit('ERROR: planner toolbar marker not found; index.html left unchanged')
    s = s.replace(old_toolbar, new_toolbar, 1)

# Remove any previous misplaced copy of the patch block.
while patch in s:
    s = s.replace(patch, '', 1)

# Also remove a legacy misplaced block by marker boundaries if needed.
if MARKER in s:
    marker_pos = s.find(MARKER)
    script_start = s.rfind('<script>', 0, marker_pos)
    script_end = s.find('</script>', marker_pos)
    if script_start >= 0 and script_end >= 0:
        s = s[:script_start] + s[script_end + len('</script>'):]

# Insert only before the FINAL closing body tag, never the report templates above.
body_pos = s.rfind('</body>')
if body_pos < 0:
    raise SystemExit('ERROR: final closing body not found; index.html left unchanged')
s = s[:body_pos] + patch + '\n' + s[body_pos:]

# Safety checks: abort rather than damage the known-good page.
required = [
    '<title>Production Control V1.35 — JOB ID</title>',
    'เลือกจากทั้งหมด 18 Line',
    'Production Plan Master',
    'prod-ok', 'prod-repair', 'prod-ng',
    'id="clearPlanFoBtn"',
    'CLEAR PLAN FO PATCH V1',
    '</html>'
]
for token in required:
    if token not in s:
        raise SystemExit(f'ERROR: required token missing after patch: {token}')

if s.count(MARKER) != 1:
    raise SystemExit(f'ERROR: expected exactly one clear-FO patch, found {s.count(MARKER)}')

# The real patch must be near the actual end of the document.
if s.rfind(MARKER) < len(s) - 12000:
    raise SystemExit('ERROR: clear-FO patch is not near final document end; refusing to write')

if len(s.encode('utf-8')) < 200000:
    raise SystemExit('ERROR: patched index unexpectedly small; refusing to write')

p.write_text(s, encoding='utf-8')
print('PATCH_OK', len(s.encode('utf-8')))
