# Production Control V1.35 — JOB ID

ชุด Source Code สำหรับส่งมอบระบบ Production Control และ Executive Production Dashboard

## ระบบหลัก

- Production Control: `index.html`
- Executive Production Dashboard: `dashboard.html`
- รองรับ LINE01–LINE18
- Production Plan Master / JOB ID / Master FO / Production FO
- Production Input: OK / REPAIR / NG
- Production Log และ Dashboard bridge
- Import Plan จาก Excel/CSV แบบ IMPORT ALL AS TEXT
- Reset / เคลียร์ FO โดยไม่ลบ Production Log

## ไฟล์ใน Repository

- `index.html` — หน้า Production Control หลัก
- `dashboard.html` — Executive Production Dashboard
- `app.js` — ไฟล์จากโครงสร้างเว็บเดิม
- `style.css` — ไฟล์ Style จากโครงสร้างเว็บเดิม
- `HANDOVER_MANIFEST.md` — รายละเอียดชุดส่งมอบ

## การใช้งานบน GitHub Pages

เปิดหน้า Production Control จาก GitHub Pages ของ Repository นี้ และเปิด Dashboard ผ่านปุ่ม Dashboard หรือ `dashboard.html`

GitHub Pages เป็น Static Hosting ดังนั้นข้อมูล Live ระหว่างหลายเครื่องจะไม่ใช้ฐานข้อมูลกลางโดยอัตโนมัติ ในโหมด GitHub Pages ระบบใช้ Browser/LocalStorage สำหรับการเชื่อม Production Log → Dashboard ใน Browser เดียวกัน

## การใช้งานแบบ Server

`index.html` และ `dashboard.html` มี Logic รองรับ Server API เมื่อไม่ได้รันบน `github.io` เช่น `/api/line/state`, `/api/event`, `/api/plan`, `/api/assignments` เป็นต้น แต่ Backend Server/API ต้องติดตั้งแยกต่างหากในสภาพแวดล้อม Server ของบริษัท

## Version

Production Control V1.35 — JOB ID

Handover snapshot: 29 September 2026
