---
name: powerbi-pbip
description: Automate Power BI dashboard creation using PBIP format. Generate report.json, model.bim, and visual definitions programmatically with Python. Use when building Power BI dashboards, creating visuals, or working with PBIP/PBIR format.
---

# Power BI PBIP Automation Skill

> สร้าง Power BI Dashboard อัตโนมัติด้วย Python + PBIP format

---

## 🧙‍♂️ Interactive Wizard (บังคับ — ต้องถามก่อนทำงานทุกครั้ง!)

> ⚠️ **กฎสำคัญ**: เมื่อ user เรียกใช้ skill นี้ **ห้ามเริ่มทำงานทันที!**
> ต้องถาม user เป็น step-by-step จนครบทุกข้อก่อน แล้วค่อยเริ่มทำ

### วิธีทำงาน

1. **ถามทีละ step** — อย่าถามทุกอย่างพร้อมกัน ให้ถามเป็นข้อๆ
2. **แนะนำตัวเลือก** — ให้เลือกเป็นข้อ 1, 2, 3... (user แค่พิมพ์เลข)
3. **อธิบายทุกตัวเลือก** — บอกความหมาย, ได้อะไร, เหมาะกับสถานการณ์ไหน
4. **สรุปก่อนทำ** — หลังถามครบทุก step ให้สรุปทั้งหมดให้ user ยืนยัน
5. **ปรับตามบริบท** — ถ้า user ให้ CSV มา ข้ามขั้นตอนที่ไม่จำเป็น

---

### 📋 Step 1: เป้าหมาย (Goal)

> ถามว่า: **"คุณต้องการทำอะไรครับ? เลือกข้อที่ตรงกับความต้องการ:"**

**1. 🆕 สร้าง Dashboard ใหม่**
สร้าง Power BI Dashboard ตั้งแต่เริ่มต้น — ตั้งแต่อ่านข้อมูล CSV, สร้างโมเดลข้อมูล (ตาราง + ความสัมพันธ์), ไปจนถึงออกแบบหน้า Dashboard พร้อม Charts, Cards, Slicers ให้เปิดใน Power BI Desktop ได้เลย

**2. 🔧 แก้ไข Dashboard ที่มีอยู่**
มี PBIP project อยู่แล้วแต่ต้องการปรับแก้ — เช่น เพิ่ม visual ใหม่, แก้ error ที่พบ, เปลี่ยนประเภท chart, อัพเดตข้อมูล, แก้ M expression ที่พัง หรือเพิ่มหน้าใหม่

**3. 🧹 Clean ข้อมูล CSV**
ทำความสะอาดไฟล์ CSV ให้พร้อมใช้งาน — ลบ duplicate, แก้ format ตัวเลข/วันที่, จัดการ null values, ลบ emoji/อักขระพิเศษ, ทำให้ข้อมูลเป็นระเบียบ (รองรับ 57+ เทคนิค cleaning) **โดยไม่ต้องสร้าง dashboard**

**4. ✅ Validate PBIP Project**
ตรวจสอบ PBIP project ที่สร้างแล้วว่ามี error หรือ warning อะไรบ้าง — เช่น M expression ผิด, column ไม่ตรง, visual config เสีย — พร้อม auto-fix ให้อัตโนมัติ

**5. 🎨 ปรับแต่ง Theme/Style**
เปลี่ยนรูปลักษณ์ของ dashboard ที่มีอยู่ — เช่น เปลี่ยนสีธีม (dark/light), เปลี่ยน font, ปรับ layout, เพิ่ม background, ทำให้สวยขึ้น

**6. ❓ อื่นๆ**
มีคำถามหรือความต้องการอื่นๆ เกี่ยวกับ Power BI — อธิบายให้ฟัง แล้วจะแนะนำแนวทางที่เหมาะสม

**ถ้าเลือก 1** → ไปต่อ Step 2
**ถ้าเลือก 2** → ถามว่า project อยู่ที่ไหน แล้วไป Step ที่เกี่ยวข้อง
**ถ้าเลือก 3** → ถาม path ของ CSV แล้วแนะนำ cleaning options
**ถ้าเลือก 4** → ถาม path ของ project แล้วรัน validate
**ถ้าเลือก 5** → ถามว่าต้องการ style แบบไหน
**ถ้าเลือก 6** → ให้ user อธิบาย แล้วแนะนำแนวทาง

---

### 📊 Step 2: แหล่งข้อมูล (Data Source)

> ถามว่า: **"ข้อมูลของคุณอยู่ในรูปแบบไหนครับ?"**

**1. 📄 มีไฟล์ CSV แล้ว**
มีไฟล์ `.csv` อยู่ในเครื่องแล้ว — บอก path ของไฟล์ (เช่น `C:\data\sales.csv`) แล้วระบบจะวิเคราะห์โครงสร้างข้อมูลให้อัตโนมัติ (จำนวน rows, columns, ประเภทข้อมูล, ปัญหาที่พบ)

**2. 📊 มีไฟล์ Excel**
มีไฟล์ `.xlsx` หรือ `.xls` — ระบบจะช่วยแปลงเป็น CSV ก่อนนำเข้า Power BI (เลือกได้ว่าจะใช้ sheet ไหน)

**3. 🗄️ ต่อ Database**
ต้องการดึงข้อมูลจากฐานข้อมูล เช่น SQL Server, PostgreSQL, MySQL — ระบบจะสร้าง M expression สำหรับ connect ตรงจาก Power BI

**4. 🌐 ต่อ API**
ต้องการดึงข้อมูลจาก REST API หรือ Web Service — ระบบจะสร้าง M expression สำหรับ Web.Contents() เพื่อ fetch ข้อมูล

**5. 💡 ยังไม่มีข้อมูล — ช่วยสร้าง Sample Data ให้**
ยังไม่มีข้อมูลจริงแต่อยากลองสร้าง dashboard ก่อน — บอกว่าอยากทำ dashboard เกี่ยวกับอะไร (เช่น Sales, HR, Finance) แล้วระบบจะสร้างข้อมูลตัวอย่างสมจริงให้พร้อมใช้

**6. 📁 มีหลายไฟล์ CSV**
มีหลายไฟล์ CSV ที่ต้องใช้ร่วมกันใน dashboard เดียว — เช่น `customers.csv`, `orders.csv`, `products.csv` ระบบจะวิเคราะห์ทุกไฟล์และสร้าง relationships (ความสัมพันธ์) ระหว่างตารางให้อัตโนมัติ

**เมื่อได้ CSV/ข้อมูลแล้ว → วิเคราะห์อัตโนมัติ:**
- จำนวน rows/columns
- ประเภทข้อมูลแต่ละ column (ตัวเลข, ข้อความ, วันที่)
- ปัญหาที่พบ (null, duplicate, format ผิด)
- แนะนำว่าต้อง clean ข้อมูลก่อนหรือไม่

---

### 🎯 Step 3: ประเภท Dashboard (Dashboard Type)

> ถามว่า: **"คุณต้องการ dashboard แบบไหนครับ?"**

**1. 📈 Executive Overview** — *เหมาะกับ: ผู้บริหาร, CEO, ผู้จัดการ*
Dashboard สรุปภาพรวมของธุรกิจ — มี KPI Cards แสดงตัวเลขสำคัญ (Revenue, Orders, Growth%) พร้อม Chart แนวโน้มรายเดือน/ปี ออกแบบให้ดูเร็ว เข้าใจง่ายใน 5 วินาที ไม่ต้อง drill-down ลึก

**2. 📊 Analytical Deep-Dive** — *เหมาะกับ: นักวิเคราะห์ข้อมูล, Data Analyst*
Dashboard สำหรับวิเคราะห์เชิงลึก — มี Chart หลายประเภท (Line, Bar, Scatter), Slicers สำหรับกรองข้อมูลหลายมิติ, Drill-through เจาะลึกจากภาพรวมไปรายละเอียด เหมาะกับคนที่ต้องการหาคำตอบจากข้อมูล

**3. 📋 Operational Report** — *เหมาะกับ: ทีมปฏิบัติการ, ฝ่ายผลิต*
รายงานข้อมูลละเอียดแบบตาราง — มี Tables, Matrix (Pivot Table) แสดงข้อมูลทุกแถว filter ได้ตามหลายเงื่อนไข เหมาะกับงานประจำวันที่ต้องดูข้อมูลรายรายการ

**4. 🎯 KPI Scorecard** — *เหมาะกับ: ทุกระดับ*
Dashboard เน้นวัดผลประเมิน — มี Gauge (เข็มวัด), KPI Cards พร้อมเทียบเป้าหมาย (Target vs Actual), สัญญาณไฟ 🔴🟡🟢 บอกสถานะ เหมาะกับ OKR, KPI Tracking

**5. 🗺️ Geographic Dashboard** — *เหมาะกับ: Sales, Logistics, การตลาด*
Dashboard แสดงข้อมูลบนแผนที่ — วิเคราะห์ตามภูมิภาค, จังหวัด, ประเทศ พร้อม Map visual, เปรียบเทียบพื้นที่ เหมาะกับข้อมูลที่มี location

**6. 🔍 Data Explorer** — *เหมาะกับ: Data Team, QA*
Dashboard สำหรับสำรวจข้อมูลอิสระ — มี Slicers เยอะ, ตารางที่ sort/filter ได้ทุก column, ไม่มี chart ที่ตายตัว ให้ผู้ใช้จัดการเองตามต้องการ

**7. 🤖 ให้ AI แนะนำ**
ไม่แน่ใจว่าแบบไหนดี — ระบบจะวิเคราะห์จาก columns และประเภทข้อมูลที่มี แล้วแนะนำประเภท dashboard + visuals ที่เหมาะสมที่สุดให้

---

### 🎨 Step 4: จำนวนหน้า & Visual (Pages & Visuals)

> ถามว่า: **"ต้องการกี่หน้าครับ? แต่ละแบบมีความเหมาะสมต่างกัน:"**

**1. 📄 1 หน้า (Simple)** — *4-6 visuals*
Dashboard หน้าเดียวสรุปทุกอย่าง — เหมาะกับข้อมูลไม่ซับซ้อน หรือต้องการ overview เร็วๆ ไม่ต้องเปลี่ยนหน้า

**2. 📑 2-3 หน้า (Standard)** — *6-8 visuals/หน้า*
แบ่งเนื้อหาเป็นหมวดหมู่ — เช่น หน้า 1: Overview, หน้า 2: Details, หน้า 3: Trends เหมาะกับ dashboard ทั่วไปที่ต้องการจัดระเบียบ

**3. 📚 4-5 หน้า (Comprehensive)** — *6-10 visuals/หน้า*
Dashboard ครบถ้วนสมบูรณ์ — ครอบคลุมทุกมิติของข้อมูล เช่น Sales → Products → Customers → Geography → Time Analysis เหมาะกับโปรเจกต์ใหญ่

**4. 📖 6+ หน้า (Enterprise)** — *กำหนดเอง*
Dashboard ระดับองค์กร — สำหรับข้อมูลหลายแผนก, หลาย department, ต้องการ drill-through ข้ามหน้า บอกจำนวนที่ต้องการ

**5. 🤖 ให้ AI จัดให้**
ระบบจะวิเคราะห์จากจำนวน columns, ประเภทข้อมูล และ dashboard type ที่เลือกไว้ แล้วแนะนำจำนวนหน้าและ visuals ที่เหมาะสม

**หลังเลือก → ถามเพิ่ม:**
- "ต้องการ **Slicer** (ตัวกรอง dropdown ที่ user คลิกเลือกเพื่อ filter ข้อมูล) ไหมครับ? ถ้าใช่ กรองด้วย column ไหนบ้าง? เช่น ปี, หมวดหมู่, ภูมิภาค"
- "ต้องการ **เปรียบเทียบช่วงเวลา** ไหมครับ? เช่น YoY (เทียบปีต่อปี), MoM (เดือนต่อเดือน), QoQ (ไตรมาสต่อไตรมาส)"

---

### 🧹 Step 5: การ Clean ข้อมูล (Data Cleaning)

> ถ้าพบปัญหาใน CSV → ถามว่า: **"พบปัญหาในข้อมูล ต้องการให้ clean ไหมครับ?"**

**1. 🧹 Clean ทั้งหมด (แนะนำ)**
แก้ทุกปัญหาที่พบอัตโนมัติ — ลบ duplicate, แก้ format ตัวเลข, จัดการ null, normalize วันที่ ฯลฯ ใช้ 57+ เทคนิคที่มีอยู่ทั้งหมด (**เหมาะกับคนที่ไม่อยากเลือกเอง**)

**2. ✅ เลือก clean เฉพาะบางอย่าง**
ดูรายการปัญหาที่พบทั้งหมดก่อน แล้วเลือกเฉพาะข้อที่ต้องการแก้ — เหมาะกับคนที่ต้องการควบคุมว่าข้อมูลจะถูกแก้ตรงไหนบ้าง (เช่น อยากลบ duplicate แต่ไม่อยากแก้ format วันที่)

**3. ❌ ไม่ต้อง clean**
ใช้ข้อมูลตามที่เป็นอยู่ — **ระวัง**: ข้อมูลที่มีปัญหาอาจทำให้ dashboard แสดงผลผิดหรือมี error

**4. 🔍 ดูรายละเอียดก่อน**
แสดง Data Profile ก่อนตัดสินใจ — จะเห็นสถิติละเอียดของทุก column (จำนวน null, unique values, min/max, format ที่พบ) เพื่อให้ตัดสินใจได้ดีขึ้น

**ถ้าเลือก 2 → แสดงรายการปัญหาที่พบ พร้อมอธิบาย:**
```
พบปัญหาต่อไปนี้:
  [ ] 1. 🔤 Null/Blank — มี cells ว่าง 245 จุด
       (ถ้าไม่แก้: chart อาจแสดงช่องว่าง หรือคำนวณผิดเพราะนับ blank)
  [ ] 2. 📝 Honorific — ชื่อมีคำนำหน้า (Mr., Mrs., Dr.) 50 rows
       (ถ้าไม่แก้: "Mr. John" กับ "John" จะถูกนับเป็นคนละคน)
  [ ] 3. 🔢 Currency Symbols — ตัวเลขมีสัญลักษณ์ ($, ฿) 120 cells
       (ถ้าไม่แก้: PBI จะอ่านเป็น text แทนตัวเลข ทำให้ SUM/AVG ไม่ได้)
  [ ] 4. 📅 Date Format — วันที่หลายรูปแบบ (DD/MM/YYYY, YYYY-MM-DD)
       (ถ้าไม่แก้: PBI อาจตีความ 01/02/2024 เป็น Jan 2 หรือ Feb 1 ผิด)
  [ ] 5. 🔁 Duplicates — มีแถวซ้ำ 15 แถว
       (ถ้าไม่แก้: ยอดรวมจะสูงกว่าความเป็นจริง)
  เลือกข้อที่ต้องการ (เช่น 1,3,5):
```

---

### 🎨 Step 6: สไตล์ & ธีม (Theme & Style)

> ถามว่า: **"ต้องการ theme แบบไหนครับ? แต่ละแบบให้ความรู้สึกต่างกัน:"**

**1. 🌑 Dark Mode**
พื้นหลังสีเข้ม (เทาเข้ม/ดำ) ตัวอักษรและ chart สีสว่าง — ดูหรูหรา ทันสมัย ลดแสงจ้าหน้าจอ เหมาะกับ presentation บนจอใหญ่หรือห้องประชุมมืด

**2. ⚪ Light Mode**
พื้นหลังสีขาว/เทาอ่อน ตัวอักษรสีเข้ม — สะอาดตา อ่านง่าย เหมาะกับ print เป็นกระดาษ หรือส่ง email เป็น PDF (**ค่าเริ่มต้นของ Power BI**)

**3. 🎨 Corporate**
สีตามแบรนด์องค์กร — จะถามสี primary/secondary ของบริษัท (เช่น สีน้ำเงิน + เงิน ของธนาคาร) แล้วสร้าง theme ที่สอดคล้อง เหมาะกับ dashboard ที่ต้องนำเสนอลูกค้าหรือผู้บริหาร

**4. 🌈 Colorful**
สีสดใสหลากหลาย — แต่ละ chart ใช้ palette สีต่างกัน ดูสนุก เหมาะกับ dashboard ที่ต้องแยกหมวดหมู่ชัดเจนหรือ marketing presentation

**5. 📊 Minimal**
เรียบง่าย เน้นข้อมูลมากกว่าตกแต่ง — สีเทา + 1-2 accent colors, ไม่มี background ฉูดฉาด, ไม่มี shadow เหมาะกับ data-driven team ที่ต้องการดูตัวเลขชัดๆ

**6. 🤖 ให้ AI จัดให้**
ระบบเลือก theme ที่เหมาะกับประเภท dashboard และข้อมูล — เช่น Financial → Dark + Blue, Marketing → Colorful, Healthcare → Light + Green

---

### ✅ Step 7: สรุป & ยืนยัน (Summary & Confirm)

> แสดงสรุปทั้งหมดก่อนเริ่มทำงาน:

```
📋 สรุปความต้องการ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 เป้าหมาย:    สร้าง Dashboard ใหม่
📊 ข้อมูล:       sales_data.csv (5,000 rows × 12 cols)
📈 ประเภท:      Executive Overview
                → KPI Cards แสดงยอดขาย + กำไร
                → Chart แนวโน้มรายเดือน
                → เปรียบเทียบ target vs actual
📄 จำนวนหน้า:   3 หน้า (Overview / Products / Trends)
🧹 Data Clean:  Clean ทั้งหมด (null 245, duplicates 15, currency 120)
🎨 Theme:       Dark Mode (พื้นเข้ม สีสดใส)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ต้องการเริ่มทำเลยไหมครับ?
  1. ✅ เริ่มเลย!
  2. ✏️ แก้ไขบางอย่าง (บอกว่าต้องการแก้อะไร)
  3. 🔙 เริ่มถามใหม่ตั้งแต่ต้น
```

---

### 🚀 Shortcut: ถ้า user ให้ข้อมูลมาครบแล้ว

> ถ้า user ส่ง CSV path + บอกว่าต้องการอะไรชัดเจนแล้ว → **ข้ามไป Step 7 (สรุป) ได้เลย**
> แต่ยังต้องแสดงสรุปและให้ยืนยันก่อนเริ่มทำงาน!

**ตัวอย่างที่ข้ามได้:**
```
User: "สร้าง dashboard จาก sales.csv ให้หน่อย dark mode 3 หน้า"
→ ข้ามไป Step 7 สรุป + ถามเพิ่มเฉพาะสิ่งที่ขาด (เช่น ประเภท dashboard)
```

**ตัวอย่างที่ต้องถามทุก step:**
```
User: "อยากทำ dashboard"
→ ถามทุก step ตั้งแต่ Step 1
```

## Companion Files

| File | เนื้อหา |
|------|--------|
| [SKILL.md](SKILL.md) | Technical reference — PBIP format, JSON structure, visual types |
| [USE_CASES.md](USE_CASES.md) | **15 อุตสาหกรรม**, 25+ dashboard blueprints, 100+ KPIs + DAX |
| [DATA_CLEANING.md](DATA_CLEANING.md) | 🆕 **Data Cleaning** — 65 industries, 2050+ patterns, M + Python + DAX + SQL + Polars (🏆 **COMPLETE ENCYCLOPEDIA v8**) |
| [ERROR_REFERENCE.md](ERROR_REFERENCE.md) | 🏆 **Error & Troubleshooting** — 1,620+ errors, **230 categories**, Privacy/Copilot/SemPy/Visuals/Params |
| [generate.py](generate.py) | **Python script** — 14 visual generators + auto CSV→dashboard |

> 💡 ใช้ `USE_CASES.md` เพื่อหา blueprint, `ERROR_REFERENCE.md` เพื่อแก้ปัญหา, แล้วกลับมาใช้ SKILL.md เพื่อสร้าง JSON

---

## 🛡️ Mandatory PBIP Validation (ต้องทำทุกครั้ง!)

> ⚠️ **กฎบังคับ**: หลังสร้าง PBIP project ด้วย `generate.py` ต้องเรียก `validate_and_fix()` **ก่อน** เปิดใน Power BI Desktop เสมอ!

### วิธีใช้งาน

```python
import sys
sys.path.insert(0, r'path/to/skills/powerbi-pbip')
from generate import validate_and_fix

# ✅ ตรวจสอบ + auto-fix (แนะนำ)
result = validate_and_fix(r'path/to/PBIP_Project')
# จะรัน validate + fix loop สูงสุด 5 รอบจนกว่าจะ 0 errors

# 📊 ตรวจสอบอย่างเดียว (ไม่แก้ไข)
from generate import validate_pbip
result = validate_pbip(r'path/to/PBIP_Project')
print(f"Errors: {len(result['errors'])}")
print(f"Warnings: {len(result['warnings'])}")
```

### Validation Error Codes

#### Structure & Config Errors

| Code | ความรุนแรง | ปัญหา | Auto-Fix? |
|------|-----------|-------|-----------|
| **STRUCT-001~006** | ❌/⚠️ | Missing/invalid .pbip file, names too long | ✅ partial |
| **RPT-001~019** | ❌/⚠️ | Missing report files, invalid config, section issues, duplicate pages, out-of-bounds dimensions | ✅ partial |
| **RPT-013** | ❌ Error | Report config missing `models` array → visuals ไม่ bind data | ✅ |
| **RPT-016** | ❌ Error | Invalid report-level filters JSON | ❌ |
| **RPT-017** | ⚠️ Warning | report.json > 5MB → PBI Desktop จะ load ช้า | ❌ |
| **ENC-001** | ❌ Error | File not UTF-8 encoded | ✅ |
| **THEME-001** | ⚠️ Warning | Custom theme missing | ❌ **NEW** |
| **BKM-001~002** | ❌/⚠️ | Invalid bookmarks, Ghost bookmarks | ❌ **NEW** |

#### Model & Data Errors

| Code | ความรุนแรง | ปัญหา | Auto-Fix? |
|------|-----------|-------|-----------|
| **MDL-001~025** | ❌/⚠️ | Missing model files, invalid types, broken relationships | ✅ partial |
| **MDL-034** | 🔥 Critical | Double-escaped quotes ใน M expression (`"Token ',' expected"`) | ✅ |
| **MDL-035** | ⚠️ Warning | Unbalanced braces / missing commas ใน M | ❌ |
| **MDL-036** | ⚠️ Warning | CSV import ขาด `Table.ReplaceErrorValues` (inf/nan) | ✅ |
| **MDL-037** | ⚠️ Warning | Missing `item.config.json` ใน SemanticModel | ✅ **NEW** |
| **MDL-038** | ⚠️ Warning | Missing `item.config.json` ใน Report | ✅ **NEW** |
| **MDL-039** | ❌ Error | DAX measure references ถึง table ที่ไม่มีอยู่ | ❌ **NEW** |
| **MDL-040** | ⚠️ Warning | Relationship column type mismatch (เช่น string → int64) | ❌ **NEW** |
| **MDL-041** | ℹ️ Info | Orphan table — ไม่มี visual ใดใช้ | ❌ **NEW** |
| **MDL-042** | ⚠️ Warning | Absolute CSV file path → ย้าย project จะพัง | ❌ **NEW** |
| **MDL-043** | ❌ Error | Malformed RLS role filter expression | ❌ **NEW** |
| **MDL-044** | ❌ Error | Multiple active relationships exist between two tables | ❌ **NEW** |
| **MDL-045** | ❌ Error | Measure references itself (circular dependency) | ❌ **NEW** |
| **MDL-046** | ❌ Error | `sortByColumn` references a non-existent column | ❌ **NEW** |
| **MDL-048** | ℹ️ Info | Geographic column lacks `dataCategory` | ❌ **NEW** |

#### Visual Errors

| Code | ความรุนแรง | ปัญหา | Auto-Fix? |
|------|-----------|-------|-----------|
| **VIS-001~035** | ❌/⚠️ | Missing sections, invalid configs, broken queries | ✅ partial |
| **VIS-036** | ⚠️ Warning | Empty projections / visual too small | ✅ |
| **VIS-037** | 🔥 Critical | Missing required projection role → chart BLANK | ❌ |
| **VIS-040** | 🔥 Critical | Column Property เป็น dict → **Missing_References!** | ✅ |
| **VIS-043** | ❌ Error | Config parses แต่ `singleVisual` ว่าง → visual blank | ❌ **NEW** |
| **VIS-044** | ⚠️ Warning | dataTransforms ขาด `projectionActiveItems` | ❌ **NEW** |
| **VIS-045** | ⚠️ Warning | Slicer ไม่มี `objects.data` → dropdown ไม่ขึ้น | ❌ **NEW** |
| **VIS-046** | ⚠️ Warning | Visual ใช้ table ที่ไม่มี data partition | ❌ **NEW** |
| **VIS-047** | ⚠️ Warning | Visual > 50 ตัวต่อ page → performance ช้า | ❌ **NEW** |
| **VIS-048** | ❌ Error | Visual is placed completely off-canvas | ❌ **NEW** |
| **VIS-049** | ❌ Error | Visual specifies non-existent `parentGroupName` | ❌ **NEW** |
| **VIS-050** | ❌ Error | Duplicate visual ID on the same page | ❌ **NEW** |
| **GENQ-001** | 🔥 Critical | Double-wrapped Column/Aggregation → **report จะไม่ load!** | ❌ |
| **GEN-001~014** | ❌/⚠️ | Config not stringified, missing dimensions | ✅ partial |

### Common Pitfalls (สาเหตุ error ที่พบบ่อย)

| ปัญหา | สาเหตุ | วิธีป้องกัน |
|-------|--------|-----------| 
| **Missing_References** | `make_table()` ได้รับ dict columns `{'col':'name'}` แทน string | ใช้ `make_table` ใหม่ที่รองรับทั้ง 2 formats |
| **Token ',' expected** | Double-escaped quotes ใน M expression | ใช้ `build_m_expression()` จาก generate.py |
| **',' cannot precede 'in'** | Trailing comma ก่อน `in` ใน M let-block | Step สุดท้ายก่อน `in` ห้ามมี comma |
| **CustomVisualNotFound** | visualType ไม่ใช่ built-in PBI type | ใช้ `VISUAL_TYPE_ALIASES` จาก generate.py |
| **funnelChart not found** 🆕 | `funnelChart` **ไม่ใช่ built-in** ใน PBIP format ต้องใช้ clusteredBarChart แทน | หลีกเลี่ยง `make_funnel()` ใน PBIP projects |
| **Visuals ว่างเปล่า** | ไม่มี `models` array ใน report config | `make_report_json()` ใส่ให้อัตโนมัติแล้ว |
| **inf/nan → "Error" cells** | CSV มี infinity values (0÷0) | `build_m_expression()` ใส่ `ReplaceErrorValues` ให้แล้ว |
| **Render error** | Property/NativeReferenceName เป็น dict | ใช้ validator ตรวจก่อนเปิด |
| **"The supplied file path must be a valid absolute path"** 🆕 | M expression ใช้ relative path ใน `File.Contents()` เช่น `..\\data.csv` | **Power BI `File.Contents()` ต้องใช้ absolute path เสมอ** เช่น `C:\\Users\\...\\data.csv` — relative path, UNC path ที่ไม่มีอยู่ หรือ path ว่างจะ error ตอน Load |
| **\"Column wasn't found\" (spaces)** 🆕 | CSV header มี trailing/leading space เช่น `Sales Channel ` | `build_m_expression()` ใส่ `Text.Trim` + BOM/invisible char cleaning ให้อัตโนมัติ |
| **"Column wasn't found" (junk rows)** 🆕 | CSV มีแถว junk/metadata ก่อน header จริง เช่น `## REPORT EXPORT WIZARD ##`, `System Message:` | ใช้ `skip_rows` parameter ใน table dict → `build_m_expression()` จะใช้ **Lines.FromBinary approach** (ตัด junk lines ก่อน parse CSV) แทน `Table.Skip` เพราะ `Csv.Document + Table.Skip` ทำให้ PQ นับ column ผิด |
| **"Column wasn't found" (delimiter)** 🆕 | CSV ใช้ delimiter อื่นเช่น pipe `\|` หรือ `;` | ใช้ `delimiter` parameter ใน table dict |
| **"Column wasn't found" (BOM/invisible chars)** 🆕 | CSV header มี BOM (U+FEFF), ZWNJ (U+200C), ZWS (U+200B) ที่มองไม่เห็น — model.bim กับ PQ ได้ชื่อ column ต่างกัน | `build_m_expression()` ใส่ `CleanedHeaders` step ที่ลบ BOM+invisible chars อัตโนมัติ + ใช้ `read_csv_headers()` เพื่อ auto-detect ชื่อ column จาก CSV ไฟล์จริง |
| **"Column wasn't found" (ChangedTypes/CleanedErrors)** 🆕 | M expression มี `ChangedTypes` หรือ `CleanedErrors` step ที่ hardcode column names — ถ้า PQ ให้ชื่อ column ต่างจากที่คาด (เช่น ติด BOM, suffix, duplicate names) จะ error | เมื่อ `skip_rows > 0`, `build_m_expression()` จะ **ไม่** generate `ChangedTypes`/`CleanedErrors` — ลงท้ายที่ `CleanedHeaders` แทน |
| **PBI Desktop lock file ทำให้ rebuild ล้มเหลว** 🆕 | PBI Desktop เปิดค้าง → `_write_pbip_project` เขียน model.bim ไม่ได้ → ไฟล์เก่ายังอยู่ | **ปิด PBI Desktop ก่อน rebuild** หรือใช้ script เขียน model.bim โดยตรง |
| **"Duplicate value" (auto-fix overwrites custom M)** 🆕 | Custom M steps (`Table.Distinct`, `Table.TransformColumns`, `Table.SelectRows`) ที่ใส่ผ่าน `m_expression` ถูก `validate_and_fix()` เขียนทับ เมื่อ rebuild M ให้มี `ChangedTypes`+`CleanedErrors` | ใช้ `inject_m_steps()` หรือ `validate_fix_and_clean()` เพื่อ inject custom steps **หลัง** auto-fix เสร็จ |
| **"Duplicate value" (case-sensitive dedup)** 🆕 | `Table.Distinct` เป็น case-sensitive — 'Widget Alpha' ≠ 'WIDGET ALPHA' ทำให้ dedup ไม่ลบ row ที่ต่างแค่ case | ใช้ `m_clean_name()` เพื่อ `Text.Lower()` ก่อน `Table.Distinct` |
| **"Duplicate value" (homoglyphs/invisible chars)** 🆕 | Key column มี Cyrillic chars (С vs C), ZWNJ, ZWS, non-breaking space ปนอยู่ — มองเหมือนกันแต่เป็นคนละ value | ใช้ `m_clean_key()` เพื่อ extract เฉพาะตัวเลขแล้วสร้าง ID ใหม่ |

> 🔑 **Best Practice**: ใช้ `read_csv_headers(csv_path, skip_rows, delimiter)` จาก generate.py เพื่อ auto-detect column names แทนการ hardcode — ป้องกัน mismatch ทุกกรณี!
> 
> ⚠️ **สำคัญ**: เมื่อ CSV มี junk rows (`skip_rows > 0`), **อย่าใส่ `ChangedTypes` หรือ `CleanedErrors`** ใน M expression — ให้จบที่ `CleanedHeaders` พอ!

### Validation Workflow (บังคับ)

```
1. สร้าง PBIP project → python build_script.py
2. ✅ เรียก validate_and_fix() → ตรวจ + auto-fix
3. 🧹 inject_m_steps() / validate_fix_and_clean() → inject custom cleaning/dedup (ถ้า CSV มี dirty data)
4. ✅ ตรวจผลลัพธ์ → 0 errors
5. เปิดใน Power BI Desktop
```

> 🔥 **ห้ามข้ามขั้นตอนที่ 2-4!** การเปิด PBIP ที่มี error จะทำให้ Power BI crash หรือแสดงผลผิด
>
> ⚠️ **สำคัญ**: ถ้าต้อง clean data (dedup, filter headers, normalize keys) ต้องทำ **หลัง** `validate_and_fix()` เสมอ! เพราะ auto-fix จะเขียนทับ custom M steps

### 🧹 Data Cleaning M Utilities (สำหรับ dirty CSV)

> ⚠️ **ปัญหา**: `validate_and_fix()` เพิ่ม `ChangedTypes` + `CleanedErrors` ให้ทุกตาราง แต่จะ **rebuild M expression ใหม่** ทำให้ custom M steps ที่ใส่ผ่าน `m_expression` ถูกเขียนทับ!
>
> ✅ **วิธีแก้**: ใช้ `inject_m_steps()` หรือ `validate_fix_and_clean()` เพื่อ inject custom steps **หลัง** auto-fix

#### Functions ใน generate.py

| Function | ใช้ทำอะไร |
|----------|----------|
| `inject_m_steps(bim_path, table, steps, final_step)` | Inject M steps เข้าไปใน model.bim ของตารางที่ระบุ |
| `m_clean_key(last_step, col, prefix)` | สร้าง M code ดึงเฉพาะตัวเลข + ใส่ prefix (เช่น 'CUST-001') |
| `m_clean_name(last_step, col)` | สร้าง M code normalize ชื่อ (lowercase + trim + เฉพาะ a-z, 0-9, space) |
| `validate_fix_and_clean(project_dir, project_name, clean_rules)` | All-in-one: validate → fix → inject clean rules |

#### Quick Example: inject_m_steps (Manual)

```python
from generate import (
    validate_and_fix, inject_m_steps, m_clean_key, m_clean_name
)
import os

# 1. Build and validate normally
results = validate_and_fix(OUTPUT_DIR)

# 2. Inject custom cleaning AFTER auto-fix
bim_path = os.path.join(OUTPUT_DIR, f'{PROJECT_NAME}.SemanticModel', 'model.bim')

# Clean Customers: extract digits → CUST-xxx, filter headers, dedup
inject_m_steps(bim_path, 'Customers', [
    m_clean_key('CleanedErrors', 'ID', 'CUST-'),
    '  RemovedHeaders = Table.SelectRows(Cleaned_ID, each [ID] <> "CUST-"),',
    '  Deduped = Table.Distinct(RemovedHeaders, {"ID"})',
], 'Deduped')

# Clean Products: lowercase normalize, filter headers, dedup
inject_m_steps(bim_path, 'Products', [
    m_clean_name('CleanedErrors', 'Product_Name'),
    '  RemovedHeaders = Table.SelectRows(Cleaned_Product_Name, each [Product_Name] <> "product name"),',
    '  Deduped = Table.Distinct(RemovedHeaders, {"Product_Name"})',
], 'Deduped')
```

#### Quick Example: validate_fix_and_clean (All-in-One)

```python
from generate import validate_fix_and_clean

results = validate_fix_and_clean(
    OUTPUT_DIR, PROJECT_NAME,
    clean_rules=[
        {
            'table': 'Customers',
            'clean_keys': [('ID', 'CUST-')],
            'filter_header_col': 'ID',
            'filter_header_value': 'CUST-',
            'dedup_col': 'ID',
        },
        {
            'table': 'Products',
            'clean_names': ['Product_Name'],
            'filter_header_col': 'Product_Name',
            'filter_header_value': 'product name',
            'dedup_col': 'Product_Name',
        },
        {
            'table': 'Sales',
            'clean_keys': [('TXN_ID', 'TXN-'), ('Customer_ID', 'CUST-')],
            'clean_names': ['Product'],
            'filter_header_col': 'TXN_ID',
            'filter_header_value': 'TXN-',
            # ไม่ใส่ dedup_col → fact table ไม่ต้อง dedup
        },
        {
            'table': 'Returns',
            'clean_keys': [('Return_ID', 'RET-'), ('Original_TXN', 'TXN-'), ('Customer', 'CUST-')],
            'clean_names': ['Product'],
            'filter_header_col': 'Return_ID',
            'filter_header_value': 'RET-',
            'dedup_col': 'Return_ID',
        },
    ]
)
```

#### clean_rules Schema

| Field | Type | Required | คำอธิบาย |
|-------|------|----------|----------|
| `table` | str | ✅ | ชื่อตาราง เช่น `'Customers'` |
| `clean_keys` | list[tuple] | ❌ | `[(col, prefix), ...]` — extract digits + prefix |
| `clean_names` | list[str] | ❌ | `[col, ...]` — lowercase + trim + filter chars |
| `filter_header_col` | str | ❌ | Column ที่ใช้ filter embedded headers |
| `filter_header_value` | str | ❌ | ค่าที่บอกว่าเป็น header row (rows ที่ col == value จะถูกลบ) |
| `dedup_col` | str | ❌ | Column ที่ใช้ `Table.Distinct` (ไม่ใส่ = ไม่ dedup) |

> 💡 **เมื่อไหร่ต้องใช้?** เมื่อ CSV มี:
> - Duplicate key values (เช่น `CUST-044` ซ้ำ)
> - Embedded header rows (header ซ้ำอยู่กลาง data)
> - Inconsistent key formats (เช่น `C-028`, `CUST-028`, `cust028`)
> - Case-sensitive conflicts (เช่น `Widget Alpha` vs `WIDGET ALPHA`)
> - Homoglyphs / invisible chars ใน keys

### 🤖 PBI Desktop Auto-Generated Content

> ⚠️ **ไม่ต้องสร้างเอง!** PBI Desktop สร้างสิ่งเหล่านี้อัตโนมัติเมื่อเปิด PBIP:

| รายการ | หน้าที่ |
|--------|--------|
| `.gitignore` | Ignore `cache.abf` + `localSettings.json` |
| `.pbi/cache.abf` 🆕 | Compressed data cache (~6MB) |
| `.pbi/localSettings.json` 🆕 | Security bindings (machine-specific, มี encrypted signature) |
| `.pbi/editorSettings.json` 🆕 | `autodetectRelationships`, `parallelQueryLoading`, `typeDetectionEnabled`, `relationshipImportEnabled` |
| `diagramLayout.json` | ตำแหน่ง tables ใน Model View (version 1.1.0) |
| `DateTableTemplate` + `LocalDateTable` × N | Auto-date tables (1 ตัวต่อ Date column) |
| `dataAccessOptions.returnErrorValuesAsNull` | แปลง error→null อัตโนมัติ |
| `dataAccessOptions.legacyRedirects` 🆕 | Legacy redirect support |
| `sourceQueryCulture` 🆕 | เพิ่ม `"sourceQueryCulture": "en-US"` ในระดับ model |
| `PBI_QueryOrder` annotation | Query order เช่น `["Table1","Table2"]` |
| `__PBI_TimeIntelligenceEnabled` annotation 🆕 | Time Intelligence = `"1"` |
| `PBI_ProTooling` annotation 🆕 | DevMode = `["DevMode"]` |
| `lineageTag` 🆕 | UUID สำหรับ **ทุก** column, measure, table (tracking ใน Fabric) |
| `summarizeBy` 🆕 | Auto-set `"none"` สำหรับ string columns ที่ไม่ควร summarize |
| `compatibilityLevel` upgrade 🆕 | PBI Desktop อาจ upgrade เช่น 1567→**1600** |
| Report config `version` 🆕 | PBI Desktop อาจ downgrade จาก `5.70`→`5.66` |

## Overview

Power BI Desktop รองรับ **PBIP (Power BI Project)** format ที่เก็บทุกอย่างเป็น JSON text files — สามารถสร้างด้วย Python ได้โดยไม่ต้องเปิด Power BI Desktop

## Prerequisites

- Power BI Desktop (latest)
- Enable preview features:
  - `Options > Preview Features > Power BI Project (.pbip) save option`
  - `Options > Preview Features > Store reports using enhanced metadata format`
- Python 3.8+ with `pandas`

---

## 📋 Phase 1: Requirement Gathering (ก่อนเริ่มทำ)

> ⚠️ **ต้องทำก่อนเปิด Power BI เสมอ** — ป้องกันการทำงานซ้ำและ dashboard ที่ไม่ตรงความต้องการ

### Step 1: ระบุ KPIs

| คำถามที่ต้องถาม | ตัวอย่างคำตอบ | ผลลัพธ์ |
|---------------|-------------|--------|
| เป้าหมายของรายงานคืออะไร? | ติดตามยอดขายรายเดือน | กำหนด Measures หลัก |
| ตัวชี้วัดสำคัญมีอะไรบ้าง? | Revenue, Orders, Avg Order Value | สร้าง KPI Cards |
| เปรียบเทียบอะไรกับอะไร? | ยอดขายปีนี้ vs ปีที่แล้ว | ต้องใช้ Time Intelligence |
| ต้องเจาะลึก (drill-down) อะไร? | จากประเทศ → จังหวัด → สาขา | ต้องสร้าง Hierarchy |

### Step 2: กำหนดกลุ่มเป้าหมาย

| กลุ่มผู้ใช้ | ต้องการ | Dashboard Style |
|-----------|--------|----------------|
| **ผู้บริหาร (Executive)** | ภาพรวม ตัวเลขสำคัญ ดูเร็ว | 4-6 KPI Cards + 1-2 Charts |
| **ผู้จัดการ (Manager)** | วิเคราะห์แนวโน้ม เปรียบเทียบ | Charts + Slicers + Drill-through |
| **นักวิเคราะห์ (Analyst)** | ข้อมูลละเอียด กรองได้หลายมิติ | Tables + Matrix + Complex Filters |
| **ทีมปฏิบัติการ (Operations)** | ข้อมูล real-time สถานะปัจจุบัน | DirectQuery + Auto-refresh |

### Step 3: สำรวจแหล่งข้อมูล

| สิ่งที่ต้องตรวจสอบ | ทำไม |
|------------------|------|
| แหล่งข้อมูลอยู่ที่ไหน? (Excel/SQL/API/SharePoint) | เลือก connection mode |
| สิทธิ์การเข้าถึงพร้อมหรือยัง? | ป้องกัน delay |
| ข้อมูลอัพเดตบ่อยแค่ไหน? (รายวัน/รายชั่วโมง) | เลือก Import vs DirectQuery |
| ขนาดข้อมูลเท่าไหร่? | วางแผน data reduction |
| ต้องรวมข้อมูลจากกี่แหล่ง? | วางแผน Merge/Append |

### 💡 Pro-Tips: Requirement Gathering

| Pro-Tip | รายละเอียด |
|---------|----------|
| **Actionable Insight** | อย่าถามแค่ "อยากเห็นอะไร" — ถามว่า **"เห็นแล้วจะทำอะไรต่อ?"** เพื่อออกแบบรายงานที่ช่วยตัดสินใจจริง |
| **Wireframe/Mockup** | ร่างแบบรายงานคร่าวๆ ใน PowerPoint หรือกระดาษก่อนเริ่มทำจริง — ประหยัดเวลาแก้ไขภายหลัง 50%+ |
| **Data Dictionary** | สร้างเอกสารอธิบาย column แต่ละตัว — ป้องกันความเข้าใจผิดเรื่อง "Revenue คือ Net หรือ Gross" |

---

## PBIP Folder Structure

```
📄 ProjectName.pbip              ← Entry point (double-click)
📁 ProjectName.Report/
   📄 .platform                  ← Metadata (type: Report)
   📄 definition.pbir            ← Links to SemanticModel (v4.0)
   📄 report.json                ← ⭐ ALL pages + visuals
📁 ProjectName.SemanticModel/
   📄 .platform                  ← Metadata (type: SemanticModel)
   📄 definition.pbism           ← Model config (v4.2)
   📄 model.bim                  ← ⭐ Tables, columns, measures, M queries
```

> **IMPORTANT**: PBI Desktop uses **PBIR-Legacy** format (single `report.json`) NOT the newer PBIR folder structure. Always use single-file format.

---

## Key Files

### 1. `.pbip` (Project Entry Point)

```json
{
  "version": "1.0",
  "artifacts": [{"report": {"path": "ProjectName.Report"}}],
  "settings": {"enableAutoRecovery": true}
}
```

### 2. `definition.pbir` (Report ↔ Model Link)

```json
{
  "version": "4.0",
  "datasetReference": {
    "byPath": {"path": "../ProjectName.SemanticModel"}
  }
}
```

### 3. `definition.pbism` (Model Config)

```json
{"version": "4.2", "settings": {}}
```

### 4. `.platform` (Metadata)

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {"type": "Report", "displayName": "ProjectName"},
  "config": {"version": "2.0", "logicalId": "<UUID>"}
}
```

---

## report.json Structure

```json
{
  "config": "<stringified JSON — theme + settings>",
  "layoutOptimization": 0,
  "sections": [
    {
      "config": "{}",
      "displayName": "Page Name",
      "displayOption": 1,
      "filters": "[]",
      "height": 720.0,
      "width": 1280.0,
      "name": "<20-char hex ID>",
      "ordinal": 0,
      "visualContainers": [...]
    }
  ]
}
```

### Report Config (stringified)

```json
{
  "version": "5.70",
  "themeCollection": {
    "baseTheme": {
      "name": "CY24SU11",
      "version": {"visual": "2.6.0", "report": "3.1.0", "page": "2.3.0"},
      "type": 2
    }
  },
  "activeSectionIndex": 0,
  "defaultDrillFilterOtherVisuals": true,
  "linguisticSchemaSyncVersion": 2,
  "settings": {
    "useNewFilterPaneExperience": true,
    "allowChangeFilterTypes": true,
    "useStylableVisualContainerHeader": true,
    "queryLimitOption": 6,
    "useEnhancedTooltips": true,
    "exportDataMode": 1,
    "useDefaultAggregateDisplayName": true
  }
}
```

---

## Visual Container Format

Every visual is a `visualContainer` in the `visualContainers` array:

```json
{
  "config": "<stringified singleVisual config>",
  "filters": "[]",
  "height": 300.0,
  "width": 600.0,
  "x": 20.0,
  "y": 190.0,
  "z": 6000.0
}
```

### Config (stringified) Structure

```json
{
  "name": "<20-char hex ID>",
  "layouts": [{
    "id": 0,
    "position": {"x": 20, "y": 190, "width": 600, "height": 300, "z": 6000, "tabOrder": 6000}
  }],
  "singleVisual": {
    "visualType": "lineChart",
    "projections": {
      "Category": [{"queryRef": "table.column", "active": true}],
      "Y": [{"queryRef": "Sum(table.column)"}]
    },
    "prototypeQuery": {
      "Version": 2,
      "From": [{"Name": "d", "Entity": "table_name", "Type": 0}],
      "Select": [...]
    },
    "drillFilterOtherVisuals": true,
    "vcObjects": {...},
    "objects": {...}
  }
}
```

---

## Complete Visual Types Reference

### Charts

| visualType | Display Name | Projection Roles |
|------------|-------------|-----------------|
| `lineChart` | Line Chart | Category, Y |
| `areaChart` | Area Chart | Category, Y |
| `stackedAreaChart` | Stacked Area | Category, Y, Series |
| `clusteredBarChart` | Clustered Bar | Category, Y |
| `clusteredColumnChart` | Clustered Column | Category, Y |
| `stackedBarChart` | Stacked Bar | Category, Y, Series |
| `stackedColumnChart` | Stacked Column | Category, Y, Series |
| `hundredPercentStackedBarChart` | 100% Stacked Bar | Category, Y, Series |
| `hundredPercentStackedColumnChart` | 100% Stacked Column | Category, Y, Series |
| `lineStackedColumnComboChart` | Line + Column Combo | Category, Y, Y2 |
| `lineClusteredColumnComboChart` | Line + Clustered Column | Category, Y, Y2 |
| `ribbonChart` | Ribbon Chart | Category, Y, Series |
| `waterfallChart` | Waterfall | Category, Y |
| `funnelChart` | Funnel | Category, Y |
| `scatterChart` | Scatter | X, Y, Size, Details |
| `pieChart` | Pie Chart | Category, Y |
| `donutChart` | Donut Chart | Category, Y |
| `treemap` | Treemap | Group, Values |

### KPI & Cards

| visualType | Display Name | Projection Roles |
|------------|-------------|-----------------|
| `card` | Card | Values |
| `multiRowCard` | Multi-Row Card | Values |
| `kpi` | KPI | Indicator, TrendAxis, Goals |
| `gauge` | Gauge | Y, MinValue, MaxValue, Target |

### Tables & Matrix

| visualType | Display Name | Projection Roles |
|------------|-------------|-----------------|
| `tableEx` | Table | Values (multiple fields) |
| `pivotTable` | Matrix | Rows, Columns, Values |

### Other

| visualType | Display Name | Projection Roles |
|------------|-------------|-----------------|
| `slicer` | Slicer | Values |
| `textbox` | Text Box | (none — uses paragraphs) |
| `shape` | Shape | (none — uses shapeType) |
| `image` | Image | (none — uses imageUrl) |
| `decompositionTreeVisual` | Decomposition Tree | Analyze, Explain By |
| `keyInfluencers` | Key Influencers | Analyze, Explain By |
| `smartNarrativeVisual` | Smart Narrative | Values |
| `qnaVisual` | Q&A | (none) |

---

## Projection Roles Quick Reference

| Role | Used By | Description |
|------|---------|-------------|
| `Category` | Charts (bar, line, column) | X-axis / Category axis |
| `Y` | Charts, Gauge, KPI | Y-axis / Primary values |
| `Y2` | Combo charts | Secondary Y-axis |
| `Values` | Card, Table, Slicer, Treemap | Data values |
| `Group` | Treemap | Grouping category |
| `Series` | Stacked/Ribbon charts | Legend / Series grouping |
| `Rows` | Matrix (pivotTable) | Row headers |
| `Columns` | Matrix (pivotTable) | Column headers |
| `X` | Scatter | X-axis value |
| `Size` | Scatter | Bubble size |
| `Details` | Scatter/Map | Detail grouping |
| `Indicator` | KPI | KPI value |
| `TrendAxis` | KPI | KPI time axis |
| `Goals` | KPI | KPI target |
| `Target` | Gauge | Gauge target value |
| `MinValue` | Gauge | Gauge minimum |
| `MaxValue` | Gauge | Gauge maximum |

---

## prototypeQuery Select Types

### Column (dimension/category)

```json
{
  "Column": {
    "Expression": {"SourceRef": {"Source": "d"}},
    "Property": "column_name"
  },
  "Name": "table_name.column_name",
  "NativeReferenceName": "column_name"
}
```

### Aggregation (measure)

```json
{
  "Aggregation": {
    "Expression": {
      "Column": {
        "Expression": {"SourceRef": {"Source": "d"}},
        "Property": "column_name"
      }
    },
    "Function": 0
  },
  "Name": "Sum(table_name.column_name)",
  "NativeReferenceName": "Sum of column_name"
}
```

### Aggregation Function Codes

| Code | Function | Name Pattern |
|------|----------|-------------|
| `0` | **Sum** | `Sum(table.col)` |
| `1` | **Average** | `Average(table.col)` |
| `2` | **Count** | `Count(table.col)` |
| `3` | **Min** | `Min(table.col)` |
| `4` | **Max** | `Max(table.col)` |
| `5` | **CountNonNull** | `CountNonNull(table.col)` |

> ⚠️ **DistinctCount is NOT available** as prototypeQuery function. Use DAX measures instead.

---

## Styling & Formatting

### vcObjects — Visual-Level Formatting

```json
"vcObjects": {
  "title": [{
    "properties": {
      "show": {"expr": {"Literal": {"Value": "true"}}},
      "text": {"expr": {"Literal": {"Value": "'My Title'"}}}
    }
  }],
  "background": [{
    "properties": {
      "show": {"expr": {"Literal": {"Value": "true"}}},
      "color": {"solid": {"color": {"expr": {"ThemeDataColor": {"ColorId": 4, "Percent": 0.4}}}}}
    }
  }],
  "border": [{
    "properties": {
      "show": {"expr": {"Literal": {"Value": "true"}}},
      "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E0E0E0'"}}}}}
    }
  }]
}
```

### objects — Data-Level Formatting

```json
"objects": {
  "dataPoint": [{
    "properties": {
      "fill": {"solid": {"color": {"expr": {"ThemeDataColor": {"ColorId": 3, "Percent": -0.25}}}}}
    }
  }]
}
```

### Color Expression Types

```json
// Theme color (recommended — respects theme changes)
{"expr": {"ThemeDataColor": {"ColorId": 0, "Percent": 0}}}

// Hex color (fixed)
{"expr": {"Literal": {"Value": "'#FF6B6B'"}}}
```

**ThemeDataColor — ColorId palette:**
- `0-9` = Theme palette colors (varies by theme)
- `Percent` = shade adjustment (-1.0 to 1.0, negative = darker, positive = lighter)

---

## model.bim Structure

```json
{
  "name": "ProjectName",
  "compatibilityLevel": 1567,
  "model": {
    "culture": "en-US",
    "defaultPowerBIDataSourceVersion": "powerBI_V3",
    "tables": [{
      "name": "table_name",
      "columns": [
        {"name": "col", "dataType": "string", "sourceColumn": "col"}
      ],
      "measures": [
        {
          "name": "Total Revenue",
          "expression": "SUM('table'[col])",
          "formatString": "#,##0.00"
        }
      ],
      "partitions": [{
        "name": "table_name",
        "mode": "import",
        "source": {
          "type": "m",
          "expression": ["let", "  Source = Csv.Document(...)", "in", "  Source"]
        }
      }]
    }]
  }
}
```

---

## 🏗️ Data Modeling Best Practices

> **Priority 2** — โครงสร้างโมเดลที่ถูกต้องเป็นรากฐานของ dashboard ที่เร็วและแม่นยำ

### Star Schema (แนะนำเสมอ)

Power BI ทำงานดีที่สุดกับ **Star Schema** — แยกตารางเป็น 2 ประเภท:

| ประเภท | หน้าที่ | ตัวอย่าง | ลักษณะ |
|--------|--------|---------|--------|
| **Fact Table** | เก็บธุรกรรม/เหตุการณ์ | Sales, Orders, Transactions | มีหลายแถว, มี foreign keys, มี measures (ยอดเงิน, จำนวน) |
| **Dimension Table** | เก็บข้อมูลอ้างอิง | Customers, Products, Date, Stores | มีแถวน้อยกว่า, มี primary key, มี attributes (ชื่อ, หมวดหมู่) |

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Dim_Product  │     │   Fact_Sales      │     │ Dim_Customer  │
│──────────────│     │──────────────────│     │──────────────│
│ ProductID (PK)│◄────│ ProductID (FK)    │     │ CustomerID(PK)│
│ Name          │     │ CustomerID (FK)   │────►│ Name          │
│ Category      │     │ DateKey (FK)      │     │ City          │
│ Price         │     │ Quantity          │     │ Segment       │
└──────────────┘     │ Revenue           │     └──────────────┘
                      │ Discount          │
    ┌──────────────┐  └──────────────────┘
    │  Dim_Date     │         │
    │──────────────│         │
    │ DateKey (PK)  │◄────────┘
    │ Year          │
    │ Month         │
    │ Quarter       │
    └──────────────┘
```

> ⚠️ **กฎสำคัญ**: หลีกเลี่ยง "flat table" (ตารางเดียวรวมทุกอย่าง) — ทำให้ช้าและยากต่อการดูแล

### 💡 Pro-Tips: Data Modeling

| Pro-Tip | รายละเอียด |
|---------|----------|
| **Snowflake → Star** | ยุบ Dimension ที่ซ้อนกัน (Snowflake) ให้เป็นตารางเดียว (Star) เพื่อลดจำนวน relationships |
| **Data Granularity** | ตรวจสอบว่าข้อมูลใน Fact/Dim มี "ความละเอียด" ตรงกัน — เช่น Sales รายวัน แต่ Target รายเดือน → ต้อง aggregate ให้ตรงกัน |
| **Bi-directional Filter** | ⚠️ หลีกเลี่ยง — อาจทำให้ผลลัพธ์ DAX ผิดพลาดและทำงานช้า ใช้ `CROSSFILTER()` ใน DAX แทน |

### Relationship Rules

| กฎ | คำอธิบาย | ตัวอย่าง |
|----|---------|---------|
| ✅ **One-to-Many (1:N)** | Dimension → Fact เสมอ | `Dim_Product (1)` → `Fact_Sales (N)` |
| ✅ **Single direction** | ใช้ Single cross-filter direction เป็นค่าเริ่มต้น | Filter จาก Dimension → Fact |
| ⚠️ **Bi-directional** | ใช้เมื่อจำเป็นจริงๆ เท่านั้น | เช่น Many-to-Many bridge table |
| ❌ **Many-to-Many** | หลีกเลี่ยง — สร้าง Bridge Table แทน | ใช้ตาราง intermediate เชื่อม |
| ❌ **Circular relationships** | ห้ามเด็ดขาด — ทำให้ DAX ผิดพลาด | A→B→C→A |

### model.bim Relationships

```json
{
  "relationships": [
    {
      "name": "sales_to_product",
      "fromTable": "Sales",
      "fromColumn": "product_id",
      "toTable": "Products",
      "toColumn": "id",
      "crossFilteringBehavior": "oneDirection"
    },
    {
      "name": "sales_to_date",
      "fromTable": "Sales",
      "fromColumn": "date_key",
      "toTable": "Calendar",
      "toColumn": "DateKey",
      "crossFilteringBehavior": "oneDirection"
    }
  ]
}
```

### 📅 Date Table — ต้องมีเสมอ!

> ⚠️ **กฎบังคับ**: ทุก data model ที่มีข้อมูลเกี่ยวกับเวลา **ต้อง** มี Calendar/Date Table เพื่อ:
> - Time Intelligence functions (YTD, MoM, YoY) ทำงานได้
> - การ drill-down ตาม Year → Quarter → Month → Day
> - การเปรียบเทียบช่วงเวลาที่แม่นยำ

**วิธีสร้าง** (ดู DAX ใน Calculated Tables section ด้านล่าง):
1. ใช้ `CALENDAR()` หรือ `CALENDARAUTO()` ใน DAX
2. Mark as Date Table ใน Power BI Desktop
3. สร้าง relationship กับ Fact Table ผ่าน date column

### 👁️ Hide Foreign Key Columns

> ⚠️ **Best Practice**: ซ่อน FK columns ใน Fact Table เพื่อไม่ให้ผู้ใช้สับสน

FK columns (เช่น `product_id`, `customer_id`) ไม่ควรแสดงใน field list เพราะผู้ใช้ควรเลือกจาก Dimension Table แทน

```json
// model.bim — ซ่อน column ด้วย isHidden
{
  "name": "product_id",
  "dataType": "int64",
  "sourceColumn": "product_id",
  "isHidden": true
}
```

**Columns ที่ควรซ่อน:**
- ✅ Foreign Key columns ใน Fact Table (`product_id`, `customer_id`, `date_key`)
- ✅ Technical columns ที่ไม่มีความหมายกับผู้ใช้ (`row_hash`, `etl_timestamp`)
- ✅ Columns ที่ใช้เฉพาะใน relationship
- ❌ ห้ามซ่อน Primary Key ใน Dimension Table

---

### Column Data Types

| dataType | M Query Type | Python Type |
|----------|-------------|-------------|
| `string` | `type text` | `str` |
| `int64` | `Int64.Type` | `int` |
| `double` | `type number` | `float` |
| `dateTime` | `type datetime` | `datetime` |
| `boolean` | `type logical` | `bool` |

---

## 📐 DAX Best Practices

### Measures vs Calculated Columns

> ⚠️ **กฎสำคัญ**: ใช้ **Measures** สำหรับการคำนวณสรุปผลเสมอ แทนการสร้าง Calculated Columns

| | Measures ✅ | Calculated Columns ⚠️ |
|---|-----------|---------------------|
| **คำนวณเมื่อไหร่** | ตอน query (runtime) | ตอน refresh (ถูกเก็บใน memory) |
| **ใช้ memory** | ไม่ใช้ | ใช้ — เพิ่มขนาดไฟล์ |
| **ตอบสนองต่อ filter** | ✅ ปรับตาม context | ❌ ค่าคงที่ต่อแถว |
| **เหมาะกับ** | SUM, AVG, COUNT, %, YoY | Grouping, Sorting, ใช้ใน relationship |

**ตัวอย่างที่ถูก:**
```dax
// ✅ MEASURE — คำนวณตอน runtime, ตอบสนองต่อ filters
Total Revenue = SUM('Sales'[Amount])
Profit Margin = DIVIDE([Profit], [Revenue], 0)
```

**ตัวอย่างที่ผิด:**
```dax
// ❌ CALCULATED COLUMN — ไม่ควรใช้สำหรับ aggregation
// เพราะค่าถูกคำนวณทุกแถวและเก็บใน memory
Revenue_Column = 'Sales'[Qty] * 'Sales'[Price]  // ใช้ Measure แทน!
```

**เมื่อไหร่ที่ใช้ Calculated Column ได้:**
- ต้องการคอลัมน์สำหรับ Slicer / Filter / Row-level grouping
- ต้องใช้เป็น Relationship key
- ต้องการ Sort By Column

### DAX Formatting Standard

> ⚠️ สูตร DAX ที่อ่านง่ายช่วยลด bug และง่ายต่อการ maintain

**กฎ Formatting:**

| กฎ | ตัวอย่าง |
|----|--------|
| ✅ ขึ้นบรรทัดใหม่หลัง `=` | `Revenue = ⏎ SUM(...)` |
| ✅ Indent ด้วย 4 spaces | `    FILTER(...)` |
| ✅ Function ตัวพิมพ์ใหญ่ | `CALCULATE`, `DIVIDE`, `FILTER` |
| ✅ ใส่ comment ด้วย `//` | `// YoY comparison` |
| ✅ ใช้ `VAR` แยกขั้นตอน | `VAR x = ... RETURN ...` |
| ❌ เขียนยาวบรรทัดเดียว | `CALCULATE(SUM(...),FILTER(...))` |

**ตัวอย่าง — ก่อน vs หลัง:**

```dax
// ❌ ไม่ดี — อ่านยาก
YoY Growth = DIVIDE(CALCULATE(SUM('Sales'[Revenue]),DATEADD('Calendar'[Date],-1,YEAR))-SUM('Sales'[Revenue]),CALCULATE(SUM('Sales'[Revenue]),DATEADD('Calendar'[Date],-1,YEAR)),0)

// ✅ ดี — อ่านง่าย, มี comment, ใช้ VAR
// Year-over-Year Growth Rate
YoY Growth =
    VAR CurrentYear = [Total Revenue]
    VAR PrevYear =
        CALCULATE(
            [Total Revenue],
            SAMEPERIODLASTYEAR('Calendar'[Date])
        )
    RETURN
        DIVIDE(
            CurrentYear - PrevYear,
            PrevYear,
            0  // return 0 if division by zero
        )
```

### DAX Comments Guide

| Comment | ใช้เมื่อ | ตัวอย่าง |
|---------|--------|--------|
| `// Description` | อธิบายจุดประสงค์ของ measure | `// Monthly revenue growth %` |
| `// TODO:` | งานที่ยังไม่เสร็จ | `// TODO: add fiscal year logic` |
| `// FIXME:` | Bug ที่รู้แล้ว | `// FIXME: fails when no data` |
| `// NOTE:` | ข้อควรระวังสำคัญ | `// NOTE: requires Calendar table` |

### 📁 Measures Table (Best Practice)

> ⚠️ **แนะนำ**: สร้าง **ตารางเปล่า** สำหรับเก็บ Measures ทั้งหมดไว้ที่เดียว

**ทำไม?**
- จัดระเบียบ Measures ไม่ปนกับ data columns
- หาง่ายขึ้นเมื่อมี Measures 20+ ตัว
- แยกหมวดหมู่ได้ (Sales Measures, Finance Measures)

**วิธีสร้างใน model.bim:**
```json
{
  "name": "_Measures",
  "columns": [
    {"name": "Helper", "dataType": "string", "sourceColumn": "Helper", "isHidden": true}
  ],
  "measures": [
    {"name": "Total Revenue", "expression": "SUM('Sales'[Amount])", "formatString": "#,##0.00"},
    {"name": "Total Orders", "expression": "DISTINCTCOUNT('Sales'[OrderID])", "formatString": "#,##0"},
    {"name": "Avg Order Value", "expression": "DIVIDE([Total Revenue], [Total Orders], 0)", "formatString": "#,##0.00"}
  ],
  "partitions": [{
    "name": "_Measures",
    "mode": "import",
    "source": {"type": "calculated", "expression": "ROW(\"Helper\", BLANK())"}
  }]
}
```

> 💡 **Naming**: ใช้ `_` นำหน้า (เช่น `_Measures`) เพื่อให้อยู่บนสุดของ field list

**Display Folders** — จัดกลุ่ม Measures:
```json
{"name": "YoY Growth", "expression": "...",
  "displayFolder": "Time Intelligence"}
{"name": "Total Revenue", "expression": "...",
  "displayFolder": "Sales"}
```

### 💡 Pro-Tips: DAX Performance

| Pro-Tip | รายละเอียด |
|---------|----------|
| **VAR/RETURN เสมอ** | ใช้ตัวแปรทุกครั้ง — อ่านง่ายขึ้น + คำนวณครั้งเดียวเก็บค่าไว้ (เร็วกว่า) |
| **Dynamic Measures** | ใช้ `SWITCH(TRUE(), ...)` + Slicer เพื่อให้ user เลือกดู "จำนวนเงิน" หรือ "จำนวนชิ้น" ในกราฟเดียว |
| **DAX Studio** | ⭐ ใช้เครื่องมือภายนอก [DAX Studio](https://daxstudio.org) เพื่อ profile สูตร DAX — เห็น query time แยกรายสูตร |
| **DIVIDE() ไม่ใช่ /** | `DIVIDE(a, b, 0)` ป้องกัน error จาก division by zero อัตโนมัติ |

---

### DAX Measure Examples

```dax
// Basic aggregations
Total Revenue = SUM('table'[total_payment])
Total Orders = DISTINCTCOUNT('table'[order_id])
Avg Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

// Percentage
On Time Pct = DIVIDE(
  COUNTROWS(FILTER('table', 'table'[delivery_on_time] = "On Time")),
  COUNTROWS('table'), 0
)

// Time Intelligence (requires date table)
YTD Revenue = TOTALYTD([Total Revenue], 'Date'[Date])
MoM Growth = DIVIDE([Total Revenue] - [Prev Month], [Prev Month], 0)
```

---

## 📊 Data Analysis & Visual Selection Guide

> **เป้าหมาย**: เลือก visual ที่เหมาะกับข้อมูลอัตโนมัติ — ทำให้ dashboard สวยและเข้าใจง่าย

### Step 1: ระบุเป้าหมายการวิเคราะห์

| เป้าหมาย | คำถามที่ตอบ | Visual ที่เหมาะ |
|----------|-----------|----------------|
| **Comparison** | อันไหนมากกว่า/น้อยกว่า? | Bar, Column, Grouped Bar |
| **Trend** | เปลี่ยนแปลงอย่างไรตามเวลา? | Line, Area, Combo |
| **Composition** | สัดส่วนเป็นอย่างไร? | Pie, Donut, Stacked Bar, Treemap |
| **Distribution** | ข้อมูลกระจายตัวอย่างไร? | Histogram, Scatter, Box Plot |
| **Relationship** | ตัวแปร 2 ตัวสัมพันธ์กันไหม? | Scatter, Bubble |
| **KPI/Summary** | ตัวเลขสำคัญคืออะไร? | Card, Gauge, KPI |
| **Detail** | ดูรายละเอียดทั้งหมด | Table, Matrix |
| **Filtering** | กรองข้อมูลตามมิติ | Slicer |

### Step 2: Data-to-Visual Mapping (ข้อมูล → Visual)

#### ตามประเภทข้อมูล

| ข้อมูลที่มี | ตัวอย่าง | Visual ที่ดีที่สุด | ห้ามใช้ |
|------------|---------|-------------------|---------|
| **1 ตัวเลข (KPI)** | Total Revenue | `card` | Line, Bar |
| **ตัวเลข + เป้าหมาย** | Revenue vs Target | `gauge` | Pie |
| **หมวดหมู่ + ตัวเลข** | Sales by City | `clusteredBarChart` | Scatter |
| **เวลา + ตัวเลข** | Revenue by Month | `lineChart` | Pie, Bar |
| **เวลา + ตัวเลข 2 ตัว** | Revenue + Orders by Month | `lineStackedColumnComboChart` | Pie |
| **หมวดหมู่ + ตัวเลข + กลุ่ม** | Sales by City by Product | `stackedBarChart` | Card |
| **สัดส่วน (< 6 กลุ่ม)** | Market Share | `donutChart` | Line |
| **สัดส่วน (> 6 กลุ่ม)** | Revenue by Category | `treemap` | Pie |
| **ตัวเลข 2 ตัวสัมพันธ์กัน** | Price vs Quantity | `scatterChart` | Bar |
| **ข้อมูลหลายคอลัมน์** | Top 10 Products detail | `tableEx` | Card |
| **ลำดับขั้น/ลดลง** | Sales Funnel | `funnelChart` | Line |
| **กำไร/ขาดทุนสะสม** | P&L Waterfall | `waterfallChart` | Pie |
| **อันดับเปลี่ยนตามเวลา** | City Rank by Year | `ribbonChart` | Bar |

#### ตามประเภท Column ใน Data

| Column Type | ลักษณะ | ลากไปที่ Role | ตัวอย่าง |
|-------------|--------|-------------|---------|
| **Date/DateTime** | วันที่, เดือน, ปี | `Category` (X-axis) | order_date, created_at |
| **Text/Category** | ชื่อ, กลุ่ม, สถานะ | `Category`, `Series`, `Group` | city, product_type, status |
| **Integer/Float (metrics)** | ยอดเงิน, จำนวน, % | `Y` (aggregate), `Values` | revenue, quantity, price |
| **Boolean** | Yes/No, True/False | `Category` (filter) | is_active, delivered |
| **ID (unique)** | ไม่ซ้ำกัน | ❌ ไม่ควรลาก | order_id, customer_id |

> ⚠️ **กฎทอง**: ID columns ไม่ควรลากเข้า visual เลย ยกเว้นเมื่อ DISTINCTCOUNT

### Step 3: กฎเลือก Aggregation ให้เหมาะ

| ลักษณะข้อมูล | Aggregation | Function Code | ตัวอย่าง |
|-------------|-------------|--------------|---------|
| **จำนวนรวม** (เงิน, น้ำหนัก) | Sum | `0` | Total Revenue |
| **ค่าเฉลี่ย** (rating, price) | Average | `1` | Avg Review Score |
| **นับจำนวน** (transactions) | Count | `2` | Total Rows |
| **ค่าต่ำสุด** (minimum) | Min | `3` | Min Price |
| **ค่าสูงสุด** (maximum) | Max | `4` | Max Delivery Days |
| **นับไม่ซ้ำ** (unique customers) | CountNonNull | `5` | Unique Customers |
| **นับไม่ซ้ำ (แม่นยำ)** | DAX DISTINCTCOUNT | — | Exact Unique Orders |

---

## 🎨 Dashboard Design Rules

### Report Header Standard

> ทุก dashboard ควรมี header ที่ชัดเจนเพื่อบอกบริบท

```
┌─────────────────────────────────────────────────────┐
│  [Logo]  Report Title          Last Refresh: {date} │
│          Subtitle/Description   Department/Team     │
└─────────────────────────────────────────────────────┘
```

**Header Components:**

| Component | วิธีทำ | ตัวอย่าง |
|-----------|--------|--------|
| **ชื่อรายงาน** | Textbox (bold, 20-24pt) | "Sales Performance Dashboard" |
| **โลโก้บริษัท** | Image visual | ไฟล์ PNG/SVG |
| **วันที่อัพเดตล่าสุด** | Card + DAX Measure | `Last Refresh = MAX('Sales'[LoadDate])` |
| **ช่วงเวลาข้อมูล** | Card + DAX | `Data Range = MIN('Date'[Date]) & " - " & MAX('Date'[Date])` |
| **แผนก/ทีม** | Textbox | "Finance Department" |

**Layout (report.json):**
```json
// Logo image — มุมซ้ายบน
{"x": 20, "y": 10, "width": 120, "height": 50, "z": 100}
// Title textbox — ข้างโลโก้
{"x": 150, "y": 10, "width": 600, "height": 50, "z": 200}
// Last Refresh card — มุมขวาบน
{"x": 1050, "y": 10, "width": 210, "height": 50, "z": 300}
```

### Visual Hierarchy (Z-Pattern)

```
┌─────────────────────────────────────────────────────┐
│  🏷️ Header (Logo + Title + Date)  (TOP — y=0)      │
├─────────────────────────────────────────────────────┤
│  🔍 Slicers / Filters           (y=65)             │
├─────────────────────────────────────────────────────┤
│  📊 KPI Cards                    (y=130)            │
│  [Revenue] [Orders] [Avg Value] [Customers]         │
├─────────────────────────────────────────────────────┤
│  📈 Main Charts (Hero)           (y=245)            │
│  [Revenue Trend Line]    [Sales by Category Bar]    │
├─────────────────────────────────────────────────────┤
│  📋 Detail / Supporting          (y=500)            │
│  [Top Products Table]  [Funnel]  [Gauge]            │
└─────────────────────────────────────────────────────┘
```

**กฎ**: ข้อมูลสำคัญที่สุดอยู่ซ้ายบน → ข้อมูลรายละเอียดอยู่ขวาล่าง

### จำนวน Visual ต่อหน้า

| Level | Visual ต่อหน้า | เหมาะกับ |
|-------|---------------|---------|
| **Executive** | 4-6 visuals | ผู้บริหาร — ดูเร็ว |
| **Analyst** | 6-8 visuals | นักวิเคราะห์ — ดูลึก |
| **Detail** | 1-2 visuals (table/matrix) | ดูรายละเอียด |

> 🎯 **Microsoft แนะนำ**: ไม่เกิน 8 visuals + 1 table ต่อหน้า

### สี — ใช้ให้มีความหมาย

| สถานการณ์ | สี | ThemeDataColor |
|----------|-----|---------------|
| **ค่าบวก/ดี** | เขียว | `ColorId: 6` |
| **ค่าลบ/แย่** | แดง | `ColorId: 2` |
| **ค่ากลาง/ปกติ** | น้ำเงิน | `ColorId: 0` |
| **เน้น/สำคัญ** | ส้ม/เหลือง | `ColorId: 1` |
| **รอง/พื้นหลัง** | เทา | `ColorId: 8, Percent: 0.6` |

**Color Rules**:
- ✅ ใช้ไม่เกิน 5-7 สีหลัก
- ✅ สีเดียวกันหมายถึงสิ่งเดียวกันทั้ง dashboard
- ✅ ใช้ contrast สูงระหว่าง text กับ background
- ❌ ห้ามใช้สีแดง+เขียวคู่กัน (color blind unfriendly)
- ❌ ห้ามใช้สีสดทุกตัว — ให้ visual สำคัญเท่านั้นที่ใช้สีสด

### Typography

| Element | ขนาดแนะนำ | น้ำหนัก |
|---------|----------|---------|
| Page Title | 20-24pt | Bold |
| Visual Title | 12-14pt | Semi-Bold |
| KPI Number | 24-32pt | Bold |
| Labels/Values | 10-12pt | Regular |
| Footnotes | 8-9pt | Light |

**Font**: Segoe UI (PBI default) หรือ Sans-serif fonts เท่านั้น

### Page Organization (Multi-Page)

| หน้า | เนื้อหา | Visual Types |
|------|--------|-------------|
| **1. Overview** | KPIs + trends + top-level | Cards, Line, Bar |
| **2. Sales/Revenue** | รายละเอียดยอดขาย | Combo, Stacked, Table |
| **3. Customer** | วิเคราะห์ลูกค้า | Scatter, Donut, Map |
| **4. Product** | วิเคราะห์สินค้า | Treemap, Funnel, Bar |
| **5. Detail** | ตารางรายละเอียด | Table, Matrix, Slicer |

### 💡 Pro-Tips: Visualization

| Pro-Tip | รายละเอียด |
|---------|----------|
| **5-Second Rule** | ผู้ใช้ต้องเข้าใจภาพรวมภายใน **5 วินาทีแรก** ที่เห็น — ถ้าไม่ได้ แปลว่ามี visual เยอะเกินหรือ layout ไม่ดี |
| **Bookmarks + Buttons** | ใช้ Bookmarks + Selection Pane สร้างปุ่มสลับ view (เช่น Chart ↔ Table) หรือ Pop-up menu — ประหยัดพื้นที่ |
| **White Space** | เว้นระยะห่างระหว่าง visuals อย่างน้อย 10-20px — ลดความรกและช่วยให้ดูง่ายขึ้น |
| **สีไม่เกิน 3-4 สี** | ใช้สีหลัก 3-4 สี + สีเทาเป็นพื้นหลัง — ลด gridlines ให้เหลือน้อยที่สุด |

---

## 🔧 Power Query Pro-Tips

### Query Folding

> ⚠️ ตรวจสอบว่าขั้นตอนการ Transform ถูกส่งไป **ประมวลผลที่ source** (SQL) หรือไม่ — เร็วกว่า PBI ทำเองมาก

**วิธีตรวจ:**
1. เปิด Power Query Editor
2. คลิกขวาที่ step ใน Applied Steps
3. ดูว่า **"View Native Query"** คลิกได้ (✅ folded) หรือเป็นสีเทา (❌ ไม่ fold)

| Step ที่ Fold ได้ ✅ | Step ที่ Fold ไม่ได้ ❌ |
|-------------------|---------------------|
| `Table.SelectRows` (filter) | `Table.AddColumn` (custom column) |
| `Table.SelectColumns` (select) | `Table.Buffer` |
| `Table.Sort` | `Table.TransformColumns` (complex) |
| `Table.Group` | Merge ข้าม data sources |
| `Table.RemoveDuplicates` | Custom M functions |

> 💡 **กฎ**: วาง steps ที่ fold ได้ไว้ **ก่อน** steps ที่ fold ไม่ได้ — เพื่อให้ database ทำงานหนักแทน PBI

### Buffer Functions

ใช้เมื่อต้องอ้างอิงตารางเดิมซ้ำๆ:

```m
// Table.Buffer — cache ตารางไว้ใน memory (ไม่ query ซ้ำ)
let
    Source = Sql.Database("server", "db"),
    Sales = Source{[Schema="dbo",Item="Sales"]}[Data],
    Buffered = Table.Buffer(Sales),     // ⬅ cache ไว้
    Step1 = Table.SelectRows(Buffered, each [Year] = 2026),
    Step2 = Table.Group(Buffered, {"Category"}, {{"Total", each List.Sum([Amount])}})
in ...

// List.Buffer — cache list สำหรับ Filter/Contains
let
    ValidIDs = List.Buffer(Table.Column(Products, "ID")),     // ⬅ cache list
    Filtered = Table.SelectRows(Sales, each List.Contains(ValidIDs, [ProductID]))
in Filtered
```

> ⚠️ ใช้ Buffer เฉพาะเมื่อตารางถูกอ้างอิง **2 ครั้งขึ้นไป** — ถ้าอ้างอิงครั้งเดียว Buffer จะ **เพิ่ม** memory โดยไม่จำเป็น

---

## 🧠 Smart Analysis Patterns

### Pattern 1: Sales Dashboard

```
ข้อมูลที่มี: date, product, city, revenue, quantity, customer_id

→ Page 1: Overview
  - Cards: Total Revenue (Sum), Total Orders (Count), Avg Order (Avg), Unique Customers (CountNonNull)
  - Line: Revenue by Month (Category=date, Y=Sum revenue)
  - Bar: Revenue by City (Category=city, Y=Sum revenue)

→ Page 2: Product Analysis
  - Treemap: Revenue by Product (Group=product, Values=Sum revenue)
  - Combo: Revenue + Quantity by Month (Category=date, Y=Sum revenue, Y2=Sum quantity)
  - Table: Top 10 Products detail
```

### Pattern 2: HR Dashboard

```
ข้อมูลที่มี: employee_name, department, hire_date, salary, performance_score, is_active

→ Page 1: Overview
  - Cards: Total Employees, Avg Salary, Avg Performance Score
  - Donut: Employees by Department
  - Line: Hiring Trend by Month (Category=hire_date, Y=Count)

→ Page 2: Analysis
  - Scatter: Salary vs Performance (X=salary, Y=performance_score)
  - Stacked Bar: Active/Inactive by Department (Category=department, Y=Count, Series=is_active)
  - Gauge: Avg Performance Score vs Target
```

### Pattern 3: Finance Dashboard

```
ข้อมูลที่มี: date, category, income, expense, profit

→ Page 1: Overview
  - Cards: Total Income, Total Expense, Net Profit, Profit Margin
  - Waterfall: P&L Breakdown (Category=category, Y=profit)
  - Combo: Income + Expense Trend (Category=date, Y=income, Y2=expense)

→ Page 2: Detail
  - Table: Monthly breakdown
  - Stacked Column: Expense by Category by Month
```

---

## ⚡ Import vs DirectQuery vs Dual

> เลือก connection mode ให้เหมาะกับสถานการณ์

| | **Import** | **DirectQuery** | **Dual** |
|---|-----------|----------------|----------|
| **วิธีทำงาน** | โหลดข้อมูลเข้า memory ทั้งหมด | Query จาก source ทุกครั้งที่ interact | ผสม — cache + query |
| **ความเร็ว** | ⚡ เร็วมาก (in-memory) | 🐌 ช้ากว่า (network + source) | ⚡ เร็ว (ถ้า cache hit) |
| **ข้อมูล real-time** | ❌ ต้อง refresh | ✅ เสมอล่าสุด | ✅ ผสม |
| **ขนาดข้อมูล** | จำกัด ~1GB (free) / 10GB (Pro) | ไม่จำกัด | ผสม |
| **DAX รองรับ** | ✅ ครบทุก function | ⚠️ บาง function ช้า/ไม่ได้ | ✅ ครบ |
| **เหมาะกับ** | ข้อมูล < 1M rows, refresh รายวัน | Database ขนาดใหญ่, real-time | ผสมทั้ง 2 แบบ |

**กฎเลือก Mode:**

| สถานการณ์ | เลือก | เหตุผล |
|-----------|------|--------|
| ข้อมูลไม่เกิน 500K rows | **Import** | เร็วที่สุด, DAX ครบทุก function |
| ข้อมูลหลายล้านแถว + real-time | **DirectQuery** | ไม่ต้องโหลดเข้า memory |
| ข้อมูลเปลี่ยนทุก 15 นาที | **DirectQuery** | ข้อมูลล่าสุดเสมอ |
| Mixed — fact ใหญ่ + dim เล็ก | **Dual** | Dimension = Import, Fact = DirectQuery |
| Excel / CSV files | **Import** | DirectQuery ไม่รองรับ |

### model.bim — ตั้ง Mode ใน partition
```json
// Import mode (default)
{"name": "Sales", "mode": "import", "source": {"type": "m", "expression": [...]}}

// DirectQuery mode
{"name": "Sales", "mode": "directQuery", "source": {"type": "m", "expression": [...]}}

// Dual mode
{"name": "Sales", "mode": "dual", "source": {"type": "m", "expression": [...]}}
```

---

## M Query Sources (Fix #8)

### CSV
```m
let Source = Csv.Document(File.Contents("C:\data\sales.csv"),
    [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Headers = Table.PromoteHeaders(Source) in Headers
```

### Excel
```m
let Source = Excel.Workbook(File.Contents("C:\data\sales.xlsx"), null, true),
    Sheet1 = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    Headers = Table.PromoteHeaders(Sheet1) in Headers
```

### SQL Server
```m
let Source = Sql.Database("server_name", "database_name"),
    Table1 = Source{[Schema="dbo",Item="sales"]}[Data] in Table1
```

### Web / API
```m
let Source = Json.Document(Web.Contents("https://api.example.com/data")),
    Table1 = Table.FromRecords(Source) in Table1
```

### SharePoint
```m
let Source = SharePoint.Files("https://company.sharepoint.com/sites/data", [ApiVersion=15]),
    File = Source{[Name="sales.xlsx"]}[Content],
    Data = Excel.Workbook(File){0}[Data] in Data
```

---

## Advanced DAX Patterns (Fix #10)

```dax
// ---- Ranking ----
Product Rank = RANKX(ALL('Products'), [Total Revenue],, DESC, Dense)

// ---- Running Total ----
Running Total = CALCULATE([Total Revenue],
    FILTER(ALL('Calendar'[Date]), 'Calendar'[Date] <= MAX('Calendar'[Date])))

// ---- Year-over-Year Growth ----
YoY Growth = 
VAR CurrentYear = [Total Revenue]
VAR PrevYear = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Calendar'[Date]))
RETURN DIVIDE(CurrentYear - PrevYear, PrevYear)

// ---- Moving Average (3 months) ----
MA_3M = AVERAGEX(
    DATESINPERIOD('Calendar'[Date], MAX('Calendar'[Date]), -3, MONTH),
    [Total Revenue])

// ---- SWITCH for dynamic measures ----
Selected Metric = SWITCH(SELECTEDVALUE('Metric'[MetricName]),
    "Revenue", [Total Revenue],
    "Orders", [Total Orders],
    "Avg Value", [Avg Order Value],
    BLANK())

// ---- Pareto (80/20) ----
Cumulative Pct = 
DIVIDE(
    CALCULATE([Total Revenue],
        FILTER(ALL('Products'),
            RANKX(ALL('Products'), [Total Revenue],, DESC) <= 
            RANKX(ALL('Products'), [Total Revenue],, DESC))),
    CALCULATE([Total Revenue], ALL('Products')))

// ---- CALCULATE with complex filter ----
Revenue Top Cities = CALCULATE([Total Revenue],
    TOPN(5, ALL('Cities'), [Total Revenue], DESC))

// ---- Dynamic Title ----
Chart Title = "Revenue for " & SELECTEDVALUE('Calendar'[Year], "All Years")

// ---- Conditional Color (for use in visual) ----
KPI Color = IF([YoY Growth] > 0, "#00B050", IF([YoY Growth] > -0.1, "#FFC000", "#FF0000"))
```

---

## Map / Geo Visual (Fix #11)

### Filled Map
```json
{
  "visualType": "filledMap",
  "projections": {
    "Category": [{"queryRef": "table.country", "active": true}],
    "Size": [{"queryRef": "Sum(table.revenue)"}]
  }
}
```

> ⚠️ **ข้อจำกัด**: Map ต้องมี column ที่ Power BI รู้จักเป็นภูมิศาสตร์ (country, state, city, lat/long)
> ตั้ง Data Category ใน model.bim: `"dataCategory": "Country"` หรือ `"City"`

### Column with Data Category (model.bim)
```json
{"name": "country", "dataType": "string", "sourceColumn": "country",
 "annotations": [{"name": "DataCategory", "value": "Country"}]}
```

---

## Tooltip Page (Fix #12)

สร้าง tooltip page โดยตั้ง `displayOption` = 2 และ size เล็ก:

```json
{
  "config": "{\"type\":2}",
  "displayName": "Tooltip Page",
  "displayOption": 2,
  "filters": "[]",
  "height": 320.0,
  "width": 240.0,
  "name": "<hex_id>",
  "ordinal": 99,
  "visualContainers": [...]
}
```

> **type: 2** = Tooltip page, **displayOption: 2** = hidden from navigation
> ขนาดมาตรฐาน: 320×240 หรือ 640×480

---

## Drill-through (Fix #13)

### Page Config (target page)
```json
{
  "config": "{\"type\":0}",
  "displayName": "Product Detail",
  "filters": "[]",
  "visualContainers": [...],
  "config_drillthrough": {
    "drillFilters": [{
      "filter": {
        "Version": 2,
        "From": [{"Name": "d", "Entity": "Products", "Type": 0}],
        "Where": [{
          "Condition": {
            "In": {
              "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "product_name"}}],
              "Values": []
            }
          }
        }]
      }
    }]
  }
}
```

> User right-clicks a data point → "Drill through" → goes to detail page filtered by that value

---

## Bookmarks (Fix #14)

### ใน report.json top-level config (stringified):
```json
{
  "bookmarks": [
    {
      "name": "bookmark_revenue",
      "displayName": "Revenue View",
      "explorationState": {
        "version": "1.0",
        "activeSectionIndex": 0,
        "filters": {"byVisual": {}}
      }
    },
    {
      "name": "bookmark_orders",
      "displayName": "Orders View",
      "explorationState": {
        "version": "1.0",
        "activeSectionIndex": 0,
        "filters": {"byVisual": {}}
      }
    }
  ]
}
```

> ใช้คู่กับ Buttons visual เพื่อ toggle views

---

## Data Bars & Sparklines (Fix #15)

### Data Bars ใน Table
```json
"objects": {
  "values": [{
    "properties": {
      "backColor": {
        "solid": {"color": {"expr": {
          "Conditional": {
            "Cases": [{
              "Condition": {"Comparison": {
                "ComparisonKind": 1,
                "Left": {"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "revenue"}},
                "Right": {"Literal": {"Value": "0L"}}
              }},
              "Value": {"Literal": {"Value": "'#E8F5E9'"}}
            }],
            "Else": {"Value": {"Literal": {"Value": "'#FFEBEE'"}}}
          }
        }}}
      }
    },
    "selector": {"metadata": "revenue"}
  }]
}
```

> ⚠️ Native Data Bars และ Sparklines ต้อง reverse-engineer จาก PBI Desktop เนื่องจากใช้ internal format ที่ซับซ้อน

---

## Conditional Formatting (Fix #3)

### Color Scale (gradient)
```json
"objects": {
  "dataPoint": [{
    "properties": {
      "fill": {
        "solid": {"color": {"expr": {
          "FillRule": {
            "Input": {"Measure": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "Total Revenue"}},
            "FillRule": {
              "linearGradient3": {
                "min": {"color": {"expr": {"Literal": {"Value": "'#FF0000'"}}}},
                "mid": {"color": {"expr": {"Literal": {"Value": "'#FFFF00'"}}}},
                "max": {"color": {"expr": {"Literal": {"Value": "'#00FF00'"}}}}
              }
            }
          }
        }}}
      }
    }
  }]
}
```

### Rules-based
```json
"objects": {
  "dataPoint": [{
    "properties": {
      "fill": {
        "solid": {"color": {"expr": {
          "Conditional": {
            "Cases": [
              {
                "Condition": {"Comparison": {"ComparisonKind": 2,
                  "Left": {"Measure": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "Score"}},
                  "Right": {"Literal": {"Value": "80L"}}}},
                "Value": {"Literal": {"Value": "'#00B050'"}}
              },
              {
                "Condition": {"Comparison": {"ComparisonKind": 2,
                  "Left": {"Measure": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "Score"}},
                  "Right": {"Literal": {"Value": "50L"}}}},
                "Value": {"Literal": {"Value": "'#FFC000'"}}
              }
            ],
            "Else": {"Value": {"Literal": {"Value": "'#FF0000'"}}}
          }
        }}}
      }
    }
  }]
}
```

> **ComparisonKind**: 0=EQ, 1=GT, 2=GTE, 3=LT, 4=LTE, 5=NE

---

## Reverse Engineering Workflow

When PBI Desktop format is unknown:

1. **Open `.pbip` in PBI Desktop** (data loads even if visuals don't show)
2. **Create 1 visual manually** (drag a field onto canvas)
3. **Save (Ctrl+S)** — PBI writes the correct format to disk
4. **Read `report.json`** — learn the exact format
5. **Replicate in Python** — generate more visuals using the same pattern

> This approach works because PBI Desktop always writes valid format when saving.

---

## Common Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| "File corrupted" | Wrong `.pbip` format | Check JSON structure matches reference |
| "Missing model.bim" | Wrong folder structure | Ensure `SemanticModel/model.bim` exists |
| Blank visuals | Wrong `projections.queryRef` ↔ `Select.Name` mismatch | queryRef MUST match Select.Name exactly |
| "Median of X" | Function code `6` = Median not DistinctCount | Use code `5` (CountNonNull) instead |
| Visual not rendering | PBIR v1 format used | Use PBIR-Legacy single file format (v4.0) |
| No data showing | M query path wrong | Use absolute CSV path in M expression |

---

## Layout Best Practices

| Element | Recommended Layout |
|---------|-------------------|
| **Canvas** | 1280 × 720 (default) |
| **Slicers** | Top row, y=10, height=50 |
| **KPI Cards** | Below slicers, y=75, height=100 |
| **Main Charts** | Middle, y=190, height=250 |
| **Detail Charts** | Bottom, y=455, height=255 |
| **Margins** | x starts at 20, gap=20 between visuals |
| **z-index** | Increment by 1000 per visual |

---

## 🎨 Dashboard Beautification & Theming

> **เป้าหมาย**: ทำให้ dashboard สวย professional ด้วย custom themes, visual styling, และ design patterns — ทั้งหมดทำได้ผ่าน JSON ใน PBIP format

### 1. Custom Theme JSON — Complete Reference

> ⚠️ **สำคัญ**: Theme JSON คือวิธีหลักในการตกแต่ง dashboard ทั้งหมดพร้อมกัน — กำหนดสี, font, border, shadow ให้ทุก visual ในครั้งเดียว

#### โครงสร้าง Theme JSON

```json
{
  "name": "My Custom Theme",

  // 1️⃣ Data Colors — สีหลักของ charts (8-10 สี)
  "dataColors": ["#118DFF", "#12239E", "#E66C37", "#6B007B", "#E044A7"],

  // 2️⃣ Sentiment Colors — สำหรับ KPI, Waterfall
  "good": "#1AAB40",
  "neutral": "#D9B300",
  "bad": "#D64554",

  // 3️⃣ Gradient Colors — สำหรับ Conditional Formatting
  "maximum": "#118DFF",
  "center": "#D9B300",
  "minimum": "#DEEFFF",
  "null": "#FF7F48",

  // 4️⃣ Structural Colors — สีพื้นฐานของ UI
  "background": "#FFFFFF",
  "secondaryBackground": "#C8C6C4",
  "foreground": "#252423",
  "tableAccent": "#118DFF",
  "firstLevelElements": "#252423",
  "secondLevelElements": "#605E5C",
  "thirdLevelElements": "#F3F2F1",
  "fourthLevelElements": "#B3B0AD",

  // 5️⃣ Text Classes — font ทั้ง report
  "textClasses": {
    "callout": {"fontSize": 28, "fontFace": "DIN", "color": "#252423"},
    "title":   {"fontSize": 12, "fontFace": "DIN", "color": "#252423"},
    "header":  {"fontSize": 12, "fontFace": "Segoe UI Semibold", "color": "#252423"},
    "label":   {"fontSize": 10, "fontFace": "Segoe UI", "color": "#252423"}
  },

  // 6️⃣ Visual Styles — formatting เฉพาะ visual type
  "visualStyles": {
    "*": {
      "*": {
        "*": [{"wordWrap": true}],
        "background": [{"show": true, "transparency": 0}],
        "border":     [{"show": true, "color": {"solid": {"color": "#E6E6E6"}}, "radius": 10}],
        "dropShadow": [{"show": true, "color": {"solid": {"color": "#CCCCCC"}}, "position": "Outer", "preset": "BottomRight"}],
        "title":      [{"show": true, "fontColor": {"solid": {"color": "#252423"}}, "fontSize": 12}]
      }
    }
  }
}
```

#### Structural Colors อธิบาย

| Property | หน้าที่ | ค่าตัวอย่าง (Light) | ค่าตัวอย่าง (Dark) |
|----------|--------|--------------------|-----------------|
| `background` | พื้นหลังหน้า report | `#FFFFFF` | `#1B1B2F` |
| `secondaryBackground` | พื้นหลังรอง (cards, panels) | `#F3F2F1` | `#252542` |
| `foreground` | สีข้อความหลัก | `#252423` | `#E0E0E0` |
| `firstLevelElements` | ข้อความ/เส้นหลัก (axes, labels) | `#252423` | `#FFFFFF` |
| `secondLevelElements` | ข้อความรอง (subtitles, gridlines) | `#605E5C` | `#A0A0A0` |
| `thirdLevelElements` | เส้น gridline อ่อน | `#F3F2F1` | `#3A3A5C` |
| `fourthLevelElements` | placeholder, disabled text | `#B3B0AD` | `#606080` |
| `tableAccent` | สี accent ของตาราง | `#118DFF` | `#00D4FF` |

#### วิธีใส่ Theme ใน PBIP Project

Theme สามารถใส่ใน `report.json` → `config` (stringified) → `themeCollection`:

```json
{
  "themeCollection": {
    "baseTheme": {
      "name": "CY24SU11",
      "version": {"visual": "2.6.0", "report": "3.1.0", "page": "2.3.0"},
      "type": 2
    },
    "customTheme": {
      "name": "My Corporate Theme",
      "dataColors": ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B"],
      "background": "#FFFFFF",
      "foreground": "#333333",
      "tableAccent": "#2E86AB"
    }
  }
}
```

> 💡 **Tip**: เปลี่ยนแค่ `dataColors` + `background` + `foreground` ก็ทำให้ dashboard ดูต่างจากเดิมมากแล้ว

---

### 2. Professional Color Palettes

> 🎯 Color palette ที่ดีทำให้ dashboard ดู professional ทันที — เลือกตามอุตสาหกรรมหรือ mood ที่ต้องการ

#### 🔵 Light Theme Palettes

| ชื่อ | dataColors (Hex) | เหมาะกับ |
|------|-----------------|----------|
| **Corporate Blue** | `#2E86AB, #A23B72, #F18F01, #C73E1D, #3B1F2B, #1B998B, #FF6B6B, #4ECDC4` | Enterprise, Finance |
| **Ocean Breeze** | `#0077B6, #00B4D8, #90E0EF, #CAF0F8, #023E8A, #48CAE4, #0096C7, #ADE8F4` | Healthcare, Tech |
| **Sunset Warm** | `#FF6B35, #F7C59F, #EFEFD0, #004E89, #1A659E, #FF9F1C, #E07A5F, #81B29A` | Marketing, Creative |
| **Forest Green** | `#2D6A4F, #40916C, #52B788, #74C69D, #95D5B2, #B7E4C7, #1B4332, #D8F3DC` | Agriculture, ESG |
| **Executive Gray** | `#2B2D42, #8D99AE, #EDF2F4, #EF233C, #D90429, #374151, #6B7280, #9CA3AF` | C-Suite, BI |

#### 🌙 Dark Theme Palettes

| ชื่อ | background | foreground | dataColors (Hex) |
|------|-----------|-----------|------------------|
| **Midnight Pro** | `#1B1B2F` | `#E0E0E0` | `#00D4FF, #FF6B6B, #4ECDC4, #FFE66D, #A855F7, #F97316, #06B6D4, #EC4899` |
| **Charcoal** | `#2D2D2D` | `#F5F5F5` | `#60A5FA, #F472B6, #34D399, #FBBF24, #A78BFA, #FB923C, #2DD4BF, #F87171` |
| **Navy Night** | `#0F172A` | `#E2E8F0` | `#38BDF8, #FB7185, #4ADE80, #FACC15, #C084FC, #FB923C, #22D3EE, #F43F5E` |

> ⚠️ **Dark Theme Tips**:
> - ❌ อย่าใช้ `#000000` (ดำสนิท) — ใช้ deep gray/navy แทน เช่น `#1B1B2F`, `#2D2D2D`
> - ✅ ให้ visual containers สว่างกว่า background เล็กน้อย → สร้าง depth
> - ✅ ใช้สี accent ที่สดใสเพื่อ contrast กับพื้นหลังเข้ม
> - ✅ ตรวจ contrast ratio ≥ 4.5:1 ระหว่าง text กับ background

#### 🚦 Sentiment & Status Colors

| สถานะ | Light Theme | Dark Theme | ใช้กับ |
|--------|-----------|-----------|--------|
| ✅ Good/Positive | `#1AAB40` | `#4ADE80` | KPI บวก, On-target |
| ⚠️ Neutral/Warning | `#D9B300` | `#FBBF24` | ค่ากลาง, Near-miss |
| ❌ Bad/Negative | `#D64554` | `#F87171` | KPI ลบ, Off-target |

---

### 3. Visual Container Formatting (vcObjects Deep Dive)

> ⚠️ `vcObjects` คือ key สำหรับตกแต่ง visual แต่ละตัวใน `report.json` — ควบคุม title, background, border, shadow

#### 3.1 Background

```json
"vcObjects": {
  "background": [{
    "properties": {
      "show": {"expr": {"Literal": {"Value": "true"}}},
      "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
      "transparency": {"expr": {"Literal": {"Value": "0D"}}}
    }
  }]
}
```

| Property | ค่า | คำอธิบาย |
|----------|-----|--------|
| `show` | `true`/`false` | แสดง/ซ่อนพื้นหลัง |
| `color` | Hex เช่น `'#F8F9FA'` | สีพื้นหลัง |
| `transparency` | `0D` - `100D` | ความโปร่งใส (0=ทึบ, 100=โปร่งใส) |

#### 3.2 Border & Rounded Corners

```json
"vcObjects": {
  "border": [{
    "properties": {
      "show": {"expr": {"Literal": {"Value": "true"}}},
      "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E0E0E0'"}}}}},
      "radius": {"expr": {"Literal": {"Value": "10D"}}},
      "width": {"expr": {"Literal": {"Value": "1D"}}}
    }
  }]
}
```

| Property | ค่าแนะนำ | ผลลัพธ์ |
|----------|---------|--------|
| `radius` | `0D` | มุมเหลี่ยม (default) |
| `radius` | `5D` - `8D` | มุมมนเล็กน้อย (subtle) |
| `radius` | `10D` - `15D` | มุมมน modern ✅ แนะนำ |
| `radius` | `20D`+ | มุมมนมาก (pill shape) |
| `width` | `1D` | ขอบบาง (subtle) |
| `width` | `2D` | ขอบปกติ |
| `color` | `'#E0E0E0'` | เทาอ่อน (light theme) |
| `color` | `'#3A3A5C'` | เทาเข้ม (dark theme) |

#### 3.3 Drop Shadow

```json
"vcObjects": {
  "dropShadow": [{
    "properties": {
      "show": {"expr": {"Literal": {"Value": "true"}}},
      "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#00000020'"}}}}},
      "position": {"expr": {"Literal": {"Value": "'Outer'"}}},
      "preset": {"expr": {"Literal": {"Value": "'BottomRight'"}}},
      "shadowSpread": {"expr": {"Literal": {"Value": "0D"}}},
      "shadowBlur": {"expr": {"Literal": {"Value": "10D"}}},
      "shadowDistance": {"expr": {"Literal": {"Value": "3D"}}},
      "shadowAngle": {"expr": {"Literal": {"Value": "135D"}}},
      "transparency": {"expr": {"Literal": {"Value": "60D"}}}
    }
  }]
}
```

| Property | ค่าแนะนำ | คำอธิบาย |
|----------|---------|--------|
| `position` | `'Outer'` / `'Inner'` | เงาด้านนอก/ด้านใน |
| `preset` | `'BottomRight'` / `'Bottom'` / `'Custom'` | ตำแหน่ง preset |
| `shadowBlur` | `5D` - `15D` | ความเบลอ (ยิ่งสูง ยิ่งนุ่ม) |
| `shadowDistance` | `2D` - `5D` | ระยะห่างเงา |
| `shadowAngle` | `135D` | มุมเงา (135° = ขวาล่าง) |
| `transparency` | `40D` - `70D` | ความจาง (ยิ่งสูง ยิ่งจาง) |

> 💡 **Pro-Tip**: เงาอ่อนๆ (`blur: 10, transparency: 60`) ทำให้ visual ดูลอยขึ้นจาก background อย่าง subtle — ดูดีมากกว่าเงาหนักๆ

#### 3.4 Visual Title Formatting

```json
"vcObjects": {
  "title": [{
    "properties": {
      "show": {"expr": {"Literal": {"Value": "true"}}},
      "text": {"expr": {"Literal": {"Value": "'Revenue by Month'"}}},
      "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#333333'"}}}}},
      "fontSize": {"expr": {"Literal": {"Value": "14D"}}},
      "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI Semibold'"}}},
      "alignment": {"expr": {"Literal": {"Value": "'left'"}}}
    }
  }]
}
```

#### 3.5 Complete "Modern Card" Example

ตัวอย่างการรวม vcObjects ทุกตัว สำหรับ card visual ที่ดูสวย:

```json
"vcObjects": {
  "title": [{
    "properties": {
      "show": {"expr": {"Literal": {"Value": "true"}}},
      "text": {"expr": {"Literal": {"Value": "'Total Revenue'"}}},
      "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#605E5C'"}}}}},
      "fontSize": {"expr": {"Literal": {"Value": "10D"}}}
    }
  }],
  "background": [{
    "properties": {
      "show": {"expr": {"Literal": {"Value": "true"}}},
      "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
      "transparency": {"expr": {"Literal": {"Value": "0D"}}}
    }
  }],
  "border": [{
    "properties": {
      "show": {"expr": {"Literal": {"Value": "true"}}},
      "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E8E8E8'"}}}}},
      "radius": {"expr": {"Literal": {"Value": "12D"}}},
      "width": {"expr": {"Literal": {"Value": "1D"}}}
    }
  }],
  "dropShadow": [{
    "properties": {
      "show": {"expr": {"Literal": {"Value": "true"}}},
      "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#00000015'"}}}}},
      "position": {"expr": {"Literal": {"Value": "'Outer'"}}},
      "preset": {"expr": {"Literal": {"Value": "'BottomRight'"}}},
      "shadowBlur": {"expr": {"Literal": {"Value": "8D"}}},
      "shadowDistance": {"expr": {"Literal": {"Value": "2D"}}},
      "transparency": {"expr": {"Literal": {"Value": "70D"}}}
    }
  }]
}
```

---

### 4. Typography & Text Formatting

> 🔤 Typography ที่ดีทำให้ dashboard อ่านง่ายและดูมีระดับ

#### Text Classes (ใน Theme JSON)

| Class | หน้าที่ | ขนาดแนะนำ | Font แนะนำ |
|-------|--------|----------|----------|
| `callout` | ตัวเลข KPI ใน Card | 28-45pt | **DIN**, Segoe UI Bold |
| `title` | หัวข้อ visual, axis titles | 12-14pt | **DIN**, Segoe UI Semibold |
| `header` | Tab headers, column headers | 12pt | **Segoe UI Semibold** |
| `label` | Values ใน table, data labels | 10-12pt | **Segoe UI** |

#### Font Recommendations

| Font | ลักษณะ | เหมาะกับ |
|------|--------|----------|
| **Segoe UI** | PBI default, อ่านง่าย | ทุก element |
| **DIN** | Clean, modern, geometric | KPI numbers, titles |
| **Segoe UI Semibold** | เน้น important text | Headers, titles |
| **Segoe UI Light** | บาง elegant | Subtitles, footnotes |

> ⚠️ **กฎ**: ใช้ไม่เกิน **2 font families** ต่อ report (เช่น DIN สำหรับ numbers + Segoe UI สำหรับ text)

#### ขนาดตัวอักษรตาม Element

```
Page Title:     20-24pt  ██████████████████████████
KPI Number:     28-45pt  ████████████████████████████████████████████
Visual Title:   12-14pt  ██████████████
Axis Labels:    10-12pt  █████████████
Data Labels:    10-11pt  ████████████
Footnotes:       8-9pt   █████████
```

---

### 5. Page Background & Canvas Styling

#### Page Background Color

Page background ตั้งใน section config ของ `report.json`:

```json
{
  "config": "{\"background\":{\"color\":{\"solid\":{\"color\":\"#F5F5F5\"}},\"transparency\":0}}",
  "displayName": "Overview",
  "height": 720.0,
  "width": 1280.0
}
```

| Pattern | Page BG | Visual BG | ผลลัพธ์ |
|---------|---------|----------|--------|
| **Classic White** | `#FFFFFF` | `#FFFFFF` | สะอาด ง่าย |
| **Soft Gray** ✅ | `#F0F0F0` / `#F5F5F5` | `#FFFFFF` | Visuals ลอยขึ้น — modern |
| **Light Blue-Gray** | `#EBF0F5` | `#FFFFFF` | Corporate, professional |
| **Dark** | `#1B1B2F` | `#252542` | Premium, modern |

> 💡 **Best Practice**: ใช้ page background สีเทาอ่อน + visual background สีขาว → สร้าง **depth** ให้ visuals ดูลอยขึ้นจาก page — เทคนิคนี้ทำให้ dashboard ดูดีขึ้นทันทีโดยแทบไม่ต้องทำอะไรเพิ่ม

#### Layered Design Pattern ด้วย Shape Backgrounds

ใช้ `shape` visual เป็น background layer เพื่อจัดกลุ่ม visuals:

```json
{
  "config": "{\"name\":\"bg_kpi_section\",\"layouts\":[{\"id\":0,\"position\":{\"x\":10,\"y\":65,\"width\":1260,\"height\":120,\"z\":0,\"tabOrder\":0}}],\"singleVisual\":{\"visualType\":\"shape\",\"objects\":{\"general\":[{\"properties\":{\"fillColor\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#FFFFFF'\"}}}}}}}],\"line\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"roundedCorner\":[{\"properties\":{\"radius\":{\"expr\":{\"Literal\":{\"Value\":\"12D\"}}}}}]}}}",
  "filters": "[]",
  "height": 120.0,
  "width": 1260.0,
  "x": 10.0,
  "y": 65.0,
  "z": 0.0
}
```

> วาง shape (z=0) ไว้ด้านหลัง แล้ว visuals จริง (z=1000+) อยู่ด้านบน → สร้าง grouped sections ที่สวยงาม

---

### 6. Ready-to-Use Theme Templates

> ✅ Copy-paste ได้เลย — ใช้ใน `themeCollection.customTheme` ของ report config

#### 🔵 Corporate Blue (Professional/Enterprise)

```json
{
  "name": "Corporate Blue",
  "dataColors": ["#2E86AB", "#1B4965", "#5FA8D3", "#62B6CB", "#BEE9E8", "#CAE9FF", "#1B998B", "#A23B72"],
  "good": "#1AAB40",
  "neutral": "#D9B300",
  "bad": "#D64554",
  "maximum": "#2E86AB",
  "center": "#BEE9E8",
  "minimum": "#FFFFFF",
  "background": "#F5F7FA",
  "secondaryBackground": "#FFFFFF",
  "foreground": "#1B4965",
  "firstLevelElements": "#1B4965",
  "secondLevelElements": "#5A7D9A",
  "thirdLevelElements": "#E8EDF2",
  "fourthLevelElements": "#A0B4C8",
  "tableAccent": "#2E86AB",
  "textClasses": {
    "callout": {"fontSize": 32, "fontFace": "DIN", "color": "#1B4965"},
    "title":   {"fontSize": 12, "fontFace": "Segoe UI Semibold", "color": "#1B4965"},
    "header":  {"fontSize": 12, "fontFace": "Segoe UI Semibold", "color": "#1B4965"},
    "label":   {"fontSize": 10, "fontFace": "Segoe UI", "color": "#5A7D9A"}
  },
  "visualStyles": {
    "*": {
      "*": {
        "border":     [{"show": true, "color": {"solid": {"color": "#E8EDF2"}}, "radius": 10}],
        "dropShadow": [{"show": true, "color": {"solid": {"color": "#1B496510"}}, "position": "Outer", "preset": "BottomRight"}],
        "background": [{"show": true, "color": {"solid": {"color": "#FFFFFF"}}, "transparency": 0}]
      }
    }
  }
}
```

#### 🌙 Modern Dark (Dark Mode Premium)

```json
{
  "name": "Modern Dark",
  "dataColors": ["#00D4FF", "#FF6B6B", "#4ECDC4", "#FFE66D", "#A855F7", "#F97316", "#06B6D4", "#EC4899"],
  "good": "#4ADE80",
  "neutral": "#FBBF24",
  "bad": "#F87171",
  "maximum": "#00D4FF",
  "center": "#FFE66D",
  "minimum": "#1E1E3F",
  "background": "#1B1B2F",
  "secondaryBackground": "#252542",
  "foreground": "#E0E0E0",
  "firstLevelElements": "#FFFFFF",
  "secondLevelElements": "#A0A0C0",
  "thirdLevelElements": "#3A3A5C",
  "fourthLevelElements": "#606080",
  "tableAccent": "#00D4FF",
  "textClasses": {
    "callout": {"fontSize": 32, "fontFace": "DIN", "color": "#FFFFFF"},
    "title":   {"fontSize": 12, "fontFace": "Segoe UI Semibold", "color": "#E0E0E0"},
    "header":  {"fontSize": 12, "fontFace": "Segoe UI Semibold", "color": "#FFFFFF"},
    "label":   {"fontSize": 10, "fontFace": "Segoe UI", "color": "#A0A0C0"}
  },
  "visualStyles": {
    "*": {
      "*": {
        "border":     [{"show": true, "color": {"solid": {"color": "#3A3A5C"}}, "radius": 12}],
        "dropShadow": [{"show": true, "color": {"solid": {"color": "#00000040"}}, "position": "Outer", "preset": "BottomRight"}],
        "background": [{"show": true, "color": {"solid": {"color": "#252542"}}, "transparency": 0}]
      }
    }
  }
}
```

#### 🎨 Vibrant Analytics (Colorful/Modern)

```json
{
  "name": "Vibrant Analytics",
  "dataColors": ["#6366F1", "#EC4899", "#14B8A6", "#F59E0B", "#8B5CF6", "#EF4444", "#06B6D4", "#84CC16"],
  "good": "#22C55E",
  "neutral": "#EAB308",
  "bad": "#EF4444",
  "maximum": "#6366F1",
  "center": "#F59E0B",
  "minimum": "#F8FAFC",
  "background": "#F8FAFC",
  "secondaryBackground": "#FFFFFF",
  "foreground": "#1E293B",
  "firstLevelElements": "#1E293B",
  "secondLevelElements": "#64748B",
  "thirdLevelElements": "#E2E8F0",
  "fourthLevelElements": "#94A3B8",
  "tableAccent": "#6366F1",
  "textClasses": {
    "callout": {"fontSize": 36, "fontFace": "DIN", "color": "#1E293B"},
    "title":   {"fontSize": 13, "fontFace": "Segoe UI Semibold", "color": "#1E293B"},
    "header":  {"fontSize": 12, "fontFace": "Segoe UI Semibold", "color": "#1E293B"},
    "label":   {"fontSize": 10, "fontFace": "Segoe UI", "color": "#64748B"}
  },
  "visualStyles": {
    "*": {
      "*": {
        "border":     [{"show": true, "color": {"solid": {"color": "#E2E8F0"}}, "radius": 14}],
        "dropShadow": [{"show": true, "color": {"solid": {"color": "#6366F115"}}, "position": "Outer", "preset": "BottomRight"}],
        "background": [{"show": true, "color": {"solid": {"color": "#FFFFFF"}}, "transparency": 0}]
      }
    }
  }
}
```

#### 🎯 Theme Selection Guide

| สถานการณ์ | Theme แนะนำ | เหตุผล |
|-----------|------------|--------|
| รายงานผู้บริหาร | **Corporate Blue** | สะอาด professional เชื่อถือได้ |
| Dashboard ภายในทีม | **Vibrant Analytics** | สีสดใส อ่านง่าย engage |
| Presentation / Demo | **Modern Dark** | ดูหรูหรา eye-catching |
| Healthcare / Finance | **Corporate Blue** | conservative เหมาะกับ formal |
| Marketing / Creative | **Vibrant Analytics** | สีสัน dynamic |
| IT / Analytics | **Modern Dark** | ดู tech-savvy modern |

### 💡 Pro-Tips: Dashboard Beautification

| # | Tip | รายละเอียด |
|---|-----|----------|
| 1 | **Soft Background** | ใช้ page BG `#F0F0F0` + visual BG `#FFFFFF` → visual ลอยขึ้นทันที |
| 2 | **Rounded Corners** | `radius: 10-12` ทุก visual → ดู modern |
| 3 | **Subtle Shadow** | `blur: 8, transparency: 70` → depth โดยไม่ overwhelming |
| 4 | **2 Fonts Max** | DIN (numbers) + Segoe UI (text) → สะอาดตา |
| 5 | **Color Hierarchy** | สี accent 1 สี + สีเทาเป็นหลัก → ดู professional |
| 6 | **Group with Shapes** | ใช้ shape visual เป็น background grouping → จัดหมวดหมู่ visuals |
| 7 | **Consistent Spacing** | ระยะห่างระหว่าง visuals เท่ากันทุกที่ (20px) |
| 8 | **KPI Color Coding** | เขียว=ดี, แดง=แย่, เหลือง=ปกติ → อ่านค่าได้ทันที |
| 9 | **Hide Visual Borders** | ถ้าใช้ shadow แล้ว ไม่ต้องใช้ border — เลือกอย่างใดอย่างหนึ่ง |
| 10 | **Title Subtitle Pattern** | Title bold + subtitle สีเทาอ่อน → hierarchy ที่ชัดเจน |

---

## Example: Complete Card Visual

> ดูไฟล์ `generate.py` สำหรับ functions ครบทุก visual type (14 functions + auto-dashboard)

---

## Calculated Tables & Columns (model.bim)

### Calculated Column
```json
{
  "name": "ProfitMargin",
  "dataType": "double",
  "isDataTypeInferred": true,
  "expression": "DIVIDE('Sales'[Profit], 'Sales'[Revenue], 0)",
  "type": "calculated"
}
```

### Calculated Table (Calendar)
```json
{
  "name": "Calendar",
  "columns": [
    {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date", "isKey": true},
    {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
    {"name": "Month", "dataType": "string", "sourceColumn": "Month"},
    {"name": "Quarter", "dataType": "string", "sourceColumn": "Quarter"}
  ],
  "partitions": [{
    "name": "Calendar",
    "mode": "import",
    "source": {
      "type": "calculated",
      "expression": "CALENDAR(DATE(2020,1,1), DATE(2026,12,31))"
    }
  }]
}
```

> **Auto-gen Calendar DAX**:
> ```dax
> Calendar = ADDCOLUMNS(
>   CALENDAR(DATE(2020,1,1), DATE(2026,12,31)),
>   "Year", YEAR([Date]), "Month", FORMAT([Date],"MMMM"),
>   "MonthNum", MONTH([Date]), "Quarter", "Q" & QUARTER([Date]),
>   "Weekday", FORMAT([Date],"dddd"), "WeekNum", WEEKNUM([Date])
> )
> ```

---

## Hierarchies (model.bim)

```json
{
  "name": "Calendar",
  "columns": [...],
  "hierarchies": [
    {
      "name": "DateHierarchy",
      "levels": [
        {"name": "Year", "column": "Year", "ordinal": 0},
        {"name": "Quarter", "column": "Quarter", "ordinal": 1},
        {"name": "Month", "column": "Month", "ordinal": 2},
        {"name": "Date", "column": "Date", "ordinal": 3}
      ]
    }
  ]
}
```

### Geography Hierarchy
```json
{
  "name": "GeoHierarchy",
  "levels": [
    {"name": "Country", "column": "country", "ordinal": 0},
    {"name": "Region", "column": "region", "ordinal": 1},
    {"name": "City", "column": "city", "ordinal": 2}
  ]
}
```

---

## Incremental Refresh Policy (model.bim)

```json
{
  "name": "Sales",
  "refreshPolicy": {
    "policyType": "basic",
    "sourceExpression": [...],
    "incrementalGranularity": "day",
    "incrementalPeriods": 30,
    "incrementalPeriodsOffset": -1,
    "rollingWindowGranularity": "month",
    "rollingWindowPeriods": 12,
    "mode": "import"
  }
}
```

> ⚠️ ต้องมี parameters `RangeStart` + `RangeEnd` (type `dateTime`) ในตาราง

---

## M Query Transforms

### Merge (JOIN)
```m
let
  Sales = ...,
  Products = ...,
  Merged = Table.NestedJoin(Sales, "product_id", Products, "id", "Products", JoinKind.LeftOuter),
  Expanded = Table.ExpandTableColumn(Merged, "Products", {"name","category"})
in Expanded
```

### Append (UNION)
```m
let
  Jan = ..., Feb = ...,
  Combined = Table.Combine({Jan, Feb})
in Combined
```

### Pivot / Unpivot
```m
// Pivot: rows → columns
Table.Pivot(Source, List.Distinct(Source[Category]), "Category", "Amount", List.Sum)

// Unpivot: columns → rows
Table.UnpivotOtherColumns(Source, {"Date","Product"}, "Attribute", "Value")
```

### Group By
```m
Table.Group(Source, {"Category"}, {
  {"Total", each List.Sum([Amount]), type number},
  {"Count", each Table.RowCount(_), Int64.Type}
})
```

### Conditional Column
```m
Table.AddColumn(Source, "Status", each
  if [Amount] > 1000 then "High"
  else if [Amount] > 500 then "Medium"
  else "Low", type text)
```

---

## M Query Parameters

### ใน model.bim (expressions section)
```json
{
  "name": "ServerName",
  "kind": "m",
  "expression": ["\"myserver.database.windows.net\" meta [IsParameterQuery=true, Type=\"Text\", IsParameterQueryRequired=true]"]
}
```

### ใน M Query (ใช้ parameter)
```m
let Source = Sql.Database(#"ServerName", #"DatabaseName"),
    Table1 = Source{[Schema="dbo",Item="Sales"]}[Data]
in Table1
```

---

## Advanced DAX — Semi-Additive & Error Handling

```dax
// ---- Semi-Additive (ใช้กับ Balance, Inventory) ----
Closing Balance = CALCULATE(SUM('Inventory'[Qty]),
    LASTDATE('Calendar'[Date]))

Opening Balance = CALCULATE(SUM('Inventory'[Qty]),
    FIRSTDATE('Calendar'[Date]))

// ---- DAX Error Handling ----
Safe Divide = IF(ISBLANK([Denominator]) || [Denominator] = 0,
    BLANK(), [Numerator] / [Denominator])

Safe Lookup = IFERROR(LOOKUPVALUE('Products'[Name],
    'Products'[ID], [ProductID]), "Unknown")

// ---- Dynamic Formatting (returns format string) ----
Revenue Format = IF([Total Revenue] >= 1000000,
    FORMAT([Total Revenue]/1000000, "#,##0.0") & "M",
    IF([Total Revenue] >= 1000,
        FORMAT([Total Revenue]/1000, "#,##0.0") & "K",
        FORMAT([Total Revenue], "#,##0")))

// ---- Calendar Auto-Generate ----
DateTable = ADDCOLUMNS(
    CALENDAR(MIN('Sales'[Date]), MAX('Sales'[Date])),
    "Year", YEAR([Date]),
    "Month", FORMAT([Date], "MMM"),
    "MonthNum", MONTH([Date]),
    "Quarter", "Q" & CEILING(MONTH([Date])/3, 1),
    "DayOfWeek", WEEKDAY([Date]),
    "IsWeekend", IF(WEEKDAY([Date]) IN {1,7}, TRUE, FALSE),
    "FiscalYear", IF(MONTH([Date]) >= 10, YEAR([Date])+1, YEAR([Date]))
)

// ---- Period Comparison ----
vs Last Period = [Total Revenue] -
    CALCULATE([Total Revenue], DATEADD('Calendar'[Date], -1, MONTH))

vs Same Period Last Year = [Total Revenue] -
    CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Calendar'[Date]))

// ---- ABC Analysis ----
ABC Class = 
VAR CumPct = [Cumulative Pct]
RETURN SWITCH(TRUE(),
    CumPct <= 0.8, "A",
    CumPct <= 0.95, "B",
    "C")
```

---

## Accessibility (report.json)

### Alt Text สำหรับ visual
```json
"vcObjects": {
  "general": [{
    "properties": {
      "altText": {"expr": {"Literal": {"Value": "'Revenue trend showing 15% growth over 12 months'"}}}
    }
  }]
}
```

### Tab Order
```json
"layouts": [{
  "id": 0,
  "position": {"x":20, "y":10, "width":600, "height":300, "z":1000,
    "tabOrder": 1}
}]
```

> **กฎ Accessibility**:
> - ทุก visual ต้องมี `altText` ที่อธิบายข้อมูล
> - `tabOrder` เรียงจากสำคัญ → รายละเอียด (1,2,3...)
> - ใช้ contrast ratio ≥ 4.5:1 สำหรับ text
> - หลีกเลี่ยง red+green only (color blind)
> - ใช้ title ที่ชัดเจนทุก visual

---

## Responsive Layout

### Mobile Layout (report.json page config)
```json
{
  "config": "{\"layouts\":[{\"id\":0},{\"id\":1}]}",
  "displayName": "Overview",
  "mobileState": {
    "mobileVisuals": [
      {"visualName": "<hex_id>", "x": 0, "y": 0, "width": 360, "height": 100},
      {"visualName": "<hex_id>", "x": 0, "y": 110, "width": 360, "height": 200}
    ]
  }
}
```

> ⚠️ Mobile layout เป็น **separate layer** — ไม่กระทบ desktop layout
> แนะนำ: จัดเรียง visuals เป็น 1 column, width=360

### Canvas Sizes
| Target | Width × Height |
|--------|---------------|
| **16:9 (default)** | 1280 × 720 |
| **4:3** | 1280 × 960 |
| **Letter** | 816 × 1056 |
| **Mobile (custom)** | 360 × 640 |

---

## Custom Visuals Reference

### ใช้ Custom Visual จาก Marketplace
```json
{
  "singleVisual": {
    "visualType": "wordCloud1447959067750",
    "projections": {
      "Category": [{"queryRef": "table.word"}],
      "Values": [{"queryRef": "Count(table.word)"}]
    }
  }
}
```

### Custom Visual Types ที่นิยม

| Visual Type ID | ชื่อ | ใช้ทำอะไร |
|---------------|------|----------|
| `wordCloud1447959067750` | Word Cloud | วิเคราะห์ text frequency |
| `infographic1501606498498` | Infographic Designer | data storytelling |
| `chicletSlicer1446647963903` | Chiclet Slicer | slicer แบบปุ่ม |
| `bulletChart1487364913498` | Bullet Chart | actual vs target |
| `sunburstChart1` | Sunburst | hierarchical composition |
| `timeline1` | Timeline Slicer | date range filter |
| `advancedCardVisual` | Advanced Card | card with sparkline |

> ⚠️ Custom visuals ต้อง **register ใน PBI Desktop ก่อน** (Import from marketplace)
> Visual Type ID หาได้จาก `report.json` หลัง save

---

## Power Automate Integration

### Data Alert (ใน Power BI Service)
```json
{
  "alertCondition": {
    "measure": "Total Revenue",
    "threshold": 100000,
    "direction": "above",
    "frequency": "daily"
  },
  "action": {
    "type": "powerAutomate",
    "flowId": "<flow-guid>",
    "notification": {
      "email": "user@company.com",
      "teams": "#channel-alerts"
    }
  }
}
```

> ⚠️ Config นี้ตั้งผ่าน Power BI Service > Dashboard > Alert — ไม่ใช่ใน PBIP files
> Power Automate connector: `Power BI` trigger → `When a data-driven alert is triggered`

---

## Q&A Visual Config

```json
{
  "singleVisual": {
    "visualType": "qnaVisual",
    "projections": {},
    "objects": {
      "question": [{
        "properties": {
          "question": {"expr": {"Literal": {"Value": "'What is total revenue by city?'"}}}
        }
      }]
    }
  }
}
```

### Smart Narrative
```json
{
  "singleVisual": {
    "visualType": "smartNarrativeVisual",
    "projections": {"Values": [{"queryRef": "Sum(table.revenue)"}]},
    "prototypeQuery": {"Version": 2, "From": [...], "Select": [...]}
  }
}
```

---

## Animation & Transition Config

### Play Axis (Scatter chart animation)
```json
{
  "singleVisual": {
    "visualType": "scatterChart",
    "projections": {
      "X": [...], "Y": [...], "Size": [...],
      "Play": [{"queryRef": "table.year"}]
    }
  }
}
```

### Visual Animation Settings
```json
"vcObjects": {
  "general": [{
    "properties": {
      "responsive": {"expr": {"Literal": {"Value": "true"}}}
    }
  }]
}
```

---

## Gateway Config Reference

| Setting | ค่า | ใช้เมื่อ |
|---------|-----|---------|
| **Personal Gateway** | `personalCloud` | dev/test |
| **Enterprise Gateway** | `gateway` | production, scheduled refresh |
| **DirectQuery** | `directQuery` | real-time data |

### model.bim — Data Source with Gateway
```json
{
  "dataSources": [{
    "name": "SqlServer",
    "connectionString": "Data Source=server;Initial Catalog=db",
    "provider": "System.Data.SqlClient",
    "impersonationMode": "impersonateServiceAccount"
  }]
}
```

---

## ⏱️ Performance Analyzer

> ใช้ตรวจสอบว่า visual หรือ DAX ตัวไหนทำงานช้า — ต้องทำก่อนส่งงาน

### วิธีเปิด
`View tab → Performance Analyzer → Start recording → Refresh visuals`

### ตีความผลลัพธ์

| Metric | ค่าปกติ | ค่าที่ต้องแก้ | วิธีแก้ |
|--------|--------|-------------|--------|
| **DAX Query** | < 100ms | > 500ms | ปรับสูตร DAX (ใช้ VAR, ลด CALCULATE ซ้อน) |
| **Visual Display** | < 50ms | > 200ms | ลดจำนวน data points, ลด visual complexity |
| **Other** | < 50ms | > 100ms | ตรวจ filter interactions, ลด cross-filtering |
| **Direct Query** | < 2s | > 5s | เพิ่ม index ที่ database, ลด columns ที่ดึง |

### แก้ปัญหา Performance ที่พบบ่อย

| ปัญหา | สาเหตุ | วิธีแก้ |
|--------|--------|--------|
| Dashboard โหลดช้า > 5s | visual เยอะเกิน | ลดเหลือ ≤ 8 visuals ต่อหน้า |
| DAX query ช้า | CALCULATE ซ้อนกันหลายชั้น | ใช้ VAR แยกขั้นตอน |
| Slicer ช้า | Column มีค่า unique เยอะ (> 10K) | ลด cardinality, ใช้ range slicer |
| Matrix ช้า | แสดง rows เยอะเกินไป | ใช้ TOPN() จำกัด, ซ่อน subtotals |
| ไฟล์ .pbix ใหญ่ | import ข้อมูลเยอะเกิน | ลบ columns ที่ไม่ใช้, ลดแถว |

> 💡 **เป้าหมาย**: ทุก visual render ภายใน 200ms, ทั้งหน้าภายใน 3 วินาที

### VertiPaq Analyzer

> ⭐ เครื่องมือ advanced สำหรับวิเคราะห์ว่า **column ไหนกินพื้นที่ memory มากที่สุด**

**วิธีใช้:** เปิดผ่าน DAX Studio → `Advanced > View Metrics` หรือ Tabular Editor → `Advanced Scripting`

| สิ่งที่ตรวจ | ปัญหาที่พบ | วิธีแก้ |
|-----------|-----------|--------|
| **Column ที่กิน memory สูงสุด** | Text column ยาว, high cardinality | ลบออกถ้าไม่ใช้, ย่อความยาว |
| **High cardinality columns** | ID, Timestamp ละเอียดถึงวินาที | ใช้ DateKey แทน full datetime |
| **Unused columns ที่ยัง import** | กิน memory เปล่า | ลบออกใน Power Query |
| **Dictionary size ใหญ่** | ค่าไม่ซ้ำกันเยอะเกิน | Group/bucket ค่าที่ใกล้เคียง |

---

## ✅ Final Delivery Checklist

> ⚠️ **ตรวจสอบทุกครั้งก่อนส่งงาน** — ป้องกันปัญหาที่พบบ่อยที่สุด

### 🔄 Data & Refresh

- [ ] ข้อมูลรีเฟรชได้ปกติไม่มี Error?
- [ ] Data source path ถูกต้อง (ไม่ใช่ local path ที่ใช้ไม่ได้บน Service)?
- [ ] Incremental refresh ตั้งค่าถูกต้อง (ถ้าใช้)?
- [ ] Gateway เชื่อมต่อได้ปกติ (สำหรับ on-premises data)?

### 🔢 Data Accuracy

- [ ] ตัวเลขในรายงานตรงกับแหล่งข้อมูลดิบ? (cross-validate อย่างน้อย 3 ตัวเลข)
- [ ] Measures คำนวณถูกต้องเมื่อ filter เปลี่ยน?
- [ ] ไม่มี double-counting จาก relationship ที่ผิด?
- [ ] Grand Total / Subtotal แสดงผลถูกต้อง?

### 🏗️ Data Model

- [ ] ใช้ Star Schema (Fact + Dimension แยกกัน)?
- [ ] Relationships เป็น One-to-Many ทั้งหมด (ไม่มี Many-to-Many ที่ไม่จำเป็น)?
- [ ] มี Calendar/Date Table สำหรับ Time Intelligence?
- [ ] Data types ถูกต้องทุกคอลัมน์ (Date=dateTime, Number=int64/double)?
- [ ] ไม่มี unused columns/tables ที่เพิ่มขนาดไฟล์?

### 📐 DAX Quality

- [ ] ใช้ Measures แทน Calculated Columns สำหรับ aggregation?
- [ ] สูตร DAX มี formatting ที่อ่านง่าย (indentation, VAR)?
- [ ] สูตรซับซ้อนมี comment อธิบาย?
- [ ] DIVIDE() ใช้แทน `/` เพื่อป้องกัน division by zero?

### 🎨 Visualization

- [ ] กราฟทุกตัวมีชื่อหัวข้อ (Title) ที่ชัดเจน?
- [ ] แกน X/Y มี label ที่เข้าใจได้?
- [ ] สีสม่ำเสมอ — สีเดียวกันหมายถึงสิ่งเดียวกันทั้ง dashboard?
- [ ] ไม่มีกราฟเกิน 8 ตัวต่อหน้า?
- [ ] Tooltip มีข้อมูลเพิ่มเติมที่เป็นประโยชน์?

### 🔍 Filters & Slicers

- [ ] ตั้งค่า Slicers ครบถ้วนตามความต้องการของผู้ใช้?
- [ ] Slicer มีค่า default ที่เหมาะสม?
- [ ] Filter interactions ระหว่าง visuals ถูกต้อง?
- [ ] Page-level / Report-level filters ตั้งค่าถูกต้อง?

### ♿ Accessibility

- [ ] ทุก visual มี Alt Text?
- [ ] Tab Order เรียงลำดับถูกต้อง?
- [ ] Contrast ratio ≥ 4.5:1 สำหรับ text?
- [ ] ไม่ใช้สี Red+Green เพียงอย่างเดียว (color blind)?

### 📱 Responsive & Performance

- [ ] Mobile layout จัดเรียงเรียบร้อย (ถ้าต้องใช้)?
- [ ] Dashboard โหลดภายใน 5 วินาที?
- [ ] ไม่มี visual ที่ใช้เวลา render นานเกินไป?

> 💡 **Tip**: Copy checklist นี้ไปใช้ทุกครั้งก่อนส่งงาน — ช่วยลดปัญหาได้ 90%+

---

## 📝 Documentation & Version Control

> ป้องกันปัญหา "ใครทำอะไร เมื่อไหร่ ทำไม" — สำคัญเมื่อทำงานเป็นทีม

### Measure Documentation

ใส่ description ให้ทุก measure ใน model.bim:
```json
{
  "name": "Total Revenue",
  "expression": "SUM('Sales'[Amount])",
  "formatString": "#,##0.00",
  "description": "ยอดรวมของ Amount ใน Sales table, ตอบสนองต่อ filter ทุกตัว"
}
```

### Report Metadata

| สิ่งที่ต้องบันทึก | ตัวอย่าง |
|-----------------|--------|
| **ชื่อรายงาน** | Sales Performance Dashboard |
| **เจ้าของ/ผู้สร้าง** | Data Team / นายก |
| **วันที่สร้าง** | 2026-03-01 |
| **แหล่งข้อมูล** | SQL Server `db_sales.dbo.FactSales` |
| **ความถี่ refresh** | ทุกวัน 06:00 UTC |
| **กลุ่มผู้ใช้** | ผู้บริหาร, ทีมขาย |
| **Measures สำคัญ** | Revenue, Growth %, Target Achievement |
| **ข้อจำกัด** | ข้อมูลย้อนหลังได้ 3 ปี |

### Version Control

| วิธี | เหมาะกับ | ข้อดี |
|------|---------|------|
| **PBIP + Git** ⭐ | ทีม dev, CI/CD | Track changes, branching, PR review |
| **SharePoint** | ทีมทั่วไป | ง่าย, มี version history อัตโนมัติ |
| **OneDrive** | คนเดียว | Auto-backup, ง่ายที่สุด |
| **File naming** | ทุกกรณี | `Report_v1.2_2026-03-01.pbix` |

**PBIP + Git workflow:**
```
1. Save as .pbip (JSON text files)
2. git add → git commit -m "feat: add YoY comparison chart"
3. git push → PR review → merge
4. ทีมอื่น git pull → เปิดใน PBI Desktop
```

> 💡 **PBIP format** เป็น JSON text ทั้งหมด — ทำให้ Git diff เห็นการเปลี่ยนแปลงทุกจุดได้ชัดเจน

---

## 🚀 External Tools (เครื่องมือเสริม)

> เครื่องมือที่ช่วยให้ Power BI workflow เร็วขึ้น 10x — ทั้งหมดเป็น **ฟรี**

| เครื่องมือ | หน้าที่ | ใช้เมื่อ | Link |
|----------|--------|--------|------|
| **Tabular Editor** ⭐ | จัดการ data model, DAX, bulk edit measures | แก้ Measures 50+ ตัว, จัดระเบียบ model | [tabulareditor.com](https://tabulareditor.com) |
| **DAX Studio** ⭐ | ทดสอบ + profile สูตร DAX, ดู query plan | วิเคราะห์สูตรที่ช้า, debug DAX | [daxstudio.org](https://daxstudio.org) |
| **PBI Inspector** | ตรวจสอบ Best Practices อัตโนมัติ | ก่อนส่งงาน, audit dashboard | [pbiinspector.com](https://pbiinspector.com) |
| **ALM Toolkit** | เปรียบเทียบ + merge data models | ย้าย measures ระหว่าง files | [alm-toolkit.com](https://alm-toolkit.com) |
| **Bravo** | จัดการ Date Table, Format DAX | สร้าง Calendar table, format สูตร | [sqlbi.com/bravo](https://sqlbi.com/bravo) |

### Tabular Editor — Quick Start

```
1. ติดตั้ง Tabular Editor 3 (Free/Paid)
2. เปิดใน PBI Desktop: External Tools tab → Tabular Editor
3. แก้ DAX, สร้าง measures, จัด Display Folders
4. บันทึก → กลับไป PBI Desktop (auto-sync)
```

**ข้อดีหลัก:**
- ✅ Bulk edit measures (เปลี่ยน format 50 measures พร้อมกัน)
- ✅ Best Practice Analyzer (ตรวจ model อัตโนมัติ)
- ✅ C# scripting สำหรับ automation
- ✅ คัดลอก measures ระหว่าง files

### DAX Studio — Quick Start

```
1. ติดตั้ง DAX Studio (ฟรี)
2. เปิดใน PBI Desktop: External Tools tab → DAX Studio
3. เขียน DAX query → Run → ดูผลลัพธ์ + timing
4. Server Timings tab → ดูรายละเอียด performance
```

**ฟีเจอร์สำคัญ:**
- ✅ **Server Timings** — เห็น query time แยกรายสูตร
- ✅ **Query Plan** — วิเคราะห์ว่า DAX Engine ทำงานอย่างไร
- ✅ **VertiPaq Analyzer** — ดู memory usage แยกราย column
- ✅ **Export Data** — export ผลลัพธ์เป็น CSV/Excel

> 💡 **แนะนำ**: เริ่มจาก **Tabular Editor** (จัดการ model) + **DAX Studio** (debug DAX) — 2 ตัวนี้เปลี่ยนชีวิตมากที่สุด

---

## 🌟 Advanced: Data Storytelling

> ไม่ใช่แค่วางกราฟ — แต่เป็นการ **"นำทาง"** ผู้ใช้ให้ได้คำตอบและตัดสินใจได้

### Narrative Flow (เล่าเรื่องด้วยข้อมูล)

จัดรายงานให้มีโครงสร้างเหมือน **เรื่องเล่า**:

```
┌─────────────────────────────────────────────────────┐
│  📖 บทนำ (Overview Page)                              │
│  "เกิดอะไรขึ้น?" → KPI Cards + Trend Lines           │
├─────────────────────────────────────────────────────┤
│  🔍 เนื้อหา (Insight Pages)                           │
│  "ทำไมถึงเป็นแบบนี้?" → Drill-down + Comparisons     │
├─────────────────────────────────────────────────────┤
│  🎯 บทสรุป (Action Page)                              │
│  "ควรทำอะไรต่อ?" → Recommendations + Alerts          │
└─────────────────────────────────────────────────────┘
```

| Page | เป้าหมาย | ตัวอย่าง Visual |
|------|---------|----------------|
| **Overview** | ตอบ "เกิดอะไรขึ้น?" | Cards, Trend Line, YoY comparison |
| **Analysis** | ตอบ "ทำไม?" | Waterfall, Decomposition Tree, Scatter |
| **Action** | ตอบ "ทำอะไรต่อ?" | Conditional alerts, Top/Bottom lists |

### Smart Narrative (AI Visual)

> ใช้ AI สรุปข้อมูลเป็น **ภาษาธรรมชาติ** — ผู้บริหารอ่านได้ทันทีไม่ต้องแปลกราฟ

**วิธีใช้:**
1. Insert → More visuals → Smart Narrative
2. ลาก fields ที่ต้องการลงใน visual
3. PBI สร้างข้อความสรุปอัตโนมัติ (ปรับแต่งได้)

**ตัวอย่างข้อความที่สร้าง:**
> "ยอดขายเดือนกุมภาพันธ์ 2026 อยู่ที่ **฿12.5M** เพิ่มขึ้น **15%** จากเดือนก่อน
> สินค้าที่เติบโตมากที่สุดคือ **Electronics (+32%)** ขณะที่ **Clothing (-8%)** ลดลง"

```json
// report.json — Smart Narrative visual config
{
  "visualType": "annotatedTimeline",
  "objects": {
    "smartNarrative": [{
      "properties": {
        "summarizeBy": {"expr": {"Literal": {"Value": "'auto'"}}},
        "fontSize": {"expr": {"Literal": {"Value": "12D"}}}
      }
    }]
  }
}
```

### Conditional Formatting (สื่อสารด้วยสี)

ใช้สีเพื่อบอก **ระดับวิกฤต** โดยอัตโนมัติ:

| สถานการณ์ | เงื่อนไข | สี | Icon |
|-----------|---------|-----|------|
| กำไรสูง | > Target 10% | 🟢 เขียวเข้ม | ▲ |
| ปกติ | ±10% ของ Target | 🟡 เหลือง | ◆ |
| วิกฤต | < Target -10% | 🔴 แดงเข้ม | ▼ ⚠️ |
| ไม่มีข้อมูล | NULL / Blank | ⬜ เทา | — |

**DAX สำหรับ Conditional Color:**
```dax
Color_Performance =
VAR _Actual = [Total Revenue]
VAR _Target = [Target Revenue]
VAR _Pct = DIVIDE(_Actual - _Target, _Target, 0)
RETURN
    SWITCH(TRUE(),
        _Pct >= 0.1, "#2E7D32",      // เขียวเข้ม (เกินเป้า 10%+)
        _Pct >= -0.1, "#F9A825",     // เหลือง (ใกล้เป้า)
        "#C62828"                      // แดง (ต่ำกว่าเป้า 10%+)
    )
```

**report.json — Conditional Formatting:**
```json
{
  "objects": {
    "dataPoint": [{
      "properties": {
        "fill": {
          "solid": {
            "color": {
              "expr": {
                "Measure": {
                  "Expression": {"SourceRef": {"Entity": "_Measures"}},
                  "Property": "Color_Performance"
                }
              }
            }
          }
        }
      }
    }]
  }
}
```

---

## ⚙️ Advanced: Reusable Data Assets

> ลดการทำงานซ้ำซ้อน — สร้างทรัพยากรที่ทั้งองค์กรใช้ร่วมกันได้

### Shared Datasets

> แยก **Model** ออกจาก **Report** — ให้หลายรายงานใช้ Dataset เดียวกัน

```
┌─────────────┐     ┌────────────────┐
│  SQL Server  │────►│  Shared Dataset │
│  (Source)    │     │  (Published)    │
└─────────────┘     └───────┬────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Sales Report │ │ Finance Rpt  │ │ Exec Summary │
    │ (ทีมขาย)     │ │ (ทีมการเงิน)  │ │ (ผู้บริหาร)   │
    └──────────────┘ └──────────────┘ └──────────────┘
```

**ข้อดี:**
- ✅ **ตัวเลขตรงกันทั้งองค์กร** — Single Source of Truth
- ✅ **ลดขนาดไฟล์** — Report ไม่ต้อง import data ซ้ำ
- ✅ **ง่ายต่อการจัดการ** — แก้ Dataset ที่เดียว มีผลทุก Report

**วิธีตั้งค่า:**
```
1. สร้าง .pbix ที่มีเฉพาะ Data Model (ไม่มี Report)
2. Publish ไป Power BI Service
3. Report ใหม่: Get Data → Power BI datasets → เลือก Dataset
4. สร้าง visuals ได้เลย — ข้อมูลมาจาก Dataset กลาง
```

### Dataflows (Power Query Online)

> ทำความสะอาดข้อมูล **ครั้งเดียว** บน Cloud — หลาย Reports มาดึงไปใช้ต่อ

| เปรียบเทียบ | **แบบเดิม** | **Dataflow** |
|------------|------------|--------------|
| Clean data ที่ | ใน Report แต่ละตัว (ซ้ำกัน) | ครั้งเดียวบน Cloud |
| Refresh data | ทุก Report refresh เอง | Dataflow refresh ที่เดียว |
| แก้ไข logic | แก้ทุก Report | แก้ที่ Dataflow ที่เดียว |
| Performance | ช้า (ทำซ้ำหลายรอบ) | เร็ว (ทำครั้งเดียว) |

**วิธีสร้าง:**
```
1. Power BI Service → Workspace → New → Dataflow
2. เลือก Data Source → เขียน Power Query transforms
3. Save + Schedule refresh
4. Report: Get Data → Power BI dataflows → เลือก entities
```

### Theme Files (JSON)

> สร้าง **มาตรฐานสีและรูปแบบ** องค์กร — ทุก Report มี Look & Feel เดียวกัน

```json
// company_theme.json — ตัวอย่าง Custom Theme
{
  "name": "CompanyBrand",
  "dataColors": [
    "#1B5E20", "#388E3C", "#66BB6A",   // Primary greens
    "#1565C0", "#42A5F5",               // Accent blues
    "#FF8F00", "#FFB74D"                // Warning oranges
  ],
  "background": "#FAFAFA",
  "foreground": "#212121",
  "tableAccent": "#1B5E20",
  "visualStyles": {
    "*": {
      "*": {
        "title": [{
          "fontFamily": "Segoe UI Semibold",
          "fontSize": {"expr": {"Literal": {"Value": "14D"}}},
          "fontColor": {"solid": {"color": "#212121"}}
        }],
        "background": [{
          "color": {"solid": {"color": "#FFFFFF"}},
          "transparency": {"expr": {"Literal": {"Value": "0D"}}}
        }]
      }
    }
  }
}
```

**วิธีใช้:** `View → Themes → Browse for themes → เลือก .json file`

**สิ่งที่ Theme ควบคุมได้:**
| หมวด | ตัวอย่าง |
|------|---------|
| **สี** | Data colors, Background, Foreground, Table accent |
| **Font** | Family, Size, Color ของ Title/Label/Value |
| **Visual Style** | Border, Shadow, Padding, Background |
| **Page** | Background color, Wallpaper |

---

## 🛠️ Advanced: Microsoft Ecosystem Integration

> เชื่อมต่อ Power BI เข้ากับ Microsoft เครื่องมืออื่น — จาก Data → Action

### Power Automate Integration

> ใส่ปุ่มใน dashboard ที่เมื่อคลิกแล้ว **ทำ action ทันที** (ส่งอีเมล, อัพเดตระบบ)

| Use Case | Trigger | Action |
|----------|---------|--------|
| ยอดขายต่ำกว่าเป้า | Data-driven alert | ส่ง email แจ้ง Manager |
| สินค้าใกล้หมด | Threshold alert | สร้าง Purchase Order |
| Report refresh สำเร็จ | Refresh complete | แจ้ง Teams channel |
| คลิกปุ่มใน Report | Power Automate button | อัพเดต status ใน SharePoint |

**วิธีตั้งค่า:**
```
1. Power BI Service → Report → Insert → Power Automate button
2. เลือก/สร้าง Flow ที่ต้องการ
3. ตั้งค่า Input parameters (ส่งค่าจาก PBI ไป Flow)
4. Test → Publish
```

### Power Apps Integration (Write-back)

> ฝัง App ใน Power BI เพื่อให้ผู้ใช้ **กรอกข้อมูลกลับ** เข้า Database ได้

| Scenario | ตัวอย่าง |
|----------|---------|
| **Sales Target Input** | ผู้จัดการกรอกเป้าหมายรายเดือนใน PBI |
| **Comment / Annotation** | เพิ่ม comment อธิบายตัวเลขผิดปกติ |
| **Approval Workflow** | อนุมัติรายการจากใน Dashboard |
| **Data Correction** | แก้ไขข้อมูลที่ผิดพลาดจากหน้า Report |

**วิธีตั้งค่า:**
```
1. สร้าง Power App (Canvas App) ที่ connect กับ data source
2. Power BI Desktop → Insert → Power Apps visual
3. เลือก App ที่สร้างไว้
4. ตั้งค่า context fields (ส่งค่า filter จาก PBI → App)
```

### Microsoft Teams Integration

> ฝัง Report ใน Teams — พูดคุยเรื่องข้อมูลในที่เดียวกับการทำงาน

| วิธี | เหมาะกับ | ข้อดี |
|------|---------|------|
| **Tab ใน Channel** | ทีมที่ดู report เดียวกันเป็นประจำ | ทุกคนเข้าถึงได้ทันที |
| **Power BI App** | รวมหลาย reports เข้าด้วยกัน | จัดหมวดหมู่ได้ดี |
| **Chat / Meeting** | แชร์ insight เฉพาะจุด | ส่ง link ไปช่วงเวลาที่เจาะจง |
| **Notification Bot** | แจ้งเตือน data-driven alerts | อัตโนมัติ ไม่ต้อง monitor เอง |

---

## 🏆 Expert Checklist (ตรวจสอบ "ความเป็นโปร")

> ถ้าตอบ ✅ ได้ทุกข้อ — คุณพร้อมสร้างระบบวิเคราะห์ระดับองค์กร

### 📊 Data Lineage (ที่มาของข้อมูล)

- [ ] อธิบายได้ว่าตัวเลขในกราฟ **เดินทางมาจากแหล่งไหน** ผ่านการคำนวณอะไรบ้าง?
- [ ] มี Data Dictionary อธิบาย columns + measures ทุกตัว?
- [ ] มี DAX description ใน model.bim ทุก measure?

### ⚡ Stress Test (ทดสอบภาระงาน)

- [ ] ถ้าข้อมูลเพิ่มขึ้น **10 เท่า** รายงานยังโหลดเร็วอยู่ไหม?
- [ ] Performance Analyzer — ทุก visual < 200ms?
- [ ] VertiPaq Analyzer — ไม่มี column ที่กิน memory เกินจำเป็น?
- [ ] ตั้ง Incremental Refresh สำหรับข้อมูลขนาดใหญ่?

### 🤝 Self-Service Readiness (พร้อมส่งต่อ)

- [ ] ถ้าคุณ **ลาพักร้อน** คนอื่นนำข้อมูลไปใช้ต่อได้หรือไม่?
- [ ] มี Documentation ครบ (Report metadata, Data source, Refresh schedule)?
- [ ] ใช้ Shared Dataset เพื่อ Single Source of Truth?
- [ ] มี Theme File มาตรฐานองค์กร?
- [ ] Version Control (PBIP + Git / SharePoint)?

### 🎯 Business Impact (ผลกระทบต่อธุรกิจ)

- [ ] รายงานช่วย **ตัดสินใจ** ได้จริง (ไม่ใช่แค่ดูสวย)?
- [ ] มี Actionable Insights ไม่ใช่แค่ descriptive statistics?
- [ ] ผู้ใช้ใช้งาน **จริง** (ดู adoption rate ใน PBI Service)?
- [ ] มี feedback loop — รับ input จากผู้ใช้เพื่อปรับปรุง?

> 🌟 **เป้าหมายสูงสุด**: สร้าง **Analytics Ecosystem** ไม่ใช่แค่ Report — จากข้อมูล → Insight → Action → ผลลัพธ์

---

## 🚀 Elite: DevOps for Power BI

> เลิกเซฟไฟล์ทับกัน — ใช้ **Version Control + CI/CD** แบบนักพัฒนาซอฟต์แวร์

### PBIP + Git Workflow (Advanced)

```
                    ┌──────────────┐
                    │  GitHub /    │
                    │  Azure DevOps│
                    └───────┬──────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Developer A │    │  Developer B │    │  Reviewer     │
│  (Branch: A) │    │  (Branch: B) │    │  (PR Review)  │
└──────────────┘    └──────────────┘    └──────────────┘
```

**เทียบกับแบบเดิม:**

| | **แบบเดิม (.pbix)** | **PBIP + Git** |
|---|---------------------|---------------|
| ไฟล์ | Binary 1 ก้อน | JSON text files (หลายไฟล์) |
| ดูการแก้ไข | ❌ ไม่ได้เลย | ✅ Git diff เห็นทุกบรรทัด |
| ทำงานพร้อมกัน | ❌ ต้องส่งไฟล์ทับกัน | ✅ Branch + Merge |
| ย้อนกลับ | ❌ เซฟทับไปแล้ว | ✅ Git revert ได้ทุก commit |
| Code review | ❌ ดูไม่ได้ | ✅ Pull Request review |

### Deployment Pipelines (Dev → Test → Prod)

```
┌──────────┐     ┌──────────┐     ┌──────────────┐
│   DEV    │────►│   TEST   │────►│  PRODUCTION  │
│ (สร้าง)   │     │ (ตรวจสอบ) │     │ (ผู้ใช้จริง)   │
└──────────┘     └──────────┘     └──────────────┘
```

| Stage | ใครใช้ | ทำอะไร |
|-------|--------|--------|
| **Development** | นักพัฒนา | สร้าง/แก้ไขรายงาน, ทดสอบ DAX |
| **Test** | QA / Business User | ตรวจสอบความถูกต้อง, ตรงกับ requirements? |
| **Production** | ผู้ใช้งานจริง | รายงานเสถียร ผ่านการตรวจแล้ว |

**วิธีตั้งค่า:**
```
1. Power BI Service → Settings → Deployment Pipelines
2. สร้าง Pipeline → กำหนด 3 Workspace (Dev/Test/Prod)
3. Deploy: Dev → click "Deploy to test" → review → "Deploy to production"
4. ตั้ง Deployment rules (เช่น เปลี่ยน connection string อัตโนมัติ)
```

### CI/CD Automation

| ขั้นตอน | เครื่องมือ | ทำอะไร |
|---------|----------|--------|
| **Build** | Azure Pipelines / GitHub Actions | ตรวจสอบไฟล์ PBIP valid |
| **Validate** | Tabular Editor / PBI Inspector | เช็ค Best Practices อัตโนมัติ |
| **Test** | DAX Studio (CLI) | รัน DAX queries ตรวจผลลัพธ์ |
| **Deploy** | Power BI REST API | Publish ไป workspace อัตโนมัติ |

**ตัวอย่าง Checks อัตโนมัติ:**
- ✅ ไม่มี column ที่ import แต่ไม่ได้ใช้?
- ✅ ทุก measure มี description?
- ✅ ไม่มี bi-directional relationship?
- ✅ ทุก DAX expression ก valid syntax?
- ✅ File size ไม่เกิน limit?

---

## 🧠 Elite: Advanced Analytics & AI

> ก้าวข้ามการสรุปข้อมูล → **ทำนาย** และ **วิเคราะห์เชิงลึก**

### Python/R Integration

> เขียน Python/R ใน Power BI เพื่อทำสิ่งที่ Power Query/DAX ทำไม่ได้

| Use Case | ภาษา | ตัวอย่าง |
|----------|------|---------|
| **Data Cleaning ซับซ้อน** | Python | Regex, NLP, fuzzy matching |
| **Machine Learning** | Python/R | Forecasting, Clustering, Anomaly Detection |
| **Statistical Analysis** | R | Regression, Hypothesis Testing |
| **Custom Visualization** | Python (matplotlib) | Box Plot, Violin Plot |

**Python Visual ใน PBI:**
```python
# Python script visual — Forecasting
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# dataset = pandas DataFrame จาก PBI (อัตโนมัติ)
X = dataset['month_num'].values.reshape(-1, 1)
y = dataset['revenue'].values

model = LinearRegression().fit(X, y)
future = [[13], [14], [15]]  # ตัวอย่าง: 3 เดือนถัดไป
predicted = model.predict(future)

plt.plot(X, y, 'b-', label='Actual')
plt.plot(future, predicted, 'r--', label='Forecast')
plt.legend()
plt.title('Revenue Forecast')
plt.show()
```

### What-if Parameters

> ให้ผู้ใช้ **ลองปรับค่า** แล้วดูผลกระทบทันที

**วิธีสร้าง:**
`Modeling → New Parameter → ตั้งค่า Min/Max/Step`

**ตัวอย่าง:**

| Parameter | ค่า | Measure ที่ใช้ |
|-----------|-----|--------------|
| Discount % | 0-30% (step 5) | `What_If_Revenue = [Revenue] * (1 - 'Discount %'[Discount % Value])` |
| Price Increase | -10 to +10% | `Simulated_Profit = [Revenue] * (1 + [Price Change]) - [Cost]` |
| Growth Rate | 0-50% | `Projected = [Current] * (1 + [Growth Rate Value])` |

```dax
// DAX — What-if Revenue with discount parameter
What_If_Revenue =
VAR _Discount = SELECTEDVALUE('Discount %'[Discount % Value], 0)
RETURN
    [Total Revenue] * (1 - _Discount)
```

### AI Visuals

| Visual | ทำอะไร | ใช้เมื่อ |
|--------|--------|--------|
| **Key Influencers** | หาปัจจัยที่ส่งผลต่อ metric | "อะไรทำให้ลูกค้า churn?" |
| **Decomposition Tree** | drill-down อัตโนมัติหาสาเหตุ | "ยอดขายตกเพราะอะไร?" |
| **Anomaly Detection** | หาจุดผิดปกติอัตโนมัติ | Line chart ที่มี spike/dip |
| **Q&A Visual** | ถามคำถามภาษาธรรมชาติ | "Show me total revenue by city" |
| **Smart Narrative** | สรุปเป็นข้อความอัตโนมัติ | Executive summary ไม่ต้องเขียนเอง |

**Key Influencers — ตัวอย่าง:**
```
Analyze: "What influences Customer Churn to increase?"
→ Results:
  1. Contract Type = "Month-to-Month" → 3.5x more likely to churn
  2. Monthly Charge > $70 → 2.1x more likely
  3. Tenure < 6 months → 1.8x more likely
```

---

## 🏗️ Elite: Semantic Layer & Fabric

> สถาปัตยกรรมข้อมูลระดับองค์กร — จาก Single Report → Enterprise Analytics

### Microsoft Fabric & OneLake

```
┌──────────────────────────────────────────────────────┐
│                    Microsoft Fabric                   │
├──────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Data Eng  │  │ Data Sci  │  │ Data Analytics   │   │
│  │ (Spark)   │  │ (ML)      │  │ (Power BI)       │   │
│  └─────┬─────┘  └─────┬─────┘  └────────┬─────────┘   │
│        └───────────────┼────────────────┘              │
│                   ┌────▼────┐                          │
│                   │ OneLake │  ← Single Data Lake      │
│                   └─────────┘                          │
└──────────────────────────────────────────────────────┘
```

| เทคโนโลยี | คำอธิบาย | ข้อดี |
|-----------|---------|------|
| **OneLake** | Data Lake กลางขององค์กร | ทุก workload ใช้ข้อมูลชุดเดียวกัน |
| **Direct Lake** | อ่านจาก Lake เร็วเท่า Import | ไม่ต้อง import ซ้ำ (Zero-Copy) |
| **Lakehouse** | รวม Data Lake + Data Warehouse | SQL + Spark ใช้ได้ทั้งคู่ |

### Composite Models

> รวม Dataset จากหลายแหล่ง — ต่อยอดจากของที่มีอยู่ไม่ต้องสร้างใหม่

```
┌──────────────┐     ┌──────────────┐
│ Shared Dataset│     │ Local Tables │
│ (Published)   │     │ (Excel/CSV)  │
│ via DirectQuery│    │ via Import   │
└──────┬───────┘     └──────┬───────┘
       └────────┬───────────┘
           ┌────▼────┐
           │Composite│
           │  Model  │
           └─────────┘
```

| สถานการณ์ | วิธีทำ |
|-----------|-------|
| ต่อยอด Shared Dataset | DirectQuery to PBI Dataset + เพิ่ม local table |
| รวมหลาย datasets | DirectQuery to Dataset A + B + merge |
| เพิ่ม custom calculations | DirectQuery to Dataset + local measures |

### Security Models

| ระดับ | ชื่อ | ควบคุม | ตัวอย่าง |
|-------|------|--------|---------|
| **Row** | RLS (Row-Level Security) | แถวที่เห็น | ทีมขายเห็นเฉพาะ region ตัวเอง |
| **Object** | OLS (Object-Level Security) | Column/Table ที่เห็น | ซ่อน column เงินเดือนจากบางกลุ่ม |
| **Workspace** | Workspace Roles | สิทธิ์ใน Workspace | Admin/Member/Contributor/Viewer |

**OLS ใน model.bim:**
```json
{
  "roles": [{
    "name": "HideSalary",
    "modelPermission": "read",
    "tablePermissions": [{
      "name": "Employees",
      "columnPermissions": [{
        "name": "Salary",
        "metadataPermission": "none"
      }]
    }]
  }]
}
```

**RLS ใน model.bim:**
```json
{
  "roles": [{
    "name": "RegionFilter",
    "modelPermission": "read",
    "tablePermissions": [{
      "name": "Sales",
      "filterExpression": "'Sales'[Region] = USERPRINCIPALNAME()"
    }]
  }]
}
```

---

## 🎨 Elite: Visualization Psychology

> ทำรายงานที่ไม่ใช่แค่ "สวย" แต่ **"ทรงพลัง"** ด้วยจิตวิทยาการรับรู้

### Gestalt Principles (หลักการจัดกลุ่ม)

สมองมนุษย์จัดกลุ่มข้อมูลอัตโนมัติตามหลักเหล่านี้:

| Principle | คำอธิบาย | ใช้ใน PBI |
|-----------|---------|----------|
| **Proximity** (ความใกล้) | สิ่งที่อยู่ใกล้กัน = กลุ่มเดียวกัน | จัด KPI Cards ที่เกี่ยวข้องไว้ชิดกัน |
| **Similarity** (ความเหมือน) | สิ่งที่เหมือนกัน = กลุ่มเดียวกัน | ใช้สีเดียวกันสำหรับ metrics ที่เกี่ยวข้อง |
| **Enclosure** (กรอบ) | สิ่งที่อยู่ในกรอบ = กลุ่มเดียวกัน | ใส่ background shape จัดกลุ่ม visuals |
| **Connection** (เส้นเชื่อม) | สิ่งที่เชื่อมกัน = สัมพันธ์กัน | ใช้ lines แบ่ง sections |
| **Continuity** (ต่อเนื่อง) | ตาจะมองตาม flow | จัด visuals เป็น Z-Pattern |

### Pre-attentive Attributes

> ดึงสายตาไปยัง **Insight สำคัญ** ภายใน **< 1 วินาที** โดยที่สมองไม่ต้องคิด

| Attribute | ใช้อย่างไร | ตัวอย่าง |
|-----------|----------|---------|
| **สี (Color)** | ข้อมูลวิกฤตเป็นสีแดง | 🔴 ยอดขายต่ำกว่าเป้า |
| **ขนาด (Size)** | ค่ามากขึ้น = ใหญ่ขึ้น | KPI Card ตัวหลักใหญ่กว่า |
| **ตำแหน่ง (Position)** | สำคัญที่สุด = ซ้ายบน | Revenue card มุมซ้ายบน |
| **ความเข้ม (Intensity)** | เข้ม = สำคัญ | Bold text สำหรับ KPI value |
| **รูปร่าง (Shape)** | ▲▼ บอกทิศทาง | ไอคอนลูกศรขึ้น/ลง |
| **Motion** | เคลื่อนไหว = สนใจ | หลีกเลี่ยง — ทำให้รำคาญ |

### Minimalist Dashboard (Data-to-Ink Ratio)

> **ลบทุกอย่างที่ไม่จำเป็น** — เหลือเฉพาะสิ่งที่สื่อสารข้อมูล

| ❌ ลบออก | ✅ เก็บไว้ | เหตุผล |
|---------|---------|--------|
| Gridlines (เส้นตาราง) | Data points | เส้นรกไม่ช่วยอ่าน |
| Legend (ถ้ามีสีเดียว) | Legend (ถ้าหลายสี) | ซ้ำซ้อน |
| 3D effects | 2D flat design | 3D บิดเบือนข้อมูล |
| Borders รอบ visuals | White space | กรอบทำให้แน่น |
| Background color (หลายสี) | สีเดียวทั้ง page | ลดความรก |
| Axis labels ที่ซ้ำ | Title ที่ชัดเจน | เห็นที่ title พอ |
| ตัวเลขทศนิยม > 2 | ปัดเลข (1.2M, 45K) | อ่านง่ายกว่า |

**กฎ Data-to-Ink:**
```
Data-to-Ink Ratio = (หมึกที่ใช้แสดงข้อมูล) / (หมึกทั้งหมดในภาพ)

เป้าหมาย: ให้ ratio สูงที่สุด (ใกล้ 1.0)
= ลบทุกอย่างที่ไม่ใช่ "ข้อมูล" ออก
```

> 💡 **ทดสอบ**: ถ้าลบ element ใดออกแล้ว dashboard ยังสื่อสารได้เหมือนเดิม → **ลบออกเลย**

---

## 🛠️ God Mode: XMLA Endpoint & API Automation

> เลิกใช้เมาส์ — จัดการ Power BI ด้วย **Code 100%**

### XMLA Read/Write

> เชื่อมต่อ Workspace โดยตรง — แก้ไข data model โดยไม่ต้องเปิด .pbix

**เครื่องมือที่ใช้ได้:**

| เครื่องมือ | ทำอะไร | สถานะ |
|----------|--------|--------|
| **SSMS** (SQL Server Management Studio) | Query + แก้ model ผ่าน XMLA | ✅ Read/Write |
| **Tabular Editor** | แก้ model + Best Practice rules | ✅ Read/Write |
| **DAX Studio** | Query + Debug DAX | ✅ Read only |
| **Visual Studio + SSAS project** | Full model development | ✅ Read/Write |
| **PowerShell + AMO/TOM** | Automation scripting | ✅ Read/Write |

**Connection String:**
```
powerbi://api.powerbi.com/v1.0/myorg/WorkspaceName
```

> ⚠️ **ต้องการ**: Power BI Premium / Premium Per User (PPU) / Fabric capacity

### Power BI REST API

> เขียน Script สั่งงาน PBI Service แบบอัตโนมัติ

**Python ตัวอย่าง:**
```python
import requests

# Authentication (Service Principal)
TOKEN = "Bearer eyJ0..."
HEADERS = {"Authorization": TOKEN, "Content-Type": "application/json"}
BASE_URL = "https://api.powerbi.com/v1.0/myorg"

# 1. List all workspaces
workspaces = requests.get(f"{BASE_URL}/groups", headers=HEADERS).json()

# 2. Trigger dataset refresh
dataset_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
group_id = "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"
requests.post(
    f"{BASE_URL}/groups/{group_id}/datasets/{dataset_id}/refreshes",
    headers=HEADERS,
    json={"notifyOption": "MailOnCompletion"}
)

# 3. Add user to workspace (bulk)
users = ["user1@company.com", "user2@company.com", "user3@company.com"]
for email in users:
    requests.post(
        f"{BASE_URL}/groups/{group_id}/users",
        headers=HEADERS,
        json={"emailAddress": email, "groupUserAccessRight": "Viewer"}
    )

# 4. Export report to PDF/PPTX
export = requests.post(
    f"{BASE_URL}/groups/{group_id}/reports/{report_id}/ExportTo",
    headers=HEADERS,
    json={"format": "PDF"}
)
```

**API Use Cases:**

| ใช้ทำอะไร | Endpoint | Method |
|-----------|----------|--------|
| Refresh dataset | `/datasets/{id}/refreshes` | POST |
| List reports | `/groups/{id}/reports` | GET |
| Add user to workspace | `/groups/{id}/users` | POST |
| Get refresh history | `/datasets/{id}/refreshes` | GET |
| Clone report | `/reports/{id}/Clone` | POST |
| Export to PDF | `/reports/{id}/ExportTo` | POST |
| Get dataset info | `/datasets/{id}` | GET |

### TMSL (Tabular Model Scripting Language)

> เขียน JSON เพื่อจัดการ data model — **Bulk update** ได้ในวินาที

```json
// TMSL — สร้าง measure ใหม่
{
  "createOrReplace": {
    "object": {
      "database": "SalesModel",
      "table": "_Measures",
      "measure": "YoY Growth %"
    },
    "measure": {
      "name": "YoY Growth %",
      "expression": "VAR _Current = [Total Revenue]\nVAR _PrevYear = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Date'[Date]))\nRETURN DIVIDE(_Current - _PrevYear, _PrevYear, 0)",
      "formatString": "0.0%",
      "description": "Year-over-Year revenue growth percentage"
    }
  }
}
```

```json
// TMSL — ลบ column ที่ไม่ใช้ (batch)
{
  "delete": {
    "object": {
      "database": "SalesModel",
      "table": "Sales",
      "column": "unused_column_1"
    }
  }
}
```

**TMSL Commands:**

| Command | ทำอะไร | ตัวอย่าง |
|---------|--------|---------|
| `createOrReplace` | สร้าง/อัพเดต object | เพิ่ม measure, table, relationship |
| `delete` | ลบ object | ลบ column, table ที่ไม่ใช้ |
| `alter` | แก้ไข properties | เปลี่ยน data type, format |
| `refresh` | สั่ง refresh data | Full, Incremental, Calculate |
| `sequence` | รัน batch commands | ทำหลายคำสั่งพร้อมกัน |

---

## ⚡ God Mode: Large Dataset Management

> จัดการข้อมูล **หลายพันล้านแถว** — เร็วและ scalable

### Hybrid Tables

> ตารางเดียวที่รวม **3 modes** เข้าด้วยกัน — ได้ทั้งความเร็วและความสด

```
┌──────────────────────────────────────────────────────┐
│                    Hybrid Table                       │
├──────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │  Historical     │  │ Recent       │  │ Latest   │ │
│  │  (Import)       │  │ (Incremental │  │ (Direct  │ │
│  │  ⚡ เร็วมาก     │  │  Refresh)    │  │  Query)  │ │
│  │                 │  │  🔄 อัพเดต   │  │  🔴 Live │ │
│  │  Jan 2020 -     │  │  ทุกวัน       │  │  Real-   │ │
│  │  Dec 2025       │  │  Jan-Feb 2026│  │  time    │ │
│  └────────────────┘  └──────────────┘  └──────────┘ │
└──────────────────────────────────────────────────────┘
```

| ส่วน | Mode | ข้อมูล | ข้อดี |
|------|------|--------|------|
| **Historical** | Import | ข้อมูลเก่า (ไม่เปลี่ยน) | ⚡ เร็วมากใน memory |
| **Recent** | Incremental Refresh | ข้อมูลล่าสุดไม่กี่เดือน | 🔄 Refresh เฉพาะส่วนใหม่ |
| **Latest** | DirectQuery | ข้อมูล real-time | 🔴 สดเสมอ |

**Incremental Refresh — วิธีตั้งค่า:**
```
1. สร้าง Parameters: RangeStart, RangeEnd (type DateTime)
2. Filter ข้อมูลใน Power Query: [Date] >= RangeStart AND [Date] < RangeEnd
3. Modeling → Manage Incremental Refresh → ตั้ง:
   - Archive: 3 years (Import)
   - Incremental: 30 days (Refresh)
   - Real-time: Enable DirectQuery partition
```

### User-Defined Aggregations

> สร้าง **ตารางสรุป** ซ่อนไว้ — PBI เลือกอัตโนมัติว่าดึงจากไหน

```
User คลิกดูภาพรวม (Year/Month)
    → PBI ดึงจาก Agg Table (Import, เร็วมาก) ⚡

User drill-down ดูรายวัน (Day/Transaction)
    → PBI สลับไป Detail Table (DirectQuery) 🔍
```

**วิธีสร้าง:**

```
┌──────────────────┐          ┌──────────────────┐
│  AggSales (ซ่อน)  │          │  Sales (Detail)   │
│  Import mode      │          │  DirectQuery      │
├──────────────────┤          ├──────────────────┤
│ Year              │          │ Date              │
│ Month             │   ←──►   │ Product           │
│ Category          │  auto    │ CustomerID        │
│ SUM(Revenue)      │  switch  │ Revenue           │
│ COUNT(Orders)     │          │ Quantity           │
└──────────────────┘          └──────────────────┘
```

**model.bim — Aggregation config:**
```json
{
  "name": "AggSales",
  "isHidden": true,
  "columns": [
    {"name": "Year", "summarizeBy": "groupBy", "alternateOf": {"baseTable": "Sales", "baseColumn": "Year"}},
    {"name": "Category", "summarizeBy": "groupBy", "alternateOf": {"baseTable": "Sales", "baseColumn": "Category"}},
    {"name": "Revenue", "summarizeBy": "sum", "alternateOf": {"baseTable": "Sales", "baseColumn": "Revenue"}}
  ]
}
```

### Calculation Groups

> ลดจำนวน Measures จาก **500 → 10** ด้วย Dynamic Time Intelligence

**ปัญหา:** ถ้ามี 50 measures × 10 time periods = **500 measures!**
```
Total Revenue, Revenue YTD, Revenue PY, Revenue YoY, Revenue MoM...
Total Orders, Orders YTD, Orders PY, Orders YoY, Orders MoM...
Total Profit, Profit YTD, Profit PY, Profit YoY, Profit MoM...
... × 50 = 500 measures 😱
```

**แก้ด้วย Calculation Group:** เก็บ 50 base measures + 1 Calculation Group

```json
// model.bim — Calculation Group (สร้างผ่าน Tabular Editor)
{
  "name": "Time Intelligence",
  "calculationGroup": {
    "calculationItems": [
      {
        "name": "Current",
        "expression": "SELECTEDMEASURE()"
      },
      {
        "name": "YTD",
        "expression": "TOTALYTD(SELECTEDMEASURE(), 'Date'[Date])"
      },
      {
        "name": "Previous Year",
        "expression": "CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))"
      },
      {
        "name": "YoY Change",
        "expression": "VAR _Current = SELECTEDMEASURE()\nVAR _PY = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))\nRETURN _Current - _PY"
      },
      {
        "name": "YoY %",
        "expression": "VAR _Current = SELECTEDMEASURE()\nVAR _PY = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))\nRETURN DIVIDE(_Current - _PY, _PY, 0)",
        "formatString": "0.0%"
      }
    ]
  }
}
```

**ผลลัพธ์:** ผู้ใช้เลือก Slicer "Time Intelligence" → ใช้ได้กับ **ทุก measure** อัตโนมัติ!

---

## 🛡️ God Mode: Governance & Tenant Administration

> คุมกฎระดับองค์กร — ปลอดภัย, เสถียร, ตรวจสอบได้

### Admin API & Activity Logs

> ดึงข้อมูลการใช้งาน PBI ทั้งองค์กรมาวิเคราะห์

**Python — ดึง Activity Log:**
```python
import requests
from datetime import datetime, timedelta

# Get activity events for last 24 hours
start = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
end = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

events = requests.get(
    f"{BASE_URL}/admin/activityevents"
    f"?startDateTime='{start}'&endDateTime='{end}'",
    headers=HEADERS
).json()

# วิเคราะห์: รายงานไหนไม่มีคนดู?
# วิเคราะห์: ใครโหลดข้อมูลออกไป?
# วิเคราะห์: Dataset ไหน refresh ล้มเหลวบ่อย?
```

**สิ่งที่ Track ได้:**

| Event | รายละเอียด | ใช้ทำอะไร |
|-------|----------|----------|
| `ViewReport` | ใครดูรายงานอะไร เมื่อไหร่ | วิเคราะห์ adoption rate |
| `ExportReport` | ใคร export ข้อมูลออก | ตรวจสอบ data leakage |
| `RefreshDataset` | Refresh สำเร็จ/ล้มเหลว | Monitor data pipeline |
| `CreateReport` | ใครสร้างรายงานใหม่ | ติดตาม self-service usage |
| `ShareReport` | ใครแชร์ให้ใคร | ตรวจสอบ access control |
| `DeleteReport` | ใครลบอะไร | Audit trail |

### Information Protection (Sensitivity Labels)

> ป้องกันข้อมูลรั่วไหลด้วย **Microsoft Purview** labels

| Label | ระดับ | ข้อจำกัด |
|-------|------|----------|
| **Public** | 🟢 ทั่วไป | ไม่มีข้อจำกัด |
| **General** | 🟡 ภายใน | ห้ามแชร์นอกองค์กร |
| **Confidential** | 🟠 ความลับ | ห้าม export, ห้าม print |
| **Highly Confidential** | 🔴 ลับสุดยอด | ห้ามทุกอย่าง + encryption |

**สิ่งที่ Label ทำ:**
- ✅ ติดตามข้อมูลตลอดทาง (Export ออกเป็น Excel → Label ติดไปด้วย)
- ✅ บังคับ encryption บน files ที่ export
- ✅ บล็อกการ export สำหรับ label Confidential+
- ✅ Audit log ว่าใครเข้าถึง/แก้ไข labeled content

### Power BI Scanner API

> สแกน **ทุกรายงาน** ในองค์กร — หาปัญหาอัตโนมัติ

```python
# Scanner API — สแกน workspace ทั้งหมด
scan_request = requests.post(
    f"{BASE_URL}/admin/workspaces/getInfo",
    headers=HEADERS,
    json={
        "workspaces": [workspace_id],
        "datasetExpressions": True,     # ดู DAX expressions
        "datasetSchema": True,          # ดู schema ทั้งหมด
        "datasourceDetails": True,      # ดู data sources
        "getArtifactUsers": True        # ดูว่าใครมีสิทธิ์
    }
)
```

**สิ่งที่สแกนได้:**

| ตรวจสอบ | ปัญหาที่หา | Action |
|---------|----------|--------|
| **DAX expressions** | สูตรผิด best practice | รายงานให้ทีม fix |
| **Data sources** | เชื่อมต่อ source ไม่ได้รับอนุญาต | บล็อก / แจ้งเตือน |
| **Unused columns** | Import column ที่ไม่ได้ใช้ | ลบออกลด memory |
| **User permissions** | ใครมีสิทธิ์เกินจำเป็น | Revoke excess access |
| **Endorsement status** | รายงานไหนผ่านการรับรอง | Promote / Certify |
| **Refresh schedules** | Dataset ที่ไม่ได้ refresh | ตั้ง schedule / ลบ |

> 🏆 **เป้าหมาย God Mode**: ทุกอย่างเป็น **Code**, ทุกอย่าง **อัตโนมัติ**, ทุกอย่าง **ตรวจสอบได้** — จากนักสร้างรายงาน สู่ **Enterprise Data Architect**

---

## 🧠 Architect: VertiPaq Engine Internals

> เลิกมอง Power BI เป็นกล่องดำ — เข้าใจ **ฟันเฟืองข้างใน** เพื่อสร้างโมเดลที่เร็วที่สุด

### Dictionary Encoding & Run-Length Encoding (RLE)

> VertiPaq บีบอัดข้อมูลใน memory ด้วย 2 วิธีหลัก

```
                    VertiPaq Compression
┌──────────────────────────────────────────────────┐
│                                                  │
│  1️⃣ Dictionary Encoding (ทุก column)              │
│  ┌────────────┐     ┌──────────────────┐         │
│  │ Raw Data   │     │ Dictionary       │         │
│  ├────────────┤     ├──────────────────┤         │
│  │ "Bangkok"  │ →   │ 0 = "Bangkok"    │         │
│  │ "Chiang Mai│     │ 1 = "Chiang Mai" │         │
│  │ "Bangkok"  │     │ 2 = "Phuket"     │         │
│  │ "Phuket"   │     └──────────────────┘         │
│  │ "Bangkok"  │     Stored as: [0,1,0,2,0]       │
│  └────────────┘                                  │
│                                                  │
│  2️⃣ RLE (ถ้า sorted — ยิ่งบีบได้มาก)               │
│  ┌────────────┐     ┌──────────────────┐         │
│  │ Sorted:    │     │ RLE:             │         │
│  │ 0,0,0      │ →   │ (0, ×3)          │         │
│  │ 1          │     │ (1, ×1)          │         │
│  │ 2          │     │ (2, ×1)          │         │
│  └────────────┘     └──────────────────┘         │
└──────────────────────────────────────────────────┘
```

**ผลกระทบต่อ Design:**

| ✅ ทำ (เร็ว + เล็ก) | ❌ ห้าม (ช้า + ใหญ่) | เหตุผล |
|---------------------|---------------------|--------|
| Sort column ก่อน import | ปล่อยข้อมูลไม่เรียง | RLE ทำงานดีกับ sorted data |
| ใช้ Integer keys | ใช้ Long text เป็น key | Dictionary ใหญ่ = ช้า |
| ลบ columns ที่ไม่ใช้ | Import ทุก column | column = memory |
| ลด decimal places | ใช้ 15 decimal places | Precision สูง = Dictionary ใหญ่ |
| Group ค่าที่ hiigh cardinality | เก็บ unique ID ทุกตัว | ยิ่ง unique มาก ยิ่งบีบไม่ได้ |

### Cardinality Management

> **Cardinality** = จำนวนค่า unique ใน column → ยิ่งสูง ยิ่งกิน memory

```
Low Cardinality (ดี ✅)          High Cardinality (แย่ ❌)
┌──────────────────┐           ┌──────────────────┐
│ Country (195)     │           │ Transaction ID    │
│ Status (5)        │           │ (10,000,000)      │
│ Category (20)     │           │ Timestamp (ms)    │
│ Gender (3)        │           │ Email Address     │
└──────────────────┘           └──────────────────┘
```

**DAX Studio — ตรวจ Cardinality:**
```dax
// VertiPaq Analyzer query — ดู column statistics
EVALUATE
SELECTCOLUMNS(
    INFO.STORAGETABLECOLUMNS(),
    "Table", [TABLE_ID],
    "Column", [COLUMN_ID],
    "Cardinality", [COLUMN_CARDINALITY],
    "DataSize (bytes)", [USED_SIZE],
    "Encoding", [COLUMN_ENCODING]
)
ORDER BY [USED_SIZE] DESC
```

**กลยุทธ์ลด Cardinality:**

| Column ปัญหา | วิธีแก้ | ผลลัพธ์ |
|-------------|--------|---------|
| DateTime (ms precision) | ตัด time ออก เก็บแค่ Date | Cardinality ↓ 86,400× |
| Product Description (text ยาว) | แยกเป็นตาราง lookup | Column size ↓ 90%+ |
| Full Name | แยก First/Last Name | Dictionary ↓ |
| Price (12.3456789) | ปัดเป็น 2 decimal | Dictionary ↓ |
| GUID/UUID | ใช้ Integer surrogate key | Cardinality ↓ memory ↓ |

### Segment & Partition Optimization

> จัดการ data **ส่วนย่อย** ผ่าน XMLA — refresh เฉพาะที่ต้องการ

```
┌──────────────────────────────────────────┐
│              Sales Table                  │
├──────────────────────────────────────────┤
│  Partition: 2024_Q1  │  Status: ✅ Current │
│  Partition: 2024_Q2  │  Status: ✅ Current │
│  Partition: 2024_Q3  │  Status: ✅ Current │
│  Partition: 2024_Q4  │  Status: ✅ Current │
│  Partition: 2025_Q1  │  Status: 🔄 Refresh │ ← เฉพาะส่วนนี้
│  Partition: 2025_Q2  │  Status: 🔄 Refresh │ ← เฉพาะส่วนนี้
└──────────────────────────────────────────┘
```

**TMSL — Refresh เฉพาะ partition:**
```json
{
  "refresh": {
    "type": "full",
    "objects": [{
      "database": "SalesModel",
      "table": "Sales",
      "partition": "2025_Q2"
    }]
  }
}
```

**model.bim — Partition definition:**
```json
{
  "name": "Sales",
  "partitions": [
    {
      "name": "2024_Archive",
      "mode": "import",
      "source": {
        "type": "m",
        "expression": "let Source = Sql.Database(\"server\", \"db\"), filtered = Table.SelectRows(Source, each [Year] = 2024) in filtered"
      }
    },
    {
      "name": "2025_Current",
      "mode": "import",
      "source": {
        "type": "m",
        "expression": "let Source = Sql.Database(\"server\", \"db\"), filtered = Table.SelectRows(Source, each [Year] = 2025) in filtered"
      }
    },
    {
      "name": "Realtime",
      "mode": "directQuery",
      "source": {
        "type": "m",
        "expression": "let Source = Sql.Database(\"server\", \"db\", [Query=\"SELECT * FROM Sales WHERE Date >= DATEADD(day, -1, GETDATE())\"]) in Source"
      }
    }
  ]
}
```

---

## 🌐 Architect: Multi-Cloud Semantic Layer

> สร้าง **"สมองกลาง"** ของข้อมูลที่ไม่ได้อยู่แค่ใน Power BI

### Direct Lake Mode on Fabric

> อ่านข้อมูลจาก **Parquet/Delta** ใน OneLake โดยตรง — ไม่ต้อง Import ไม่ต้องรอ DQ

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│          เปรียบเทียบ 3 Modes                          │
│                                                      │
│  Import Mode      DirectQuery     Direct Lake         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  │ Copy data │    │ Live query│    │ Read from│        │
│  │ to memory │    │ to source │    │ Parquet  │        │
│  │           │    │           │    │ in Lake  │        │
│  │ ⚡ เร็วสุด │    │ 🐌 ช้าสุด │    │ ⚡ เร็ว   │        │
│  │ 📦 กิน RAM│    │ 🔴 Live  │    │ 🔴 Live  │        │
│  │ 🔄 Stale │    │ ✅ Fresh │    │ ✅ Fresh │        │
│  └──────────┘    └──────────┘    └──────────┘        │
│                                                      │
│  Best of Both Worlds = Direct Lake ⭐                │
└──────────────────────────────────────────────────────┘
```

| Feature | Import | DirectQuery | **Direct Lake** |
|---------|--------|-------------|----------------|
| Speed | ⚡⚡⚡ | ⚡ | ⚡⚡⚡ |
| Freshness | ❌ Stale | ✅ Live | ✅ Live |
| Memory | 📦 สูง | 📦 ต่ำ | 📦 ปานกลาง |
| Max size | ~10 GB | Unlimited | Unlimited |
| File format | N/A | SQL source | **Parquet / Delta** |
| Requires | Power BI Pro | DQ-compatible source | **Microsoft Fabric** |

**Parquet in OneLake:**
```python
# Python — เขียน Parquet ลง OneLake
import pandas as pd

df = pd.read_sql("SELECT * FROM Sales", connection)
df.to_parquet(
    "abfss://workspace@onelake.dfs.fabric.microsoft.com/lakehouse/Tables/Sales",
    engine="pyarrow",
    partition_cols=["Year", "Month"]  # Partition by date
)
# Power BI Direct Lake จะอ่านได้ทันที!
```

### Semantic Link (Python for PBI Datasets)

> ดึง Power BI dataset ออกมาทำ **Data Science** ใน Fabric Notebook

```python
# Semantic Link — ดึงข้อมูลจาก PBI Dataset
import sempy.fabric as fabric

# ดึง list of datasets
datasets = fabric.list_datasets()

# อ่านข้อมูลจาก dataset ด้วย DAX
df = fabric.evaluate_dax(
    dataset="Sales Model",
    dax_string="""
        EVALUATE
        SUMMARIZE(
            Sales,
            'Product'[Category],
            "Revenue", [Total Revenue],
            "Orders", [Total Orders]
        )
    """
)

# ทำ ML / Analysis
from sklearn.cluster import KMeans
clusters = KMeans(n_clusters=3).fit_predict(df[['Revenue', 'Orders']])
df['Segment'] = clusters

# เขียนผลลัพธ์กลับเข้า Lakehouse → PBI อ่านได้ทันที
df.to_delta("Tables/CustomerSegments")
```

**Use Cases:**

| ทำอะไร | วิธี | ผลลัพธ์ |
|--------|------|---------|
| Customer Segmentation | KMeans on PBI data | เพิ่ม Segment column |
| Data Validation | Compare PBI vs Source | หา discrepancies |
| Anomaly Detection | Isolation Forest | Flag outliers |
| Forecast | Prophet / ARIMA | Prediction table |
| Model Documentation | Export metadata | Auto-generate docs |

### External Tool Development

> สร้าง **เครื่องมือเฉพาะทาง** ของคุณเอง สำหรับทีม

**External Tool = .pbitool.json:**
```json
// MyModelChecker.pbitool.json — ติดตั้งใน PBI Desktop
{
  "version": "1.0",
  "name": "Model Health Checker",
  "description": "ตรวจสอบ Best Practices อัตโนมัติ",
  "path": "C:\\Tools\\ModelChecker.exe",
  "arguments": "\"%server%\" \"%database%\"",
  "iconData": "data:image/png;base64,..."
}
```

**Python — Auto-Doc Generator:**
```python
# สร้าง Data Dictionary จาก model อัตโนมัติ
import pyadomd
from tabulate import tabulate

conn = pyadomd.connect(f"Provider=MSOLAP;Data Source={xmla_endpoint};")
cursor = conn.cursor()

# ดึง measures ทั้งหมด
cursor.execute("""
    SELECT
        MEASURE_NAME, MEASURE_CAPTION,
        EXPRESSION, DESCRIPTION
    FROM $SYSTEM.MDSCHEMA_MEASURES
    WHERE MEASURE_IS_VISIBLE
""")

measures = cursor.fetchall()
print(tabulate(measures, headers=["Name", "Caption", "DAX", "Description"]))

# Export เป็น markdown documentation
with open("DATA_DICTIONARY.md", "w") as f:
    f.write("# Data Dictionary\n\n")
    for m in measures:
        f.write(f"## {m[0]}\n- **DAX:** `{m[2]}`\n- **Description:** {m[3]}\n\n")
```

---

## 🔐 Architect: Custom Connector & API Development

> เมื่อ PBI เชื่อมต่ออะไรไม่ได้ — **สร้างทางเดินเอง**

### Custom Connector (M Language Extension)

> เขียน Connector ด้วย M เพื่อเชื่อมระบบที่ไม่มีใน Standard

**โครงสร้าง Custom Connector:**
```
MyConnector/
├── MyConnector.pq          ← M code หลัก
├── MyConnector.query.pq    ← Test queries
├── resources/
│   └── MyConnector.png     ← Icon
└── MyConnector.proj        ← Project file
```

**M Code — OAuth2 Connector:**
```m
// MyConnector.pq — Custom REST API Connector
section MyConnector;

[DataSource.Kind="MyConnector", Publish="MyConnector.Publish"]
shared MyConnector.Contents = (endpoint as text) =>
    let
        // OAuth2 Authentication
        token = GetAccessToken(),
        headers = [
            Authorization = "Bearer " & token,
            #"Content-Type" = "application/json"
        ],

        // Paginated API call
        allData = List.Generate(
            () => [page = 1, hasMore = true, data = {}],
            each [hasMore],
            each let
                response = Web.Contents(
                    endpoint & "?page=" & Text.From([page]),
                    [Headers = headers]
                ),
                json = Json.Document(response),
                newData = json[results]
            in
                [page = [page] + 1, hasMore = json[hasNext], data = newData],
            each [data]
        ),
        combined = List.Combine(allData),
        result = Table.FromList(combined, Splitter.SplitByNothing())
    in
        result;

// Authentication config
MyConnector = [
    Authentication = [
        OAuth = [
            StartLogin = StartLogin,
            FinishLogin = FinishLogin,
            Refresh = RefreshToken
        ]
    ],
    Label = "My Custom API"
];
```

### Power BI Embedded & Custom Visuals

> ฝัง PBI ในเว็บแอป + สร้าง Visual ใหม่ด้วย **TypeScript/D3.js**

**Embedded — JavaScript:**
```javascript
// Power BI Embedded — ฝัง report ในเว็บ
import * as pbi from 'powerbi-client';

const embedConfig = {
    type: 'report',
    id: reportId,
    embedUrl: embedUrl,
    accessToken: token,
    tokenType: pbi.models.TokenType.Embed,
    settings: {
        panes: { filters: { visible: false } },
        navContentPaneEnabled: false,
        background: pbi.models.BackgroundType.Transparent
    }
};

const report = powerbi.embed(container, embedConfig);

// Listen for events
report.on('loaded', () => console.log('Report loaded'));
report.on('dataSelected', (event) => {
    const data = event.detail;
    // ส่ง selected data ไป backend
    handleSelection(data);
});
```

**Custom Visual — pbiviz.json:**
```json
{
  "visual": {
    "name": "myCustomRadar",
    "displayName": "Radar Chart Pro",
    "guid": "myCustomRadar_GUID",
    "visualClassName": "RadarChart",
    "version": "1.0.0",
    "description": "Custom radar chart with animations"
  },
  "apiVersion": "5.3.0",
  "capabilities": {
    "dataRoles": [
      {"name": "category", "kind": "Grouping"},
      {"name": "values", "kind": "Measure"}
    ]
  }
}
```

### Real-time Push Dataset via API

> **Push** ข้อมูลเข้า PBI แบบ **วินาทีต่อวินาที** — Dashboard มีชีวิต

```python
import requests
import time
import random

# 1. สร้าง Push Dataset
dataset_schema = {
    "name": "IoT Sensor Data",
    "defaultMode": "Push",
    "tables": [{
        "name": "SensorReadings",
        "columns": [
            {"name": "Timestamp", "dataType": "DateTime"},
            {"name": "SensorID", "dataType": "String"},
            {"name": "Temperature", "dataType": "Double"},
            {"name": "Humidity", "dataType": "Double"},
            {"name": "Status", "dataType": "String"}
        ]
    }]
}

created = requests.post(
    f"{BASE_URL}/groups/{group_id}/datasets",
    headers=HEADERS, json=dataset_schema
).json()

dataset_id = created["id"]

# 2. Push data ทุกวินาที
while True:
    rows = [{
        "Timestamp": datetime.utcnow().isoformat(),
        "SensorID": f"SENSOR_{random.randint(1,10)}",
        "Temperature": round(random.uniform(20, 45), 1),
        "Humidity": round(random.uniform(30, 90), 1),
        "Status": random.choice(["Normal", "Warning", "Critical"])
    }]

    requests.post(
        f"{BASE_URL}/groups/{group_id}/datasets/{dataset_id}"
        f"/tables/SensorReadings/rows",
        headers=HEADERS, json={"rows": rows}
    )

    time.sleep(1)  # Push ทุก 1 วินาที
```

**Push Dataset Limits:**

| Limit | ค่า |
|-------|-----|
| Max rows per POST | 10,000 |
| Max POST requests/hr | 120 (Pro) / 7,200 (Premium) |
| Max pending rows | 200,000 |
| Row retention | FIFO (ลบเก่าอัตโนมัติ) |
| Dataset size | 1 MB (Pro) / 10 GB (Premium) |

> 🧬 **เป้าหมาย Architect**: ไม่ใช่แค่ **ใช้** Power BI — แต่ **สร้าง**, **ขยาย**, และ **ควบคุม** ทุกอย่างด้วย Code จากระดับ Engine ไปจนถึง Cloud

---

## 🧠 Omnipotent: Memory Engine Internal Profiling

> เลิกเขียนสูตร — เขียน **"กลไกการทำงาน"** ของหน่วยความจำ

### Storage Engine (SE) vs Formula Engine (FE)

> DAX ทุกสูตรถูกแบ่งประมวลผลใน 2 engines — เข้าใจความแตกต่างคือกุญแจสู่ความเร็ว

```
┌──────────────────────────────────────────────────────┐
│                  DAX Query Execution                  │
├──────────────────────────────────────────────────────┤
│                                                      │
│  User → DAX Query                                    │
│         ↓                                            │
│  ┌──────────────────┐                                │
│  │  Formula Engine   │  ← Single-threaded 🐌         │
│  │  (FE)             │  ← Handles: Iteration,        │
│  │                   │    Context Transition,         │
│  │                   │    Complex logic               │
│  └────────┬─────────┘                                │
│           │ xmSQL queries                            │
│           ▼                                          │
│  ┌──────────────────┐                                │
│  │  Storage Engine   │  ← Multi-threaded ⚡️          │
│  │  (SE / VertiPaq)  │  ← Handles: Scan, Filter,     │
│  │                   │    Aggregate, GroupBy          │
│  │                   │  ← Works on compressed data   │
│  └──────────────────┘                                │
│                                                      │
│  🎯 เป้าหมาย: ให้ SE ทำงานมากที่สุด (เร็ว)            │
│              ลดงาน FE ให้น้อยที่สุด (ช้า)              │
└──────────────────────────────────────────────────────┘
```

| Feature | Storage Engine (SE) | Formula Engine (FE) |
|---------|-------------------|-------------------|
| Threading | ⚡ **Multi-threaded** | 🐌 **Single-threaded** |
| ทำอะไร | Scan, Filter, Aggregate | Iteration, Complex logic |
| ข้อมูล | VertiPaq compressed | Row-by-row |
| Cache | ✅ Cacheable | ❌ ไม่ cache |
| ความเร็ว | มิลลิวินาที | วินาที-นาที |

**DAX ที่ทำงานใน SE (ดี ✅):**
```dax
// SE-friendly — aggregate scan
Total Revenue = SUM(Sales[Revenue])
Revenue by Category = SUMX(VALUES('Product'[Category]), [Total Revenue])
```

**DAX ที่ตกไป FE (ช้า ❌):**
```dax
// FE-heavy — row-by-row iteration
Running Total =
SUMX(
    FILTER(ALL(Sales), Sales[Date] <= MAX(Sales[Date])),
    Sales[Revenue]
)
// แก้: ใช้ window functions หรือ pre-calculate
```

**DAX Studio — ตรวจ SE vs FE:**
```
Server Timings tab:
┌──────────────────────────────────────────┐
│ Total:           245 ms                  │
│ ├─ SE Queries:    12  (198 ms)  ← ดี ✅  │
│ ├─ SE Cache:       8  (0 ms)    ← ดีมาก │
│ └─ FE:            47 ms         ← ถ้าสูง = ปัญหา │
└──────────────────────────────────────────┘

กฎ: FE time < 20% ของ Total = ดี
     FE time > 50% ของ Total = ต้อง optimize
```

### Cache Warming (Pre-load Reports)

> โหลดรายงานเข้า memory **ล่วงหน้า** — ผู้บริหารเปิดดูได้ทันทีใน 0.1 วินาที

```python
# Cache Warming Script — รันก่อนเวลาทำงาน (เช่น 7:30 AM)
import requests
import schedule
import time

CRITICAL_REPORTS = [
    {"group_id": "xxx", "report_id": "aaa", "name": "Executive Dashboard"},
    {"group_id": "xxx", "report_id": "bbb", "name": "Sales Overview"},
    {"group_id": "xxx", "report_id": "ccc", "name": "Finance Summary"},
]

def warm_cache():
    """Pre-load reports โดยสั่ง refresh + execute DAX query"""
    for report in CRITICAL_REPORTS:
        # 1. Trigger dataset refresh
        requests.post(
            f"{BASE_URL}/groups/{report['group_id']}"
            f"/datasets/{report['dataset_id']}/refreshes",
            headers=HEADERS,
            json={"notifyOption": "NoNotification"}
        )

        # 2. Execute DAX query to warm VertiPaq cache
        requests.post(
            f"{BASE_URL}/groups/{report['group_id']}"
            f"/datasets/{report['dataset_id']}/executeQueries",
            headers=HEADERS,
            json={
                "queries": [{"query": "EVALUATE ROW(\"warm\", 1)"}],
                "serializerSettings": {"includeNulls": True}
            }
        )
        print(f"✅ Warmed: {report['name']}")

# Schedule: ทุกวัน 7:30 AM
schedule.every().day.at("07:30").do(warm_cache)
while True:
    schedule.run_pending()
    time.sleep(60)
```

### Materialized Views in Fabric

> Pre-calculate ใน **Spark** → เก็บเป็น Delta → Direct Lake อ่านได้ทันที

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│ Raw Data     │     │ Spark Job         │     │ Power BI      │
│ (Billions of │────►│ (Pre-aggregate)   │────►│ (Direct Lake) │
│  rows)       │     │ Materialized View │     │ ⚡ 0.1s query │
└─────────────┘     └──────────────────┘     └──────────────┘
```

```python
# PySpark — สร้าง Materialized View ใน Fabric Lakehouse
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

spark = SparkSession.builder.getOrCreate()

# อ่าน raw data (10 billion rows)
raw_sales = spark.read.format("delta").load("Tables/Sales")

# Pre-aggregate → Materialized View
materialized = (
    raw_sales
    .groupBy("Year", "Quarter", "Region", "Category")
    .agg(
        F.sum("Revenue").alias("Total_Revenue"),
        F.sum("Cost").alias("Total_Cost"),
        F.count("OrderID").alias("Order_Count"),
        F.countDistinct("CustomerID").alias("Unique_Customers")
    )
)

# เขียนเป็น Delta table
materialized.write.format("delta").mode("overwrite") \
    .saveAsTable("MaterializedSalesSummary")

# Power BI Direct Lake อ่าน MaterializedSalesSummary ได้ทันที!
# จาก 10B rows → ~100K rows = เร็ว 100,000x
```

---

## 🌐 Omnipotent: Distributed Semantic Layer

> สร้าง **"สมองกล"** ที่กระจายตัวรองรับผู้ใช้ **ทั่วโลก**

### Cross-Region Load Balancing

```
┌──────────────────────────────────────────────────────────┐
│              Global Power BI Architecture                 │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  🌏 Asia Pacific          🌍 Europe           🌎 Americas │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐│
│  │ Fabric Cap.  │    │ Fabric Cap.  │    │ Fabric Cap.  ││
│  │ (Southeast   │    │ (West Europe)│    │ (East US)    ││
│  │  Asia)       │    │              │    │              ││
│  │ ┌──────────┐ │    │ ┌──────────┐ │    │ ┌──────────┐ ││
│  │ │ OneLake  │ │    │ │ OneLake  │ │    │ │ OneLake  │ ││
│  │ │ (replica)│ │    │ │ (replica)│ │    │ │ (primary)│ ││
│  │ └──────────┘ │    │ └──────────┘ │    │ └──────────┘ ││
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘│
│         └─────────────┬─────┘                   │        │
│                  ┌────▼────────────────────────▼─┐       │
│                  │  Azure Front Door / Traffic    │       │
│                  │  Manager (DNS-based routing)   │       │
│                  └───────────────────────────────┘       │
└──────────────────────────────────────────────────────────┘
```

| Component | ทำอะไร | เหตุผล |
|-----------|--------|--------|
| **Multi-Geo Capacities** | แยก Fabric capacity ตาม region | ข้อมูลอยู่ใกล้ผู้ใช้ |
| **OneLake Replication** | Replicate data across regions | Read-local, Write-global |
| **Azure Front Door** | Route users → nearest capacity | ลด latency < 50ms |
| **Deployment Pipelines** | Sync reports across regions | Dev→Test→Prod ทุก region |

### Multi-Tenant Embedded Architecture

> รองรับ **หลายหมื่นลูกค้า** ในแอปเดียว — แต่ละคนเห็นข้อมูลตัวเอง

```
┌────────────────────────────────────────────────────┐
│                  SaaS Application                   │
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────────┐  Request  ┌──────────────────┐  │
│  │ Tenant A     │──────────►│  Auth Service     │  │
│  │ (Company X)  │           │  (Service         │  │
│  │              │◄──────────│   Principal)      │  │
│  └──────────────┘  Token    └────────┬─────────┘  │
│                                      │             │
│  ┌──────────────┐           ┌────────▼─────────┐  │
│  │ Tenant B     │           │  Token Generator  │  │
│  │ (Company Y)  │           │  (Per-Tenant      │  │
│  └──────────────┘           │   Embed Token)    │  │
│                              └────────┬─────────┘  │
│                                      │             │
│                    ┌─────────────────┼──────────┐  │
│                    ▼                 ▼          ▼  │
│            ┌────────────┐  ┌────────────┐  ┌───┐  │
│            │ Workspace A│  │ Workspace B│  │...│  │
│            │ Dataset A  │  │ Dataset B  │  │   │  │
│            │ Report A   │  │ Report B   │  │   │  │
│            └────────────┘  └────────────┘  └───┘  │
└────────────────────────────────────────────────────┘
```

**Python — Multi-Tenant Token Generation:**
```python
import msal

# Service Principal authentication
app = msal.ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}"
)

def get_embed_token(tenant_config):
    """Generate embed token for specific tenant"""
    # 1. Get Azure AD token
    token = app.acquire_token_for_client(
        scopes=["https://analysis.windows.net/powerbi/api/.default"]
    )

    # 2. Generate Embed Token with RLS identity
    embed_request = {
        "datasets": [{"id": tenant_config["dataset_id"]}],
        "reports": [{"id": tenant_config["report_id"]}],
        "identities": [{
            "username": tenant_config["tenant_id"],
            "roles": ["TenantFilter"],
            "datasets": [tenant_config["dataset_id"]]
        }]
    }

    embed_token = requests.post(
        f"{BASE_URL}/GenerateToken",
        headers={"Authorization": f"Bearer {token['access_token']}"},
        json=embed_request
    ).json()

    return embed_token["token"]
```

### Dynamic Dataset Binding

> เปลี่ยน dataset ที่ผูกกับ report **แบบ runtime** — หน้าจอเดียว, ข้อมูลคนละ DB

```python
# Dynamic Dataset Binding — สลับ dataset ตาม user identity
def rebind_report(report_id, target_dataset_id, group_id):
    """Rebind report to different dataset at runtime"""
    response = requests.post(
        f"{BASE_URL}/groups/{group_id}/reports/{report_id}/Rebind",
        headers=HEADERS,
        json={"datasetId": target_dataset_id}
    )
    return response.status_code == 200

# Use case: ลูกค้า A → Dataset Thailand, ลูกค้า B → Dataset Japan
tenant_datasets = {
    "tenant_a": {"dataset_id": "ds-thailand", "report_id": "shared-report"},
    "tenant_b": {"dataset_id": "ds-japan", "report_id": "shared-report"},
    "tenant_c": {"dataset_id": "ds-usa", "report_id": "shared-report"},
}

def serve_tenant(tenant_id):
    config = tenant_datasets[tenant_id]
    rebind_report(config["report_id"], config["dataset_id"], GROUP_ID)
    token = get_embed_token(config)
    return {"embedUrl": EMBED_URL, "token": token}
```

---

## 🔐 Omnipotent: Data Sovereignty & Security Engineering

> **ผู้คุมกฎสูงสุด** — แม้ Microsoft ก็แตะข้อมูลไม่ได้

### Double Key Encryption (DKE)

> กุญแจ **2 ดอก** — ดอกหนึ่งคุณถือ, อีกดอก Microsoft ถือ → ต้องมีทั้งคู่ถึงถอดรหัสได้

```
┌──────────────────────────────────────────────────────┐
│              Double Key Encryption                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────┐         ┌─────────────┐            │
│  │  Key 1 🔑    │         │  Key 2 🗝️    │            │
│  │  (Your HSM)  │         │  (Microsoft  │            │
│  │  On-premises │         │   Azure KV)  │            │
│  └──────┬──────┘         └──────┬──────┘            │
│         └──────────┬───────────┘                    │
│              ┌─────▼─────┐                          │
│              │ Encrypted │                          │
│              │  Content  │                          │
│              └───────────┘                          │
│                                                      │
│  ✅ ทั้ง 2 ดอกต้องมี → ถึงถอดรหัสได้                  │
│  ❌ Microsoft มีแค่ดอกเดียว → อ่านไม่ได้               │
│  ❌ คุณมีแค่ดอกเดียว → อ่านไม่ได้                      │
└──────────────────────────────────────────────────────┘
```

| Component | ที่อยู่ | ใครควบคุม |
|-----------|--------|----------|
| **Key 1** | Your on-premises HSM | คุณ 100% |
| **Key 2** | Azure Key Vault | Microsoft (managed) |
| **Sensitivity Label** | Microsoft Purview | คุณ (config) |
| **Encryption at rest** | Azure Storage | Automatic |
| **Encryption in transit** | TLS 1.3 | Automatic |

### Dynamic RLS + OLS Integration

> ระบบ security อัตโนมัติที่ **sync กับ HR / Active Directory**

```python
# Dynamic RLS — ดึงสิทธิ์จาก Active Directory อัตโนมัติ
import ldap3

def sync_rls_from_ad():
    """Sync user permissions from Active Directory to PBI model"""
    # 1. Connect to AD
    server = ldap3.Server("ldap://ad.company.com")
    conn = ldap3.Connection(server, user="admin", password="***")
    conn.bind()

    # 2. Get user-region mapping
    conn.search(
        "ou=users,dc=company,dc=com",
        "(objectClass=person)",
        attributes=["mail", "department", "l"]  # l = location
    )

    # 3. Build RLS mapping table
    rls_mapping = []
    for entry in conn.entries:
        rls_mapping.append({
            "email": str(entry.mail),
            "region": str(entry.l),
            "department": str(entry.department),
            "security_level": get_security_level(entry)  # Custom logic
        })

    # 4. Push to Power BI dataset (Security table)
    push_to_dataset(rls_mapping, "SecurityMapping")
    return len(rls_mapping)
```

**model.bim — Dynamic RLS + OLS combined:**
```json
{
  "roles": [{
    "name": "DynamicAccess",
    "modelPermission": "read",
    "tablePermissions": [{
      "name": "Sales",
      "filterExpression": "VAR _UserEmail = USERPRINCIPALNAME() VAR _AllowedRegions = CALCULATETABLE(VALUES(SecurityMapping[Region]), SecurityMapping[Email] = _UserEmail) RETURN Sales[Region] IN _AllowedRegions"
    }],
    "columnPermissions": [{
      "name": "Salary",
      "metadataPermission": "none"
    }, {
      "name": "SSN",
      "metadataPermission": "none"
    }]
  }]
}
```

### Automated Governance via Scanner API + Purview

> สแกน + จัดหมวดหมู่ + ตรวจ PII **อัตโนมัติ** ทั้งองค์กร

```python
# Automated Governance Pipeline
import requests
from datetime import datetime

class GovernanceScanner:
    def __init__(self, headers):
        self.headers = headers
        self.issues = []

    def scan_all_workspaces(self):
        """สแกนทุก workspace ในองค์กร"""
        workspaces = requests.get(
            f"{BASE_URL}/admin/groups?$top=5000",
            headers=self.headers
        ).json()["value"]

        for ws in workspaces:
            self.scan_workspace(ws["id"], ws["name"])

        return self.generate_report()

    def scan_workspace(self, ws_id, ws_name):
        """สแกน workspace เดี่ยว"""
        # 1. Get workspace scan info
        scan = requests.post(
            f"{BASE_URL}/admin/workspaces/getInfo",
            headers=self.headers,
            json={
                "workspaces": [ws_id],
                "datasetExpressions": True,
                "datasetSchema": True,
                "datasourceDetails": True
            }
        ).json()

        # 2. Check for PII columns
        for dataset in scan.get("datasets", []):
            for table in dataset.get("tables", []):
                for col in table.get("columns", []):
                    if self.is_pii(col["name"]):
                        self.issues.append({
                            "type": "PII_DETECTED",
                            "severity": "CRITICAL",
                            "workspace": ws_name,
                            "table": table["name"],
                            "column": col["name"],
                            "action": "Apply Sensitivity Label + OLS"
                        })

        # 3. Check DAX best practices
        for dataset in scan.get("datasets", []):
            for measure in dataset.get("expressions", []):
                if "FILTER(ALL(" in measure.get("expression", ""):
                    self.issues.append({
                        "type": "DAX_ANTI_PATTERN",
                        "severity": "WARNING",
                        "detail": "FILTER(ALL()) detected — use CALCULATE instead"
                    })

    def is_pii(self, column_name):
        """ตรวจว่า column มีชื่อที่บ่งชี้ PII"""
        pii_patterns = [
            "ssn", "social_security", "id_card", "passport",
            "email", "phone", "address", "salary", "bank_account",
            "credit_card", "birthdate", "national_id"
        ]
        return any(p in column_name.lower() for p in pii_patterns)

    def generate_report(self):
        """สร้างรายงาน Governance"""
        critical = [i for i in self.issues if i["severity"] == "CRITICAL"]
        warnings = [i for i in self.issues if i["severity"] == "WARNING"]
        return {
            "scan_date": datetime.utcnow().isoformat(),
            "total_issues": len(self.issues),
            "critical": len(critical),
            "warnings": len(warnings),
            "issues": self.issues
        }

# รัน scan ทุกสัปดาห์
scanner = GovernanceScanner(HEADERS)
report = scanner.scan_all_workspaces()
```

**Purview Integration:**

| Purview Feature | ทำอะไรกับ PBI | ผลลัพธ์ |
|----------------|--------------|---------|
| **Data Catalog** | จัดหมวด datasets ทั้งองค์กร | ค้นหาได้ง่าย |
| **Auto-Classification** | ตรวจ PII อัตโนมัติ (AI) | ป้องกัน data breach |
| **Sensitivity Labels** | ติด label → บังคับ policy | ห้าม export/print |
| **Data Lineage** | แสดง flow: Source → PBI → Export | ตรวจสอบได้ทุกจุด |
| **Access Policies** | บังคับ access ตาม label | Zero-trust security |

> ♾️ **เป้าหมาย Omnipotent**: ออกแบบระบบที่ **ไม่มีขีดจำกัด** — Performance ระดับ Petabytes, Security แม้ Microsoft ยังแตะไม่ได้, Architecture ที่รองรับผู้ใช้ทั่วโลก

---

# 📘 PART 2: Power BI Practical Guide (End-to-End)

> คู่มือทักษะ Power BI แบบใช้งานได้จริง — ครอบคลุมตั้งแต่ติดตั้งจนถึง CI/CD

## Executive Summary & Workflow

```
flowchart LR
A[กำหนดโจทย์ธุรกิจ/KPI]
  → B[เลือกไลเซนส์ & สถาปัตยกรรม]
  → C[Connect data: Import/DirectQuery/Composite]
  → D[Power Query (M): Transform + Query folding]
  → E[Data Model: Star schema + Relationship]
  → F[DAX Measures: KPI/Time intelligence/RLS]
  → G[Report UX: Visual + Interaction]
  → H[Publish: Workspace/App + Permissions]
  → I[Refresh: Schedule + Gateway + Incremental]
  → J[Governance: Sensitivity labels/Standards]
  → K[CI/CD + Versioning + REST API Automation]
```

---

## 🎯 กลุ่มเป้าหมาย & พื้นฐานที่ควรรู้

| กลุ่ม | ต้องการ | ควรรู้ก่อน |
|-------|--------|-----------|
| **Business/Analyst** | Dashboard จาก Excel/CSV แชร์ให้ทีม | พื้นฐาน Excel, การอ่านกราฟ |
| **BI Developer** | โมเดลถูกต้อง, DAX, Performance, ทำงานเป็นทีม | SQL พื้นฐาน, Dimensional modeling |
| **Data/Platform/IT Admin** | Gateway, Refresh, สิทธิ์, Governance, API | Network, Azure AD, Security concepts |

> ⚠️ Power BI Desktop = Windows only (Win 10/Server 2016+), 64-bit เท่านั้น

---

## 📊 Competency Levels

| Level | ทำได้อะไร |
|-------|----------|
| **Beginner** | รายงานจากไฟล์/Excel, clean data ง่ายๆ, visual พื้นฐาน, SUM/COUNT, publish My workspace |
| **Intermediate** | Star schema, CALCULATE/time intelligence, drillthrough/bookmark, refresh+gateway, workspace/app+roles |
| **Advanced** | Performance tuning, incremental refresh, dynamic RLS, sensitivity labels, PBIP+Git+Pipeline+API |

---

## 💳 Licensing & Pricing Comparison

| ตัวเลือก | เหมาะกับ | แชร์ได้ | ราคาอ้างอิง |
|----------|--------|--------|------------|
| **Free** | ทดลอง/ของตัวเอง | ❌ แชร์ไม่ได้ | Free |
| **Pro** | ทีมขนาดเล็ก-กลาง | ✅ ผู้รับต้อง Pro/PPU | **US$14**/user/เดือน |
| **PPU** | ผู้พัฒนาขั้นสูง | ✅ + ฟีเจอร์ Premium | **US$24**/user/เดือน |
| **Premium/Fabric** | องค์กร (free viewers) | ✅ free user ดูได้ (≥F64) | Variable (capacity) |
| **Embedded** | ฝังในแอป | ✅ ลูกค้าภายนอก | Variable |

> ⚠️ ถ้า workspace ไม่ใช่ Premium → ทั้งผู้แชร์และผู้รับต้องมี Pro/PPU
> ✅ ถ้ามี Premium capacity (≥F64/P1) → free user ดูได้

---

## 🔌 Data Connection Examples (M Code)

### Excel Workbook

```m
let
    Source = Excel.Workbook(File.Contents("C:\data\sales.xlsx"), null, true),
    SalesSheet = Source{[Item="Sales",Kind="Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(SalesSheet, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"OrderDate", type date},
            {"OrderId", type text},
            {"CustomerId", type text},
            {"ProductId", type text},
            {"Quantity", Int64.Type},
            {"SalesAmount", type number}
        }
    )
in
    Typed
```

### CSV File

```m
let
    Source = Csv.Document(
        File.Contents("C:\data\sales.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(PromotedHeaders,
        {{"OrderDate", type date}, {"SalesAmount", type number}})
in
    Typed
```

### SQL Server

```m
let
    Source = Sql.Database(
        "SQLSERVER01\INST01", "RetailDW",
        [Query="
            SELECT s.OrderDate, s.OrderId, s.CustomerKey, s.ProductKey,
                   s.Quantity, s.SalesAmount
            FROM dbo.FactSales s
            WHERE s.OrderDate >= DATEADD(year,-2,GETDATE());
        "]
    )
in
    Source
```

### MySQL

```m
let
    Source = MySQL.Database(
        "mysql-host.company.local", "retail",
        [ReturnSingleDatabase=true,
         Query="SELECT order_date, order_id, customer_id, product_id,
                       quantity, sales_amount
                FROM fact_sales
                WHERE order_date >= CURDATE() - INTERVAL 365 DAY;"]
    )
in
    Source
```

### PostgreSQL

```m
let
    Source = PostgreSQL.Database(
        "postgres.company.local", "retail",
        [Query="SELECT order_date, order_id, customer_id, product_id,
                       quantity, sales_amount
                FROM fact_sales
                WHERE order_date >= CURRENT_DATE - INTERVAL '365 days';"]
    )
in
    Source
```

### Web/REST API

```m
let
    Source = Json.Document(
        Web.Contents("https://api.example.com",
            [RelativePath="v1/sales/daily",
             Query=[start="2025-01-01", end="2025-12-31"],
             Headers=[Accept="application/json"]]
        )
    ),
    Data = Source[data],
    ToTable = Table.FromList(Data, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    Expand = Table.ExpandRecordColumn(ToTable, "Column1",
        {"date","revenue","orders"}, {"Date","Revenue","Orders"}),
    Typed = Table.TransformColumnTypes(Expand,
        {{"Date", type date}, {"Revenue", type number}, {"Orders", Int64.Type}})
in
    Typed
```

### SharePoint (แนวทาง)

| Use case | Connector | วิธี |
|----------|-----------|------|
| หลายไฟล์ใน library | SharePoint folder | Combine + Transform |
| List/รายการ | SharePoint Online List | กำหนด column types ตั้งแต่ต้น |

---

## 🔧 Power Query Best Practices

| หลักการ | ทำไม | วิธี |
|---------|------|------|
| **ตั้ง data types เร็ว** | ลด error + ช่วย compression | `Table.TransformColumnTypes` |
| **Query folding** | ส่ง transformation ไปทำที่ต้นทาง | ใช้ native functions, filter ก่อน transform |
| **Filter early** | ลดข้อมูลที่ดึง | `Table.SelectRows` ก่อน join/expand |
| **Remove columns early** | ลด memory | `Table.RemoveColumns` ก่อน load |

### M Transformation Snippets

**1) เปลี่ยนชนิดคอลัมน์:**
```m
Table.TransformColumnTypes(Source,
    {{"OrderDate", type date}, {"Quantity", Int64.Type}, {"SalesAmount", type number}})
```

**2) แปลงค่าเฉพาะคอลัมน์:**
```m
Table.TransformColumns(Source,
    {{"OrderId", Text.Trim, type text}, {"CustomerId", Text.Upper, type text}})
```

**3) เพิ่มคอลัมน์คำนวณ + จัดการ error:**
```m
let
    Added = Table.AddColumn(Source, "UnitPrice",
        each try [SalesAmount] / [Quantity] otherwise null, type number),
    Cleaned = Table.ReplaceErrorValues(Added, {{"UnitPrice", null}})
in
    Cleaned
```

**4) Combine หลายไฟล์ CSV จากโฟลเดอร์:**
```m
let
    Source = Folder.Files("C:\data\retail\daily_csv"),
    OnlyCsv = Table.SelectRows(Source, each Text.EndsWith([Extension], ".csv")),
    ToTables = Table.AddColumn(OnlyCsv, "Data",
        each Csv.Document([Content], [Delimiter=",", Encoding=65001])),
    Expanded = Table.ExpandTableColumn(ToTables, "Data",
        {"Column1","Column2","Column3","Column4","Column5","Column6"},
        {"OrderDate","OrderId","CustomerId","ProductId","Quantity","SalesAmount"}),
    Typed = Table.TransformColumnTypes(Expanded,
        {{"OrderDate", type date}, {"Quantity", Int64.Type}, {"SalesAmount", type number}})
in
    Typed
```

### Incremental Refresh — M Parameter

```m
// สร้าง parameters: RangeStart, RangeEnd (ชนิด datetime)
let
    Source = Sql.Database("SQLSERVER01\INST01", "RetailDW"),
    Sales = Source{[Schema="dbo", Item="FactSales"]}[Data],
    Filtered = Table.SelectRows(Sales,
        each [OrderDateTime] >= RangeStart and [OrderDateTime] < RangeEnd)
in
    Filtered
// ⚠️ ต้องรักษา query folding → filter pushdown ไป SQL
```

---

## ⭐ Star Schema Design

```
┌─────────────┐     ┌─────────────────────────────────────┐     ┌─────────────┐
│  DIM_DATE    │     │            FACT_SALES                │     │ DIM_PRODUCT  │
│─────────────│     │─────────────────────────────────────│     │─────────────│
│ DateKey (PK) │◄────│ DateKey (FK)                         │────►│ ProductKey   │
│ Date         │     │ ProductKey (FK)                      │     │ ProductName  │
│ Year         │     │ CustomerKey (FK)                     │     │ Category     │
│ Month        │     │ StoreKey (FK)                        │     │ Brand        │
│ MonthName    │     │ Quantity                             │     └─────────────┘
└─────────────┘     │ SalesAmount                          │
                    │ CostAmount                           │     ┌─────────────┐
┌─────────────┐     └─────────────────────────────────────┘     │ DIM_STORE    │
│ DIM_CUSTOMER │                                                │─────────────│
│─────────────│                                                │ StoreKey     │
│ CustomerKey  │                                                │ StoreName    │
│ CustomerName │                                                │ Province     │
│ Segment      │                                                └─────────────┘
│ Region       │
└─────────────┘
```

| หลักการ | ✅ ทำ | ❌ ห้าม |
|---------|------|--------|
| Relationship | 1-to-many (Dim→Fact) | Many-to-many โดยไม่จำเป็น |
| Cross filter | Single direction | Bi-directional โดยไม่จำเป็น |
| Active relationship | ใช้เป็นค่าเริ่มต้น | Inactive ทุก relationship |
| Keys | Integer surrogate keys | Text/composite keys |

---

## 📐 DAX Fundamentals

### Core Functions

| Function | ทำอะไร | ใช้เมื่อ |
|----------|--------|---------|
| `CALCULATE` | ประเมิน expression ภายใต้ filter context ที่ปรับแล้ว | เกือบทุก measure ที่ซับซ้อน |
| `FILTER` | คืนตารางที่กรองแล้ว | เงื่อนไขซับซ้อน/เกี่ยวข้องกับ measure |
| `ALL` | ลบ filter context ของ column/table | % of total, benchmark |
| `REMOVEFILTERS` | ล้าง filter (modifier) | ลบ filter context เฉพาะจุด |

### Basic Measures

```dax
-- ยอดขายรวม
[Total Sales] = SUM(FactSales[SalesAmount])

-- จำนวนคำสั่งซื้อ
[Orders] = DISTINCTCOUNT(FactSales[OrderId])

-- จำนวนลูกค้า
[Customers] = DISTINCTCOUNT(FactSales[CustomerKey])
```

### CALCULATE + FILTER

```dax
-- ยอดขายเฉพาะ "Bikes"
[Sales Bikes] =
CALCULATE([Total Sales], FILTER(DimProduct, DimProduct[Category] = "Bikes"))

-- Best practice: ใช้ Boolean filter แทน FILTER เมื่อทำได้
[Sales Bikes v2] =
CALCULATE([Total Sales], DimProduct[Category] = "Bikes")
```

### ALL / REMOVEFILTERS — % of Total

```dax
-- % ยอดขายเทียบทุกสินค้า (ยังคง filter อื่นเช่น Date/Region)
[Sales % of All Products] =
DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(DimProduct)))

-- ยอดขาย "ไม่สนใจ filter วันที่"
[Sales Ignore Date] =
CALCULATE([Total Sales], REMOVEFILTERS(DimDate))
```

### Time Intelligence

```dax
-- Year-to-Date
[Sales YTD] = TOTALYTD([Total Sales], DimDate[Date])

-- Same Period Last Year
[Sales SPLY] = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DimDate[Date]))

-- % Year-over-Year
[Sales YoY %] =
VAR CurrentSales = [Total Sales]
VAR LastYearSales = [Sales SPLY]
RETURN DIVIDE(CurrentSales - LastYearSales, LastYearSales)
```

---

## 🔒 Row-Level Security (RLS)

### Dynamic RLS — ผู้ใช้เห็นเฉพาะภูมิภาคของตน

**ตาราง MapUserRegion:**

| UPN (อีเมล) | RegionKey |
|-------------|-----------|
| user1@co.th | 1 |
| user1@co.th | 2 |
| user2@co.th | 3 |

**Role filter (ใส่ที่ MapUserRegion):**
```dax
MapUserRegion[UPN] = USERPRINCIPALNAME()
```

> ⚠️ RLS มีผลกับ **Viewer** เท่านั้น — Admin/Member/Contributor ไม่ถูก filter
> ⚠️ RLS ถูกแปะเป็น filter อัตโนมัติในทุก DAX query → ทดสอบ performance ด้วยข้อมูลจริง

---

## 🎨 Report Design Best Practices

### Performance

| ✅ ทำ | ❌ ห้าม |
|------|--------|
| จำกัด datapoints ต่อ visual | ยัดข้อมูลหมื่นจุดใน visual เดียว |
| ใช้ drilldown/drillthrough แทน | แสดงทุก detail ในหน้าเดียว |
| จำกัดจำนวน visuals ต่อหน้า | ≥15 visuals ในหน้าเดียว |
| ใช้ filter ที่จำกัดที่สุด | ไม่มี default filter |

### Interactivity

| Feature | ทำอะไร | ใช้เมื่อ |
|---------|--------|---------|
| **Slicers** | ตัวกรองบนหน้า report | ให้ผู้ใช้จำกัดข้อมูลด้วยตัวเอง |
| **Bookmarks** | บันทึกสถานะหน้า report | Guided analytics, เมนูนำทาง |
| **Drillthrough** | นำทางจากสรุป → รายละเอียด | วิเคราะห์เจาะลึกตาม context |

### Accessibility (มาตรฐาน ไม่ใช่ option)

| ต้องทำ | วิธี |
|--------|------|
| Keyboard navigation | ตั้ง tab order |
| Screen reader support | ใส่ alt text ทุก visual |
| High contrast | ทดสอบ high contrast mode |
| Color blind friendly | ไม่ใช้สีเดียวแยกข้อมูล |

---

## 🚀 Publish & Governance

### Workspace Roles

| Role | สร้าง/แก้ content | Publish | ลบ content | จัดการสิทธิ์ |
|------|-----------------|---------|-----------|------------|
| **Admin** | ✅ | ✅ | ✅ | ✅ |
| **Member** | ✅ | ✅ | ✅ | ❌ |
| **Contributor** | ✅ | ✅ | ❌ (ของตัวเอง) | ❌ |
| **Viewer** | ❌ | ❌ | ❌ | ❌ |

### Refresh & Gateway

| Component | ทำอะไร | ระวัง |
|-----------|--------|-------|
| **Scheduled refresh** | ตั้งเวลา refresh dataset | Map server/DB ให้ตรงกับ gateway |
| **On-premises gateway** | เชื่อมแหล่งข้อมูลภายใน | Standard vs Personal mode |
| **Incremental refresh** | Refresh เฉพาะ partition ที่เปลี่ยน | ต้องรักษา query folding |

### Sensitivity Labels (Microsoft Purview)

| Label | ผลเมื่อ export | ผลใน Desktop |
|-------|---------------|-------------|
| Public | ไม่จำกัด | ไม่จำกัด |
| Internal | ติด label ตาม policy | ไม่จำกัด |
| Confidential | บังคับ encryption | ต้องมีสิทธิ์เปิดไฟล์ |
| Highly Confidential | ห้าม export บาง format | ต้องมีสิทธิ์ + encryption |

---

## 🔄 CI/CD: PBIP + Git + Pipeline

### PBIP Project Structure

```
Project/
├── Retail.Report/          ← Report definition
├── Retail.SemanticModel/   ← Data model
├── .gitignore
└── Retail.pbip             ← Project file
```

> ⚠️ PBIP ยังเป็น Preview → เปิดใน File > Options > Preview features

### Deployment Pipelines

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Dev          │────►│  Test         │────►│  Prod         │
│  Workspace    │     │  Workspace    │     │  Workspace    │
│               │     │  QA + Rules   │     │  Live users   │
└──────────────┘     └──────────────┘     └──────────────┘
```

### REST API Automation

**Trigger refresh:**
```http
POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes
Authorization: Bearer {access_token}
Content-Type: application/json

{"notifyOption": "MailOnFailure"}
```

**Check refresh history:**
```http
GET https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes?$top=20
Authorization: Bearer {access_token}
```

> ⚠️ Shared capacity มีข้อจำกัด request/วัน; enhanced refresh ต้องใช้ Premium

---

## 📋 Project Templates

### Template A: Retail Sales Analytics

**Schema:** `FactSales(DateKey, StoreKey, ProductKey, CustomerKey, Quantity, SalesAmount, CostAmount)` + DimDate, DimStore, DimProduct, DimCustomer

**DAX Measures:**
```dax
[Total Cost] = SUM(FactSales[CostAmount])
[Gross Profit] = [Total Sales] - [Total Cost]
[Gross Margin %] = DIVIDE([Gross Profit], [Total Sales])
[Sales YTD] = TOTALYTD([Total Sales], DimDate[Date])
[Sales YoY %] =
    VAR LY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DimDate[Date]))
    RETURN DIVIDE([Total Sales] - LY, LY)
```

**Folder Structure:**
```
retail-sales-analytics/
├── powerbi/
│   ├── RetailSales.pbip
│   ├── RetailSales.Report/
│   └── RetailSales.SemanticModel/
├── data/raw/ + sample/
├── sql/extract_fact_sales.sql + dims/
├── docs/kpi-definition.md + data-dictionary.md
└── ops/refresh-plan.md + gateway-setup.md
```

### Template B: Marketing Analytics

**Schema:** `FactSessions(DateKey, ChannelKey, CampaignKey, Sessions, Users, Conversions, Revenue)` + DimDate, DimChannel, DimCampaign, DimLandingPage

**DAX Measures:**
```dax
[Conversion Rate] = DIVIDE([Conversions], [Sessions])
[Revenue per Session] = DIVIDE([Total Revenue], [Sessions])
```

**Folder Structure:**
```
marketing-analytics/
├── powerbi/Marketing.pbip + Report/ + SemanticModel/
├── data/staging/
├── m/web-api-queries.md
├── docs/metric-definition.md
└── ops/refresh-schedule.md + data-quality-checks.md
```

### Template C: Finance Actual vs Budget

**Schema:** `FactGLPosting(DateKey, AccountKey, CostCenterKey, Amount, DocumentNo)` + `FactBudget(DateKey, AccountKey, CostCenterKey, BudgetAmount)` + DimDate, DimAccount, DimCostCenter

**DAX Measures:**
```dax
[Actual] = SUM(FactGLPosting[Amount])
[Budget] = SUM(FactBudget[BudgetAmount])
[Variance] = [Actual] - [Budget]
[Variance %] = DIVIDE([Variance], [Budget])
```

**RLS:** ใช้ mapping user → CostCenterKey + `USERPRINCIPALNAME()`

**Folder Structure:**
```
finance-avb/
├── powerbi/FinanceAVB.pbip + Report/ + SemanticModel/
├── sql/extract_gl.sql + extract_budget.sql + dims.sql
├── docs/chart-of-accounts.md + rls-design.md
└── ops/gateway.md + refresh.md + access-control.md
```

---

## ✅ Pre-Production Checklists

### Checklist 1: คุณภาพโมเดล

- [ ] คอลัมน์ที่ไม่ใช้ถูกลบตั้งแต่ Power Query
- [ ] โมเดลเป็น Star schema, หลีกเลี่ยง many-to-many
- [ ] Relationship เป็น single direction, active relationship เป็นค่าเริ่มต้น
- [ ] Measures ใช้ Boolean filter แทน FILTER เมื่อทำได้
- [ ] ทดสอบ performance กับ RLS

### Checklist 2: รายงาน/UX

- [ ] หน้าแรกตอบคำถามหลักได้ใน 10-30 วินาที
- [ ] Slicer ไม่เยอะเกิน + ตั้ง default สมเหตุสมผล
- [ ] Drillthrough มีปุ่มกลับ + flow ชัดเจน
- [ ] Alt text + tab order + accessibility ครบ
- [ ] จำนวน datapoints ต่อ visual ไม่เกิน threshold

### Checklist 3: Production/Ops/Governance

- [ ] Workspace roles กำหนดตามหน้าที่
- [ ] Refresh schedule ทดสอบผ่าน + credential/gateway mapping ตรง
- [ ] Sensitivity labels + นโยบาย export กำหนดแล้ว (ถ้าข้อมูลอ่อนไหว)
- [ ] CI/CD: PBIP + Git + deployment pipeline พร้อม

---

## 📅 8-Week Study Timeline

| สัปดาห์ | หัวข้อ | Checkpoint |
|---------|--------|-----------|
| **1** | Install Desktop + เข้าใจ license/service | ✅ เปิด PBI Desktop ได้ |
| **2** | Connect data + Power Query basics | ✅ มีตารางพร้อมทำโมเดล |
| **3** | Star schema + relationships | ✅ โมเดล dim/fact ถูกต้อง |
| **4** | DAX basics (measures + CALCULATE) | ✅ มี KPI measures ≥10 ตัว |
| **5** | Time intelligence + performance | ✅ YTD/YoY + DAX Studio check |
| **6** | Report design + interactivity | ✅ Slicer + bookmark/drillthrough + performance ผ่าน |
| **7** | Publish/share/workspace + refresh/gateway | ✅ Publish เป็น app + refresh schedule |
| **8** | Governance + PBIP/Git + API | ✅ CI/CD pipeline + versioning + automation |

> 📘 **แนะนำ**: เริ่มจาก **Template A (Retail)** เพื่อฝึกครบวงจร → ค่อยไป Marketing/Finance ตามสายงาน

---

# 🔥 PART 3: Advanced Pro-Tips & Beyond

> เทคนิคเจาะลึกที่ทำให้รายงาน "ก้าวข้ามกราฟธรรมดา" ไปสู่ระบบวิเคราะห์ระดับสูง

---

## 🎯 1. Requirement Gathering Pro-Tips

### User Persona Analysis

| ❌ ถามแบบเดิม | ✅ ถามแบบ Pro |
|-------------|------------|
| "อยากเห็นอะไรในรายงาน?" | "เห็นแล้วจะทำอะไรต่อ? (Actionable Insight)" |
| "ต้องการกราฟอะไร?" | "ตัดสินใจอะไรจากข้อมูลนี้?" |
| "ข้อมูลอะไรบ้าง?" | "KPI ไหนที่ถ้าเปลี่ยน 10% จะกระทบธุรกิจมากที่สุด?" |

### Wireframe/Mockup Design

ร่างแบบรายงานก่อนลงมือทำ:

```
┌──────────────────────────────────────────────┐
│  📊 Sales Dashboard                    [🔍]  │
├──────────┬──────────┬──────────┬─────────────┤
│ Revenue  │ Orders   │ Margin % │ vs LY       │
│ ▓▓▓ 2.4M │ ▓▓ 12K  │ ▓▓ 35%  │ ↗ +12%     │
├──────────┴──────────┴──────────┴─────────────┤
│ [Slicer: Year ▼] [Slicer: Region ▼]         │
├─────────────────────┬────────────────────────┤
│  Sales Trend (Line) │  Top 10 Products (Bar) │
│  ~~~~~/\~~~~        │  ████████ Product A    │
│  ~~~/~~~~\~~        │  ██████   Product B    │
│                     │  ████     Product C    │
├─────────────────────┴────────────────────────┤
│  Sales by Region (Map)   → Drillthrough →    │
│  [🗺️]                     [Detail Page]      │
└──────────────────────────────────────────────┘
```

> 💡 ร่างใน PowerPoint/กระดาษก่อน → ลดเวลาแก้ไขใน Power BI 50%+

---

## ⭐ 2. Advanced Data Modeling

### Bridge Table — Many-to-Many Pattern

เมื่อ 1 คำสั่งซื้อมีหลายหมวดหมู่ หรือ 1 ลูกค้ามีหลาย segment:

```
DimCategory ←(1:M)── BridgeOrderCategory ──(M:1)→ FactSales
```

```dax
-- Measure ที่ใช้กับ Bridge table (ป้องกัน double-count)
[Sales via Bridge] =
CALCULATE(
    [Total Sales],
    BridgeOrderCategory
) / CALCULATE(
    COUNTROWS(BridgeOrderCategory),
    ALLEXCEPT(BridgeOrderCategory, BridgeOrderCategory[OrderId])
)
```

> ⚠️ Bridge table ต้องมี filter direction **Both** + ใช้ `TREATAS` หรือ `CROSSFILTER` ในบาง scenario

### SCD Type 2 — Slowly Changing Dimensions

จัดการกรณีข้อมูล dimension เปลี่ยนแปลงตามเวลา (เช่น ลูกค้าเปลี่ยน region):

| CustomerKey | CustomerName | Region | ValidFrom | ValidTo | IsCurrent |
|-------------|-------------|--------|-----------|---------|-----------|
| 1001 | สมชาย | กรุงเทพ | 2024-01-01 | 2025-06-30 | FALSE |
| 1002 | สมชาย | เชียงใหม่ | 2025-07-01 | 9999-12-31 | TRUE |

```dax
-- ดึงเฉพาะ record ปัจจุบัน
[Current Customers] =
CALCULATE(
    DISTINCTCOUNT(DimCustomer[CustomerName]),
    DimCustomer[IsCurrent] = TRUE
)
```

### Composite Models

ผสม Import + DirectQuery ในโมเดลเดียวกัน:

```
┌─────────────────────────────────┐
│         Composite Model          │
├────────────────┬────────────────┤
│  Import Mode   │ DirectQuery    │
│  (เร็ว+cache)  │ (real-time)    │
│                │                │
│  DimDate       │ FactSales      │
│  DimProduct    │ (ข้อมูลล้าน+)  │
│  DimStore      │                │
│  DimCustomer   │ LiveInventory  │
└────────────────┴────────────────┘
```

| ข้อดี | ข้อจำกัด |
|-------|---------|
| Dimension import = เร็ว | ต้อง Premium/PPU สำหรับ remote models |
| Fact DirectQuery = real-time | DAX บางตัวไม่รองรับ DirectQuery |
| ลดขนาดไฟล์ .pbix | Relationship ระหว่าง mode มีข้อจำกัด |

### Role-Playing Dimensions

```dax
-- OrderDate ใช้ Active relationship
[Sales by Order Date] = [Total Sales]   -- ใช้ค่าเริ่มต้น

-- ShipDate ใช้ Inactive relationship → ต้อง USERELATIONSHIP
[Sales by Ship Date] =
CALCULATE(
    [Total Sales],
    USERELATIONSHIP(FactSales[ShipDateKey], DimDate[DateKey])
)
```

---

## 📐 3. Advanced DAX Patterns

### SWITCH + TRUE — Dynamic Classification

```dax
[Sales Category] =
SWITCH(
    TRUE(),
    [Total Sales] >= 1000000, "🟢 High",
    [Total Sales] >= 500000,  "🟡 Medium",
    [Total Sales] >= 100000,  "🟠 Low",
    "🔴 Very Low"
)
```

### Variables — Best Practice

```dax
[Profit Margin with Status] =
VAR TotalRev = [Total Sales]
VAR TotalCost = [Total Cost]
VAR Margin = DIVIDE(TotalRev - TotalCost, TotalRev)
VAR Status =
    SWITCH(
        TRUE(),
        Margin >= 0.3, "✅ Healthy",
        Margin >= 0.15, "⚠️ Watch",
        "🔴 Action Required"
    )
RETURN
    Margin

-- ใช้ VAR อีกตัวสำหรับ Status (วาง Measure แยก)
[Margin Status] =
VAR Margin = [Profit Margin with Status]
RETURN
    SWITCH(TRUE(), Margin >= 0.3, "Healthy", Margin >= 0.15, "Watch", "Action Required")
```

> 💡 ใช้ VAR เสมอ — อ่านง่าย + performance ดี (ประเมินแค่ครั้งเดียว)

### Calculation Groups (XMLA/Tabular Editor)

จัดกลุ่ม Time Intelligence ให้ใช้ซ้ำกับทุก measure:

```dax
-- สร้าง Calculation Group: "Time Calculation"
-- Item: "Current"
SELECTEDMEASURE()

-- Item: "YTD"
TOTALYTD(SELECTEDMEASURE(), DimDate[Date])

-- Item: "PY" (Previous Year)
CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR(DimDate[Date]))

-- Item: "YoY %"
VAR Current = SELECTEDMEASURE()
VAR PY = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR(DimDate[Date]))
RETURN DIVIDE(Current - PY, PY)
```

> ⚠️ ต้องใช้ Tabular Editor หรือ XMLA endpoint (Premium/PPU) — ไม่สามารถสร้างใน Desktop UI

### Field Parameters

ให้ผู้ใช้เลือกเปลี่ยน measure/column ที่แสดงใน visual แบบ dynamic:

```dax
// สร้างผ่าน Modeling > New parameter > Fields
Sales Metrics =
{
    ("Revenue", NAMEOF('FactSales'[SalesAmount]), 0),
    ("Quantity", NAMEOF('FactSales'[Quantity]), 1),
    ("Orders", NAMEOF('Measures'[Orders]), 2),
    ("Margin %", NAMEOF('Measures'[Gross Margin %]), 3)
}
```

> ✅ ใช้กับ Slicer → ผู้ใช้เลือก metric ที่ต้องการดูใน bar/line chart ได้เอง
> ⚠️ เปิดใน File > Options > Preview features > Field parameters

### What-if Parameters

สร้าง slider ให้ผู้ใช้ปรับสมมติฐานแบบ interactive:

```dax
// สร้างผ่าน Modeling > New parameter > What-if
// ตัวอย่าง: ปรับ Discount Rate 0% - 50%
Discount Rate = GENERATESERIES(0, 0.50, 0.01)

// Measure ที่ใช้ What-if
[Adjusted Revenue] =
[Total Sales] * (1 - SELECTEDVALUE('Discount Rate'[Discount Rate], 0))

[Revenue Impact] =
[Adjusted Revenue] - [Total Sales]
```

> ✅ เหมาะกับ Scenario analysis, Sensitivity analysis, Financial forecasting

---

## 📖 4. Data Storytelling & AI Visuals

### Narrative Flow — จัดวาง report ให้ "เล่าเรื่อง"

```
Page 1: Overview (บทนำ)
  → "ภาพรวมสถานการณ์เป็นอย่างไร?"
  → KPI cards + trend line + vs target

Page 2: Analysis (เนื้อหา)
  → "ทำไมถึงเป็นแบบนี้?"
  → Breakdown by category/region + anomaly highlights

Page 3: Action (บทสรุป)
  → "ต้องทำอะไรต่อ?"
  → Top issues + recommendations + drillthrough to detail
```

### Smart Narratives Visual

Auto-generate text สรุปข้อมูลจาก visual:

| ขั้นตอน | วิธี |
|---------|------|
| 1. เพิ่ม Smart Narrative visual | Insert > Smart narrative |
| 2. ปรับ template | กด "Review" แก้ข้อความ/เพิ่ม dynamic values |
| 3. ผสมกับ field references | เช่น: "ยอดขายรวม **{SalesAmount}** เพิ่มขึ้น **{YoY%}** จากปีก่อน" |

> ⚠️ Visual นี้รองรับ **ภาษาอังกฤษ** เป็นหลัก — ข้อความไทยต้องพิมพ์เอง

### Anomaly Detection (Line Chart)

| ขั้นตอน | วิธี |
|---------|------|
| 1. สร้าง Line chart (date + measure) | ลากเข้า visual |
| 2. เปิด Anomaly detection | Analytics pane > Find anomalies |
| 3. ปรับ Sensitivity | ค่าสูง = จับมากขึ้น, ค่าต่ำ = เฉพาะจุดผิดปกติชัด |
| 4. ดู Explanations | คลิก anomaly point → Power BI อธิบายสาเหตุ |

### Key Influencers Visual

ค้นหาว่า **ปัจจัยไหน** ส่งผลกระทบต่อ KPI มากที่สุด:

| ขั้นตอน | วิธี |
|---------|------|
| 1. เพิ่ม Key Influencers visual | Insert > Key influencers |
| 2. "Analyze" field | ลาก KPI ที่ต้องการวิเคราะห์ (เช่น Churn = Yes/No) |
| 3. "Explain by" fields | ลาก factors ที่อาจมีผล (เช่น Region, Tenure, Plan) |
| 4. อ่านผล | "When Region is X, Churn is **2.3x** more likely" |

> ✅ ใช้ ML ภายใน → ไม่ต้องเขียน code
> ⚠️ ต้องมี categorical target หรือ continuous measure

### Decomposition Tree

"ทำไม" แตกย่อยอัตโนมัติ:

| ขั้นตอน | วิธี |
|---------|------|
| 1. เพิ่ม Decomposition Tree | Insert > Decomposition tree |
| 2. "Analyze" = measure (เช่น [Total Sales]) | |
| 3. "Explain by" = dimensions (Category, Region, Channel) | |
| 4. คลิก "+" AI หรือ manual | AI = Power BI เลือกมิติที่ส่งผลมากที่สุด |

### Python/R Script Visuals

```python
# ตัวอย่าง: Heatmap ด้วย Seaborn ใน Power BI
import matplotlib.pyplot as plt
import seaborn as sns

# 'dataset' = ตัวแปร auto-generated จาก Power BI
pivot = dataset.pivot_table(values='SalesAmount',
                            index='Category',
                            columns='MonthName',
                            aggfunc='sum')
plt.figure(figsize=(12, 6))
sns.heatmap(pivot, annot=True, fmt=',.0f', cmap='YlOrRd')
plt.title('Sales Heatmap by Category × Month')
plt.tight_layout()
plt.show()
```

> ⚠️ ต้องติดตั้ง Python/R บนเครื่องที่เปิด Desktop + กำหนด path ใน Options
> ⚠️ Script visuals **ไม่ refresh อัตโนมัติ** ใน Power BI Service → ใช้ Personal Gateway

---

## 🎨 5. Advanced Interactivity

### Bookmarks as Navigation Menu

สร้างเมนูนำทางระหว่างหน้า:

| ขั้นตอน | วิธี |
|---------|------|
| 1. สร้าง Bookmark สำหรับแต่ละหน้า | View > Bookmarks > Add |
| 2. สร้างปุ่ม (Button/Image) | Insert > Button/Image |
| 3. กำหนด Action | Format > Action > Type = Bookmark > เลือก bookmark |
| 4. จัดวาง Navigation bar | วางปุ่มแถวเดียวกันทุกหน้า |

```
┌─────────────────────────────────────────┐
│  [📊 Overview] [📈 Trend] [🗺️ Region]  │  ← Navigation bar
├─────────────────────────────────────────┤
│  (เนื้อหาหน้านั้นๆ)                      │
└─────────────────────────────────────────┘
```

### Drillthrough with Custom Back Button

| ขั้นตอน | วิธี |
|---------|------|
| 1. สร้างหน้า Detail | ตั้ง drillthrough field (เช่น ProductKey) |
| 2. Power BI สร้างปุ่ม "Back" อัตโนมัติ | ปรับตำแหน่ง + style |
| 3. เพิ่ม Context | แสดง ProductName, Category ที่ถูก drillthrough |

```dax
-- แสดง context ในหน้า Drillthrough
[Drillthrough Product] =
IF(
    ISFILTERED(DimProduct[ProductName]),
    SELECTEDVALUE(DimProduct[ProductName], "All Products"),
    "All Products"
)
```

### Conditional Formatting

| ประเภท | ใช้กับ | ตัวอย่าง |
|--------|-------|---------|
| **Data Bars** | Table/Matrix columns | แถบสีตาม magnitude |
| **Color Scale** | Background/font | เขียว → แดง ตามค่า |
| **Icons** | Status indicators | ✅ 🟡 🔴 ตามเงื่อนไข |
| **Rules** | Category-based | ถ้า > target = สีเขียว |

```dax
-- Measure สำหรับ Conditional formatting (Icons)
[Performance Icon] =
VAR Achievement = DIVIDE([Total Sales], [Target Sales])
RETURN
    SWITCH(
        TRUE(),
        Achievement >= 1.0, 1,    -- ✅ On track
        Achievement >= 0.8, 2,    -- 🟡 At risk
        3                          -- 🔴 Below target
    )
```

### Tooltip Pages

สร้างหน้า Tooltip แบบ custom เพื่อแสดงข้อมูลเพิ่มเมื่อ hover:

| ขั้นตอน | วิธี |
|---------|------|
| 1. สร้างหน้าใหม่ | ตั้งขนาด = Tooltip (320×240 px) |
| 2. Page Information | เปิด "Allow use as tooltip" |
| 3. ออกแบบเนื้อหา | KPI cards, mini chart, ข้อมูลเพิ่ม |
| 4. ไปที่ visual ต้นทาง | Format > Tooltip > Page = เลือกหน้า tooltip |

---

## 🛡️ 6. Data Quality & Change Management

### Data Quality Monitoring

```
┌──────────────────────────────────────────────┐
│            Data Quality Framework             │
├──────────────┬───────────────────────────────┤
│  ขั้นตอน     │  สิ่งที่ตรวจสอบ                 │
├──────────────┼───────────────────────────────┤
│  Source       │  Connection status, schema    │
│  Transform    │  Null %, duplicates, outliers │
│  Model        │  Relationship integrity       │
│  Report       │  Visual rendering, RLS test   │
│  Service      │  Refresh success rate         │
└──────────────┴───────────────────────────────┘
```

### Data Profiling in Power Query

```m
// เปิด View > Column quality + Column distribution + Column profile
// เห็นได้ทันที:
// - Valid/Error/Empty %
// - Min/Max/Avg/Distinct count
// - Value distribution (histogram)

// ⚠️ ค่าเริ่มต้น profile แค่ 1,000 แถวแรก
// → เปลี่ยนเป็น "Column profiling based on entire data set" ที่ status bar
```

### Data Quality Measures (DAX)

```dax
-- ตรวจสอบ Null rate
[Null Rate %] =
DIVIDE(
    COUNTBLANK(FactSales[SalesAmount]),
    COUNTROWS(FactSales)
)

-- ตรวจสอบ Duplicate orders
[Duplicate Orders] =
SUMX(
    VALUES(FactSales[OrderId]),
    IF(CALCULATE(COUNTROWS(FactSales)) > 1, 1, 0)
)

-- Data freshness
[Last Refresh Date] =
MAX(FactSales[OrderDate])

[Days Since Last Data] =
DATEDIFF([Last Refresh Date], TODAY(), DAY)
```

### Change Management Process

| ขั้นตอน | กิจกรรม | ผู้รับผิดชอบ |
|---------|---------|------------|
| 1. Request | ผู้ใช้ส่ง Change Request | Business User |
| 2. Assess | ประเมินผลกระทบ + effort | BI Developer |
| 3. Develop | แก้ไขใน Dev workspace | BI Developer |
| 4. Test | ทดสอบใน Test workspace | QA + Business |
| 5. Deploy | Deploy ผ่าน Pipeline | BI Admin |
| 6. Validate | ตรวจสอบ production | Business User |
| 7. Document | อัพเดท data dictionary + changelog | BI Developer |

> 📘 **Learning Resources:** [Microsoft Learn — Power BI](https://learn.microsoft.com/power-bi/), [DAX Guide](https://dax.guide/), [SQLBI (Marco Russo & Alberto Ferrari)](https://www.sqlbi.com/), [Guy in a Cube (YouTube)](https://www.youtube.com/@GuyInACube)

---

## 📊 PBIR Complete Property Reference (~1,294 Properties)

> 📅 Consolidated จาก 81 sections, 70+ audit rounds, 72 ไฟล์ deep-read
> 🎯 ใช้เป็น reference สำหรับสร้าง Power BI Dashboard Generator

### สารบัญ (TOC)

1. [Visual Types (48+ ตัว)](#visual-types-complete)
2. [Report-Level Config](#report-level-config)
3. [Page/Section Config](#pagesection-config)
4. [Layout & Position](#layout--position)
5. [Projections/Data Roles](#projections-complete)
6. [Query & Prototype](#query--prototype)
7. [Axis Properties](#axis-properties)
8. [Legend](#legend-properties)
9. [Data Point](#datapoint-properties)
10. [Line Styles](#linestyles-properties)
11. [Labels/Data Labels](#labels-properties)
12. [Error Bars/Bands](#error-bars-properties)
13. [Reference Lines](#reference-lines)
14. [Small Multiples](#small-multiples-layout)
15. [Visual-Specific Properties](#visual-specific-properties)
16. [Color Systems](#color-systems)
17. [Selector Types](#selector-types)
18. [vcObjects](#vcobjects-properties)
19. [Filter Properties](#filter-properties)
20. [Textbox & Paragraphs](#textbox--paragraphs)
21. [Shape Types (23 แบบ)](#shape-types)
22. [Action Button States](#action-button-states)
23. [Theme Colors & Text Classes](#theme-colors--text-classes)
24. [Fill Types](#fill-types)
25. [PBIR vs PBIP Format](#pbir-vs-pbip-format)
26. [PBIR Decomposed Files](#pbir-decomposed-files)
27. [Bookmarks & Interactions](#bookmarks--interactions)
28. [Advanced Filters](#advanced-filters)
29. [Azure Maps](#azure-maps)
30. [Conditional Icons & Expressions](#conditional-icons--expressions)
31. [Mobile/Pods Layout](#mobilepods-layout)
32. [Dataset Schemas](#dataset-schemas)
33. [Resource Packages](#resource-packages)
34. [Visual Group Container](#visual-group-container)
35. [Base Theme visualStyles](#base-theme-visualstyles)

---

### Visual Types (Complete)

| # | visualType | Category | Projection Roles |
|---|-----------|----------|-----------------|
| 1 | `barChart` | Charts | Category, Y, Series |
| 2 | `columnChart` | Charts | Category, Y, Series |
| 3 | `clusteredBarChart` | Charts | Category, Y, Series |
| 4 | `clusteredColumnChart` | Charts | Category, Y, Series |
| 5 | `stackedBarChart` | Charts | Category, Y, Series |
| 6 | `stackedColumnChart` | Charts | Category, Y, Series |
| 7 | `hundredPercentStackedBarChart` | Charts | Category, Y, Series |
| 8 | `hundredPercentStackedColumnChart` | Charts | Category, Y, Series |
| 9 | `lineChart` | Charts | Category, Y, Series |
| 10 | `areaChart` | Charts | Category, Y, Series |
| 11 | `stackedAreaChart` | Charts | Category, Y, Series |
| 12 | `hundredPercentStackedAreaChart` | Charts | Category, Y, Series |
| 13 | `lineStackedColumnComboChart` | Charts | Category, Y, Y2, Series |
| 14 | `lineClusteredColumnComboChart` | Charts | Category, Y, Y2, Series |
| 15 | `ribbonChart` | Charts | Category, Y, Series |
| 16 | `waterfallChart` | Charts | Category, Y, Breakdown |
| 17 | `funnel` | Charts | Category, Y |
| 18 | `scatterChart` | Charts | Category, X, Y, Size, Series |
| 19 | `pieChart` | Charts | Category, Y |
| 20 | `donutChart` | Charts | Category, Y |
| 21 | `treemap` | Charts | Group, Values, Details |
| 22 | `map` | Maps | Category, Size, Series |
| 23 | `filledMap` | Maps | Location, Values |
| 24 | `shapeMap` | Maps | Location, Values |
| 25 | `azureMap` | Maps | Category, Size, Series |
| 26 | `gauge` | Indicators | Y, TargetValue |
| 27 | `card` | Cards | Values |
| 28 | `cardVisual` | Cards | Data |
| 29 | `multiRowCard` | Cards | Values |
| 30 | `kpi` | Indicators | Indicator, TrendLine, Goal |
| 31 | `slicer` | Filters | Values |
| 32 | `advancedSlicerVisual` | Filters | Values, Tooltips |
| 33 | `textSlicer` | Filters | Values |
| 34 | `listSlicer` | Filters | Values |
| 35 | `tableEx` | Tables | Values |
| 36 | `pivotTable` | Tables | Rows, Columns, Values |
| 37 | `actionButton` | Interactive | (none) |
| 38 | `bookmarkNavigator` | Interactive | (none) |
| 39 | `pageNavigator` | Interactive | (none) |
| 40 | `textbox` | Text | (none — uses paragraphs) |
| 41 | `shape` | Shapes | (none — uses shapeType) |
| 42 | `basicShape` | Shapes | (none — legacy shape) |
| 43 | `image` | Media | (none — uses imageUrl) |
| 44 | `scriptVisual` | Code | R visual |
| 45 | `pythonVisual` | Code | Python visual |
| 46 | `keyDriversVisual` | AI | Analyze, Explain By |
| 47 | `decompositionTreeVisual` | AI | Analyze, Explain By |
| 48 | `qnaVisual` | AI | (none) |
| 49 | `aiNarratives` | AI | Smart narrative |
| 50 | `scorecard` | Indicators | Scorecard/Metrics |
| 51 | `rdlVisual` | Reports | Paginated report visual |

---

### Report-Level Config

| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `publicCustomVisuals` | array | Custom visual IDs |
| `queryLimitOption` | `6` | Query limit option |
| `useEnhancedTooltips` | `true` | Enhanced tooltips |
| `exportDataMode` | `0`/`1` (PBIP) / `"AllowSummarized"` (PBIR) | Export data mode |
| `isPersistentUserStateDisabled` | boolean | Persistent user state |
| `useCrossReportDrillthrough` | boolean | Cross-report drillthrough |
| `allowInlineExploration` | boolean | Inline exploration |
| `disableFilterPaneSearch` | boolean | Filter pane search |
| `enableDeveloperMode` | boolean | Developer mode |
| `defaultFilterActionIsDataFilter` | boolean | Default filter action |
| `allowDataPointLassoSelect` | boolean | Lasso selection |
| `useDefaultAggregateDisplayName` | boolean | Default aggregate name |
| `hideVisualContainerHeader` | boolean | Global hide visual headers |
| `defaultDrillFilterOtherVisuals` | boolean | Cross-filter on drill |
| `allowChangeFilterTypes` | boolean | Allow filter type changes |
| `useStylableVisualContainerHeader` | boolean | Stylable visual header |
| `outspacePane.expanded` | boolean | Filter pane expanded |
| `outspacePane.visible` | boolean | Filter pane visible |
| `outspacePane.width` | `251L`/`303L` | Filter pane width |

#### slowDataSourceSettings (DirectQuery)
| Property | Default | หมายเหตุ |
|----------|---------|----------|
| `isCrossHighlightingDisabled` | `false` | Disable cross-highlighting |
| `isSlicerSelectionsButtonEnabled` | `false` | Slicer "Apply" button |
| `isFilterSelectionsButtonEnabled` | `false` | Filter "Apply" button |
| `isFieldWellButtonEnabled` | `false` | Field well "Apply" button |
| `isApplyAllButtonEnabled` | `false` | Apply all button |

---

### Page/Section Config

| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `displayName` | string | Page title |
| `displayOption` | `"FitToPage"`/`"FitToWidth"`/`"ActualSize"` | Display mode |
| `height` | `720` (default) | Page height |
| `width` | `1280` (default) | Page width |
| `visibility` | `0` (hidden) / `1` (visible) | Page visibility |
| `type` | `1` (tooltip) / `2` (drillthrough) | Page type |
| `ordinal` | number | Page display order |
| `section.background.color` | hex color | Page background color |
| `section.background.transparency` | `66D` | Background transparency |
| `outspacePane.width` | `"303L"` | Filter pane width per page |
| `theme` | filename string | Active theme filename |

#### Page Refresh
| Property | Type | Values |
|----------|------|--------|
| `duration` | string | Refresh interval (`"00:00:30"`) |
| `refreshType` | string | `APR` (Auto) / `CDM` (Change detection) |
| `show` | boolean | Enable page refresh |

#### Page Information
| Property | Type | หมายเหตุ |
|----------|------|----------|
| `pageInformationName` | string | Page name |
| `pageInformationAltName` | string | Alternate names (comma-separated) |
| `pageInformationQnaPodEnabled` | boolean | Enable Q&A |
| `pageInformationType` | boolean | Allow use as tooltip |

---

### Layout & Position

| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `x` | number (D) | Horizontal position |
| `y` | number (D) | Vertical position |
| `z` | number (D) | Z-index (layer order) |
| `width` | number (D) | Visual width |
| `height` | number (D) | Visual height |
| `tabOrder` | number (L) | Tab navigation order |
| `id` | `0` (desktop) / `1` (mobile) | Layout ID |

#### Dual Layouts (Desktop + Mobile)
```json
"layouts": [
  { "id": 0, "position": { "x": 256, "y": 80, "width": 224, "height": 111 } },
  { "id": 1, "position": { "x": 0, "y": 240, "width": 324, "height": 120 } }
]
```

---

### Projections (Complete)

| Role | Used By | Description |
|------|---------|-------------|
| `Category` | Bar/Column/Line/Pie/Donut/Funnel/Map | X-axis or category |
| `Y` | Bar/Column/Line/Pie/Gauge | Y-axis values |
| `Y2` | Combo charts | Secondary axis values |
| `Series` | Chart + Map | Legend grouping |
| `Values` | Card/Table/Slicer | Value fields |
| `Rows` | PivotTable | Matrix row fields |
| `Columns` | PivotTable | Matrix column fields |
| `Size` | Scatter/Map | Bubble/point size |
| `X` | Scatter | X-axis position |
| `Group` | Treemap | Category grouping |
| `Details` | Treemap | Detail drilldown |
| `Breakdown` | Waterfall | Breakdown category |
| `Indicator` | KPI | KPI main value |
| `TrendLine` | KPI | KPI trend line data |
| `Goal` | KPI | Target/goal value |
| `TargetValue` | Gauge | Target comparison value |
| `Tooltips` | AdvancedSlicer/Scatter | Tooltip extra fields |
| `Location` | FilledMap/ShapeMap | Geographic field |
| `Analyze` | KeyInfluencers/Decomposition | Analysis field |
| `Explain By` | KeyInfluencers/Decomposition | Explanation fields |
| `Data` | cardVisual | Modern card data |
| `SparklineData` | tableEx | Sparkline inline data (`{Measure, Groupings}`) |

#### Projection Expression Formats

```json
// Column reference
{ "Column": { "Expression": { "SourceRef": { "Source": "d" } }, "Property": "column_name" } }

// Measure reference
{ "Measure": { "Expression": { "SourceRef": { "Source": "d" } }, "Property": "measure_name" } }

// Aggregation
{ "Aggregation": { "Expression": { "Column": { ... } }, "Function": 0 } }

// Hierarchy level
{ "HierarchyLevel": { "Expression": { "Hierarchy": { ... } }, "Level": "Year" } }
```

#### Aggregation Function Codes
| Code | Function | Name Pattern |
|------|----------|-------------|
| `0` | Sum | `Sum(table.col)` |
| `1` | Average | `Average(table.col)` |
| `2` | Count | `Count(table.col)` |
| `3` | Min | `Min(table.col)` |
| `4` | Max | `Max(table.col)` |

---

### Query & Prototype

| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `queryState.Category` | object | Category field well |
| `queryState.Y` | object | Value field well |
| `queryState.Y2` | object | Secondary axis field well |
| `queryState.Series` | object | Series/legend field well |
| `queryState.Rows` | object | Matrix row field well |
| `queryState.Tooltips` | object | Tooltip field well |
| `queryState.Details` | object | Details field well (treemap) |
| `queryState.Group` | object | Group field well (treemap) |
| `queryState.Category.showAll` | boolean | Show all items (including empty) |
| `sortDefinition.sort[]` | array | Sort fields with direction |
| `sortDefinition.isDefaultSort` | boolean | Whether default sort |
| `orderBy` | array | Sort order with `Direction` (1=Asc, 2=Desc) |
| `queryOptions.allowBinnedLineSample` | boolean | Allow binned sampling |
| `showAllRoles` | array | Show data roles (e.g., `["Category"]`) |
| `drillFilterOtherVisuals` | boolean | Cross-filter when drilling |
| `activeProjections` | object | Active fields per data role |
| `projection.displayName` | string | Custom field display name |
| `PropertyVariationSource.Name` | string | Date hierarchy variation |
| `Hierarchy.Hierarchy` | string | Hierarchy name |

---

### Axis Properties

#### categoryAxis (19+ Properties)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `show` | boolean | Show/hide axis |
| `showAxisTitle` | boolean | Show axis title |
| `axisTitle` | string | Custom axis title |
| `fontSize` | `11D` | Font size |
| `fontFamily` | font string | Font family |
| `fontColor` | ThemeDataColor/hex | Font color |
| `showGridlines` | boolean | Show gridlines |
| `gridlineColor` | ThemeDataColor | Gridline color |
| `gridlineThickness` | `3L` | Gridline thickness |
| `gridlineStyle` | `'solid'`/`'dashed'`/`'dotted'` | Gridline style |
| `labelDisplayUnits` | number | Display units (K/M/B) |
| `preferredCategoryWidth` | `20D` | Preferred bar width |
| `innerPadding` | `0L` | Inner padding (combo chart) |
| `maxMarginFactor` | `50L` | Max margin % |
| `switchAxisPosition` | boolean | Switch axis position |
| `concatenateLabels` | boolean | Concatenate multi-level labels |
| `reverseStackOrder` | boolean | Reverse stack order |
| `treatNullsAsZero` | boolean | Null → 0 |
| `axisType` | `'Categorical'`/`'Scalar'` | Axis type |

#### valueAxis (21+ Properties)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `show` | boolean | Show/hide axis |
| `showAxisTitle` | boolean | Show axis title |
| `axisTitle` | string | Custom axis title |
| `fontSize` | number (D) | Font size |
| `fontFamily` | font string | Font family |
| `fontColor` | ThemeDataColor/hex | Font color |
| `start` | number/Measure | Axis start value |
| `end` | number/Measure | Axis end value |
| `labelDisplayUnits` | number | Display units |
| `labelPrecision` | number (L) | Decimal places |
| `showGridlines` | boolean | Show gridlines |
| `gridlineColor` | ThemeDataColor | Gridline color |
| `gridlineThickness` | `1L` | Gridline thickness |
| `gridlineStyle` | `'solid'`/`'dashed'`/`'dotted'` | Gridline style |
| `invertAxis` | boolean | Invert axis direction |
| `secShow` | boolean | Show secondary Y axis |
| `secStart` | Measure | Secondary axis start |
| `secEnd` | Measure | Secondary axis end |

#### y2Axis (Combo Charts)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `show` | boolean | Show/hide Y2 axis |
| `showAxisTitle` | boolean | Show Y2 axis title |
| `axisTitle` | string | Custom Y2 title |
| `fontSize` | number (D) | Font size |
| `fontColor` | ThemeDataColor | Font color |

---

### Legend Properties

| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `show` | boolean | Show/hide legend |
| `position` | `'Top'`/`'Bottom'`/`'Left'`/`'Right'`/`'TopCenter'` | Legend position |
| `fontSize` | number (D) | Font size |
| `fontFamily` | font string | Font family |
| `fontColor` | ThemeDataColor | Font color |
| `labelColor` | ThemeDataColor | Legend label color |
| `showGradientLegend` | boolean | Gradient legend for scatter/map |

---

### DataPoint Properties

| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `fill` | solid color / ThemeDataColor | Data point color |
| `fill` via Measure | Measure expression | Dynamic color from measure |
| `fill` per scopeId | ThemeDataColor per data point | Per-category colors |
| `target` | solid color | Gauge target indicator color |
| `transparency` | number | Data point transparency |

---

### LineStyles Properties

| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `lineStyle` | `'solid'`/`'dashed'`/`'dotted'` | Line style |
| `lineStyle` per metadata | varies | Per-series line style |
| `lineChartType` | `'linear'`/`'smooth'`/`'step'` | Line chart type |
| `showMarker` | boolean | Show markers on line |
| `markerShape` | `'circle'`/`'triangle'`/`'diamond'` | Marker shape |
| `markerColor` per metadata | ThemeDataColor | Marker color per series |
| `strokeWidth` | integer | Line stroke width |

---

### Labels Properties (33+ Properties)

| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `show` | boolean | Show/hide labels |
| `color` | ThemeDataColor/hex | Label text color |
| `fontSize` | number (D) | Font size |
| `fontFamily` | font string | Font family |
| `bold` | boolean | Bold text |
| `italic` | boolean | Italic text |
| `underline` | boolean | Underline text |
| `labelDisplayUnits` | `1000D` | Display units (K/M/B) |
| `labelPrecision` | number (L) | Decimal places |
| `labelPosition` | `'Auto'`/`'OutsideEnd'`/`'InsideEnd'`/`'InsideCenter'`/`'InsideBase'`/`'Under'` | Label position |
| `position` | `'preferOutside'` | Label position (donut) |
| `labelStyle` | `'Data'`/`'Data value, percent of total'`/`'Both'` | Label display style |
| `labelOverflow` | boolean | Allow label overflow |
| `labelMatchSeriesColor` | boolean | Label uses series color |
| `showSeries` | boolean per metadata | Show per-series labels |
| `leaderLines` | boolean | Connector lines from label |
| `minimumOffset` | `8D` | Minimum label offset |
| `preserveWhitespace` | boolean | Preserve whitespace (waffle text) |
| `enableBackground` | boolean | Label background |
| `showDynamicLabels` | boolean | Dynamic labels |
| `dynamicLabelValue` via Measure | Measure expression | Dynamic label from measure |

---

### Error Bars Properties (43+ Properties)

| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `show` | boolean | Show/hide error bars |
| `type` | `'ByPercentOfMeasure'`/`'ByField'` | Error bar type |
| `upperBoundPercentile` | `10L` | Upper bound % |
| `upperBound` via Measure | Measure expression | Upper bound dynamic |
| `lowerBound` via Measure | Measure expression | Lower bound dynamic |
| `barColor` | ThemeDataColor/Literal | Error bar color |
| `barWidth` | `1L`/`5L` | Error bar thickness |
| `barBorderSize` | `0L` | Error bar border size |
| `barBorderColor` | ThemeDataColor | Error bar border color |
| `barShow` | boolean | Show error bar stick |
| `barMatchSeriesColor` | boolean | Use series color |
| `tooltipShow` | boolean | Show error tooltip |
| `markerShape` | `'circle'`/`'triangle'`/`'diamond'`/`'none'`/`'longDash'` | Marker shape |
| **Shade Properties** | | |
| `shadeShow` | boolean | Show shade band |
| `shadeColor` | ThemeDataColor/Literal | Shade color |
| `shadeBandStyle` | `'fill'`/`'fillLine'` | Shade band style |
| `shadeMatchSeriesColor` | boolean | Shade uses series color |
| `shadeTransparency` | `66D`/`47D`/`75D` | Shade transparency |
| **Label Properties** | | |
| `labelShow` | boolean | Show error label |
| `labelFormat` | `'absolute'` | Label number format |
| `labelColor` | ThemeDataColor | Label text color |
| `labelFontSize` | `11D` | Label font size |
| `labelFontFamily` | font string | Label font family |
| `labelBold` | boolean | Label bold |
| `labelUnderline` | boolean | Label underline |
| `labelBackground` | boolean | Label background |
| `labelBackgroundColor` | ThemeDataColor | Label background color |
| `labelBackgroundTransparency` | `58L` | Label background transparency |

---

### Reference Lines

#### y1AxisReferenceLine (Y-axis)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `show` | boolean | Show reference line |
| `displayName` | string (`'Target'`) | Line display name |
| `value` via Measure | Measure expression | Dynamic reference value |
| `lineColor` | literal color | Line color |
| `transparency` | `0D` | Line transparency |
| `dataLabelShow` | boolean | Show data label |
| `dataLabelText` | `'Value'`/`'Name'`/`'ValueAndName'` | Label content |
| `dataLabelColor` | literal color | Label color |
| `dataLabelHorizontalPosition` | `'left'`/`'right'` | Label position |
| `dataLabelVerticalPosition` | `'above'`/`'under'` | Label V position |
| `dataLabelDecimalPoints` | number | Decimal places |
| `dataLabelDisplayUnits` | integer | Display units |
| `selector.id` | `'1'`, `'2'` etc. | Multiple lines per chart |

#### xAxisReferenceLine (X-axis, scatterChart)
Same properties as y1AxisReferenceLine but for scatter X-axis.

#### Reference Line Shading
| Property | Type | Values |
|----------|------|--------|
| `shadeShow` | boolean | Enable shading |
| `shadeRegion` | string | `before`/`after`/`none` |
| `shadeColor` | fill | Shade fill color |
| `shadeTransparency` | number | 0-100 |
| `shadeColorMatchStroke` | boolean | Match line color |

---

### Small Multiples Layout

| Property | Type | หมายเหตุ |
|----------|------|----------|
| `layoutType` | `'auto'`/`'custom'` | Layout mode |
| `columnCount` | integer | Columns count |
| `rowCount` | integer | Rows count |
| `gridPadding` | number | Overall grid padding |
| `advancedPaddingOptions` | boolean | Enable advanced padding |
| `columnPaddingInner/Outer` | number | Column padding |
| `rowPaddingInner/Outer` | number | Row padding |
| **Gridlines** | | |
| `gridLineShow` | boolean | Show/hide gridlines |
| `gridLineColor` | fill | Gridline color |
| `gridLineStyle` | `'solid'`/`'dashed'`/`'dotted'` | Gridline style |
| `gridLineWidth` | number | Line width |
| `gridLineTransparency` | number | Transparency |
| `gridLineType` | `'all'`/`'inner'`/`'innerHorizontal'`/`'innerVertical'` | Gridline type |
| **Subheader** | | |
| `subheader.show` | boolean | Show title |
| `subheader.alignment` | `'left'`/`'center'`/`'right'` | Alignment |
| `subheader.position` | `'top'`/`'bottom'` | Position |
| `subheader.fontColor` | fill / Measure | Title color |
| `subheader.fontFamily` | string | Font |
| `subheader.fontSize` | number (6-45) | Size |
| `subheader.bold/italic/underline` | boolean | Styling |
| `subheader.titleWrap` | boolean | Word wrap |

---

### Visual-Specific Properties

#### KPI Visual (`kpi`)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `indicator.fontFamily` | font string | Indicator font |
| `indicator.fontSize` | `48D` | Indicator size |
| `indicator.iconSize` | `18D` | Icon ▲/▼ size |
| `indicator.verticalAlignment` | `'middle'` | Vertical alignment |
| `indicator.indicatorDisplayUnits` | `1000D` | Display units (K) |
| `indicator.indicatorPrecision` | `0L` | Decimal places |
| `trendline.show` | boolean | Show/hide trendline |
| `trendline.transparency` | `28D` | Trendline transparency |
| `goals.goalText` | string | Goal description |
| `goals.goalFontColor` | ThemeDataColor | Goal font color |
| `goals.distanceLabel` | `'Percent'`/`'Δ'` | Distance format |
| `goals.distanceFontColor` | FillRule/conditional | Distance color conditional |
| `goals.labelPrecision` | `0L` | Goal decimal places |
| `status.goodColor` | hex color | Good status color |
| `status.badColor` | ThemeDataColor | Bad status color |
| `status.neutralColor` | ThemeDataColor | Neutral status color |
| `lastDate.show` | boolean | Show last date |

#### Gauge Visual (`gauge`)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `axis.max` | `1D` | Max value |
| `axis.min` | `0D` | Min value |
| `calloutValue.show` | boolean | Show callout |
| `calloutValue.fontFamily` | font string | Callout font |
| `calloutValue.color` | hex color | Callout color |
| `target.color` | ThemeDataColor | Target color |
| `target.fontFamily` | font string | Target font |
| `target.fontSize` | `10D` | Target font size |
| `target.labelPrecision` | `0L` | Target decimal places |
| `target.labelDisplayUnits` | `1D` | Target units (Auto) |

#### Table/Matrix (`tableEx`/`pivotTable`)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `values.fontFamily` | font string | Cell font |
| `values.fontSize` | `18D` | Cell font size |
| `values.bold` | boolean | Bold cells |
| `values.backColorPrimary` | ThemeDataColor | Odd row background |
| `values.backColorSecondary` | ThemeDataColor | Even row background |
| `values.fontColorPrimary` | ThemeDataColor | Odd row font color |
| `values.fontColorSecondary` | ThemeDataColor | Even row font color |
| `columnHeaders.backColor` | ThemeDataColor | Header background |
| `columnHeaders.fontColor` | ThemeDataColor | Header font color |
| `columnHeaders.autoSizeColumnWidth` | boolean | Auto-resize columns |
| `columnWidth.value` per metadata | number (D) | Per-column width |
| `columnFormatting.alignment` | `'Center'`/`'Right'` | Column alignment |
| `columnFormatting.fontColor` | ThemeDataColor | Column font color |
| `columnFormatting.labelDisplayUnits` | `1000D` | Column units |
| `columnFormatting.styleHeader` | boolean | Style header row |
| `columnProperties.[col].displayName` | string | Custom column name |
| `grid.rowPadding` | `8D`/`9D` | Row padding |
| `grid.gridHorizontal` | boolean | Show horizontal lines |
| `grid.gridHorizontalWeight` | `2D` | Horizontal line width |
| `grid.outlineColor` | ThemeDataColor | Grid outline color |
| `grid.textSize` | `15D` | Grid text size |
| `total.totals` | boolean | Show/hide totals row |
| `totals.fontSize` | `14D` | Totals font size |
| `totals.bold` | boolean | Totals bold |
| `totals.fontFamily` | font string | Totals font |
| `totals.showPositiveAndNegative` | boolean | Show +/- totals |

#### Sparklines (in `tableEx`)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `sparklines.strokeWidth` | `2L` | Line thickness |
| `sparklines.dataColor` | ThemeDataColor | Line color |
| `sparklines.markers` | `16D` | Marker display mode |
| `sparklines.markerSize` | `4L` | Marker size |
| `sparklines.markerShape` | `'circle'` | Marker shape |
| `sparklines.markerColor` | ThemeDataColor | Marker color |

#### Data Bars (Table/Matrix Conditional Formatting)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `dataBars.positiveColor` | solid color | Positive bar color |
| `dataBars.negativeColor` | solid color | Negative bar color |
| `dataBars.axisColor` | solid color | Axis line color |
| `dataBars.reverseDirection` | boolean | Reverse bar direction |
| `dataBars.hideText` | boolean | Hide value text |

#### Donut Chart (`donutChart`)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `slices.innerRadiusRatio` | `63L` | Donut hole ratio |
| `slices.startAngle` | `0L` | Start angle |

#### Scatter Chart (`scatterChart`)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `bubbles.bubbleSize` | `4L` | Bubble size |
| `bubbles.markerShape` | `'circle'`/`'triangle'`/`'none'` | Marker shape |
| `categoryLabels.show` | boolean | Show category labels |
| `categoryLabels.color` | ThemeDataColor | Label color |
| `categoryLabels.fontSize` | `8D` | Label size |
| `categoryLabels.fontFamily` | font string | Label font |
| `fillPoint.show` | boolean | Fill data points |

#### Card Visual (`cardVisual` — Modern)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `referenceLabel.value` | string | Reference label |
| `referenceLabelDetail.show` | boolean | Show detail label |
| `shadowCustom.show` | boolean | Custom shadow |

#### Advanced Slicer (`advancedSlicerVisual`)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `shapeCustomRectangle.tileShape` | string | Tile shape style |
| `shapeCustomRectangle.rectangleRoundedCurve` | number | Corner radius |
| `selection.strictSingleSelect` | boolean | Force single select |
| `layout.cellPadding` | number | Cell padding |
| `padding.paddingSelection` | number | Selection padding |
| `glowCustom.show` | boolean | Glow effect |
| `accentBar.show` | boolean | Accent bar |
| `header.show` | boolean | Header visibility |
| `data.mode` | `'Dropdown'`/`'Basic'` | Display mode |
| `general.orientation` | `"0D"` | Orientation |
| `selection.singleSelect` | boolean | Single selection mode |

#### Slicer (Legacy)
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `header.show` | boolean | Header visibility |
| `data.mode` | `'Dropdown'`/`'Basic'` | Display mode |

#### MultiRowCard
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `outlineWeight` | integer | Card outline thickness |
| `barShow` | boolean | Show colored bar |
| `barWeight` | integer | Bar thickness |
| `card.barColor` | color | Bar accent color |

---

### Color Systems

| System | Format | Example |
|--------|--------|---------|
| **ThemeDataColor** | `{ColorId, Percent}` | `{"ColorId": 3, "Percent": -0.25}` |
| **Literal hex** | `'#RRGGBB'` | `"'#4C5D8A'"` |
| **Solid color** | `{solid: {color: ...}}` | `{"solid": {"color": "#FF0000"}}` |
| **FillRule** | `{linearGradient2/3}` | Conditional gradient coloring |
| **Gradient** | `{gradient: {startColor, endColor}}` | Gradient fill |
| **Pattern** | `{pattern: {patternKind, color}}` | Pattern fill |
| **Semantic** | `"foreground"`, `"minColor"` | Reference theme semantic |
| **Conditional** | `{Conditional: {Cases: [...]}}` | Rule-based via expressions |

#### ThemeDataColor Percent
- `0` = base color
- Negative (e.g., `-0.25`) = darker shade
- Positive (e.g., `0.4`) = lighter shade

#### Color Format Pattern
```
^#[0-9a-fA-F]{8}$|^#(?:[0-9a-fA-F]{3}){1,2}$
// #AARRGGBB (8-digit), #RRGGBB (6-digit), #RGB (3-digit)
```

---

### Selector Types

| Selector | ใช้กับ | Example |
|----------|--------|---------|
| `scopeId` | Per-category color | `{data:[{scopeId:{...}}]}` |
| `metadata` | Per-series/column | `{metadata: "Sum(table.col)"}` |
| `dataViewWildcard` | All data points | `{matchingOption: 1}` |
| `id` | Button states | `{id: "default"/"hover"/"selected"}` |
| `data.roles` | Per-role styling | `{data:[{roles:['Category']}]}` |
| `highlightMatching` | Highlight mode | `{highlightMatching: 1}` |

---

### vcObjects Properties

#### Title
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `show` | boolean | Show/hide title |
| `text` | string / Measure | Title text (dynamic via measure) |
| `fontColor` | ThemeDataColor/hex | Font color |
| `fontSize` | number (D) | Font size |
| `fontFamily` | font string | Font family |
| `bold` | boolean | Bold |
| `italic` | boolean | Italic |
| `underline` | boolean | Underline |
| `alignment` | `'left'`/`'center'`/`'right'` | Text alignment |
| `titleWrap` | boolean | Word wrap |
| `background` | solid color / `null` | Title background |

#### SubTitle
| Property | Value/Type | หมายเหตุ |
|----------|-----------|----------|
| `show` | boolean | Show/hide subtitle |
| `text` | string / Measure | Subtitle text |
| `fontColor` | ThemeDataColor | Font color |
| `fontSize` | number (D) | Font size |
| `fontFamily` | font string | Font family |
| `bold` | boolean | Bold |
| `italic` | boolean | Italic |
| `underline` | boolean | Underline |

#### Other vcObjects
| Object | Key Properties |
|--------|---------------|
| `divider` | `show`, `color` (ThemeDataColor), `width` (`2D`) |
| `spacing` | `customizeSpacing`, `spacingBottom/Top` (D) |
| `padding` | `left`, `right`, `top`, `bottom` (D) |
| `background` | `show`, `color`, `transparency` |
| `border` | `show`, `color` |
| `visualHeader` | `show`, `foreground`, `background`, `border`, `transparency` |
| `visualTooltip` | `section` (page reference string) |
| `visualLink` | `show`, `type` (`'Bookmark'`/`'PageNavigation'`/`'WebUrl'`), `bookmark` |
| `general.altText` | string (accessibility) |
| `stylePreset.name` | `"None"` |

#### Visual Header Buttons
| Property | Type | หมายเหตุ |
|----------|------|----------|
| `showVisualInformationButton` | boolean | Info button |
| `showVisualWarningButton` | boolean | Warning button |
| `showVisualErrorButton` | boolean | Error button |
| `showDrillRoleSelector` | boolean | Drill role selector |
| `showDrillUpButton` | boolean | Drill up |
| `showDrillToggleButton` | boolean | Drill toggle |
| `showDrillDownLevelButton` | boolean | Drill down level |
| `showDrillDownExpandButton` | boolean | Drill expand |
| `showPinButton` | boolean | Pin to dashboard |
| `showFocusModeButton` | boolean | Focus mode |
| `showSeeDataLayoutToggleButton` | boolean | Data layout toggle |
| `showOptionsMenu` | boolean | Options menu (…) |
| `showPersonalizeVisualButton` | boolean | Personalize visual |

---

### Filter Properties

| Property | Values | หมายเหตุ |
|----------|--------|----------|
| `howCreated` | `0` (auto), `1`(user), `5` (drill) | Filter creation source |
| `isHiddenInViewMode` | boolean | Hide in view mode |
| `isLockedInViewMode` | boolean | Lock in view mode |
| `filterSortOrder` | `3` | Filter sort ordering |
| `filter.ordinal` | number | Filter display order |
| `requireSingleSelect` | boolean | Force single selection |
| `isInvertedSelectionMode` | boolean | Inverted filter mode |

#### Filter Types
| Type | คำอธิบาย |
|------|----------|
| `TopN` | Top N with subquery |
| `Advanced` | Advanced with `Contains` |
| `RelativeDate` | Relative date (PBIR) |

#### Filter Conditions
| Condition | คำอธิบาย |
|-----------|----------|
| `In` | In list of values |
| `Comparison` | `=`, `>`, `<`, `>=`, `<=` |
| `Between` | Between two bounds |
| `Contains` | Contains text |
| `And` | Left + Right combination |
| `Or` | Left + Right OR |
| `Not` | Logical negation |

#### ComparisonKind Values
| Code | Operator |
|------|----------|
| `0` | `=` (Equal) |
| `1` | `>` (Greater Than) |
| `2` | `>=` (Greater Than or Equal) |
| `3` | `<` (Less Than) |

#### Filter Pane Properties
| Property | Type | หมายเหตุ |
|----------|------|----------|
| `checkboxAndApplyColor` | fill | Checkbox & Apply color |
| `headerSize` | integer | Header text size |
| `searchTextSize` | integer | Search text size |
| `titleSize` | integer | Title text size |
| `inputBoxColor` | fill | Input field background |
| `textSize` | integer | Filter text size |
| `width` | integer | Pane width |

#### Filter Card (`$id`)
| `$id` | คำอธิบาย |
|--------|----------|
| `Available` | Available filter card styling |
| `Applied` | Applied filter card styling |

---

### Textbox & Paragraphs

```json
{
  "paragraphs": [{
    "horizontalTextAlignment": "center",
    "listType": "bullet",
    "textRuns": [{
      "value": "Hello World",
      "url": "https://example.com",
      "textStyle": {
        "fontFamily": "Segoe UI",
        "fontSize": "11pt",
        "fontStyle": "normal",
        "fontWeight": "bold",
        "color": "#000000",
        "textDecoration": "underline"
      }
    }]
  }]
}
```

---

### Shape Types (23 แบบ)

| Shape | Title | Shape-Specific Params |
|-------|-------|-----------------------|
| `rectangle` | Rectangle | — |
| `rectangleRounded` | Rounded rectangle | `rectangleRoundedCurve` |
| `oval` | Oval | — |
| `pill` | Pill | — |
| `arrow` | Arrow | `arrowStemWidth`, `arrowheadSize` |
| `arrowChevron` | Chevron | `chevronAngle` |
| `arrowPentagon` | Pentagon arrow | — |
| `heart` | Heart | — |
| `hexagon` | Hexagon | `hexagonSlant` |
| `line` | Line | `linecapType` (`flat`/`round`) |
| `octagon` | Octagon | `octagonSnipSize` |
| `parallelogram` | Parallelogram | `parallelogramSlant` |
| `pentagon` | Pentagon | — |
| `trapezoid` | Trapezoid | `trapezoidSlant` |
| `triangleIsoc` | Isosceles Triangle | `isocelesTriangleTipPosition` |
| `triangleRight` | Right Triangle | — |
| `tabCutCorner` | Snipped tab | `tabCutCornerSnipSizeTop/Right` |
| `tabCutTopCorners` | Snipped tab both | `tabCutCornerSnipSizeTop/Bottom` |
| `tabRoundCorner` | Rounded tab | `tabRoundCornerTop/Right` |
| `tabRoundTopCorners` | Rounded tab both | `tabRoundCornerTop/Bottom` |
| `speechbubbleRectangle` | Speech Bubble | `speechBubbleHeight/TailAngle/TailPosition` |

> `speechBubbleTailPosition` values: `bottomLeft`, `bottomRight`, `rightDown`, `rightUp`, `topRight`, `topLeft`, `leftUp`, `leftDown`

---

### Action Button States

Buttons support `default`, `hover`, `selected`, `disabled` states via `selector.id`:

| Card | Properties |
|------|-----------|
| `fill` | fillColor, show, transparency |
| `outline` | lineColor, show, transparency, weight |
| `glow` | color, shadowBlur, show, transparency |
| `shadow` | angle, color, shadowBlur, shadowDistance, shadowPositionPreset, show, transparency |
| `text` | bold, fontColor, fontFamily, fontSize, italic, underline, margins, alignment |
| `icon` | iconSize, image, placement, margins, lineColor, lineWeight, shapeType |

#### Icon/Shape Types for Buttons
`blank`, `leftArrow`, `rightArrow`, `back`, `reset`, `help`, `information`, `qna`, `bookmarks`, `applyAllSlicers`, `clearAllSlicers`, `custom`, `spinner`

#### Shadow Position Presets
`custom`, `top`, `topLeft`, `topRight`, `center`, `centerLeft`, `centerRight`, `bottom`, `bottomLeft`, `bottomRight`

---

### Theme Colors & Text Classes

#### Official Semantic Colors (from Theme Schema)
| Color Key | ใช้กับ |
|-----------|--------|
| `firstLevelElements` | Primary text/icons |
| `secondLevelElements` | Secondary text |
| `thirdLevelElements` | Tertiary/disabled |
| `fourthLevelElements` | Low-emphasis |
| `background` | Main background |
| `secondaryBackground` | Alt/secondary background |
| `tableAccent` | Table accent color |
| `hyperlink` | Link color |
| `headingColor` | Heading text |
| `cardForeground` | Card text |
| `cardBackground` | Card background |
| `good` | Good/positive status |
| `bad` | Bad/negative status |
| `neutral` | Neutral status |
| `maximum` | Diverging gradient max |
| `center` | Diverging gradient middle |
| `minimum` | Diverging gradient min |

#### Text Classes
| Class | Default Size | Weight |
|-------|-------------|--------|
| `title` | varies | bold |
| `header` | varies | bold |
| `label` | 10pt | normal |
| `callout` | varies | bold |
| `largeLightTitle` | large | light |
| `largeTitle` | large | normal |
| `smallLightTitle` | small | light |
| `body` | varies | normal |
| `annotation` | smallest | normal |

### Fill Types

| Type | JSON Key | ใช้กับ |
|------|----------|--------|
| `solid` | `{solid: {color: "#hex"}}` | Single color fill |
| `linearGradient2` | `{min, max, nullColoringStrategy}` | 2-point gradient |
| `linearGradient3` | `{min, mid, max}` | 3-point gradient |
| `pattern` | `{pattern: {patternKind, color, backColor}}` | Pattern fill |
| `image` | `{image: {url}}` | Image fill |

#### Pattern Kinds
`checkerboard`, `chevronDown`, `chevronUp`, `circles`, `crosshatch`, `diamonds`, `diagonalStripeBottomLeftToTopRight`, `diagonalStripeTopLeftToBottomRight`, `dottedDiamond`, `dottedGrid`, `grid`, `horizontalStripe`, `largeDiamond`, `lightDiamonds`, `lightGrid`, `lightHorizontalStripe`, `lightVerticalStripe`, `plaid`, `smallChecker`, `smallGrid`, `solidDiamond`, `sphere`, `thickDiagonalCross`, `trellis`, `verticalStripe`, `wave`, `weave`, `wideChecker`, `zigZag`

---

### PBIR vs PBIP Format

| Feature | PBIP (Legacy) | PBIR (Modern) |
|---------|--------------|---------------|
| Format | Single `report.json` with stringified objects | Decomposed multi-file structure |
| Visual Definition | Inline in `report.json` | Separate `visual.json` files per visual |
| Page Definition | Inline in `report.json` | Separate `page.json` files per page |
| Bookmark Storage | Inline array | Separate `*.bookmark.json` files |
| Color Values | `Literal.Value` in expressions | Direct string/object |
| Schema | No `$schema` field | Official `$schema` URL per file |
| String Encoding | `\"\"text\"\"` double-escaped | `"text"` standard JSON |
| Config Schema | `reportConfig` → Base64 | `report.json` v3.0.0 direct |
| Filter Format | `filters` as escaped JSON string | `filterConfig` structured |
| Numeric Suffix | Always (`10D`, `5L`) | Sometimes omitted (plain numbers) |
| `drillFilterOtherVisuals` | In objects config | Direct property on visual |
| `display.mode` | Not available | `"hidden"` to hide visual |

---

### PBIR Decomposed Files

```
📁 MyReport.Report/
├── item.metadata.json          ← {type: "report", displayName}
├── item.config.json            ← {logicalId: "guid"}
├── definition/
│   ├── report.json             ← Report-level config (v3.0.0)
│   ├── pages/
│   │   ├── ReportSection1/
│   │   │   ├── page.json       ← Page config
│   │   │   └── visuals/
│   │   │       ├── visual1/
│   │   │       │   └── visual.json  ← Visual definition
│   │   │       └── visual2/
│   │   │           └── visual.json
│   │   └── ReportSection2/
│   │       ├── page.json
│   │       └── visuals/...
│   ├── bookmarks/
│   │   ├── bookmarksMetadata.json  ← Bookmark ordering
│   │   ├── Bookmark1.bookmark.json ← Individual bookmarks
│   │   └── Bookmark2.bookmark.json
│   └── SharedResources/
│       ├── BaseThemes/*.json    ← Base themes
│       └── BuiltInThemes/*.json ← Custom themes
```

#### Official Schema URLs
| File | Schema Version |
|------|---------------|
| `report.json` | `report/3.0.0/schema.json` |
| `visual.json` | `visualContainer/2.2.0/schema.json` |
| `page.json` | `page/2.0.0/schema.json` |
| `bookmarksMetadata.json` | `bookmarksMetadata/1.0.0/schema.json` |
| `bookmark.json` | `bookmark/1.4.0/schema.json` |

---

### Bookmarks & Interactions

#### Bookmark Options
| Property | Type | หมายเหตุ |
|----------|------|----------|
| `applyOnlyToTargetVisuals` | boolean | Apply only to specific visuals |
| `targetVisualNames` | string[] | Target visual name list |
| `suppressActiveSection` | boolean | Don't change active page |
| `suppressData` | boolean | Don't change data state |

#### explorationState
| Property | Type | หมายเหตุ |
|----------|------|----------|
| `version` | `"1.3"` | Exploration state version |
| `activeSection` | string | Active section/page ID |
| `sections.{id}.filters` | object | Per-section filter states |
| `sections.{id}.visualContainers.{id}` | object | Per-visual state |
| `objects.merge.outspacePane` | object | Filter pane state |

#### Visual Interactions
| Type | `type` | Description |
|------|--------|-------------|
| Cross-filter | `0` | Filters other visuals |
| Cross-highlight | `1` | Highlights other visuals |
| None | `2` | No interaction |

---

### Advanced Filters

#### Report-Level filterConfig (PBIR)
```json
{
  "filterConfig": {
    "filters": [{
      "name": "Filter",
      "type": "RelativeDate",
      "filter": {
        "Where": [{ "Condition": { "Between": {
          "LowerBound": { "DateSpan": ... },
          "UpperBound": { "DateSpan": ... }
        }}}]
      },
      "howCreated": "User"
    }]
  }
}
```

#### DateSpan/DateAdd Time Units
| Code | Unit |
|------|------|
| `0` | Year |
| `1` | Quarter |
| `2` | Month |
| `3` | Day |

---

### Azure Maps

| Property | Type | หมายเหตุ |
|----------|------|----------|
| `layerType` | `'cluster'`/`'heatmap'`/`'reference'` | Map layer type |
| `clusterRadius` | `50D` | Cluster radius |
| `mapStyle` | `'grayscale'`/`'road'`/`'aerial'` | Map style |
| `autoZoom` | boolean | Auto zoom |
| `zoomLevel` | `13D` | Default zoom level |
| `showBubbleSize` | boolean | Show bubble size legend |
| `bubbleTransparency` | `0D` | Bubble transparency |
| `bubbleColor` | ThemeDataColor | Bubble color |
| `bubbleOutlineColor` | ThemeDataColor | Bubble outline |
| `bubbleOutlineWidth` | `1L` | Outline width |

#### FilledMap Properties
| Property | Type | หมายเหตุ |
|----------|------|----------|
| `mapStyles.mapTheme` | string | `"grayscale"`/`"aerial"`/`"road"` |
| `mapStyles.showLabels` | boolean | Show geographic labels |
| `categoryLabels.show` | boolean | Show category on map |

---

### Conditional Icons & Expressions

#### Conditional Icon Formatting
```json
{
  "Conditional": {
    "Cases": [{
      "Condition": { "Comparison": { "ComparisonKind": 0, ... }},
      "Value": { "Literal": { "Value": "'signal'" }}
    }],
    "DefaultValue": { "Literal": { "Value": "'trafficLight'" }}
  }
}
```

#### FillRule (Gradient Coloring)
```json
{
  "FillRule": {
    "Input": { "Measure": { ... } },
    "FillRule": {
      "linearGradient2": {
        "min": { "color": { "Literal": { "Value": "'#fae9a0'" }}},
        "max": { "color": { "Literal": { "Value": "'#4C5D8A'" }}},
        "nullColoringStrategy": { "strategy": { "Literal": { "Value": "'asZero'" }}}
      }
    }
  }
}
```

---

### Mobile/Pods Layout

| Property | Type | หมายเหตุ |
|----------|------|----------|
| `layout.id` | `1` | Mobile layout (vs `0` = desktop) |
| `filter.name` | `mobileReformatState` | Mobile-specific filter |
| `filter.objects.general.properties` | object | Mobile container properties |
| `filter.objects.general.properties.x/y/width/height` | D values | Mobile position/size |
| `pods` | array | Mobile visual pods (arrange order) |

---

### Dataset Schemas

#### `editorSettings.json`
| Property | Default | หมายเหตุ |
|----------|---------|----------|
| `showHiddenFields` | boolean | Show hidden fields |
| `autodetectRelationships` | boolean | Auto-detect relationships |
| `parallelQueryLoading` | boolean | Parallel M query loading |
| `typeDetectionEnabled` | boolean | Column type auto-detection |
| `relationshipImportEnabled` | boolean | Import relationships |
| `relationshipRefreshEnabled` | boolean | Update on refresh |
| `runBackgroundAnalysis` | boolean | Background data preview |

#### `unappliedChanges.json`
| Property | Type | หมายเหตุ |
|----------|------|----------|
| `queries[]` | QueryStorage[] | M queries not yet applied |
| `queryGroups[]` | array | Query group organization |
| `culture` | string | Culture (e.g., `"en-US"`) |
| `firewallEnabled` | boolean | Privacy level enforcement |

#### `diagramLayout.json`
| Property | Type | หมายเหตุ |
|----------|------|----------|
| `diagrams[].nodes[].location` | `{x, y}` | Table position in diagram |
| `diagrams[].nodes[].nodeIndex` | string | Table name reference |
| `diagrams[].zoomValue` | `100` | Diagram zoom level |
| `diagrams[].tablesLocked` | boolean | Lock table positions |

#### External Tool Registration (`.pbitool.json`)
| Property | Type | หมายเหตุ |
|----------|------|----------|
| `name` | string | Display name in PBI Desktop |
| `path` | string | Executable path (`%PATH%`) |
| `arguments` | string | CLI args (`%server%`, `%database%`) |
| `iconData` | string | Base64-encoded icon |

---

### Resource Packages

```json
{
  "resourcePackages": [{
    "name": "SharedResources",
    "type": "SharedResources",
    "items": [
      { "name": "CY20SU09", "path": "BaseThemes/CY20SU09.json", "type": "BaseTheme" },
      { "name": "MyTheme", "path": "BuiltInThemes/MyTheme.json", "type": "CustomTheme" },
      { "name": "logo.png", "path": "RegisteredResources/logo.png", "type": "Image" }
    ]
  }]
}
```

| Item Type | คำอธิบาย |
|-----------|----------|
| `BaseTheme` | Built-in base theme |
| `CustomTheme` | Custom theme file |
| `Image` | Registered image resource |
| `SharedResources` | Resource package type |
| `RegisteredResources` | Custom images/assets |

---

### Visual Group Container

```json
{
  "visualGroup": {
    "displayName": "Opportunity Cards",
    "groupMode": "ScaleMode"
  },
  "parentGroupName": "parentGroup"
}
```

| Property | Type | หมายเหตุ |
|----------|------|----------|
| `visualGroup` | object | Group container (แทน `visual`) |
| `displayName` | string | Group display name |
| `groupMode` | `"ScaleMode"` | Scale children together |
| `parentGroupName` | string | Parent group reference |

---

### Base Theme visualStyles

#### Wildcard Selector Pattern
```json
{
  "visualStyles": {
    "*": {
      "*": {
        "*": [{ "wordWrap": true }],
        "line": [{ "transparency": 0 }],
        "background": [{ "show": true, "transparency": 0 }],
        "categoryAxis": [{ "showAxisTitle": true, "gridlineStyle": "dotted" }],
        "title": [{ "titleWrap": true }]
      }
    },
    "scatterChart": {
      "*": {
        "bubbles": [{ "bubbleSize": -10 }],
        "fillPoint": [{ "show": true }]
      }
    }
  }
}
```

#### Visual Types with Per-Type Defaults
`scatterChart`, `lineChart`, `map`, `pieChart`, `donutChart`, `pivotTable`, `multiRowCard`, `kpi`, `slicer`, `waterfallChart`, `columnChart`, `clusteredColumnChart`, `hundredPercentStackedColumnChart`, `barChart`, `clusteredBarChart`, `hundredPercentStackedBarChart`, `areaChart`, `stackedAreaChart`, `lineClusteredColumnComboChart`, `lineStackedColumnComboChart`, `ribbonChart`, `group`, `basicShape`, `image`, `actionButton`, `textbox`, `page`

---

### AI Visuals

#### keyDriversVisual — Key Influencers (AI-powered)
| Object | Properties |
|--------|-----------|
| `keyDrivers` | `targetValue`, `selectedSort` (`'impact'`/`'count'`), `selectedAnalysis` (`'keyInfluencers'`/`'topSegments'`), `numericTargetSelectedKind`, `allowKeyDriversCounting`, `countType` (`'relative'`/`'absolute'`) |
| `keyInfluencersVisual` | `primaryColor`, `primaryFontColor`, `secondaryColor`, `secondaryFontColor`, `canvasColor` |
| `keyDriversDrillVisual` | `defaultColor`, `referenceLineColor` |
| Projections | `ExplainBy` (multiple columns), `Target` (column/measure to analyze) |

#### decompositionTreeVisual — Decomposition Tree (AI-powered)
| Object | Properties |
|--------|-----------|
| `tree` | `barsPerLevel`, `connectorDefaultColor`, `accentColor`, `connectorType` (`'curve'`/`'straight'`), `defaultClickAction` (`'select'`/`'expand'`), `density` (`'dense'`/`'normal'`/`'sparse'`) |
| `levelHeader` | `levelTitleFontFamily`, `levelTitleFontSize`, `levelTitleFontColor`, `showSubtitles`, `levelSubtitleFontSize`, `levelSubtitleFontColor`, `levelHeaderBackgroundColor` |
| `analysis` | `aiMode` (`'absolute'`/`'relative'`) |
| `insights` | `isAINode` (per data scope via `selector.data.scopeId`) |
| Projections | `Analyze` (measure), `ExplainBy` (dimensions, `active: true/false`) |

#### expansionStates (decompositionTree / slicer)
```jsonc
"expansionStates": [{
  "roles": ["ExplainBy"],
  "levels": [{
    "queryRefs": ["Country.Region"],
    "isCollapsed": true,
    "identityKeys": [{ "Column": { ... } }],
    "isPinned": true,
    "AIInformation": { "method": "MaxSplit", "disabled": false }
  }],
  "root": {
    "children": [{ "identityValues": [{ "Literal": { "Value": "'Europe'" } }], "isToggled": true }]
  }
}]
```

#### qnaVisual — Q&A Natural Language
| Object | Properties |
|--------|-----------|
| `hiddenProperties` | `savedUtterance` (saved question text) |
| `inputBox` | `questionFontSize`, `acceptedColor`, `errorColor`, `hoverColor`, `warningColor` |
| `suggestions` | `cardBackground`, `cardFontSize` |

#### FlowVisual — Power Automate Flow
| Object | Properties |
|--------|-----------|
| `flowInfo` | `FlowId`, `ManagementUri` |
| `buttonFill` | fill styling |
| `buttonText` | text styling |

---

### SparklineData — Sparkline ใน Table

#### SparklineData Projection
```jsonc
"Select": [{
  "SparklineData": {
    "Measure": { "Measure": { ... }, "Property": "Sum" },
    "Groupings": [{ "Column": { ..., "Property": "Month (MMM)" } }]
  },
  "Name": "SparklineData(1. Measures.Sum_[Date.Month (MMM)])",
  "NativeReferenceName": "Sum by Month (MMM)"
}]
```

#### sparklines Object — Styling
| Property | คำอธิบาย |
|----------|---------|
| `strokeWidth` | ความหนาเส้น (`2L`) |
| `dataColor` | สีเส้น sparkline |
| `markers` | marker visibility (bit field, `16D`) |
| `markerSize` | ขนาด marker (`4L`) |
| `markerShape` | รูปร่าง (`'circle'`, `'diamond'`) |
| `markerColor` | สี marker |
| selector | `{ "metadata": "SparklineData(...)" }` |

---

### Conditional Expression — IF/THEN/ELSE
```jsonc
"fill": { "solid": { "color": { "expr": {
  "Conditional": {
    "Cases": [
      { "Condition": { "Comparison": { "ComparisonKind": 3, "Left": { "Measure": ... }, "Right": { "Literal": { "Value": "0D" } } } },
        "Value": { "Literal": { "Value": "'#C8C2B5'" } } },
      { "Condition": { "Comparison": { "ComparisonKind": 2, ... } },
        "Value": { "Literal": { "Value": "'#658E95'" } } }
    ]
  }
}}}}
```

#### ComparisonKind — Complete Enum
| Value | Meaning |
|-------|---------|
| 0 | Equals (=) |
| 1 | LessThan (<) |
| 2 | GreaterThan (>) |
| 3 | GreaterThanOrEqual (>=) |
| 4 | LessThanOrEqual (<=) |
| 5 | NotEqual (≠) |

---

### Scatter Chart — bubbles, categoryLabels, xAxisReferenceLine

#### bubbles Object
| Property | คำอธิบาย |
|----------|---------|
| `bubbleSize` | ขนาด bubble (`1`-`10`) |
| `markerShape` | `'circle'`, `'triangle'`, `'diamond'`, `'square'`, `'pentagon'`, `'hexagon'`, `'none'` |

#### categoryLabels Object (scatter)
`show`, `color`, `fontSize`, `fontFamily`

#### xAxisReferenceLine
| Property | คำอธิบาย |
|----------|---------|
| `show`, `value`, `displayName` | พื้นฐาน |
| `lineColor`, `transparency`, `style` | สไตล์เส้น |
| `position` | `'front'`/`'back'` |
| `dataLabelShow/Color/Text` | label: `'Value'`/`'Name'`/`'ValueAndName'` |
| `dataLabelHorizontalPosition` | `'left'`/`'right'` |
| `dataLabelVerticalPosition` | `'above'`/`'under'` |
| selector | `{ "id": "1" }` (per reference line) |

---

### Line/Area Chart Extended

#### lineChartType Enum (Complete)
| Value | คำอธิบาย |
|-------|---------|
| `'linear'` | เส้นตรง (default) |
| `'smooth'` | เส้นโค้ง spline |
| `'step'` | ขั้นบันได stepped |

#### lineStyle Enum
`'solid'`, `'dotted'`, `'dashed'`

#### markerShape Enum (Complete)
`'circle'`, `'diamond'`, `'triangle'`, `'square'`, `'pentagon'`, `'hexagon'`, `'longDash'`, `'none'`

#### seriesLabels Object (NEW)
| Property | คำอธิบาย |
|----------|---------|
| `show` | แสดง/ซ่อน |
| `seriesPosition` | `'Left'`/`'Right'` — ตำแหน่ง label ข้างกราฟ |
| `seriesColor` | สี per-series (via `selector.data.scopeId`) |
| `seriesFontFamily` | font per-series |

#### subheader Object (Small Multiples Header)
| Property | คำอธิบาย |
|----------|---------|
| `fontFamily` | font |
| `fontColor` | สี — รองรับ Measure expression (conditional color!) |
| selector | `{ "data": [{ "roles": ["Rows"] }] }` (role-based) |

#### lineStyles Extended
| Property | คำอธิบาย |
|----------|---------|
| `strokeLineJoin` | `'bevel'`, `'round'`, `'miter'` |
| `areaShow` | แสดง area fill |
| `strokeWidth` `0L` | ซ่อนเส้น (area only / dumbbell) |
| Per-series selector | via `selector.metadata` หรือ `selector.data.scopeId` |

#### y2Axis — Secondary Y Axis
`show` (boolean) — ใช้กับ combo charts

---

### Gauge Extended

#### Gauge-Specific Objects
| Object | Properties |
|--------|-----------|
| `axis` | `max`, `min` — กำหนดช่วงแกน |
| `calloutValue` | `show`, `fontFamily`, `color` — ค่าแสดงกลาง gauge |
| `target` | `color`, `fontFamily`, `fontSize`, `labelPrecision`, `labelDisplayUnits` — target value styling |
| `dataPoint` (gauge) | `target` (solid color), `fill` (actual value color) |
| `status` | `goodColor`, `badColor`, `neutralColor` — gauge status |
| `goals` | `show`, `fontSize`, `distanceFontColor`, `goalFontColor`, `goalFontFamily`, `bold`, `distanceLabel`, `goalText`, `labelPrecision`, `titleBold` |
| Projection | `TargetValue` (gauge target role) |

---

### KPI Extended

| Object | Properties |
|--------|-----------|
| `indicator` | `fontColor`, `fontSize`, `horizontalAlignment`, `verticalAlignment`, `fontFamily`, `iconSize`, `indicatorDisplayUnits`, `indicatorPrecision` |
| `header` | `show`, `fontColor`, `fontFamily`, `textSize` |
| `value` | `show`, `fontColor` |
| `lastDate` | `show` — show last date |
| Projections | `Indicator`, `TrendLine`, `Target` |

---

### Error Bars Extended (Complete — 28 sub-properties)

#### Bar Configuration
| Property | คำอธิบาย |
|----------|---------|
| `barShow` | แสดง/ซ่อนแท่ง error bar |
| `barColor` | สีแท่ง |
| `barWidth` | ความกว้าง (`2L`-`8L`) |
| `barBorderColor` | สีขอบแท่ง |
| `barBorderSize` | ขนาดขอบ |
| `barMatchSeriesColor` | ใช้สีตาม series |

#### Shade/Band Configuration
| Property | คำอธิบาย |
|----------|---------|
| `shadeShow` | แสดง shading area |
| `shadeColor` | สี shade |
| `shadeTransparency` | ความโปร่งใส (0-100) |
| `shadeBandStyle` | `'fill'`, `'fillLine'` |
| `shadeMatchSeriesColor` | ใช้สีตาม series |

#### Label Configuration
| Property | คำอธิบาย |
|----------|---------|
| `labelShow/Color/FontFamily/FontSize` | พื้นฐาน |
| `labelFormat` | `'absolute'`/`'relative'` |
| `labelBold`, `labelUnderline` | styling |
| `labelBackground` | แสดง/ซ่อน background |
| `labelBackgroundColor`, `labelBackgroundTransparency` | สีพื้น label |
| `labelMatchSeriesColor` | ใช้สีตาม series |

#### Error Range (explicit bounds)
```jsonc
"errorRange": {
  "kind": "ErrorRange",
  "explicit": {
    "isRelative": false,
    "lowerBound": { "expr": { "Measure": { ... } } },
    "upperBound": { "expr": { "Measure": { ... } } }
  }
}
// Also supports: upperBoundColumn, lowerBoundColumn (Column-based)
```

#### Tooltip + Marker
`tooltipShow`, `markerShape` (`'longDash'`, `'none'`), `markerSize`

---

### Table/Matrix Extended (tableEx)

#### values — Alternating Row Colors (Zebra Striping)
| Property | คำอธิบาย |
|----------|---------|
| `backColorPrimary` / `backColorSecondary` | สีพื้น แถวคี่/คู่ |
| `fontColorPrimary` / `fontColorSecondary` | สีตัวอักษร แถวคี่/คู่ |
| `bandedRowHeaders`, `valuesOnRow`, `outlineStyle` | layout |

#### columnWidth — Per-Column Width
```jsonc
"columnWidth": [
  { "properties": { "value": { "...": "103.96D" } }, "selector": { "metadata": "Table.Dimension" } }
]
```

#### columnFormatting — Per-Column Format
| Property | คำอธิบาย |
|----------|---------|
| `alignment` | `'Center'`, `'Right'`, `'Left'` |
| `labelDisplayUnits` | display units ต่อ column |
| `fontColor` | สีต่อ column |
| `dataBars` | `positiveColor`, `negativeColor`, `axisColor`, `dataBarBackgroundColor`, `dataBarWidthPercent`, `reverseDirection`, `hideText` |

#### columnHeaders Extended
`backColor`, `fontColor`, `outlineStyle` (`'RowAndColumnHeaders'`)

#### grid Extended
`rowPadding`, `gridHorizontalWeight`, `outlineColor`, `outlineWeight`, `imageHeight`, `imageWidth`

#### total — Footer Totals
`totals` (show/hide), `backColor`, `fontColor`, `fontFamily`

#### PivotTable — rowHeaders Extended
| Property | คำอธิบาย |
|----------|---------|
| `showExpandCollapseButtons` | แสดงปุ่ม expand/collapse |
| `expandCollapseButtonsSize` | ขนาดปุ่ม |
| `expandCollapseButtonsColor` | สีปุ่ม |
| `steppedLayoutIndentation` | indent depth |
| `outlineStyle` | `'RowAndColumnHeaders'` |

#### PivotTable — subTotals + Totals
| Object | Properties |
|--------|-----------|
| `subTotals` | `columnSubtotals`, `rowSubtotals`, `perRowLevel` |
| `columnTotal` | `fontColor`, `fontFamily`, `fontSize` |
| `rowTotal` | `applyToHeaders`, `backColor`, `fontColor`, `fontFamily`, `fontSize` |

---

### Labels Extended (Complete)

#### labelPosition — Complete Enum
`'Auto'`, `'Inside'`, `'Outside'`, `'InsideBase'`, `'InsideEnd'`, `'InsideCenter'`, `'OutsideEnd'`, `'Under'`, `'Above'`

#### labels.labelStyle Enum
`'Data'`, `'Category'`, `'Percent'`, `'DataAndPercent'`, `'CategoryAndPercent'`

#### Dynamic Labels
| Property | คำอธิบาย |
|----------|---------|
| `showDynamicLabels` | เปิด/ปิด dynamic labels |
| `dynamicLabelValue` | ค่าจาก Measure อื่น |
| `leaderLines` | เส้นชี้จาก label |
| `enableBackground` | พื้นหลัง label |
| `labelDensity` | ความหนาแน่น label (`'100D'` = ทั้งหมด) |
| `minimumOffset` | offset ขั้นต่ำ (`'8D'`) |
| `labelOverflow` | จัดการ label ล้น |
| `showSeries` | แสดงชื่อ series |
| `showAll` | แสดง label ทั้งหมด |
| `preserveWhitespace` | รักษาช่องว่าง (text art) |
| `labelOrientation` | การหมุน label |
| `dataLabelFontColor` | สีตัวอักษร explicit |

---

### Axis Extended

#### categoryAxis Extended
| Property | คำอธิบาย |
|----------|---------|
| `axisType` | `'Categorical'` / `'Continuous'` |
| `preferredCategoryWidth` | ความกว้างหมวด (`20D`) |
| `innerPadding` | padding ด้านใน |
| `maxMarginFactor` | margin สูงสุด |
| `switchAxisPosition` | สลับตำแหน่งแกน |
| `concatenateLabels` | รวม labels hierarchical |
| `reverseStackOrder` | กลับลำดับ stack |
| `gridlineColor` | สี gridline |
| `gridlineStyle` | `'solid'`, `'dashed'` |
| `gridlineThickness` | ความหนา gridline |
| `treatNullsAsZero` | null = 0 |
| `start`, `end` | bounds (scatter/category) |
| `titleFontSize`, `titleFontFamily` | axis title styling |

#### valueAxis Extended
| Property | คำอธิบาย |
|----------|---------|
| `start`, `end` | manual axis range (supports Measure/Literal, negative) |
| `logAxisScale` | logarithmic scale |
| `invertAxis` | กลับทิศแกน |
| `alignZeros` | align zero on dual axis |
| `titleText`, `titleColor`, `titleFontFamily`, `titleFontSize` | title styling |
| `gridlineShow`, `gridlineStyle`, `gridlineThickness` | gridline |
| `secShow`, `secStart`, `secEnd`, `secFontSize`, `secShowAxisTitle` | secondary axis |

#### y1AxisReferenceLine Extended
| Property | คำอธิบาย |
|----------|---------|
| `value` | Literal หรือ Measure |
| `position` | `'front'`/`'back'` (z-order) |
| `dataLabelVerticalPosition` | `'above'`/`'under'` |
| Multiple lines | via `selector.id`: `'0'`, `'1'`, `'2'`, `'3'` |

---

### Totals Object
| Property | คำอธิบาย |
|----------|---------|
| `show` | แสดง/ซ่อน totals |
| `fontSize`, `fontFamily`, `bold`, `color` | styling |
| `showPositiveAndNegative` | แยกบวก/ลบ |
| Per-series selector | `{ "data": [{ "dataViewWildcard": { "matchingOption": 1 } }] }` |

---

### Slicer Extended

| Property/Object | คำอธิบาย |
|-----------------|---------|
| `data.mode` | `'Basic'` / `'Dropdown'` |
| `data.numericStart` | numeric range start |
| `selection.singleSelect` | จำกัดเลือกค่าเดียว |
| `selection.selectAllCheckboxEnabled` | checkbox เลือกทั้งหมด |
| `selection.strictSingleSelect` | บังคับเลือก 1 ค่า |
| `general.selfFilterEnabled` | slicer filter ตัวเอง |
| `items` | `background`, `fontColor` — slicer items styling |
| `slider` | `show`, `color` — numeric range slider |
| `numericInputStyle` | `background`, `fontColor` — slicer numeric input |
| `syncGroup` | `groupName`, `fieldChanges`, `filterChanges` — cross-page sync |

---

### Filters Extended

#### Filter Types (Complete)
| Type | คำอธิบาย |
|------|---------|
| `Categorical` | In/Contains values |
| `Advanced` | Comparison conditions |
| `TopN` | Top/Bottom N with Subquery |

#### Filter Metadata
| Property | คำอธิบาย |
|----------|---------|
| `isHiddenInViewMode` | ซ่อน filter ใน view mode |
| `isLockedInViewMode` | ล็อก filter |
| `howCreated` | `'User'` / `'Auto'` |
| `ordinal` | ลำดับ filter |
| `filterSortOrder` | ลำดับการ sort |
| `requireSingleSelect` | บังคับเลือกค่าเดียว |

#### Filter Conditions (Complete)
| Condition | คำอธิบาย |
|-----------|---------|
| `Comparison` | ComparisonKind 0-5 |
| `In` | Multi-value list |
| `Not` | Negation wrapper |
| `Between` | Range (if exists) |

#### TopN Filter with Subquery
```jsonc
"filter.Where.Condition.Not.Expression.In.Values": [[{
  "Subquery": {
    "Query": {
      "From": [{ "Name": "t", "Entity": "Table", "Type": 0 }],
      "Select": [{ "Column": { ... } }],
      "Top": 1,
      "OrderBy": [{ "Direction": 2 }]
    }
  }
}]]
```

#### Filter Annotations
```jsonc
"Annotations": {
  "filterExpressionMetadata": {
    "expressions": [{ "HierarchyLevel": { ... } }],
    "decomposedIdentities": { "values": [...], "columns": [...] },
    "valueMap": [{ "0": "FY2019" }]
  }
}
```

---

### Visual Structure Properties

| Property | คำอธิบาย |
|----------|---------|
| `drillFilterOtherVisuals` | cross-filter เมื่อ drill |
| `parentGroupName` | visual อยู่ใน group ไหน |
| `position.tabOrder` | ลำดับ tab navigation (accessibility, supports negative) |
| `isHidden` | visual ซ่อน |
| `sortDefinition.isDefaultSort` | default sort indicator |
| `lockAspect` | lock aspect ratio |
| `general.keepLayerOrder` | maintain z-order during interactions |
| `general.responsive` | responsive layout |
| `general.orientation` | horizontal/vertical |

#### visualGroup
| Property | คำอธิบาย |
|----------|---------|
| `displayName` | ชื่อ group |
| `groupMode` | `'ScaleMode'` / `'ShowAll'` |

---

### VCObjects Extended (Phase 2)

#### dropShadow — Full Custom Control
| Property | คำอธิบาย |
|----------|---------|
| `show` | แสดง/ซ่อน |
| `color` | สีเงา |
| `preset` | `'Custom'` / default presets |
| `position` | `'Inner'` / `'Outer'` |
| `shadowSpread` | spread radius |
| `shadowBlur` | blur radius |
| `shadowDistance` | offset distance |
| `angle` | shadow angle (degrees) |
| `transparency` | ความโปร่งใส |

#### padding Object
`top`, `bottom`, `left`, `right`, `paddingSelection` (preset)

#### spacing Object
| Property | คำอธิบาย |
|----------|---------|
| `customizeSpacing` | เปิดใช้ custom spacing |
| `verticalSpacing` | ระยะห่างแนวตั้ง |
| `spaceBelowTitleArea` | ระยะห่างใต้ title area |
| `spaceBelowSubTitle` | ระยะห่างใต้ subtitle |

#### divider Object
| Property | คำอธิบาย |
|----------|---------|
| `show`, `style` (`'solid'`), `width`, `color` | styling |
| `ignorePadding` | ไม่สนใจ padding |
| Supports `FillRule` for conditional color |

#### visualTooltip Extended
| Property | คำอธิบาย |
|----------|---------|
| `section` | ReportSection ID — link to tooltip page |
| `type` | `'Default'` |
| `titleFontColor`, `valueFontColor` | custom tooltip font colors |
| `background` | tooltip background |

#### visualHeaderTooltip
`show`, `text` — header tooltip

#### visualHeader Extended
| Property | คำอธิบาย |
|----------|---------|
| `show`, `background`, `border`, `transparency`, `foreground` | display |
| `showPersonalizeVisualButton` | personalize visual |
| `showVisualWarningButton` | warning icon |
| `showVisualErrorButton` | error icon |
| `showVisualInformationButton` | info icon |
| `showDrillRoleSelector` | drill selector |
| `showDrillUpButton` | drill up |
| `showDrillToggleButton` | drill toggle |
| `showDrillDownLevelButton` | drill down level |
| `showDrillDownExpandButton` | drill down expand |
| `showPinButton` | pin visual |
| `showFocusModeButton` | focus mode |
| `showSeeDataLayoutToggleButton` | see data toggle |
| `showOptionsMenu` | options menu |
| `showFilterRestatementButton` | filter restatement |
| `showTooltipButton` | tooltip button |

#### title Extended
`titleWrap`, `heading`, `background` (solid color/null), `alignment` (`'left'`/`'center'`/`'right'`), `italic`

#### border Extended
`radius` (rounded corners, px)

#### stylePreset
`name` (`'None'` / other presets)

---

### Legend Extended

| Property | คำอธิบาย |
|----------|---------|
| `position` | `'Top'`, `'Bottom'`, `'Left'`, `'Right'`, `'TopCenter'`, `'BottomCenter'`, `'LeftCenter'`, `'RightCenter'` |
| `showGradientLegend` | gradient legend |
| `showTitle` | show/hide legend title |
| `labelColor` | color |
| `legendMarkerRendering` | marker rendering mode |
| `matchLineColor` | match legend to line color |
| `fontFamily` | font family |

---

### Forecast & Anomaly Detection

#### anomalyDetection Object
```jsonc
"anomalyDetection": [{
  "properties": {
    "show": true,
    "transform": {
      "algorithm": "SampleAndDetectAnomaly",
      "parameters": [
        { "Name": "Sensitivity", "Value": "0.73D" },
        { "Name": "SampleSizePerSeries", "Value": "3500L" }
      ]
    },
    "explainBy": { "exprs": [{ "expr": { "Column": { ... } } }], "kind": "ExprList" },
    "displayName": "'Find anomalies 1'",
    "markerShapeSize": "7D",
    "transparency": "64D"
  },
  "selector": { "metadata": "Measure.Name", "id": "1" }
}]
```

#### trend / trendline Object
| Property | คำอธิบาย |
|----------|---------|
| `trend.show` | แสดง trend line |
| `trend.displayName` | ชื่อเส้น trend |
| `trendline.show` | alternative trend object |
| `trendline.transparency` | ความโปร่งใส |

#### forecast Object
| Property | คำอธิบาย |
|----------|---------|
| `show` | แสดง forecast |
| `displayName` | ชื่อ forecast |
| `transform` | ML algorithm parameters |

---

### Donut/Pie Extended

#### slices Object
| Property | คำอธิบาย |
|----------|---------|
| `innerRadiusRatio` | ขนาดรูตรงกลาง (0=pie, 100=thin ring, 63=default donut) |
| `startAngle` | มุมเริ่มต้น (degrees) |

---

### Textbox Extended

#### textRuns Properties
| Property | คำอธิบาย |
|----------|---------|
| `url` | hyperlink in textRun |
| `textStyle.color` | สีตัวอักษร |
| `textStyle.fontWeight` | `'bold'` |
| `textStyle.fontStyle` | `'italic'` / `'normal'` |
| `textStyle.fontFamily` | `'inherit'` = use theme font |
| `textStyle.fontSize` | e.g. `'20pt'` |

#### paragraphs Properties
| Property | คำอธิบาย |
|----------|---------|
| `horizontalTextAlignment` | `'center'` / `'left'` / `'right'` |

#### Dynamic Value (propertyIdentifier)
```jsonc
"textRuns": [{
  "value": {
    "propertyIdentifier": { "objectName": "values", "propertyName": "expr" },
    "selector": { "id": "Value" }
  }
}]
```

---

### Button States Extended

#### actionButton — visualLink Types (Complete)
`'Back'`, `'Bookmark'`, `'Qna'`, `'WebUrl'`, `'PageNavigation'`, `'Drillthrough'`

#### Bookmark Navigation
```jsonc
"visualLink": [{
  "show": true,
  "type": "'Bookmark'",
  "bookmark": "'BookmarkId'"
}]
```

#### fill/text/icon States
| State (selector.id) | คำอธิบาย |
|---------------------|---------|
| `'default'` | สถานะปกติ |
| `'hover'` | เมาส์ชี้ |
| `'selected'` | ถูกเลือก |
| `'pressed'` | กดค้าง |
| `'disabled'` | ปิดใช้งาน |

#### icon Extended
| Property | คำอธิบาย |
|----------|---------|
| `shapeType` | `'back'`, `'rightArrow'`, `'arrowbutton'` |
| `lineWeight` | stroke weight |
| `topMargin/bottomMargin/leftMargin/rightMargin` | margins |
| `horizontalAlignment` | `'center'` |

---

### Shape Visual (shape vs basicShape)

#### shape Visual
| Object | Properties |
|--------|-----------|
| `shape` | `tileShape` (`'rectangle'` / etc), `map`, `projectionEnum` |
| `rotation` | `shapeAngle` |
| `outline` | `show` |

#### basicShape Extended
| Property | คำอธิบาย |
|----------|---------|
| `rotation.angle` | rotation angle |
| `line.roundEdge` | rounded corners |
| `line.transparency` | line transparency |
| `shapeType` | `'arrowbutton'` (new) |

---

### Map Extended

#### mapControls Object (NEW)
| Property | คำอธิบาย |
|----------|---------|
| `autoZoom` | auto-fit map to data |
| `centerLatitude`, `centerLongitude` | map center |
| `zoomLevel` | initial zoom level |
| `showLassoButton` | lasso selection tool |
| `showZoomButtons` | zoom +/- buttons |
| `showNavigationControls` | nav controls |
| `showSelectionControl` | selection tool |
| `showStylePicker` | style picker |
| `defaultStyle` | default map style |
| `autoZoomIncludesReferenceLayer` | include ref layer in zoom |

#### mapStyles Object
| Property | คำอธิบาย |
|----------|---------|
| `mapTheme` | `'grayscale'`, `'aerial'`, `'road'`, `'dark'` |
| `showLabels` | show location labels |

#### shapeMap — Custom Geography
`shape.map.geoJson` — custom GeoJSON data, `shape.projectionEnum` — map projection type

---

### Vega/Deneb Custom Visual (PBIP format)

| Property | คำอธิบาย |
|----------|---------|
| `jsonSpec` | Vega-Lite JSON specification |
| `jsonConfig` | Vega configuration overrides |
| `provider` | `'vegaLite'` / `'vega'` |
| `version` | Vega version |
| `enableTooltips`, `enableContextMenu` | interactivity |
| `enableHighlight`, `enableSelection` | cross-visual |
| `selectionMaxDataPoints` | max selectable points |

---

### Projection Roles — Complete Registry

| Role | ใช้กับ |
|------|--------|
| `Category` | Charts (X-axis) |
| `Y` | Values (measure) |
| `Y2` | Secondary Y-axis (combo charts) |
| `X` | X values (scatter) |
| `Series` | Split/stack by |
| `Size` | Bubble size (scatter) |
| `Values` | Card/table values |
| `Gradient` | Color gradient |
| `Tooltips` | Tooltip values |
| `Rows` | Small Multiples (splits into panels) |
| `TargetValue` | Gauge target |
| `ExplainBy` | AI analysis dimensions |
| `Analyze` | AI analysis target |
| `Target` | KPI target |
| `Indicator` | KPI indicator |
| `TrendLine` | KPI trend data |
| `Play` | Play axis (animation) |
| `Details` | Treemap details |
| `Group` | Treemap grouping |
| `ReferenceLabels` | Reference labels |
| `table` | Table binding |
| `Data` | Generic (custom visuals) |
| `Goal` | KPI goal |

---

### Selector Extended

#### selector.data — Role-Based (NEW)
```jsonc
// Role-based selector (Small Multiples headers)
{ "data": [{ "roles": ["Rows"] }] }
{ "data": [{ "roles": ["Rows", "Category"] }] }   // Multi-role
```

#### Combined Selector
```jsonc
{ "data": [{ "dataViewWildcard": { "matchingOption": 0 } }],
  "metadata": "1. Measures.Sum",
  "highlightMatching": 1 }
```

#### dataViewWildcard.matchingOption
| Value | คำอธิบาย |
|-------|---------|
| 0 | MatchAll — apply to all instances |
| 1 | MatchAny — per-series/per-instance |

---

### Query Extended

#### queryOptions
| Property | คำอธิบาย |
|----------|---------|
| `keepProjectionOrder` | คงลำดับ projection |
| `allowBinnedLineSample` | binned line sampling |

#### showAllRoles
`["Category"]` — แสดงทุก role ใน category

#### Aggregation Function Enum
| Value | Function |
|-------|---------|
| 0 | Sum |
| 1 | Avg |
| 3 | Min |
| 4 | Max |
| 5 | CountNonNull |

---

### Expression Types — Complete Registry

| Type | คำอธิบาย |
|------|---------|
| `Literal` | ค่าคงที่ (`'text'`, `0D`, `1L`, `true`) |
| `ThemeDataColor` | สีจาก theme (`ColorId`, `Percent` -0.5 to 0.6) |
| `Measure` | ค่าจาก DAX measure |
| `Column` | ค่าจาก column |
| `SolidColorPropertyExpression` | สีคงที่ |
| `Conditional` | IF/THEN/ELSE (`Cases[]`, `Comparison`, `ComparisonKind`) |
| `FillRule` | Gradient (`linearGradient2`) |
| `SparklineData` | Sparkline (`Measure`, `Groupings`) |
| `ResourcePackageItem` | รูปจาก package (`PackageName`, `ItemName`) |
| `HierarchyLevel` | Hierarchy expression |
| `Arithmetic` | Math (`Left`, `Right`, `Operator`) |
| `ScopedEval` | Scoped evaluation |
| `PropertyVariationSource` | Property variation |
| `Aggregation` | Aggregation function |
| `Subquery` | Embedded DAX query |

---

### PBIR File Types — Complete Registry

| File | คำอธิบาย |
|------|---------|
| `visual.json` | Visual definition (per visual) |
| `report.json` | Report/layout config (PBIR) หรือ embedded visuals (PBIP) |
| `page.json` | Page definition (height, width, displayOption, type, visibility) |
| `bookmark.json` | Bookmark state (explorationState, filters, visual display) |
| `bookmarks.json` | Bookmarks metadata (ordered list) |
| `pages.json` | Pages metadata (pageOrder, activePageName) |
| `version.json` | Report format version |
| `theme.json` | Theme (dataColors, tableAccent, maximum/center/minimum) |
| `diagramLayout.json` | Data model diagram layout |
| `definition.pbir` | Dataset binding (byPath / byConnection) |
| `item.config.json` | Fabric item identity (logicalId) |
| `item.metadata.json` | Item display info (type, displayName) |
| `.pbip` | Project shortcut (artifacts, settings) |
| `localSettings.json` | Per-user settings (reportId, securityBindingsSignature) |

#### page.json Properties
| Property | คำอธิบาย |
|----------|---------|
| `name` | page internal name |
| `displayName` | page display name |
| `displayOption` | `'FitToPage'`/`'FitToWidth'`/`'ActualSize'` |
| `height`, `width` | dimensions (px) |
| `type` | 0=normal, 1=tooltip, 2=drillthrough |
| `visibility` | 0=visible, 1=hidden |
| `objects` | `background`, `displayArea`, `outspace`, `outspacePane` |
| `filterConfig` | page-level filters + `filterSortOrder` |
| `pageBinding` | drillthrough config (`name`, `type`, `parameters`, `acceptsFilterContext`) |
| `visualInteractions` | cross-visual interaction rules |

#### bookmark.json Properties
| Property | คำอธิบาย |
|----------|---------|
| `options.applyOnlyToTargetVisuals` | apply to subset |
| `options.targetVisualNames` | list of target visuals |
| `explorationState.activeSection` | active page |
| `explorationState.sections.*.filters` | page-level filters |
| `explorationState.sections.*.visualContainers` | per-visual state |
| `display.mode` | `'hidden'`/`'visible'` — visual visibility |

---

### Visual Types — Complete Registry (44 unique)

```
Standard Charts:  barChart, columnChart, clusteredBarChart, clusteredColumnChart,
                  hundredPercentStackedBarChart, lineChart, areaChart, stackedAreaChart,
                  ribbonChart, waterfallChart, lineClusteredColumnComboChart,
                  lineStackedColumnComboChart, pieChart, donutChart, funnel, scatterChart, treemap

Tables/Matrix:    tableEx, pivotTable, multiRowCard

KPI/Cards:        card, cardVisual, kpi, gauge

Maps:             map, filledMap, shapeMap, azureMap

Shapes/Text:      shape, basicShape, textbox, image

Interactive:      slicer, advancedSlicerVisual, actionButton

AI/Analytics:     decompositionTreeVisual, keyDriversVisual, qnaVisual

Custom Visuals:   deneb..., Aquarium..., FlowVisual_..., FilterByList..., BarChartF5983...

Grouping:         visualGroup (placeholder)
```

---

### Additional Objects (from PBIP/R70)

| Object | คำอธิบาย |
|--------|---------|
| `dataBars` | Conditional data bars (`positiveBarColor`, `negativeBarColor`, `dataBarBackgroundColor`, `dataBarWidthPercent`) |
| `plotArea` | Chart plot area (`transparency`) |
| `percentBarLabel` | Funnel/gauge % labels (`show`, `color`, `fontFamily`, `fontSize`) |
| `wordWrap` | Text wrapping (`show`) |
| `zoom` | Map/chart zoom control (`show`) |
| `shadowCustom` | Custom shadow (`show`, `color`, `position`, `shadowPositionPreset`) |
| `shapeCustomRectangle` | Rectangle customization (`tileShape`, `rectangleRoundedCurve`, `rectangleRoundedCurveCustomStyle`) |
| `overFlow` | Overflow control (`overFlowDirection`, `overFlowStyle`) |
| `layout` | Grid layout (`alignment`, `cellPadding`, `columnCount`, `rowCount`, `orientation`) |
| `imageScaling` | Image scale (`imageScalingType`) |
| `fillCustom`, `glowCustom` | Visual effects (`show`) |
| `referenceLabel`, `referenceLabelDetail` | Reference labels |

---

### Format Versions — Complete

| Format | Versions |
|--------|---------|
| PBIR Schema | 2.1.0, 2.2.0 |
| PBIP Legacy | config version 5.44, 5.46 |
| Theme | version varies |
| definition.pbir | 1.0 |
| page.json | various |
| bookmark.json | schema 1.4.0 |

---

> 📝 **จบ PBIR Complete Property Reference** — Consolidated จาก 228+ sections, R1-R72 audit rounds, 1,373+ files scanned, ~3,800+ properties

---

## 📦 Semantic Model (model.bim) Reference

> โครงสร้าง model.bim — Tabular Model Definition Language (TMDL)

### model.bim Root Structure
```jsonc
{
  "name": "ProjectName",
  "compatibilityLevel": 1567,  // Power BI Desktop = 1567+
  "model": {
    "culture": "en-US",         // or "th-TH"
    "defaultPowerBIDataSourceVersion": "powerBI_V3",
    "tables": [],
    "relationships": [],
    "roles": [],                // RLS
    "perspectives": [],
    "cultures": [],
    "annotations": []
  }
}
```

### Table Definition
| Property | คำอธิบาย | ตัวอย่าง |
|----------|---------|---------|
| `name` | ชื่อ table | `"Sales"` |
| `columns[]` | รายการ columns | ดูด้านล่าง |
| `partitions[]` | data source (M expression) | ดูด้านล่าง |
| `measures[]` | DAX measures | ดูด้านล่าง |
| `hierarchies[]` | drill-down hierarchies | `[{name, levels:[]}]` |
| `isHidden` | ซ่อน table | `true` |
| `annotations[]` | metadata | `[{name, value}]` |

### Column Types
| `dataType` | Power BI Type | JSON Value |
|-----------|--------------|------------|
| `string` | Text | `"string"` |
| `int64` | Whole Number | `"int64"` |
| `double` | Decimal | `"double"` |
| `dateTime` | Date/DateTime | `"dateTime"` |
| `boolean` | True/False | `"boolean"` |
| `decimal` | Fixed Decimal | `"decimal"` |
| `binary` | Binary | `"binary"` |

### Column Properties
```jsonc
{
  "name": "ProductName",
  "dataType": "string",
  "sourceColumn": "ProductName",      // maps to source
  "displayFolder": "Dimensions",      // folder grouping
  "isHidden": false,
  "sortByColumn": "ProductNameSort",  // sort by another column
  "summarizeBy": "none",              // none/sum/average/min/max/count
  "dataCategory": "City",             // geo category for maps
  "formatString": "#,##0.00",
  "annotations": [{ "name": "SummarizationSetBy", "value": "Automatic" }]
}
```

### Measure Definition
```jsonc
{
  "name": "Total Revenue",
  "expression": "SUM('Sales'[Amount])",
  "formatString": "#,##0",
  "displayFolder": "KPIs",
  "description": "Sum of all sales amounts",
  "isHidden": false,
  "annotations": [],
  "kpi": {                            // KPI object (optional)
    "targetExpression": "1000000",
    "statusExpression": "IF([Total Revenue]>[Target], 1, -1)",
    "statusGraphic": "Three Circles Colored"
  }
}
```

### Partition (M Expression)
```jsonc
{
  "name": "Sales",
  "mode": "import",                   // import / directQuery / dual
  "source": {
    "type": "m",
    "expression": [
      "let",
      "  Source = Csv.Document(File.Contents(\"data.csv\"), [Delimiter=\",\", Encoding=65001]),",
      "  Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
      "  Types = Table.TransformColumnTypes(Headers, {{\"Date\", type date}, {\"Amount\", type number}})",
      "in",
      "  Types"
    ]
  }
}
```

### Relationships
```jsonc
{
  "name": "Sales_Products",
  "fromTable": "Sales",
  "fromColumn": "ProductID",
  "toTable": "Products",
  "toColumn": "ProductID",
  "fromCardinality": "many",         // many / one
  "toCardinality": "one",
  "crossFilteringBehavior": 1,       // 1=single, 2=both
  "securityFilteringBehavior": 1,    // 1=oneDirection, 2=bothDirections
  "isActive": true
}
```

### Row-Level Security (RLS)
```jsonc
{
  "roles": [{
    "name": "RegionalManager",
    "modelPermission": "read",
    "tablePermissions": [{
      "name": "Sales",
      "filterExpression": "'Sales'[Region] = USERPRINCIPALNAME()"
    }]
  }]
}
```

### Hierarchy
```jsonc
{
  "name": "Geography",
  "levels": [
    { "name": "Country", "ordinal": 0, "column": "Country" },
    { "name": "State", "ordinal": 1, "column": "State" },
    { "name": "City", "ordinal": 2, "column": "City" }
  ]
}
```

---

## 🔄 CI/CD & Git Integration

### Git Workflow for PBIP

#### .gitignore (แนะนำ)
```gitignore
# User-specific settings
**/localSettings.json
**/.pbi/

# Cache
**/*.pbicache
**/cache.abf

# Backup
*.bak
*.tmp

# OS
.DS_Store
Thumbs.db
desktop.ini
```

#### Branching Strategy
| Branch | Purpose |
|--------|---------|
| `main` | Production reports |
| `develop` | Integration branch |
| `feature/*` | New visuals/pages |
| `hotfix/*` | Urgent fixes |

#### Merge Strategy
- **report.json** → ⚠️ JSON merge conflicts สูง → ใช้ visual-level PBIR format แทน
- **model.bim** → merge ระวัง column order
- **definition.pbir** / `.platform` → มักไม่เปลี่ยน

### Azure DevOps Pipeline
```yaml
# azure-pipelines.yml
trigger:
  branches: [main, develop]

pool:
  vmImage: 'windows-latest'

steps:
- task: PowerShell@2
  displayName: 'Validate PBIP Structure'
  inputs:
    targetType: inline
    script: |
      $errors = @()
      # Check required files
      if (-not (Test-Path "*.pbip")) { $errors += "Missing .pbip" }
      $reportDir = Get-ChildItem -Filter "*.Report" -Directory
      if (-not $reportDir) { $errors += "Missing .Report folder" }
      else {
        if (-not (Test-Path "$($reportDir.Name)/report.json")) { $errors += "Missing report.json" }
        if (-not (Test-Path "$($reportDir.Name)/definition.pbir")) { $errors += "Missing definition.pbir" }
      }
      $modelDir = Get-ChildItem -Filter "*.SemanticModel" -Directory
      if (-not $modelDir) { $errors += "Missing .SemanticModel folder" }
      else {
        if (-not (Test-Path "$($modelDir.Name)/model.bim")) { $errors += "Missing model.bim" }
        # Validate JSON
        $bim = Get-Content "$($modelDir.Name)/model.bim" -Raw | ConvertFrom-Json
        if (-not $bim.model.tables) { $errors += "model.bim has no tables" }
      }
      if ($errors.Count -gt 0) { $errors | ForEach-Object { Write-Error $_ }; exit 1 }
      Write-Host "✅ Validation passed"

- task: PowerShell@2
  displayName: 'Deploy to Fabric Workspace'
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
  inputs:
    targetType: inline
    script: |
      # Deploy via Power BI REST API
      $token = (Get-AzAccessToken -ResourceUrl "https://analysis.windows.net/powerbi/api").Token
      $headers = @{ Authorization = "Bearer $token" }
      # Import PBIP to workspace
      Invoke-RestMethod -Uri "https://api.powerbi.com/v1.0/myorg/groups/{workspaceId}/imports" `
        -Method Post -Headers $headers -ContentType "application/json" `
        -Body (@{ fileUrl = $env:ARTIFACT_URL } | ConvertTo-Json)
```

### Fabric Git Integration
| Feature | คำอธิบาย |
|---------|---------|
| Workspace → Git | Connect workspace to Azure DevOps or GitHub repo |
| Auto-sync | Changes in workspace auto-commit |
| Branch switching | Switch workspace between branches |
| Conflict resolution | UI-based merge conflict resolver |

---

## 🎨 Custom Visual Integration

### pbiviz Format
| File | คำอธิบาย |
|------|---------|
| `pbiviz.json` | Visual metadata (name, version, author) |
| `capabilities.json` | Data roles, objects, data view mappings |
| `src/visual.ts` | Main visual TypeScript code |
| `style/visual.less` | Styling (LESS/CSS) |
| `assets/icon.png` | Visual icon (20×20 px) |

### capabilities.json Structure
```jsonc
{
  "dataRoles": [
    { "name": "category", "kind": "Grouping", "displayName": "Category" },
    { "name": "measure", "kind": "Measure", "displayName": "Values" }
  ],
  "dataViewMappings": [{
    "categorical": {
      "categories": { "for": { "in": "category" } },
      "values": { "select": [{ "bind": { "to": "measure" } }] }
    }
  }],
  "objects": {
    "dataColors": {
      "displayName": "Data Colors",
      "properties": {
        "fill": { "type": { "fill": { "solid": { "color": true } } } }
      }
    }
  }
}
```

### PBIP Integration — Custom Visual Reference
```jsonc
// In visual.json — referencing a custom visual
{
  "singleVisual": {
    "visualType": "deneb9A2B4B3E7CCA4547B538B76B0EDAA09E",  // GUID-based
    // or AppSource visual:
    "visualType": "Aquarium1695746498133",
    "projections": { ... },
    "objects": {
      "vega": [{
        "properties": {
          "jsonSpec": "{ ... Vega-Lite spec ... }",
          "provider": "'vegaLite'",
          "isNewDialogOpen": "false"
        }
      }]
    }
  }
}
```

### Deneb (Vega-Lite) Integration
| Property | คำอธิบาย |
|----------|---------|
| `vega.jsonSpec` | Full Vega-Lite JSON specification |
| `vega.provider` | `'vega'` หรือ `'vegaLite'` |
| `vega.isNewDialogOpen` | Open editor on load |
| `vega.renderMode` | `'canvas'` / `'svg'` |

### Charticulator Integration
| Property | คำอธิบาย |
|----------|---------|
| `charticulatorSpec` | Full chart specification JSON |
| `charticulatorVersion` | Version of Charticulator engine |

### Custom Visual Deployment
| ช่องทาง | เหมาะสำหรับ |
|---------|-----------|
| **Organization** | Internal use — upload .pbiviz to Admin Portal |
| **AppSource** | Public — submit to Microsoft certification |
| **File import** | One-off — import .pbiviz per report |

---

## ⚡ Performance Optimization Checklist

### Report-Level (Visual Layer)

| # | Optimization | Impact | How |
|---|-------------|--------|-----|
| 1 | **จำกัด visuals ≤ 8 per page** | 🔴 High | แยกหน้า, ใช้ drill-through |
| 2 | **ปิด visual interactions ที่ไม่จำเป็น** | 🟡 Medium | Edit interactions → None |
| 3 | **ใช้ bookmarks แทน visuals ซ่อน** | 🟡 Medium | Toggle visibility via bookmarks |
| 4 | **ปิด Auto-Date hierarchy** | 🟡 Medium | `Options > Data Load > Auto Date/Time` off |
| 5 | **ใช้ Tooltips page แทน default** | 🟢 Low | Custom tooltip pages |
| 6 | **ลด animation duration** | 🟢 Low | `"animationDuration": 0` |

### Data Model (Semantic Layer)

| # | Optimization | Impact | How |
|---|-------------|--------|-----|
| 7 | **Star Schema** | 🔴 High | Fact + Dimension tables, single-direction relationships |
| 8 | **ลบ columns ที่ไม่ใช้** | 🔴 High | `isHidden` ไม่พอ — ต้องลบจาก source |
| 9 | **ใช้ integers แทน strings สำหรับ keys** | 🟡 Medium | Int64 joins เร็วกว่า string |
| 10 | **ลด cardinality** | 🟡 Medium | Group rare values → "Other" |
| 11 | **ใช้ calculated columns เท่าที่จำเป็น** | 🟡 Medium | Prefer source transformations |
| 12 | **Avoid bi-directional cross-filter** | 🟡 Medium | `crossFilteringBehavior: 1` (single) |
| 13 | **Pre-aggregate ใน source** | 🔴 High | Aggregate before import |

### DAX Optimization

| # | Pattern | ❌ ช้า | ✅ เร็ว |
|---|---------|-------|--------|
| 14 | **ใช้ VAR** | `DIVIDE(SUM(A), SUM(B))` repeated | `VAR _a = SUM(A) VAR _b = SUM(B) RETURN DIVIDE(_a, _b)` |
| 15 | **หลีกเลี่ยง FILTER** | `CALCULATE(SUM(A), FILTER(ALL(T), T[X]>10))` | `CALCULATE(SUM(A), T[X]>10)` |
| 16 | **SUMX/AVERAGEX minimal** | Nested iterators | Pre-calculate columns |
| 17 | **DISTINCTCOUNT → COUNTROWS** | `DISTINCTCOUNT(T[ID])` | `COUNTROWS(VALUES(T[ID]))` sometimes faster |
| 18 | **Avoid EARLIER** | `EARLIER(T[Col])` | Use VAR instead |
| 19 | **IF short-circuit** | Complex IF chains | `SWITCH(TRUE(), ...)` |

### Refresh & Connectivity

| # | Optimization | Impact | How |
|---|-------------|--------|-----|
| 20 | **Incremental Refresh** | 🔴 High | `rangeStart`/`rangeEnd` parameters in M |
| 21 | **DirectQuery for real-time** | 🔴 High | Large datasets > 1GB |
| 22 | **Composite model** | 🟡 Medium | Mix Import + DirectQuery |
| 23 | **Query folding** | 🔴 High | Keep steps foldable → check with "View Native Query" |
| 24 | **Dataflows** | 🟡 Medium | Shared data prep across reports |

### File Size Optimization

| # | Optimization | Impact | How |
|---|-------------|--------|-----|
| 25 | **Compress images** | 🟡 Medium | WebP < 100KB, resize to actual display size |
| 26 | **Remove unused resources** | 🟢 Low | Delete from `RegisteredResources` |
| 27 | **Minimize theme file** | 🟢 Low | Only override needed tokens |
| 28 | **Clean unused measures** | 🟡 Medium | Remove orphan measures |

### Performance Targets

| Metric | 🟢 Good | 🟡 Fair | 🔴 Poor |
|--------|---------|---------|---------|
| Page load time | < 3s | 3-8s | > 8s |
| Visual render | < 1s | 1-3s | > 3s |
| File size (PBIX) | < 50MB | 50-200MB | > 200MB |
| DAX query time | < 100ms | 100-500ms | > 500ms |
| Visuals per page | ≤ 8 | 9-15 | > 15 |
| Model columns | < 100 | 100-300 | > 300 |
| Relationships | < 20 | 20-50 | > 50 |

---

> 📝 **จบ Power BI PBIP Complete Skill** — 100/100 Score: PBIR Reference (3,800+ properties), Semantic Model, CI/CD, Custom Visuals, Performance, 25 Visual Generators, 31 DAX Templates, 15 Industries, 1,620+ Errors
