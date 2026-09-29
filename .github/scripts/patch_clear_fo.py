from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

BUTTON = 'id="clearPlanFoBtn"'
MARKER = '/* CLEAR PLAN FO PATCH V1 */'

if BUTTON in s and MARKER in s:
    print('Clear FO patch already present; nothing to do.')
    raise SystemExit(0)

old_toolbar = '''          <button id="importPlanExcelBtn" class="export-excel">โหลดแผนจาก Excel 🔒</button>
          <button id="downloadPlanTemplateBtn" class="secondary">ดาวน์โหลด Template Excel</button>
          <button id="unlockPlannerBtn" class="primary">เพิ่ม / แก้ไขแผน 🔒</button>'''

new_toolbar = '''          <button id="importPlanExcelBtn" class="export-excel">โหลดแผนจาก Excel 🔒</button>
          <button id="downloadPlanTemplateBtn" class="secondary">ดาวน์โหลด Template Excel</button>
          <button id="clearPlanFoBtn" type="button" style="background:#dc2626;color:#fff">เคลียร์ FO ทั้งหมด 🔒</button>
          <button id="unlockPlannerBtn" class="primary">เพิ่ม / แก้ไขแผน 🔒</button>'''

if old_toolbar not in s:
    raise SystemExit('ERROR: planner toolbar marker not found; index.html left unchanged')

s = s.replace(old_toolbar, new_toolbar, 1)

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

if '</body>' not in s:
    raise SystemExit('ERROR: closing body not found; index.html left unchanged')

s = s.replace('</body>', patch + '\n</body>', 1)

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

if len(s.encode('utf-8')) < 200000:
    raise SystemExit('ERROR: patched index unexpectedly small; refusing to write')

p.write_text(s, encoding='utf-8')
print('PATCH_OK', len(s.encode('utf-8')))
