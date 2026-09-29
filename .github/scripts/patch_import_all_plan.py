from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# 1) Production Code can be used as JOB ID
old='jobId: find(["job id","job_id","jobid","รหัสงานย่อย","รหัสงาน"]),'
new='jobId: find(["job id","job_id","jobid","production code","production_code","productioncode","รหัสงานย่อย","รหัสงาน","รหัสผลิต"]),'
if old not in s:
    raise SystemExit('ERROR jobId alias marker not found')
s=s.replace(old,new,1)

# 2) Do not reject the whole file when JOB IDs repeat. Keep every row and suffix duplicates.
old='''  const duplicateIds=[]; const seen=new Set();\n  imported.forEach(r=>{ const k=normalizeJobKey(r.jobId); if(seen.has(k)) duplicateIds.push(r.jobId); seen.add(k); });\n  if(duplicateIds.length) throw new Error(`JOB ID ซ้ำในไฟล์: ${[...new Set(duplicateIds)].slice(0,5).join(", ")}`);\n  const ok=confirm(`พบ Production Job ${imported.length} งาน\\nระบบจะใช้ JOB ID แยกงานตาม Size / Line\\n\\nต้องการนำเข้าใช่หรือไม่?`);'''
new='''  const usedJobIds=new Set();\n  let duplicateRenamed=0;\n  imported.forEach((r,i)=>{\n    const base=cellText(r.jobId)||generateJobId(r,i+1);\n    let candidate=base;\n    let n=1;\n    while(usedJobIds.has(normalizeJobKey(candidate))){\n      n++;\n      candidate=`${base}-${String(n).padStart(2,"0")}`;\n    }\n    if(candidate!==base) duplicateRenamed++;\n    r.jobId=candidate;\n    usedJobIds.add(normalizeJobKey(candidate));\n  });\n  const ok=confirm(`พบข้อมูล ${imported.length} แถว\\nโหลดทุกแถวแบบ IMPORT ALL AS TEXT\\nJOB ID ซ้ำจะเติมเลขท้ายให้อัตโนมัติ${duplicateRenamed?` (${duplicateRenamed} แถว)`:""}\\n\\nต้องการนำเข้าใช่หรือไม่?`);'''
if old not in s:
    raise SystemExit('ERROR duplicate validation block not found')
s=s.replace(old,new,1)

# 3) Keep every non-empty row, even when FO fields are blank.
old='''    if(!cellText(item.productionFo) && !cellText(item.masterFo)) continue;\n    imported.push(ensurePlanJobId(item,imported.length+1));'''
new='''    imported.push(ensurePlanJobId(item,imported.length+1));'''
if old not in s:
    raise SystemExit('ERROR row skip block not found')
s=s.replace(old,new,1)

# 4) Wider spreadsheet picker
old='accept=".xlsx,.xls,.csv"'
new='accept=".xlsx,.xls,.xlsm,.xlsb,.xlt,.xltx,.xltm,.xml,.csv,.ods,.fods,.txt,.prn,.dif,.slk,.sylk,.dbf,.wk1,.wk3,.wk4,.wks,.123"'
if old not in s:
    raise SystemExit('ERROR file accept marker not found')
s=s.replace(old,new,1)

# 5) Reader: CSV/TXT/PRN as text; all other formats are attempted through SheetJS instead of extension blocking.
old='''    if(ext==="csv"){\n      const text=await file.text();\n      validateAndImportPlanRows(parseCsvText(text));\n      return;\n    }\n\n    if(!["xlsx","xls"].includes(ext)){\n      throw new Error("รองรับเฉพาะ .xlsx, .xls และ .csv");\n    }\n\n    const XLSX=await loadSheetJs();\n    const buffer=await file.arrayBuffer();\n    const wb=XLSX.read(buffer,{type:"array"});'''
new='''    if(["csv","txt","prn"].includes(ext)){\n      const text=await file.text();\n      validateAndImportPlanRows(parseCsvText(text));\n      return;\n    }\n\n    // IMPORT ALL: do not block by file extension. Let SheetJS detect supported spreadsheet formats.\n    const XLSX=await loadSheetJs();\n    const buffer=await file.arrayBuffer();\n    let wb;\n    try{\n      wb=XLSX.read(buffer,{type:"array",cellDates:true});\n    }catch(readErr){\n      throw new Error(`อ่านไฟล์ ${file.name} ไม่สำเร็จ: ไฟล์อาจเสียหาย มีรหัสผ่าน หรือไม่ใช่ Spreadsheet ที่รองรับ`);\n    }'''
if old not in s:
    raise SystemExit('ERROR import extension block not found')
s=s.replace(old,new,1)

# 6) Make import status explicit
old='''  const detail=`โหลดสำเร็จ ${imported.length} Production Job | ${mode} | JOB ID พร้อมใช้งาน`;'''
new='''  const detail=`โหลดสำเร็จทุกแถว ${imported.length} รายการ | IMPORT ALL AS TEXT | ${mode} | JOB ID พร้อมใช้งาน`;'''
if old not in s:
    raise SystemExit('ERROR import detail marker not found')
s=s.replace(old,new,1)

required=[
 '<title>Production Control V1.35 — JOB ID</title>',
 'เลือกจากทั้งหมด 18 Line','Production Plan Master','id="clearPlanFoBtn"',
 'production code','usedJobIds','IMPORT ALL AS TEXT',
 'prod-ok','prod-repair','prod-ng','</html>'
]
for token in required:
    if token not in s:
        raise SystemExit('ERROR missing required token: '+token)
if len(s.encode('utf-8'))<200000:
    raise SystemExit('ERROR file unexpectedly small')

p.write_text(s,encoding='utf-8')
print('PATCH_OK IMPORT ALL PLAN',len(s.encode('utf-8')))
