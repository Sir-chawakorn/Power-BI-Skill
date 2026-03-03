# 🚨 Power BI Error Reference & Troubleshooting Guide

> คู่มือแก้ไขปัญหา Power BI ครบทุก Category — ตั้งแต่ PBIP/PBIR format จนถึง DAX, Power Query, Refresh, Publish, Visual Rendering

---

## 📋 สารบัญ

| # | หมวด | ปัญหาทั้งหมด |
|---|------|-------------|
| 1 | [PBIP/PBIR Format Errors](#1-pbippbir-format-errors) | 8 |
| 2 | [File Corruption & Recovery](#2-file-corruption--recovery) | 6 |
| 3 | [DAX Errors](#3-dax-errors) | 10 |
| 4 | [Power Query M Errors](#4-power-query-m-errors) | 9 |
| 5 | [Data Refresh Errors](#5-data-refresh-errors) | 8 |
| 6 | [Visual Rendering Errors](#6-visual-rendering-errors) | 7 |
| 7 | [Publish & Permission Errors](#7-publish--permission-errors) | 8 |
| 8 | [Performance Issues](#8-performance-issues) | 10 |
| 9 | [PBIP Python Generator Errors](#9-pbip-python-generator-errors) | 12 |
| 10 | [Prevention Best Practices](#10-prevention-best-practices) | — |

> **Total: 78+ error patterns + solutions**

---

## 1. PBIP/PBIR Format Errors

### ERR-PBIP-001: ไม่สามารถเปิดไฟล์ .pbip

**Error Message:**
```
"Unable to open Power BI Project file"
"The file format is not recognized"
```

**สาเหตุ:**
- Power BI Desktop เวอร์ชันเก่าไม่รองรับ PBIP format
- ยังไม่ได้เปิด Preview feature

**วิธีแก้:**
1. อัพเดท Power BI Desktop เป็นเวอร์ชันล่าสุด
2. เปิด Preview features:
   - `File > Options > Preview Features > Power BI Project (.pbip)`
   - `File > Options > Preview Features > Store reports using enhanced metadata format`
3. Restart Power BI Desktop

**ป้องกัน:**
- ตรวจสอบเวอร์ชัน PBI Desktop ก่อนเริ่มทำงาน

---

### ERR-PBIP-002: model.bim หายจาก SemanticModel folder

**Error Message:**
```
"Unable to load the data model"
"SemanticModel definition is missing"
```

**สาเหตุ:**
- Save ไม่สมบูรณ์ (ปิดโปรแกรมกลางทาง)
- git merge ผิดพลาดทำให้ไฟล์ถูกลบ

**วิธีแก้:**
1. เปิด Power BI Desktop แล้ว Save ใหม่ (regenerate model.bim)
2. ตรวจ Auto-Recovery: `File > Options > Auto Recovery`
3. ถ้าใช้ git → `git log --all -- "*.bim"` หา commit ที่มีไฟล์
4. สุดท้าย: สร้าง data model ใหม่จาก data source

**ป้องกัน:**
- ใส่ `model.bim` ในการตรวจสอบ CI pipeline
- Auto-save เปิดไว้เสมอ

---

### ERR-PBIP-003: definition.pbir version ไม่ตรง

**Error Message:**
```
"Incompatible report definition version"
```

**สาเหตุ:**
- ใช้ version ที่ PBI Desktop ไม่รองรับ
- mix PBIR-Legacy กับ PBIR folder format

**วิธีแก้:**
```json
// ✅ PBIR-Legacy (recommended — single report.json)
{"version": "4.0", "datasetReference": {"byPath": {"path": "..."}}}

// ❌ อย่าใช้ version ที่เก่ากว่า 4.0
```

**ป้องกัน:**
- ใช้ `"version": "4.0"` เสมอ
- อย่า mix format แบบ PBIR folder structure กับ PBIR-Legacy

---

### ERR-PBIP-004: report.json invalid JSON

**Error Message:**
```
"Cannot parse report definition"
"Invalid JSON in report.json"
```

**สาเหตุ:**
- JSON syntax error (missing comma, bracket, quote)
- Stringified JSON ใน config/filters ไม่ได้ escape ถูกต้อง
- Encoding ไม่ใช่ UTF-8

**วิธีแก้:**
1. Validate JSON: ใช้ `python -m json.tool report.json`
2. ตรวจสอบ stringified fields:
   ```python
   import json
   # ทดสอบ parse ทุก stringified field
   data = json.loads(open('report.json').read())
   for section in data.get('sections', []):
       json.loads(section.get('config', '{}'))  # ต้อง parse ได้
       json.loads(section.get('filters', '[]'))
       for vc in section.get('visualContainers', []):
           json.loads(vc.get('config', '{}'))
           json.loads(vc.get('filters', '[]'))
   ```
3. ตรวจ encoding: เปิดด้วย Notepad++ ดู encoding → แปลงเป็น UTF-8

**ป้องกัน:**
- ใช้ `json.dumps(..., ensure_ascii=False)` เมื่อเขียนด้วย Python
- Validate ทุกครั้งก่อนเปิดใน PBI Desktop

---

### ERR-PBIP-005: .platform file ไม่ถูกต้อง

**Error Message:**
```
"Invalid platform configuration"
```

**สาเหตุ:**
- logicalId ไม่ใช่ UUID ที่ถูกต้อง
- type ไม่ตรง (Report vs SemanticModel)

**วิธีแก้:**
```json
// ✅ Report .platform
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {"type": "Report", "displayName": "MyReport"},
  "config": {"version": "2.0", "logicalId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}
}

// ✅ SemanticModel .platform
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {"type": "SemanticModel", "displayName": "MyModel"},
  "config": {"version": "2.0", "logicalId": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"}
}
```

**ป้องกัน:**
- ใช้ `uuid.uuid4()` ใน Python สร้าง logicalId
- Report กับ SemanticModel ต้องใช้ logicalId **คนละตัว**

---

### ERR-PBIP-006: Deployment Pipeline — "Something went wrong"

**Error Message:**
```
"Something went wrong. Unable to load report"
"Different from Source"
```

**สาเหตุ:**
- Report ที่ save เป็น .pbip + PBIR preview ไม่ compatible กับ Pipeline
- Report/Model pairing ผิดข้าม stage

**วิธีแก้:**
1. ลองปิด PBIR Preview Feature → Save เป็น .pbix ก่อน → deploy
2. ตรวจสอบ pairing: Report ↔ Semantic Model ต้องตรงกันทุก stage
3. ตรวจ file structure ใน git ว่าไม่ถูกแก้นอก PBI Desktop
4. ถ้ายังไม่ได้ → publish .pbix ตรงแทน pipeline

---

### ERR-PBIP-007: รูปภาพหายหลัง Reset Filters (PBIR)

**Error Message:**
```
// ไม่มี error message — รูปภาพหายเฉยๆ
```

**สาเหตุ:**
- PBIR thin reports อ้างรูปจาก external path แทน embedded
- User กด "Reset filters" → รูปหาย

**วิธีแก้:**
1. เปิดใน PBI Desktop → ลบรูปเก่า → เพิ่มใหม่ด้วย "Add image" (จะ embed เป็น Base64)
2. Republish report

**ป้องกัน:**
- อย่าอ้างรูปจาก local path ใน PBIP → ใช้ embedded เสมอ

---

### ERR-PBIP-008: PBIRS Upgrade ทำให้ Report เปิดไม่ได้

**Error Message:**
```
"Unable to load the data model for your Power BI report"
HTTP 500
```

**สาเหตุ:**
- ใช้ PBI Desktop ไม่ตรง edition กับ PBIRS version

**วิธีแก้:**
1. ใช้ PBI Desktop **Report Server edition** ที่ตรงกับ PBIRS version
2. Clear cache: `Options > Data Load > Clear Cache`
3. Refresh manual → Save As ชื่อใหม่

---

## 2. File Corruption & Recovery

### ERR-FILE-001: ไฟล์ .pbix เปิดไม่ได้

**Error Message:**
```
"We're sorry, this file appears to be corrupted"
"Cannot open file"
```

**วิธีแก้ (ลองตามลำดับ):**

| ลำดับ | วิธี | รายละเอียด |
|-------|------|-----------|
| 1 | Auto-Recovery | เปิด PBI Desktop ก่อน → `File > Open` → คลิก yellow ribbon |
| 2 | TempSaves | ไปที่ `%LocalAppData%\Microsoft\Power BI Desktop\TempSaves\` |
| 3 | OneDrive/SharePoint | Download fresh copy จาก cloud |
| 4 | PBI Service | Download จาก workspace ที่เคย publish ไว้ |
| 5 | Unzip method | เปลี่ยน .pbix → .zip → extract → แก้ → zip กลับ |
| 6 | Tabular Editor | ถ้า model สำคัญ → ใช้ .bim จาก Tabular Editor inject เข้าไฟล์ใหม่ |

---

### ERR-FILE-002: Version Incompatibility

**วิธีแก้:**
- อัพเดท PBI Desktop ให้เป็นเวอร์ชันล่าสุด
- ลบ installation เก่าทั้งหมด → clean install จาก Microsoft website
- ตรวจสอบว่าไม่มีหลาย version ติดตั้งพร้อมกัน

---

### ERR-FILE-003: ไฟล์ .pbix ขนาดใหญ่ > 1GB

**อาการ:**
- Save ช้ามาก / ค้าง
- เปิดไม่ได้หลัง save

**วิธีแก้:**
1. ลดขนาด data: ลบ column ที่ไม่ใช้ / filter rows
2. ใช้ Aggregation tables
3. เปลี่ยนเป็น DirectQuery สำหรับ table ใหญ่
4. แยก report ออกเป็นหลาย files

---

### ERR-FILE-004: Antivirus Block

**วิธีแก้:**
- Whitelist Power BI Desktop ใน antivirus
- Whitelist โฟลเดอร์ `%LocalAppData%\Microsoft\Power BI Desktop\`

---

### ERR-FILE-005: localSettings.json Invalid

**Error Message:**
```
"Invalid type. Expected String but got Null"
```

**วิธีแก้:**
- ลบไฟล์ `localSettings.json` ออก → PBI Desktop จะสร้างใหม่

---

### ERR-FILE-006: Git Merge Conflict ใน report.json

**อาการ:**
- `<<<<<<<` markers ใน JSON file

**วิธีแก้:**
1. ใช้ JSON-aware merge tool
2. หรือ accept ฝั่งเดียว → เปิดใน PBI Desktop → แก้ไข manual → save

**ป้องกัน:**
- ใช้ `.gitattributes` กำหนด merge strategy
- ใช้ branching strategy ที่ไม่ให้แก้ report.json พร้อมกัน

---

## 3. DAX Errors

### ERR-DAX-001: Circular Dependency

**Error Message:**
```
"A circular dependency was detected"
```

**สาเหตุ:**
- Calculated column A อ้าง B, B อ้าง A
- `CALCULATE` ใน calculated column ทำให้เกิด context transition loop
- Bi-directional relationship สร้าง loop

**วิธีแก้:**

```dax
// ❌ BAD — circular dependency
Column_A = [Column_B] * 2
Column_B = [Column_A] + 1

// ✅ FIX 1: รวม logic เข้าด้วยกัน
Column_Result = <base_value> * 2 + 1

// ✅ FIX 2: ใช้ VAR
My Measure =
VAR BaseVal = SUM('Table'[Amount])
VAR Adjusted = BaseVal * 1.1
RETURN Adjusted

// ✅ FIX 3: ใช้ Measure แทน Calculated Column
// Measure ไม่เก็บ dependency แบบ column

// ✅ FIX 4: ย้าย logic ไป Power Query (M)
// M ไม่มี circular dependency issue
```

**ป้องกัน:**
- ใช้ **Measure** แทน Calculated Column เมื่อทำได้
- หลีกเลี่ยง bi-directional relationships ที่ไม่จำเป็น
- ใช้ `ALLEXCEPT` / `REMOVEFILTERS` จำกัด dependency

---

### ERR-DAX-002: Ambiguous Column Reference

**Error Message:**
```
"The column 'ColumnName' in table 'Table' is ambiguous"
```

**วิธีแก้:**
```dax
// ❌ BAD — ambiguous
Total = SUM([Amount])

// ✅ GOOD — fully qualified
Total = SUM('Sales'[Amount])

// ❌ BAD — LOOKUPVALUE without table name
LOOKUPVALUE([Name], [ID], 1)

// ✅ GOOD
LOOKUPVALUE('Products'[Name], 'Products'[ID], 1)
```

**กฎ:**
- **เสมอ** qualify column ด้วยชื่อ table: `'TableName'[ColumnName]`
- ชื่อ column ห้ามซ้ำกับ measure ใน table เดียวกัน

---

### ERR-DAX-003: Division by Zero

**Error Message:**
```
"Cannot divide by zero"
```

**วิธีแก้:**
```dax
// ❌ BAD
Margin = [Revenue] / [Cost]

// ✅ GOOD — ใช้ DIVIDE()
Margin = DIVIDE([Revenue], [Cost], 0)

// ✅ GOOD — ใช้ IF
Margin = IF([Cost] = 0, 0, [Revenue] / [Cost])
```

---

### ERR-DAX-004: Type Mismatch

**Error Message:**
```
"Cannot convert value 'text' of type Text to Number"
```

**วิธีแก้:**
```dax
// แปลง text → number
VALUE("123")

// แปลง number → text
FORMAT(123, "0")

// แปลง date → text
FORMAT(TODAY(), "YYYY-MM-DD")
```

---

### ERR-DAX-005: CALCULATE Context Transition Error

**Error Message:**
```
"A table of multiple values was supplied where a single value was expected"
```

**วิธีแก้:**
```dax
// ❌ BAD — ใน Calculated Column
Col = CALCULATE(SUM('Table'[Amount]))  // context transition ทั้ง table!

// ✅ GOOD — จำกัด filter
Col = CALCULATE(
    SUM('Table'[Amount]),
    ALLEXCEPT('Table', 'Table'[ID])
)
```

---

### ERR-DAX-006: RELATED() ใช้ไม่ได้

**Error Message:**
```
"RELATED function requires a row context"
"No relationship found"
```

**วิธีแก้:**
1. ตรวจว่ามี relationship ระหว่าง 2 tables (Model view)
2. `RELATED()` ใช้ได้เฉพาะ many-to-one direction
3. ถ้า one-to-many → ใช้ `RELATEDTABLE()` แทน
4. ถ้าไม่มี relationship → ใช้ `LOOKUPVALUE()` แทน

---

### ERR-DAX-007: Time Intelligence ไม่ทำงาน

**Error Message:**
```
"TOTALYTD requires a date column marked as date table"
// หรือ return BLANK()
```

**วิธีแก้:**
```dax
// ต้องมี Date table ที่ mark แล้ว
// ใน model.bim:
// 1. สร้าง Date table ครบทุกวัน (ไม่ขาด)
// 2. Mark as date table

// DAX สร้าง Date table:
DateTable = CALENDAR(DATE(2020,1,1), DATE(2030,12,31))

// Mark as date table:
// Model view → Table → Mark as Date Table → เลือก Date column
```

**Checklist:**
- [ ] Date table ครบทุกวัน ไม่มี gap
- [ ] Mark as Date Table แล้ว
- [ ] Relationship ระหว่าง Date table กับ Fact table ถูกต้อง

---

### ERR-DAX-008: DISTINCTCOUNT ไม่มีใน prototypeQuery

**Error Message:**
```
// ใน PBIP: visual ไม่แสดงค่าถูกต้อง
```

**สาเหตุ:**
- `DISTINCTCOUNT` ไม่อยู่ใน prototypeQuery aggregation functions (0-5)

**วิธีแก้:**
```dax
// สร้าง DAX measure แทน
Unique Customers = DISTINCTCOUNT('Orders'[customer_id])
```

```json
// ใน prototypeQuery ใช้ Measure reference:
{
  "Measure": {
    "Expression": {"SourceRef": {"Source": "d"}},
    "Property": "Unique Customers"
  },
  "Name": "Orders.Unique Customers"
}
```

---

### ERR-DAX-009: SELECTEDVALUE / SWITCH ไม่ทำงาน

**วิธีแก้:**
```dax
// ต้องมี Slicer ที่เชื่อมกับ column ที่ SELECTEDVALUE อ้างถึง
Selected Metric = SWITCH(
    SELECTEDVALUE('Metrics'[Name]),
    "Revenue", [Total Revenue],
    "Orders", [Total Orders],
    BLANK()  // ← ต้องมี default!
)
```

---

### ERR-DAX-010: Measure ใช้ใน Filter ไม่ได้

**วิธีแก้:**
- สร้าง Calculated Column แทน (ถ้าต้อง filter ที่ row level)
- หรือใช้ Visual-level filter ด้วย Measure (ซึ่ง PBI รองรับ)

---

## 4. Power Query M Errors

### ERR-PQ-001: Expression.Error — Column Not Found

**Error Message:**
```
Expression.Error: The column 'OldName' of the table wasn't found
```

**วิธีแก้:**
1. เปิด Power Query Editor
2. ไปที่ Applied Steps → หา step ที่ error
3. ตรวจชื่อ column ใน M code → แก้ให้ตรงกับชื่อจริง
4. ถ้า column ถูก rename → อัพเดท step ถัดไปด้วย

---

### ERR-PQ-002: DataFormat.Error — ข้อมูล type ไม่ตรง

**Error Message:**
```
DataFormat.Error: We couldn't convert to Number
DataFormat.Error: We couldn't parse the input provided as a Date value
```

**วิธีแก้:**
```m
// ✅ FIX 1: ลบ auto "Changed Type" step → set type manual
// ✅ FIX 2: Replace errors
= Table.ReplaceErrorValues(PreviousStep, {{"Column", 0}})

// ✅ FIX 3: ใช้ try...otherwise สำหรับ cell-level
= Table.TransformColumns(Source, {
    {"Price", each try Number.From(_) otherwise 0}
})

// ✅ FIX 4: ใช้ locale-aware type change
// Right-click column > Change Type > Using Locale
```

**ป้องกัน:**
- อย่าใช้ auto type detection สำหรับ data ที่มี mixed types
- Clean data ก่อน change type (Trim, Clean, Replace)

---

### ERR-PQ-003: DataSource.Error — หา source ไม่เจอ

**Error Message:**
```
DataSource.Error: The path '...' doesn't exist
DataSource.Error: Could not find file
```

**วิธีแก้:**
```m
// ✅ FIX 1: ใช้ Parameter แทน hardcode path
let
    FilePath = Excel.CurrentWorkbook(){[Name="ParamPath"]}[Content]{0}[Column1],
    Source = Csv.Document(File.Contents(FilePath))
in Source

// ✅ FIX 2: แก้ path ใน Data Source Settings
// File > Options > Data source settings > Change Source
```

---

### ERR-PQ-004: Formula.Firewall — Privacy Levels

**Error Message:**
```
Formula.Firewall: Query references other queries or steps
```

**วิธีแก้:**
1. `File > Options > Privacy > Ignore the Privacy Levels`
2. หรือ set Privacy Level ของทุก source ให้เป็น level เดียวกัน
3. หรือ combine queries ให้ source เดียวกัน

---

### ERR-PQ-005: OLE DB / ODBC Connection Error

**Error Message:**
```
DataSource.Error: Microsoft SQL: Login failed
DataSource.Error: ODBC: connection refused
```

**วิธีแก้:**
1. ตรวจ server name, database name ถูกต้อง
2. ตรวจ credentials ใน Data Source Settings
3. ตรวจ firewall/VPN (ต้อง connect กับ server ได้)
4. ตรวจ ODBC driver ติดตั้งแล้ว

---

### ERR-PQ-006: Web.Contents & API Errors

**Error Message:**
```
DataSource.Error: The remote server returned an error: (401) Unauthorized
DataSource.Error: The remote server returned an error: (429) Too Many Requests
```

**วิธีแก้:**
```m
// ✅ 401: ใส่ auth header
= Json.Document(Web.Contents("https://api.example.com/data", [
    Headers = [
        #"Authorization" = "Bearer " & token,
        #"Content-Type" = "application/json"
    ]
]))

// ✅ 429: ใช้ Binary.Buffer + delay
// ลด request frequency หรือ implement pagination
```

---

### ERR-PQ-007: Query Folding ไม่ทำงาน

**อาการ:**
- Refresh ช้ามาก (ดึง data ทั้งหมดแล้ว filter ใน engine)

**ตรวจสอบ:**
- Right-click step → "View Native Query" → ถ้าเป็นสีเทา = ไม่ fold

**วิธีแก้:**
- ย้าย filter/column removal ไปเป็น step แรกๆ
- หลีกเลี่ยง custom functions ที่ทำให้ folding หยุด
- ใช้ `Table.SelectRows` แทน custom filter

---

### ERR-PQ-008: Encoding ผิด — ภาษาไทย/Unicode

**อาการ:**
- ข้อมูลภาษาไทยแสดงเป็นอักขระแปลกๆ

**วิธีแก้:**
```m
// ✅ ระบุ Encoding 65001 (UTF-8) ตอน import CSV
= Csv.Document(File.Contents("data.csv"), [
    Delimiter = ",",
    Encoding = 65001,    // ← UTF-8!
    QuoteStyle = QuoteStyle.None
])
```

**Encoding codes:**
| Code | Encoding |
|------|----------|
| 65001 | UTF-8 |
| 874 | Thai (Windows) |
| 1252 | Western European |
| 932 | Japanese Shift-JIS |

---

### ERR-PQ-009: Duplicate Column ตอน Pivot

**Error Message:**
```
Expression.Error: There weren't enough elements in the enumeration
```

**วิธีแก้:**
- เพิ่ม Index column ก่อน pivot
- หรือลบ duplicate values ก่อน

---

## 5. Data Refresh Errors

### ERR-REFRESH-001: Gateway Timeout

**Error Message:**
```
"The gateway did not receive a response from the data source"
"Processing timed out"
```

**Timeout limits:**
| Workspace Type | Timeout |
|----------------|---------|
| Standard | 2 ชั่วโมง |
| Premium | 5 ชั่วโมง |

**วิธีแก้:**
1. Optimize queries: ลดขนาด dataset / แยกเป็น incremental refresh
2. Stagger refresh schedules: ไม่ refresh หลาย dataset พร้อมกัน
3. พิจารณา DirectQuery สำหรับ real-time data
4. ตรวจ database-side timeout settings

---

### ERR-REFRESH-002: Credentials Expired

**Error Message:**
```
"The credentials provided for the data source are invalid"
"Access to the resource is forbidden"
```

**วิธีแก้:**
1. PBI Service → Dataset Settings → Data source credentials → Edit → re-enter
2. เปิด `https://app.powerbi.com?alwaysPromptForContentProviderCreds=true`
3. PBI Desktop → Transform Data → Data source settings → Edit credentials
4. Clear Windows Credential Manager (ลบ entry ที่เกี่ยวกับ powerbi/microsoft)

**ป้องกัน:**
- ใช้ Service Principal แทน user account สำหรับ automated refresh
- ตั้ง reminder update password ก่อนหมดอายุ

---

### ERR-REFRESH-003: Data Source Not Found

**Error Message:**
```
"Data source path has changed"
"File not found"
```

**วิธีแก้:**
1. ตรวจไฟล์ยังอยู่ที่เดิม
2. Update path: Dataset Settings → Parameters → Edit
3. ใช้ Power Query Parameter สำหรับ file paths (เปลี่ยนง่าย)
4. ถ้าใช้ local file → อัพโหลดไป SharePoint Online แทน

---

### ERR-REFRESH-004: 4 ครั้ง fail → Scheduled Refresh ถูกปิด

**สาเหตุ:**
- Power BI auto-disable scheduled refresh หลัง fail 4 ครั้งติด

**วิธีแก้:**
1. แก้ root cause ของ refresh error ก่อน
2. Dataset Settings → Scheduled Refresh → เปิดใหม่
3. Trigger manual refresh ทดสอบก่อน

---

### ERR-REFRESH-005: OAuth Token Expired (Entra ID)

**วิธีแก้:**
- Token expire หลัง ~1 ชั่วโมง
- ถ้า data load นานกว่า 1 ชั่วโมง → ลดขนาด data / optimize queries
- ใช้ Service Principal แทน OAuth token

---

### ERR-REFRESH-006: Complex M Expression Timeout

**วิธีแก้:**
```m
// ✅ ใช้ Table.Buffer สำหรับ outer join
let
    BufferedTable = Table.Buffer(OtherTable),
    Merged = Table.NestedJoin(MainTable, "Key", BufferedTable, "Key", "Joined")
in Merged
```

---

### ERR-REFRESH-007: Incremental Refresh ไม่ทำงาน

**Checklist:**
- [ ] มี RangeStart และ RangeEnd parameters (type DateTime)
- [ ] Query fold ได้ (Native Query available)
- [ ] Filter step ใช้ parameters ถูกต้อง

---

### ERR-REFRESH-008: Gateway Offline / Version เก่า

**วิธีแก้:**
1. ตรวจ gateway service กำลังทำงาน
2. อัพเดท gateway เป็นเวอร์ชันล่าสุด (Microsoft support เฉพาะ 6 versions ล่าสุด)
3. Restart gateway service

---

## 6. Visual Rendering Errors

### ERR-VIS-001: "Can't display this visual"

**สาเหตุ & วิธีแก้:**

| สาเหตุ | วิธีแก้ |
|--------|---------|
| Data มากเกินไป | Filter / ลด rows → ใช้ Top N |
| DAX error ใน measure | ตรวจ DAX ใน measure ที่ visual ใช้ |
| Relationship ผิด | ตรวจ Model view → fix relationships |
| Column/Measure ถูกลบ | ตรวจ Fields pane → ลบ field ที่ broken |
| Custom visual ไม่ compatible | อัพเดท custom visual หรือใช้ native visual |
| RLS ไม่ได้ assign role | Assign user เข้า RLS role |

---

### ERR-VIS-002: "Too many values"

**วิธีแก้:**
1. Apply filters ลด data points
2. Aggregate ขึ้นระดับที่สูงกว่า (เช่น per hour → per day)
3. ใช้ Top N filter
4. เปลี่ยน visual type ที่รองรับ data เยอะกว่า (table แทน chart)

**Limits:**
| Visual Type | Max Data Points |
|-------------|----------------|
| R Visual | 150,000 rows |
| Python Visual | 150,000 rows |
| Map | ~3,500 unique locations |
| Line/Bar/Column | ~30,000 data points |

---

### ERR-VIS-003: Visual แสดงค่าผิด / ว่าง

**Checklist:**
- [ ] Aggregation ถูกต้อง (Sum vs Count vs Average)
- [ ] Relationship direction ถูก (1:N vs N:1)
- [ ] Filter context ไม่ block data
- [ ] Date column marked as Date type
- [ ] ไม่มี blank rows ใน data

---

### ERR-VIS-004: Slicer ไม่ filter visuals อื่น

**วิธีแก้:**
1. ตรวจ Slicer column มี relationship กับ table ที่ visual อื่นใช้
2. ตรวจ Edit Interactions: Format → Edit Interactions → ไม่ได้ set เป็น "None"
3. ตรวจ Slicer ไม่ได้อยู่ใน different page (ใช้ Sync Slicers แทน)

---

### ERR-VIS-005: Conditional Formatting ไม่ทำงาน

**วิธีแก้:**
1. ตรวจว่า measure return ค่า color ถูกต้อง (เช่น `"#FF0000"`)
2. ตรวจว่า rule range ไม่ overlap
3. ถ้าใช้ field value → ตรวจว่า field มีค่าจริง (ไม่ BLANK)

---

### ERR-VIS-006: Tooltip ไม่แสดง

**วิธีแก้:**
1. ตรวจ Tooltip page: `displayOption: 2` + size 320×240 หรือ 640×480
2. Visual ต้อง set tooltip → Report page → เลือก Tooltip page
3. Tooltip page ต้องมี field ที่ match กับ visual (drill-through field)

---

### ERR-VIS-007: Map Visual ไม่แสดงข้อมูล

**วิธีแก้:**
1. Set Data Category ใน model.bim:
   ```json
   {"name": "city", "dataType": "string", "sourceColumn": "city",
    "annotations": [{"name": "DataCategory", "value": "City"}]}
   ```
2. Data Category options: `Country`, `StateOrProvince`, `City`, `Latitude`, `Longitude`
3. ตรวจว่า Bing Maps service ใช้ได้ (ต้อง internet)

---

## 7. Publish & Permission Errors

### ERR-PUB-001: Access Denied — ไม่มีสิทธิ์ publish

**วิธีแก้:**
- ต้องมี role อย่างน้อย **Contributor** ใน workspace

| Role | Publish? | Edit? | View? |
|------|----------|-------|-------|
| Viewer | ❌ | ❌ | ✅ |
| Contributor | ✅ | ✅ | ✅ |
| Member | ✅ | ✅ | ✅ |
| Admin | ✅ | ✅ | ✅ |

---

### ERR-PUB-002: Cross-Workspace Semantic Model Error

**วิธีแก้:**
- เปิด tenant setting: "Use semantic models across workspaces"
- หรือ publish report ไปที่ workspace เดียวกับ dataset

---

### ERR-PUB-003: RLS ไม่ทำงานหลัง publish

**วิธีแก้:**
1. สร้าง RLS roles ใน PBI Desktop (Modeling tab → Manage Roles)
2. Publish report + dataset
3. **ใน PBI Service**: Dataset → Security → Assign users/groups เข้า roles
4. ทดสอบ: Dataset → Security → "Test as role"

**ผิดบ่อย:**
- ลืม assign users ใน Service (ขั้นตอนที่ 3)
- Dynamic RLS ใช้ `USERPRINCIPALNAME()` แต่ email ไม่ตรง

---

### ERR-PUB-004: Publish ล้มเหลว — Network/Firewall

**วิธีแก้:**
1. ตรวจ internet connection
2. Whitelist Power BI URLs ใน firewall:
   - `*.powerbi.com`
   - `*.analysis.windows.net`
   - `*.pbidedicated.windows.net`
3. ตรวจ proxy settings
4. ลอง upload .pbix ผ่าน PBI Service แทน (Get Data → Local file)

---

### ERR-PUB-005: "Take Over" Dataset

**อาการ:**
- ไม่สามารถ edit credentials ของ dataset ที่คนอื่นสร้าง

**วิธีแก้:**
- Dataset Settings → "Take over" (เปลี่ยน ownership ให้ตัวเอง)

---

### ERR-PUB-006: App ไม่ update หลัง publish

**วิธีแก้:**
- ต้อง "Update App" แยกจากการ publish report
- Workspace → App → Update App

---

### ERR-PUB-007: Sensitivity Label Block

**วิธีแก้:**
- ต้องมี Premium license สำหรับ sensitivity labels
- ตรวจว่า label ที่ใช้ไม่ block download/export

---

### ERR-PUB-008: Paginated Report Publish Error

**วิธีแก้:**
- ต้อง publish ไปที่ Premium workspace เท่านั้น
- ใช้ Power BI Report Builder (ไม่ใช่ Desktop)

---

## 8. Performance Issues

### PERF-001: Dashboard โหลดช้า

**Diagnostic Tool:** View → Performance Analyzer

**ตรวจดู:**
| Component | ช้า = | วิธีแก้ |
|-----------|-------|---------|
| DAX Query | > 500ms | Optimize DAX, ลด complexity |
| Visual Rendering | > 300ms | ลดจำนวน data points |
| Other | > 200ms | ตรวจ data source / network |

---

### PERF-002: ลดจำนวน Visual ต่อหน้า

**แนะนำ:** ไม่เกิน 8 visuals + 1 table ต่อหน้า

**ทำไม:** แต่ละ visual = 1 query → ยิ่งเยอะยิ่งช้า

---

### PERF-003: Star Schema

```
// ✅ GOOD — Star Schema
FactSales ←→ DimProduct
           ←→ DimCustomer
           ←→ DimDate
           ←→ DimStore

// ❌ BAD — Flat Table (ทุกอย่างรวมใน table เดียว)
```

**ทำไม:** Star Schema ใช้ memory น้อยกว่า + query เร็วกว่า

---

### PERF-004: Remove Unused Columns

```m
// ✅ ลบ column ที่ไม่ใช้ตั้งแต่ใน Power Query
= Table.RemoveColumns(Source, {"col1", "col2", "unused_col"})
```

**กฎ:** ทุก column ใช้ memory — ลบ column ที่ไม่ได้ใช้ใน visual

---

### PERF-005: Optimize Data Types

| เดิม | เปลี่ยนเป็น | ประหยัด |
|------|------------|---------|
| `double` (8 bytes) | `int64` (8 bytes, compress ดีกว่า) | ~30% |
| `string` (variable) | `int64` + lookup table | ~50-80% |
| `datetime` (8 bytes) | `date` only (4 bytes) | ~50% |

---

### PERF-006: ใช้ Aggregations

```json
// ใน model.bim — สร้าง aggregation table
// Pre-aggregate: SUM, COUNT, AVG ที่ grain ที่ใช้บ่อย
// PBI จะใช้ aggregation table แทน detail table เมื่อทำได้
```

---

### PERF-007: Slicer Optimization

- ลด cardinality (จำนวน unique values) ใน slicer
- ใช้ Dropdown แทน List สำหรับ slicer ที่มีค่าเยอะ
- ปิด cross-filtering ที่ไม่จำเป็น

---

### PERF-008: DAX Optimization

```dax
// ❌ SLOW — iterates over every row
Slow Measure = SUMX('BigTable', 'BigTable'[Price] * 'BigTable'[Qty])

// ✅ FAST — pre-calculated column or measure
// สร้าง calculated column: LineTotal = [Price] * [Qty]
// แล้ว: Fast Measure = SUM('BigTable'[LineTotal])

// ❌ SLOW — multiple CALCULATE
Slow = CALCULATE(SUM(...)) + CALCULATE(COUNT(...))

// ✅ FAST — VAR + single context
Fast =
VAR TotalSales = SUM('Sales'[Amount])
VAR TotalOrders = COUNTROWS('Sales')
RETURN TotalSales / TotalOrders
```

---

### PERF-009: Import vs DirectQuery

| Mode | เร็วที่สุด | เหมาะกับ |
|------|-----------|---------|
| **Import** | ⚡⚡⚡ | Dataset < 1GB, ไม่ต้อง real-time |
| **DirectQuery** | ⚡ | Dataset ใหญ่มาก, ต้อง real-time |
| **Composite** | ⚡⚡ | Mix: table สำคัญ = Import, table ใหญ่ = DirectQuery |

---

### PERF-010: Performance Targets

| Metric | Target |
|--------|--------|
| Initial page load | < 3 วินาที |
| Visual interaction | < 1 วินาที |
| Slicer response | < 500ms |
| Refresh time (daily) | < 30 นาที |
| Dataset size (.pbix) | < 500MB |

---

## 9. PBIP Python Generator Errors

> สำหรับเมื่อสร้าง dashboard ด้วย `generate.py` หรือ script อื่น

### ERR-GEN-001: config ไม่ได้ stringify

```python
# ❌ BAD — config เป็น dict
visual_container = {
    "config": {"name": "abc", "singleVisual": {...}},  # ผิด!
}

# ✅ GOOD — config ต้อง stringify
import json
visual_container = {
    "config": json.dumps({"name": "abc", "singleVisual": {...}}),
}
```

---

### ERR-GEN-002: filters ไม่ได้ stringify

```python
# ❌ BAD
"filters": []

# ✅ GOOD
"filters": "[]"
```

---

### ERR-GEN-003: ไม่มี prototypeQuery

**อาการ:** Visual แสดงแต่ไม่มี data

**วิธีแก้:** ทุก visual (ยกเว้น textbox/shape/image) ต้องมี prototypeQuery

---

### ERR-GEN-004: queryRef ไม่ตรงกับ prototypeQuery.Select.Name

```python
# ❌ BAD — ไม่ตรง
"projections": {"Category": [{"queryRef": "date_col"}]}
# แต่ใน Select: {"Name": "table.date_col"}

# ✅ GOOD — ต้องตรงกับ Name
"projections": {"Category": [{"queryRef": "table.date_col"}]}
# Select: {"Name": "table.date_col"}
```

---

### ERR-GEN-005: From alias ไม่ตรง

```python
# Select ใช้ Source "d" แต่ From ใช้ Name "t"
# ❌ BAD
"From": [{"Name": "t", "Entity": "Sales", "Type": 0}],
"Select": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}}}]

# ✅ GOOD — ต้องตรงกัน
"From": [{"Name": "d", "Entity": "Sales", "Type": 0}],
"Select": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}}}]
```

---

### ERR-GEN-006: hex ID ไม่ unique

```python
# ❌ BAD — ใช้ ID ซ้ำ
section_name = "abc123"
visual_name = "abc123"  # ซ้ำ!

# ✅ GOOD — unique hex IDs
import secrets
section_name = secrets.token_hex(10)  # 20-char hex
visual_name = secrets.token_hex(10)   # different!
```

---

### ERR-GEN-007: z-order / tabOrder ซ้ำ

**วิธีแก้:** ใช้ z-order ที่เพิ่มขึ้นตามลำดับ

```python
for i, visual in enumerate(visuals):
    visual["z"] = (i + 1) * 1000.0
    config = json.loads(visual["config"])
    config["layouts"][0]["position"]["z"] = (i + 1) * 1000
    config["layouts"][0]["position"]["tabOrder"] = (i + 1) * 1000
```

---

### ERR-GEN-008: Float precision ใน position

```python
# ❌ BAD
"height": 300, "width": 600

# ✅ GOOD — ใช้ float
"height": 300.0, "width": 600.0, "x": 20.0, "y": 190.0
```

---

### ERR-GEN-009: model.bim — partition expression ผิด format

```python
# ❌ BAD — string เดียว
"expression": "let Source = ... in Source"

# ✅ GOOD — array ของ strings (แต่ละบรรทัด)
"expression": [
    "let",
    "  Source = Csv.Document(File.Contents(\"C:\\\\data\\\\file.csv\"), [Delimiter=\",\", Encoding=65001]),",
    "  Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true])",
    "in",
    "  Headers"
]
```

---

### ERR-GEN-010: ลืมใส่ compatibilityLevel

```python
# ❌ BAD
{"name": "Model", "model": {...}}

# ✅ GOOD
{"name": "Model", "compatibilityLevel": 1567, "model": {...}}
```

---

### ERR-GEN-011: ลืม drillFilterOtherVisuals

```python
# ต้องมีใน singleVisual
"drillFilterOtherVisuals": True
```

---

### ERR-GEN-012: Theme version ไม่ตรง

```python
# ✅ ใช้ theme ที่ compatible
"themeCollection": {
    "baseTheme": {
        "name": "CY24SU11",  # ตรวจว่าตรงกับ PBI version
        "version": {"visual": "2.6.0", "report": "3.1.0", "page": "2.3.0"},
        "type": 2
    }
}
```

---

## 10. Prevention Best Practices

### 🛡️ Checklist ก่อน Publish

- [ ] JSON ทุกไฟล์ valid (`python -m json.tool`)
- [ ] config / filters fields เป็น **stringified** JSON
- [ ] hex IDs ไม่ซ้ำกัน
- [ ] prototypeQuery.Select.Name ตรงกับ projections.queryRef
- [ ] From.Name ตรงกับ SourceRef.Source
- [ ] Position values เป็น float (300.0 ไม่ใช่ 300)
- [ ] Data refresh ทำงานปกติ
- [ ] RLS roles assigned (ถ้ามี)
- [ ] Workspace permissions ถูกต้อง

### 🛡️ Regular Maintenance

| ทำทุก | Action |
|-------|--------|
| วัน | ตรวจ scheduled refresh ไม่ fail |
| สัปดาห์ | ตรวจ gateway status + version |
| เดือน | Review dataset size + optimize |
| ไตรมาส | Review permissions + RLS + cleanup |

### 🛡️ Version Control (Git)

```gitignore
# .gitignore สำหรับ PBIP
*.pbi.local.*
localSettings.json
.pbi/
```

```gitattributes
# .gitattributes — ป้องกัน merge conflict
*.json merge=union
report.json -merge
```

### 🛡️ Backup Strategy

| วิธี | ข้อดี |
|------|------|
| OneDrive/SharePoint | Auto version history |
| Git | Full history + branching |
| PBI Service publish | Cloud backup |
| Export .pbix periodically | Offline backup |

---

## 11. Power BI Embedded & REST API Errors

### ERR-EMBED-001: TokenExpired (403)

**Error Message:**
```
"TokenExpired" / 403 Forbidden
```

**สาเหตุ:** Access token หมดอายุ

**วิธีแก้:**
1. สร้าง token ใหม่ก่อน token เดิมหมดอายุ
2. Implement auto-refresh token logic:
```javascript
// Check token expiry before each API call
if (tokenExpiry < Date.now() + 60000) {
  token = await generateNewToken();
}
```

---

### ERR-EMBED-002: LoadReportFailed (404/403)

**Error Message:**
```
"LoadReportFailed" — Report ID ไม่ถูกต้องหรือไม่มีสิทธิ์
```

**วิธีแก้:**
- 404: ตรวจ Report ID ว่าถูกต้อง + report ยังมีอยู่
- 403: ตรวจ Report ID ตรงกับ workspace ใน token
- ตรวจว่า token scope ถูกต้อง: `https://analysis.windows.net/powerbi/api/.default`

---

### ERR-EMBED-003: CapacityLimitExceeded

**Error Message:**
```
"CapacityLimitExceeded" — Report ไม่สามารถโหลดได้
```

**วิธีแก้:**
1. ตรวจ capacity usage ผ่าน Microsoft Fabric Capacity Metrics app
2. Restart Power BI Service
3. เพิ่ม SKU capacity (A1 → A2 → A3)
4. ลด concurrent users / queries

---

### ERR-EMBED-004: Service Principal 401

**Error Message:**
```
"PowerBINotAuthorizedException" (Status 401)
```

**วิธีแก้:**
1. ตรวจ app registration ใน Microsoft Entra ID
2. เพิ่ม API permissions: `Dataset.ReadWrite.All`, `Report.Read.All`
3. Grant admin consent
4. เพิ่ม Service Principal เป็น workspace member
5. เปิด tenant setting: "Allow service principals to use Power BI APIs"

---

### ERR-EMBED-005: Embed Token Exhausted (Free Capacity)

**Error Message:**
```
"Forbidden" when generating EmbedToken
```

**สาเหตุ:** Free embed token หมด

**วิธีแก้:**
- ซื้อ Premium capacity (P1/EM1/A1+)
- Assign workspace ไปที่ capacity

---

## 12. Export Errors (PDF / PowerPoint / CSV)

### ERR-EXPORT-001: PDF Export Failed

**Error Messages:**
```
"Report can't be exported to PDF"
"Failed to export — 403"
```

**Limits:**
| Limit | ค่า |
|-------|-----|
| Max pages | 50 |
| Max file size | 250 MB |
| Custom fonts | ไม่รองรับ (ใช้ default แทน) |
| External user | ไม่สามารถ export ได้ |

**วิธีแก้:**
1. ลดจำนวนหน้า / แยก report
2. ตรวจ admin settings: "Export reports as PDF" enabled
3. Design report ด้วย print layout
4. ตรวจ WebView2 GPU Process version (PBI Desktop)
5. Custom fonts → จะถูกแทนด้วย default font

---

### ERR-EXPORT-002: PowerPoint Export Issues

**Limits:**
- Export ได้สูงสุด **30 pages** แรก
- Exported slides เป็น **static images** (ไม่ refresh)
- Custom page sizes อาจไม่ fit slide

**วิธีแก้:**
1. ใช้ page size 16:9 (1280×720) ให้ match PowerPoint
2. External users ไม่สามารถ export ได้ → share report access ก่อน
3. Grouped views อาจเลื่อนไปมุมซ้ายบน → ลบ grouping ก่อน export

---

### ERR-EXPORT-003: CSV Export Data Incorrect

**อาการ:**
- Leading zeros หายตอนเปิดใน Excel
- Data ไม่แยก column ถูกต้อง
- Unicode/ภาษาไทย แสดงผิด

**Limits:**
| License | Max Rows |
|---------|----------|
| Free | 30,000 |
| Pro | 150,000 |

**วิธีแก้:**
1. **Excel**: ใช้ Data → From Text/CSV (Power Query) แทนเปิดตรง
2. Matrix visuals → Export จาก Table visual แทน (ง่ายกว่า)
3. Unicode: ใช้ UTF-8 with BOM encoding
4. ตรวจ RLS ไม่ block data export

---

### ERR-EXPORT-004: Admin Disabled Export

**อาการ:** Export options greyed out / ไม่มี

**วิธีแก้:**
- ตรวจ Admin Portal → Tenant Settings → Export and sharing settings
- Settings ที่ต้องเปิด:
  - "Export reports as PDF"
  - "Export reports as PowerPoint presentations"
  - "Allow users to export data from reports"

---

## 13. Subscription & Alert Errors

### ERR-SUB-001: Email ไม่ส่ง / ไม่ได้รับ

**Checklist:**
- [ ] Email ถูกต้อง + มี Exchange license
- [ ] ตรวจ spam/junk folder
- [ ] เพิ่ม `no-reply-powerbi@microsoft.com` เป็น safe sender
- [ ] Subscription enabled + ถูก time zone
- [ ] ถ้า "After data refresh" → ส่งแค่ refresh แรกของวัน

**วิธีแก้เพิ่มเติม:**
- Run data refresh และ subscription คนละเวลา
- ตรวจ Power BI service status page
- Email อาจ delay ถึง 24 ชั่วโมงช่วง peak

---

### ERR-SUB-002: Unsupported Content in Subscription

**ไม่รองรับ:**
- Streaming tiles / Video tiles
- Custom web content tiles
- R/Python/ESRI ArcGIS visuals
- RLS-applied tiles (ไม่แสดง)

**Full Report Attachment conditions:**
- Premium / PPU workspace เท่านั้น
- ≤ 20 pages
- Attachment ≤ 25 MB

---

### ERR-SUB-003: "Something Went Wrong" ตอนสร้าง Subscription

**วิธีแก้:**
- เปลี่ยน Language ใน PBI Service จาก "Browser Language" → เลือกภาษาเฉพาะ
- Settings → General → Language

---

## 14. Composite Model & DirectQuery Errors

### ERR-DQ-001: Query Timeout (4 นาที)

**Error Message:**
```
"The query was cancelled because it exceeded the timeout"
```

**Limits:** Power BI Service = **4 นาที** ต่อ query

**วิธีแก้:**
1. ใช้ Performance Analyzer → หา visual ที่ช้า
2. เพิ่ม Aggregation tables (pre-calculate ใน cache)
3. Optimize source database (indexes, materialized views)
4. ลดขนาด data ผ่าน filters / DirectQuery-specific optimizations
5. ตรวจ Gateway performance + network latency

---

### ERR-DQ-002: Aggregation Proxy Model Not Supported

**Error Message:**
```
"Object 'Partition'. Cannot apply refresh policy"
"Aggregation proxy model not supported"
```

**วิธีแก้:**
1. ลบ native queries ออกจาก imported part ของ model
2. ตรวจ relationships: ต้องเป็น 1:M + uni-directional
3. Dimension tables ใช้ **Dual** storage mode
4. ปิด SSO สำหรับ Import mode aggregation tables
5. ห้ามใช้ Dynamic M Query Parameters กับ Aggregations

---

### ERR-DQ-003: Mixed Storage Mode Issues

**อาการ:** "Limited" relationship warning

**วิธีแก้:**
```
// ✅ ใช้ Dual mode สำหรับ dimension tables
// Model view → table → Storage mode → Dual
// Fact table (DirectQuery) → Dimension (Dual) = ไม่มี limited warning
```

**Best Practice:**
- Import: small dimension tables
- DirectQuery: large fact tables
- Dual: dimension tables ที่เชื่อมทั้ง Import + DirectQuery

---

## 15. Dataflow Errors

### ERR-DF-001: Entity Not Found

**Error Message:**
```
"Entity not found" during dataflow refresh
```

**สาเหตุ:**
- ชื่อ table สะกดผิด / case ไม่ตรง (Delta = case-sensitive)
- Table ถูกลบจาก source
- เชื่อมกับ Lakehouse workspace ผิด

**วิธีแก้:**
1. ตรวจ spelling + casing ของ table names
2. Validate dataflow references ใน PBI Service
3. ตรวจ permissions: Service Principal ต้องมี read access
4. ลอง refresh ทีละ step เพื่อหา step ที่ error

---

### ERR-DF-002: Mashup Error

**Error Message:**
```
"Mashup error" during dataflow refresh
```

**สาเหตุ:**
- Data type mismatch (Date vs DateTime)
- Null values ใน non-nullable columns
- Unsupported column types

**วิธีแก้:**
1. Disable Power Query staging → ลอง refresh ใหม่
2. ใช้ "Keep rows → Keep errors" เพื่อหา rows ที่มีปัญหา
3. แก้ data types ให้ consistent
4. Null handling: `Table.ReplaceErrorValues` / `try...otherwise`

---

### ERR-DF-003: Gateway Sporadic Failures

**อาการ:** Dataflow refresh fail intermittently

**วิธีแก้:**
1. Clear cached files บน gateway machine
2. Restart gateway service
3. อัพเดท gateway เป็น latest version
4. ถ้ายังไม่หาย → contact Microsoft support (อาจเป็น internal bug)

---

## 16. Template (.pbit) Errors

### ERR-PBIT-001: Parameter Required

**Error Message:**
```
"Please enter required parameter values"
```

**วิธีแก้:**
1. อ่าน documentation ที่มากับ template
2. กรอก parameters ให้ครบ (server name, database, file path)
3. ถ้ายัง error → เปิด Power Query Editor → refresh preview ทีละ step
4. Copy T-SQL แล้วทดสอบใน SSMS

---

### ERR-PBIT-002: Template ไม่ reusable

**สาเหตุ:** Parameters hardcode ค่า / ไม่มี parameters

**วิธีสร้าง template ที่ดี:**
```m
// ✅ ใช้ parameters สำหรับทุก connection
let
    Source = Sql.Database(#"ServerName", #"DatabaseName")
in Source
```

**Checklist:**
- [ ] ทุก data source ใช้ parameters
- [ ] Parameters มีชื่อชัดเจน + description
- [ ] ตรวจว่า template เปิดได้บน machine อื่น

---

## 17. Custom Visual Errors

### ERR-CV-001: ไม่สามารถ Import Custom Visual ได้

**Error Message:**
```
"We can't import custom visual object. This may be a temporary problem."
```

**วิธีแก้:**
1. อัพเดท Power BI Desktop → latest version
2. ลอง import จาก `.pbiviz` file โดยตรง (แทน marketplace)
3. ตรวจ internet → whitelist `https://pbivisuals.powerbi.com:443`
4. ลอง account อื่น
5. Set environment variable: `PBI_userFavoriteResourcePackagesEnabled=0` → restart PBI

---

### ERR-CV-002: Custom Visual ไม่ render ตอน Export

**อาการ:** Custom visual แสดงเป็น grey box ใน PDF/PPT export

**Limitations:**
| Visual Type | Export Support |
|-------------|--------------|
| Certified custom visuals | ✅ รองรับ |
| Uncertified custom visuals | ⚠️ อาจไม่แสดง |
| R / Python visuals | ❌ ไม่รองรับ |
| Power Apps visuals | ❌ ไม่รองรับ |
| ESRI ArcGIS | ❌ ไม่รองรับ |

---

### ERR-CV-003: Custom Visual Version Conflict

**อาการ:** Visual render ต่างกันใน Desktop vs Service

**วิธีแก้:**
1. อัพเดท custom visual ทั้ง Desktop + Service ให้ตรงกัน
2. ใน workspace: Manage → Custom visuals → Update
3. Pin version ใน Organizational visuals (Admin Portal)

---

## 18. Fabric / Lakehouse Errors

### ERR-FABRIC-001: Shortcut Permission Error

**อาการ:** ไม่สามารถเข้าถึง data ผ่าน shortcut

**วิธีแก้:**
1. ตรวจ user มีสิทธิ์เข้า **source Lakehouse** (ไม่ใช่แค่ shortcut)
2. ตรวจ shortcut creator มีสิทธิ์เข้า source
3. ห้ามใช้ hyphens (`-`) ในชื่อ → ใช้ underscores (`_`) แทน
4. ถ้า shortcut ไม่แสดงใน SQL Endpoint → ตรวจ permissions ของ creator

---

### ERR-FABRIC-002: Shortcut Data Latency

**อาการ:** Data ใน shortcut ไม่ update

**สาเหตุ:** OneLake caching → periodic snapshots

**วิธีแก้:**
1. ใช้ Direct Query connection แทน
2. Manual refresh cache: `REFRESH <shortcut_name>` ใน Fabric Notebook
3. รอ automatic sync (มี delay ปกติ)

---

### ERR-FABRIC-003: Deployment Pipeline Error

**Error Message:**
```
"Can't complete the deployment. The artifact couldn't be deployed"
```

**วิธีแก้:**
1. ตรวจ artifact ทั้งหมดที่รวมใน deployment
2. Semantic model deploy = **metadata only** → ต้อง manual refresh หลัง deploy
3. ตรวจ gateway connections + credentials ใน target workspace
4. ลบ native queries จาก imported part (proxy model limitation)
5. ตรวจ shortcut references ไม่ชี้ไป workspace ที่ไม่มี

---

### ERR-FABRIC-004: Direct Lake Mode Errors

**อาการ:** Semantic model ไม่สามารถเข้าถึง Lakehouse data

**วิธีแก้:**
1. ตรวจ Lakehouse เชื่อมกับ semantic model ถูกต้อง
2. ตรวจ table format = Delta (ห้ามใช้ Parquet/CSV โดยตรง)
3. ตรวจ user permissions ใน workspace
4. Fallback: ใช้ Import mode ถ้า Direct Lake ไม่รองรับ scenario

---

## 19. Paginated Report Errors

### ERR-PAG-001: Report Processing Error

**Error Message:**
```
"An error has occurred during report processing"
"Cannot read the next data row for the dataset"
```

**วิธีแก้:**
1. Validate RDL schema + expression syntax
2. ถ้าใช้ multiple datasets → ระบุ scope: `=First(Fields!Name.Value, "DataSet1")`
3. Object names: 1-256 characters เท่านั้น
4. ตรวจ data source connectivity + credentials

---

### ERR-PAG-002: DirectQuery Timeout (600s)

**Error Message:**
```
"Error communicating with Analysis Service"
```

**สาเหตุ:** Report ใช้ DirectQuery semantic model + query > 600 วินาที

**วิธีแก้:**
1. ใช้ XMLA endpoint แทน DirectQuery
2. Optimize queries ให้เร็วขึ้น
3. ลด data volume ใน report

---

### ERR-PAG-003: Parameter Conflict

**อาการ:** Report ไม่ render เมื่อใช้ parameters จาก PBI Desktop

**วิธีแก้:**
1. ตรวจ parameter names ตรงกันระหว่าง paginated report + PBI Desktop
2. Hidden parameters ต้องตั้งค่า correctly
3. Allow blank values ถ้า parameter อาจว่าง
4. ตรวจ available values list ไม่ conflict

---

### ERR-PAG-004: RDL Version Incompatibility

**Error Message:**
```
"The definition of this report is not valid"
```

**วิธีแก้:**
- ตรวจว่า RDL version ตรงกับ SSRS server version
- Save as older RDL version ถ้าใช้ older server
- ใช้ Power BI Report Builder (latest) สำหรับ PBI Service

---

## 20. Data Model Relationship Errors

### ERR-REL-001: Many-to-Many Relationship Issues

**อาการ:** Totals ไม่ถูกต้อง / ผลลัพธ์สับสน

**วิธีแก้:**
```
// ❌ BAD — M:M โดยตรง
TableA ←M:M→ TableB

// ✅ GOOD — ใช้ Bridge Table
TableA ←M:1→ BridgeTable ←1:M→ TableB
```

**ขั้นตอน:**
1. สร้าง Bridge Table ที่มี unique values จาก common column
2. สร้าง relationship 1:M จากทั้งสอง table ไปที่ bridge
3. ตรวจว่า totals คำนวณถูกต้อง

---

### ERR-REL-002: Ambiguous Path (Loop)

**Error Message:**
```
"Ambiguous relationship detected between tables"
```

**สาเหตุ:** มี 2+ active relationships ระหว่าง tables สร้าง loop

**วิธีแก้:**
1. Deactivate relationship ที่ไม่จำเป็น
2. ใช้ `USERELATIONSHIP()` ใน DAX เมื่อต้องการ:
```dax
Sales By Ship Date =
CALCULATE(
    SUM(Sales[Amount]),
    USERELATIONSHIP(Sales[ShipDate], Calendar[Date])
)
```
3. Redesign model → Star Schema
4. ใช้ single-directional filtering

---

### ERR-REL-003: Bidirectional Filter — Security Risk

**อาการ:** Data leak ผ่าน bidirectional filter + RLS ไม่ทำงานถูกต้อง

**ความเสี่ยง:**
- สร้าง ambiguous paths → ผลลัพธ์ไม่คาดคิด
- RLS อาจ bypass ผ่าน bidirectional filter routeways
- Performance ลดลงอย่างมาก

**Best Practice:**
1. ใช้ **single-directional** filtering เสมอ (default)
2. Bidirectional ใช้เฉพาะ: role-playing dimensions หรือ bridge tables
3. ทดสอบ RLS ทุกครั้งหลังเพิ่ม bidirectional relationship
4. ใช้ Performance Analyzer ตรวจ impact

---

### ERR-REL-004: Q&A "Couldn't Understand"

**อาการ:** Power BI Q&A ตอบว่า "Sorry, I couldn't understand"

**สาเหตุ:**
- ไม่มี relationships ระหว่าง tables
- ชื่อ table/column ไม่ user-friendly
- ไม่มี synonyms

**วิธีแก้:**
1. Rename tables/columns ให้เป็นภาษา business: `tbl_ord` → `Orders`
2. เพิ่ม Synonyms: Modeling → Q&A → Manage Linguistic Schema
3. Set data types ถูกต้อง (IDs = text, dates = date)
4. ตรวจ relationships ครบ

> ⚠️ **หมายเหตุ:** Power BI Q&A จะ deprecated ใน December 2026 — Microsoft แนะนำ Copilot แทน

---

### ERR-REL-005: Incremental Refresh Policy Error

**Error Messages:**
```
"Before you can set/modify incremental refresh you need to apply pending changes"
"We cannot apply operator < to types Date and Text"
```

**วิธีแก้:**
1. ตรวจ `RangeStart` / `RangeEnd` parameters = DateTime type
2. Data type ต้อง match กับ column ที่ filter
3. Query folding ต้องทำงานได้ (ตรวจ Native Query)
4. ตั้ง report locale ให้ถูกต้อง (ปัญหา date format)
5. Publish model ก่อน → เปิด incremental refresh policy ใน Service

---

## 21. Power BI Desktop Installation & Startup Errors

### ERR-DESKTOP-001: Gray Window / ไม่เปิด

**อาการ:** Power BI Desktop เปิดแล้วจอเทา หรือไม่ตอบสนอง

**สาเหตุหลัก:**
- WebView2 Runtime มีปัญหา
- On-premises Data Gateway เก่าเกินไป
- Antivirus block process

**วิธีแก้:**
1. ตั้ง environment variable:
```
WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS = --disable-features=RendererCodeIntegrity
```
2. Reinstall Microsoft Edge WebView2 Runtime
3. อัพเดท Data Gateway → latest version
4. เพิ่ม Power BI Desktop ใน antivirus exception list
5. Run as Administrator

---

### ERR-DESKTOP-002: Crash ตอนเปิด

**Checklist:**
- [ ] RAM ≥ 1.5 GB (แนะนำ 4 GB+)
- [ ] .NET Framework 4.7 หรือ 4.8 ติดตั้งแล้ว
- [ ] ใช้ 64-bit version (ถ้า OS เป็น 64-bit)
- [ ] Display scaling = 100% (ถ้ามี dialog หาย)

**วิธี Repair:**
1. Settings → Apps → Power BI Desktop → Repair/Reset
2. ถ้ายังไม่หาย: Uninstall → ลบ `%AppData%\Local\Microsoft\Power BI Desktop` → Reinstall
3. ลอง Microsoft Store version แทน .exe installer

---

### ERR-DESKTOP-003: Report Server Version Conflict

**Error:** "ไม่สามารถเปิดไฟล์ .pbix ได้"

**สาเหตุ:** PBI Desktop version ไม่ตรงกับ Report Server release cycle

**วิธีแก้:**
- ใช้ PBI Desktop เฉพาะ version ที่ match กับ Report Server (Jan/May/Sep releases)
- ดาวน์โหลดจาก Report Server portal โดยตรง (ไม่ใช่ Microsoft Store)

---

## 22. XMLA Endpoint Errors

### ERR-XMLA-001: Failed to Connect

**Error Messages:**
```
"Cannot connect to server"
"There was an issue with your workload settings"
```

**Requirements:**
| Item | ค่าที่ต้องการ |
|------|-------------|
| Capacity | Premium (P1+), PPU, หรือ Embedded (A1+) |
| Setting | XMLA endpoint = Read/Write (Admin Portal) |
| Network | Allow `*.pbidedicated.windows.net` |
| Tools | SSMS 18.8+ (เวอร์ชันเก่ามี bug) |

**วิธีแก้:**
1. Admin Portal → Capacity Settings → XMLA Endpoints → Read/Write
2. Tenant setting: "Allow XMLA endpoints" = Enabled
3. ตรวจ firewall/proxy ไม่ block `*.pbidedicated.windows.net`
4. ลด memory ของ Dataflows ถ้า capacity เล็ก (A1)

---

### ERR-XMLA-002: Unsupported Dataset Types

**ไม่รองรับ:**
- Live connection to Azure AS / SQL Server AS
- Live connection to another PBI dataset ใน workspace อื่น
- Push datasets (REST API)
- Excel workbook semantic models

---

## 23. TMDL & Git Integration Errors

### ERR-TMDL-001: Parsing Error / InvalidLineType

**อาการ:** PBI Desktop เปิด TMDL model ไม่ได้

**วิธีแก้:**
1. อัพเดท Tabular Editor → latest version
2. ตรวจ TMDL syntax: indentation, line endings (CRLF vs LF)
3. Validate ด้วย VS Code + TMDL extension
4. Restart PBI Desktop หลังแก้ไขไฟล์ TMDL ภายนอก

---

### ERR-TMDL-002: Git Merge Conflict ใน PBIP

**ไฟล์ที่ conflict บ่อย:**
| ไฟล์ | สาเหตุ |
|------|--------|
| `Measures.tmdl` | PBI reorder measures อัตโนมัติ |
| `model.tmdl` | references เปลี่ยน |
| `report.json` | layout changes (one-line JSON) |

**วิธีป้องกัน:**
1. แยก measures ตาม folder/theme
2. Commit บ่อย + small changes
3. ใช้ `.gitattributes`: `report.json -merge` (force manual merge)
4. Resolve conflicts ด้วย VS Code (Tabular Editor ช่วย validate)
5. **หลัง merge:** Restart PBI Desktop เสมอ

---

## 24. Calculation Group Errors

### ERR-CALC-001: Visual แตกหลังเพิ่ม Calculation Group

**สาเหตุ:** Invalid DAX ใน calculation item / type mismatch

**วิธีแก้:**
1. ตรวจ DAX expression ใน calculation items
2. ใช้ `ISSELECTEDMEASURE()` เพื่อ handle measures ต่าง type:
```dax
// ✅ Handle ทั้ง numeric + text measures
IF(
    ISSELECTEDMEASURE([Text Measure]),
    SELECTEDMEASURE(),
    SELECTEDMEASURE() * 1.1
)
```
3. ตรวจว่า calculation group ถูก refresh หลังแก้ไข

---

### ERR-CALC-002: "Does Not Hold Any Data"

**Error:**
```
"Query referenced Calculation Group Table... does not hold any data"
```

**วิธีแก้:**
1. Process → Recalculate ใน SSMS
2. ถ้ายังไม่หาย → Process Database (Full) ใน SSMS
3. Refresh semantic model ใน PBI Service

---

### ERR-CALC-003: Format String ไม่ทำงาน

**อาการ:** Calculation group ไม่ apply format string ให้ measures จาก PBI Desktop

**วิธีแก้:**
1. ตรวจว่า format string expression ถูกต้อง:
```dax
// ✅ Dynamic format string
SELECTEDMEASUREFORMATSTRING()
```
2. ตรวจ calculation item มี FormatStringExpression property
3. Measures ต้องมี format string ตั้งไว้ก่อน

---

## 25. DAX Format String & Dynamic Format Errors

### ERR-FORMAT-001: FORMAT() Return String (ไม่ใช่ Number)

**อาการ:** Visual ไม่แสดง axis / conditional formatting ไม่ทำงาน

**สาเหตุ:** `FORMAT()` function return **text** เสมอ

**วิธีแก้:**
```dax
// ❌ BAD — returns text, breaks sorting/conditional formatting
Formatted Sales = FORMAT(SUM(Sales[Amount]), "#,##0")

// ✅ GOOD — ใช้ Dynamic Format String (PBI Desktop 2023+)
// Measure: Total Sales = SUM(Sales[Amount])
// Format String Expression: "#,##0"
```

---

### ERR-FORMAT-002: Dynamic Format String ไม่แสดง

**Checklist:**
- [ ] PBI Desktop version ≥ October 2023
- [ ] Enable feature: Options → Preview features → Dynamic format strings
- [ ] Measure มี format string expression ใน Properties
- [ ] ❌ ไม่รองรับใน Excel Pivot Tables (connected to PBI dataset)

---

## 26. Analyze in Excel Errors

### ERR-EXCEL-001: Forbidden (403) ตอนเชื่อม

**สาเหตุ:**
- Login ผิด account (มีหลาย PBI accounts)
- ไม่มี read access ใน workspace
- External user ไม่มี permission

**วิธีแก้:**
1. ใน Excel: File → Account → Sign out → Sign in ด้วย account ที่ถูกต้อง
2. ตรวจ workspace permissions: ต้องมี Viewer+ role
3. On-prem SSAS: user ต้องมี read access ทั้ง PBI + Analysis Services

---

### ERR-EXCEL-002: Measures ไม่แสดงใน PivotTable

**สาเหตุ:** Data model ไม่มี explicit measures

**วิธีแก้:**
1. สร้าง measures ใน PBI Desktop → Publish ใหม่
2. ตรวจว่า dataset ถูก refresh อย่างน้อย 1 ครั้ง

---

### ERR-EXCEL-003: "Unable to obtain list of tables"

**สาเหตุ:** Live connection ไป on-prem SSAS Tabular ผิดวิธี

**วิธีแก้:**
1. ใน PBI Desktop: Get Data → เลือก database จาก list (ไม่ใช่พิมพ์ชื่อ)
2. อัพเดท 64-bit OLE DB driver
3. ตรวจ TLS 1.2 enabled

---

## 27. Streaming & Push Dataset Errors

### ERR-STREAM-001: InvalidJson (400 Bad Request)

**Error:**
```
"RealTime_PushRowsInvalidJson" (400)
```

**วิธีแก้:**
1. ส่ง data เป็น JSON **array** เสมอ:
```json
[{"timestamp": "2026-03-01T12:00:00Z", "value": 42.5}]
```
2. ❌ ห้ามส่งเป็น object เดี่ยว: `{"timestamp": "...", "value": 42.5}`
3. Timestamp ต้องเป็น **string** ถ้าเปิด Historic data

---

### ERR-STREAM-002: API Key Expired (401)

**สาเหตุ:** API key / client secret หมดอายุ (~1 ปี)

**วิธีแก้:**
1. สร้าง client secret ใหม่ใน App Registration
2. อัพเดทค่าใน application ที่ push data
3. ใช้ managed identity แทน (Azure-hosted apps)

---

### ERR-STREAM-003: ไม่มี Fields ตอนสร้าง Report

**อาการ:** Push dataset สร้างแล้ว แต่ไม่มี fields ตอนสร้าง report

**วิธีแก้:**
1. Push data อย่างน้อย 1 row ก่อน
2. ตรวจ dataset schema ถูกต้อง
3. ⚠️ Streaming datasets จะ deprecated ใน October 2027

---

## 28. SharePoint & Teams Embed Errors

### ERR-SP-001: "Report Couldn't Be Loaded"

**Checklist:**
- [ ] Report เปิดได้ปกติใน powerbi.com
- [ ] User มี Pro/PPU license หรือ content อยู่ใน Premium capacity
- [ ] ใช้ embed URL ถูกต้อง (ไม่ใช่ workspace URL)
- [ ] MFA ไม่ block (ลอง login ใหม่)
- [ ] Clear browser cache

---

### ERR-SP-002: Embed Options Greyed Out

**สาเหตุ:** Admin Portal disabled embed features

**วิธีแก้:**
- Admin Portal → Tenant Settings → Enable:
  - "Publish to web"
  - "Embed content in apps"
  - "Allow embedding with SharePoint"

---

### ERR-SP-003: Teams Tab — "Something Went Wrong"

**วิธีแก้:**
1. ตรวจ user sign in ใน PBI Service (ไม่ใช่แค่ Teams)
2. ลอง incognito / browser อื่น
3. เปลี่ยน Language settings ใน PBI Service → เลือกภาษาเฉพาะ
4. Clear Teams cache: `%AppData%\Microsoft\Teams\Cache`

---

## 29. Power BI Copilot Errors

### ERR-COPILOT-001: "Copilot Not Available"

**Requirements:**
| Item | ค่าที่ต้องการ |
|------|-------------|
| Capacity | F64+ / P1+ |
| Admin | Copilot enabled ใน Microsoft Fabric Admin |
| Region | US/France default; อื่นๆ ต้องเปิด cross-geo setting |
| Workspace | ต้อง assign capacity ที่ถูกต้อง |

**วิธีแก้:**
1. Fabric Admin → Copilot → Enable
2. ถ้า tenant อยู่นอก US/France → เปิด "Allow data to be processed outside geo"
3. Save report ไปที่ workspace ที่มี capacity ที่ถูกต้อง

---

### ERR-COPILOT-002: คำตอบไม่ถูกต้อง / Inconsistent

**สาเหตุ:** Data model quality ต่ำ

**วิธีแก้:**
1. Rename tables/columns เป็นภาษา business (ไม่ใช่ `tbl_01`, `col_xyz`)
2. เพิ่ม descriptions ให้ measures + tables
3. ตรวจ relationships ครบ + ถูกต้อง
4. ลด complexity: ลด calculated columns, ใช้ measures แทน

---

### ERR-COPILOT-003: ConnectorRequestFailure (400)

**อาการ:** Copilot Studio เชื่อมกับ PBI dataset ไม่ได้

**วิธีแก้:**
1. ตรวจ dataset อยู่ใน supported format (Import mode)
2. ตรวจ API permissions + service principal
3. ตรวจ network connectivity ระหว่าง Copilot Studio + PBI Service

---

## 30. Datamart & Metrics Scorecard Errors

### ERR-DM-001: Datamart สร้างไม่สำเร็จ

**อาการ:** "Creating Datamart" แล้ว revert กลับ workspace

**วิธีแก้:**
1. ตรวจ license: ต้องมี Premium Per User (PPU) + ใน workspace ที่ถูกต้อง
2. ❌ "My workspace" ไม่รองรับ → สร้าง workspace ใหม่
3. รอ + ลองใหม่ (อาจเป็น temporary service issue)

---

### ERR-DM-002: "Datamart Unavailable"

**Error:**
```
"Datamart is unavailable - Unable to open because it is not connected to its dataset"
```

**วิธีแก้:**
1. ตรวจ dataset ยังอยู่ + accessible
2. Refresh datamart → reconnect
3. ถ้ายังไม่หาย → recreate datamart

---

### ERR-METRICS-001: Scorecard ไม่ Refresh

**อาการ:** Metrics/Goals ไม่ update อัตโนมัติ

**วิธีแก้:**
1. ตรวจ underlying dataset refresh สำเร็จ
2. Manual refresh: เปิด scorecard → refresh individual metric
3. ตรวจ goal correctly bound ไป report visual
4. ⚠️ Known issue (2024): บาง scorecards ไม่ auto-refresh → manual workaround

---

### ERR-METRICS-002: Reports ไม่แสดงใน Connect Dialog

**อาการ:** สร้าง metric ใน scorecard แต่ไม่เห็น reports/apps ให้เชื่อม

**Workaround (April 2024):**
- เพิ่ม `&subfolderInWorkspace=0` ต่อท้าย URL → Reload

---

## 31. Power BI Mobile App Errors

### ERR-MOBILE-001: Report ไม่โหลด / "Content Not Available"

**Checklist:**
- [ ] อัพเดท PBI Mobile app → latest version
- [ ] ตรวจ network connectivity (Wi-Fi / 4G/5G)
- [ ] User มี Pro/PPU license หรือ content อยู่ใน Premium
- [ ] Report ทำงานปกติใน powerbi.com

**วิธีแก้:**
1. Clear app cache → reinstall
2. Sign out → Sign in ใหม่
3. ตรวจ report ใช้ Mobile Layout (PBI Desktop → View → Mobile Layout)
4. ลด complexity ของ visuals (mobile มี processing power จำกัด)

---

### ERR-MOBILE-002: Offline Mode ไม่ทำงาน

**ข้อจำกัด Offline:**
| ไม่รองรับ Offline | เหตุผล |
|-------------------|--------|
| DirectQuery / Live Connection | ต้อง server connection |
| Bing Maps / ArcGIS | ต้อง internet |
| Excel workbooks | ไม่ cache |
| Paginated Reports (RDL) | ไม่รองรับ |
| Interactive slicers/filters | จำกัด |

**Cache limit:** สูงสุด **250 MB** ต่อ device

**วิธีแก้:**
1. เปิด report ขณะ online ก่อน → cache data อัตโนมัติ
2. Background refresh: ทุก 2 ชม. (Wi-Fi) / 24 ชม. (cellular)
3. ใช้ Import mode แทน DirectQuery สำหรับ reports ที่ต้องดู offline

---

### ERR-MOBILE-003: Notifications ไม่ทำงาน (iOS)

**วิธีแก้:**
1. Settings → Power BI → Allow Notifications → ON
2. ปิด Focus Mode
3. Settings → General → Background App Refresh → Power BI → ON

---

## 32. R & Python Visual Errors

### ERR-RPY-001: "R/Python Script Error" / Unable to Start

**สาเหตุหลัก:**
- PBI Desktop หา R/Python installation ไม่เจอ
- Package ที่ต้องการไม่มี
- Antivirus block execution

**วิธีแก้:**
1. Options → R/Python Scripting → ตั้งค่า home directory ให้ถูกต้อง
2. Install packages ที่จำเป็น:
```bash
# Python
pip install pandas matplotlib seaborn

# R
install.packages(c("ggplot2", "dplyr"))
```
3. เพิ่ม R/Python path ใน antivirus exception
4. ⚠️ PBI Service (2025): ต้องใช้ Python 3.11 + R 4.3.3

---

### ERR-RPY-002: Service Sandbox Restrictions

**ข้อจำกัดใน PBI Service:**
| Limit | ค่า |
|-------|-----|
| Timeout | 5 นาที |
| Max rows | 150,000 |
| R output size | 2 MB |
| Internet access | ❌ ไม่อนุญาต |
| File system access | ❌ ไม่อนุญาต |
| External data sources | ❌ ไม่อนุญาต |

**Output:** เป็น **static image** เท่านั้น (ไม่มี tooltips/cross-filter)

---

### ERR-RPY-003: PBI Embedded ไม่รองรับ Python Visuals

**สถานะ:** Python visuals ❌ **ไม่รองรับ** ใน Power BI Embedded

**Workaround:**
- Pre-compute output ภายนอก → แสดงเป็น native visual หรือ static image

---

## 33. Map & Geospatial Visual Errors

### ERR-MAP-001: Map ไม่โหลด / เปิดไม่ได้

**สาเหตุ:** Map visuals ถูก disabled ใน Security settings

**วิธีแก้:**
1. PBI Desktop: File → Options → Security → ✅ "Use Map and Filled Map Visuals"
2. Admin Portal → Tenant Settings → "Map and Filled Map visuals" → Enabled
3. ตรวจ firewall ไม่ block geographic endpoints

---

### ERR-MAP-002: ArcGIS Map Blank / ไม่แสดงข้อมูล

**อาการ:** Map แสดงเป็นว่าง หรือ "This map does not meet the requirements"

**วิธีแก้ (PBI Desktop):**
1. Toggle option ใน Format Visual panel
2. ลบ map visual → Clear cache (`%AppData%\Local\Microsoft\Power BI Desktop\Cache`) → สร้างใหม่
3. อัพเดท PBI Desktop → latest version (Esri fix late 2024)

---

### ERR-MAP-003: Geocoding ไม่ถูกต้อง (Azure Maps)

**อาการ:** ตำแหน่งแสดงผิดประเทศ / ผิดตำแหน่ง

**วิธีแก้:**
1. ตั้ง Data Category ให้ถูกต้อง: Address, City, Country, Latitude, Longitude
2. ใช้ geo-hierarchy (Country → State → City)
3. ให้ข้อมูลครบ: ไม่ใช่แค่ City แต่ต้องมี Country ด้วย
4. ⚠️ Bing Maps จะถูกลบจาก PBI Desktop ตั้งแต่ October 2025 → ย้ายไป Azure Maps

---

## 34. Conditional Formatting Errors

### ERR-CF-001: Rule ไม่ Apply

**สาเหตุ:**
- Data type ไม่ตรง (ใช้ color scale กับ text column)
- Blank values ใน data
- Visual มีมากกว่า 1 measure + legend → ไม่มี fx icon

**วิธีแก้:**
1. ตรวจ data types ถูกต้อง
2. Percentage rules: ใส่เป็น decimal (0.5 ไม่ใช่ 50) + เลือก "Number"
3. ลบ blank values ก่อน apply
4. ถ้า rules conflict → จัดลำดับ priority ใหม่

---

### ERR-CF-002: สีต่างกันใน Desktop vs Service

**สาเหตุ:** Color codes render ต่างกันระหว่าง platforms

**วิธีแก้:**
1. ใช้ HEX codes แทน preset colors
2. ทดสอบใน Service หลัง publish ทุกครั้ง
3. ใช้ measures-based formatting แทน field-based

---

## 35. Bookmarks & Navigation Errors

### ERR-BOOKMARK-001: Bookmark Navigator Highlight ผิด

**อาการ:** Bookmark Navigator แสดง highlight ที่ bookmark เก่า ไม่ใช่ bookmark ปัจจุบัน

**สาเหตุ:** Navigator "จำ" selection เดิม ไม่ reset

**วิธีแก้:**
1. ใช้ individual buttons แทน Bookmark Navigator
2. สร้าง bookmarks ด้วย "Selected Visuals" option (ไม่ใช่ "All Visuals")
3. ​ตั้ง "Current page" bookmark type

---

### ERR-BOOKMARK-002: Bookmark เปลี่ยน Slicer State

**อาการ:** กดเปลี่ยน page แล้ว slicer reset / เปลี่ยนค่า

**วิธีแก้:**
1. สร้าง bookmark: ❌ uncheck "Data" option (เก็บแค่ display state)
2. แยก bookmark groups ตาม page
3. ใช้ "Only Selected Visuals" ไม่ใช่ "All Visuals on this Page"

---

## 36. Drillthrough & Cross-Report Errors

### ERR-DRILL-001: Drillthrough Option ไม่แสดง

**Checklist:**
- [ ] Target page มี drillthrough field ตั้งค่าแล้ว
- [ ] Cross-report drillthrough enabled ใน report settings (ทั้ง source + target)
- [ ] ทั้ง 2 reports อยู่ใน same workspace (ไม่ใช่ "My Workspace")
- [ ] Published เป็น Workspace App
- [ ] Field names + data types ตรงกัน (case-sensitive)
- [ ] User มี Viewer permission ที่ workspace level (ไม่ใช่ link sharing)

---

### ERR-DRILL-002: "Undefined" Page Name

**สาเหตุ:** Bug กับ `.pbip/.pbir` format ใน PBI Service

**วิธีแก้:**
1. รอ fix จาก Microsoft (known bug)
2. Workaround: ใช้ `.pbix` format แทนชั่วคราว

---

### ERR-DRILL-003: Cross-Report ไม่รองรับ Report Server

**สถานะ:** Cross-report drillthrough ❌ **ไม่รองรับ** ใน Power BI Report Server

**Alternative:** ใช้ single-report drillthrough pages แทน

---

## 37. Field Parameters Errors

### ERR-FPARAM-001: Field Parameters ไม่ทำงานหลังอัพเดท

**สาเหตุ:** Preview feature ถูก reset หลัง PBI Desktop update

**วิธีแก้:**
1. File → Options → Preview Features → ✅ Re-enable "Field Parameters"
2. อัพเดท PBI Desktop → latest version
3. ถ้ายังไม่หาย → recreate field parameter table

---

### ERR-FPARAM-002: Numeric Range Parameter ไม่รับค่า

**อาการ:** Input box default กลับไปค่าเริ่มต้น

**สาเหตุ:** Sampling issue เมื่อมีค่ามากเกินไป

**วิธีแก้:**
1. ลดจำนวนค่า (distinct values) ใน column
2. ใช้ What-If parameter แทน
3. ⚠️ "What-If" Parameters ไม่รองรับใน Report Server

---

## 38. Sensitivity Labels & Information Protection Errors

### ERR-LABEL-001: ไม่สามารถ Apply Sensitivity Label

**Requirements:**
| Item | ค่าที่ต้องการ |
|------|-------------|
| License | Azure Information Protection **P1/P2** + Power BI Pro/PPU |
| Migration | Labels ต้อง migrate ไป Microsoft Purview |
| Admin | Labels published ผ่าน Purview compliance portal |

**วิธีแก้:**
1. ตรวจ license assignments ใน Microsoft 365 admin center
2. ตรวจ sensitivity labels ถูก published ให้ user
3. อัพเดท PBI Desktop ≥ December 2020

---

### ERR-LABEL-002: Label แสดงเป็น GUID

**อาการ:** Sensitivity label แสดงเป็น GUID แทนชื่อ

**สาเหตุ:** Receiving tenant ไม่รู้จัก label

**วิธีแก้:**
1. ตรวจ sensitivity label ตรงกันระหว่าง tenants
2. Enable cross-tenant label mapping
3. Re-upload file หลังตั้ง label ใหม่

---

## 39. Licensing Limits & Capacity Errors

### ERR-LIC-001: Feature ไม่พร้อมใช้งาน (Free vs Pro vs PPU)

**Feature Matrix:**
| Feature | Free | Pro | PPU | Premium/Fabric |
|---------|------|-----|-----|----------------|
| View shared content | ✅ (Premium only) | ✅ | ✅ | ✅ |
| Share reports | ❌ | ✅ | ✅ | ✅ |
| XMLA endpoint | ❌ | ❌ | ✅ | ✅ |
| AI features | ❌ | ❌ | ✅ | ✅ |
| Max refreshes/day | 8 | 8 | 48 | 48 |
| Model size limit | 1 GB | 1 GB | 100 GB | 400 GB |

---

### ERR-LIC-002: Premium P-SKU Retirement

**สถานะ:**
- New purchases: หยุดหลัง **July 1, 2024**
- Non-EA renewals: หมดเขต **February 1, 2025**
- ต้อง migrate ไป **Microsoft Fabric F-SKUs**

**F-SKU Viewer License:**
- F64+: Viewers ไม่ต้องมี Pro license
- F32 และต่ำกว่า: Viewers ยังต้องมี Pro license

---

## 40. Power Automate + Power BI Integration Errors

### ERR-PA-001: Refresh Flow "Succeeded" แต่ Data ไม่ Update

**สาเหตุ:** Flow ตรวจแค่ว่า **call ส่งสำเร็จ** ไม่ใช่ **refresh เสร็จ**

**วิธีแก้:**
1. เพิ่ม "Delay" action หลัง trigger refresh
2. ใช้ "Get refresh history" action เพื่อตรวจ status
3. เพิ่ม "Run After" → Configure failure path

---

### ERR-PA-002: "Not API Push Dataset" Error

**Error:**
```
"XYZ is not API Push Dataset"
```

**สาเหตุ:** ใช้ "Add rows" action กับ dataset ที่ไม่ได้สร้างจาก REST API

**วิธีแก้:**
1. สร้าง dataset ผ่าน Power BI REST API (ไม่ใช่จาก PBI Desktop)
2. ใช้ dataflow หรือ scheduled refresh แทน push rows

---

### ERR-PA-003: Trigger ไม่ Fire

**Checklist:**
- [ ] Connection credentials ยังใช้ได้
- [ ] DLP policies ไม่ block flow
- [ ] Service endpoints allowlisted
- [ ] Flow ยัง enabled + ไม่ถูก suspend
- [ ] ตรวจ Power BI Service status page

---

## 41. Power BI Report Server (On-Premises) Errors

### ERR-PBIRS-001: "Unable to Load the Data Model" (500)

**สาเหตุ:** Version mismatch หลังอัพเกรด PBIRS

**วิธีแก้:**
1. ⚠️ ใช้ **PBI Desktop (optimized for Report Server)** เท่านั้น — ไม่ใช่ cloud version
2. เปิดไฟล์ด้วย PBIRS-optimized Desktop → Refresh → Save As → Re-upload
3. ตรวจ custom mashup extensions ว่า compatible กับ version ใหม่

---

### ERR-PBIRS-002: Report ไม่ Render

**Checklist:**
- [ ] ใช้ PBI Desktop version ที่ตรงกับ PBIRS version
- [ ] Third-party drivers ติดตั้ง (32/64-bit ตรง architecture)
- [ ] Memory + disk space เพียงพอ
- [ ] Features ที่ใช้ supported ใน PBIRS (ไม่ใช่ทุก feature จาก cloud)

**Logging:**
```
แก้ไข ReportingServicesService.exe.config → เปิด verbose logging
```

---

## 42. Data Gateway Errors (Deep Dive)

### ERR-GW-001: "Gateway Offline"

| ประเภท Gateway | สาเหตุ | วิธีแก้ |
|----------------|--------|---------|
| **Personal** | เครื่องปิด / user ไม่ login | เปิดเครื่อง + login ตลอดเวลา หรือ ย้ายไป Enterprise |
| **Enterprise** | Service ไม่ทำงาน | เปิด On-premises Gateway app → Start service |
| **ทุกประเภท** | Gateway version เก่า | อัพเดท → last 6 releases เท่านั้นที่ support |
| **ทุกประเภท** | Resource ไม่พอ (CPU/RAM/Disk) | Monitor resource → scale up server |

**Ports ที่ต้องเปิด:** `servicebus.windows.net` → ports **80, 443**

---

### ERR-GW-002: "Invalid Connection Credentials"

**วิธีแก้:**
1. PBI Service → Dataset Settings → Manage Data Sources → **Edit Credentials**
2. ตรวจ OAuth2 token ไม่ expired
3. ชื่อ Server + Database ใน Desktop ต้อง **ตรงกัน** กับใน Gateway (IP ก็ต้องตรง)
4. ตรวจ user อยู่ใน "Users" tab ของ data source

---

### ERR-GW-003: "DM_GWPipeline_Gateway_DataSourceAccessError"

**สาเหตุ:** Personal Mode connection ถูกสร้างอัตโนมัติหลัง publish → แสดง "Offline"

**วิธีแก้:**
1. ลบ personal mode data source ที่ไม่ได้ใช้
2. Reconfigure เป็น enterprise gateway data source
3. อัพเดท gateway → latest version

---

## 43. Query Folding Errors

### ERR-FOLD-001: Query ไม่ Fold (Performance ช้า)

**สาเหตุที่ Query ไม่ Fold:**
| ปัจจัย | คำอธิบาย |
|--------|----------|
| Unsupported M function | ไม่มี native SQL equivalent |
| Step order ผิด | Non-foldable step อยู่ก่อน foldable steps |
| Custom SQL ("black box") | Power BI ไม่สามารถ optimize ต่อ |
| ผสม data sources | Merge/Append ต่าง sources → local processing |
| Privacy levels | ถูก block โดย privacy settings |

**วิธีตรวจ:**
1. Right-click step ใน Power Query → "View Native Query"
2. ถ้า greyed out = **ไม่ fold**

**วิธีแก้:**
1. จัดลำดับ steps: foldable steps ก่อน
2. ใช้ `Value.NativeQuery(..., [EnableFolding=true])` สำหรับ native queries
3. ทำ transformation ใน database view แทน Power Query
4. ⚠️ Native queries ไม่รองรับ Incremental Refresh

---

## 44. Report Theme & JSON Errors

### ERR-THEME-001: "Invalid Theme" เมื่อ Import JSON

**สาเหตุ:** JSON ไม่ตรง schema / syntax error

**วิธีแก้:**
1. Validate JSON ด้วย [jsonlint.com](https://jsonlint.com)
2. ใช้ VS Code + PBI Theme Schema สำหรับ autocompletion
3. ลบ properties ที่ outdated (schema เปลี่ยนทุกเดือน)
4. ใช้ Theme Generator tool (PowerBI.Tips / BIBB)

---

### ERR-THEME-002: Theme ไม่ Apply กับ Existing Visuals

**สาเหตุ:** Manual overrides → individual visual settings ทับ theme

**วิธีแก้:**
1. Reset visuals → default settings ก่อน apply theme ใหม่
2. ใช้ `dataColors` array ให้ครบ (ถ้ามี 60+ legend items → ต้องกำหนด 60+ colors)
3. Save theme เป็น custom theme → ป้องกัน updates revert

---

## 45. Slicer Sync & Cross-Page Filter Errors

### ERR-SLICER-001: Slicer ไม่ Sync ข้ามหน้า

**สาเหตุ:** "New slicer" element มี sync bugs (2024)

**วิธีแก้:**
1. View → Sync Slicers pane → ตั้ง visibility + sync ต่อ page
2. ตรวจ Selection Pane → ไม่มี hidden synced slicers ที่ซ่อนอยู่
3. ถ้ายังมีปัญหา → recreate slicer ใหม่
4. ตรวจ custom theme ไม่ conflict กับ slicer formatting

---

### ERR-SLICER-002: Cross-Filter ทำงานใน Desktop แต่ไม่ทำงานใน Service

**วิธีแก้:**
1. ตรวจ dataset + report ถูก refresh ใน Service
2. ใช้ "Edit Interactions" ตั้งค่า filter/highlight behavior
3. สร้าง dedicated filter page ด้วย synced slicers

---

## 46. Dashboard & Pinned Tile Errors

### ERR-TILE-001: Tile ไม่ Refresh / แสดงข้อมูลเก่า

**สาเหตุ:** Pinned tiles = **static snapshots** ณ เวลาที่ pin

**วิธีแก้:**
1. ใช้ **Live Tile** (pin entire report page) แทน pin individual visual
2. ตั้ง tile refresh frequency สำหรับ DirectQuery/Live Connection
3. ตรวจ scheduled refresh ยังทำงาน (ถ้า fail 4 ครั้ง → PBI disable auto)
4. Force refresh: Update credentials → `https://app.powerbi.com?alwaysPromptForContentProviderCreds=true`

---

### ERR-TILE-002: Custom Visual Tile ไม่โหลด

**สาเหตุ:** Service ไม่ access `pbivisuals.powerbi.com` ได้

**วิธีแก้:**
1. ตรวจ internet connectivity
2. เพิ่ม `pbivisuals.powerbi.com` ใน firewall allowlist

---

## 47. RLS & OLS (Security) Errors

### ERR-RLS-001: RLS ไม่ทำงาน / User เห็นข้อมูลทั้งหมด

**Checklist:**
- [ ] RLS roles + filters configured ใน Desktop
- [ ] Users assigned ให้ roles ใน Service (Dataset Settings → Security)
- [ ] Permissions ไม่ conflict (Member → Viewer ต้อง remove + re-add)
- [ ] Dataset refreshed หลัง publish
- [ ] App permissions updated + published
- [ ] User มี Pro license หรืออยู่ใน Premium workspace

**⚠️ Permission change delay:** อาจใช้เวลา **24-48 ชม.** กว่าจะมีผล

---

### ERR-OLS-001: "Cannot Load Model" เมื่อใช้ OLS + RLS

**สาเหตุ:** ใช้ RLS + OLS ใน **separate roles** → conflict

**วิธีแก้:**
1. ✅ Configure RLS + OLS ใน **single role** เดียวกัน
2. OLS ใช้ได้เฉพาะ **Viewer** role เท่านั้น (Admin/Member/Contributor ไม่ affected)
3. ⚠️ OLS ไม่รองรับ: Quick Insights, Smart Narratives, Excel Data Types

---

## 48. AI Visual Errors (Key Influencers / Decomposition Tree)

### ERR-AI-001: Key Influencers ผลลัพธ์ไม่น่าเชื่อถือ

**Requirements:**
| Condition | ค่าแนะนำ |
|-----------|---------|
| Min rows | **10,000+** |
| Categories | ต้อง standardize (USA ≠ United States) |
| Missing values | ลดให้น้อยที่สุด |

**ข้อจำกัด:**
- ❌ ไม่รองรับ DirectQuery / Live Connection to SSAS
- ❌ ไม่รองรับ Field Parameters
- ❌ ไม่รองรับ Publish to Web / SharePoint embed

---

### ERR-AI-002: Decomposition Tree "Couldn't Load Data"

**ข้อจำกัด:**
| Limit | ค่า |
|-------|-----|
| Max levels | 50 |
| Max data points | 5,000 |
| AI Splits support | ❌ ไม่รองรับ Azure AS, PBIRS, Publish to Web |

**วิธีแก้:**
1. ลดข้อมูลด้วย filters
2. Reset report → default → refresh
3. จำกัด AI visuals ≤ **2-3 ตัวต่อ page**

---

## 49. Workspace Management Errors

### ERR-WS-001: "Failed to Create Workspace"

**สาเหตุ:** Workspace creation ถูก disable ที่ tenant level

**วิธีแก้:**
1. Admin Portal → Tenant Settings → **"Create workspaces"** → Enabled
2. ตรวจ user/security group อยู่ใน allow list
3. API: ต้อง enable ใน Admin Portal + Service Principal มี permissions
4. Premium workspace: ต้อง Tenant Admin role

---

### ERR-WS-002: "403 Forbidden" จาก API

**สาเหตุ:** Service Principal ไม่มี permissions

**วิธีแก้:**
1. Admin Portal → Tenant Settings → Enable "Allow service principals to use Power BI APIs"
2. เพิ่ม Service Principal ใน security group ที่ allowed
3. ตรวจ API permissions ใน Azure AD app registration

---

## 50. Tooltip Page & Custom Connector Errors

### ERR-TOOLTIP-001: Tooltip ไม่แสดง

**Checklist:**
- [ ] Page Settings → ✅ "Allow use as tooltip" enabled
- [ ] Tooltip page ไม่ complex เกินไป (load time)
- [ ] PBI Desktop อัพเดท latest version
- [ ] Clear browser cache (สำหรับ Service)

**⚠️ Known:** Tooltip ทำงานปกติใน Desktop แต่ไม่แสดงใน Service (known issue)

---

### ERR-CONNECTOR-001: Custom Connector ทำงานใน Desktop แต่ Fail ใน Service

**Checklist:**
- [ ] `TestConnection` function implemented ใน `.pq` file
- [ ] OAuth `state` parameter passed ใน `StartLogin`
- [ ] `.mez` file unblocked (file properties)
- [ ] Data Extensions security → ไม่ block custom connectors

**Error: "Description must be written in English"**
→ ลบ **special characters** (parentheses) ออกจาก description

---

### ERR-CONNECTOR-002: "Failed to Provision Compute for Custom Code"

**สาเหตุ:** Cloud backend ไม่สามารถ provision function app

**วิธีแก้:**
1. รอ + retry (อาจเป็น transient)
2. ตรวจ Azure subscription ไม่มี restrictions
3. Contact Microsoft support (อยู่นอก scope ปกติ)

---

## 51. Auto Page Refresh Errors

### ERR-APR-001: Auto Page Refresh ไม่ทำงาน

**Requirements:**
| Condition | ต้องมี |
|-----------|--------|
| Data source | **DirectQuery** หรือ Mixed Mode เท่านั้น (❌ Import ไม่รองรับ) |
| Minimum interval | 30 วินาที (Premium), 5 นาที (Pro) |
| Capacity | ต้อง enable ใน Admin Portal |

**สาเหตุ:**
- Page Refresh option หายไปหลังอัพเดท Desktop → UI change / bug
- Visuals แสดง error หลังผ่านไป 30 นาที (known issue กับ SSAS connection)

**วิธีแก้:**
1. ตรวจ data source = DirectQuery
2. Admin Portal → Tenant Settings → Enable "Automatic page refresh"
3. ตั้ง interval ไม่ต่ำกว่า minimum
4. อัพเดท PBI Desktop → latest version

---

### ERR-APR-002: "DataFormat.Error: The specified package is invalid"

**สาเหตุ:** SharePoint connection เสียหายระหว่าง auto refresh

**วิธีแก้:**
1. ตรวจ SharePoint URL / permissions ยังถูกต้อง
2. Re-authenticate credentials ใน Service
3. ถ้า fail 4 ครั้งติด → PBI จะ **disable scheduled refresh** → ต้อง fix แล้ว re-enable

---

## 52. Composite Model & Hybrid Table Errors

### ERR-COMPOSITE-001: Mixed Mode ไม่ทำงานข้าม Data Sources

**สาเหตุ:** Import + DirectQuery ต่าง sources ต้อง gateway mapping

**วิธีแก้:**
1. ตั้ง gateway สำหรับ on-premises data sources
2. ตรวจ "Enhanced Compute" สำหรับ dataflows → ตั้ง **"On"** (ไม่ใช่ "Optimize")
3. ⚠️ Power BI Desktop update อาจเปลี่ยน DirectQuery → Import silently → ตรวจ storage mode

---

### ERR-COMPOSITE-002: Hybrid Table ไม่ Refresh ถูกต้อง

**สาเหตุ:** Partitions (Import + DirectQuery) มี configuration conflict

**วิธีแก้:**
1. ใช้ Incremental Refresh + real-time data เฉพาะ SQL/Oracle/Teradata
2. ตรวจ partition policies ใน Tabular Editor
3. ⚠️ Hybrid tables ไม่รองรับ Incremental Refresh ในทุก scenario

---

## 53. Smart Narrative Errors

### ERR-NARRATIVE-001: Smart Narrative ไม่สร้างข้อความ

**Unsupported Visuals:**
- ❌ Tabular visuals เท่านั้น (ต้องมี chart ด้วย)
- ❌ R/Python visuals, custom visuals, map visuals
- ❌ Multi-row cards > 3 categorical fields
- ❌ Cards ที่มี non-numeric measures

**วิธีแก้:**
1. เพิ่ม chart visual (bar, line, etc.) ร่วมกับ tabular
2. ถ้า fields ใหม่ไม่ถูก detect → ปิด/เปิด Q&A feature
3. Reinstall PBI Desktop ถ้า Smart Narrative visual หายไป

---

### ERR-NARRATIVE-002: "Smart Narratives feature is not supported"

**สาเหตุ:** Rendering problem ใน Power BI Service

**วิธีแก้:**
1. Clear browser cache → reload
2. ตรวจ Power BI Service ไม่มี outage
3. ลองใน Incognito/Private mode

---

## 54. Anomaly Detection Errors

### ERR-ANOMALY-001: "No Anomalies Found" (แต่ควรมี)

**Requirements:**
| Condition | ต้องมี |
|-----------|--------|
| Visual type | **Line chart** เท่านั้น |
| Axis | Time series data (date/datetime) |
| Min data points | **≥ 4** |
| Data | ❌ ไม่รองรับ Legend, multiple values, secondary axis |

**วิธีแก้:**
1. ตรวจ visual = line chart + date on X-axis
2. ❌ อย่าใช้ Date Hierarchy → ใช้ raw date column
3. ปรับ **Sensitivity** ขึ้น → detect anomalies มากขึ้น
4. ตรวจข้อมูลเพียงพอ (30+ time periods แนะนำ)

---

## 55. Forecasting Errors

### ERR-FORECAST-001: "To forecast, data cannot have empty values"

**สาเหตุ:** Blank rows จาก YTD measures / Date table ไม่ครบ

**วิธีแก้ DAX:**
```dax
// เพิ่ม filter ป้องกัน blank
Sales YTD = 
CALCULATE(
    [Total Sales],
    DATESYTD('Calendar'[Date]),
    'Calendar'[Date] <> BLANK()
)
```

---

### ERR-FORECAST-002: Forecast ไม่แสดง

**สาเหตุ:**
- X-axis ใช้ month part แทน full date
- Data gaps / outliers ทำให้ model ไม่ reliable

**วิธีแก้:**
1. ใช้ **full date column** หรือ complete date hierarchy บน X-axis
2. จัดการ missing dates ให้ต่อเนื่อง
3. ตรวจ forecast parameters: length, confidence interval, seasonality

---

## 56. Data Alerts Errors

### ERR-ALERT-001: Data Alert ไม่ส่ง Notification

**Requirements:**
| Condition | ต้องมี |
|-----------|--------|
| License | **Pro** หรือ Premium workspace |
| Visual type | Gauge, KPI, หรือ Card เท่านั้น |
| Data type | **Numeric** เท่านั้น (❌ date/time) |
| Data | ต้อง **refreshed** (ไม่ใช่ static) |
| Max alerts | 250 alerts per user |

**สาเหตุ:**
- Data ไม่เปลี่ยนแปลง → alert ไม่ trigger ซ้ำ
- SharePoint List = source → ทำให้ refresh มีปัญหา

**วิธีแก้:**
1. ตรวจ visual type = gauge/KPI/card + numeric
2. ตรวจ data refresh ทำงานปกติ
3. Streaming datasets → alert ใช้ได้เฉพาะ pinned to dashboard
4. SharePoint: re-download .pbix → refresh Desktop → republish

---

## 57. External Tools Errors (DAX Studio / Tabular Editor)

### ERR-EXTOOL-001: External Tool "Failed to Connect"

**Checklist:**
- [ ] PBI Desktop เปิดอยู่ + มี loaded data model
- [ ] `.pbitool.json` อยู่ใน `C:\Program Files (x86)\Common Files\Microsoft Shared\Power BI Desktop\External Tools`
- [ ] Restart PBI Desktop หลัง install tool ใหม่
- [ ] ลอง Run as Administrator
- [ ] PBI Desktop ไม่ใช่ "for Report Server" version (ไม่มี External Tools ribbon)

---

### ERR-EXTOOL-002: External Tools Ribbon Grayed Out

**วิธีแก้:**
1. อัพเดท PBI Desktop + external tool → latest versions
2. Tabular Editor: Preferences → ✅ "Allow unsupported Power BI features"
3. ตรวจ `.pbitool.json` path ถูกต้อง (ถ้าติดตั้ง custom drive)

---

### ERR-EXTOOL-003: XMLA Connection 500 Error จาก Service

**สาเหตุ:** SQL latency/timeout, insufficient permissions

**วิธีแก้:**
1. ตรวจ user มี **Build** permission สำหรับ semantic model
2. Workspace ต้อง Premium (XMLA endpoint)
3. Enable "Connect to external semantic models" ใน Desktop preview settings

---

## 58. Large Dataset & Memory Errors

### ERR-MEM-001: "Out of Memory" เมื่อ Refresh

**Size Limits:**
| License | Max Dataset Size |
|---------|-----------------|
| Pro | **1 GB** |
| Premium (per user) | **10 GB** (.pbix) |
| Premium (capacity) | **10 GB** default, ปรับได้ถึง 400 GB |

**วิธีแก้:**
1. ลด data volume: ลบ columns/tables ที่ไม่ใช้
2. ใช้ **Incremental Refresh** → ไม่ load historical ทั้งหมดทุกครั้ง
3. ย้ายไป **DirectQuery/Live Connection** สำหรับ dataset ใหญ่มาก
4. Simplify Power Query → ลด complex merges
5. Premium: เพิ่ม capacity tier

---

### ERR-MEM-002: VertiPaq Memory ใช้เกิน

**วิธีแก้:**
1. DAX Studio → VertiPaq Analyzer → หา columns ที่ใช้ memory มาก
2. Process Defrag → rebuild dictionaries
3. ปิด/เปิด .pbix → reset memory allocation
4. ลดรายละเอียด high-cardinality columns

---

## 59. Accessibility / Narrator Errors

### ERR-A11Y-001: Screen Reader ไม่อ่าน Visual Data

**สาเหตุ:** Missing alt text / visual ไม่มี data table

**วิธีแก้:**
1. เพิ่ม **Alt Text** ให้ทุก visual (Format → General → Alt Text)
2. Enable "Show data table" สำหรับ visuals ที่สำคัญ
3. ใช้ **Tab Order** (View → Selection Pane) จัดลำดับ keyboard navigation
4. ตรวจ color contrast ratio ≥ **4.5:1** (WCAG AA)

---

### ERR-A11Y-002: Keyboard Navigation ไม่ทำงาน

**วิธีแก้:**
1. Selection Pane → จัด tab order ให้ logical
2. ❌ ห้ามใช้ overlapping visuals → ทำให้ tab skip
3. ทดสอบด้วย Narrator (Windows) หรือ NVDA

---

## 60. Visual Interaction & Cross-Highlight Errors

### ERR-INTERACT-001: Visual ไม่ Filter/Highlight อีก Visual

**สาเหตุ:** Edit Interactions ถูกตั้งเป็น "None"

**วิธีแก้:**
1. Format → Edit Interactions → เลือก Filter / Highlight / None ต่อ visual pair
2. ตรวจว่า visual ใช้ fields จาก table เดียวกัน (มี relationship)
3. ⚠️ Some visual types ไม่รองรับ cross-highlighting

---

### ERR-INTERACT-002: Cross-Filter ทำงานผิดทิศทาง

**สาเหตุ:** Bidirectional filtering ใน relationships

**วิธีแก้:**
1. Model View → ตรวจ relationship direction
2. ใช้ Single direction แทน Both เมื่อเป็นไปได้
3. ตั้ง "Apply security filter in both directions" เฉพาะที่จำเป็นเท่านั้น

---

## 🔍 Quick Lookup Table (Full — 60 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "ambiguous column" | ERR-DAX-002 |
| "division by zero" | ERR-DAX-003 |
| "can't display" | ERR-VIS-001 |
| "too many values" | ERR-VIS-002 |
| "credentials expired" | ERR-REFRESH-002 |
| "gateway timeout" | ERR-REFRESH-001 |
| "access denied" / publish | ERR-PUB-001 |
| "Expression.Error" | ERR-PQ-001 |
| "DataFormat.Error" | ERR-PQ-002 |
| "DataSource.Error" | ERR-PQ-003 |
| "file corrupted" | ERR-FILE-001 |
| "invalid JSON" | ERR-PBIP-004 |
| "model.bim missing" | ERR-PBIP-002 |
| "RLS" / "row level" | ERR-RLS-001 |
| "OLS" / "object level" | ERR-OLS-001 |
| "slow" / "performance" | PERF-001 |
| "config stringify" | ERR-GEN-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "CapacityLimitExceeded" | ERR-EMBED-003 |
| "Service Principal" 401 | ERR-EMBED-004 |
| "export PDF" failed | ERR-EXPORT-001 |
| CSV data incorrect | ERR-EXPORT-003 |
| subscription ไม่ส่ง email | ERR-SUB-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| "aggregation proxy" | ERR-DQ-002 |
| "entity not found" dataflow | ERR-DF-001 |
| "mashup error" | ERR-DF-002 |
| "parameter required" .pbit | ERR-PBIT-001 |
| custom visual import fail | ERR-CV-001 |
| shortcut permission | ERR-FABRIC-001 |
| deployment pipeline error | ERR-FABRIC-003 |
| paginated "processing error" | ERR-PAG-001 |
| "many-to-many" relationship | ERR-REL-001 |
| "ambiguous path" loop | ERR-REL-002 |
| bidirectional filter risk | ERR-REL-003 |
| mobile "content not available" | ERR-MOBILE-001 |
| R/Python script error | ERR-RPY-001 |
| map ไม่โหลด | ERR-MAP-001 |
| ArcGIS blank | ERR-MAP-002 |
| conditional formatting ไม่ apply | ERR-CF-001 |
| bookmark highlight ผิด | ERR-BOOKMARK-001 |
| drillthrough ไม่แสดง | ERR-DRILL-001 |
| field parameter ไม่ทำงาน | ERR-FPARAM-001 |
| sensitivity label GUID | ERR-LABEL-002 |
| Pro vs PPU limits | ERR-LIC-001 |
| Power Automate refresh | ERR-PA-001 |
| Report Server 500 | ERR-PBIRS-001 |
| gateway offline | ERR-GW-001 |
| invalid credentials gateway | ERR-GW-002 |
| query ไม่ fold | ERR-FOLD-001 |
| "invalid theme" JSON | ERR-THEME-001 |
| theme ไม่ apply | ERR-THEME-002 |
| slicer sync ข้ามหน้า | ERR-SLICER-001 |
| tile ไม่ refresh | ERR-TILE-001 |
| Key Influencers ไม่น่าเชื่อถือ | ERR-AI-001 |
| Decomposition Tree error | ERR-AI-002 |
| workspace สร้างไม่ได้ | ERR-WS-001 |
| API 403 workspace | ERR-WS-002 |
| tooltip ไม่แสดง | ERR-TOOLTIP-001 |
| custom connector fail | ERR-CONNECTOR-001 |
| auto page refresh ไม่ทำงาน | ERR-APR-001 |
| "package is invalid" | ERR-APR-002 |
| mixed mode / composite model | ERR-COMPOSITE-001 |
| hybrid table refresh | ERR-COMPOSITE-002 |
| smart narrative ไม่สร้าง | ERR-NARRATIVE-001 |
| anomaly detection ไม่พบ | ERR-ANOMALY-001 |
| forecast "empty values" | ERR-FORECAST-001 |
| data alert ไม่ส่ง | ERR-ALERT-001 |
| external tool connect fail | ERR-EXTOOL-001 |
| tools ribbon grayed out | ERR-EXTOOL-002 |
| "out of memory" | ERR-MEM-001 |
| VertiPaq memory | ERR-MEM-002 |
| screen reader / alt text | ERR-A11Y-001 |
| keyboard navigation | ERR-A11Y-002 |
| visual interaction ไม่ filter | ERR-INTERACT-001 |
| cross-filter ผิดทิศ | ERR-INTERACT-002 |

---

## 61. REST API Errors

### ERR-API-001: "Unauthorized" (401/403) จาก REST API

**Checklist:**
- [ ] Access token ยัง valid (ไม่ expired)
- [ ] Azure AD app มี permission scopes ที่ต้องการ + **Admin consent granted**
- [ ] Service Principal อยู่ใน Azure AD security group
- [ ] Admin Portal → "Allow service principals to use read-only admin APIs" → Enabled
- [ ] User/SP มี Admin/Contributor access ใน target workspace

**วิธีแก้:**
1. Implement **token refresh** logic ก่อน expiry
2. ใช้ Authorization Code flow สำหรับ `myorg` operations (ไม่ใช่ Client Credentials)

---

### ERR-API-002: "Too Many Requests" (429 Rate Limit)

**วิธีแก้:**
1. อ่าน `Retry-After` header → รอตาม duration
2. ใช้ **Exponential Backoff** strategy
3. Monitor `X-RateLimit-Remaining` header
4. Batch requests แทน single calls
5. ใช้ **Scanner API** สำหรับ metadata จำนวนมาก
6. ลด polling frequency (1 min → 10 min)

---

## 62. PowerShell Cmdlets Errors

### ERR-PS-001: Get-PowerBIWorkspace "Unauthorized"

**สาเหตุ:** ต้อง PBI Admin account สำหรับ organizational scope

**วิธีแก้:**
1. `Login-PowerBIServiceAccount` ด้วย **PBI Admin** account
2. ตรวจ authentication method ถูกต้อง
3. ทดสอบใน clean session: `powershell -noprofile`

---

### ERR-PS-002: New-PowerBIWorkspace "BadRequest" (400)

**สาเหตุ:** Workspace ชื่อซ้ำ / SP ไม่มี permissions

**วิธีแก้:**
1. ใช้ชื่อ workspace ที่ unique
2. ตรวจ Service Principal permissions
3. อัพเดท PowerShell modules: `Update-Module MicrosoftPowerBIMgmt`

---

## 63. Template App Publishing Errors

### ERR-TAPP-001: "Failed to Publish App"

**สาเหตุ:**
- Lingering metadata references จาก deleted reports
- Invalid identities ใน audience/contact lists
- Data model > 1 GB (Pro license)

**วิธีแก้:**
1. ลบ orphaned content จาก workspace + app
2. Validate audience/contact lists → ลบ invalid identities
3. ใช้ Premium license สำหรับ models > 1 GB
4. ใช้ REST API/PowerShell ลบ stuck artifacts

---

### ERR-TAPP-002: Template App Update ล้มเหลว

**วิธีแก้:**
1. "There has been an issue modifying the template application" → ลอง recreate app ใหม่
2. ตรวจ paginated report dependencies ถูกต้อง
3. Contact support ถ้า error ยังคงอยู่

---

## 64. What-If Parameter Errors

### ERR-WHATIF-001: What-If Parameter ไม่ทำงาน

**สาเหตุ:**
| ปัญหา | วิธีแก้ |
|--------|---------|
| Data type ผิด (integer แทน decimal) | ตั้ง data type ให้ตรง |
| ใช้ใน calculated column | เปลี่ยนเป็น **measure** แทน |
| Hidden slicers ซ่อนอยู่ | ตรวจ Selection Pane |
| PBIRS ไม่รองรับ | ใช้ใน Desktop/Service เท่านั้น |

**⚠️ DAX Limitation:** What-If values อาจไม่ทำงานร่วมกับ `IF`/`SWITCH` สำหรับ dynamic x-axis

---

## 65. Date / Calendar Table Errors

### ERR-DATE-001: CALENDARAUTO() Error

**สาเหตุ:**
- Model มีแค่ date table เดียว (ไม่มี data tables อื่น)
- ไม่มี date columns ใน model

**วิธีแก้:**
1. Import data tables ก่อนสร้าง date table
2. ใช้ `CALENDAR(DATE(2020,1,1), DATE(2025,12,31))` แทน CALENDARAUTO

---

### ERR-DATE-002: Relationship กับ Date Table ไม่ทำงาน

**สาเหตุ:** Data type mismatch (Date vs DateTime vs Text)

**วิธีแก้:**
1. เปลี่ยน data type **ใน Power Query** (ไม่ใช่ Data View)
2. ✅ "Mark as Date Table" สำหรับ custom date tables
3. ⚠️ ปิด "Auto Time Intelligence" ถ้าใช้ custom date table

---

## 66. Usage Metrics Report Errors

### ERR-USAGE-001: Usage Metrics Report ว่างเปล่า

**วิธีแก้:**
1. ตรวจ dataset refresh ทำงาน
2. Clear browser/Desktop cache
3. อัพเดท PBI Desktop → latest version
4. ลองสร้าง Usage Metrics report ใหม่ (ลบ dataset เก่า)

---

### ERR-USAGE-002: "This usage report will be retired in 2024"

**สาเหตุ:** ข้อความหมายถึง **Admin Portal dashboard** ที่ retire (ไม่ใช่ทุก usage report)

**วิธีแก้:**
1. ใช้ **Admin Monitoring Workspace** แทน Admin Portal dashboard
2. ignore ข้อความนี้สำหรับ workspace-level usage reports

---

## 67. Connector-Specific Errors (SAP / Oracle / Snowflake / Databricks)

### ERR-SAP-001: "One or more additional components required" (SAP HANA)

**วิธีแก้:**
1. ติดตั้ง **SAP HANA ODBC Driver** (64-bit ตรงกับ PBI Desktop)
2. ตรวจ user privileges ใน HANA view
3. Reinstall PBI Desktop ถ้ายังมีปัญหา

---

### ERR-ORACLE-001: "No ODAC driver is found"

**วิธีแก้:**
1. ติดตั้ง **Oracle Instant Client** (64-bit) + ODAC
2. Configure `TNSNAMES.ORA` ให้ถูกต้อง
3. ⚠️ ดาวน์โหลด PBI Desktop จาก **Download Center** (ไม่ใช่ Microsoft Store)
4. Enable "Configure ODP.NET and/or Oracle Providers for ASP.NET" ตอนติดตั้ง

---

### ERR-SNOW-001: Snowflake Driver Mismatch

**Error:** `'Simba Snowflake ODBC Driver' does not match an installed ODBC driver`

**วิธีแก้:**
1. Reinstall PBI Desktop (โดยเฉพาะ Microsoft Store version)
2. ปิด "Use new Snowflake connector implementation" preview
3. Service: เพิ่ม **Azure Public IP ranges** ใน Snowflake network policy
4. ตรวจ OAuth EMAIL_ADDRESS unique

---

### ERR-DATABRICKS-001: "Databricks ODBC driver is not installed"

**สาเหตุ:** PBI Desktop update (Aug-Sep 2024) ทำให้ driver หาย

**วิธีแก้:**
1. Reinstall PBI Desktop
2. ลอง previous version ของ PBI Desktop
3. Manual install Databricks ODBC driver
4. ตรวจ SSL + firewall settings

---

## 68. Lineage & Impact Analysis Errors

### ERR-LINEAGE-001: Lineage View ไม่แสดง Items ทั้งหมด

**สาเหตุ:** "Limited access" items ไม่แสดงแม้เป็น tenant admin

**วิธีแก้:**
1. ใช้ **Power BI REST API** + PowerShell สำหรับ tenant-wide lineage
2. ใช้ **Log Analytics integration** สำหรับ detailed telemetry
3. ⚠️ Built-in lineage view มีข้อจำกัด → ควรใช้ external tools เสริม

---

## 69. Endorsement (Promoted / Certified) Errors

### ERR-ENDORSE-001: "Certified" Option Grayed Out

**สาเหตุ:** User ไม่ได้อยู่ใน authorized reviewers group

**วิธีแก้:**
1. Admin Portal → Certification Settings → กำหนดกลุ่มผู้มีสิทธิ์ certify
2. **Promoted:** ทำได้โดย content owner / users with write permission
3. **Certified:** ทำได้เฉพาะ **authorized reviewers** ที่ admin กำหนด

---

## 70. Grouping & Binning Errors

### ERR-GROUP-001: Grouping / Binning ไม่ถูกต้อง

**Common Issues:**
| ปัญหา | สาเหตุ | วิธีแก้ |
|--------|--------|---------|
| กลุ่มไม่ตรง | Data entry ไม่ consistent ("USA" vs "United States") | ทำ grouping ใน Power Query ก่อน |
| Bin size ไม่เหมาะ | ตั้งค่า interval ไม่เหมาะกับ data distribution | ปรับ bin size ตาม data range |
| Grouping หายหลัง refresh | Source data เปลี่ยน | ใช้ conditional column ใน Power Query แทน manual grouping |

**วิธีแก้:**
1. ใช้ **Power Query** สำหรับ grouping ที่ stable (ไม่หายหลัง refresh)
2. ใช้ DAX `SWITCH(TRUE(), ...)` สำหรับ dynamic binning
3. ตรวจ data type ก่อนสร้าง bins (numeric columns เท่านั้น)

---

## 🔍 Quick Lookup Table (Full — 70 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "ambiguous column" | ERR-DAX-002 |
| "division by zero" | ERR-DAX-003 |
| "can't display" | ERR-VIS-001 |
| "too many values" | ERR-VIS-002 |
| "credentials expired" | ERR-REFRESH-002 |
| "gateway timeout" | ERR-REFRESH-001 |
| "access denied" / publish | ERR-PUB-001 |
| "Expression.Error" | ERR-PQ-001 |
| "DataFormat.Error" | ERR-PQ-002 |
| "DataSource.Error" | ERR-PQ-003 |
| "file corrupted" | ERR-FILE-001 |
| "invalid JSON" | ERR-PBIP-004 |
| "model.bim missing" | ERR-PBIP-002 |
| "RLS" / "row level" | ERR-RLS-001 |
| "OLS" / "object level" | ERR-OLS-001 |
| "slow" / "performance" | PERF-001 |
| "config stringify" | ERR-GEN-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "CapacityLimitExceeded" | ERR-EMBED-003 |
| "Service Principal" 401 | ERR-EMBED-004 |
| "export PDF" failed | ERR-EXPORT-001 |
| CSV data incorrect | ERR-EXPORT-003 |
| subscription ไม่ส่ง email | ERR-SUB-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| "aggregation proxy" | ERR-DQ-002 |
| "entity not found" dataflow | ERR-DF-001 |
| "mashup error" | ERR-DF-002 |
| "parameter required" .pbit | ERR-PBIT-001 |
| custom visual import fail | ERR-CV-001 |
| shortcut permission | ERR-FABRIC-001 |
| deployment pipeline error | ERR-FABRIC-003 |
| paginated "processing error" | ERR-PAG-001 |
| "many-to-many" relationship | ERR-REL-001 |
| "ambiguous path" loop | ERR-REL-002 |
| bidirectional filter risk | ERR-REL-003 |
| mobile "content not available" | ERR-MOBILE-001 |
| R/Python script error | ERR-RPY-001 |
| map ไม่โหลด | ERR-MAP-001 |
| ArcGIS blank | ERR-MAP-002 |
| conditional formatting ไม่ apply | ERR-CF-001 |
| bookmark highlight ผิด | ERR-BOOKMARK-001 |
| drillthrough ไม่แสดง | ERR-DRILL-001 |
| field parameter ไม่ทำงาน | ERR-FPARAM-001 |
| sensitivity label GUID | ERR-LABEL-002 |
| Pro vs PPU limits | ERR-LIC-001 |
| Power Automate refresh | ERR-PA-001 |
| Report Server 500 | ERR-PBIRS-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "invalid theme" JSON | ERR-THEME-001 |
| slicer sync ข้ามหน้า | ERR-SLICER-001 |
| tile ไม่ refresh | ERR-TILE-001 |
| Key Influencers ไม่น่าเชื่อถือ | ERR-AI-001 |
| workspace สร้างไม่ได้ | ERR-WS-001 |
| tooltip ไม่แสดง | ERR-TOOLTIP-001 |
| auto page refresh ไม่ทำงาน | ERR-APR-001 |
| composite model / hybrid | ERR-COMPOSITE-001 |
| smart narrative ไม่สร้าง | ERR-NARRATIVE-001 |
| anomaly detection ไม่พบ | ERR-ANOMALY-001 |
| forecast "empty values" | ERR-FORECAST-001 |
| data alert ไม่ส่ง | ERR-ALERT-001 |
| external tool connect fail | ERR-EXTOOL-001 |
| "out of memory" | ERR-MEM-001 |
| screen reader / alt text | ERR-A11Y-001 |
| visual interaction ไม่ filter | ERR-INTERACT-001 |
| REST API 401/403 | ERR-API-001 |
| rate limit 429 | ERR-API-002 |
| PowerShell unauthorized | ERR-PS-001 |
| template app publish fail | ERR-TAPP-001 |
| What-If parameter ไม่ทำงาน | ERR-WHATIF-001 |
| CALENDARAUTO() error | ERR-DATE-001 |
| date table relationship | ERR-DATE-002 |
| usage metrics ว่าง | ERR-USAGE-001 |
| SAP HANA driver | ERR-SAP-001 |
| Oracle ODAC missing | ERR-ORACLE-001 |
| Snowflake driver mismatch | ERR-SNOW-001 |
| Databricks driver missing | ERR-DATABRICKS-001 |
| lineage ไม่ครบ | ERR-LINEAGE-001 |
| certified grayed out | ERR-ENDORSE-001 |
| grouping/binning ผิด | ERR-GROUP-001 |

---

## 71. Formula.Firewall & Privacy Level Errors

### ERR-FIREWALL-001: "Formula.Firewall: Query is accessing data sources that have privacy levels which cannot be used together"

**สาเหตุ:** Power Query firewall ป้องกัน data จาก sources ที่มี privacy levels ต่างกัน

**วิธีแก้:**
1. Data Source Settings → ตั้ง privacy level ให้ตรง (Public / Organizational / Private)
2. "Flatten" queries → ให้แต่ละ query ดึงข้อมูลจาก source เดียว
3. ⚠️ **Desktop vs Service ต่างกัน:** "Always ignore privacy levels" ใน Desktop จะ **ไม่ทำงาน** ใน Service
4. Service: ตั้ง privacy level ที่ dataset settings สำหรับทุก source

**Pattern: Staging Query**
```
// สร้าง staging query กันปัญหา firewall
StagingQuery = Table.Buffer(SourceQuery)  // Buffer ก่อน combine
```

---

## 72. Dynamic Data Source Errors

### ERR-DYNSRC-001: Dataset Refresh Fail เมื่อใช้ Dynamic Source

**สาเหตุ:** PBI Service ทำ static analysis บน M code → ไม่สามารถระบุ data source ที่ dynamic ได้

**ตัวอย่างที่มีปัญหา:**
- `Web.Contents(parameterURL)` — URL มาจาก parameter
- Custom M functions ที่ source definition ขึ้นอยู่กับ function parameters

**วิธีแก้:**
1. ใช้ `Web.Contents(baseURL, [RelativePath = dynamicPart])` แทน URL เดียว
2. ตรวจ "Skip test connection" ใน gateway settings
3. ประกาศ query parameters ให้ชัดเจน (ไม่ dynamic generate)

---

## 73. Dataverse / CDS Connector Errors

### ERR-DATAVERSE-001: "Request Entity Too Large" (413)

**สาเหตุ:** ไฟล์ > 16 MB / data payload เกิน limit

**วิธีแก้:**
1. ใช้ **staged chunk download** สำหรับไฟล์ > 16 MB
2. ลด columns/rows ที่ดึง → ใช้ OData query filters
3. Paginate data ด้วย `$top` + `$skip` parameters

---

### ERR-DATAVERSE-002: Dataverse Connection Timeout

**วิธีแก้:**
1. ใช้ **Dataverse (Legacy)** connector ถ้า new connector มีปัญหา
2. ตรวจ Dataverse environment URL ถูกต้อง
3. ตรวจ user มี Security Role ที่เหมาะสมใน Dataverse

---

## 74. Visual Calculations Errors

### ERR-VISCALC-001: Visual Calculations ไม่แสดงหลัง Publish

**Limitations:**
| Scenario | รองรับ? |
|----------|--------|
| Power BI Desktop | ✅ (Preview, enabled by default) |
| Power BI Service | ✅ (ปกติ) |
| Publish to Web | ❌ **ไม่รองรับ** |
| Power BI Report Server | ❌ **ไม่รองรับ** (preview features) |

**วิธีแก้:**
1. แทน visual calculations ด้วย **DAX measures** ใน data model
2. อัพเดท PBI Desktop → latest version
3. ⚠️ ห้ามใช้กับ "Publish to Web" → ใช้ standard DAX แทน

---

## 75. Report Builder & Semantic Model Connection Errors

### ERR-RPTBUILD-001: "Unexpected Error" เมื่อเชื่อม Semantic Model

**สาเหตุ:**
- OAuth token expired
- Browser tracking prevention settings
- Company firewall blocks connection

**วิธีแก้:**
1. Re-authenticate ด้วย **OAuth2** ใน data source settings
2. ลด browser tracking prevention (Settings → Privacy)
3. ตรวจ firewall ไม่ block Power BI Service endpoints
4. อัพเดท **Power BI Report Builder** → latest version

---

## 76. Backup & Restore Workspace Errors

### ERR-BACKUP-001: ไม่สามารถ Restore Report ที่ลบไปแล้ว

**⚠️ สำคัญ:** Power BI Service **ไม่มี** built-in backup/restore / versioning

**วิธีแก้:**
1. ใช้ **PBIP format + Git** สำหรับ version control
2. สำรอง .pbix ไว้ local/SharePoint เป็นประจำ
3. ใช้ **Deployment Pipelines** สำหรับ staging → production
4. ⚠️ Reports สร้างใน Service โดยตรง → ไม่สามารถ recover ถ้าลบแล้ว

---

### ERR-BACKUP-002: Upload Report ไป Workspace ไม่ได้

**สาเหตุ:** Storage quota เต็ม / service outage / permission

**วิธีแก้:**
1. ตรวจ workspace storage quota
2. ตรวจ user มี Contributor+ permission
3. ลอง upload อีกครั้ง (อาจเป็น transient failure)

---

## 77. Dynamic Format Strings Errors

### ERR-DYNFMT-001: Dynamic Format String ไม่แสดงใน Excel / DAX Studio

**⚠️ Limitation:** Dynamic format strings **ไม่รองรับ** ใน:
- Excel Pivot Tables (connected to PBI dataset)
- DAX Studio
- External tools ที่ query นอก PBI report

**วิธีแก้:**
1. ใช้ `FORMAT()` function สำหรับ external tool compatibility (แต่ผลลัพธ์เป็น text)
2. ดูผลลัพธ์จริงใน PBI Desktop/Service เท่านั้น

---

### ERR-DYNFMT-002: Format String Silent Reset

**สาเหตุ:** PBI Desktop version เก่าทำให้ format string reset หลังยืนยัน

**วิธีแก้:**
1. อัพเดท PBI Desktop → **latest version**
2. ใช้ "Format string expression" แทน manual format
3. ใช้ **Tabular Editor** สำหรับ create/edit measures with dynamic format

---

## 78. Admin Audit Log Errors

### ERR-AUDIT-001: Audit Log ไม่แสดงข้อมูล

**Checklist:**
- [ ] Microsoft 365 Compliance Center → Audit retention configured
- [ ] Power BI Admin rights (ไม่ต้องใช้ M365 Global Admin แล้วใน 2025)
- [ ] Retention default = 180 วัน → ตั้งค่าเพิ่มถ้าต้องการ
- [ ] ActivityEvents API → ดึงได้สูงสุด 1 วัน/request

**วิธีแก้:**
1. ใช้ **Power BI API ActivityEvents** endpoint สำหรับ custom dashboards
2. Export ไป **Azure Log Analytics** สำหรับ long-term retention
3. ตั้ง Service Principal + security group สำหรับ automated extraction

---

## 79. On-Object Interaction Errors

### ERR-ONOBJ-001: Custom Visual Dialog Box ไม่แสดง

**สาเหตุ:** Bug ใน PBI Desktop (reported Feb 2025) — dialog boxes เปิดแล้ว "หายไป"

**วิธีแก้:**
1. อัพเดท PBI Desktop → version ที่มี fix แล้ว
2. ปิด on-object interaction → ใช้ Format Pane แทนชั่วคราว

---

### ERR-ONOBJ-002: Embedded Report — Settings ไม่ Apply ใน View Mode

**สาเหตุ:** Configuration settings ต้อง "Edit mode" จึงจะทำงาน

**วิธีแก้:**
1. ตั้ง embedded content เป็น **Edit mode**
2. ตรวจ permission level รองรับ editing

---

## 80. Multi-Geo Configuration Errors

### ERR-MULTIGEO-001: Data Residency ไม่ตรง Region ที่กำหนด

**Requirements:**
| Condition | ต้องมี |
|-----------|--------|
| License | **Premium** capacity เท่านั้น |
| Config | Admin Portal → Capacity Settings → assign region |
| Data at rest | อยู่ใน specified remote geography |

**วิธีแก้:**
1. ตรวจ capacity assigned ถูก region
2. ⚠️ Metadata (workspace names, user info) อาจยังอยู่ใน home region
3. ใช้ Admin API → ตรวจ actual data location
4. Contact Microsoft support สำหรับ region migration ที่ซับซ้อน

---

## 🔍 Quick Lookup Table (Full — 80 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "ambiguous column" | ERR-DAX-002 |
| "division by zero" | ERR-DAX-003 |
| "can't display" | ERR-VIS-001 |
| "too many values" | ERR-VIS-002 |
| "credentials expired" | ERR-REFRESH-002 |
| "gateway timeout" | ERR-REFRESH-001 |
| "access denied" / publish | ERR-PUB-001 |
| "Expression.Error" | ERR-PQ-001 |
| "DataFormat.Error" | ERR-PQ-002 |
| "DataSource.Error" | ERR-PQ-003 |
| "file corrupted" | ERR-FILE-001 |
| "invalid JSON" | ERR-PBIP-004 |
| "model.bim missing" | ERR-PBIP-002 |
| "RLS" / "row level" | ERR-RLS-001 |
| "OLS" / "object level" | ERR-OLS-001 |
| "slow" / "performance" | PERF-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "CapacityLimitExceeded" | ERR-EMBED-003 |
| "export PDF" failed | ERR-EXPORT-001 |
| subscription ไม่ส่ง email | ERR-SUB-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| "entity not found" dataflow | ERR-DF-001 |
| "parameter required" .pbit | ERR-PBIT-001 |
| custom visual import fail | ERR-CV-001 |
| shortcut permission | ERR-FABRIC-001 |
| deployment pipeline error | ERR-FABRIC-003 |
| paginated "processing error" | ERR-PAG-001 |
| "many-to-many" relationship | ERR-REL-001 |
| "ambiguous path" loop | ERR-REL-002 |
| mobile "content not available" | ERR-MOBILE-001 |
| R/Python script error | ERR-RPY-001 |
| map ไม่โหลด | ERR-MAP-001 |
| conditional formatting ไม่ apply | ERR-CF-001 |
| bookmark highlight ผิด | ERR-BOOKMARK-001 |
| drillthrough ไม่แสดง | ERR-DRILL-001 |
| field parameter ไม่ทำงาน | ERR-FPARAM-001 |
| sensitivity label GUID | ERR-LABEL-002 |
| Pro vs PPU limits | ERR-LIC-001 |
| Power Automate refresh | ERR-PA-001 |
| Report Server 500 | ERR-PBIRS-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "invalid theme" JSON | ERR-THEME-001 |
| slicer sync ข้ามหน้า | ERR-SLICER-001 |
| tile ไม่ refresh | ERR-TILE-001 |
| Key Influencers ไม่น่าเชื่อถือ | ERR-AI-001 |
| workspace สร้างไม่ได้ | ERR-WS-001 |
| tooltip ไม่แสดง | ERR-TOOLTIP-001 |
| auto page refresh ไม่ทำงาน | ERR-APR-001 |
| composite model / hybrid | ERR-COMPOSITE-001 |
| smart narrative ไม่สร้าง | ERR-NARRATIVE-001 |
| forecast "empty values" | ERR-FORECAST-001 |
| data alert ไม่ส่ง | ERR-ALERT-001 |
| external tool connect fail | ERR-EXTOOL-001 |
| "out of memory" | ERR-MEM-001 |
| screen reader / alt text | ERR-A11Y-001 |
| visual interaction ไม่ filter | ERR-INTERACT-001 |
| REST API 401/403 | ERR-API-001 |
| rate limit 429 | ERR-API-002 |
| PowerShell unauthorized | ERR-PS-001 |
| template app publish fail | ERR-TAPP-001 |
| What-If parameter ไม่ทำงาน | ERR-WHATIF-001 |
| CALENDARAUTO() error | ERR-DATE-001 |
| usage metrics ว่าง | ERR-USAGE-001 |
| SAP HANA driver | ERR-SAP-001 |
| Oracle ODAC missing | ERR-ORACLE-001 |
| Snowflake driver mismatch | ERR-SNOW-001 |
| Databricks driver missing | ERR-DATABRICKS-001 |
| lineage ไม่ครบ | ERR-LINEAGE-001 |
| certified grayed out | ERR-ENDORSE-001 |
| grouping/binning ผิด | ERR-GROUP-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| privacy levels ไม่ compatible | ERR-FIREWALL-001 |
| dynamic data source refresh fail | ERR-DYNSRC-001 |
| Dataverse "entity too large" | ERR-DATAVERSE-001 |
| Dataverse connection timeout | ERR-DATAVERSE-002 |
| visual calculations ไม่แสดง | ERR-VISCALC-001 |
| Report Builder semantic model | ERR-RPTBUILD-001 |
| backup / restore ไม่ได้ | ERR-BACKUP-001 |
| upload workspace fail | ERR-BACKUP-002 |
| dynamic format string ไม่แสดง | ERR-DYNFMT-001 |
| format string reset | ERR-DYNFMT-002 |
| audit log ว่าง | ERR-AUDIT-001 |
| on-object dialog หาย | ERR-ONOBJ-001 |
| embedded edit mode | ERR-ONOBJ-002 |
| multi-geo data residency | ERR-MULTIGEO-001 |

---

## 81. Metrics / Goals / Scorecards Errors

### ERR-SCORE-001: Scorecard ไม่ Refresh อัตโนมัติ

**สาเหตุ:** Metrics ใน Scorecard ไม่อัพเดทแม้ dataset refresh สำเร็จ

**วิธีแก้:**
1. ตรวจว่า metric connection ยังถูกต้อง → re-establish ถ้า report ถูก republish
2. ⚠️ เมื่อ **RLS** เปิดอยู่ → Scorecard จะ **ไม่** auto-refresh
   - Workaround: ใช้ **Power Automate** trigger "Refresh All Metrics" หลัง dataset refresh
3. ตรวจ measures ว่าไม่ return BLANK → ใช้ `IF(ISBLANK(...), 0, ...)` แทน
4. อัพเดท PBI Desktop → latest version (Scorecard visual อาจยังเป็น preview)

---

### ERR-SCORE-002: Scorecard Visual ไม่แสดงใน Desktop

**วิธีแก้:**
1. File → Options → Preview Features → enable "Scorecard Visual"
2. อัพเดท PBI Desktop → latest version
3. ⚠️ Scorecard visual ต้องใช้ **Power BI Service** สำหรับ full features

---

## 82. Q&A Natural Language / Copilot Errors

### ERR-QA-001: Q&A Visual แสดง "Couldn't determine" หรือ ผลลัพธ์ผิด

**⚠️ สำคัญ: Q&A ถูก deprecated (Dec 2025)** → retire Dec 2026

**วิธีแก้ (ระหว่างนี้):**
1. ตั้ง **Synonyms** ให้ fields ใน Model View → Synonyms pane
2. ใช้ชื่อ column ที่ **เข้าใจง่าย** (ไม่ใช่ abbreviations)
3. ซ่อน technical columns ที่ไม่ต้องการใน Q&A
4. **แนะนำ:** เปลี่ยนไปใช้ **Power BI Copilot** แทน (ต้องมี F64+ capacity)

---

### ERR-QA-002: Copilot ไม่พร้อมใช้งาน

**Requirements:**
| Condition | ต้องมี |
|-----------|--------|
| Capacity | **F64+ หรือ P1+** |
| Language | English (primary support) |
| Tenant setting | Admin Portal → "Copilot" → enabled |
| Data | Star schema recommended |

---

## 83. SSO (Single Sign-On) / Kerberos / SAML Errors

### ERR-SSO-001: Kerberos SSO ล้มเหลว — "Credentials cannot be used"

**Checklist:**
- [ ] Gateway service account = **domain account** (ไม่ใช่ local service)
- [ ] SPN (Service Principal Name) ตั้งค่าถูกต้อง
- [ ] AES 128-bit + 256-bit encryption เปิดใน AD สำหรับทั้ง gateway + data source account
- [ ] UPN mapping ถูกต้อง
- [ ] ทดสอบ connection **ไม่ใช้ SSO** ก่อน → ถ้ายัง fail → ปัญหาไม่ใช่ Kerberos

**วิธีแก้:**
1. ใช้ "Test Single Sign-On" feature ใน Power BI Service
2. ตรวจ Event Viewer ของ gateway server → Kerberos errors
3. ตรวจ firewall ไม่ block Kerberos ports (88, 464)

---

### ERR-SSO-002: SAML SSO "Credentials Rejected" (SAP HANA / อื่นๆ)

**วิธีแก้:**
1. Gateway → Advanced settings → enable "SSO via SAML"
2. ตรวจ SAML certificate ยังไม่หมดอายุ
3. ดู authentication traces ฝั่ง data source (e.g., SAP HANA trace logs)
4. ⚠️ PBI Report Server **ไม่รองรับ** SAML/OIDC natively → ต้องใช้ custom security extension

---

## 84. Incremental Refresh Errors

### ERR-INCREF-001: Incremental Refresh Policy ไม่ทำงาน

**สาเหตุ:**
- `RangeStart`/`RangeEnd` parameters ไม่ใช่ **Date/Time** type
- Data source ไม่รองรับ Query Folding
- Initial full load timeout (Pro: 2 ชม., Premium: 5 ชม.)

**วิธีแก้:**
1. ตรวจ parameters ใน Power Query: `RangeStart`, `RangeEnd` → ต้องเป็น **Date/Time** type
2. ตรวจ date column ในตาราง → ต้อง **Date/Time** เช่นกัน (ไม่ใช่ Date only)
3. ใช้ data source ที่รองรับ query folding (SQL Server, Azure SQL, etc.)
4. สำหรับ first-time refresh → อาจต้อง Premium capacity (5 ชม. limit)

---

### ERR-INCREF-002: "Incremental Refresh Policy No Longer Valid"

**สาเหตุ:** Republish .pbix หลังเพิ่ม measures/เปลี่ยน Power Query → policy reset

**วิธีแก้:**
1. ✅ ใช้ XMLA endpoint สำหรับ publish model changes (ไม่ต้อง re-upload .pbix)
2. ตั้ง incremental refresh policy ใหม่หลัง republish
3. ⚠️ หลัง republish → partition structure อาจถูก overwrite

---

## 85. Aggregation Table Errors

### ERR-AGG-001: Aggregation Table ไม่ถูกใช้ (Fall-back to DirectQuery)

**สาเหตุ:**
- Data type mismatch ระหว่าง aggregation column กับ detail column
- Visual ต้องการ grain ที่ละเอียดกว่า aggregation
- Complex DAX measures bypass aggregation

**วิธีแก้:**
1. ตรวจ data types ให้ตรงกัน (ทั้ง aggregation + detail columns)
2. Dimension tables → ตั้งเป็น **Dual** storage mode
3. Detail table → ต้องเป็น **DirectQuery** (ไม่ใช่ Import)
4. ใช้ **DAX Studio** → ดู aggregation hits/misses

---

### ERR-AGG-002: "Chained Aggregation" ไม่รองรับ

**Limitation:** ❌ ไม่สามารถ chain aggregation ข้าม 3+ tables

**วิธีแก้:**
1. Flatten aggregation → ทำ aggregation ใน 1-2 tables เท่านั้น
2. ⚠️ ห้ามใช้ duplicate aggregation (same function + same detail column)
3. ⚠️ `USERELATIONSHIP` → ไม่ work กับ aggregation hits → ใช้ `TREATAS` แทน

---

## 86. Shared Dataset / Live Connection Errors

### ERR-SHARED-001: Live Connection ไม่สามารถแก้ไข Data Model ได้

**สาเหตุ:** Live connection reports → read-only สำหรับ data model

**วิธีแก้:**
1. ⚠️ **By design** — ต้องไปแก้ที่ original semantic model
2. ใช้ **Measures** ที่ defined ใน report level ได้ (report-level measures)
3. ใช้ DirectQuery connection to semantic model → สามารถ add local tables ได้

---

### ERR-SHARED-002: "Allow DirectQuery connections to Power BI semantic models" ปิดอยู่

**วิธีแก้:**
1. Admin Portal → Tenant Settings → "Allow DirectQuery connections..." → **Enable**
2. ตรวจ user มี contributor access ใน target workspace
3. ตรวจ credentials ไม่ expired → clear old credentials + reconnect

---

## 87. Dynamic M Query Parameters Errors

### ERR-MPARAM-001: Dynamic M Parameter ไม่อัพเดทจาก Slicer

**สาเหตุ:** Parameter "bind to" ไม่ถูกต้อง / PBI Desktop เก่า

**วิธีแก้:**
1. Direct Query → "Bind to parameter" ในสูตร M query ต้องตั้งค่าถูกต้อง
2. อัพเดท PBI Desktop → **latest version** (feature อาจ broken ใน versions เก่า)
3. ⚠️ **ไม่รองรับ** ใน: Power BI Report Server, Excel live connection

---

### ERR-MPARAM-002: "DirectQuery may not be used with this data source"

**สาเหตุ:** Data source ไม่รองรับ DirectQuery + dynamic parameters

**วิธีแก้:**
1. ตรวจ data source compatibility สำหรับ DirectQuery
2. ⚠️ Switching data source ด้วย dynamic parameter → **ไม่รองรับ** ใน PBI Service
3. ตรวจ M query syntax ถูกต้อง → parameter ต้อง reference ถูก column

---

## 88. Personal Gateway (Personal Mode) Errors

### ERR-PGATEWAY-001: "Personal Gateway is Offline"

**สาเหตุ:** เครื่องปิด / sleep / หลุดจาก internet

**วิธีแก้:**
1. ⚠️ Personal gateway run เป็น **application** (ไม่ใช่ service) → ต้องเปิดเครื่องตลอด
2. **แนะนำ**: เปลี่ยนไปใช้ **On-premises Data Gateway (Standard)** → run เป็น service
3. ตรวจ Windows power settings → ไม่ให้ sleep

---

### ERR-PGATEWAY-002: "Unable to Update Connection Credentials"

**สาเหตุ:** Personal gateway update ทำให้ credentials เสีย (reported Jun 2024)

**วิธีแก้:**
1. ไปที่ "Manage Connections and Gateways" → สร้าง connection ใหม่
2. อัพเดท semantic model settings → เลือก gateway connection ใหม่
3. ⚠️ Personal gateway **ไม่รองรับ** mashup queries ที่ mix cloud + on-prem sources ผ่าน OAuth

---

## 89. Azure Analysis Services (AAS) Connection Errors

### ERR-AAS-001: "400 Bad Request" เมื่อ Refresh AAS Model

**วิธีแก้:**
1. ตรวจ Service Principal มี **Analysis Services Admin** permissions
2. Validate credentials → re-enter ถ้า expired
3. ตรวจ firewall rules → Azure services ต้องมี access ไป AAS instance
4. ตรวจ API request format ถูกต้อง (REST API)

---

### ERR-AAS-002: PBI Desktop เปิด PBIX ที่ Live Connect ไป AAS ไม่ได้

**สาเหตุ:** PBIX download จาก Service → connection string อาจ broken

**วิธีแก้:**
1. อัพเดท PBI Desktop → latest version
2. ตรวจ connection string ใน PBIX → ชี้ไป AAS endpoint ที่ถูกต้อง
3. ⚠️ AAS retirement (after Fabric launch) → พิจารณาย้ายไป **Fabric Semantic Model**

---

## 90. Quick Measures Errors

### ERR-QMEASURE-001: "New Quick Measure" หายไปหลังใช้ครั้งแรก

**สาเหตุ:** By design — หลังสร้าง Quick Measure ครั้งแรก → เปิด Quick Measure pane แทน

**วิธีแก้:**
1. ใช้ Quick Measure pane (เปิดมาแล้ว) สำหรับสร้าง measures ถัดไป
2. หรือพิมพ์ DAX measure ด้วยตัวเอง

---

### ERR-QMEASURE-002: PBI Desktop Crash เมื่อใช้ Quick Measure บางตัว

**สาเหตุ:** Bug ใน PBI Desktop versions เฉพาะ (reported Apr 2024) — เช่น "percentage difference"

**วิธีแก้:**
1. อัพเดท PBI Desktop → **latest version**
2. Clear cache: `%LOCALAPPDATA%\Microsoft\Power BI Desktop\CEF\cache` → ลบทั้งหมด
3. Clean reinstall PBI Desktop
4. Workaround: เขียน DAX measure เอง (ไม่ใช้ Quick Measure)

---

## 🔍 Quick Lookup Table (Full — 90 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "ambiguous column" | ERR-DAX-002 |
| "division by zero" | ERR-DAX-003 |
| "can't display" | ERR-VIS-001 |
| "too many values" | ERR-VIS-002 |
| "credentials expired" | ERR-REFRESH-002 |
| "gateway timeout" | ERR-REFRESH-001 |
| "access denied" / publish | ERR-PUB-001 |
| "Expression.Error" | ERR-PQ-001 |
| "DataFormat.Error" | ERR-PQ-002 |
| "DataSource.Error" | ERR-PQ-003 |
| "file corrupted" | ERR-FILE-001 |
| "invalid JSON" | ERR-PBIP-004 |
| "model.bim missing" | ERR-PBIP-002 |
| "RLS" / "row level" | ERR-RLS-001 |
| "OLS" / "object level" | ERR-OLS-001 |
| "slow" / "performance" | PERF-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "CapacityLimitExceeded" | ERR-EMBED-003 |
| "export PDF" failed | ERR-EXPORT-001 |
| subscription ไม่ส่ง email | ERR-SUB-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| "entity not found" dataflow | ERR-DF-001 |
| "parameter required" .pbit | ERR-PBIT-001 |
| custom visual import fail | ERR-CV-001 |
| shortcut permission | ERR-FABRIC-001 |
| deployment pipeline error | ERR-FABRIC-003 |
| paginated "processing error" | ERR-PAG-001 |
| "many-to-many" relationship | ERR-REL-001 |
| "ambiguous path" loop | ERR-REL-002 |
| mobile "content not available" | ERR-MOBILE-001 |
| R/Python script error | ERR-RPY-001 |
| map ไม่โหลด | ERR-MAP-001 |
| conditional formatting ไม่ apply | ERR-CF-001 |
| bookmark highlight ผิด | ERR-BOOKMARK-001 |
| drillthrough ไม่แสดง | ERR-DRILL-001 |
| field parameter ไม่ทำงาน | ERR-FPARAM-001 |
| sensitivity label GUID | ERR-LABEL-002 |
| Pro vs PPU limits | ERR-LIC-001 |
| Power Automate refresh | ERR-PA-001 |
| Report Server 500 | ERR-PBIRS-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "invalid theme" JSON | ERR-THEME-001 |
| slicer sync ข้ามหน้า | ERR-SLICER-001 |
| tile ไม่ refresh | ERR-TILE-001 |
| Key Influencers ไม่น่าเชื่อถือ | ERR-AI-001 |
| workspace สร้างไม่ได้ | ERR-WS-001 |
| tooltip ไม่แสดง | ERR-TOOLTIP-001 |
| auto page refresh ไม่ทำงาน | ERR-APR-001 |
| composite model / hybrid | ERR-COMPOSITE-001 |
| smart narrative ไม่สร้าง | ERR-NARRATIVE-001 |
| forecast "empty values" | ERR-FORECAST-001 |
| data alert ไม่ส่ง | ERR-ALERT-001 |
| external tool connect fail | ERR-EXTOOL-001 |
| "out of memory" | ERR-MEM-001 |
| screen reader / alt text | ERR-A11Y-001 |
| visual interaction ไม่ filter | ERR-INTERACT-001 |
| REST API 401/403 | ERR-API-001 |
| rate limit 429 | ERR-API-002 |
| PowerShell unauthorized | ERR-PS-001 |
| template app publish fail | ERR-TAPP-001 |
| What-If parameter ไม่ทำงาน | ERR-WHATIF-001 |
| CALENDARAUTO() error | ERR-DATE-001 |
| usage metrics ว่าง | ERR-USAGE-001 |
| SAP HANA driver | ERR-SAP-001 |
| Oracle ODAC missing | ERR-ORACLE-001 |
| Snowflake driver mismatch | ERR-SNOW-001 |
| Databricks driver missing | ERR-DATABRICKS-001 |
| lineage ไม่ครบ | ERR-LINEAGE-001 |
| certified grayed out | ERR-ENDORSE-001 |
| grouping/binning ผิด | ERR-GROUP-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| privacy levels ไม่ compatible | ERR-FIREWALL-001 |
| dynamic data source refresh fail | ERR-DYNSRC-001 |
| Dataverse "entity too large" | ERR-DATAVERSE-001 |
| visual calculations ไม่แสดง | ERR-VISCALC-001 |
| Report Builder semantic model | ERR-RPTBUILD-001 |
| backup / restore ไม่ได้ | ERR-BACKUP-001 |
| dynamic format string ไม่แสดง | ERR-DYNFMT-001 |
| audit log ว่าง | ERR-AUDIT-001 |
| on-object dialog หาย | ERR-ONOBJ-001 |
| multi-geo data residency | ERR-MULTIGEO-001 |
| scorecard ไม่ refresh | ERR-SCORE-001 |
| scorecard visual ไม่แสดง | ERR-SCORE-002 |
| Q&A "couldn't determine" | ERR-QA-001 |
| Copilot ไม่พร้อมใช้ | ERR-QA-002 |
| Kerberos SSO fail | ERR-SSO-001 |
| SAML credentials rejected | ERR-SSO-002 |
| incremental refresh policy fail | ERR-INCREF-001 |
| "policy no longer valid" | ERR-INCREF-002 |
| aggregation table ไม่ถูกใช้ | ERR-AGG-001 |
| chained aggregation | ERR-AGG-002 |
| live connection แก้ model ไม่ได้ | ERR-SHARED-001 |
| DirectQuery to semantic model ปิด | ERR-SHARED-002 |
| dynamic M parameter ไม่ทำงาน | ERR-MPARAM-001 |
| DirectQuery + dynamic parameter fail | ERR-MPARAM-002 |
| personal gateway offline | ERR-PGATEWAY-001 |
| personal gateway credentials fail | ERR-PGATEWAY-002 |
| Azure Analysis Services 400 | ERR-AAS-001 |
| AAS live connect PBIX fail | ERR-AAS-002 |
| quick measure หายไป | ERR-QMEASURE-001 |
| quick measure crash | ERR-QMEASURE-002 |

---

## 91. Calculation Groups — Advanced Errors

### ERR-CALCGRP-001: Calculation Group ไม่ทำงานหลัง Deploy ผ่าน Pipeline

**สาเหตุ:** Deployment pipeline ไม่ carry over security / service principal access

**วิธีแก้:**
1. Refresh **service principal** permissions หลัง deploy
2. Refresh semantic model ใน target workspace
3. ⚠️ ถ้า publish ตรงจาก PBI Desktop → ทำงานปกติ (ปัญหาเฉพาะ pipeline)

---

### ERR-CALCGRP-002: Format Expression ไม่ทำงานกับ Measures จาก PBI Desktop

**สาเหตุ:** Data format ของ measure ใน Desktop override format expression

**วิธีแก้:**
1. ตั้ง measure data format เป็น "Automatic" (ไม่ force format)
2. ใช้ **Tabular Editor** สร้าง/แก้ calculation groups (แนะนำ)
3. ตรวจ DAX ไม่ return text เมื่อ visual คาดหวัง number

---

## 92. Streaming & Push Dataset Errors

### ERR-STREAM-001: Streaming Dataset "403 Forbidden" / "Unauthorized"

**สาเหตุ:** Client secret / API key หมดอายุ (มักเกิดหลัง ~1 ปี)

**⚠️ สำคัญ:** Streaming datasets **deprecated** → retire Oct 2027

**วิธีแก้:**
1. ตรวจ Entra ID app registration → client secret expiry
2. Renew secret + update application config
3. **แนะนำ:** ย้ายไป **Microsoft Fabric Real-Time Intelligence**

---

### ERR-STREAM-002: Push Dataset "400 Bad Request"

**Rate Limits:**
| Type | Limit |
|------|-------|
| Push dataset | 120 POST requests/min/dataset |
| Streaming dataset | 5 requests/sec, 15 KB payload |

**วิธีแก้:**
1. ตรวจ JSON syntax → valid format
2. Batch rows → ลดจำนวน requests
3. ตรวจ column names + data types ตรงกับ schema

---

## 93. Direct Lake Errors (Fabric)

### ERR-DLAKE-001: "You don't have permission to view Direct Lake table"

**สาเหตุ:** User ไม่มี permission บน underlying Lakehouse

**วิธีแก้:**
1. Grant **Viewer** access ที่ Lakehouse workspace
2. หรือ grant **ReadAll** permission บน Lakehouse item
3. ตรวจ OneLake security settings

---

### ERR-DLAKE-002: Direct Lake Fallback ไป DirectQuery โดยไม่ตั้งใจ

**สาเหตุ:**
- Views จาก Warehouse → ยังทำงานใน DirectQuery mode
- DAX queries ที่ไม่รองรับใน Direct Lake
- ❌ Direct Lake on OneLake → **ไม่มี** DQ fallback (query จะ fail)

**วิธีแก้:**
1. ตรวจ Capacity Metrics → ดู fallback events
2. ใช้ tables (ไม่ใช่ views) สำหรับ Direct Lake
3. ⚠️ ถ้าตั้ง "Direct Lake Only" → queries ที่ไม่ support จะ **error ทันที**

---

## 94. OneLake Shortcut Errors (Fabric)

### ERR-SHORTCUT-001: Shortcut Tables "หายไป" จาก Lakehouse

**สาเหตุ:** User ไม่มี permission บน source Lakehouse

**วิธีแก้:**
1. ตรวจ permission บน **source** Lakehouse (ที่สร้าง shortcut ไป)
2. ตรวจ OneLake security settings ของ source
3. ⚠️ Items ที่ติดอยู่ใน "Unidentified" folder → อาจเกิดจาก case sensitivity ใน schema

---

### ERR-SHORTCUT-002: "Underlying file has changed" — Frequent Read Errors

**วิธีแก้:**
1. Refresh metadata ของ shortcut
2. ตรวจ source data ไม่ถูก update ขณะ read
3. ⚠️ Known issue — metadata handling bugs → อัพเดท Fabric environment

---

## 95. Analyze in Excel Errors

### ERR-AIE-001: "No Data Fields in OLAP Cube"

**สาเหตุ:** Dataset ไม่มี **measures** defined → Excel ต้องการ measures

**วิธีแก้:**
1. สร้าง **explicit measures** ใน data model (ไม่ใช่แค่ implicit aggregation)
2. ตรวจ user มี access ไป dataset ใน Service
3. ⚠️ ODC file จาก Desktop → เป็น temporary connection → ปิด Desktop = connection break

---

### ERR-AIE-002: Excel ไม่ Refresh หลังเปิด ODC File

**วิธีแก้:**
1. ใช้ "Analyze in Excel" จาก **Power BI Service** (ไม่ใช่ Desktop)
2. ตรวจ Excel → Data → Refresh All (manual trigger)
3. ตรวจ network connection ไปยัง Power BI Service

---

## 96. Embed for Customers (App-Owns-Data) Errors

### ERR-APPEMBED-001: Embedded Report ไม่โหลด — CORS / 403

**สาเหตุ:** Domain ไม่ได้ whitelist / Azure AD app config ผิด

**วิธีแก้:**
1. ตรวจ Azure AD App Registration → redirect URIs ถูกต้อง
2. ตรวจ API permissions: `Power BI Service` → `Report.Read.All` / `Dataset.Read.All`
3. ตรวจ service principal มี access ไป workspace
4. CORS: ตรวจ server-side proxy ว่า set headers ถูกต้อง

---

### ERR-APPEMBED-002: Embed Token Expired — "TokenExpired" (ซ้ำ ERR-EMBED-001 แต่เฉพาะ App-Owns-Data)

**วิธีแก้:**
1. ตรวจ token lifetime → default 1 ชม.
2. Implement **automatic token refresh** ก่อน expire
3. ใช้ `GenerateToken` API กับ `accessLevel` ที่ถูกต้อง

---

## 97. Data Loss Prevention (DLP) Errors

### ERR-DLP-001: ไม่สามารถ Share / Export Report ได้ — ถูก DLP Policy Block

**สาเหตุ:** M365 DLP policy ตรวจพบ sensitive data ใน dataset

**วิธีแก้:**
1. ตรวจ **M365 Compliance Center** → ดู policy ที่ trigger
2. ลบ/mask sensitive data จาก dataset
3. ขอ admin อนุญาต override (ถ้า business need)
4. ⚠️ DLP เป็น **policy enforcement** ไม่ใช่ bug → ต้องแก้ที่ data หรือ policy

---

## 98. Capacity Throttling Errors (Fabric / Premium)

### ERR-THROTTLE-001: "Organization's Fabric compute capacity has exceeded its limits"

**สาเหตุ:** CPU overuse เกิน purchased capacity

**Throttling Stages:**
| Stage | Duration | ผลกระทบ |
|-------|----------|---------|
| Overage | 0-10 min | ไม่ throttle (grace period) |
| Interactive delay | 10-60 min | Delay 20 วินาที |
| Interactive reject | 60+ min | Reject interactive jobs |
| Background reject | Continued | Reject ทุก request |

**วิธีแก้:**
1. ใช้ **Capacity Metrics App** → ดู CPU usage + throttling events
2. Optimize refresh schedules (ใช้ incremental refresh)
3. Optimize DAX queries (ใช้ Performance Analyzer)
4. ⚠️ ถ้า throttle บ่อย → **เพิ่ม SKU capacity**

---

## 99. XMLA Endpoint — Advanced Errors

### ERR-XMLA-ADV-001: "Cannot process database — DatasourceHasNoCredentialError"

**สาเหตุ:** Deploy model via XMLA → ยังไม่ตั้ง credentials ใน Service

**วิธีแก้:**
1. Deployment Options → Processing Options → **"Do Not Process"**
2. หลัง deploy → ตั้ง data source credentials ใน PBI Service
3. แล้วค่อย refresh semantic model

---

### ERR-XMLA-ADV-002: "XMLA Read/Write permission is disabled"

**วิธีแก้:**
1. Admin Portal → Capacity Settings → XMLA Endpoint → **Read/Write**
2. Tenant Settings → "Allow XMLA endpoints..." → **Enabled**
3. ใช้ **SSMS 18.8+** (versions เก่ามี bugs กับ XMLA)
4. ตรวจ connectivity ไป `*.pbidedicated.windows.net` → proxy อาจ block

---

## 100. Datamart & SQL Endpoint Errors (Fabric)

### ERR-DATAMART-001: SQL Endpoint ไม่แสดงข้อมูลล่าสุด

**สาเหตุ:** Column mapping enabled / sync delay

**วิธีแก้:**
1. ตรวจ table ไม่ใช้ column mapping (ยังไม่รองรับ SQL endpoint)
2. ⚠️ Sync เป็น **non-deterministic** → ขึ้นอยู่กับจำนวน tables + Delta log size
3. ใช้ REST API → force metadata refresh
4. Vacuum + checkpoint Delta tables เป็นประจำ

---

### ERR-DATAMART-002: Datamart Deployment Pipeline Fail

**วิธีแก้:**
1. Republish "unsupported reports" ใน target workspace
2. Recreate deployment pipeline ถ้ายัง fail
3. ตรวจ permissions ครบใน target workspace

---

## 🔍 Quick Lookup Table (Full — 100 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "ambiguous column" | ERR-DAX-002 |
| "division by zero" | ERR-DAX-003 |
| "can't display" | ERR-VIS-001 |
| "too many values" | ERR-VIS-002 |
| "credentials expired" | ERR-REFRESH-002 |
| "gateway timeout" | ERR-REFRESH-001 |
| "access denied" / publish | ERR-PUB-001 |
| "Expression.Error" | ERR-PQ-001 |
| "DataFormat.Error" | ERR-PQ-002 |
| "DataSource.Error" | ERR-PQ-003 |
| "file corrupted" | ERR-FILE-001 |
| "invalid JSON" | ERR-PBIP-004 |
| "model.bim missing" | ERR-PBIP-002 |
| "RLS" / "row level" | ERR-RLS-001 |
| "OLS" / "object level" | ERR-OLS-001 |
| "slow" / "performance" | PERF-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "CapacityLimitExceeded" | ERR-EMBED-003 |
| "export PDF" failed | ERR-EXPORT-001 |
| subscription ไม่ส่ง email | ERR-SUB-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| "entity not found" dataflow | ERR-DF-001 |
| "parameter required" .pbit | ERR-PBIT-001 |
| custom visual import fail | ERR-CV-001 |
| shortcut permission | ERR-FABRIC-001 |
| deployment pipeline error | ERR-FABRIC-003 |
| paginated "processing error" | ERR-PAG-001 |
| "many-to-many" relationship | ERR-REL-001 |
| "ambiguous path" loop | ERR-REL-002 |
| mobile "content not available" | ERR-MOBILE-001 |
| R/Python script error | ERR-RPY-001 |
| map ไม่โหลด | ERR-MAP-001 |
| conditional formatting ไม่ apply | ERR-CF-001 |
| bookmark highlight ผิด | ERR-BOOKMARK-001 |
| drillthrough ไม่แสดง | ERR-DRILL-001 |
| field parameter ไม่ทำงาน | ERR-FPARAM-001 |
| sensitivity label GUID | ERR-LABEL-002 |
| Pro vs PPU limits | ERR-LIC-001 |
| Power Automate refresh | ERR-PA-001 |
| Report Server 500 | ERR-PBIRS-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "invalid theme" JSON | ERR-THEME-001 |
| slicer sync ข้ามหน้า | ERR-SLICER-001 |
| tile ไม่ refresh | ERR-TILE-001 |
| Key Influencers ไม่น่าเชื่อถือ | ERR-AI-001 |
| workspace สร้างไม่ได้ | ERR-WS-001 |
| tooltip ไม่แสดง | ERR-TOOLTIP-001 |
| auto page refresh ไม่ทำงาน | ERR-APR-001 |
| composite model / hybrid | ERR-COMPOSITE-001 |
| smart narrative ไม่สร้าง | ERR-NARRATIVE-001 |
| forecast "empty values" | ERR-FORECAST-001 |
| data alert ไม่ส่ง | ERR-ALERT-001 |
| external tool connect fail | ERR-EXTOOL-001 |
| "out of memory" | ERR-MEM-001 |
| screen reader / alt text | ERR-A11Y-001 |
| visual interaction ไม่ filter | ERR-INTERACT-001 |
| REST API 401/403 | ERR-API-001 |
| rate limit 429 | ERR-API-002 |
| PowerShell unauthorized | ERR-PS-001 |
| template app publish fail | ERR-TAPP-001 |
| What-If parameter ไม่ทำงาน | ERR-WHATIF-001 |
| CALENDARAUTO() error | ERR-DATE-001 |
| usage metrics ว่าง | ERR-USAGE-001 |
| SAP HANA driver | ERR-SAP-001 |
| Oracle ODAC missing | ERR-ORACLE-001 |
| Snowflake driver mismatch | ERR-SNOW-001 |
| Databricks driver missing | ERR-DATABRICKS-001 |
| lineage ไม่ครบ | ERR-LINEAGE-001 |
| certified grayed out | ERR-ENDORSE-001 |
| grouping/binning ผิด | ERR-GROUP-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| privacy levels ไม่ compatible | ERR-FIREWALL-001 |
| dynamic data source refresh fail | ERR-DYNSRC-001 |
| Dataverse "entity too large" | ERR-DATAVERSE-001 |
| visual calculations ไม่แสดง | ERR-VISCALC-001 |
| Report Builder semantic model | ERR-RPTBUILD-001 |
| backup / restore ไม่ได้ | ERR-BACKUP-001 |
| dynamic format string ไม่แสดง | ERR-DYNFMT-001 |
| audit log ว่าง | ERR-AUDIT-001 |
| on-object dialog หาย | ERR-ONOBJ-001 |
| multi-geo data residency | ERR-MULTIGEO-001 |
| scorecard ไม่ refresh | ERR-SCORE-001 |
| Q&A "couldn't determine" | ERR-QA-001 |
| Copilot ไม่พร้อมใช้ | ERR-QA-002 |
| Kerberos SSO fail | ERR-SSO-001 |
| SAML credentials rejected | ERR-SSO-002 |
| incremental refresh fail | ERR-INCREF-001 |
| aggregation table ไม่ถูกใช้ | ERR-AGG-001 |
| live connection แก้ model ไม่ได้ | ERR-SHARED-001 |
| dynamic M parameter ไม่ทำงาน | ERR-MPARAM-001 |
| personal gateway offline | ERR-PGATEWAY-001 |
| Azure Analysis Services 400 | ERR-AAS-001 |
| quick measure crash | ERR-QMEASURE-002 |
| calculation group pipeline fail | ERR-CALCGRP-001 |
| calc group format expression | ERR-CALCGRP-002 |
| streaming dataset 403 | ERR-STREAM-001 |
| push dataset 400 | ERR-STREAM-002 |
| Direct Lake permission error | ERR-DLAKE-001 |
| Direct Lake DQ fallback | ERR-DLAKE-002 |
| OneLake shortcut หายไป | ERR-SHORTCUT-001 |
| shortcut read error | ERR-SHORTCUT-002 |
| Analyze in Excel "no data" | ERR-AIE-001 |
| ODC file refresh fail | ERR-AIE-002 |
| App-Owns-Data CORS / 403 | ERR-APPEMBED-001 |
| embed token expired | ERR-APPEMBED-002 |
| DLP block share/export | ERR-DLP-001 |
| capacity throttling / exceeded | ERR-THROTTLE-001 |
| XMLA "no credential" | ERR-XMLA-ADV-001 |
| XMLA read/write disabled | ERR-XMLA-ADV-002 |
| Datamart SQL endpoint stale | ERR-DATAMART-001 |
| Datamart pipeline fail | ERR-DATAMART-002 |

---

## 101. Custom Connector / Data Extension Errors

### ERR-CUSTCONN-001: Custom Connector ไม่แสดงใน "Get Data"

**สาเหตุ:** .mez file ผิดที่ / Data Extensions security ปิดอยู่

**วิธีแก้:**
1. วาง `.mez` file ใน: `%USERPROFILE%\Documents\Power BI Desktop\Custom Connectors\`
2. Options → Security → Data Extensions → **"Allow any extension to load"**
3. Restart PBI Desktop
4. ⚠️ Custom connectors **ต้อง gateway** หรือ **Microsoft certification** สำหรับ Service refresh

---

### ERR-CUSTCONN-002: "We couldn't authenticate with the credentials provided"

**สาเหตุ:** Cached credentials เสียหลังใช้ครั้งแรก

**วิธีแก้:**
1. Clear cache: File → Options → Data Source Settings → Clear Permissions
2. ลอง connect ใหม่ด้วย fresh credentials
3. ตรวจ OAuth flow ถูกต้อง (ถ้าเป็น OAuth connector)

---

## 102. Managed VNet / Private Endpoint Errors

### ERR-VNET-001: "Connection was denied — Deny Public Network Access is set to Yes"

**สาเหตุ:** PBI Service ยังใช้ public endpoint แม้ตั้ง private endpoint แล้ว

**วิธีแก้:**
1. ตรวจ Managed Private Endpoint ถูก **approved** ฝั่ง Azure resource
2. ตรวจ Private DNS Zone association ถูกต้อง
3. ตรวจ Role assignments: Service Principal ต้องมี access
4. ⚠️ Region ของ Fabric capacity ต้องตรงกับ VNet region

---

### ERR-VNET-002: Managed VNet Gateway Refresh Failures (Intermittent)

**วิธีแก้:**
1. ⚠️ Known issue — bugs ใน Managed VNet Gateway (reported ตั้งแต่ 2023)
2. Retry refresh → อาจเป็น transient failure
3. ติดต่อ Microsoft Support ถ้า failure rate สูง
4. พิจารณาใช้ **On-premises Gateway** เป็น fallback

---

## 103. Table Partitioning Errors

### ERR-PARTITION-001: Hybrid Table Partitions ไม่ช่วย Performance

**สาเหตุ:** PBI queries **ทุก partition** by default → ไม่ลด load

**วิธีแก้:**
1. ใช้ `DataCoverageDefinition` บน DirectQuery partitions → ป้องกัน unnecessary queries
2. ใช้ **Tabular Editor** สำหรับ manage partitions (ไม่ใช่ PBI Desktop)
3. Monitor partition count → มากเกินไปจะเพิ่ม metadata overhead

---

### ERR-PARTITION-002: Custom Partitions + Incremental Refresh ขัดแย้ง

**วิธีแก้:**
1. ⚠️ Incremental refresh ใช้ **date column** เท่านั้น → ไม่รองรับ non-date partitioning
2. ใช้ XMLA endpoint + Tabular Editor สำหรับ custom partition management
3. อย่า mix incremental refresh policy กับ manual partitions

---

## 104. Fabric Notebook / Spark Integration Errors

### ERR-NOTEBOOK-001: "Livy Session Failed" / Notebook ค้าง

**สาเหตุ:**
- Spark auto-scaling decommission executor ที่มี checkpointed RDDs
- Large Delta merge operations
- Memory pressure

**วิธีแก้:**
1. Restart notebook session
2. ลด auto-scale range (min/max executors)
3. Checkpoint data ก่อน complex operations
4. ใช้ smaller batch sizes สำหรับ Delta merge

---

### ERR-NOTEBOOK-002: Pipeline → Notebook Fails หลัง Deploy

**สาเหตุ:** fabric-cicd deployment → broken references / metadata

**วิธีแก้:**
1. ตรวจ notebook references ยังถูกต้องหลัง deploy
2. Re-link notebook ใน pipeline activity
3. ตรวจ Lakehouse attachment ยังอยู่

---

## 105. Git Integration Errors (Fabric)

### ERR-GIT-001: "Unsupported Item Type" เมื่อ Sync ไป Git

**สาเหตุ:** บาง Fabric items ยังไม่รองรับ Git integration

**Supported Items (2025):**
| Item | Git Support |
|------|:-----------:|
| Reports | ✅ |
| Semantic Models | ✅ |
| Notebooks | ✅ |
| Pipelines | ✅ |
| Lakehouses | ⚠️ Partial |
| Dashboards | ❌ |

**วิธีแก้:**
1. ตรวจ item type ว่ารองรับ Git sync
2. ใช้ **PBIP format** สำหรับ Reports + Semantic Models
3. Manual export สำหรับ unsupported items

---

### ERR-GIT-002: Merge Conflicts ใน definition.pbir / model.bim

**วิธีแก้:**
1. ⚠️ JSON files → merge conflicts บ่อย → ใช้ **branching strategy** ที่ชัดเจน
2. ใช้ dedicated tool สำหรับ JSON merge (e.g., VS Code JSON diff)
3. model.bim → ใช้ **TMDL format** แทน (human-readable, merge-friendly)

---

## 106. Cross-Tenant / Workspace Migration Errors

### ERR-MIGRATE-001: ไม่สามารถย้าย Workspace ข้าม Tenant

**⚠️ Limitation:** PBI **ไม่รองรับ** native cross-tenant workspace migration

**วิธีแก้:**
1. Export .pbix files → re-upload ใน new tenant
2. ใช้ **Power BI REST API** สำหรับ batch export/import
3. Re-configure data sources + credentials ใน new tenant
4. ⚠️ Dashboard tiles, subscriptions, alerts → ต้องสร้างใหม่

---

## 107. Dataflow Gen2 Errors (Fabric)

### ERR-DFGEN2-001: Dataflow Gen2 Timeout / Performance Issues

**สาเหตุ:** Complex transformations + large datasets + no query folding

**วิธีแก้:**
1. ใช้ **staging Lakehouse** → land data first, transform later
2. Enable query folding where possible
3. ลด transformations ใน single dataflow → split into multiple
4. ⚠️ Dataflow Gen2 → ยังมี known performance issues (active development)

---

### ERR-DFGEN2-002: "Output destination not configured"

**วิธีแก้:**
1. ตรวจ output destination (Lakehouse / Warehouse) ถูก selected
2. ตรวจ column mapping ถูกต้อง
3. ตรวจ permissions บน destination item

---

## 108. Notification & Email Delivery Errors

### ERR-NOTIFY-001: Subscription Email ไม่ส่ง (Service)

**Checklist:**
- [ ] Recipient มี PBI Pro/PPU license
- [ ] Email address verified ใน Azure AD
- [ ] ไม่เกิน 24 subscriptions/report
- [ ] Report ไม่ใช้ RLS ที่ block recipient
- [ ] Exchange Online ไม่ block PBI emails

**วิธีแก้:**
1. ตรวจ subscription settings → schedule ถูกต้อง
2. ตรวจ spam/junk folder
3. Admin: ตรวจ Exchange Online transport rules

---

### ERR-NOTIFY-002: Teams Notification ไม่แสดง

**วิธีแก้:**
1. ตรวจ Power BI app ติดตั้งใน Teams
2. Admin: Tenant Settings → "Microsoft Teams integration" → **Enabled**
3. ตรวจ user มี access ไป report/dashboard

---

## 109. Service Principal / App Registration Errors

### ERR-SP-001: Service Principal "Unauthorized" เมื่อเรียก API

**Checklist:**
- [ ] Azure AD App Registration → API permissions granted + admin consented
- [ ] Service Principal added to **Security Group**
- [ ] Tenant Settings → "Allow service principals..." → **Enabled** สำหรับ security group
- [ ] Service Principal added to **workspace** (Contributor+)

**วิธีแก้:**
1. ตรวจ client ID + secret ถูกต้อง (secret ไม่หมดอายุ)
2. ตรวจ scope/permissions: `Workspace.Read.All`, `Dataset.ReadWrite.All`
3. ⚠️ Service principal ต้องอยู่ใน security group ที่ tenant settings อนุญาต

---

## 110. Paginated Report (SSRS) Migration Errors

### ERR-PAGMIGRATE-001: RDL File ไม่ render ถูกต้องใน PBI Service

**สาเหตุ:** PBI Service paginated reports ไม่รองรับ SSRS ทุก features

**Unsupported Features:**
| Feature | PBI Service |
|---------|:-----------:|
| Custom assemblies | ❌ |
| Embedded images (some) | ⚠️ Partial |
| Map data regions | ⚠️ Partial |
| Drillthrough to other reports (SSRS URL) | ❌ |

**วิธีแก้:**
1. ใช้ **RDL Migration Tool** (Microsoft) สำหรับ automated check
2. แก้ unsupported features ก่อน upload
3. Test render ใน Power BI Report Builder ก่อน publish
4. ⚠️ ต้องมี **Premium / PPU** capacity สำหรับ paginated reports

---

## 🔍 Quick Lookup Table (Full — 110 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "gateway timeout" | ERR-REFRESH-001 |
| "Expression.Error" | ERR-PQ-001 |
| "DataFormat.Error" | ERR-PQ-002 |
| "file corrupted" | ERR-FILE-001 |
| "invalid JSON" | ERR-PBIP-004 |
| "RLS" / "row level" | ERR-RLS-001 |
| "slow" / "performance" | PERF-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "export PDF" failed | ERR-EXPORT-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| custom visual import fail | ERR-CV-001 |
| deployment pipeline error | ERR-FABRIC-003 |
| "many-to-many" relationship | ERR-REL-001 |
| R/Python script error | ERR-RPY-001 |
| map ไม่โหลด | ERR-MAP-001 |
| bookmark highlight ผิด | ERR-BOOKMARK-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| slicer sync ข้ามหน้า | ERR-SLICER-001 |
| Key Influencers ไม่น่าเชื่อถือ | ERR-AI-001 |
| auto page refresh ไม่ทำงาน | ERR-APR-001 |
| "out of memory" | ERR-MEM-001 |
| REST API 401/403 | ERR-API-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| dynamic data source refresh fail | ERR-DYNSRC-001 |
| Dataverse "entity too large" | ERR-DATAVERSE-001 |
| visual calculations ไม่แสดง | ERR-VISCALC-001 |
| scorecard ไม่ refresh | ERR-SCORE-001 |
| Q&A "couldn't determine" | ERR-QA-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| incremental refresh fail | ERR-INCREF-001 |
| aggregation table ไม่ถูกใช้ | ERR-AGG-001 |
| live connection แก้ model ไม่ได้ | ERR-SHARED-001 |
| dynamic M parameter ไม่ทำงาน | ERR-MPARAM-001 |
| personal gateway offline | ERR-PGATEWAY-001 |
| Azure Analysis Services 400 | ERR-AAS-001 |
| quick measure crash | ERR-QMEASURE-002 |
| calculation group pipeline fail | ERR-CALCGRP-001 |
| streaming dataset 403 | ERR-STREAM-001 |
| Direct Lake permission error | ERR-DLAKE-001 |
| OneLake shortcut หายไป | ERR-SHORTCUT-001 |
| Analyze in Excel "no data" | ERR-AIE-001 |
| App-Owns-Data CORS / 403 | ERR-APPEMBED-001 |
| DLP block share/export | ERR-DLP-001 |
| capacity throttling / exceeded | ERR-THROTTLE-001 |
| XMLA "no credential" | ERR-XMLA-ADV-001 |
| Datamart SQL endpoint stale | ERR-DATAMART-001 |
| custom connector ไม่แสดง | ERR-CUSTCONN-001 |
| custom connector auth fail | ERR-CUSTCONN-002 |
| VNet "deny public access" | ERR-VNET-001 |
| managed VNet refresh fail | ERR-VNET-002 |
| partitioning ไม่ช่วย performance | ERR-PARTITION-001 |
| partition + incremental conflict | ERR-PARTITION-002 |
| Spark notebook "Livy failed" | ERR-NOTEBOOK-001 |
| notebook pipeline deploy fail | ERR-NOTEBOOK-002 |
| Git "unsupported item type" | ERR-GIT-001 |
| Git merge conflict pbir/bim | ERR-GIT-002 |
| cross-tenant migration | ERR-MIGRATE-001 |
| Dataflow Gen2 timeout | ERR-DFGEN2-001 |
| Dataflow Gen2 output missing | ERR-DFGEN2-002 |
| subscription email ไม่ส่ง | ERR-NOTIFY-001 |
| Teams notification ไม่แสดง | ERR-NOTIFY-002 |
| service principal unauthorized | ERR-SP-001 |
| RDL migration render ผิด | ERR-PAGMIGRATE-001 |

---

## 111. Object-Level Security (OLS) — Advanced Errors

### ERR-OLS-ADV-001: Visual แตกเมื่อ OLS ซ่อน Column ที่ใช้ใน Field Parameter

**สาเหตุ:** PBI ยัง "see" restricted column แม้จะถูกซ่อน → visual error

**วิธีแก้:**
1. ใช้ **Calculation Groups** → สร้าง calculation item ต่อ column (แทน field parameters)
2. ใช้ measure กับ `SWITCH(TRUE(), …)` → return ค่าตาม slicer selection
3. Duplicate table → ลบ sensitive columns → ชี้ visual ไป table ที่ปลอดภัย
4. ⚠️ Test OLS ใน **PBI Service** ("Test as Role") ไม่ใช่แค่ Desktop "View As"

---

## 112. Data Activator / Reflex Trigger Errors (Fabric)

### ERR-REFLEX-001: Reflex Alert ไม่ Trigger อัตโนมัติ (แม้ Test ผ่าน)

**สาเหตุ:** Data refresh interval (5 min), Direct Lake ต้อง manual refresh, threshold config ผิด

**วิธีแก้:**
1. ตรวจ data source refresh frequency → Data Activator check ทุก ~5 min
2. ⚠️ Direct Lake datasets → อาจต้อง manual refresh ก่อน trigger
3. Re-check threshold conditions (numeric/text/boolean เท่านั้น → ❌ datetime)

---

### ERR-REFLEX-002: "Cannot trigger actions — visual does not have measures"

**สาเหตุ:** Visual ใช้ datetime measure → Data Activator ไม่รองรับ

**วิธีแก้:**
1. Convert datetime measure → text measure (FORMAT function)
2. ใช้ numeric measure แทน (e.g., DATEDIFF)
3. ⚠️ ถ้าเจอ "Reflex - Public" disabled → admin ต้อง enable ใน Entra

---

## 113. Power Pages (Portal) Embed Errors

### ERR-PORTAL-001: "Liquid syntax error — Missing required report id in path"

**สาเหตุ:** Permission / config ผิดภายใน Power Pages Studio

**วิธีแก้:**
1. ตรวจ report ID ถูก embed อย่างถูกต้องใน Liquid tag
2. ตรวจ service principal permissions สำหรับ Power Pages embedding
3. ตรวจ RLS role mapping ถูกต้อง (ถ้าใช้ RLS)

---

### ERR-PORTAL-002: "LoadReportFailed" (404 / 403) ใน Power Pages

**วิธีแก้:**
1. HTTP 404 → ตรวจ report ID ถูกต้อง (อาจถูกลบ/ย้าย)
2. HTTP 403 → ตรวจ permissions + "Publish to web" enabled ใน tenant
3. ตรวจ embed URL format ถูกต้อง

---

## 114. Microsoft Purview / Data Governance Integration Errors

### ERR-PURVIEW-001: Power BI Assets ไม่แสดงใน Purview Data Catalog

**สาเหตุ:** Registration ไม่ครบ / scan ยังไม่ run

**วิธีแก้:**
1. Register Power BI tenant ใน Purview → ตรวจ scan สำเร็จ
2. ตรวจ service principal มี "Viewer" role ใน Purview
3. ⚠️ Data lineage อาจไม่ clickable สำหรับบาง data products (known issue)

---

## 115. Semantic Link / SemPy Errors (Fabric)

### ERR-SEMPY-001: "%pip magic command is disabled" ใน Notebook

**สาเหตุ:** Fabric persona ไม่ถูกต้อง / environment ไม่มี semantic-link library

**วิธีแก้:**
1. เลือก **Data Engineering** persona ใน Fabric
2. ตรวจ environment มี `semantic-link` library installed
3. ใช้ `%pip install semantic-link` ใน notebook cell (ถ้า magic enabled)

---

### ERR-SEMPY-002: Default Semantic Model จะถูกยกเลิก (Aug 2025)

**⚠️ สำคัญ:** PBI จะไม่สร้าง default semantic model ใหม่หลัง Aug 8, 2025

**วิธีแก้:**
1. ใช้ SemPy labs → ตรวจหา reports ที่ยังใช้ default semantic model
2. ย้ายไปใช้ explicit semantic model ก่อน deadline
3. สร้าง custom semantic model แทน default

---

## 116. Mirrored Database Errors (Fabric)

### ERR-MIRROR-001: "The database has already been mirrored on another Fabric warehouse"

**วิธีแก้:**
1. Execute `exec sp_change_feed_disable_db` บน source SQL Server
2. แล้ว re-create mirroring ใน Fabric
3. ตรวจ CDC enabled + permissions ถูกต้อง

---

### ERR-MIRROR-002: Large Table Mirroring Fails — "A task was canceled"

**สาเหตุ:** Timeout / chunking issues กับ tables ขนาดใหญ่ (50M+ rows)

**วิธีแก้:**
1. ตรวจ Fabric capacity ไม่ถูก throttle
2. ตรวจ firewall rules → allow Fabric IPs
3. ใช้ DMVs: `sys.dm_change_feed_log_scan_sessions` + `sys.dm_change_feed_errors` เพื่อ diagnose
4. ⚠️ Retry → initial replication อาจ timeout กับ very large tables

---

## 117. Conditional Access / MFA Errors

### ERR-CA-001: "AADSTS700056" — MFA / Conditional Access Block

**สาเหตุ:** Service account ถูก block โดย CA policy / MFA requirement

**วิธีแก้:**
1. Exclude service account จาก CA policy (หรือ create exception)
2. Disable Azure Security Defaults ถ้าใช้ custom CA policies
3. ตรวจ Entra ID Sign-in Logs → ดู policy ที่ block

---

### ERR-CA-002: PBI Desktop Sign-in Fail เมื่อ MFA Enabled

**วิธีแก้:**
1. Update PBI Desktop → latest version (แก้ MFA compatibility)
2. ลอง sign in ผ่าน browser (ไม่ใช่ embedded login)
3. ตรวจ device compliance ถ้า CA policy require

---

## 118. PPU / Premium Licensing Errors

### ERR-PPU-001: "Model size exceeds limit" — PPU 100 GB / Pro 1 GB

**Limits:**
| License | Max Model Size | Max Table Refresh (Gateway) |
|---------|:-------------:|:--------------------------:|
| Pro (shared) | 1 GB | 10 GB |
| PPU | 100 GB | 10 GB |
| Premium P1+ | 400 GB | Unlimited |

**วิธีแก้:**
1. Optimize model → remove unused columns/tables
2. Upgrade license tier
3. ⚠️ P-SKU retirement: ไม่ขายใหม่หลัง Jul 2024 → ย้ายไป **Fabric capacity**

---

## 119. Copilot — DAX Generation Errors

### ERR-COPILOT-001: Copilot สร้าง DAX ที่ไม่ถูกต้อง / ผลลัพธ์ผิด

**สาเหตุ:** Ambiguous prompts + poor model structure → LLM "guesses"

**วิธีแก้:**
1. เขียน prompt ที่ **specific + deterministic** (ไม่คลุมเครือ)
2. สร้าง "AI-ready" semantic model: ชื่อ field ชัดเจน, relationships ถูกต้อง, measures consistent
3. ⚠️ Copilot ≠ replacement for DAX expertise → ตรวจสอบ output เสมอ

---

### ERR-COPILOT-002: Copilot ไม่ปรากฏ / ไม่ทำงาน

**Requirements:**
- [ ] Workspace on **Fabric F64** หรือ **Premium capacity**
- [ ] Tenant Settings → Copilot → **Enabled**
- [ ] ถ้าอยู่นอก US/France → enable "Allow data processing outside geo"

**วิธีแก้:**
1. ตรวจ capacity SKU ≥ F64
2. ตรวจ tenant admin settings
3. ตรวจ geographic data processing setting

---

## 120. Autoscale / Burst Errors (Premium / Fabric)

### ERR-AUTOSCALE-001: Autoscale ไม่ Trigger แม้ Capacity > 100%

**สาเหตุ:** Algorithm optimization / carry-forward accumulated usage

**วิธีแก้:**
1. ตรวจ Autoscale **enabled** + Azure subscription linked
2. ตรวจ max v-core limit ไม่ต่ำเกินไป
3. Monitor ด้วย **Capacity Metrics App** → ดู actual CPU vs autoscale events
4. ⚠️ Autoscale ใช้ได้กับ **P-SKUs** เท่านั้น → Fabric F-SKUs ใช้ scale-up แทน

---

### ERR-AUTOSCALE-002: Autoscale Active 24+ ชม. — ค่าใช้จ่ายสูง

**วิธีแก้:**
1. ⚠️ Autoscale v-core active **minimum 24 ชม.** (ไม่ปิดทันที)
2. ตั้ง proactive + reactive limits เพื่อ control costs
3. Optimize workloads → ลด peak CPU usage
4. พิจารณา **scale-up SKU** ถ้า autoscale trigger บ่อย (ประหยัดกว่า)

---

## 🔍 Quick Lookup Table (Full — 120 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| "many-to-many" relationship | ERR-REL-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| REST API 401/403 | ERR-API-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| incremental refresh fail | ERR-INCREF-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| OneLake shortcut หายไป | ERR-SHORTCUT-001 |
| DLP block share/export | ERR-DLP-001 |
| capacity throttling | ERR-THROTTLE-001 |
| XMLA "no credential" | ERR-XMLA-ADV-001 |
| custom connector ไม่แสดง | ERR-CUSTCONN-001 |
| VNet "deny public access" | ERR-VNET-001 |
| partitioning ไม่ช่วย | ERR-PARTITION-001 |
| Spark notebook "Livy" | ERR-NOTEBOOK-001 |
| Git "unsupported item" | ERR-GIT-001 |
| cross-tenant migration | ERR-MIGRATE-001 |
| Dataflow Gen2 timeout | ERR-DFGEN2-001 |
| service principal unauthorized | ERR-SP-001 |
| RDL migration render ผิด | ERR-PAGMIGRATE-001 |
| OLS column / visual แตก | ERR-OLS-ADV-001 |
| Data Activator / Reflex ไม่ trigger | ERR-REFLEX-001 |
| Reflex "no measures" error | ERR-REFLEX-002 |
| Power Pages Liquid syntax | ERR-PORTAL-001 |
| Power Pages LoadReportFailed | ERR-PORTAL-002 |
| Purview data catalog ไม่แสดง | ERR-PURVIEW-001 |
| SemPy "%pip disabled" | ERR-SEMPY-001 |
| default semantic model deprecated | ERR-SEMPY-002 |
| mirrored database conflict | ERR-MIRROR-001 |
| mirror large table canceled | ERR-MIRROR-002 |
| MFA AADSTS700056 | ERR-CA-001 |
| PBI Desktop MFA sign-in fail | ERR-CA-002 |
| model size exceeds PPU limit | ERR-PPU-001 |
| Copilot DAX ไม่ถูกต้อง | ERR-COPILOT-001 |
| Copilot ไม่ปรากฏ | ERR-COPILOT-002 |
| autoscale ไม่ trigger | ERR-AUTOSCALE-001 |
| autoscale ค่าใช้จ่ายสูง | ERR-AUTOSCALE-002 |

---

## 121. Log Analytics / Workspace Monitoring Errors

### ERR-LOGANA-001: "Access to the resource is forbidden" — Log Analytics Connection

**สาเหตุ:** Cached expired credentials / ขาด role "Log Analytics Reader"

**วิธีแก้:**
1. Re-authenticate ใน PBI Desktop → clear credentials for `https://api.loganalytics.io`
2. ตรวจ account มี **Log Analytics Reader** หรือ **Monitoring Reader** role
3. ตรวจ workspace name, subscription ID, resource group ถูกต้อง
4. ⚠️ ถ้าใช้ AAD App Registration → ต้องมี "Log Analytics API → Data.Read" + admin consent

---

### ERR-LOGANA-002: Workspace Logging ไม่ทำงาน / ไม่แสดง Logs

**วิธีแก้:**
1. Admin → Tenant Settings → **Azure Log Analytics connections** → Enabled
2. ⚠️ รองรับเฉพาะ **Premium workspaces** + **Workspace v2** (ไม่รองรับ Classic)
3. ตรวจ KQL query ถูกต้อง → test ใน Azure Logs portal ก่อน

---

## 122. Eventstream / Real-Time Hub Errors (Fabric)

### ERR-EVSTREAM-001: 500 Internal Server Error — Custom HTTP Endpoint

**สาเหตุ:** Event Hub integration issue / endpoint config ผิด

**วิธีแก้:**
1. ตรวจ endpoint configuration ถูกต้อง
2. ตรวจ data ingestion rate → อาจต้อง rate limit / batch processing
3. ใช้ **Runtime Logs** ใน Eventstream → ดู error details

---

### ERR-EVSTREAM-002: Latency สูง (10-15 min) / Data ไม่แสดง Real-Time

**วิธีแก้:**
1. ตรวจ IoT Hub endpoint configuration
2. ลด data ingestion rate ถ้า overwhelming
3. ⚠️ Schema drift → data อาจ land ได้แต่แสดง NULL (ตรวจ data quality downstream)

---

## 123. Fabric Warehouse / Cross-Database Query Errors

### ERR-FWHOUSE-001: "Unable to connect — DataSource Error" Cross-Database Query

**สาเหตุ:** Gateway connection ชี้ไป DB เดียว → ไม่เข้าถึง DB อื่นได้

**วิธีแก้:**
1. ใช้ **SQL View** รวม data จากทั้ง 2 databases
2. ใช้ three-part naming: `DatabaseName.SchemaName.TableName`
3. ⚠️ Fabric SQL Database: cross-DB queries ใช้ได้เฉพาะผ่าน **SQL Analytics Endpoint** + same workspace

---

### ERR-FWHOUSE-002: "Value cannot be null" — Lakehouse SQL Endpoint

**สาเหตุ:** Internal reference / corrupted object metadata (transient)

**วิธีแก้:**
1. Wait + retry (อาจเป็น service-side transient issue)
2. Run metadata queries เพื่อ verify structure
3. Revert recent table deletions/renames
4. Manual refresh SQL Analytics Endpoint หลัง ETL notebooks

---

## 124. SharePoint List Connector Errors

### ERR-SPLIST-001: Delegation Warning — ข้อมูลไม่ครบ (เกิน 500/2000 rows)

**สาเหตุ:** Function ไม่ delegate → process local → ข้อมูลถูกตัด

**วิธีแก้:**
1. สร้าง **column indexes** ใน SharePoint list (สำหรับ columns ที่ filter)
2. ใช้ delegable functions: `Filter`, `LookUp` (ไม่ใช่ `Search`, `Collect`)
3. ⚠️ Lists > 5,000 items ต้อง index columns

---

### ERR-SPLIST-002: Headers แสดง "Field1, Field2" แทนชื่อจริง / ข้อมูลไม่ครบ

**วิธีแก้:**
1. Refresh data source + verify SharePoint column settings
2. Clear Power BI cache
3. ใช้ **OData Feed** แทน (`Implementation="2.0"`)
4. ⚠️ "URL" data type อาจ break API → exclude จาก Default view

---

## 125. Azure DevOps / OData Connector Errors

### ERR-DEVOPS-001: OData Query Fails กับ Custom Fields / Null Values

**สาเหตุ:** New datetime fields ยังไม่ sync กับ OData model / null in expansion

**วิธีแก้:**
1. Wait 24-48 hrs สำหรับ new custom fields → Azure DevOps internal model update
2. Handle null values: ใช้ `try-otherwise` ใน M query
3. ⚠️ Schema changes (e.g., entity rename) อาจ break existing queries

---

### ERR-DEVOPS-002: "Access is Forbidden" (403) / Refresh Timeout

**วิธีแก้:**
1. ตรวจ permissions → account ต้องมี access to Analytics
2. ตรวจ OData URL ถูกต้อง (project scope vs org scope)
3. Large datasets → เพิ่ม refresh timeout / ใช้ Premium capacity
4. ⚠️ Scheduled refresh อาจ timeout แม้ Desktop ทำงานปกติ

---

## 126. Localization / Locale / Format Errors

### ERR-LOCALE-001: Date Format ผิด (DD.MM.YYYY vs MM-DD-YYYY)

**สาเหตุ:** Regional settings mismatch ระหว่าง source / PBI / browser

**วิธีแก้:**
1. Power Query → **Change Type with Locale** (ไม่ใช่ Change Type ธรรมดา)
2. ตรวจ PBI Desktop → Options → Regional Settings → Current File
3. ⚠️ Browser regional settings อาจแสดงผลต่างจาก Desktop

---

### ERR-LOCALE-002: Number/Currency Format แสดงผิด (เช่น 1.000 vs 1,000)

**วิธีแก้:**
1. ตั้ง **Global Locale** ใน PBI Desktop Options
2. ใช้ FORMAT function ใน DAX กำหนด format string
3. สำหรับ international apps → convert currency to text format

---

## 127. Matrix / Table Visual Rendering Errors

### ERR-VISUAL-RENDER-001: Matrix Hierarchy ไม่ Expand ใน Service (แต่ Desktop ปกติ)

**สาเหตุ:** Known issue กับ field parameters ใน PBI Online / PBIRS bugs

**วิธีแก้:**
1. ⚠️ Known issue: Field parameters + matrix hierarchy ไม่ทำงานใน Service
2. ใช้ static columns แทน field parameters (workaround)
3. Update PBIRS → latest version (Jan 2025 มี matrix bug → ต้อง patch)

---

### ERR-VISUAL-RENDER-002: Matrix "Auto-size width" ทำให้ report.json ใหญ่ → Load ช้า

**สาเหตุ:** Disabled auto-size → PBI stores large Base64 strings ใน report.json

**วิธีแก้:**
1. Enable "Auto-size column width" ใน matrix visual settings
2. ตรวจ report.json file size → ถ้าใหญ่ผิดปกติ อาจเกิดจาก column widths

---

## 128. Eventhouse / KQL Errors (Fabric Real-Time Intelligence)

### ERR-EVENTHOUSE-001: Error Creating Eventhouse Destination

**สาเหตุ:** Incomplete fields / table creation ไม่ save / workspace permissions

**วิธีแก้:**
1. ตรวจ required fields ครบทุกช่อง
2. Save new table ก่อน → แล้ว assign as destination
3. Refresh browser / ใช้ incognito mode (UI glitch)
4. ตรวจ workspace permissions + objects อยู่ same workspace/region

---

### ERR-EVENTHOUSE-002: "Partial Query Failure" ใน KQL

**วิธีแก้:**
1. ตรวจ query syntax → ลอง simplify query
2. ตรวจ data volume → อาจ exceed query limits
3. ใช้ Copilot ช่วยเขียน KQL (Fabric June 2025+)

---

## 129. Deployment Pipeline — Stage / Compare Errors

### ERR-DEPLOY-001: "Stage can't perform a comparison" / Compare ค้าง

**สาเหตุ:** Browser compatibility / service-side issue

**วิธีแก้:**
1. ลอง **Firefox หรือ Edge** (Chrome อาจมีปัญหากับ comparison view)
2. Refresh pipeline view / reopen PBI Service
3. Clear browser cache + cookies
4. ⚠️ ถ้ายังไม่ได้ → recreate pipeline + reassign workspaces

---

### ERR-DEPLOY-002: Deployment ลบ Background Filters / ไม่ Push Changes

**วิธีแก้:**
1. ตรวจ **deployment rules** ถูกต้อง (parameter overrides, connection strings)
2. Manual republish content ในแต่ละ workspace
3. ⚠️ Pipeline รองรับ max 10 stages → ใช้ compare tool ดู diff ก่อน deploy

---

## 130. Report Version Compatibility / Lifecycle Errors

### ERR-VERSION-001: PBIX ไม่สามารถเปิดใน PBI Desktop เวอร์ชันเก่า

**⚠️ สำคัญ:** PBIX files **ไม่ backward-compatible** → save ใน version ใหม่ → เปิดใน version เก่าไม่ได้

**วิธีแก้:**
1. Restore older backup ของ .pbix file
2. หรือ rebuild report ใน required older Desktop version
3. สำหรับ PBIRS → ใช้ **PBIRS-aligned Desktop version** เท่านั้น

---

### ERR-VERSION-002: Semantic Model Version History / Restore

**วิธีแก้:**
1. PBI Service → semantic model → **Version History** (GA Nov 2025)
2. Auto-stores up to 5 versions → restore ได้ถ้าทำผิด
3. ⚠️ ต้องตรวจ compatibility กับ PBIRS version ถ้า publish ไป Report Server

---

## 🔍 Quick Lookup Table (Full — 130 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| "many-to-many" relationship | ERR-REL-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| REST API 401/403 | ERR-API-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| incremental refresh fail | ERR-INCREF-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| DLP block share/export | ERR-DLP-001 |
| capacity throttling | ERR-THROTTLE-001 |
| custom connector ไม่แสดง | ERR-CUSTCONN-001 |
| VNet "deny public access" | ERR-VNET-001 |
| Git "unsupported item" | ERR-GIT-001 |
| Dataflow Gen2 timeout | ERR-DFGEN2-001 |
| OLS column / visual แตก | ERR-OLS-ADV-001 |
| Data Activator / Reflex | ERR-REFLEX-001 |
| Power Pages Liquid syntax | ERR-PORTAL-001 |
| Purview data catalog | ERR-PURVIEW-001 |
| SemPy "%pip disabled" | ERR-SEMPY-001 |
| mirrored database conflict | ERR-MIRROR-001 |
| MFA AADSTS700056 | ERR-CA-001 |
| model size PPU limit | ERR-PPU-001 |
| Copilot DAX ไม่ถูกต้อง | ERR-COPILOT-001 |
| autoscale ไม่ trigger | ERR-AUTOSCALE-001 |
| Log Analytics "forbidden" | ERR-LOGANA-001 |
| workspace logging ไม่ทำงาน | ERR-LOGANA-002 |
| Eventstream 500 error | ERR-EVSTREAM-001 |
| real-time latency สูง | ERR-EVSTREAM-002 |
| cross-database query fail | ERR-FWHOUSE-001 |
| Lakehouse "value cannot be null" | ERR-FWHOUSE-002 |
| SharePoint list delegation | ERR-SPLIST-001 |
| SharePoint headers "Field1" | ERR-SPLIST-002 |
| Azure DevOps OData fail | ERR-DEVOPS-001 |
| DevOps "Access Forbidden" | ERR-DEVOPS-002 |
| date format DD.MM vs MM-DD | ERR-LOCALE-001 |
| number/currency format ผิด | ERR-LOCALE-002 |
| matrix hierarchy ไม่ expand | ERR-VISUAL-RENDER-001 |
| matrix auto-size slow | ERR-VISUAL-RENDER-002 |
| Eventhouse destination error | ERR-EVENTHOUSE-001 |
| KQL "partial query failure" | ERR-EVENTHOUSE-002 |
| deployment "can't compare" | ERR-DEPLOY-001 |
| deployment ลบ background filters | ERR-DEPLOY-002 |
| PBIX backward-incompatible | ERR-VERSION-001 |
| semantic model version history | ERR-VERSION-002 |

---

## 131. Composite Model / DirectQuery Chaining Errors

### ERR-COMPOSITE-CHAIN-001: "Error fetching data for this visual" — DQ Chain

**สาเหตุ:** Chaining ไม่ถูกต้อง / XMLA endpoint ไม่ enabled / เกิน 3 levels

**วิธีแก้:**
1. Enable **XMLA endpoints** ใน Admin Portal
2. ใน Desktop → enable "DirectQuery for PBI datasets and AS"
3. ⚠️ Max **3 levels** of chaining → ถ้าเกินจะ error
4. Schema changes upstream → ต้อง refresh composite model ใน Desktop + republish

---

## 132. Hybrid Table Errors (Import + DirectQuery)

### ERR-HYBRID-001: Hybrid Table ไม่ทำงาน / Publish ไม่ได้

**Requirements:**
- [ ] **Premium / PPU** workspace (ต้องมี XMLA endpoint)
- [ ] Compatibility level ≥ **1565**
- [ ] Data source supports **query folding**

**วิธีแก้:**
1. ตรวจ workspace เป็น Premium/PPU
2. ตั้ง compatibility level ≥ 1565 ผ่าน Tabular Editor
3. ⚠️ `dataCoverageDefinition` ใช้ได้แค่ **hard-coded dates** (ไม่ใช่ dynamic MAX)
4. Related tables → ตั้งเป็น **Dual mode** เพื่อ performance

---

## 133. Dual Mode (Import/DirectQuery) Errors

### ERR-DUAL-001: Import Table แปลงเป็น Dual Mode ไม่ได้

**สาเหตุ:** Import table ใช้ features ที่ Dual mode ไม่รองรับ

**วิธีแก้:**
1. ลบ table → recreate เป็น DirectQuery → แล้วเปลี่ยนเป็น Dual
2. ⚠️ DirectQuery limitations ยังใช้: บาง DAX functions ไม่รองรับ, Quick Insights ❌
3. Dual mode เหมาะกับ **dimension tables** (slicer/filter ใช้ cached data)

---

## 134. Power Automate Visual / Button Trigger Errors

### ERR-PA-VISUAL-001: Button ใน Report ไม่ Trigger Power Query / ไม่ส่งข้อมูลกลับ

**⚠️ Limitation:** PBI button ❌ ไม่สามารถ trigger Power Query M query ได้

**วิธีแก้:**
1. ใช้ **Power Automate flow** → trigger ผ่าน POST request
2. ⚠️ Data จาก flow ❌ ไม่สามารถ load กลับเข้า **same report** ที่ trigger
3. ใช้ Power Automate visual → configure flow ใน PBI Service (ไม่ใช่ Desktop)

---

## 135. Sensitivity Label / Information Protection Errors

### ERR-LABEL-001: "Azure Information Protection cannot apply this label"

**สาเหตุ:** OneDrive ไม่ sync / label ถูกลบ / unsupported label type

**วิธีแก้:**
1. Refresh + re-login → ensure OneDrive sync
2. Admin → Tenant Settings → **Information Protection** → Enabled
3. ⚠️ Unsupported: "Do Not Forward", "User-defined", "HYOk" labels

---

### ERR-LABEL-002: ไม่สามารถใส่ Label ได้ (ข้อจำกัดต่างๆ)

**ข้อจำกัด Sensitivity Labels:**
| ❌ ไม่รองรับ | หมายเหตุ |
|-------------|---------|
| B2B / Multi-tenant | ❌ |
| PBIRS Desktop | ❌ |
| Paginated reports (direct) | ต้อง publish ก่อน แล้วใส่ใน Service |
| Template apps | ❌ |
| .pbix > 2 GB | ❌ save ไม่ได้ |
| Labels with encryption via API | ❌ |
| Encrypted Excel files | ❌ refresh ไม่ได้ |

---

## 136. Personal Bookmark Errors

### ERR-BOOKMARK-001: Personal Bookmarks หายหลัง Report Update / Republish

**สาเหตุ:** Fields ที่ bookmark ใช้ถูกลบ/เปลี่ยนแปลง

**วิธีแก้:**
1. Re-create personal bookmarks หลัง major report updates
2. ⚠️ Bookmarks อาจไม่ sync จาก workspace → published app
3. ถ้าเจอ "Unable to Resolve Requested Application" → refresh browser + re-login

---

## 137. Azure SQL Connector Errors

### ERR-AZURESQL-001: Connection Timeout / Firewall Block

**สาเหตุ:** Port 1433 blocked / Azure SQL Serverless auto-pause / TLS mismatch

**วิธีแก้:**
1. ตรวจ firewall → allow port **1433**
2. ⚠️ Azure SQL **Serverless** → auto-pause อาจทำให้ scheduled refresh timeout
3. ใช้ FQDN (ไม่ใช่ IP) + update SQL ODBC drivers
4. เพิ่ม connection timeout value ใน PBI settings

---

### ERR-AZURESQL-002: "The underlying provider failed on open" (Sep 2024+ bug)

**วิธีแก้:**
1. Clear credentials ใน Data Source Settings → re-enter
2. Update PBI Desktop → latest version
3. ตรวจ TLS/SSL settings (ลอง disable encryption ชั่วคราว)

---

## 138. Snowflake Connector — SSO / OAuth Errors

### ERR-SNOWFLAKE-001: "Invalid OAuth access token" / Authentication Failed

**สาเหตุ:** User mapping mismatch / security integration disabled / expired token

**Checklist ตรวจสอบ:**
- [ ] Snowflake `LOGIN_NAME` = Azure AD **UPN** (ต้อง match!)
- [ ] Security integration created + **enabled** ใน Snowflake
- [ ] `external_oauth_issuer` URL ถูกต้อง
- [ ] User มี default role + role ถูก grant
- [ ] ⚠️ ถ้า map on `EMAIL_ADDRESS` → ห้าม duplicate emails

**วิธีแก้:**
1. ตรวจ LOGIN_NAME ↔ UPN mapping
2. Verify security integration parameters
3. Clear credentials ใน PBI → reconnect
4. Update PBI Desktop → latest version

---

## 139. Certificate / TLS Connection Errors

### ERR-CERT-001: "Certificate error — Invalid remote certificate"

**สาเหตุ:** Self-signed cert / expired cert / TLS version mismatch

**วิธีแก้:**
1. ตรวจ SSL certificate ยังไม่ expired
2. Import certificate เข้า trusted root store (ถ้า self-signed)
3. ตรวจ TLS version compatibility (PBI ต้องการ TLS 1.2+)
4. ⚠️ Cloud data sources (e.g., AWS PostgreSQL) → ตรวจ cert chain

---

## 140. Fabric Capacity — Pause / Resume / SKU Errors

### ERR-FABCAP-001: Capacity Paused → ทุกอย่างหยุดทำงาน

**สาเหตุ:** Admin pause capacity เพื่อประหยัดค่าใช้จ่าย → datasets/reports offline

**วิธีแก้:**
1. Resume capacity ใน **Azure Portal** → Fabric capacity resource
2. ⚠️ Pause = ทุก workloads หยุด (refresh, queries, pipelines ทั้งหมด)
3. ⚠️ Resume อาจใช้เวลา ~2-5 นาที

---

### ERR-FABCAP-002: Scale Up/Down ไม่มีผลทันที / Throttle ยังเกิดอยู่

**วิธีแก้:**
1. Scale up ใน Azure Portal → เลือก SKU ที่ใหญ่ขึ้น
2. ⚠️ Throttle อาจยังเกิดอยู่หลัง scale up เพราะ **carry-forward** accumulated usage
3. Monitor ด้วย **Capacity Metrics App** → ดู CU usage trends
4. พิจารณา workload scheduling → กระจาย peak loads

---

## 🔍 Quick Lookup Table (Full — 140 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| capacity throttling | ERR-THROTTLE-001 |
| Git "unsupported item" | ERR-GIT-001 |
| OLS column / visual แตก | ERR-OLS-ADV-001 |
| Data Activator / Reflex | ERR-REFLEX-001 |
| Purview data catalog | ERR-PURVIEW-001 |
| MFA AADSTS700056 | ERR-CA-001 |
| Copilot DAX ไม่ถูกต้อง | ERR-COPILOT-001 |
| Log Analytics "forbidden" | ERR-LOGANA-001 |
| Eventstream 500 error | ERR-EVSTREAM-001 |
| cross-database query fail | ERR-FWHOUSE-001 |
| SharePoint list delegation | ERR-SPLIST-001 |
| Azure DevOps OData fail | ERR-DEVOPS-001 |
| date format locale mismatch | ERR-LOCALE-001 |
| matrix hierarchy ไม่ expand | ERR-VISUAL-RENDER-001 |
| KQL "partial query failure" | ERR-EVENTHOUSE-002 |
| deployment "can't compare" | ERR-DEPLOY-001 |
| PBIX backward-incompatible | ERR-VERSION-001 |
| composite model chain error | ERR-COMPOSITE-CHAIN-001 |
| hybrid table ไม่ทำงาน | ERR-HYBRID-001 |
| Import → Dual mode แปลงไม่ได้ | ERR-DUAL-001 |
| PA button ไม่ trigger M query | ERR-PA-VISUAL-001 |
| sensitivity label "cannot apply" | ERR-LABEL-001 |
| sensitivity label ข้อจำกัด | ERR-LABEL-002 |
| personal bookmark หาย | ERR-BOOKMARK-001 |
| Azure SQL timeout / firewall | ERR-AZURESQL-001 |
| Azure SQL "provider failed" | ERR-AZURESQL-002 |
| Snowflake OAuth / SSO fail | ERR-SNOWFLAKE-001 |
| certificate error TLS | ERR-CERT-001 |
| Fabric capacity paused | ERR-FABCAP-001 |
| Fabric scale up ไม่มีผล | ERR-FABCAP-002 |

---

## 141. Tabular Editor Compatibility Errors

### ERR-TABED-001: Functions Greyed Out / Inoperable หลัง PBI Desktop Update

**สาเหตุ:** PBI Desktop update ทำให้ Tabular Editor ใช้งานบาง features ไม่ได้

**วิธีแก้:**
1. เปิด Tabular Editor → Preferences → enable **"Allow unsupported Power BI features"**
2. Update Tabular Editor → latest version (≥ 3.25.3)

---

### ERR-TABED-002: Save Back ไม่ทำงาน / Visuals Corrupted

**สาเหตุ:** Changes ใน TE ไม่ sync กลับ Desktop / enhanced PBIR bug

**วิธีแก้:**
1. หลัง save ใน TE → **refresh table** manually ใน PBI Desktop
2. ⚠️ "model column does not exist" → เกิดจาก PBIR preview + column formatting change
3. ปิด PBIR preview ชั่วคราว → save → เปิดใหม่

---

## 142. ALM Toolkit / Schema Compare Errors

### ERR-ALM-001: Compatibility Level Mismatch (Source vs Target)

**สาเหตุ:** Desktop file compatibility ≠ Service model (e.g., 1567 vs 1550)

**วิธีแก้:**
1. ALM Toolkit จะเสนอให้ update compatibility level → **ยอมรับ**
2. ⚠️ Backup model ผ่าน Tabular Editor ก่อน update
3. ใช้ PBI Desktop version ล่าสุดเสมอ

---

### ERR-ALM-002: Power Query Changes ไม่ถูกตรวจจับ

**⚠️ Limitation:** ALM Toolkit เน้น **metadata definition** → M code changes อาจไม่ถูก detect

**วิธีแก้:**
1. ใช้ Git diff สำหรับ Power Query M code comparison
2. ALM Toolkit เหมาะกับ metadata-only deployment (measures, columns, tables)

---

## 143. TMDL Advanced Errors

### ERR-TMDL-ADV-001: "Parsing error type - InvalidLineType"

**สาเหตุ:** TMDL files ถูก edit ด้วยมือไม่ถูกต้อง / Tabular Editor save format mismatch

**วิธีแก้:**
1. ตรวจ syntax ตาม error location ที่ PBI Desktop แจ้ง
2. ⚠️ TMSL → TMDL conversion = **irreversible** → backup ก่อน!
3. ถ้า Desktop เปิด TMDL ของ TE ไม่ได้ → ตรวจ TE version compatibility

---

### ERR-TMDL-ADV-002: Download PBIX ไม่ได้หลัง Publish จาก TMDL

**สาเหตุ:** Specific PBI Desktop version bug (e.g., July 2025)

**วิธีแก้:**
1. ลอง downgrade Desktop → previous month version
2. Republish หลัง downgrade

---

## 144. Excel Data Type Integration Errors

### ERR-EXCEL-DT-001: Rich Data Types ทำให้ Power Query Error

**สาเหตุ:** Excel rich data types (geography icons etc.) → PQ import error

**วิธีแก้:**
1. ลบ Data Type formatting ใน Excel ก่อน import
2. หรือใช้ PQ → ลบ columns ที่มี rich type ออก

---

### ERR-EXCEL-DT-002: Organization Data Types Retired (July 2025)

**⚠️ Retirement:** Organization data types ถูก retired เมื่อ July 31, 2025

**วิธีแก้:**
1. เปลี่ยนไปใช้ **Get Data > From Power BI** แทน
2. Data เก่าจะยังอยู่แต่ ❌ ไม่ refresh แล้ว

---

## 145. Embed Token / Effective Identity Errors

### ERR-EMBEDTOKEN-001: "Shouldn't have effective identity"

**สาเหตุ:** ส่ง `identities` section ทั้งที่ dataset ไม่ต้องการ / ไม่ใช่ DQ+RLS

**วิธีแก้:**
1. ลบ `identities` ออกจาก request body (ถ้าไม่ใช้ DQ + RLS)
2. ถ้าใช้ Service Principal → `EffectiveIdentity.username` = **SP Object ID** (ไม่ใช่ App Registration ID!)
3. ⚠️ SSO semantic model → ต้องมี contextual identity

---

## 146. Dynamic RLS — USERNAME / USERPRINCIPALNAME Errors

### ERR-DYNRLS-001: RLS ไม่ Filter / ไม่ทำงาน

**สาเหตุ:** DAX function ใช้ผิด / UPN mismatch / role ไม่ได้ assign

**วิธีแก้:**
1. ใช้ **`USERPRINCIPALNAME()`** (ไม่ใช่ `USERNAME()`) → consistent ทั้ง Desktop + Service
2. `USERNAME()` ใน Desktop = `DOMAIN\user` แต่ใน Service = UPN → **ไม่ consistent!**
3. ⚠️ Assign RLS roles ใน **PBI Service** (ไม่ใช่ Desktop)
4. ตรวจ mapping table match กับ UPN exactly (case-sensitive!)

---

### ERR-DYNRLS-002: "USERPRINCIPALNAME is not a function"

**สาเหตุ:** ใช้ PBI Desktop **Report Server** edition (ไม่รองรับ)

**วิธีแก้:**
1. PBIRS Desktop → ใช้ `USERNAME()` แทน
2. หรือเปลี่ยนใช้ regular PBI Desktop

---

## 147. SAP HANA Connector Errors

### ERR-SAPHANA-001: SSO (Kerberos/SAML) Authentication Failed

**สาเหตุ:** SPN misconfigured / ODBC driver เก่า / TLS cert error

**วิธีแก้:**
1. Update SAP HANA ODBC driver ≥ **2.00.020.00**
2. ตรวจ SPN configuration + service account
3. ⚠️ SAML SSO → ใช้ได้เฉพาะผ่าน **On-Premises Gateway** (ไม่ใช่ Desktop โดยตรง)
4. Desktop direct → ใช้ Kerberos เท่านั้น

---

### ERR-SAPHANA-002: "Edit variables not working" / Gateway Error

**วิธีแก้:**
1. ตรวจ gateway installation + update latest version
2. Verify SAML/Kerberos configuration ใน gateway settings
3. ตรวจ DirectQuery mode (AAD SSO for HANA → DQ only)

---

## 148. Tenant Settings / Admin Portal Errors

### ERR-TENANT-001: Tenant Settings ไม่แสดง / หน้าว่าง

**สาเหตุ:** ไม่มี admin role ที่เหมาะสม

**วิธีแก้:**
1. ต้องเป็น: **Global Admin**, **Fabric Admin**, หรือ **PBI Service Admin**
2. ⚠️ Feature ใหม่อาจ deploy โดยไม่มี notification → ตรวจ Tenant settings เป็นประจำ

---

### ERR-TENANT-002: "Publish to Web" ไม่มี / Disabled

**วิธีแก้:**
1. Admin Portal → Tenant Settings → **"Publish to Web"** → Enable
2. ⚠️ Security risk → เปิดเฉพาะ specific security groups
3. ⚠️ Publish to Web = **public** → ไม่มี authentication!

---

## 149. Workspace Roles & Permission Errors

### ERR-WSROLE-001: User ทำงานไม่ได้ / Permission Denied

**ตาราง Roles:**
| Role | View | Create/Edit | Share | Manage Users |
|------|------|-------------|-------|-------------|
| Viewer | ✅ | ❌ | ❌ | ❌ |
| Contributor | ✅ | ✅ | ❌ | ❌ |
| Member | ✅ | ✅ | ✅ | ✅ (Viewer/Contributor) |
| Admin | ✅ | ✅ | ✅ | ✅ (ทุก role) |

**วิธีแก้:**
1. ตรวจ role ตรงกับงานที่ต้องทำ
2. ⚠️ Viewer ใน **Premium capacity** → ไม่ต้องมี Pro license!
3. ⚠️ Content creation ยังต้องมี **Pro/PPU** license แม้จะมี role

---

## 150. PDF Export Errors

### ERR-PDF-001: Content ถูกตัด / Truncated ใน PDF Export

**สาเหตุ:** Report ออกแบบสำหรับ scroll → PDF เป็น static snapshot

**วิธีแก้:**
1. ออกแบบ report ด้วย **print layout** → canvas size 16:9 หรือ A4
2. ⚠️ Multi-page table → ใช้ **Paginated Report** แทน
3. ปรับ visual size ให้พอดี printable area

---

### ERR-PDF-002: Custom Visuals ไม่แสดงใน PDF

**สาเหตุ:** Non-certified visuals render ❌ ใน export / WebView2 issue

**วิธีแก้:**
1. ใช้เฉพาะ **Microsoft-certified** custom visuals
2. ⚠️ Known issue (Oct 2025) → ลอง export จาก **PBI Service** แทน Desktop
3. Update/repair **WebView2** component

---

### ERR-PDF-003: Export ล้มเหลว / HTTP 403 / Timeout

**สาเหตุ:** Token expired / PPU license + non-Premium workspace / random failure

**วิธีแก้:**
1. Re-login → refresh token
2. ⚠️ Power Automate PDF export → ต้อง **Premium capacity** workspace (PPU ไม่พอ)
3. Update PBI Desktop → latest version
4. ลอง export ผ่าน browser อื่น

---

## 🔍 Quick Lookup Table (Full — 150 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| capacity throttling | ERR-THROTTLE-001 |
| Git "unsupported item" | ERR-GIT-001 |
| OLS column / visual แตก | ERR-OLS-ADV-001 |
| Data Activator / Reflex | ERR-REFLEX-001 |
| Purview data catalog | ERR-PURVIEW-001 |
| MFA AADSTS700056 | ERR-CA-001 |
| Copilot DAX ไม่ถูกต้อง | ERR-COPILOT-001 |
| Log Analytics "forbidden" | ERR-LOGANA-001 |
| Eventstream 500 error | ERR-EVSTREAM-001 |
| cross-database query fail | ERR-FWHOUSE-001 |
| SharePoint list delegation | ERR-SPLIST-001 |
| Azure DevOps OData fail | ERR-DEVOPS-001 |
| date format locale mismatch | ERR-LOCALE-001 |
| matrix hierarchy ไม่ expand | ERR-VISUAL-RENDER-001 |
| KQL "partial query failure" | ERR-EVENTHOUSE-002 |
| deployment "can't compare" | ERR-DEPLOY-001 |
| PBIX backward-incompatible | ERR-VERSION-001 |
| composite model chain error | ERR-COMPOSITE-CHAIN-001 |
| hybrid table ไม่ทำงาน | ERR-HYBRID-001 |
| Import → Dual mode แปลงไม่ได้ | ERR-DUAL-001 |
| PA button ไม่ trigger M query | ERR-PA-VISUAL-001 |
| sensitivity label "cannot apply" | ERR-LABEL-001 |
| personal bookmark หาย | ERR-BOOKMARK-001 |
| Azure SQL timeout / firewall | ERR-AZURESQL-001 |
| Snowflake OAuth / SSO fail | ERR-SNOWFLAKE-001 |
| certificate error TLS | ERR-CERT-001 |
| Fabric capacity paused | ERR-FABCAP-001 |
| Tabular Editor greyed out | ERR-TABED-001 |
| TE save back / visual corrupt | ERR-TABED-002 |
| ALM compatibility mismatch | ERR-ALM-001 |
| ALM PQ changes ไม่ detect | ERR-ALM-002 |
| TMDL parsing error | ERR-TMDL-ADV-001 |
| TMDL download PBIX fail | ERR-TMDL-ADV-002 |
| Excel rich data type PQ error | ERR-EXCEL-DT-001 |
| Organization data types retired | ERR-EXCEL-DT-002 |
| embed "shouldn't have identity" | ERR-EMBEDTOKEN-001 |
| USERPRINCIPALNAME RLS fail | ERR-DYNRLS-001 |
| "not a function" PBIRS | ERR-DYNRLS-002 |
| SAP HANA SSO / Kerberos | ERR-SAPHANA-001 |
| SAP HANA variables gateway | ERR-SAPHANA-002 |
| tenant settings ไม่แสดง | ERR-TENANT-001 |
| Publish to Web disabled | ERR-TENANT-002 |
| workspace role permission | ERR-WSROLE-001 |
| PDF truncated / cut off | ERR-PDF-001 |
| PDF custom visuals blank | ERR-PDF-002 |
| PDF export 403 / timeout | ERR-PDF-003 |

---

## 151. Power BI REST API Errors (403 / Unauthorized)

### ERR-API-ADV-001: 403 Forbidden เมื่อเรียก REST API

**สาเหตุ:** Permission scope ไม่ครบ / token expired / SP ไม่มี workspace role

**Checklist ตรวจสอบ:**
- [ ] App Registration มี scopes: `Dataset.Read.All`, `Report.Read.All`, etc.
- [ ] **Admin consent** ได้รับแล้ว
- [ ] Service Principal มี **Admin role** ใน workspace
- [ ] Tenant Settings → "Service principals can use Fabric API" → **Enabled**

**วิธีแก้:**
1. ตรวจ scopes + admin consent
2. เพิ่ม SP เข้า workspace ด้วย Admin role
3. ⚠️ Token expired → re-authenticate
4. ถ้า timeout → ใช้ `preferClientRouting=true` ใน URL

---

## 152. PowerShell Cmdlets / MicrosoftPowerBIMgmt Errors

### ERR-PSCMD-001: "One or more errors occurred" — Connect-PowerBIServiceAccount

**สาเหตุ:** Module version conflict / TLS issue / assembly loading error

**วิธีแก้:**
1. Update module: `Install-Module MicrosoftPowerBIMgmt -Force -AllowClobber`
2. ตั้ง TLS: `[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12`
3. ⚠️ Conflict กับ `Az.Accounts` → ลอง `pwsh.exe -noprofile`
4. ถ้ายังไม่ได้ → uninstall + ลบ folder ใน `WindowsPowerShell\Modules` + reinstall

---

## 153. Image URL / Broken Image Errors

### ERR-IMGURL-001: รูปภาพไม่แสดง / Broken Image Icon

**สาเหตุ:** URL ไม่ public / HTTP vs HTTPS / caching issue

**วิธีแก้:**
1. ตรวจ image URL เป็น **publicly accessible** (ไม่ต้อง login)
2. ใช้ **HTTPS** แทน HTTP
3. ⚠️ SharePoint images ต้องมี anonymous access หรือ convert เป็น **Base64**
4. Image ไม่ update → เพิ่ม `?t=` + random parameter ใน URL เพื่อ bypass cache
5. ตั้ง Data Category → **"Image URL"** ใน Modeling tab

---

## 154. Field Parameter Errors

### ERR-FIELDPARAM-001: Visual ว่าง / AI Visual ไม่รองรับ Field Parameter

**ข้อจำกัด:**
| ❌ ไม่รองรับ | หมายเหตุ |
|-------------|---------|
| Key Influencers (Analyze field) | ❌ AI visuals |
| Excel queries | Client-side feature only |
| Live Connection → DQ conversion | ต้องเพิ่ม `JsonExtendedProperty` ผ่าน TE |

**วิธีแก้:**
1. ใช้ **measures** (SUM, COUNT) แทน raw columns ใน field parameters
2. `SELECTEDVALUE` error → ตรวจ "Group By Columns" property
3. ⚠️ Paginated reports + calc groups → สร้าง helper parameter table

---

## 155. Smart Narrative / Narrative Visual Errors

### ERR-NARRATIVE-001: "Summary not available" / "Couldn't load data"

**สาเหตุ:** Unsupported visuals / browser caching / visual renamed

**วิธีแก้:**
1. ⚠️ **Renamed:** "Smart Narrative" → **"Narrative"** (July 2025+)
2. Clear browser cache / ใช้ incognito
3. ต้องมี ≥ 1 supported visual ใน page (ไม่ใช่ custom/R/Python/map)
4. ถ้าหา visual ไม่เจอ → reinstall PBI Desktop

---

## 156. Anomaly Detection Errors

### ERR-ANOMALY-001: "No anomalies" / "Analysis returned no results"

**สาเหตุ:** Sensitivity ต่ำเกินไป / data ไม่พอ / unsupported scenario

**Requirements:**
- [ ] **Line chart** only + time series on Axis
- [ ] ≥ **4 data points**
- [ ] ❌ ไม่รองรับ: legends, multiple values, DQ over SAP, PBIRS, Live Connection AAS

**วิธีแก้:**
1. เพิ่ม **sensitivity** ใน Find Anomalies format tab
2. เพิ่ม data points / ขยาย time range
3. ถ้า error → reset default settings ใน format tab

---

## 157. Key Influencers Visual Errors

### ERR-KEYINF-001: "Couldn't load data" / Field Relationship Error

**สาเหตุ:** Explain by ไม่อยู่ same table / ไม่มี many-to-one relationship / PBI เก่า

**ข้อจำกัด:**
| ❌ ไม่รองรับ | หมายเหตุ |
|-------------|---------|
| Direct Query | ❌ |
| Live Connection (AAS/SSAS) | ❌ |
| Publish to Web | ❌ |
| Field Parameters as Analyze | ❌ |

**วิธีแก้:**
1. ตรวจ relationship เป็น **many-to-one** จาก Explain by → Analyze table
2. ลอง summarize field ที่ error
3. Update PBI Desktop → latest version

---

## 158. Date Table / Auto Date/Time Errors

### ERR-DATETABLE-001: CALENDARAUTO ไม่ work / Circular Dependency / Blank Value Error

**สาเหตุ:** Blank dates / outlier dates ทำให้ CALENDARAUTO สร้าง table ใหญ่เกินไป

**Best Practice:**
1. ❌ **ปิด Auto Date/Time** → File > Options > Data Load → uncheck
2. ✅ ใช้ `CALENDAR(start, end)` แทน `CALENDARAUTO()` → ควบคุม range ได้
3. **Mark as Date Table** → Modeling > Mark as Date Table
4. ⚠️ "Start date cannot be Blank" → ตรวจ blank/null dates ใน source

---

## 159. Google BigQuery Connector Errors

### ERR-BIGQUERY-001: Authentication Failed / Storage API Error

**สาเหตุ:** OAuth embedded browser deprecated / Storage API ไม่ enabled / scope ไม่ครบ

**วิธีแก้:**
1. ใช้ PBI Desktop **June 2021+** (Google blocked embedded browser sign-in)
2. ⚠️ "Unable to authenticate with Storage API" → ตั้ง `UseStorageApi = false` ใน M code
3. Enterprise → ใช้ **Service Account** + JSON key file ผ่าน Gateway
4. ⚠️ New ADBC driver (May 2025+ preview) → ลองใช้ถ้า performance ไม่ดี

---

## 160. Oracle Connector Errors (ORA- / TNS)

### ERR-ORACLE-001: ORA-12154 "TNS: could not resolve connect identifier"

**สาเหตุ:** TNSNAMES.ora ไม่ถูกต้อง / Oracle client ไม่ match / PATH ไม่ตั้ง

**วิธีแก้:**
1. ตรวจ `TNSNAMES.ora` → connect identifier ตรงกับที่ใส่ใน PBI
2. ตั้ง environment variables: `PATH` + `TNS_ADMIN` → ชี้ไปที่ Oracle client
3. ใช้ **64-bit Oracle Instant Client** (match กับ PBI Desktop 64-bit)
4. ⚠️ PBI จาก **Microsoft Store** → อาจ error "Object reference not set"
   → ใช้ PBI จาก **Download Center** แทน

---

### ERR-ORACLE-002: ORA-12170 / ORA-50000 Connection Timeout

**วิธีแก้:**
1. ตรวจ firewall → port Oracle (1521) ไม่ถูก block
2. ตรวจ TNSNAMES.ora configuration
3. ⚠️ Sep 2025 Desktop → ลอง disable preview features ที่เพิ่ง activate

---

## 🔍 Quick Lookup Table (Full — 160 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| capacity throttling | ERR-THROTTLE-001 |
| Git "unsupported item" | ERR-GIT-001 |
| MFA AADSTS700056 | ERR-CA-001 |
| Copilot DAX ไม่ถูกต้อง | ERR-COPILOT-001 |
| composite model chain | ERR-COMPOSITE-CHAIN-001 |
| hybrid table | ERR-HYBRID-001 |
| sensitivity label | ERR-LABEL-001 |
| Azure SQL timeout | ERR-AZURESQL-001 |
| Snowflake OAuth | ERR-SNOWFLAKE-001 |
| Tabular Editor greyed out | ERR-TABED-001 |
| ALM compatibility | ERR-ALM-001 |
| TMDL parsing | ERR-TMDL-ADV-001 |
| embed effective identity | ERR-EMBEDTOKEN-001 |
| USERPRINCIPALNAME RLS | ERR-DYNRLS-001 |
| SAP HANA SSO | ERR-SAPHANA-001 |
| tenant settings blank | ERR-TENANT-001 |
| workspace role permission | ERR-WSROLE-001 |
| PDF truncated | ERR-PDF-001 |
| REST API 403 unauthorized | ERR-API-ADV-001 |
| PowerShell Connect-PBI error | ERR-PSCMD-001 |
| broken image URL | ERR-IMGURL-001 |
| field parameter blank visual | ERR-FIELDPARAM-001 |
| smart narrative / summary | ERR-NARRATIVE-001 |
| anomaly detection no results | ERR-ANOMALY-001 |
| key influencer "couldn't load" | ERR-KEYINF-001 |
| CALENDARAUTO / auto date | ERR-DATETABLE-001 |
| BigQuery authentication | ERR-BIGQUERY-001 |
| Oracle ORA-12154 TNS | ERR-ORACLE-001 |
| Oracle ORA-12170 timeout | ERR-ORACLE-002 |

---

## 161. Databricks Connector Errors

### ERR-DATABRICKS-001: PAT Expired / OAuth Token Refresh Failed / Cluster Inactive

**สาเหตุ:** Personal Access Token หมดอายุ / cluster auto-terminated / hostname ผิด

**วิธีแก้:**
1. ตรวจ PAT → generate ใหม่จาก Databricks User Settings
2. ตรวจ **Server Hostname** + **HTTP Path** ให้ตรงกับ JDBC/ODBC settings
3. ⚠️ Cluster auto-terminate → schedule query ก่อน refresh เพื่อ wake up cluster
4. `DMTS_OAuthTokenRefreshFailedError` → ตรวจ OAuth token expiration + re-auth ใน PBI Service
5. Desktop ✅ แต่ Service ❌ → re-enter credentials ใน Service data source settings
6. ✅ **แนะนำ:** ใช้ SQL Warehouse แทน Job Cluster (ดีกว่าสำหรับ BI workloads)

---

## 162. MySQL Connector Errors (SSL / Handshake)

### ERR-MYSQL-001: SSL Handshake Failed / Connection Refused

**สาเหตุ:** PBI Service บังคับ encrypted connection / MySQL .NET connector เก่า / TLS mismatch

**วิธีแก้:**
1. ตรวจ MySQL server → enable SSL/TLS ถ้า PBI Service ต้องการ
2. Update **MySQL .NET Connector** → latest version
3. ⚠️ Desktop ✅ แต่ Service ❌ → Service อาจบังคับ encryption ที่ Desktop ไม่ได้
4. Clear cached credentials → File > Options > Data Source Settings > Clear Permissions
5. ตรวจ server name ตรงกับ SSL certificate

---

## 163. PostgreSQL / Npgsql Connector Errors

### ERR-PGSQL-001: Npgsql Driver Error / Connection Refused

**สาเหตุ:** Npgsql version ไม่ compatible / GAC ไม่ได้ติดตั้ง / pg_hba.conf ไม่อนุญาต

**วิธีแก้:**
1. Install Npgsql → ✅ **เลือก "GAC Installation"** ตอน install
2. ⚠️ Oct 2024 PBI Desktop → Npgsql 4.0.16 มีปัญหา → ใช้ 4.0.10 หรือ 4.0.17
3. ตรวจ `pg_hba.conf` → อนุญาต IP ของ PBI machine + auth method (md5/scram-sha-256)
4. Connection refused → ตรวจ host, port (5432), firewall
5. ถ้าต้องการ SSL → enable ใน connection settings + ให้ cert

---

## 164. Web Connector Errors (403 Forbidden / Dynamic Content)

### ERR-WEBCONN-001: "Access to resource forbidden" / 403 Error

**สาเหตุ:** Server block non-browser requests / cached permissions / privacy settings

**วิธีแก้:**
1. เพิ่ม **User-Agent header** ใน `Web.Contents` options
2. Clear permissions → Data Source Settings > Clear Permissions
3. ⚠️ Privacy Levels → ลอง "Ignore privacy levels" ใน Options > Privacy
4. Dynamic content (JS-rendered) → ใช้ `Web.BrowserContents` แทน `Web.Contents`
5. ถ้ามี API available → ใช้ API แทน web scraping (เสถียรกว่า)

---

## 165. Decomposition Tree Errors

### ERR-DECOMP-001: "Couldn't load data" / AI Splits ไม่ทำงาน

**สาเหตุ:** Composite model / query ซับซ้อนเกินไป / ข้อจำกัดของ AI splits

**ข้อจำกัด AI Splits:**
| ❌ ไม่รองรับ | หมายเหตุ |
|-------------|---------|
| Azure Analysis Services | ❌ |
| Power BI Report Server | ❌ |
| Publish to Web | ❌ |
| Complex measures (บางกรณี) | อาจ error |

**วิธีแก้:**
1. ลดความซับซ้อนของ measure / จำกัด tables ที่ reference
2. ตรวจ data model relationships
3. ⚠️ Query processor resource error → ลด data volume

---

## 166. Waterfall Chart Errors

### ERR-WATERFALL-001: Breakdown ไม่แสดง / Negative Values ผิดพลาด

**สาเหตุ:** Categories มากเกินไป / data format ไม่ถูกต้อง

**วิธีแก้:**
1. จำกัดจำนวน categories → ไม่ควรเกิน 10-15 เพื่อให้อ่านง่าย
2. ⚠️ Negative values → ตรวจ data type เป็น numeric + sign ถูกต้อง
3. Breakdown field → ต้องเป็น categorical (ไม่ใช่ continuous)
4. ✅ ใช้ waterfall สำหรับ margin breakdown → ดีกว่า doughnut สำหรับ negative numbers

---

## 167. Performance Analyzer Errors

### ERR-PERFANALYZE-001: ผลลัพธ์ไม่ consistent / Visual ช้า

**สาเหตุ:** Cache ทำให้ผลลัพธ์ผิด / DAX ซับซ้อน / update ใหม่ทำให้ช้า

**วิธีใช้ Performance Analyzer ถูกต้อง:**
1. **Clear cache ก่อนทุกครั้ง** → เพื่อ consistent results
2. Copy DAX query → วิเคราะห์ใน **DAX Studio** เพื่อหา bottleneck
3. ดู breakdown → DAX query time vs. visual rendering time
4. ⚠️ หลัง update → ถ้าช้าลง → ลองลดความซับซ้อน DAX + clear cache

---

## 168. Query Diagnostics Errors

### ERR-QUERYDIAG-001: ไม่บันทึกทุก Steps / Slow Query ไม่ทราบสาเหตุ

**สาเหตุ:** Tracing ไม่ enabled / data cache / query ไม่ fold

**วิธีแก้:**
1. Enable Query Diagnostics → Tools > Diagnostics > Start Diagnostics
2. ⚠️ ไม่บันทึกทุก steps → ลอง disable other queries + clear data cache
3. DirectQuery slow → ใช้ Performance Analyzer + ดู SQL ที่ส่งไป source
4. ✅ ตรวจ query folding → ถ้า fold ไม่ได้ = performance จะแย่

---

## 169. Report Theme / Custom JSON Errors

### ERR-THEME-001: Theme JSON Import Error / Format ผิด

**สาเหตุ:** JSON syntax error / unsupported properties / visual override

**วิธีแก้:**
1. ตรวจ **JSON syntax** → missing comma, quotes, brackets
2. ใช้ JSON validator ก่อน import
3. ⚠️ Unsupported fields → PBI จะแสดง error message บอก field ที่ผิด
4. Theme ไม่ apply → visual formatting อาจ **override** theme → reset visual to default
5. ✅ Mar 2025+ → รองรับ **style presets** ใน JSON themes

---

## 170. Data Profiling Errors (Column Quality / Distribution)

### ERR-PROFILE-001: Data Quality Issues ไม่แสดง / Sample ไม่ครบ

**สาเหตุ:** Default = sample first 1,000 rows เท่านั้น

**วิธีแก้:**
1. ⚠️ **เปลี่ยน sampling** → status bar ใน PQ Editor → "Based on entire dataset"
2. Column Quality แสดง: Valid (🟢) / Error (🔴) / Empty (⬛)
3. Error พบ → คลิกขวา → "Remove Errors" หรือ "Replace Errors"
4. ✅ ตรวจ data types → เช่น text ใน number column = error
5. Column Distribution → ดู distinct vs unique count เพื่อหา duplicates

---

## 🔍 Quick Lookup Table (Full — 170 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| capacity throttling | ERR-THROTTLE-001 |
| Git "unsupported item" | ERR-GIT-001 |
| MFA AADSTS700056 | ERR-CA-001 |
| Copilot DAX ไม่ถูกต้อง | ERR-COPILOT-001 |
| composite model chain | ERR-COMPOSITE-CHAIN-001 |
| hybrid table | ERR-HYBRID-001 |
| sensitivity label | ERR-LABEL-001 |
| Azure SQL timeout | ERR-AZURESQL-001 |
| Snowflake OAuth | ERR-SNOWFLAKE-001 |
| Tabular Editor greyed out | ERR-TABED-001 |
| ALM compatibility | ERR-ALM-001 |
| TMDL parsing | ERR-TMDL-ADV-001 |
| embed effective identity | ERR-EMBEDTOKEN-001 |
| USERPRINCIPALNAME RLS | ERR-DYNRLS-001 |
| SAP HANA SSO | ERR-SAPHANA-001 |
| tenant settings blank | ERR-TENANT-001 |
| workspace role permission | ERR-WSROLE-001 |
| PDF truncated | ERR-PDF-001 |
| REST API 403 unauthorized | ERR-API-ADV-001 |
| PowerShell Connect-PBI error | ERR-PSCMD-001 |
| broken image URL | ERR-IMGURL-001 |
| field parameter blank visual | ERR-FIELDPARAM-001 |
| smart narrative / summary | ERR-NARRATIVE-001 |
| anomaly detection no results | ERR-ANOMALY-001 |
| key influencer "couldn't load" | ERR-KEYINF-001 |
| CALENDARAUTO / auto date | ERR-DATETABLE-001 |
| BigQuery authentication | ERR-BIGQUERY-001 |
| Oracle ORA-12154 TNS | ERR-ORACLE-001 |
| Databricks PAT / OAuth | ERR-DATABRICKS-001 |
| MySQL SSL handshake | ERR-MYSQL-001 |
| PostgreSQL Npgsql driver | ERR-PGSQL-001 |
| web connector 403 forbidden | ERR-WEBCONN-001 |
| decomposition tree AI splits | ERR-DECOMP-001 |
| waterfall breakdown negative | ERR-WATERFALL-001 |
| performance analyzer slow | ERR-PERFANALYZE-001 |
| query diagnostics trace | ERR-QUERYDIAG-001 |
| report theme JSON format | ERR-THEME-001 |
| data profiling column quality | ERR-PROFILE-001 |

---

## 171. Drill-Through Errors

### ERR-DRILLTHRU-001: No Data / Cross-Report Drill-Through ไม่ทำงาน

**สาเหตุ:** Column names ไม่ตรงกันระหว่าง reports / ไม่ได้ enable cross-report / ใช้ measure แทน column

**วิธีแก้:**
1. ตรวจ **column names + table names** ตรงกันใน source & target datasets
2. Enable: File > Options > Report settings > "Allow visuals to use drill through from other reports"
3. ⚠️ Drill-through field ต้องเป็น **categorical column** ไม่ใช่ measure
4. ตรวจ data model relationships ให้ถูกต้อง

---

## 172. Report Page Tooltip Errors

### ERR-TOOLTIP-001: Tooltip ไม่แสดง / แสดงข้อมูลผิด

**สาเหตุ:** PBI Desktop เก่า / blank card / Service vs Desktop bug / filter settings

**วิธีแก้:**
1. Update PBI Desktop → latest version
2. ⚠️ Blank card visual → ใส่ space (" ") เพื่อให้ tooltip trigger ได้
3. Desktop ✅ แต่ Service ❌ → ลอง republish report
4. ข้อมูลผิด → ตรวจ "Keep all filters" setting ใน tooltip page
5. "Loading Report Page Tooltip" ค้าง → clear browser cache

---

## 173. Bookmark Navigator Errors

### ERR-BOOKMARK-001: Navigator ไม่ reset state / Button highlight ผิด

**สาเหตุ:** Known limitation — navigator จำ last selection ไว้

**วิธีแก้:**
1. ⚠️ **Known issue since 2021** → Navigator จะไม่ reset highlight เมื่อ apply bookmark อื่น
2. **Workaround:** ใช้ individual buttons + Selection Pane แทน bookmark navigator
3. Bookmark break → ตรวจว่า field names ไม่ได้เปลี่ยน (rename field = bookmark พัง)
4. ✅ สร้าง "Reset" bookmark → ใช้เป็น clear-all-filters button

---

## 174. Sync Slicers Errors

### ERR-SYNCSLICER-001: Slicer ไม่ sync ข้ามหน้า / Reset เมื่อเปลี่ยนหน้า

**สาเหตุ:** Recurring bug ใน Org Apps / New Slicer visual bug / button navigation issue

**วิธีแก้:**
1. ⚠️ **New Slicer** อาจไม่ sync ผ่าน button/page navigator → ลอง old slicer type
2. Fix: ลบ slicers ทั้งหมด → สร้างใหม่ 1 ตัว → copy paste ไปหน้าอื่น → เปิด Sync ทุกหน้า → republish
3. ⚠️ Bug: remove filter ไม่ sync (late 2024) → filter apply sync ได้ แต่ clear ไม่ sync
4. Org App → slicer reset เมื่อ navigate → known recurring bug

---

## 175. Q&A Visual Errors

### ERR-QA-001: Q&A ไม่เข้าใจคำถาม / ผลลัพธ์ผิด

**สาเหตุ:** Data model ไม่ structured ดี / relationships ผิด / column names ไม่ชัดเจน

**วิธีแก้:**
1. ตั้งชื่อ columns ให้ **human-readable** (เช่น "Sales Amount" ไม่ใช่ "col_sa")
2. สร้าง **synonyms** → Modeling > Q&A Setup > Teach Q&A
3. ตรวจ relationships ระหว่าง tables ให้ถูกต้อง
4. ⚠️ Q&A ต้องการ well-structured star schema → ไม่เหมาะกับ flat tables

---

## 176. Paginated Reports / Subreport Errors

### ERR-PAGINATED-001: "Subreport could not be processed" / Query Execution Failed

**สาเหตุ:** Version mismatch ระหว่าง main report + subreport / user ไม่มี DB access

**วิธีแก้:**
1. ⚠️ Subreport error → ตรวจว่า main report + subreport ใช้ **same processor version**
2. "Query execution failed for dataset" → ตรวจ user permissions บน underlying DB
3. ❌ SSRS shared datasets (.rds/.rsd) ไม่รองรับใน PBI Service
4. ✅ ใช้ Power BI semantic model เป็น data source แทน

---

## 177. Subscription / Email Errors

### ERR-SUBSCRIPTION-001: Email ไม่ส่ง / Attachment เก่า / เกิน Limit

**สาเหตุ:** Dataset refresh failed / attachment > 25MB / recipients > 1000

**ข้อจำกัด:**
| Limit | ค่า |
|-------|-----|
| Attachment pages | ≤ 20 pages |
| Attachment size | < 25 MB |
| Dynamic recipients | ≤ 1,000 |

**วิธีแก้:**
1. ⚠️ "After data refresh" → ถ้า refresh fail = subscription ไม่ส่ง
2. Attachment ข้อมูลเก่า → ตรวจ dataset refresh schedule
3. Custom visuals อาจ distorted ใน email
4. Recipients ต้องมี **permissions** ดู report ใน PBI Service

---

## 178. App Distribution / Audience Errors

### ERR-APP-001: Audience Access ไม่ update / Install ไม่ได้

**สาเหตุ:** Audience settings ไม่ save / เกิน 10 audiences / workspace role ไม่ถูก

**วิธีแก้:**
1. ตรวจ audience settings → save + **republish** app
2. ⚠️ **Limit: 10 audiences** per app → ต้องการมากกว่า? ใช้ secondary workspace
3. Publish/Update app → ต้องเป็น **Admin หรือ Member** role
4. Auto-install → Tenant admin เปิด setting ได้

---

## 179. Dataverse / TDS Endpoint Errors

### ERR-DATAVERSE-001: "Unable to connect" / Table not found

**สาเหตุ:** TDS endpoint ไม่ enabled / port 1433/5558 ถูก block / privilege ไม่พอ

**วิธีแก้:**
1. Power Platform Admin Center → Settings > Product > Features → **Enable TDS endpoint**
2. ตรวจ security role → "Allow user to access TDS endpoint" = **Organization**
3. ⚠️ Port 1433 + 5558 ต้องเปิด → VPN อาจ block
4. ลอง toggle TDS endpoint off → on (หลัง system update)
5. Large datasets → ใช้ **Azure Synapse Link** แทน TDS (ดีกว่าสำหรับ > 80 columns)

---

## 180. Azure Synapse Serverless SQL Pool Errors

### ERR-SYNAPSE-001: "Could not open connection" / "Cannot find CREDENTIAL" / Capacity Error

**สาเหตุ:** Port blocked / ADLS permissions ไม่พอ / replicated DB issues

**วิธีแก้:**
1. ตรวจ ports 1433 + 443 + 80 → ไม่ถูก block
2. ⚠️ "Cannot find CREDENTIAL" → ใช้ **Azure AD login** แทน username/password
3. ต้องมี **Storage Blob Data Contributor** role บน ADLS Gen2
4. ❌ อย่าใช้ replicated databases กับ PBI → สร้าง custom DB ใน serverless pool แทน
5. "Not enough capacity" → intermittent Synapse issue → retry

---

## 🔍 Quick Lookup Table (Full — 180 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| capacity throttling | ERR-THROTTLE-001 |
| Git "unsupported item" | ERR-GIT-001 |
| MFA AADSTS700056 | ERR-CA-001 |
| Copilot DAX ไม่ถูกต้อง | ERR-COPILOT-001 |
| composite model chain | ERR-COMPOSITE-CHAIN-001 |
| hybrid table | ERR-HYBRID-001 |
| sensitivity label | ERR-LABEL-001 |
| Tabular Editor greyed out | ERR-TABED-001 |
| TMDL parsing | ERR-TMDL-ADV-001 |
| embed effective identity | ERR-EMBEDTOKEN-001 |
| SAP HANA SSO | ERR-SAPHANA-001 |
| PDF truncated | ERR-PDF-001 |
| REST API 403 | ERR-API-ADV-001 |
| PowerShell Connect-PBI | ERR-PSCMD-001 |
| broken image URL | ERR-IMGURL-001 |
| field parameter blank | ERR-FIELDPARAM-001 |
| smart narrative | ERR-NARRATIVE-001 |
| anomaly detection | ERR-ANOMALY-001 |
| key influencer | ERR-KEYINF-001 |
| CALENDARAUTO / auto date | ERR-DATETABLE-001 |
| BigQuery auth | ERR-BIGQUERY-001 |
| Oracle ORA-12154 | ERR-ORACLE-001 |
| Databricks PAT | ERR-DATABRICKS-001 |
| MySQL SSL | ERR-MYSQL-001 |
| PostgreSQL Npgsql | ERR-PGSQL-001 |
| web connector 403 | ERR-WEBCONN-001 |
| decomposition tree | ERR-DECOMP-001 |
| performance analyzer | ERR-PERFANALYZE-001 |
| query diagnostics | ERR-QUERYDIAG-001 |
| report theme JSON | ERR-THEME-001 |
| data profiling | ERR-PROFILE-001 |
| drill-through no data | ERR-DRILLTHRU-001 |
| tooltip not showing | ERR-TOOLTIP-001 |
| bookmark navigator reset | ERR-BOOKMARK-001 |
| sync slicers not syncing | ERR-SYNCSLICER-001 |
| Q&A visual not understanding | ERR-QA-001 |
| paginated subreport error | ERR-PAGINATED-001 |
| subscription email failed | ERR-SUBSCRIPTION-001 |
| app audience install | ERR-APP-001 |
| Dataverse TDS endpoint | ERR-DATAVERSE-001 |
| Synapse serverless credential | ERR-SYNAPSE-001 |

---

## 181. RLS "Test as Role" Errors

### ERR-RLS-TEST-001: "Test as role" ไม่ทำงาน / Permission required

**สาเหตุ:** SSO active / user เป็น Admin/Member (RLS ไม่ apply) / Service bug

**วิธีแก้:**
1. ⚠️ SSO (DirectQuery/Live Connection) → "Test as role" ไม่รองรับ → ทดสอบใน **Desktop** แทน
2. RLS apply เฉพาะ **Viewer** role เท่านั้น → Admin/Member/Contributor ไม่โดน RLS
3. "Permission required" → ลอง republish report
4. ✅ Best practice: ทดสอบ RLS ใน Desktop ก่อน → แล้ว assign real users ใน Service

---

## 182. Incremental Refresh Partition Errors

### ERR-INCREFRESH-001: Overlapping Data / Partition Conflict / Query Folding Fail

**สาเหตุ:** RangeEnd ใช้ <= แทน < / data type mismatch / source date column ถูก update

**วิธีแก้:**
1. ⚠️ Power Query filter → ใช้ `< RangeEnd` (น้อยกว่า) **ไม่ใช่** `<= RangeEnd`
2. Native SQL → `WHERE DateColumn >= @RangeStart AND DateColumn < @RangeEnd`
3. **Data type** ของ RangeStart/RangeEnd ต้องเป็น `Date/Time` ตรงกับ column
4. ❌ Source date column ถูก update → Incremental Refresh ไม่รองรับ (partition-key conflict)
5. Query folding fail → ตรวจ warning ใน policy dialog

---

## 183. External Tools Registration Errors

### ERR-EXTTOOLS-001: DAX Studio / Tabular Editor ไม่แสดงใน Tab

**สาเหตุ:** .pbitool.json ไม่ถูกสร้าง / ไม่ได้ restart PBI / ไม่ได้เปิด .pbix

**วิธีแก้:**
1. ตรวจ `.pbitool.json` อยู่ใน `C:\Program Files (x86)\Common Files\Microsoft Shared\Power BI Desktop\External Tools`
2. **Restart Power BI Desktop** หลัง install tool
3. ⚠️ External Tools tab แสดงเฉพาะเมื่อ **เปิด .pbix file** ที่มี data model
4. ลอง **Run as Administrator**
5. "Executable not found" → ตรวจ installation path ของ tool

---

## 184. Workspace Migration Errors (Classic → New)

### ERR-WSMIGRATE-001: Permission ผิดหลัง migrate / Orphaned Workspace

**สาเหตุ:** Role mapping เปลี่ยน / admin ถูกลบใน AAD / licensing

**วิธีแก้:**
1. ⚠️ Classic → New: Contributor แทน "Members can reshare", Viewer แทน read-only
2. "Only users with Pro licenses..." → New workspace บังคับ Pro/PPU license
3. **Orphaned workspace** → admin ถูกเปลี่ยนใน AAD → ติดต่อ Fabric admin เพื่อ assign admin ใหม่
4. M365 Group owners → ถูกเพิ่มเป็น Admin role โดยอัตโนมัติ

---

## 185. Endorsement / Certification Errors

### ERR-ENDORSE-001: Certification greyed out / ไม่มีตัวเลือก

**สาเหตุ:** Tenant admin ยังไม่ enable / user ไม่อยู่ใน authorized security group

**วิธีแก้:**
1. **Promotion** → ทุกคนที่มี write permission ทำได้
2. **Certification** → ต้องให้ Tenant Admin เปิด + กำหนด security group ที่ authorized
3. ⚠️ Greyed out → Admin ยังไม่ enable certification feature
4. ✅ กำหนด organizational standards ว่า "certified" หมายถึงอะไร

---

## 186. Lineage View / Impact Analysis Errors

### ERR-LINEAGE-001: "Limited access" / ไม่เห็น dependencies ทั้งหมด

**สาเหตุ:** ไม่มี access ทุก workspace / privacy restrictions / external semantic models

**วิธีแก้:**
1. ต้องมี **Contributor role** + Pro license เพื่อดู lineage
2. ⚠️ **Tenant-wide lineage ไม่มี** → แม้ admin ก็เห็นเฉพาะ workspace ที่มี access
3. "Limited access" → items ที่ไม่มี permission จะแสดงแบบนี้
4. External semantic models → ต้องไปที่ source workspace เพื่อทำ impact analysis

---

## 187. Usage Metrics Errors

### ERR-USAGE-001: Zero values / "Semantic model not found" / ข้อมูลไม่ update

**สาเหตุ:** Dataset refresh issue / Private Link + Block Public Access / browser tracking

**วิธีแก้:**
1. ⚠️ "Semantic model not found" → ลอง delete + recreate Usage Metrics dataset
2. Private Link + Block Public Internet Access → อาจทำให้ usage metrics ไม่แสดง
3. Edge ไม่ track แต่ Chrome ได้ → ตรวจ Edge privacy settings
4. Date filter ถูกจำกัด → known issue (late 2024)

---

## 188. SharePoint Embed / CSP Errors

### ERR-SPEMBED-001: "Refused to frame" / CSP Violation / License Required

**สาเหตุ:** Content Security Policy block / custom domain ไม่อยู่ใน whitelist / Chromium update

**วิธีแก้:**
1. ⚠️ CSP "Refused to frame" → ใช้ **"Embed in SharePoint Online"** แทน generic iframe
2. Chromium security update → อาจ prompt auth หลายครั้ง → ใช้ user-owns-data method
3. License suddenly required (2025+) → ตรวจ licensing enforcement changes
4. ❌ Private links → ไม่รองรับ "Publish to web (Public)"
5. Number separator ผิด → ตรวจ browser language settings

---

## 189. Teams Integration Errors

### ERR-TEAMS-001: "Tab couldn't load" / Permission Error / AADSTS90094

**สาเหตุ:** User ไม่มี access / admin consent ไม่ได้ grant / Teams analytics deprecated

**วิธีแก้:**
1. "AADSTS90094" → admin ต้อง **grant consent** ใน Microsoft Entra ID
2. ⚠️ **Teams Activity Analytics** → deprecated Jan 31, 2025 → ใช้ native Teams Analytics แทน
3. "Tab couldn't load" → เพิ่ม user ใน dataset security settings / grant guest role ใน AAD
4. "Couldn't load model schema" → ตรวจ capacity ไม่ paused/deleted

---

## 190. Composite Model + Live Connection Errors (Advanced)

### ERR-COMPOSITE-LC-001: "Cannot add local model" / Refresh Error / Query Limit

**สาเหตุ:** Tenant settings ไม่ enable / calculated tables depend on SSAS / gateway SSO missing

**วิธีแก้:**
1. Enable: Desktop > Options > Preview features > "DirectQuery for PBI datasets and AAS"
2. ⚠️ Calculated tables/columns ที่ depend on SSAS DirectQuery → **refresh ไม่ได้**
3. "Resultset exceeded maximum allowed size" → query limit ของ DirectQuery
4. Gateway + on-premises → ตรวจ SSO credentials ใน gateway config
5. ❌ บาง SSAS cube versions → ไม่รองรับ composite models

---

## 🔍 Quick Lookup Table (Full — 190 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| capacity throttling | ERR-THROTTLE-001 |
| Git "unsupported item" | ERR-GIT-001 |
| MFA AADSTS700056 | ERR-CA-001 |
| Copilot DAX | ERR-COPILOT-001 |
| composite model chain | ERR-COMPOSITE-CHAIN-001 |
| hybrid table | ERR-HYBRID-001 |
| sensitivity label | ERR-LABEL-001 |
| Tabular Editor | ERR-TABED-001 |
| TMDL parsing | ERR-TMDL-ADV-001 |
| embed effective identity | ERR-EMBEDTOKEN-001 |
| SAP HANA SSO | ERR-SAPHANA-001 |
| PDF truncated | ERR-PDF-001 |
| REST API 403 | ERR-API-ADV-001 |
| PowerShell Connect-PBI | ERR-PSCMD-001 |
| image URL | ERR-IMGURL-001 |
| field parameter | ERR-FIELDPARAM-001 |
| smart narrative | ERR-NARRATIVE-001 |
| anomaly detection | ERR-ANOMALY-001 |
| key influencer | ERR-KEYINF-001 |
| CALENDARAUTO | ERR-DATETABLE-001 |
| BigQuery | ERR-BIGQUERY-001 |
| Oracle ORA | ERR-ORACLE-001 |
| Databricks | ERR-DATABRICKS-001 |
| MySQL SSL | ERR-MYSQL-001 |
| PostgreSQL Npgsql | ERR-PGSQL-001 |
| web connector 403 | ERR-WEBCONN-001 |
| decomposition tree | ERR-DECOMP-001 |
| performance analyzer | ERR-PERFANALYZE-001 |
| report theme JSON | ERR-THEME-001 |
| data profiling | ERR-PROFILE-001 |
| drill-through no data | ERR-DRILLTHRU-001 |
| tooltip not showing | ERR-TOOLTIP-001 |
| bookmark navigator | ERR-BOOKMARK-001 |
| sync slicers | ERR-SYNCSLICER-001 |
| Q&A visual | ERR-QA-001 |
| paginated subreport | ERR-PAGINATED-001 |
| subscription email | ERR-SUBSCRIPTION-001 |
| app audience | ERR-APP-001 |
| Dataverse TDS | ERR-DATAVERSE-001 |
| Synapse serverless | ERR-SYNAPSE-001 |
| RLS test as role | ERR-RLS-TEST-001 |
| incremental refresh partition | ERR-INCREFRESH-001 |
| external tools DAX Studio | ERR-EXTTOOLS-001 |
| workspace migration classic | ERR-WSMIGRATE-001 |
| endorsement certified | ERR-ENDORSE-001 |
| lineage view impact | ERR-LINEAGE-001 |
| usage metrics zero | ERR-USAGE-001 |
| SharePoint embed CSP | ERR-SPEMBED-001 |
| Teams tab couldn't load | ERR-TEAMS-001 |
| composite live connection | ERR-COMPOSITE-LC-001 |

---

## 191. R / Python Visual Errors

### ERR-RPYTHON-001: "Script Runtime Error" / Visual Blocked / Disabled

**สาเหตุ:** Tenant admin disable / PBI update ทำให้ script visual พัง / Embedded ไม่รองรับ

**วิธีแก้:**
1. Admin Portal → Tenant Settings > Developer Settings → **Enable Python/R visuals**
2. ⚠️ Sep 2024 update → Script Runtime Error → Microsoft reverted update, ตรวจ PBI version
3. Embedded environment → Python visuals อาจไม่ทำงาน (known limitation)
4. "Error Fetching Data" → ตรวจ Python path + packages installed

---

## 192. ArcGIS Maps Errors

### ERR-ARCGIS-001: "License not available" / Sign-in Error / Layer ไม่โหลด

**สาเหตุ:** Subscription expired / public account ไม่รองรับ / URL blocked / credits หมด

**วิธีแก้:**
1. Standard account → ใช้ได้เลยไม่ต้อง sign in
2. ⚠️ Sign-in ต้องใช้ **ArcGIS Online organizational account** เท่านั้น (❌ public account)
3. "License not available" → ตรวจ subscription + credits กับ admin
4. URL blocked → เพิ่ม `pbivisuals.powerbi.com` ใน allowlist
5. Desktop sign-in fail → ลบ CEF + Cache folders ใน PBI installation dir

---

## 193. Power Automate Visual Errors

### ERR-PAVISUAL-001: "Problem that needs to be fixed to trigger this flow"

**สาเหตุ:** Column name ผิดใน filter rows / new designer vs old designer bug / DLP block

**วิธีแก้:**
1. ตรวจ **column names ตรงกันเป๊ะ** → typo = trigger fail
2. ⚠️ Data ไม่ flow → bug ระหว่าง new/old designer → re-add "On Power BI button" trigger
3. DLP policy block → ตรวจ connector ที่ใช้ไม่ violate DLP rules
4. ✅ ใช้ **Flow checker** เพื่อ diagnose issues

---

## 194. Small Multiples Errors

### ERR-SMALLMULT-001: Max 6 Columns / Data Labels ผิด / Chart Type ไม่รองรับ

**สาเหตุ:** Column limit 6 / stacked column label bug / chart type ไม่ support

**วิธีแก้:**
1. ⚠️ **Max 6 columns** per visual → เกินนั้นจะขึ้นแถวใหม่
2. Stacked column chart → data labels bug (market share) → ใช้ custom tooltips แทน
3. ✅ May 2025+ → รองรับ all chart types ใน small multiples
4. ต้องการมากกว่า 6 → สร้าง separate charts + visual-level filters

---

## 195. Conditional Formatting Errors

### ERR-CONDFMT-001: Rules ไม่ทำงาน / Measures Greyed Out / Color Scale ผิด

**สาเหตุ:** New card visual bug / percentage format issue / measure unavailable

**วิธีแก้:**
1. ⚠️ **New Card Visual (Apr 2025+)** → conditional formatting settings ไม่แสดงใน UI → ใช้ traditional card แทน
2. Percentage → ใช้ decimal numbers แทนในกฎ conditional formatting
3. Measures greyed out → ตรวจ data type + context
4. Color scale ไม่ update → ลอง clear visual cache / refresh

---

## 196. Mobile Layout Errors

### ERR-MOBILE-001: Layout เพี้ยน / ไม่แสดงบนมือถือ / Interaction ไม่ทำงาน

**สาเหตุ:** Browser ≠ App / fixed-width visuals / ไม่ได้ใช้ mobile layout view

**วิธีแก้:**
1. ⚠️ Mobile layout ทำงาน **เฉพาะ PBI Mobile App** → browser จะแสดง desktop layout ย่อ
2. ใช้ **Mobile Layout View** ใน Desktop เพื่อ design สำหรับมือถือ
3. ❌ fixed-width visuals, complex labels → render ไม่ดีบนมือถือ
4. ✅ ทดสอบบน actual devices (iOS + Android) ก่อน publish

---

## 197. XMLA Endpoint Errors

### ERR-XMLA-001: "Cannot connect" / Read-only / Processing Failed

**สาเหตุ:** Default = read-only / tenant setting ไม่ enable / capacity เล็กเกินไป

**วิธีแก้:**
1. Admin Portal → Capacity settings → XMLA Endpoint = **"Read Write"**
2. Tenant setting → Enable "Allow XMLA endpoints and Analyze in Excel"
3. ⚠️ **A1 capacity** → อาจ fail เพราะ memory ไม่พอ → disable unnecessary services
4. Processing failed (VS deploy) → set "Do not Process" → config credentials ใน UI แทน
5. ❌ Free/Pro license ไม่รองรับ XMLA → ต้อง Premium/PPU
6. ❌ "My Workspace" datasets → ไม่ accessible ผ่าน XMLA

---

## 198. Deployment Pipeline Errors

### ERR-DEPLOYPIPE-001: "Deploy failed" / Stuck Stage / Backward Deploy Corruption

**สาเหตุ:** Dependent items ไม่ครบ / browser issue / backward deploy = corrupt

**วิธีแก้:**
1. ⚠️ Deploy fail → ตรวจ dependent semantic models → ใช้ **"Select related"** button
2. Stage stuck → clear browser cache / ลอง Firefox หรือ Edge
3. ❌ **Backward deploy (Prod→Test) → อาจ corrupt models** → ใช้เฉพาะ forward CI/CD
4. Incremental refresh → ต้องใช้ enhanced semantic model metadata

---

## 199. Template App Errors

### ERR-TEMPLATE-001: "Unable to load report" / Parameter ผิด / Testing Limitations

**สาเหตุ:** Unsupported objects / DirectQuery / Azure Maps / RLS / parameter type "Any"

**ข้อจำกัด:**
| ❌ ไม่รองรับใน Template App | หมายเหตุ |
|---------------------------|---------|
| DirectQuery | ❌ |
| Personal gateway | ❌ |
| Azure Maps (non-certified) | ❌ |
| Parameter type "Any" / "Binary" | ❌ ใช้ "Text" แทน |

**วิธีแก้:**
1. ⚠️ "Unable to load" → ทดสอบด้วย minimal report แล้วเพิ่ม visuals ทีละตัว
2. Parameter dropdown ไม่แสดง → known limitation ใน install wizard
3. เปลี่ยน test environment → ต้อง re-publish for testing

---

## 🏆 200. Data Alert Errors

### ERR-ALERT-001: Alert ไม่ trigger / "Max Fabric trial" / ไม่ได้ Refresh

**สาเหตุ:** Static data / ❌ Fabric capacity required (2025+) / visual type ไม่รองรับ

**ข้อจำกัด Alerts:**
| ข้อจำกัด | รายละเอียด |
|----------|----------|
| Visual types | เฉพาะ gauge, KPI, card tiles บน dashboard |
| Data type | numeric เท่านั้น |
| Refresh | ต้อง refresh data → static ไม่ trigger |
| Personal | เฉพาะผู้สร้าง alert เท่านั้นที่ได้รับ |

**วิธีแก้:**
1. ⚠️ **2025+** → ต้องมี **Fabric capacity** เพื่อสร้าง alerts ใหม่
2. Alert ไม่ trigger → ตรวจว่า data refresh ทำงาน
3. Duplicate alerts ไม่ส่ง → ส่งเฉพาะเมื่อข้าม threshold + data เปลี่ยน
4. ✅ Multi-user alerts → ใช้ **Power Automate** หรือ **Data Activator**

---

## 🔍 Quick Lookup Table (Full — 🏆 200 Categories!)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| capacity throttling | ERR-THROTTLE-001 |
| Git "unsupported item" | ERR-GIT-001 |
| MFA AADSTS700056 | ERR-CA-001 |
| Copilot DAX | ERR-COPILOT-001 |
| composite model chain | ERR-COMPOSITE-CHAIN-001 |
| hybrid table | ERR-HYBRID-001 |
| sensitivity label | ERR-LABEL-001 |
| Tabular Editor | ERR-TABED-001 |
| TMDL parsing | ERR-TMDL-ADV-001 |
| SAP HANA SSO | ERR-SAPHANA-001 |
| PDF truncated | ERR-PDF-001 |
| REST API 403 | ERR-API-ADV-001 |
| PowerShell Connect-PBI | ERR-PSCMD-001 |
| field parameter | ERR-FIELDPARAM-001 |
| BigQuery | ERR-BIGQUERY-001 |
| Oracle ORA | ERR-ORACLE-001 |
| Databricks | ERR-DATABRICKS-001 |
| MySQL SSL | ERR-MYSQL-001 |
| PostgreSQL Npgsql | ERR-PGSQL-001 |
| web connector 403 | ERR-WEBCONN-001 |
| drill-through | ERR-DRILLTHRU-001 |
| tooltip | ERR-TOOLTIP-001 |
| bookmark navigator | ERR-BOOKMARK-001 |
| sync slicers | ERR-SYNCSLICER-001 |
| Q&A visual | ERR-QA-001 |
| paginated subreport | ERR-PAGINATED-001 |
| subscription email | ERR-SUBSCRIPTION-001 |
| app audience | ERR-APP-001 |
| Dataverse TDS | ERR-DATAVERSE-001 |
| Synapse serverless | ERR-SYNAPSE-001 |
| RLS test as role | ERR-RLS-TEST-001 |
| incremental refresh | ERR-INCREFRESH-001 |
| external tools | ERR-EXTTOOLS-001 |
| workspace migration | ERR-WSMIGRATE-001 |
| endorsement certified | ERR-ENDORSE-001 |
| lineage view | ERR-LINEAGE-001 |
| usage metrics | ERR-USAGE-001 |
| SharePoint embed CSP | ERR-SPEMBED-001 |
| Teams tab | ERR-TEAMS-001 |
| composite live connection | ERR-COMPOSITE-LC-001 |
| R Python visual blocked | ERR-RPYTHON-001 |
| ArcGIS maps license | ERR-ARCGIS-001 |
| Power Automate flow trigger | ERR-PAVISUAL-001 |
| small multiples 6 columns | ERR-SMALLMULT-001 |
| conditional formatting rules | ERR-CONDFMT-001 |
| mobile layout phone | ERR-MOBILE-001 |
| XMLA endpoint read-write | ERR-XMLA-001 |
| deployment pipeline failed | ERR-DEPLOYPIPE-001 |
| template app install | ERR-TEMPLATE-001 |
| data alert not triggering | ERR-ALERT-001 |

---

## 201. Publish to Web Errors

### ERR-PUBTOWEB-001: Option Disabled / Greyed Out / RLS Block

**สาเหตุ:** Tenant admin disable / Block Public Internet Access / RLS enabled

**วิธีแก้:**
1. Admin Portal → Tenant settings → Export and sharing → **Enable "Publish to Web"**
2. ⚠️ Greyed out → ตรวจ "Block Public Internet Access" → ต้อง disable ก่อน
3. ❌ RLS enabled → "Publish to Web" จะ **ไม่แสดง** (by design — security)
4. ⚠️ **PUBLIC = ไม่มี authentication** → ห้ามใช้กับข้อมูลลับ!
5. ใช้ได้เฉพาะ reports ที่ editable + Pro/PPU license

---

## 202. Export Data Limits

### ERR-EXPORT-001: Row Limit / Unicode ผิด / DirectQuery 16MB

**ข้อจำกัด:**
| Format | Max Rows | หมายเหตุ |
|--------|---------|---------|
| .csv | 30,000 | Unicode อาจเพี้ยน |
| .xlsx | 150,000 | ขึ้นกับ data types + columns |
| DirectQuery | 16 MB uncompressed | อาจได้น้อยกว่า 150K rows |

**วิธีแก้:**
1. ⚠️ ต้องมี **Build permission** บน dataset เพื่อ export
2. Dynamic format strings ไม่ retain ใน Excel export
3. ต้องการมากกว่า limit → ใช้ **Analyze in Excel** หรือ **REST API**

---

## 203. Analyze in Excel Errors

### ERR-ANALYZEXL-001: "Failed to connect" / ODC ไม่เปิด / Permission Error

**สาเหตุ:** Modern auth ไม่ enable / tenant setting ปิด / MSOLAP provider ไม่ installed

**วิธีแก้:**
1. Tenant setting → Enable "Allow XMLA endpoints and Analyze in Excel"
2. ⚠️ ต้อง **Modern authentication** → Legacy auth จะไม่ทำงาน
3. ติดตั้ง **MSOLAP provider** ล่าสุดใน Excel
4. ODC file ไม่เปิด → ตรวจ default program association

---

## 204. Calculation Group Errors

### ERR-CALCGROUP-001: Precedence ผิด / Format String ไม่ทำงาน / Composite Model Break

**สาเหตุ:** Precedence value ไม่ถูกต้อง / visual ไม่ support format string / composite model conflict

**วิธีแก้:**
1. ⚠️ **Precedence** → ค่าสูง = apply ก่อน → ตรวจลำดับ calculation groups
2. Format string expression → บาง visuals (combined chart) ไม่รองรับ
3. ❌ Composite models → format string จาก calc group อาจทำให้ remote measures break
4. Tabular Editor → ไม่มี Intellisense สำหรับ format string expression → ระวัง syntax
5. Live-connected reports → format string อาจไม่ apply → ใช้ DAX `FORMAT()` แทน (แต่แปลงเป็น text)

---

## 205. Dynamic Format String Errors

### ERR-DYNFORMAT-001: ค่าแสดง text แทน number / Live Connection ไม่ทำงาน

**สาเหตุ:** ใช้ FORMAT() DAX = text output / live-connected report measure / old PBI version

**วิธีแก้:**
1. ⚠️ `FORMAT()` DAX → แปลงเป็น **text** → chart visuals ใช้ไม่ได้!
2. ✅ ใช้ **Dynamic Format String** feature (Jan 2025+ GA) → preserve numeric data type
3. Live connection → measure ต้องอยู่ใน dataset ไม่ใช่ report-level
4. `SELECTEDMEASUREFORMATSTRING()` → ใช้ได้เฉพาะใน calculation items

---

## 206. Auto Date/Time Hierarchy Errors

### ERR-AUTODATE-001: Model Size โต / Performance ช้า / Date Range ผิด

**สาเหตุ:** Hidden date table สร้างทุก date column / DirectQuery ไม่รองรับ / auto summarize

**วิธีแก้:**
1. ⚠️ **Disable Auto Date/Time** → Options > Data Load > uncheck "Auto date/time"
2. สร้าง **custom Date dimension table** แทน → ดีกว่าเรื่อง performance + control
3. DirectQuery → auto date hierarchy อาจไม่สร้าง (known limitation)
4. Date fields auto summarize (SUM) → set "Don't Summarize" + ตรวจ data type

---

## 207. User-Defined Aggregation Errors

### ERR-USERAGG-001: Data Type Mismatch / Dual Storage ผิด / Data ไม่ตรง

**สาเหตุ:** Detail vs aggregate table data type ไม่ตรง / aggregation table ใช้ Dual ไม่ได้

**วิธีแก้:**
1. **Dimension tables** → set **Dual storage mode** (ทำงานทั้ง Import + DirectQuery)
2. ❌ **Aggregation table ใช้ Dual mode ไม่ได้** → ต้องเป็น Import หรือ DirectQuery เท่านั้น
3. Data ไม่ตรง → Import agg table ต้อง refresh sync กับ source
4. ตรวจ data types ระหว่าง detail + aggregate tables ต้องตรงกัน

---

## 208. Dynamic RLS / USERPRINCIPALNAME Errors

### ERR-DYNRLS-001: USERPRINCIPALNAME() Blank / ไม่ Filter / Case Mismatch

**สาเหตุ:** Desktop vs Service behavior ต่างกัน / case sensitivity / Report Server ไม่รองรับ

**วิธีแก้:**
1. ⚠️ `USERPRINCIPALNAME()` → Desktop = local login, Service = actual UPN → ทดสอบใน Service
2. **Case mismatch** → ใช้ `LOWER(USERPRINCIPALNAME())` เปรียบเทียบกับ `LOWER([Email])`
3. ❌ **Power BI Report Server** → ไม่รองรับ `USERPRINCIPALNAME()` → ใช้ `USERNAME()` แทน
4. Visual blank = RLS filter out ทุก rows → สร้าง security table + measure แสดง "no access"

---

## 209. Object-Level Security (OLS) Advanced Errors

### ERR-OLS-ADV-001: "Unrecognized fields" / Measure Hidden / Cannot Create in Desktop

**สาเหตุ:** OLS hide column → measures ที่ reference ก็ hidden / ❌ Desktop ไม่รองรับ OLS creation

**วิธีแก้:**
1. ❌ OLS **ต้องสร้างด้วย Tabular Editor** → Desktop ยังไม่รองรับ native
2. ⚠️ Measure reference OLS column → measure จะ **hidden อัตโนมัติ**
3. "Unrecognized fields" → user อยู่ใน role ที่ถูก restrict
4. ❌ Quick Insights, Smart Narrative → ไม่รองรับ datasets ที่มี OLS
5. **RLS + OLS ต้องอยู่ใน role เดียวกัน** → แยก role = "cannot load model schema" error

---

## 210. Personal Bookmark Errors

### ERR-BOOKMARK-PERS-001: Bookmark ไม่ Save / Default ไม่ Apply / Conflict กับ Shared

**สาเหตุ:** Browser cache / shared bookmark override / report republish reset

**วิธีแก้:**
1. ⚠️ Personal bookmarks save ใน **user's browser session** → clear cache = หาย
2. "Default personal bookmark" → ต้อง set เป็น default แยกต่างหากจาก report default
3. Report republish → personal bookmarks อาจ break ถ้า visuals เปลี่ยน
4. ✅ ใช้ **persistent bookmarks** (Tenant setting) เพื่อ save across sessions

---

## 🔍 Quick Lookup Table (Full — 210 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| capacity throttling | ERR-THROTTLE-001 |
| Git "unsupported item" | ERR-GIT-001 |
| MFA AADSTS700056 | ERR-CA-001 |
| Copilot DAX | ERR-COPILOT-001 |
| composite model chain | ERR-COMPOSITE-CHAIN-001 |
| hybrid table | ERR-HYBRID-001 |
| sensitivity label | ERR-LABEL-001 |
| Tabular Editor | ERR-TABED-001 |
| TMDL parsing | ERR-TMDL-ADV-001 |
| SAP HANA SSO | ERR-SAPHANA-001 |
| PDF truncated | ERR-PDF-001 |
| REST API 403 | ERR-API-ADV-001 |
| PowerShell Connect-PBI | ERR-PSCMD-001 |
| field parameter | ERR-FIELDPARAM-001 |
| BigQuery | ERR-BIGQUERY-001 |
| Oracle ORA | ERR-ORACLE-001 |
| Databricks | ERR-DATABRICKS-001 |
| MySQL SSL | ERR-MYSQL-001 |
| PostgreSQL Npgsql | ERR-PGSQL-001 |
| drill-through | ERR-DRILLTHRU-001 |
| tooltip | ERR-TOOLTIP-001 |
| sync slicers | ERR-SYNCSLICER-001 |
| Q&A visual | ERR-QA-001 |
| paginated subreport | ERR-PAGINATED-001 |
| subscription email | ERR-SUBSCRIPTION-001 |
| Dataverse TDS | ERR-DATAVERSE-001 |
| Synapse serverless | ERR-SYNAPSE-001 |
| RLS test as role | ERR-RLS-TEST-001 |
| incremental refresh | ERR-INCREFRESH-001 |
| external tools | ERR-EXTTOOLS-001 |
| workspace migration | ERR-WSMIGRATE-001 |
| lineage view | ERR-LINEAGE-001 |
| usage metrics | ERR-USAGE-001 |
| SharePoint embed CSP | ERR-SPEMBED-001 |
| Teams tab | ERR-TEAMS-001 |
| composite live connection | ERR-COMPOSITE-LC-001 |
| R Python visual | ERR-RPYTHON-001 |
| ArcGIS maps | ERR-ARCGIS-001 |
| Power Automate flow | ERR-PAVISUAL-001 |
| small multiples | ERR-SMALLMULT-001 |
| conditional formatting | ERR-CONDFMT-001 |
| mobile layout | ERR-MOBILE-001 |
| XMLA endpoint | ERR-XMLA-001 |
| deployment pipeline | ERR-DEPLOYPIPE-001 |
| template app | ERR-TEMPLATE-001 |
| data alert | ERR-ALERT-001 |
| publish to web disabled | ERR-PUBTOWEB-001 |
| export data row limit | ERR-EXPORT-001 |
| analyze in Excel ODC | ERR-ANALYZEXL-001 |
| calculation group precedence | ERR-CALCGROUP-001 |
| dynamic format string | ERR-DYNFORMAT-001 |
| auto date time hierarchy | ERR-AUTODATE-001 |
| user-defined aggregation | ERR-USERAGG-001 |
| USERPRINCIPALNAME blank | ERR-DYNRLS-001 |
| OLS unrecognized fields | ERR-OLS-ADV-001 |
| personal bookmark | ERR-BOOKMARK-PERS-001 |

---

## 211. Custom Visual / Sandbox Errors

### ERR-CUSTOMVIS-001: Visual ไม่โหลด / Dialog Fail / Sandbox Restriction

**สาเหตุ:** URL blocked / offline mode / sandbox iFrame isolation / Feb 2025 dialog bug

**วิธีแก้:**
1. ⚠️ URL blocked → allowlist `pbivisuals.powerbi.com`
2. Offline mode → set env var `PBI_userFavoriteResourcePackagesEnabled` (แต่จะช้าขึ้น)
3. **Sandbox** → custom visuals ทำงานใน iFrame → ❌ ไม่สามารถเข้าถึง PBI CSS/fonts/APIs
4. Feb 2025 dialog bug → อัพเดท PBI Desktop เป็น v2.140.1454.0+
5. ❌ Non-certified visuals → tenant admin อาจ block → ใช้ certified visuals จาก AppSource

---

## 212. Dataflow Mashup Timeout Errors

### ERR-DFMASHUP-001: MetadataEvaluationGatewayTimeout / Entity Refresh Failed

**สาเหตุ:** Query ช้าเกินไป / gateway overloaded / complex transformations / capacity maxed

**วิธีแก้:**
1. ⚠️ `MetadataEvaluationGatewayTimeout` → schema validation ช้า → optimize queries
2. Gateway → อัพเดท version + ตรวจ load → เพิ่ม `MashupDefaultTimeout` ใน GatewayConfig.json
3. **Query folding** → push transformations กลับไป source เพื่อลด compute
4. Split dataflows → แยก dataflow ใหญ่เป็นหลายตัว
5. Capacity maxed → ลอง switch workspace type (Premium→Pro→กลับ) เพื่อ reallocate node

---

## 213. Relationship Ambiguity Errors

### ERR-RELATIONSHIP-001: "Ambiguous relationship" / Many-to-Many ผิด / Cross-Filter ไม่ทำงาน

**สาเหตุ:** หลาย paths ระหว่าง tables / M:M ไม่มี bridge / cross-filter direction ผิด

**วิธีแก้:**
1. ⚠️ **Ambiguous relationship** → มี 2+ paths ระหว่าง tables → ใช้ `USERELATIONSHIP()` ใน measure
2. Many-to-Many → สร้าง **bridge table** หรือตรวจว่า cross-filter = Both
3. ❌ Inactive relationship → ถูก ignore โดย default → ต้อง activate ด้วย `USERELATIONSHIP()`
4. Cross-filter "Both" → ⚠️ อาจทำให้ performance ช้า → ใช้เท่าที่จำเป็น

---

## 214. Context Transition / CALCULATE Errors

### ERR-CALCCTX-001: Measure ให้ค่าผิด / Row Context vs Filter Context / CALCULATE Unexpected

**สาเหตุ:** ไม่เข้าใจ context transition / CALCULATE เปลี่ยน filter context / iterator ซ้อน

**วิธีแก้:**
1. ⚠️ **CALCULATE** → แปลง row context เป็น filter context (context transition)
2. Measure ให้ค่าเดียวกันทุกแถว → ลืมใส่ filter ใน CALCULATE
3. ❌ `CALCULATE(SUM(Table[Col]))` ใน calculated column → context transition ทำงานเสมอ
4. ✅ ใช้ variables (`VAR`) เพื่อ capture context ก่อน CALCULATE
5. Iterator (SUMX, AVERAGEX) + CALCULATE → ค่าอาจซ้อน → ตรวจด้วย DAX Studio

---

## 215. Date Slicer Errors

### ERR-DATESLICER-001: Relative Date ผิด / Between ไม่ Filter / Calendar ไม่แสดง

**สาเหตุ:** Data type ไม่ใช่ Date / auto date hierarchy conflict / timezone offset

**วิธีแก้:**
1. ⚠️ Column data type ต้องเป็น **Date** หรือ **Date/Time** → Text จะไม่ทำงาน
2. "Relative date" slicer → ใช้กับ date column ที่ mark as Date Table
3. Calendar ไม่แสดง → ตรวจว่า column มีค่า continuous (ไม่มี gaps ใหญ่เกิน)
4. Between filter ไม่ work → ตรวจ date format ตรงกับ regional settings

---

## 216. Matrix Visual Errors

### ERR-MATRIX-001: Stepped Layout เพี้ยน / Expand/Collapse ไม่ทำงาน / Subtotal ผิด

**สาเหตุ:** Too many levels / measure context ผิดกับ subtotal / mobile rendering

**วิธีแก้:**
1. **Stepped layout** → ใช้ได้สูงสุด ~10 levels → เกินนั้นจะ render ผิด
2. ⚠️ Subtotals → ใช้ `HASONEVALUE()` หรือ `ISINSCOPE()` ตรวจ level ก่อน calculate
3. Expand/Collapse ไม่ทำงาน → ต้อง enable ใน Format pane > Row headers
4. ❌ Mobile → matrix ซับซ้อนจะ render ไม่ดี → ลด columns/rows

---

## 217. Scatter Chart / Play Axis Errors

### ERR-SCATTER-001: Play Axis ไม่เคลื่อนไหว / Bubble Size ผิดสัดส่วน / Data Points หาย

**สาเหตุ:** Data points เกิน 10,000 / bubble size min/max / play axis data type

**วิธีแก้:**
1. ⚠️ **Max 10,000 data points** ต่อ scatter → เกินนั้นจะ sample หรือไม่แสดง
2. Play axis → data type ต้องเป็น **Date/Time** หรือ **Whole Number**
3. Bubble size ไม่ proportional → ตรวจ min/max size settings ใน format pane
4. "Too many values" → aggregate data ก่อน หรือใช้ Top N filter

---

## 218. DirectQuery SSO Advanced Errors

### ERR-DQSSO-001: SSO ไม่ Pass Credentials / Fallback to Service Account / Azure AD Token

**สาเหตุ:** Gateway ไม่ config SSO / Kerberos delegation ผิด / Azure AD token expired

**วิธีแก้:**
1. On-premises gateway → config **Kerberos Constrained Delegation (KCD)** อย่างถูกต้อง
2. ⚠️ SSO fallback → ถ้า Kerberos fail จะใช้ service account → data ไม่ filter ตาม user
3. Azure AD SSO → ตรวจ token lifetime + conditional access policies
4. ❌ "Test Connection" สำเร็จ แต่ SSO fail → เพราะ test ใช้ service account ไม่ใช่ user token
5. ✅ ตรวจ SPN (Service Principal Name) registration ถูกต้อง

---

## 219. Self-Signed Certificate / SSL Errors

### ERR-SSLCERT-001: "Certificate chain not trusted" / SSL Provider Error 0

**สาเหตุ:** SQL Server ใช้ self-signed cert / gateway ไม่ trust cert / Feb 2024+ enforcement

**วิธีแก้:**
1. Gateway → เพิ่ม `SqlTrustedServers` ใน gateway config file
2. Desktop → set env var `PBI_SQL_TRUSTED_SERVERS` = server name
3. ⚠️ **Feb 2024+** → Power BI enforce SSL certificate validation → ต้อง config trust
4. ✅ Best practice → ใช้ **CA-signed certificate** แทน self-signed
5. Multiple servers → คั่นด้วย comma ใน SqlTrustedServers

---

## 220. Semantic Model Refresh Orchestration Errors

### ERR-REFRESHORCH-001: Downstream Model ใช้ Stale Data / Chain Refresh Fail

**สาเหตุ:** Dataflow fail แต่ semantic model refresh ต่อ / ไม่มี dependency chain

**วิธีแก้:**
1. ⚠️ Default → semantic model refresh ไม่รอ dataflow → อาจได้ stale data
2. ✅ ใช้ **Fabric Data Pipeline** → orchestrate sequential refresh (Aug 2025+ preview)
3. Explicit connection credentials → ต้องกำหนดเอง (ห้ามใช้ default data connection)
4. Chain fail → ตรวจ upstream dataflow status ก่อน trigger downstream refresh

---

## 🔍 Quick Lookup Table (Full — 220 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| capacity throttling | ERR-THROTTLE-001 |
| Git "unsupported item" | ERR-GIT-001 |
| Copilot DAX | ERR-COPILOT-001 |
| composite model chain | ERR-COMPOSITE-CHAIN-001 |
| hybrid table | ERR-HYBRID-001 |
| sensitivity label | ERR-LABEL-001 |
| Tabular Editor | ERR-TABED-001 |
| TMDL parsing | ERR-TMDL-ADV-001 |
| SAP HANA SSO | ERR-SAPHANA-001 |
| PDF truncated | ERR-PDF-001 |
| REST API 403 | ERR-API-ADV-001 |
| PowerShell Connect-PBI | ERR-PSCMD-001 |
| field parameter | ERR-FIELDPARAM-001 |
| BigQuery | ERR-BIGQUERY-001 |
| Oracle ORA | ERR-ORACLE-001 |
| Databricks | ERR-DATABRICKS-001 |
| MySQL SSL | ERR-MYSQL-001 |
| PostgreSQL Npgsql | ERR-PGSQL-001 |
| drill-through | ERR-DRILLTHRU-001 |
| sync slicers | ERR-SYNCSLICER-001 |
| Q&A visual | ERR-QA-001 |
| paginated subreport | ERR-PAGINATED-001 |
| subscription email | ERR-SUBSCRIPTION-001 |
| Dataverse TDS | ERR-DATAVERSE-001 |
| Synapse serverless | ERR-SYNAPSE-001 |
| incremental refresh | ERR-INCREFRESH-001 |
| external tools | ERR-EXTTOOLS-001 |
| workspace migration | ERR-WSMIGRATE-001 |
| lineage view | ERR-LINEAGE-001 |
| SharePoint embed CSP | ERR-SPEMBED-001 |
| Teams tab | ERR-TEAMS-001 |
| composite live connection | ERR-COMPOSITE-LC-001 |
| R Python visual | ERR-RPYTHON-001 |
| ArcGIS maps | ERR-ARCGIS-001 |
| Power Automate flow | ERR-PAVISUAL-001 |
| small multiples | ERR-SMALLMULT-001 |
| conditional formatting | ERR-CONDFMT-001 |
| mobile layout | ERR-MOBILE-001 |
| XMLA endpoint | ERR-XMLA-001 |
| deployment pipeline | ERR-DEPLOYPIPE-001 |
| template app | ERR-TEMPLATE-001 |
| data alert | ERR-ALERT-001 |
| publish to web | ERR-PUBTOWEB-001 |
| export data row limit | ERR-EXPORT-001 |
| analyze in Excel | ERR-ANALYZEXL-001 |
| calculation group | ERR-CALCGROUP-001 |
| dynamic format string | ERR-DYNFORMAT-001 |
| auto date hierarchy | ERR-AUTODATE-001 |
| user-defined aggregation | ERR-USERAGG-001 |
| USERPRINCIPALNAME | ERR-DYNRLS-001 |
| OLS unrecognized fields | ERR-OLS-ADV-001 |
| personal bookmark | ERR-BOOKMARK-PERS-001 |
| custom visual sandbox | ERR-CUSTOMVIS-001 |
| dataflow mashup timeout | ERR-DFMASHUP-001 |
| ambiguous relationship | ERR-RELATIONSHIP-001 |
| context transition CALCULATE | ERR-CALCCTX-001 |
| date slicer relative | ERR-DATESLICER-001 |
| matrix stepped layout | ERR-MATRIX-001 |
| scatter play axis | ERR-SCATTER-001 |
| DirectQuery SSO Kerberos | ERR-DQSSO-001 |
| self-signed certificate SSL | ERR-SSLCERT-001 |
| refresh orchestration stale | ERR-REFRESHORCH-001 |

---

## 221. Privacy Levels / Data Source Combining Errors

### ERR-PRIVACY-001: "Privacy levels cannot be used together" / Formula.Firewall ขั้นสูง

**สาเหตุ:** Private + Public/Organizational combine / Desktop vs Service ต่างกัน / ไม่ได้ set privacy level

**วิธีแก้:**
1. ⚠️ Private + Public = ❌ ทำ combine ไม่ได้ (by design — data protection)
2. Desktop → "Ignore privacy levels" ได้ แต่ **Service ไม่ honor setting นี้!**
3. Service → ต้อง set privacy level **ทุก data source** ใน Data source credentials
4. ✅ เปลี่ยน Private → Organizational ถ้าข้อมูลอยู่ภายในองค์กร
5. "Cannot convert value 'Function' to type Function" → privacy firewall block → ตรวจ privacy levels

---

## 222. What-If Parameter Errors

### ERR-WHATIF-001: Slicer ไม่ทำงาน / Data Type ผิด / Too Many Values

**สาเหตุ:** Data type mismatch / slicer > 1,000 values / Report Server ไม่ support

**วิธีแก้:**
1. ⚠️ Data type → Whole Number vs Decimal Number → ต้องตรงกัน
2. Slicer > ~1,000 values → "Too many values" → ใช้ `UNION()` + `GENERATESERIES()` ลดช่วง
3. ❌ Power BI Report Server → What-If ทำงานไม่เต็ม → ใช้ measures แทน calculated columns
4. Bind parameter → slicer ต้องเป็น DirectQuery mode เพื่อ dynamic query

---

## 223. Dynamic Web Source / RelativePath Errors

### ERR-DYNWEB-001: "Dynamic data source cannot be refreshed" / RelativePath Auth Issue

**สาเหตุ:** Web.Contents + dynamic URL / Service static validation / SharePoint OAuth conflict

**วิธีแก้:**
1. ⚠️ PBI Service **ต้อง validate URL แบบ static** → dynamic URL = refresh fail
2. ✅ ใช้ **RelativePath** แยก base URL (static) + dynamic part
3. SharePoint + RelativePath + OAuth → ❌ auth อาจ fail → set base URL เป็น "Always allow"
4. ตั้ง `Query` + `Headers` keys explicitly ใน `Web.Contents()`
5. `Web.BrowserContents` + `WaitFor` → สำหรับ dynamic content ที่ load ช้า

---

## 224. Paginated Report Multi-Value Parameter Errors

### ERR-PAGMV-001: "Must declare scalar variable" / Cascading ไม่ Filter / Subreport Param Mismatch

**สาเหตุ:** Query ไม่ใช้ IN operator / cascading dependency order ผิด / parameter name mismatch

**วิธีแก้:**
1. Multi-value → query text ต้องใช้ `IN (@Parameter)` **พร้อมวงเล็บ**
2. "Non-boolean type" error → dataset query structure ไม่รองรับ multi-select
3. Cascading → ตรวจ **dependency order** + data types ต้องตรง + handle NULL
4. Subreport → parameter names + data types ต้อง **exact match** ระหว่าง main ↔ sub report

---

## 225. Copilot Narrative Availability Errors

### ERR-COPILOTAVAIL-001: "Copilot is not available" / Region ไม่ Support / Capacity ไม่พอ

**สาเหตุ:** Capacity < F2 / unsupported region / tenant setting ปิด / Trial SKU

**วิธีแก้:**
1. ⚠️ ต้อง **Fabric capacity F2+** หรือ **Premium P1+** (❌ Trial ไม่ supported)
2. Region → ไม่ใช่ทุก region support → enable "Allow data processing outside geo region"
3. Tenant admin → Fabric admin portal → **Enable Copilot** ที่ tenant + capacity level
4. ❌ Free license → ดู Copilot visuals ไม่ได้ แม้ workspace มี P1
5. หลัง scale up → **รอ 24 ชม.** ก่อน Copilot จะ available

---

## 226. Semantic Link / SemPy Errors

### ERR-SEMLINK-001: ModuleNotFoundError / Notebook Execution Failed / Persona ผิด

**สาเหตุ:** SemPy ไม่ installed / Fabric persona ไม่ถูก / %pip disabled

**วิธีแก้:**
1. `ModuleNotFoundError: notebookutils.credentials` → Fabric environment เปลี่ยน → reinstall
2. ❌ "%pip magic disabled" → Fabric persona ต้องเป็น **Data Engineering**
3. ✅ Add SemPy ใน Fabric environment → **publish** environment ก่อนใช้
4. Semantic model connection → ตรวจ permissions + refresh credentials + PBI Desktop version

---

## 227. Gauge Visual Errors

### ERR-GAUGE-001: Min/Max ไม่ถูกต้อง / Target ไม่แสดง / Callout Value ผิด

**สาเหตุ:** Min/Max auto-calculate ผิด / target measure return NULL / format ไม่ตรง

**วิธีแก้:**
1. Min/Max → ตั้งค่า **manual** ใน format pane แทน auto
2. Target ไม่แสดง → measure return NULL/BLANK → ใส่ `IF(ISBLANK(), 0, value)`
3. Callout value format → ตั้งใน measure format string ไม่ใช่ visual format
4. ⚠️ Native gauge = customization จำกัด → พิจารณา custom visual จาก AppSource

---

## 228. Ribbon Chart Errors

### ERR-RIBBON-001: Too Many Categories / Rank ผิด / Width Misinterpret

**สาเหตุ:** > 10 categories ทำ ribbon อ่านยาก / sort ผิด / width ≠ ค่า (width = rank)

**วิธีแก้:**
1. ⚠️ จำกัด categories ไม่เกิน **5-10** หรือใช้ Top N filter
2. Sort → ตรวจ time axis ถูกต้อง (ascending) → sort ผิด = rank เพี้ยน
3. ❌ **Width = Rank** ไม่ใช่ magnitude → ribbon กว้าง = rank สูง (1st)
4. Dynamic values (e.g., millions/thousands) + slicer → DAX measure อาจซับซ้อน

---

## 229. Funnel Chart Errors

### ERR-FUNNEL-001: Percentage ผิด / Labels ซ้อน / Category Order ไม่ถูก

**สาเหตุ:** Data ไม่เรียง sequential / labels text overlap / too many categories

**วิธีแก้:**
1. ⚠️ Funnel ต้องมี **sequential stages** → data ไม่เรียง = แสดงผลเพี้ยน
2. Labels overlap → ลดขนาด text + ตั้ง position ใน format pane
3. Category order → sort ด้วย column ที่กำหนด stage order
4. Too many categories → ใช้ filter หรือ group minor stages

---

## 230. Table Visual Conditional Image Errors

### ERR-TABLEIMG-001: Image URL ไม่แสดง / Conditional Icon ไม่ทำงาน / Web URL Category ผิด

**สาเหตุ:** URL ไม่ accessible / data category ไม่ใช่ "Web URL" / CORS block

**วิธีแก้:**
1. ⚠️ Column data category ต้องเป็น **"Image URL"** หรือ **"Web URL"**
2. URL ต้อง publicly accessible → internal/private URLs จะไม่แสดง
3. Conditional icons → ตรวจ rules + value ranges ใน conditional formatting dialog
4. ❌ CORS block → image server ต้อง allow cross-origin requests

---

## 🔍 Quick Lookup Table (Full — 230 Categories)

> ค้นหา error จาก keyword

| Keyword | ไปที่ Section |
|---------|-------------|
| "circular dependency" | ERR-DAX-001 |
| "credentials expired" | ERR-REFRESH-002 |
| "Expression.Error" | ERR-PQ-001 |
| "file corrupted" | ERR-FILE-001 |
| "RLS" / "row level" | ERR-RLS-001 |
| "TokenExpired" / embed | ERR-EMBED-001 |
| "query timeout" DirectQuery | ERR-DQ-001 |
| gateway offline | ERR-GW-001 |
| query ไม่ fold | ERR-FOLD-001 |
| "out of memory" | ERR-MEM-001 |
| Formula.Firewall | ERR-FIREWALL-001 |
| Kerberos SSO fail | ERR-SSO-001 |
| Direct Lake permission | ERR-DLAKE-001 |
| capacity throttling | ERR-THROTTLE-001 |
| Git "unsupported item" | ERR-GIT-001 |
| Copilot DAX | ERR-COPILOT-001 |
| composite model chain | ERR-COMPOSITE-CHAIN-001 |
| hybrid table | ERR-HYBRID-001 |
| sensitivity label | ERR-LABEL-001 |
| Tabular Editor | ERR-TABED-001 |
| TMDL parsing | ERR-TMDL-ADV-001 |
| SAP HANA SSO | ERR-SAPHANA-001 |
| PDF truncated | ERR-PDF-001 |
| REST API 403 | ERR-API-ADV-001 |
| PowerShell Connect-PBI | ERR-PSCMD-001 |
| field parameter | ERR-FIELDPARAM-001 |
| BigQuery | ERR-BIGQUERY-001 |
| Oracle ORA | ERR-ORACLE-001 |
| Databricks | ERR-DATABRICKS-001 |
| MySQL SSL | ERR-MYSQL-001 |
| PostgreSQL Npgsql | ERR-PGSQL-001 |
| drill-through | ERR-DRILLTHRU-001 |
| sync slicers | ERR-SYNCSLICER-001 |
| Q&A visual | ERR-QA-001 |
| paginated subreport | ERR-PAGINATED-001 |
| subscription email | ERR-SUBSCRIPTION-001 |
| Dataverse TDS | ERR-DATAVERSE-001 |
| Synapse serverless | ERR-SYNAPSE-001 |
| incremental refresh | ERR-INCREFRESH-001 |
| external tools | ERR-EXTTOOLS-001 |
| workspace migration | ERR-WSMIGRATE-001 |
| lineage view | ERR-LINEAGE-001 |
| SharePoint embed CSP | ERR-SPEMBED-001 |
| Teams tab | ERR-TEAMS-001 |
| composite live connection | ERR-COMPOSITE-LC-001 |
| R Python visual | ERR-RPYTHON-001 |
| ArcGIS maps | ERR-ARCGIS-001 |
| Power Automate flow | ERR-PAVISUAL-001 |
| small multiples | ERR-SMALLMULT-001 |
| conditional formatting | ERR-CONDFMT-001 |
| mobile layout | ERR-MOBILE-001 |
| XMLA endpoint | ERR-XMLA-001 |
| deployment pipeline | ERR-DEPLOYPIPE-001 |
| template app | ERR-TEMPLATE-001 |
| data alert | ERR-ALERT-001 |
| publish to web | ERR-PUBTOWEB-001 |
| export data row limit | ERR-EXPORT-001 |
| analyze in Excel | ERR-ANALYZEXL-001 |
| calculation group | ERR-CALCGROUP-001 |
| dynamic format string | ERR-DYNFORMAT-001 |
| auto date hierarchy | ERR-AUTODATE-001 |
| user-defined aggregation | ERR-USERAGG-001 |
| USERPRINCIPALNAME | ERR-DYNRLS-001 |
| OLS unrecognized fields | ERR-OLS-ADV-001 |
| personal bookmark | ERR-BOOKMARK-PERS-001 |
| custom visual sandbox | ERR-CUSTOMVIS-001 |
| dataflow mashup timeout | ERR-DFMASHUP-001 |
| ambiguous relationship | ERR-RELATIONSHIP-001 |
| context transition CALCULATE | ERR-CALCCTX-001 |
| date slicer relative | ERR-DATESLICER-001 |
| matrix stepped layout | ERR-MATRIX-001 |
| scatter play axis | ERR-SCATTER-001 |
| DirectQuery SSO Kerberos | ERR-DQSSO-001 |
| self-signed certificate SSL | ERR-SSLCERT-001 |
| refresh orchestration stale | ERR-REFRESHORCH-001 |
| privacy levels combine | ERR-PRIVACY-001 |
| what-if parameter slicer | ERR-WHATIF-001 |
| dynamic web source RelativePath | ERR-DYNWEB-001 |
| paginated multi-value param | ERR-PAGMV-001 |
| Copilot not available region | ERR-COPILOTAVAIL-001 |
| semantic link SemPy | ERR-SEMLINK-001 |
| gauge min max target | ERR-GAUGE-001 |
| ribbon chart rank width | ERR-RIBBON-001 |
| funnel chart percentage | ERR-FUNNEL-001 |
| table image URL conditional | ERR-TABLEIMG-001 |

---

---

## 231. PBIP Generator — Visual Query Format Errors (Production-Tested)

> 🔥 **พบจากการ debug จริง** — ปัญหาที่ทำให้ report ไม่โหลดหรือ visual ไม่แสดงข้อมูล

### ERR-GENQ-001: Double-Wrapped Column/Aggregation ทำให้ Report ไม่โหลด

**Error Message:**
```
"Failed to load the report"
// หรือ Power BI ค้างที่หน้า loading
```

**สาเหตุ:** prototypeQuery Select ใช้ double-wrap format ผิด

```json
// ❌ WRONG — Double-wrap (ทำให้ report ไม่โหลดเลย!)
{
  "Column": {
    "Column": {
      "Expression": {"SourceRef": {"Source": "d"}},
      "Property": "Date"
    }
  },
  "Name": "table.Date"
}

// ❌ WRONG — Double-wrap Aggregation
{
  "Aggregation": {
    "Aggregation": {
      "Expression": {"Column": {...}},
      "Function": 0
    }
  },
  "Name": "Sum(table.col)"
}
```

**วิธีแก้:** ใช้ **single-wrap** format เท่านั้น

```json
// ✅ CORRECT — Single-wrap Column
{
  "Column": {
    "Expression": {"SourceRef": {"Source": "d"}},
    "Property": "Date"
  },
  "Name": "table.Date",
  "NativeReferenceName": "Date"
}

// ✅ CORRECT — Single-wrap Aggregation
{
  "Aggregation": {
    "Expression": {
      "Column": {
        "Expression": {"SourceRef": {"Source": "d"}},
        "Property": "col"
      }
    },
    "Function": 0
  },
  "Name": "Sum(table.col)",
  "NativeReferenceName": "Sum of col"
}
```

**ข้อสังเกต:**
- `Name` และ `NativeReferenceName` ต้องเป็น **siblings** ของ `Column`/`Aggregation` (อยู่ระดับเดียวกัน)
- Textbox ไม่ได้ใช้ prototypeQuery → จึงไม่ได้รับผลกระทบ
- ถ้า report โหลดไม่ได้เลย → ตรวจ format ของ Select items เป็นอย่างแรก

---

### ERR-GENQ-002: M Expression ไม่มี Table.TransformColumnTypes → "Something's wrong with fields"

**Error Message:**
```
"Something's wrong with one or more fields. See details"
// พร้อมปุ่ม "Fix this" บน visual
```

**สาเหตุ:** CSV import ด้วย `Table.PromoteHeaders` อย่างเดียวจะทำให้ **ทุกคอลัมน์เป็น type text** → Power BI ไม่สามารถ SUM/COUNT/AVG บน text ได้

```m
// ❌ WRONG — ไม่ระบุ data types (ทุกอย่างเป็น text)
let
  Source = Csv.Document(File.Contents("data.csv"), [Delimiter=",", Encoding=65001]),
  PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
  PromotedHeaders
```

**วิธีแก้:** เพิ่ม `Table.TransformColumnTypes` เสมอ

```m
// ✅ CORRECT — ระบุ data types ชัดเจน
let
  Source = Csv.Document(File.Contents("data.csv"), [Delimiter=",", Encoding=65001]),
  PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
  ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
    {"Date", type date},
    {"Amount", Int64.Type},
    {"Price", type number},
    {"Name", type text}
  })
in
  ChangedTypes
```

**Type Mapping สำหรับ model.bim:**

| model.bim dataType | M Query Type | ใช้กับ |
|---------------------|-------------|--------|
| `string` | `type text` | ชื่อ, หมวดหมู่ |
| `int64` | `Int64.Type` | จำนวนนับ (Count, Qty) |
| `double` | `type number` | ทศนิยม (Price, Rate) |
| `dateTime` | `type date` | วันที่ |
| `boolean` | `type logical` | True/False |

**Checklist:**
- [ ] ทุก CSV import ต้องมี `Table.TransformColumnTypes`
- [ ] Types ใน M expression ต้องตรงกับ `dataType` ใน model.bim columns
- [ ] ถ้า visual ขึ้น "Fix this" → ตรวจ M expression ก่อน

---

> 📅 สร้างเมื่อ: 2026-03-01 | อัพเดท: 2026-03-01 (Round 23 + GENQ fix)
> 📊 Total: **1,622+ error patterns**, **231 categories**, **370+ keywords** ใน Quick Lookup
> 🔗 ใช้คู่กับ: [SKILL.md](SKILL.md) | [USE_CASES.md](USE_CASES.md) | [DATA_CLEANING.md](DATA_CLEANING.md)
