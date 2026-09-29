# HANDOVER MANIFEST

## Project
Production Control V1.35 — JOB ID

## Handover Date
29 September 2026

## Repository
`wasankanlaya79-design/garment-production-web`

## Main Source Files

1. `index.html`
   - Production Control main application
   - LINE01–LINE18
   - Production Plan Master
   - JOB ID / Master FO / Production FO
   - Import Excel/CSV
   - OK / REPAIR / NG input
   - Production Log
   - FO lifecycle / close / new FO
   - Reset / Clear FO without deleting Production Log
   - Dashboard Log Publisher

2. `dashboard.html`
   - Executive Production Dashboard
   - LINE01–LINE18
   - KPI / charts / filters
   - Reads Production Log from Browser LocalStorage in GitHub Pages mode
   - Reads `/api/line/state` in Server mode when available

3. `README.md`
   - System overview and deployment notes

4. `app.js`
   - Legacy/original web structure file retained for source-history completeness

5. `style.css`
   - Legacy/original web structure stylesheet retained for source-history completeness

## Current Functional Rules

- Output = OK + NG
- Repair is recorded separately and does not count as Output
- Production Log/history must remain when starting a new FO
- Reset/Clear FO clears Production Plan Master only; Production Log is retained
- Blank plan rows must not generate fake `JOBxxx-NS-LNA` values
- One active JOB ID must not be opened simultaneously by multiple Lines in Server mode
- GitHub Pages mode is static and does not provide a shared central multi-device database

## Deployment Modes

### GitHub Pages / Static
Use `index.html` and `dashboard.html` directly. Production Log → Dashboard bridge uses Browser LocalStorage on the same browser/origin.

### Company Server
The HTML source contains Server API integration hooks. A separate Backend Server/API installation is required for shared multi-device data, persistent central logs, Excel/OneDrive write operations, and central Line state.

## Delivery Note
This repository ZIP is the complete current GitHub web-source snapshot for handover. Preserve the ZIP unchanged as the source baseline before any future modification.
