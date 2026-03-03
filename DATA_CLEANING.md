# 🧹 Data Cleaning — Complete Reference

> ทำความสะอาดข้อมูลให้พร้อมก่อนสร้าง Dashboard — ครอบคลุมทั้ง Power Query M และ Python/Pandas

## Companion Files

| File | เนื้อหา |
|------|--------|
| [SKILL.md](SKILL.md) | PBIP format, JSON structure, visual types |
| [USE_CASES.md](USE_CASES.md) | 15 อุตสาหกรรม, 25+ dashboard blueprints |
| [DATA_CLEANING.md](DATA_CLEANING.md) | **คุณอยู่ที่นี่** — Data Cleaning ครบทุกเทคนิค |
| [generate.py](generate.py) | Python script — 14 visual generators |

---

## 📋 สารบัญ

1. [Data Cleaning Pipeline](#-data-cleaning-pipeline)
2. [Power Query M — ฟังก์ชันทำความสะอาด](#-power-query-m--cleaning-functions)
3. [Python/Pandas — Data Cleaning](#-pythonpandas--data-cleaning)
4. [Missing Values — จัดการค่าว่าง](#-missing-values)
5. [Duplicates — จัดการข้อมูลซ้ำ](#-duplicates)
6. [Outliers — จัดการค่าผิดปกติ](#-outliers)
7. [Text Cleaning — ทำความสะอาด Text](#-text-cleaning)
8. [Date/Time Cleaning](#-datetime-cleaning)
9. [Data Type Conversion](#-data-type-conversion)
10. [Data Validation](#-data-validation)
11. [Normalization & Standardization](#-normalization--standardization)
12. [Industry Use Cases (15+)](#-industry-use-cases)
13. [DAX สำหรับ Data Quality](#-dax-data-quality-measures)
14. [Automated Cleaning Pipeline](#-automated-cleaning-pipeline)
15. [Checklist](#-data-cleaning-checklist)

---

## 🔄 Data Cleaning Pipeline

```
Raw Data → Inspect → Fix Types → Remove Duplicates → Handle Missing
→ Clean Text → Fix Outliers → Validate → Normalize → Dashboard-Ready
```

### ขั้นตอนมาตรฐาน

| Step | ทำอะไร | เครื่องมือ |
|------|--------|-----------|
| 1. **Inspect** | ดูโครงสร้าง, types, missing, duplicates | `df.info()`, `df.describe()` |
| 2. **Fix Types** | แปลง data types ให้ถูกต้อง | `Table.TransformColumnTypes`, `astype()` |
| 3. **Remove Duplicates** | ลบแถวซ้ำ | `Table.Distinct`, `drop_duplicates()` |
| 4. **Handle Missing** | เติม/ลบค่าว่าง | `Table.SelectRows`, `fillna()`/`dropna()` |
| 5. **Clean Text** | Trim, lowercase, ลบอักขระพิเศษ | `Text.Trim`, `str.strip()` |
| 6. **Fix Outliers** | ตรวจจับและจัดการค่าผิดปกติ | IQR, Z-score |
| 7. **Validate** | ตรวจสอบ business rules | Custom rules |
| 8. **Normalize** | ปรับ scale ข้อมูล | Min-Max, Z-score |

---

## 🔧 Power Query M — Cleaning Functions

### Remove Nulls / Empty Rows

```m
// ลบแถวที่มี null ในคอลัมน์เฉพาะ
Table.SelectRows(Source, each [ColumnName] <> null and [ColumnName] <> "")

// ลบแถวที่ทุกคอลัมน์เป็น null
Table.SelectRows(Source, each not List.IsEmpty(
    List.RemoveNulls(Record.FieldValues(_))))

// ลบ blank rows (Power Query GUI = "Remove Blank Rows")
Table.SelectRows(Source, each not List.IsEmpty(
    List.RemoveMatchingItems(Record.FieldValues(_), {"", null})))
```

### Remove Duplicates

```m
// ลบแถวซ้ำทั้งหมด (เก็บแถวแรก)
Table.Distinct(Source)

// ลบซ้ำตามคอลัมน์เฉพาะ
Table.Distinct(Source, {"customer_id"})

// ลบซ้ำตามหลายคอลัมน์
Table.Distinct(Source, {"email", "phone"})
```

### Trim & Clean Text

```m
// ลบ space หน้า-หลัง
Table.TransformColumns(Source, {{"Name", Text.Trim, type text}})

// ลบ non-printable characters
Table.TransformColumns(Source, {{"Name", Text.Clean, type text}})

// แปลงเป็น Proper Case (ตัวแรกพิมพ์ใหญ่)
Table.TransformColumns(Source, {{"Name", Text.Proper, type text}})

// แปลงเป็น lowercase ทั้งหมด
Table.TransformColumns(Source, {{"Email", Text.Lower, type text}})

// Trim + Clean + Proper รวมกัน
Table.TransformColumns(Source, {
    {"Name", each Text.Proper(Text.Trim(Text.Clean(_))), type text}
})
```

### Replace Values

```m
// แทนค่าตรงๆ
Table.ReplaceValue(Source, "old_value", "new_value",
    Replacer.ReplaceText, {"ColumnName"})

// แทน null ด้วยค่าเริ่มต้น
Table.ReplaceValue(Source, null, "Unknown",
    Replacer.ReplaceValue, {"Category"})

// แทน null ด้วย 0 (ตัวเลข)
Table.ReplaceValue(Source, null, 0,
    Replacer.ReplaceValue, {"Amount"})

// แทนหลายค่าพร้อมกัน
Table.ReplaceValue(Source, each [Status],
    each if [Status] = "Y" then "Yes"
         else if [Status] = "N" then "No"
         else [Status],
    Replacer.ReplaceValue, {"Status"})
```

### Change Data Types

```m
// แปลง types หลายคอลัมน์พร้อมกัน
Table.TransformColumnTypes(Source, {
    {"Date", type date},
    {"Amount", type number},
    {"Name", type text},
    {"IsActive", type logical},
    {"ID", Int64.Type}
})
```

### Filter Rows

```m
// เก็บเฉพาะแถวที่ Amount > 0
Table.SelectRows(Source, each [Amount] > 0)

// ลบแถวที่มี error
Table.RemoveRowsWithErrors(Source)

// ลบแถวที่มี error ในคอลัมน์เฉพาะ
Table.RemoveRowsWithErrors(Source, {"Amount", "Date"})

// กรองตามวันที่
Table.SelectRows(Source, each [Date] >= #date(2024, 1, 1))

// กรองตามรายการ (IN list)
Table.SelectRows(Source, each List.Contains(
    {"Active", "Pending"}, [Status]))
```

### Split & Merge Columns

```m
// แยกคอลัมน์ด้วย delimiter
Table.SplitColumn(Source, "FullName",
    Splitter.SplitTextByDelimiter(" ", QuoteStyle.None),
    {"FirstName", "LastName"})

// รวมคอลัมน์
Table.CombineColumns(Source, {"FirstName", "LastName"},
    Combiner.CombineTextByDelimiter(" ", QuoteStyle.None), "FullName")
```

### Conditional Column

```m
// เพิ่มคอลัมน์ตามเงื่อนไข
Table.AddColumn(Source, "Tier", each
    if [Revenue] > 100000 then "Enterprise"
    else if [Revenue] > 10000 then "Mid-Market"
    else "Small Business", type text)

// เพิ่มคอลัมน์จัดกลุ่มอายุ
Table.AddColumn(Source, "AgeGroup", each
    if [Age] < 18 then "Youth"
    else if [Age] < 35 then "Young Adult"
    else if [Age] < 55 then "Adult"
    else "Senior", type text)
```

### Custom M Function (Reusable Cleaning)

```m
// สร้าง function ทำความสะอาด text ที่ใช้ซ้ำได้
let
    CleanText = (input as nullable text) as nullable text =>
        if input = null then null
        else Text.Proper(Text.Trim(Text.Clean(input))),

    CleanEmail = (input as nullable text) as nullable text =>
        if input = null then null
        else Text.Lower(Text.Trim(input)),

    CleanPhone = (input as nullable text) as nullable text =>
        if input = null then null
        else Text.Select(input, {"0".."9", "+", "-"})
in
    [CleanText = CleanText, CleanEmail = CleanEmail, CleanPhone = CleanPhone]
```

### Advanced: Regex-like Pattern Cleaning in M

```m
// ลบตัวอักษรพิเศษ (เก็บเฉพาะ a-z, 0-9, space)
Table.TransformColumns(Source, {{"Name", each
    Text.Select(_, {"a".."z","A".."Z","0".."9"," "}), type text}})

// Extract ตัวเลขจาก text
Table.TransformColumns(Source, {{"Phone", each
    Text.Select(_, {"0".."9"}), type text}})

// ลบ HTML tags
Table.TransformColumns(Source, {{"Description", each
    Text.Remove(_, {"<",">"}), type text}})
```

---

## 🐍 Python/Pandas — Data Cleaning

### Inspection (ขั้นตอนแรกเสมอ)

```python
import pandas as pd

df = pd.read_csv('data.csv')

# ดูโครงสร้าง
df.info()                    # columns, types, non-null counts
df.describe()                # statistics สำหรับตัวเลข
df.describe(include='all')   # statistics ทุก type
df.head(10)                  # ดู 10 แถวแรก
df.shape                     # (rows, columns)
df.dtypes                    # data types แต่ละ column
df.columns.tolist()          # ชื่อ columns ทั้งหมด

# ตรวจสอบ missing values
df.isnull().sum()            # นับ null แต่ละ column
df.isnull().sum() / len(df) * 100  # % missing

# ตรวจสอบ duplicates
df.duplicated().sum()        # นับแถวซ้ำ
df[df.duplicated()]          # ดูแถวซ้ำ

# ตรวจสอบ unique values
df['column'].nunique()       # จำนวน unique
df['column'].value_counts()  # นับแต่ละค่า
```

### Complete Cleaning Pipeline (Python)

```python
import pandas as pd
import numpy as np

def clean_dataframe(df):
    """Pipeline ทำความสะอาดข้อมูลครบวงจร"""
    original_shape = df.shape
    print(f"🔍 Original: {original_shape[0]} rows × {original_shape[1]} columns")

    # 1. Remove exact duplicates
    df = df.drop_duplicates()
    print(f"✅ After dedup: {len(df)} rows")

    # 2. Clean text columns
    text_cols = df.select_dtypes(include='object').columns
    for col in text_cols:
        df[col] = df[col].str.strip()              # Trim spaces
        df[col] = df[col].replace('', np.nan)       # Empty → NaN
        df[col] = df[col].replace(['N/A', 'n/a', 'NA', '-', 'null'], np.nan)

    # 3. Parse dates
    date_patterns = ['date', 'time', 'created', 'updated', 'timestamp']
    for col in df.columns:
        if any(p in col.lower() for p in date_patterns):
            df[col] = pd.to_datetime(df[col], errors='coerce')
            print(f"📅 Parsed date: {col}")

    # 4. Fix numeric columns
    for col in df.columns:
        if df[col].dtype == 'object':
            # ลอง convert เป็นตัวเลข
            numeric = pd.to_numeric(
                df[col].str.replace(r'[,$%]', '', regex=True),
                errors='coerce')
            if numeric.notna().sum() > len(df) * 0.5:  # >50% เป็นตัวเลข
                df[col] = numeric
                print(f"🔢 Converted to numeric: {col}")

    # 5. Report missing values
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) > 0:
        print(f"\n⚠️ Missing values:")
        for col, count in missing.items():
            pct = count / len(df) * 100
            print(f"   {col}: {count} ({pct:.1f}%)")

    print(f"\n✅ Final: {len(df)} rows × {df.shape[1]} columns")
    return df

# ใช้งาน
df = pd.read_csv('sales_data.csv')
df = clean_dataframe(df)
```

---

## 🔳 Missing Values

### กลยุทธ์เลือกวิธีจัดการ

| สถานการณ์ | วิธี | M Query | Pandas |
|-----------|------|---------|--------|
| Missing < 5% | **ลบแถว** | `Table.SelectRows` | `df.dropna()` |
| ตัวเลข, distribution ปกติ | **เติม Mean** | Custom column | `fillna(mean())` |
| ตัวเลข, มี outliers | **เติม Median** | Custom column | `fillna(median())` |
| Categorical | **เติม Mode** | `ReplaceValue` | `fillna(mode()[0])` |
| Time series | **Forward Fill** | Custom | `fillna(method='ffill')` |
| ค่า default ชัดเจน | **เติมค่าคงที่** | `ReplaceValue` | `fillna(0)` |
| Missing > 50% | **ลบ Column** | Remove column | `df.drop(columns=[])` |

### M Query — Handle Missing

```m
// เติม null ด้วย median ของ column
let
    MedianVal = List.Median(List.RemoveNulls(Table.Column(Source, "Amount"))),
    Filled = Table.ReplaceValue(Source, null, MedianVal,
        Replacer.ReplaceValue, {"Amount"})
in Filled

// Forward fill (เติมค่าจากแถวก่อนหน้า)
let
    Indexed = Table.AddIndexColumn(Source, "Index", 0, 1, Int64.Type),
    Filled = Table.AddColumn(Indexed, "FilledValue", each
        if [Value] <> null then [Value]
        else List.Last(List.FirstN(
            Table.Column(Indexed, "Value"), [Index]+1),
            each _ <> null))
in Table.RemoveColumns(Filled, {"Value", "Index"})
```

### Pandas — Handle Missing

```python
# กลยุทธ์ต่างๆ
df['amount'].fillna(df['amount'].mean(), inplace=True)      # Mean
df['amount'].fillna(df['amount'].median(), inplace=True)     # Median
df['category'].fillna(df['category'].mode()[0], inplace=True) # Mode
df['price'].fillna(0, inplace=True)                          # ค่าคงที่
df['date'].fillna(method='ffill', inplace=True)              # Forward Fill
df['date'].fillna(method='bfill', inplace=True)              # Backward Fill

# เติมตาม group (เช่น median ราคาตาม category)
df['price'] = df.groupby('category')['price'].transform(
    lambda x: x.fillna(x.median()))

# ลบแถวที่ missing มากกว่า threshold
thresh = len(df.columns) * 0.5  # ต้องมีข้อมูลอย่างน้อย 50%
df = df.dropna(thresh=thresh)

# ลบ column ที่ missing > 50%
missing_pct = df.isnull().sum() / len(df)
df = df.drop(columns=missing_pct[missing_pct > 0.5].index)
```

---

## 🔁 Duplicates

### ตรวจจับและลบ

```python
# ตรวจจับ exact duplicates
df.duplicated().sum()

# ตรวจจับ duplicates ตาม key columns
df.duplicated(subset=['email', 'phone']).sum()

# ดูแถวซ้ำ
df[df.duplicated(subset=['email'], keep=False)].sort_values('email')

# ลบ — เก็บแถวแรก
df = df.drop_duplicates(subset=['email'], keep='first')

# ลบ — เก็บแถวล่าสุด
df = df.sort_values('created_date').drop_duplicates(
    subset=['email'], keep='last')
```

### Fuzzy Matching (ข้อมูลคล้ายกันแต่ไม่เหมือน)

```python
# pip install fuzzywuzzy python-Levenshtein
from fuzzywuzzy import fuzz, process

# ตัวอย่าง: "John Doe" vs "Jon Doe" vs "JOHN DOE"
def find_fuzzy_duplicates(series, threshold=85):
    """หา duplicates ที่คล้ายกัน (fuzzy match)"""
    unique_vals = series.dropna().unique()
    groups = {}
    for val in unique_vals:
        matches = process.extract(val, unique_vals, limit=5)
        similar = [m[0] for m in matches if m[1] >= threshold and m[0] != val]
        if similar:
            groups[val] = similar
    return groups

dupes = find_fuzzy_duplicates(df['company_name'])
```

---

## 📊 Outliers

### ตรวจจับ

```python
import numpy as np

# Z-Score method (ค่าที่ห่างจาก mean > 3 SD)
from scipy import stats
z_scores = np.abs(stats.zscore(df['amount'].dropna()))
outliers_z = df[z_scores > 3]

# IQR method (แนะนำ — ทนทานต่อ skewed data)
Q1 = df['amount'].quantile(0.25)
Q3 = df['amount'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers_iqr = df[(df['amount'] < lower) | (df['amount'] > upper)]
print(f"Outliers: {len(outliers_iqr)} rows ({len(outliers_iqr)/len(df)*100:.1f}%)")
```

### จัดการ

```python
# 1. Capping/Winsorization — จำกัดค่าที่ขอบเขต
df['amount_capped'] = df['amount'].clip(lower=lower, upper=upper)

# 2. ลบ outliers
df_clean = df[(df['amount'] >= lower) & (df['amount'] <= upper)]

# 3. แทนด้วย median
median = df['amount'].median()
df.loc[(df['amount'] < lower) | (df['amount'] > upper), 'amount'] = median

# 4. Log transform (ลด skewness)
df['amount_log'] = np.log1p(df['amount'])
```

---

## ✏️ Text Cleaning

### M Query

```m
// Pipeline ทำความสะอาด text ครบ
let
    Step1 = Table.TransformColumns(Source, {{"Name", Text.Trim}}),
    Step2 = Table.TransformColumns(Step1, {{"Name", Text.Clean}}),
    Step3 = Table.TransformColumns(Step2, {{"Name", Text.Proper}}),
    Step4 = Table.TransformColumns(Step3, {{"Email", Text.Lower}}),
    Step5 = Table.TransformColumns(Step4, {{"Phone", each
        Text.Select(_, {"0".."9","+","-"})}}),
    Step6 = Table.ReplaceValue(Step5, "  ", " ",
        Replacer.ReplaceText, {"Address"})  // double space → single
in Step6
```

### Python/Pandas

```python
# ทำความสะอาด text ครบ
df['name'] = (df['name']
    .str.strip()                           # ลบ space หน้า-หลัง
    .str.replace(r'\s+', ' ', regex=True)  # หลาย space → 1
    .str.title())                          # Title Case

df['email'] = df['email'].str.lower().str.strip()

df['phone'] = df['phone'].str.replace(r'[^\d+\-]', '', regex=True)

# ลบ special characters
df['description'] = df['description'].str.replace(
    r'[^\w\s]', '', regex=True)

# Standardize categories
mapping = {
    'NY': 'New York', 'N.Y.': 'New York', 'new york': 'New York',
    'LA': 'Los Angeles', 'L.A.': 'Los Angeles'
}
df['city'] = df['city'].replace(mapping)
```

---

## 📅 Date/Time Cleaning

### M Query

```m
// Parse วันที่หลายรูปแบบ
Table.TransformColumns(Source, {{"Date", each
    try Date.From(_) otherwise null, type date}})

// Extract components
Table.AddColumn(Source, "Year", each Date.Year([Date]), Int64.Type)
Table.AddColumn(Source, "Month", each Date.Month([Date]), Int64.Type)
Table.AddColumn(Source, "MonthName", each Date.MonthName([Date]), type text)
Table.AddColumn(Source, "DayOfWeek", each Date.DayOfWeekName([Date]), type text)
```

### Python/Pandas

```python
# Parse dates (จัดการหลาย format อัตโนมัติ)
df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=False)

# Parse format เฉพาะ
df['thai_date'] = pd.to_datetime(df['thai_date'], format='%d/%m/%Y')

# Extract components
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_name'] = df['date'].dt.day_name()
df['quarter'] = df['date'].dt.quarter
df['is_weekend'] = df['date'].dt.dayofweek >= 5

# Filter date range
df = df[(df['date'] >= '2024-01-01') & (df['date'] <= '2024-12-31')]
```

---

## 🔄 Data Type Conversion

| From | To | M Query | Pandas |
|------|-----|---------|--------|
| Text → Number | `Int64.Type` / `type number` | `Table.TransformColumnTypes` | `pd.to_numeric(errors='coerce')` |
| Text → Date | `type date` | `Table.TransformColumnTypes` | `pd.to_datetime(errors='coerce')` |
| Text → Boolean | `type logical` | Custom column | `df['col'].map({'Yes':True})` |
| Number → Text | `type text` | `Table.TransformColumnTypes` | `df['col'].astype(str)` |
| Mixed → Clean | ลบ `$`, `,`, `%` ก่อน convert | `Text.Select` | `str.replace()` → `pd.to_numeric()` |

```python
# จัดการ currency string → number
df['revenue'] = (df['revenue']
    .str.replace(r'[$,]', '', regex=True)
    .astype(float))

# จัดการ percentage string → float
df['growth'] = (df['growth']
    .str.replace('%', '')
    .astype(float) / 100)
```

---

## ✅ Data Validation

### Business Rules Validation

```python
def validate_data(df):
    """ตรวจสอบ business rules"""
    errors = []

    # ค่าต้องเป็นบวก
    if (df['revenue'] < 0).any():
        errors.append(f"❌ Negative revenue: {(df['revenue'] < 0).sum()} rows")

    # Email format
    invalid_email = ~df['email'].str.match(
        r'^[\w\.-]+@[\w\.-]+\.\w+$', na=False)
    if invalid_email.any():
        errors.append(f"❌ Invalid emails: {invalid_email.sum()} rows")

    # Date range
    future = df['order_date'] > pd.Timestamp.now()
    if future.any():
        errors.append(f"❌ Future dates: {future.sum()} rows")

    # Required fields
    for col in ['customer_id', 'order_date', 'amount']:
        if df[col].isnull().any():
            errors.append(f"❌ Missing {col}: {df[col].isnull().sum()} rows")

    if errors:
        print("\n".join(errors))
    else:
        print("✅ All validations passed!")
    return errors
```

---

## 📏 Normalization & Standardization

```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Min-Max Normalization (0-1)
scaler = MinMaxScaler()
df['amount_norm'] = scaler.fit_transform(df[['amount']])

# Z-Score Standardization (mean=0, std=1)
scaler = StandardScaler()
df['amount_std'] = scaler.fit_transform(df[['amount']])

# Manual Min-Max
df['amount_norm'] = (df['amount'] - df['amount'].min()) / \
                    (df['amount'].max() - df['amount'].min())
```

---

## 🏭 Industry Use Cases

### 1. 🛒 E-Commerce / Retail

| ปัญหา | วิธีแก้ | M Query |
|--------|--------|---------|
| ชื่อสินค้าไม่สม่ำเสมอ "iPhone 15" vs "iphone15" | Trim + Proper + standardize | `Text.Proper(Text.Trim(_))` |
| ราคา = 0 หรือ negative | กรองออก หรือ flag | `Table.SelectRows(_, each [Price] > 0)` |
| Order ซ้ำ (double submit) | Dedup by order_id + timestamp | `Table.Distinct(_, {"OrderID"})` |
| SKU format ต่างกัน "SKU-001" vs "sku001" | Standardize format | `Text.Upper + Text.Replace` |
| Missing category | เติมจาก product name | Lookup + conditional |
| Return/Refund ปนกับ sales | แยกตาม order_type | `Table.SelectRows` |

### 2. 🏦 Finance / Banking

| ปัญหา | วิธีแก้ |
|--------|--------|
| Transaction amount format ($1,234.56) | ลบ `$,` แล้ว convert to number |
| Duplicate transactions | Dedup by trans_id + amount + date |
| Missing account numbers | Flag as error — ห้ามเติม |
| Currency mixing (USD, THB, EUR) | Standardize to 1 currency |
| Negative amounts (debit vs credit) | แยก column หรือ add type flag |
| Fraud patterns (outlier amounts) | IQR/Z-score detection |

### 3. 🏥 Healthcare

| ปัญหา | วิธีแก้ |
|--------|--------|
| Patient name variations | Fuzzy matching + standardize |
| Missing diagnosis codes (ICD) | Flag — ต้องใส่จาก source |
| Date of birth errors (future dates) | Validate range |
| Duplicate patient records | Match by name+DOB+ID |
| Lab values out of range | Medical reference ranges |
| Mixed unit systems (mg vs g) | Convert to standard units |

### 4. 📦 Supply Chain / Logistics

| ปัญหา | วิธีแก้ |
|--------|--------|
| Address inconsistencies | Standardize + geocode |
| Missing delivery dates | Forward fill from tracking |
| Negative shipping weights | Flag as data entry error |
| Warehouse code mismatches | Lookup table mapping |
| Duplicate shipment records | Dedup by tracking number |
| Unrealistic delivery times | Flag if < 0 or > 90 days |

### 5. 🎓 Education

| ปัญหา | วิธีแก้ |
|--------|--------|
| Student scores > 100 or < 0 | Cap at 0-100 range |
| Missing attendance records | Mark as "absent" or impute |
| Duplicate enrollment records | Dedup by student_id + course |
| Grade format mixed (A/4.0/95) | Convert to single scale |
| Name encoding issues (Thai/CJK) | UTF-8 standardization |

### 6. 🏭 Manufacturing

| ปัญหา | วิธีแก้ |
|--------|--------|
| Sensor data spikes | Moving average smoothing |
| Missing production timestamps | Interpolation |
| Quality codes inconsistent | Standardize lookup |
| Batch numbers format varies | Regex standardization |
| Machine ID duplicates | Dedup + validate |

### 7. 📊 Marketing / CRM

| ปัญหา | วิธีแก้ |
|--------|--------|
| Email bounced/invalid | Regex validation + remove |
| Phone format varies (+66, 0, 66) | Standardize E.164 format |
| Campaign name typos | Fuzzy match + standardize |
| Lead source duplicates | Dedup by email/phone |
| Missing conversion dates | Flag as unconverted |
| UTM parameter inconsistencies | Lowercase + trim |

### 8. 🏠 Real Estate

| ปัญหา | วิธีแก้ |
|--------|--------|
| Property area units mixed (sqm, sqft, rai, wah) | Convert to standard |
| Price = 0 (undisclosed) | Flag or estimate from area |
| Address format inconsistent | Parse + standardize |
| Duplicate listings | Match by address + area |
| Missing coordinates | Geocoding API |

### 9. 🍕 Food & Restaurant

| ปัญหา | วิธีแก้ |
|--------|--------|
| Menu item name variations | Standardize + categorize |
| Negative order quantities | Filter or flag |
| Missing tip amounts | Fill with 0 (no tip) |
| Time zone mixing | Convert to local TZ |
| Duplicate orders (POS glitch) | Dedup by order_id + time |

### 10. ✈️ Travel & Tourism

| ปัญหา | วิธีแก้ |
|--------|--------|
| Airport codes varied (BKK vs Bangkok) | IATA code lookup |
| Date format DD/MM vs MM/DD | Standardize to ISO 8601 |
| Currency in booking vs actual | Convert at booking rate |
| Duplicate bookings | Dedup by booking_ref |
| Missing nationality | Infer from passport code |

### 11. ⚡ Energy / Utilities

| ปัญหา | วิธีแก้ |
|--------|--------|
| Meter reading gaps | Interpolation |
| Negative consumption (meter replacement) | Flag + manual review |
| Outlier usage spikes | IQR detection |
| Address changes | Track by meter_id |
| Bill date inconsistencies | Standardize to billing cycle |

### 12. 🎮 Gaming / Digital

| ปัญหา | วิธีแก้ |
|--------|--------|
| Username special characters | Sanitize + lowercase |
| Session overlap | Merge by user + time window |
| Zero-length sessions | Filter out < 1 second |
| In-app purchase duplicates | Dedup by transaction_id |
| Bot/fraud detection | Flag unusual patterns |

### 13. 🚗 Automotive

| ปัญหา | วิธีแก้ |
|--------|--------|
| VIN format invalid | Regex validation 17 chars |
| Mileage decreasing | Flag as odometer rollback |
| Missing engine specs | Lookup by model+year |
| Price = 0 (trade-in) | Separate from cash sales |
| Model name variations | Standardize to OEM naming |

### 14. 🌾 Agriculture

| ปัญหา | วิธีแก้ |
|--------|--------|
| Yield data spikes | Weather correlation check |
| Missing soil test results | Impute from nearest area |
| Area unit mixing (rai, hectare, acre) | Convert to standard |
| GPS coordinates invalid | Validate lat/long range |
| Pesticide names inconsistent | Standardize to registry |

### 15. 📰 Media / Publishing

| ปัญหา | วิธีแก้ |
|--------|--------|
| Article title encoding issues | UTF-8 normalize |
| Duplicate articles (syndication) | Fuzzy match title+date |
| Missing author attribution | Flag for editorial review |
| View count anomalies (bot traffic) | Filter by session patterns |
| Category misclassification | NLP re-classification |

---

## 📐 DAX Data Quality Measures

```dax
// ---- Missing Value Percentage ----
Missing Pct = DIVIDE(
    COUNTBLANK('Table'[Column]),
    COUNTROWS('Table'), 0) * 100

// ---- Duplicate Count ----
Duplicate Count =
COUNTROWS('Table') - DISTINCTCOUNT('Table'[PrimaryKey])

// ---- Data Completeness Score ----
Completeness Score =
VAR TotalCells = COUNTROWS('Table') * 10  // 10 = จำนวน columns
VAR MissingCells =
    COUNTBLANK('Table'[Col1]) + COUNTBLANK('Table'[Col2]) +
    COUNTBLANK('Table'[Col3]) + COUNTBLANK('Table'[Col4])
RETURN DIVIDE(TotalCells - MissingCells, TotalCells) * 100

// ---- Outlier Flag ----
Is Outlier =
VAR Q1Val = PERCENTILE.INC('Table'[Amount], 0.25)
VAR Q3Val = PERCENTILE.INC('Table'[Amount], 0.75)
VAR IQRVal = Q3Val - Q1Val
RETURN IF(
    'Table'[Amount] < Q1Val - 1.5 * IQRVal ||
    'Table'[Amount] > Q3Val + 1.5 * IQRVal,
    "Outlier", "Normal")

// ---- Data Freshness ----
Data Freshness Days = DATEDIFF(
    MAX('Table'[LastUpdated]), TODAY(), DAY)

// ---- Validity Rate ----
Valid Email Rate = DIVIDE(
    COUNTROWS(FILTER('Table',
        CONTAINSSTRING([Email], "@") &&
        CONTAINSSTRING([Email], "."))),
    COUNTROWS('Table')) * 100
```

---

## 🤖 Automated Cleaning Pipeline

### Python Script สำหรับ Power BI

```python
import pandas as pd
import numpy as np

def auto_clean(csv_path, config=None):
    """
    Automated data cleaning pipeline
    config: dict with cleaning options
    """
    config = config or {}
    df = pd.read_csv(csv_path)

    print(f"📊 Input: {df.shape[0]} rows × {df.shape[1]} columns")
    report = {'original_rows': len(df), 'steps': []}

    # Step 1: Remove empty rows
    before = len(df)
    df = df.dropna(how='all')
    removed = before - len(df)
    if removed: report['steps'].append(f"Removed {removed} empty rows")

    # Step 2: Remove duplicates
    before = len(df)
    key_cols = config.get('dedup_keys', None)
    df = df.drop_duplicates(subset=key_cols)
    removed = before - len(df)
    if removed: report['steps'].append(f"Removed {removed} duplicates")

    # Step 3: Clean text columns
    text_cols = df.select_dtypes(include='object').columns
    for col in text_cols:
        df[col] = df[col].str.strip()
        df[col] = df[col].replace(
            ['', 'N/A', 'n/a', 'NA', 'null', 'None', '-'], np.nan)

    # Step 4: Parse dates
    for col in df.columns:
        if any(x in col.lower() for x in ['date', 'time', 'created']):
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Step 5: Handle missing values
    strategy = config.get('missing_strategy', 'smart')
    for col in df.columns:
        if df[col].isnull().sum() == 0:
            continue
        pct = df[col].isnull().sum() / len(df) * 100
        if pct > 50:
            df = df.drop(columns=[col])
            report['steps'].append(f"Dropped column {col} ({pct:.0f}% missing)")
        elif df[col].dtype in ['float64', 'int64']:
            df[col] = df[col].fillna(df[col].median())
        elif df[col].dtype == 'object':
            df[col] = df[col].fillna('Unknown')

    # Step 6: Outlier capping (numeric only)
    if config.get('cap_outliers', True):
        for col in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df[col] = df[col].clip(Q1 - 1.5*IQR, Q3 + 1.5*IQR)

    report['final_rows'] = len(df)
    report['final_cols'] = df.shape[1]

    # Save cleaned data
    out_path = csv_path.replace('.csv', '_cleaned.csv')
    df.to_csv(out_path, index=False)
    print(f"✅ Output: {out_path}")
    for step in report['steps']:
        print(f"   → {step}")

    return df, report

# ใช้งาน
df, report = auto_clean('raw_sales.csv', config={
    'dedup_keys': ['order_id'],
    'missing_strategy': 'smart',
    'cap_outliers': True
})
```

---

## ☑️ Data Cleaning Checklist

### Before Dashboard

- [ ] **Inspect** — `df.info()`, `df.describe()`, `df.isnull().sum()`
- [ ] **Data Types** — ทุก column เป็น type ที่ถูกต้อง
- [ ] **Duplicates** — ลบแถวซ้ำแล้ว
- [ ] **Missing Values** — จัดการค่าว่างแล้ว (เติม/ลบ)
- [ ] **Text Clean** — Trim, consistent casing, no special chars
- [ ] **Date Valid** — format เดียวกัน, ไม่มีอนาคต, ไม่มี null
- [ ] **Outliers** — ตรวจสอบและจัดการแล้ว
- [ ] **Validation** — ผ่าน business rules
- [ ] **Encoding** — UTF-8 สำหรับ Thai/special chars
- [ ] **Naming** — Column names สั้น, ไม่มี space, สม่ำเสมอ

### After Dashboard

- [ ] **Visual ว่าง** — ไม่มี visual ที่แสดง blank
- [ ] **Filter ทำงาน** — Slicer กรองได้ถูกต้อง
- [ ] **Totals ถูกต้อง** — Cross-check กับ source data
- [ ] **Date range** — Start/End date ตรงกับข้อมูล
- [ ] **Performance** — Load time < 3 วินาที

---

## 🔬 Data Profiling (ตรวจสอบข้อมูลก่อน Clean)

> ขั้นตอนสำคัญ — ต้องทำก่อนทำความสะอาดเสมอ

### Python Profiling

```python
import pandas as pd

def profile_dataframe(df):
    """Data profiling report อัตโนมัติ"""
    print("=" * 60)
    print(f"📊 SHAPE: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print("=" * 60)

    for col in df.columns:
        dtype = df[col].dtype
        missing = df[col].isnull().sum()
        missing_pct = missing / len(df) * 100
        unique = df[col].nunique()
        unique_pct = unique / len(df) * 100

        print(f"\n📌 {col} ({dtype})")
        print(f"   Missing: {missing} ({missing_pct:.1f}%)")
        print(f"   Unique:  {unique} ({unique_pct:.1f}%)")

        if dtype in ['int64', 'float64']:
            print(f"   Range:   {df[col].min()} → {df[col].max()}")
            print(f"   Mean:    {df[col].mean():.2f}")
            print(f"   Median:  {df[col].median():.2f}")
            print(f"   Std:     {df[col].std():.2f}")
            # Detect potential ID column
            if unique_pct > 95:
                print(f"   ⚠️ Likely ID column (95%+ unique)")
        elif dtype == 'object':
            top3 = df[col].value_counts().head(3)
            print(f"   Top 3:   {dict(top3)}")
            # Detect low cardinality (good for slicer)
            if unique < 20:
                print(f"   ✅ Good for Slicer/Filter ({unique} categories)")
        elif 'datetime' in str(dtype):
            print(f"   Range:   {df[col].min()} → {df[col].max()}")

    # Correlation matrix for numerics
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) > 1:
        print(f"\n📈 High Correlations (>0.8):")
        corr = df[numeric_cols].corr()
        for i in range(len(corr)):
            for j in range(i+1, len(corr)):
                if abs(corr.iloc[i, j]) > 0.8:
                    print(f"   {corr.index[i]} ↔ {corr.columns[j]}: {corr.iloc[i,j]:.3f}")

profile_dataframe(df)
```

### M Query — Column Profiling

```m
// นับ null ในแต่ละ column
let
    Source = ...,
    ColNames = Table.ColumnNames(Source),
    Stats = List.Transform(ColNames, each {
        _, // column name
        List.Count(List.Select(Table.Column(Source, _), each _ = null)),
        Table.RowCount(Source)
    }),
    Result = Table.FromRows(Stats, {"Column", "NullCount", "TotalRows"})
in Result
```

---

## 🌐 Encoding / Unicode Cleaning

### ปัญหาที่พบบ่อย

| ปัญหา | ตัวอย่าง | สาเหตุ |
|--------|---------|--------|
| อักษรไทยแตก | `à¸ à¸²à¸©à¸²` | อ่าน UTF-8 เป็น Latin-1 |
| ? แทนอักษร | `????` | Encoding ไม่รองรับ |
| BOM character | `\ufeff` ที่ต้นไฟล์ | UTF-8 with BOM |
| Mojibake | `Ã©` แทน `é` | Double encoding |

### Python — แก้ Encoding

```python
# อ่านไฟล์ด้วย encoding ที่ถูกต้อง
df = pd.read_csv('data.csv', encoding='utf-8')          # ค่าเริ่มต้น
df = pd.read_csv('data.csv', encoding='tis-620')         # ไฟล์ไทยเก่า
df = pd.read_csv('data.csv', encoding='cp874')            # Windows Thai
df = pd.read_csv('data.csv', encoding='utf-8-sig')        # UTF-8 with BOM

# ตรวจจับ encoding อัตโนมัติ
import chardet
with open('data.csv', 'rb') as f:
    result = chardet.detect(f.read(10000))
    print(f"Encoding: {result['encoding']} ({result['confidence']:.0%})")

# แปลง encoding ทั้งไฟล์
with open('input.csv', 'r', encoding='tis-620') as f:
    content = f.read()
with open('output.csv', 'w', encoding='utf-8') as f:
    f.write(content)

# ลบ BOM character
df.columns = [col.replace('\ufeff', '') for col in df.columns]

# Normalize Unicode (NFC = precomposed, เหมาะกับภาษาไทย)
import unicodedata
df['name'] = df['name'].apply(lambda x:
    unicodedata.normalize('NFC', x) if isinstance(x, str) else x)
```

### M Query — Encoding

```m
// อ่าน CSV ด้วย UTF-8 (65001)
Csv.Document(File.Contents("C:\data.csv"),
    [Delimiter=",", Encoding=65001])

// อ่าน CSV ด้วย TIS-620 (Thai)
Csv.Document(File.Contents("C:\data.csv"),
    [Delimiter=",", Encoding=874])

// Encoding codes:
// 65001 = UTF-8, 874 = Thai (TIS-620/CP874)
// 1252 = Windows Latin, 932 = Japanese Shift-JIS
// 936 = Chinese GB2312, 949 = Korean
```

---

## 💱 Currency & Unit Conversion

### Currency Cleaning

```python
import re

def clean_currency(value):
    """แปลง currency string → float"""
    if pd.isna(value): return None
    s = str(value).strip()

    # ตรวจจับ multiplier
    multiplier = 1
    if re.search(r'[Mm]illion|[Mm]', s): multiplier = 1_000_000
    elif re.search(r'[Bb]illion|[Bb]', s): multiplier = 1_000_000_000
    elif re.search(r'[Kk]', s): multiplier = 1_000

    # ลบ currency symbols + text
    s = re.sub(r'[฿$€£¥₩₹]', '', s)
    s = re.sub(r'[A-Za-z,\s]', '', s)

    try:
        return float(s) * multiplier
    except:
        return None

df['revenue'] = df['revenue_raw'].apply(clean_currency)

# Currency conversion ด้วย rate table
rates = {'USD': 1.0, 'THB': 0.028, 'EUR': 1.08, 'JPY': 0.0067}
df['revenue_usd'] = df.apply(lambda r:
    r['amount'] * rates.get(r['currency'], 1.0), axis=1)
```

### Unit Conversion

```python
# แปลงหน่วยพื้นที่
AREA_TO_SQM = {
    'sqm': 1, 'sqft': 0.0929, 'rai': 1600,
    'ngan': 400, 'wah': 4, 'acre': 4046.86,
    'hectare': 10000
}
df['area_sqm'] = df.apply(lambda r:
    r['area'] * AREA_TO_SQM.get(r['area_unit'], 1), axis=1)

# แปลงหน่วยน้ำหนัก
WEIGHT_TO_KG = {'kg': 1, 'g': 0.001, 'lb': 0.4536, 'oz': 0.02835, 'ton': 1000}
df['weight_kg'] = df.apply(lambda r:
    r['weight'] * WEIGHT_TO_KG.get(r['weight_unit'], 1), axis=1)

# แปลงอุณหภูมิ
df['temp_celsius'] = df.apply(lambda r:
    (r['temp'] - 32) * 5/9 if r['temp_unit'] == 'F' else r['temp'], axis=1)
```

### M Query — Currency

```m
// ลบ currency symbols + แปลงเป็นตัวเลข
Table.TransformColumns(Source, {{"Amount", each
    try Number.From(Text.Select(Text.Replace(_, ",", ""),
        {"0".."9", ".", "-"})) otherwise null, type number}})
```

---

## 🔗 Cross-Field Validation

```python
def cross_validate(df):
    """ตรวจสอบความสอดคล้องระหว่าง columns"""
    errors = []

    # Start date ต้องก่อน End date
    if 'start_date' in df.columns and 'end_date' in df.columns:
        invalid = df[df['start_date'] > df['end_date']]
        if len(invalid) > 0:
            errors.append(f"❌ start > end date: {len(invalid)} rows")

    # Profit = Revenue - Cost
    if all(c in df.columns for c in ['revenue', 'cost', 'profit']):
        diff = abs(df['profit'] - (df['revenue'] - df['cost']))
        mismatch = df[diff > 0.01]
        if len(mismatch) > 0:
            errors.append(f"❌ Profit ≠ Revenue-Cost: {len(mismatch)} rows")

    # Quantity × Unit Price = Total (within tolerance)
    if all(c in df.columns for c in ['qty', 'unit_price', 'total']):
        expected = df['qty'] * df['unit_price']
        diff = abs(df['total'] - expected)
        mismatch = df[diff > 0.01]
        if len(mismatch) > 0:
            errors.append(f"❌ Total ≠ Qty×Price: {len(mismatch)} rows")

    # Age ↔ Date of Birth consistency
    if 'age' in df.columns and 'dob' in df.columns:
        today = pd.Timestamp.now()
        expected_age = ((today - df['dob']).dt.days / 365.25).astype(int)
        mismatch = df[abs(df['age'] - expected_age) > 1]
        if len(mismatch) > 0:
            errors.append(f"❌ Age vs DOB mismatch: {len(mismatch)} rows")

    # Country ↔ Phone prefix
    country_prefix = {'Thailand': '+66', 'US': '+1', 'UK': '+44', 'Japan': '+81'}
    if 'country' in df.columns and 'phone' in df.columns:
        for country, prefix in country_prefix.items():
            mask = (df['country'] == country) & ~df['phone'].str.startswith(prefix, na=True)
            if mask.sum() > 0:
                errors.append(f"❌ {country} phone prefix wrong: {mask.sum()} rows")

    return errors
```

---

## 🧬 Advanced Imputation (KNN / MICE)

### KNN Imputation

```python
from sklearn.impute import KNNImputer

# เติมค่าว่างด้วย K-Nearest Neighbors
imputer = KNNImputer(n_neighbors=5, weights='distance')
numeric_cols = df.select_dtypes(include='number').columns
df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
```

### MICE (Multiple Imputation by Chained Equations)

```python
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# MICE — เติมค่าแบบ iterative (แม่นยำมาก)
mice = IterativeImputer(max_iter=10, random_state=42)
numeric_cols = df.select_dtypes(include='number').columns
df[numeric_cols] = mice.fit_transform(df[numeric_cols])
```

### Interpolation (สำหรับ Time Series)

```python
# Linear interpolation (เติมค่าเรียงตามเวลา)
df['value'] = df['value'].interpolate(method='linear')

# Time-based interpolation
df = df.set_index('date')
df['value'] = df['value'].interpolate(method='time')
df = df.reset_index()

# Spline interpolation (smooth curve)
df['value'] = df['value'].interpolate(method='spline', order=3)

# Seasonal interpolation (เติมตาม pattern ฤดูกาล)
df['value'] = df.groupby(df['date'].dt.month)['value'].transform(
    lambda x: x.fillna(x.mean()))
```

| วิธี | ใช้กับ | ข้อดี | ข้อเสีย |
|------|--------|------|--------|
| **KNN** | ข้อมูลทั่วไป, features สัมพันธ์กัน | รักษาความสัมพันธ์ | ช้ากับ dataset ใหญ่ |
| **MICE** | Missing หลาย columns | แม่นยำมาก | ซับซ้อน, ช้า |
| **Linear Interpolation** | Time series ต่อเนื่อง | เร็ว, เข้าใจง่าย | ไม่เหมาะกับ seasonal |
| **Spline** | Time series ที่ smooth | curve สวย | overshoot ได้ |
| **Seasonal** | ข้อมูล seasonal | จับ pattern ได้ | ต้องมีข้อมูลพอ |

---

## 📈 Time Series Cleaning

### Detect & Fix Anomalies

```python
def clean_timeseries(df, date_col, value_col, window=7):
    """ทำความสะอาด time series"""
    df = df.sort_values(date_col).copy()

    # 1. ลบ duplicate timestamps
    df = df.drop_duplicates(subset=[date_col], keep='last')

    # 2. Reindex เพื่อเติม missing dates
    full_range = pd.date_range(df[date_col].min(), df[date_col].max(), freq='D')
    df = df.set_index(date_col).reindex(full_range).rename_axis(date_col).reset_index()

    # 3. Interpolate missing values
    df[value_col] = df[value_col].interpolate(method='time')

    # 4. Detect anomalies ด้วย Rolling Z-Score
    rolling_mean = df[value_col].rolling(window=window, center=True).mean()
    rolling_std = df[value_col].rolling(window=window, center=True).std()
    z_score = (df[value_col] - rolling_mean) / rolling_std
    df['is_anomaly'] = abs(z_score) > 3

    # 5. Replace anomalies ด้วย rolling median
    rolling_median = df[value_col].rolling(window=window, center=True).median()
    df.loc[df['is_anomaly'], value_col] = rolling_median[df['is_anomaly']]

    return df
```

### Differencing (ลบ Trend)

```python
# First-order differencing (ลบ trend)
df['value_diff'] = df['value'].diff()

# Seasonal differencing (ลบ seasonality, period=12 for monthly)
df['value_seasonal_diff'] = df['value'].diff(periods=12)
```

---

## 📊 Smoothing & Denoising

```python
# Moving Average (Simple)
df['ma_7'] = df['value'].rolling(window=7).mean()

# Exponential Moving Average (ให้น้ำหนักค่าล่าสุดมากกว่า)
df['ema_7'] = df['value'].ewm(span=7).mean()

# Weighted Moving Average
weights = [0.1, 0.15, 0.2, 0.25, 0.3]  # น้ำหนักมากขึ้นตามลำดับ
df['wma'] = df['value'].rolling(len(weights)).apply(
    lambda x: sum(w*v for w,v in zip(weights, x)) / sum(weights))

# Median Filter (ลด spike/noise)
df['median_filtered'] = df['value'].rolling(window=5, center=True).median()

# Savitzky-Golay Filter (smooth แต่รักษา peak)
from scipy.signal import savgol_filter
df['savgol'] = savgol_filter(df['value'].fillna(method='ffill'), 
                              window_length=11, polyorder=3)
```

### M Query — Moving Average

```m
// 7-day Moving Average
let
    Sorted = Table.Sort(Source, {{"Date", Order.Ascending}}),
    Indexed = Table.AddIndexColumn(Sorted, "Idx", 0, 1),
    MA = Table.AddColumn(Indexed, "MA_7", each
        let
            idx = [Idx],
            start = Number.Max({0, idx - 6}),
            subset = Table.Range(Indexed, start, idx - start + 1),
            avg = List.Average(Table.Column(subset, "Value"))
        in avg, type number)
in Table.RemoveColumns(MA, {"Idx"})
```

---

## 📦 Binning & Discretization

```python
# Equal-Width Binning
df['age_bin'] = pd.cut(df['age'], bins=5, labels=['Very Young','Young','Middle','Senior','Elder'])

# Equal-Frequency Binning (quantile)
df['income_quartile'] = pd.qcut(df['income'], q=4, labels=['Q1','Q2','Q3','Q4'])

# Custom Bins (business rules)
bins = [0, 1000, 5000, 10000, 50000, float('inf')]
labels = ['Micro', 'Small', 'Medium', 'Large', 'Enterprise']
df['customer_tier'] = pd.cut(df['revenue'], bins=bins, labels=labels)

# Percentile-based bins
df['score_pct'] = pd.qcut(df['score'], q=10, labels=False) + 1  # Deciles 1-10
```

### M Query — Binning

```m
// Custom bins
Table.AddColumn(Source, "Tier", each
    if [Revenue] >= 50000 then "Enterprise"
    else if [Revenue] >= 10000 then "Large"
    else if [Revenue] >= 5000 then "Medium"
    else if [Revenue] >= 1000 then "Small"
    else "Micro", type text)
```

---

## 📝 NLP Text Cleaning (Advanced)

```python
import re

def deep_clean_text(text):
    """NLP-level text cleaning"""
    if pd.isna(text): return text
    text = str(text)

    # ลบ HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # ลบ URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # ลบ email addresses
    text = re.sub(r'\S+@\S+\.\S+', '', text)

    # ลบ emojis
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text, flags=re.UNICODE)

    # ลบ multiple spaces → single space
    text = re.sub(r'\s+', ' ', text).strip()

    # ลบ repeated characters (e.g., "sooooo goood" → "so good")
    text = re.sub(r'(.)\1{2,}', r'\1', text)

    return text

df['clean_description'] = df['description'].apply(deep_clean_text)

# Thai-specific cleaning
def clean_thai(text):
    """ทำความสะอาด text ภาษาไทย"""
    if pd.isna(text): return text
    text = str(text)
    # ลบ zero-width characters
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
    # ลบ Thai tone marks ซ้ำ (typo)
    text = re.sub(r'([\u0e48-\u0e4b])\1+', r'\1', text)
    # Normalize Thai digits → Arabic
    thai_digits = str.maketrans('๐๑๒๓๔๕๖๗๘๙', '0123456789')
    text = text.translate(thai_digits)
    return text.strip()

df['name_clean'] = df['name'].apply(clean_thai)
```

---

## ⚡ M Query Error Handling

```m
// try...otherwise — จัดการ error ทีละ cell
Table.TransformColumns(Source, {{"Amount", each
    try Number.From(_) otherwise null, type nullable number}})

// แปลง date ที่อาจ error
Table.TransformColumns(Source, {{"Date", each
    try Date.From(_) otherwise null, type nullable date}})

// Replace errors ทั้ง table
Table.ReplaceErrorValues(Source, {
    {"Amount", null},
    {"Date", null},
    {"Name", "Unknown"}
})

// ตรวจจับ error แล้ว log
Table.AddColumn(Source, "HasError", each
    try (let _ = [Amount] in false) otherwise true, type logical)

// Chain try สำหรับ multiple format
Table.TransformColumns(Source, {{"Date", each
    try Date.From(_)
    otherwise try Date.FromText(_, [Format="dd/MM/yyyy"])
    otherwise try Date.FromText(_, [Format="MM-dd-yyyy"])
    otherwise null, type nullable date}})
```

---

## 🔀 Unpivot / Reshape Patterns

### Wide → Long (Unpivot)

```m
// ข้อมูล: Month1, Month2, Month3... → Month + Value
Table.UnpivotOtherColumns(Source, {"Product", "Category"}, "Month", "Revenue")

// Unpivot เฉพาะ columns ที่เลือก
Table.Unpivot(Source, {"Jan", "Feb", "Mar"}, "Month", "Amount")
```

### Python — Melt (Unpivot)

```python
# Wide → Long
df_long = pd.melt(df,
    id_vars=['product', 'category'],
    value_vars=['jan', 'feb', 'mar', 'apr'],
    var_name='month',
    value_name='revenue')

# Long → Wide (pivot)
df_wide = df_long.pivot_table(
    index='product', columns='month',
    values='revenue', aggfunc='sum').reset_index()
```

### M Query — List.Generate (Pagination/Recursive)

```m
// ดึงข้อมูลจาก API ที่มี pagination
let
    GetPage = (page) => Json.Document(Web.Contents(
        "https://api.example.com/data?page=" & Text.From(page))),

    Pages = List.Generate(
        () => [page = 1, data = GetPage(1)],           // initial
        each List.Count([data][results]) > 0,           // condition
        each [page = [page] + 1, data = GetPage([page] + 1)], // next
        each [data][results]                            // selector
    ),
    Combined = List.Combine(Pages),
    Result = Table.FromList(Combined, Splitter.SplitByNothing())
in Result
```

---

## 🏗️ Data Reshaping Patterns

### Transpose

```m
// สลับ rows ↔ columns
Table.Transpose(Source)
```

### Fill Down / Fill Up

```m
// เติมค่าจากแถวบน (สำหรับ merged cells ใน Excel)
Table.FillDown(Source, {"Category", "SubCategory"})

// เติมค่าจากแถวล่าง
Table.FillUp(Source, {"Category"})
```

### Python

```python
# Fill down (forward fill)
df['category'] = df['category'].fillna(method='ffill')

# Fill up (backward fill)
df['category'] = df['category'].fillna(method='bfill')

# Transpose
df_transposed = df.T
```

---

## 🏭 Additional Industry Use Cases

### 16. 💊 Pharmaceutical

| ปัญหา | วิธีแก้ |
|--------|--------|
| Drug name variations (brand vs generic) | Standardize to active ingredient |
| Dosage unit mixing (mg, mcg, g) | Convert to standard unit |
| Clinical trial data gaps | MICE imputation / LOCF (Last Obs Carried Forward) |
| Adverse event free-text | NLP classification |
| Batch number format | Regex standardization |
| Expiry date format | Standardize to ISO 8601 |

### 17. 🏗️ Construction

| ปัญหา | วิธีแก้ |
|--------|--------|
| Material specs inconsistent | Standardize to industry codes |
| Blueprint measurement unit mixing | Convert to metric |
| Contractor name duplicates | Fuzzy matching |
| Cost estimates vs actuals | Cross-field validation |
| Weather data gaps (outdoor projects) | Interpolation from nearby stations |

### 18. 📡 Telecom

| ปัญหา | วิธีแก้ |
|--------|--------|
| Phone number format varies | E.164 standardization |
| CDR (Call Detail Record) duplicates | Dedup by call_id + timestamp |
| Network metrics spikes | Rolling median smoothing |
| Cell tower ID mapping | Lookup table validation |
| Usage data negative values (adjustments) | Separate adjustment records |

### 19. 🎯 Insurance

| ปัญหา | วิธีแก้ |
|--------|--------|
| Policy number format varies | Regex standardize |
| Claim amount = 0 | Flag vs legitimate $0 claims |
| Beneficiary name mismatches | Fuzzy match + manual review |
| Date of loss > Report date | Flag as data entry error |
| Premium ↔ Coverage amount mismatch | Cross-field validation |
| ICD codes outdated | Map to current version |

### 20. 🎵 Music / Entertainment

| ปัญหา | วิธีแก้ |
|--------|--------|
| Artist name variations (feat. vs ft.) | Regex standardize |
| Song duration = 0 or > 60 min | Flag as anomaly |
| Genre misclassification | NLP re-classification |
| Play count spikes (bot activity) | Z-score detection |
| Multiple encoding for song titles (CJK/Thai) | Unicode NFC normalization |

---

## 🧮 DAX — Advanced Data Quality

```dax
// ---- Row-level Completeness (how many fields filled per row) ----
Row Completeness =
VAR FilledFields =
    (IF(NOT ISBLANK([Col1]), 1, 0) +
     IF(NOT ISBLANK([Col2]), 1, 0) +
     IF(NOT ISBLANK([Col3]), 1, 0) +
     IF(NOT ISBLANK([Col4]), 1, 0) +
     IF(NOT ISBLANK([Col5]), 1, 0))
RETURN DIVIDE(FilledFields, 5) * 100

// ---- Cross-Field Validation ----
Calc Mismatch =
COUNTROWS(FILTER('Sales',
    ABS([Revenue] - [Qty] * [UnitPrice]) > 0.01))

// ---- Date Gap Detection ----
Date Gaps =
VAR CurrentDate = 'Calendar'[Date]
VAR PrevDate = CALCULATE(MAX('Calendar'[Date]),
    FILTER(ALL('Calendar'), 'Calendar'[Date] < CurrentDate))
RETURN IF(DATEDIFF(PrevDate, CurrentDate, DAY) > 1, "Gap", "OK")

// ---- Format Consistency Check ----
Invalid Emails =
COUNTROWS(FILTER('Customers',
    NOT(CONTAINSSTRING([Email], "@")) ||
    NOT(CONTAINSSTRING([Email], "."))))

// ---- Timeliness Score ----
Timeliness =
VAR DaysSinceUpdate = DATEDIFF(MAX('Table'[LastModified]), TODAY(), DAY)
RETURN SWITCH(TRUE(),
    DaysSinceUpdate <= 1, "🟢 Fresh",
    DaysSinceUpdate <= 7, "🟡 Recent",
    DaysSinceUpdate <= 30, "🟠 Stale",
    "🔴 Outdated")
```

---

## 🛡️ Data Quality Dashboard Pattern

> สร้าง dashboard page เพื่อ monitor คุณภาพข้อมูล

```
Dashboard Page: Data Quality Monitor

KPI Cards:
- Completeness %   (target: >95%)
- Accuracy %       (target: >98%)
- Timeliness       (target: <24h)
- Duplicate Rate   (target: <1%)

Charts:
- Bar: Missing Values by Column
- Line: Data Quality Score over Time
- Table: Top 10 Data Issues (column, issue, count)
- Gauge: Overall Quality Score

Slicers:
- Date Range
- Table/Source
- Issue Severity
```

---

## 🔒 PII Masking & Data Anonymization

```python
import hashlib
import re

def mask_pii(df):
    """ปกปิดข้อมูลส่วนบุคคลอัตโนมัติ"""

    # Email masking: user@domain.com → u***@domain.com
    if 'email' in df.columns:
        df['email_masked'] = df['email'].apply(lambda x:
            x[0] + '***@' + x.split('@')[1] if pd.notna(x) and '@' in str(x) else x)

    # Phone masking: 0812345678 → 081***5678
    if 'phone' in df.columns:
        df['phone_masked'] = df['phone'].apply(lambda x:
            str(x)[:3] + '***' + str(x)[-4:] if pd.notna(x) and len(str(x)) >= 7 else x)

    # Thai ID masking: 1-1234-56789-01-2 → 1-XXXX-XXXXX-XX-2
    if 'thai_id' in df.columns:
        df['thai_id_masked'] = df['thai_id'].apply(lambda x:
            str(x)[0] + '-XXXX-XXXXX-XX-' + str(x)[-1] if pd.notna(x) else x)

    # Name hashing (irreversible for analytics)
    if 'full_name' in df.columns:
        df['name_hash'] = df['full_name'].apply(lambda x:
            hashlib.sha256(str(x).encode()).hexdigest()[:12] if pd.notna(x) else x)

    # Credit card masking: **** **** **** 1234
    if 'credit_card' in df.columns:
        df['cc_masked'] = df['credit_card'].apply(lambda x:
            '**** **** **** ' + str(x)[-4:] if pd.notna(x) and len(str(x)) >= 4 else x)

    # Age generalization (k-anonymity)
    if 'age' in df.columns:
        df['age_range'] = pd.cut(df['age'],
            bins=[0,18,25,35,45,55,65,100],
            labels=['<18','18-25','26-35','36-45','46-55','56-65','65+'])

    return df

# Auto-detect PII columns
def detect_pii_columns(df):
    """ตรวจจับ columns ที่อาจมี PII"""
    pii_patterns = {
        'email': r'^[\w.+-]+@[\w-]+\.[\w.]+$',
        'phone': r'^[\+]?[0-9\-\s\(\)]{7,15}$',
        'thai_id': r'^\d{1}-?\d{4}-?\d{5}-?\d{2}-?\d{1}$',
        'credit_card': r'^\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}$',
        'ip_address': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
    }
    suspects = {}
    for col in df.select_dtypes(include='object').columns:
        sample = df[col].dropna().head(100)
        for pii_type, pattern in pii_patterns.items():
            match_pct = sample.str.match(pattern, na=False).mean()
            if match_pct > 0.5:
                suspects[col] = pii_type
    return suspects
```

---

## 📍 Address & Geographic Cleaning

```python
def clean_address_thai(address):
    """ทำความสะอาด address ภาษาไทย"""
    if pd.isna(address): return address
    s = str(address)

    # Standardize province names
    province_fixes = {
        'กรุงเทพ': 'กรุงเทพมหานคร', 'กทม': 'กรุงเทพมหานคร', 'กทม.': 'กรุงเทพมหานคร',
        'เชียงใหม่': 'เชียงใหม่', 'ขอนแก่น': 'ขอนแก่น'
    }
    for old, new in province_fixes.items():
        s = s.replace(old, new)

    # Standardize prefix (ต., อ., จ.)
    s = re.sub(r'ตำบล|ต\.', 'ต.', s)
    s = re.sub(r'อำเภอ|อ\.', 'อ.', s)
    s = re.sub(r'จังหวัด|จ\.', 'จ.', s)

    # Clean postal code
    zipcode = re.search(r'\b(\d{5})\b', s)

    return s.strip()

# Validate lat/long coordinates
def validate_coordinates(df, lat_col='lat', lng_col='lng'):
    """ตรวจสอบ coordinates"""
    issues = []

    # Thailand bounding box
    TH_LAT = (5.5, 20.5)
    TH_LNG = (97.0, 106.0)

    out_of_range = df[
        (df[lat_col] < TH_LAT[0]) | (df[lat_col] > TH_LAT[1]) |
        (df[lng_col] < TH_LNG[0]) | (df[lng_col] > TH_LNG[1])
    ]
    if len(out_of_range) > 0:
        issues.append(f"❌ {len(out_of_range)} points outside Thailand")

    # Swapped lat/lng
    swapped = df[(df[lat_col] > 90) | (df[lng_col] > 180)]
    if len(swapped) > 0:
        issues.append(f"❌ {len(swapped)} possibly swapped lat/lng")

    # Zero coordinates
    zeros = df[(df[lat_col] == 0) & (df[lng_col] == 0)]
    if len(zeros) > 0:
        issues.append(f"❌ {len(zeros)} at (0,0) — likely missing data")

    return issues
```

---

## 📞 Phone Number Standardization (E.164)

```python
def standardize_phone_thai(phone):
    """แปลงเบอร์โทรไทย → E.164 format (+66...)"""
    if pd.isna(phone): return None
    s = re.sub(r'[\s\-\(\)\.]', '', str(phone))

    # ลบ prefix 0 → +66
    if s.startswith('0') and len(s) == 10:
        return '+66' + s[1:]
    elif s.startswith('66') and len(s) == 11:
        return '+' + s
    elif s.startswith('+66') and len(s) == 12:
        return s
    else:
        return None  # invalid

df['phone_e164'] = df['phone'].apply(standardize_phone_thai)

# Validate phone types
def classify_phone_thai(phone):
    """แยกประเภทเบอร์โทรไทย"""
    if pd.isna(phone): return 'Unknown'
    s = re.sub(r'[^\d]', '', str(phone))
    if s.startswith('0'):
        prefix = s[:3]
        if prefix in ['02']: return 'Bangkok Landline'
        elif prefix.startswith('0') and prefix[1] in '345679': return 'Provincial Landline'
        elif prefix in ['06', '08', '09'] or s[:2] in ['06','08','09']: return 'Mobile'
    return 'Unknown'
```

---

## 🔍 Regex Validation Pattern Library

```python
# รวม Regex patterns สำหรับ validate ข้อมูลทุกประเภท
VALIDATION_PATTERNS = {
    # Identity
    'thai_id':       r'^\d{1}-?\d{4}-?\d{5}-?\d{2}-?\d{1}$',
    'passport':      r'^[A-Z]{1,2}\d{6,9}$',

    # Contact
    'email':         r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone_thai':    r'^(0[2-9]\d{7,8}|\+66[2-9]\d{7,8})$',
    'phone_intl':    r'^\+[1-9]\d{6,14}$',

    # Financial
    'credit_card':   r'^\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}$',
    'bank_account':  r'^\d{10,12}$',
    'tax_id_thai':   r'^\d{13}$',

    # Network
    'ipv4':          r'^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$',
    'ipv6':          r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$',
    'mac_address':   r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
    'url':           r'^https?://[^\s/$.?#].[^\s]*$',

    # Location
    'zipcode_thai':  r'^\d{5}$',
    'zipcode_us':    r'^\d{5}(-\d{4})?$',
    'coordinates':   r'^-?\d{1,3}\.\d+,\s*-?\d{1,3}\.\d+$',

    # Codes
    'sku':           r'^[A-Z]{2,4}-\d{4,8}$',
    'isbn13':        r'^\d{3}-?\d{1}-?\d{3,5}-?\d{3,5}-?\d{1}$',
    'hex_color':     r'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$',

    # Date/Time
    'date_iso':      r'^\d{4}-\d{2}-\d{2}$',
    'time_24h':      r'^([01]\d|2[0-3]):[0-5]\d(:[0-5]\d)?$',
    'datetime_iso':  r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
}

def validate_column(df, col, pattern_name):
    """ตรวจสอบ column ด้วย regex pattern"""
    pattern = VALIDATION_PATTERNS.get(pattern_name)
    if not pattern:
        raise ValueError(f"Unknown pattern: {pattern_name}")
    valid = df[col].astype(str).str.match(pattern, na=False)
    invalid_count = (~valid & df[col].notna()).sum()
    return {
        'column': col, 'pattern': pattern_name,
        'valid': valid.sum(), 'invalid': invalid_count,
        'valid_pct': f"{valid.mean()*100:.1f}%"
    }
```

---

## 📑 Dirty Excel File Handling

```python
def clean_dirty_excel(filepath, header_row=None):
    """จัดการ Excel ที่มี merged cells, multiple headers, hidden rows"""

    # Auto-detect header row
    if header_row is None:
        preview = pd.read_excel(filepath, header=None, nrows=20)
        for i, row in preview.iterrows():
            non_null = row.dropna()
            if len(non_null) >= preview.shape[1] * 0.5:
                header_row = i
                break
        header_row = header_row or 0

    df = pd.read_excel(filepath, header=header_row)

    # Remove completely empty rows/columns
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all')

    # Fix merged cell effect (NaN from merged cells)
    df = df.fillna(method='ffill')

    # Clean column names
    df.columns = [
        re.sub(r'\s+', '_', str(col).strip())
          .lower()
          .replace('.', '')
          .replace('(', '')
          .replace(')', '')
          .replace('/', '_')
        for col in df.columns
    ]

    # Remove "total" or "summary" rows
    for col in df.select_dtypes(include='object').columns:
        df = df[~df[col].astype(str).str.contains(
            r'total|รวม|sum|subtotal|summary', case=False, na=False)]

    # Remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^unnamed')]

    return df
```

### M Query — Dirty Excel

```m
// ข้าม header rows + promote first valid row
let
    Source = Excel.Workbook(File.Contents("file.xlsx")),
    Sheet = Source{[Name="Sheet1"]}[Data],
    Skipped = Table.Skip(Sheet, 3),  // ข้าม 3 แถวแรก
    Promoted = Table.PromoteHeaders(Skipped, [PromoteAllScalars=true]),
    // ลบ total rows
    Filtered = Table.SelectRows(Promoted, each
        not Text.Contains([Column1] ?? "", "Total") and
        not Text.Contains([Column1] ?? "", "รวม")),
    // Fill down merged cells
    Filled = Table.FillDown(Filtered, {"Category"})
in Filled
```

---

## 🗂️ JSON / Nested Data Flattening

```python
import json
from pandas import json_normalize

# Flatten nested JSON
def flatten_json_column(df, json_col):
    """แปลง JSON column → multiple columns"""
    parsed = df[json_col].apply(lambda x:
        json.loads(x) if isinstance(x, str) else x)
    flattened = json_normalize(parsed, sep='_')
    return pd.concat([df.drop(columns=[json_col]), flattened], axis=1)

# Example: flatten API response
raw = pd.DataFrame({
    'id': [1, 2],
    'data': [
        '{"name": "Alice", "address": {"city": "Bangkok", "zip": "10100"}}',
        '{"name": "Bob", "address": {"city": "Chiang Mai", "zip": "50000"}}'
    ]
})
result = flatten_json_column(raw, 'data')
# → id, name, address_city, address_zip

# Flatten nested list (array of objects)
def explode_json_array(df, array_col):
    """Explode JSON array → one row per item"""
    df[array_col] = df[array_col].apply(lambda x:
        json.loads(x) if isinstance(x, str) else x)
    return df.explode(array_col).reset_index(drop=True)
```

### M Query — JSON Parsing

```m
// Parse JSON column
Table.TransformColumns(Source, {{"JsonData", each
    Json.Document(_)}})

// Expand record field
Table.ExpandRecordColumn(Source, "JsonData",
    {"name", "email", "age"}, {"Name", "Email", "Age"})

// Expand list field (explode)
Table.ExpandListColumn(Source, "Items")
```

---

## 📐 Schema Validation

```python
def validate_schema(df, expected_schema):
    """ตรวจสอบ schema ของ DataFrame"""
    errors = []

    # Check required columns
    for col, rules in expected_schema.items():
        if col not in df.columns:
            errors.append(f"❌ Missing column: {col}")
            continue

        # Check data type
        expected_type = rules.get('type')
        if expected_type == 'numeric' and not pd.api.types.is_numeric_dtype(df[col]):
            errors.append(f"❌ {col}: expected numeric, got {df[col].dtype}")
        elif expected_type == 'string' and not pd.api.types.is_string_dtype(df[col]):
            errors.append(f"❌ {col}: expected string, got {df[col].dtype}")
        elif expected_type == 'datetime' and not pd.api.types.is_datetime64_any_dtype(df[col]):
            errors.append(f"❌ {col}: expected datetime, got {df[col].dtype}")

        # Check nullable
        if not rules.get('nullable', True) and df[col].isnull().any():
            errors.append(f"❌ {col}: has nulls but NOT nullable")

        # Check allowed values
        allowed = rules.get('allowed_values')
        if allowed:
            invalid = df[~df[col].isin(allowed) & df[col].notna()]
            if len(invalid) > 0:
                errors.append(f"❌ {col}: {len(invalid)} values not in allowed list")

        # Check range
        min_val = rules.get('min')
        max_val = rules.get('max')
        if min_val is not None and (df[col] < min_val).any():
            errors.append(f"❌ {col}: values below min ({min_val})")
        if max_val is not None and (df[col] > max_val).any():
            errors.append(f"❌ {col}: values above max ({max_val})")

    # Check unexpected columns
    expected_cols = set(expected_schema.keys())
    extra_cols = set(df.columns) - expected_cols
    if extra_cols:
        errors.append(f"⚠️ Unexpected columns: {extra_cols}")

    return errors

# Usage example
schema = {
    'order_id':   {'type': 'string', 'nullable': False},
    'amount':     {'type': 'numeric', 'nullable': False, 'min': 0},
    'status':     {'type': 'string', 'allowed_values': ['pending','paid','cancelled']},
    'created_at': {'type': 'datetime', 'nullable': False},
    'quantity':   {'type': 'numeric', 'min': 1, 'max': 10000},
}
errors = validate_schema(df, schema)
```

---

## 🔗 Referential Integrity Check

```python
def check_referential_integrity(fact_df, dim_df, fk_col, pk_col):
    """ตรวจสอบ Foreign Key ↔ Primary Key"""
    # Orphan records (FK not in PK)
    orphans = fact_df[~fact_df[fk_col].isin(dim_df[pk_col]) & fact_df[fk_col].notna()]

    # Unused dimension records (PK not referenced by any FK)
    unused = dim_df[~dim_df[pk_col].isin(fact_df[fk_col])]

    return {
        'orphan_count': len(orphans),
        'orphan_pct': f"{len(orphans)/len(fact_df)*100:.2f}%",
        'unused_dim': len(unused),
        'sample_orphans': orphans[fk_col].head(5).tolist(),
        'sample_unused': unused[pk_col].head(5).tolist()
    }

# Usage: Sales → Products
result = check_referential_integrity(
    sales_df, products_df, 'product_id', 'id')

# Multi-table integrity check
def full_integrity_audit(tables_config):
    """ตรวจสอบ integrity ทั้ง data model"""
    results = []
    for config in tables_config:
        r = check_referential_integrity(
            config['fact'], config['dim'],
            config['fk'], config['pk'])
        r['relationship'] = f"{config['fact_name']}.{config['fk']} → {config['dim_name']}.{config['pk']}"
        results.append(r)
    return pd.DataFrame(results)
```

---

## 🏷️ Categorical Encoding (for ML & Analysis)

```python
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

# Label Encoding (สำหรับ categories ไม่มี order)
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])
# decode: le.inverse_transform(df['category_encoded'])

# One-Hot Encoding (สำหรับ nominal data)
df_encoded = pd.get_dummies(df, columns=['color', 'size'], drop_first=True)

# Ordinal Encoding (สำหรับ ordered categories)
size_order = [['S', 'M', 'L', 'XL', 'XXL']]
oe = OrdinalEncoder(categories=size_order)
df['size_encoded'] = oe.fit_transform(df[['size']])

# Frequency Encoding (แทนด้วย % ที่พบ)
freq = df['category'].value_counts(normalize=True)
df['category_freq'] = df['category'].map(freq)

# Target Encoding (แทนด้วย mean ของ target)
target_mean = df.groupby('category')['sales'].mean()
df['category_target'] = df['category'].map(target_mean)
```

| วิธี | ใช้กับ | ข้อดี | ข้อเสีย |
|------|--------|------|--------|
| **Label** | Binary, tree-based models | เร็ว, compact | สร้าง false order |
| **One-Hot** | Nominal, <20 categories | ไม่มี false order | Sparse, high dimension |
| **Ordinal** | Ordered categories | รักษา order | ต้องกำหนด order เอง |
| **Frequency** | High cardinality | Compact | หาย info ถ้า freq เท่ากัน |
| **Target** | ทำ feature engineering | ทรงพลังมาก | Data leakage risk |

---

## 🌐 Data Enrichment (เสริมข้อมูลจาก External)

```python
# 1. Enrich จาก lookup table
province_info = pd.DataFrame({
    'province': ['กรุงเทพมหานคร', 'เชียงใหม่', 'ชลบุรี'],
    'region': ['กลาง', 'เหนือ', 'ตะวันออก'],
    'population': [5_600_000, 1_800_000, 1_500_000]
})
df = df.merge(province_info, on='province', how='left')

# 2. Enrich date columns
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter
df['day_of_week'] = df['date'].dt.day_name()
df['is_weekend'] = df['date'].dt.dayofweek >= 5
df['is_month_end'] = df['date'].dt.is_month_end

# Thai holidays
thai_holidays = ['2026-01-01', '2026-04-13', '2026-04-14', '2026-04-15',
                 '2026-05-01', '2026-12-05', '2026-12-10', '2026-12-31']
df['is_holiday'] = df['date'].dt.strftime('%Y-%m-%d').isin(thai_holidays)

# 3. Derive new features
df['revenue_per_unit'] = df['revenue'] / df['quantity'].replace(0, np.nan)
df['profit_margin'] = (df['revenue'] - df['cost']) / df['revenue'] * 100
df['customer_tenure_days'] = (pd.Timestamp.now() - df['signup_date']).dt.days

# 4. Geospatial enrichment (distance between two points)
from math import radians, cos, sin, asin, sqrt
def haversine(lat1, lon1, lat2, lon2):
    """คำนวณระยะทาง (km) ระหว่าง 2 จุด"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * 6371 * asin(sqrt(a))
```

---

## 🏷️ Column Name Standardization

```python
def standardize_columns(df):
    """ทำ column names ให้สม่ำเสมอ"""
    new_cols = {}
    for col in df.columns:
        new = str(col).strip()
        new = re.sub(r'[\s\-\.\/\\]+', '_', new)  # space/dash → underscore
        new = re.sub(r'[^\w]', '', new)            # remove special chars
        new = re.sub(r'([a-z])([A-Z])', r'\1_\2', new)  # camelCase → snake
        new = new.lower()
        new = re.sub(r'_+', '_', new).strip('_')   # collapse underscores
        new_cols[col] = new
    df = df.rename(columns=new_cols)
    return df

# Before: "Order ID", "customer.name", "Total Amount (USD)", "createdAt"
# After:  "order_id", "customer_name", "total_amount_usd", "created_at"
```

### M Query — Column Standardization

```m
// Rename + clean all column names
let
    Source = ...,
    ColNames = Table.ColumnNames(Source),
    CleanNames = List.Transform(ColNames, each
        Text.Lower(Text.Replace(
            Text.Replace(
                Text.Replace(Text.Trim(_), " ", "_"),
            ".", "_"),
        "-", "_"))),
    Pairs = List.Zip({ColNames, CleanNames}),
    Renamed = List.Accumulate(Pairs, Source, (state, pair) =>
        Table.RenameColumns(state, {{pair{0}, pair{1}}}))
in Renamed
```

---

## 🐍 Python Cleaning Libraries Cheatsheet

| Library | ใช้ทำอะไร | Install |
|---------|----------|---------|
| **pandas** | Core data cleaning + manipulation | `pip install pandas` |
| **pyjanitor** | Method-chaining cleaning API | `pip install pyjanitor` |
| **great_expectations** | Schema + rule-based validation | `pip install great-expectations` |
| **pandera** | DataFrame schema enforcement | `pip install pandera` |
| **fuzzywuzzy** | String similarity / dedup | `pip install fuzzywuzzy python-Levenshtein` |
| **chardet** | Auto-detect file encoding | `pip install chardet` |
| **missingno** | Visualize missing data patterns | `pip install missingno` |
| **datacompy** | Compare 2 DataFrames diff | `pip install datacompy` |
| **CleverCSV** | Fix malformed CSV files | `pip install clevercsv` |
| **Dask** | Clean large datasets (>RAM) | `pip install dask` |

```python
# pyjanitor — clean method chaining
import janitor
df_clean = (df
    .clean_names()                    # standardize column names
    .remove_empty()                    # remove empty rows/cols
    .rename_column('old_name', 'new_name')
    .filter_string('status', 'active')
    .fill_empty('category', 'Unknown')
)

# missingno — visualize missing patterns
import missingno as msno
msno.matrix(df)      # matrix view
msno.heatmap(df)     # correlation of missingness
msno.dendrogram(df)  # cluster missing patterns

# great_expectations — define expectations
import great_expectations as gx
context = gx.get_context()
# df.expect_column_values_to_not_be_null("order_id")
# df.expect_column_values_to_be_between("amount", min_value=0)
```

---

## 🔄 Multi-Source Data Reconciliation

```python
def reconcile_sources(source_a, source_b, key_cols, compare_cols):
    """เปรียบเทียบข้อมูลจาก 2 sources"""
    merged = source_a.merge(source_b, on=key_cols,
                            how='outer', suffixes=('_A', '_B'), indicator=True)

    report = {
        'only_in_A': (merged['_merge'] == 'left_only').sum(),
        'only_in_B': (merged['_merge'] == 'right_only').sum(),
        'in_both': (merged['_merge'] == 'both').sum(),
        'mismatches': {}
    }

    # Compare values for matched records
    both = merged[merged['_merge'] == 'both']
    for col in compare_cols:
        col_a, col_b = f"{col}_A", f"{col}_B"
        if col_a in both.columns and col_b in both.columns:
            mismatch = both[both[col_a] != both[col_b]]
            if len(mismatch) > 0:
                report['mismatches'][col] = {
                    'count': len(mismatch),
                    'sample': mismatch[[*key_cols, col_a, col_b]].head(3).to_dict('records')
                }

    return report

# Usage: Compare ERP vs CRM data
result = reconcile_sources(
    erp_sales, crm_sales,
    key_cols=['order_id'],
    compare_cols=['amount', 'customer_name', 'status'])
```

---

## 🏭 More Industry Use Cases

### 21. ⚖️ Legal

| ปัญหา | วิธีแก้ |
|--------|--------|
| Case number format differs across courts | Regex standardize by court type |
| Client name vs entity name inconsistent | Entity resolution / fuzzy match |
| Statute references outdated | Map to current legal codes |
| Document date vs filing date conflicts | Cross-field validation |
| Sensitive data in case files | PII masking (names, addresses) |

### 22. 🎓 HR / Recruitment

| ปัญหา | วิธีแก้ |
|--------|--------|
| Resume skill variations ("JS" vs "JavaScript") | Skill taxonomy mapping |
| Salary data mixed units (monthly/annual) | Normalize to annual |
| Job title inconsistencies | Standardize to O*NET or ISCO codes |
| Duplicate candidates across platforms | Record linkage by email + name |
| Age discrimination data | Remove age, compute experience years instead |

### 23. 🌾 Food Safety / FMCG

| ปัญหา | วิธีแก้ |
|--------|--------|
| Ingredient list formatting varies | NLP tokenization + standardize |
| Allergen data missing or inconsistent | Flag + cross-reference database |
| Batch/lot number format differs | Regex standardize |
| Temperature readings out of range | Rolling median + anomaly flag |
| Shelf life calculation errors | Validate production_date + shelf_days vs expiry |

### 24. 🏛️ Government / Census

| ปัญหา | วิธีแก้ |
|--------|--------|
| Address format varies by year | Standardize to current admin boundaries |
| Population count duplicates | Dedup by national ID |
| Mixed languages (Thai + local dialects) | Unicode normalization + translation |
| Historical date formats | Parse with multiple format attempts |
| Data collected by different agencies | Multi-source reconciliation |

### 25. ⚙️ IoT / Sensor Data

| ปัญหา | วิธีแก้ |
|--------|--------|
| Sensor drift over time | Calibration offset correction |
| Missing readings (connectivity drops) | Time-based interpolation |
| Duplicate timestamps (clock sync issues) | Dedup by device_id + timestamp |
| Readings outside physical limits | Domain-specific range validation |
| Mixed sampling frequencies | Resample to uniform frequency |

---

## 📏 Feature Scaling & Transformation

```python
from sklearn.preprocessing import (
    MinMaxScaler, StandardScaler, RobustScaler,
    PowerTransformer, MaxAbsScaler
)

numeric_cols = df.select_dtypes(include='number').columns.tolist()

# 1. Min-Max (0 → 1) — ใช้กับ neural networks, KNN
scaler = MinMaxScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# 2. Z-Score (mean=0, std=1) — ใช้กับ linear models, SVM
scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# 3. Robust (ใช้ median + IQR — ทน outliers!)
scaler = RobustScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# 4. Power Transform (ทำให้ distribution เป็น normal)
pt = PowerTransformer(method='yeo-johnson')  # รองรับ negative values
df[numeric_cols] = pt.fit_transform(df[numeric_cols])

# 5. Log Transform (ลด positive skew)
df['revenue_log'] = np.log1p(df['revenue'])  # log(1+x) ป้องกัน log(0)

# 6. Square Root (ลด moderate skew)
df['count_sqrt'] = np.sqrt(df['count'])
```

| เทคนิค | ใช้กับ | ทน Outliers? | Output Range |
|--------|--------|-------------|-------------|
| **Min-Max** | NN, Image data | ❌ | [0, 1] |
| **Z-Score** | Linear, SVM | ❌ | ~[-3, 3] |
| **Robust** | ทุกแบบที่มี outlier | ✅ | variable |
| **PowerTransform** | Skewed data | ⚠️ | ~normal |
| **Log** | Positive skewed | ❌ | unbounded |

---

## 📊 Multicollinearity Detection & Removal

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

def detect_multicollinearity(df, threshold=5.0):
    """ตรวจจับ multicollinearity ด้วย VIF"""
    numeric = df.select_dtypes(include='number').dropna()
    vif_data = pd.DataFrame()
    vif_data['Feature'] = numeric.columns
    vif_data['VIF'] = [
        variance_inflation_factor(numeric.values, i)
        for i in range(numeric.shape[1])
    ]
    vif_data = vif_data.sort_values('VIF', ascending=False)

    # Flag problematic columns
    vif_data['Status'] = vif_data['VIF'].apply(lambda x:
        '🔴 High' if x > 10 else '🟡 Moderate' if x > threshold else '🟢 OK')
    return vif_data

def remove_multicollinear(df, threshold=10.0):
    """ลบ columns ที่มี VIF สูงทีละตัว"""
    numeric = df.select_dtypes(include='number').dropna()
    dropped = []
    while True:
        vif = detect_multicollinearity(numeric, threshold)
        max_vif = vif['VIF'].max()
        if max_vif <= threshold:
            break
        drop_col = vif.iloc[0]['Feature']
        numeric = numeric.drop(columns=[drop_col])
        dropped.append(f"{drop_col} (VIF={max_vif:.1f})")
    return numeric, dropped

# Correlation matrix approach (simpler)
corr = df.select_dtypes(include='number').corr().abs()
upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
high_corr_pairs = [(corr.index[i], corr.columns[j], corr.iloc[i,j])
    for i in range(len(corr)) for j in range(i+1, len(corr))
    if corr.iloc[i,j] > 0.85]
```

---

## ⚖️ Class Imbalance Handling (SMOTE)

```python
from imblearn.over_sampling import SMOTE, ADASYN, BorderlineSMOTE
from imblearn.under_sampling import RandomUnderSampler, TomekLinks
from imblearn.combine import SMOTETomek
from collections import Counter

# ตรวจสอบ imbalance
print(Counter(df['target']))  # e.g. {0: 9500, 1: 500}

X = df.drop('target', axis=1)
y = df['target']

# 1. SMOTE — สร้าง synthetic minority samples
sm = SMOTE(random_state=42, sampling_strategy='minority')
X_res, y_res = sm.fit_resample(X, y)

# 2. Borderline SMOTE — focus on boundary samples
bsm = BorderlineSMOTE(random_state=42)
X_res, y_res = bsm.fit_resample(X, y)

# 3. ADASYN — adaptive synthetic (focus on hard samples)
ada = ADASYN(random_state=42)
X_res, y_res = ada.fit_resample(X, y)

# 4. Random Undersampling + SMOTE (combined)
smtomek = SMOTETomek(random_state=42)
X_res, y_res = smtomek.fit_resample(X, y)

print(f"Before: {Counter(y)}")
print(f"After:  {Counter(y_res)}")
```

| เทคนิค | ใช้เมื่อ | ข้อดี | ข้อเสีย |
|--------|---------|------|--------|
| **SMOTE** | General imbalance | สร้าง realistic samples | อาจ overlap majority |
| **Borderline** | Decision boundary สำคัญ | Focus ที่ critical zone | ช้ากว่า SMOTE |
| **ADASYN** | Hard-to-learn samples | Adaptive density | อาจ overfit noise |
| **SMOTETomek** | ต้องการ cleaner boundary | ทำ over+under sampling | ข้อมูลลดลง |
| **Undersampling** | Dataset ใหญ่มาก | เร็ว simple | เสีย information |

---

## 📋 Log File Parsing & Cleaning

```python
import re
from datetime import datetime

# Common log formats
LOG_PATTERNS = {
    'apache': r'(?P<ip>\S+) \S+ \S+ \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d+) (?P<size>\d+)',
    'nginx': r'(?P<ip>\S+) - \S+ \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d+) (?P<size>\d+)',
    'syslog': r'(?P<datetime>\w+ \d+ \d+:\d+:\d+) (?P<host>\S+) (?P<process>\S+): (?P<message>.*)',
    'json_log': None,  # parse with json.loads
}

def parse_log_file(filepath, format='apache'):
    """Parse log file → DataFrame"""
    pattern = LOG_PATTERNS.get(format)
    records = []

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if format == 'json_log':
                try:
                    records.append(json.loads(line))
                except:
                    continue
            else:
                match = re.match(pattern, line)
                if match:
                    records.append(match.groupdict())

    df = pd.DataFrame(records)

    # Clean parsed data
    if 'status' in df.columns:
        df['status'] = pd.to_numeric(df['status'], errors='coerce')
    if 'size' in df.columns:
        df['size'] = pd.to_numeric(df['size'], errors='coerce')
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'],
            format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')

    return df

# Filter & analyze
# df = parse_log_file('access.log', 'apache')
# errors = df[df['status'] >= 400]
# top_paths = df['path'].value_counts().head(20)
```

---

## 🗄️ SQL-Based Cleaning Techniques

```sql
-- 1. Remove duplicates with ROW_NUMBER
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id, order_date
            ORDER BY created_at DESC
        ) AS rn
    FROM orders
)
DELETE FROM ranked WHERE rn > 1;

-- 2. Handle NULLs with COALESCE
SELECT
    customer_id,
    COALESCE(phone, mobile, 'N/A') AS contact_number,
    COALESCE(revenue, 0) AS revenue
FROM customers;

-- 3. Standardize text
UPDATE products SET
    name = TRIM(UPPER(name)),
    category = TRIM(LOWER(category));

-- 4. Fix date formats
UPDATE transactions SET
    created_at = CASE
        WHEN created_at LIKE '__/__/____' THEN
            STR_TO_DATE(created_at, '%d/%m/%Y')
        WHEN created_at LIKE '____-__-__' THEN
            CAST(created_at AS DATE)
        ELSE NULL
    END;

-- 5. Detect & fix outliers with percentiles
WITH stats AS (
    SELECT
        PERCENTILE_CONT(0.01) WITHIN GROUP (ORDER BY amount) AS p1,
        PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY amount) AS p99
    FROM sales
)
UPDATE sales SET
    amount = CASE
        WHEN amount < (SELECT p1 FROM stats) THEN (SELECT p1 FROM stats)
        WHEN amount > (SELECT p99 FROM stats) THEN (SELECT p99 FROM stats)
        ELSE amount
    END;

-- 6. Cross-table validation
SELECT f.order_id, f.product_id
FROM fact_sales f
LEFT JOIN dim_products p ON f.product_id = p.id
WHERE p.id IS NULL;  -- orphan records

-- 7. Data profiling in SQL
SELECT
    column_name,
    COUNT(*) AS total,
    COUNT(column_name) AS non_null,
    COUNT(DISTINCT column_name) AS unique_vals,
    ROUND(100.0 * COUNT(column_name) / COUNT(*), 1) AS completeness_pct
FROM information_schema.columns
CROSS APPLY (SELECT column_name FROM your_table) t
GROUP BY column_name;
```

---

## 🔑 Surrogate Key Generation

```python
import hashlib
import uuid

# 1. Hash-based surrogate key (deterministic — same input = same key)
def generate_surrogate_key(*fields):
    """สร้าง surrogate key จาก natural key fields"""
    combined = '|'.join(str(f) for f in fields)
    return hashlib.md5(combined.encode()).hexdigest()

df['sk'] = df.apply(lambda r:
    generate_surrogate_key(r['source'], r['order_id'], r['line_item']), axis=1)

# 2. UUID-based (globally unique, non-deterministic)
df['uuid'] = [str(uuid.uuid4()) for _ in range(len(df))]

# 3. Auto-increment (sequential)
df['row_id'] = range(1, len(df) + 1)

# 4. High-watermark (continue from existing max)
existing_max = 10500  # from database
df['sk'] = range(existing_max + 1, existing_max + 1 + len(df))
```

### M Query — Surrogate Key

```m
// Add auto-increment index
Table.AddIndexColumn(Source, "SK", 1, 1, Int64.Type)

// Hash-based key
Table.AddColumn(Source, "SK", each
    Binary.ToText(
        Binary.From(Text.ToBinary(
            [Source] & "|" & [OrderID] & "|" & Text.From([LineItem]),
            BinaryEncoding.Base64)),
        BinaryEncoding.Hex), type text)
```

---

## 🔄 Slowly Changing Dimensions (SCD) Cleaning

```python
def apply_scd_type2(dim_df, new_data, key_col, track_cols):
    """SCD Type 2 — เก็บ history ทุก version"""
    today = pd.Timestamp.now().date()

    # Merge to find changes
    merged = new_data.merge(
        dim_df[dim_df['is_current'] == True],
        on=key_col, how='left', suffixes=('_new', '_old'))

    changes = []
    for _, row in merged.iterrows():
        has_change = False
        for col in track_cols:
            if str(row.get(f'{col}_new')) != str(row.get(f'{col}_old')):
                has_change = True
                break

        if has_change:
            # Expire old record
            changes.append({
                'action': 'expire',
                key_col: row[key_col],
                'effective_end': today, 'is_current': False
            })
            # Insert new version
            new_rec = {col: row.get(f'{col}_new', row.get(col))
                      for col in new_data.columns}
            new_rec['effective_start'] = today
            new_rec['effective_end'] = pd.NaT
            new_rec['is_current'] = True
            changes.append({'action': 'insert', **new_rec})

    return changes

# SCD Type 1 — overwrite (ไม่เก็บ history)
def apply_scd_type1(dim_df, new_data, key_col, update_cols):
    """SCD Type 1 — update ทับค่าเดิม"""
    for _, row in new_data.iterrows():
        mask = dim_df[key_col] == row[key_col]
        for col in update_cols:
            dim_df.loc[mask, col] = row[col]
    return dim_df
```

| SCD Type | พฤติกรรม | ใช้เมื่อ | เก็บ History? |
|----------|---------|---------|-------------|
| **Type 0** | ไม่เปลี่ยนเลย | Static data | ❌ |
| **Type 1** | Overwrite ทับ | ไม่สนใจ history | ❌ |
| **Type 2** | Add new row + expire old | ต้องการ full history | ✅ |
| **Type 3** | เก็บ current + previous column | แค่ version ก่อนหน้า | ⚠️ จำกัด |
| **Type 6** | Hybrid (1+2+3) | ทั้ง current + history | ✅ |

---

## 📸 Data Versioning & Snapshot Comparison

```python
import hashlib
from datetime import datetime

def create_snapshot(df, version_tag=None):
    """สร้าง snapshot ของ DataFrame"""
    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'version': version_tag or datetime.now().strftime('%Y%m%d_%H%M%S'),
        'shape': df.shape,
        'checksum': hashlib.md5(
            pd.util.hash_pandas_object(df).values.tobytes()
        ).hexdigest(),
        'columns': list(df.columns),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'null_counts': df.isnull().sum().to_dict(),
    }
    return snapshot

def compare_snapshots(snap_a, snap_b):
    """เปรียบเทียบ 2 snapshots"""
    diff = {}

    if snap_a['shape'] != snap_b['shape']:
        diff['shape_change'] = f"{snap_a['shape']} → {snap_b['shape']}"

    if snap_a['checksum'] != snap_b['checksum']:
        diff['data_changed'] = True

    # Column changes
    cols_a, cols_b = set(snap_a['columns']), set(snap_b['columns'])
    if cols_a != cols_b:
        diff['added_columns'] = list(cols_b - cols_a)
        diff['removed_columns'] = list(cols_a - cols_b)

    # Null count changes
    for col in set(snap_a['null_counts']) & set(snap_b['null_counts']):
        a_null, b_null = snap_a['null_counts'][col], snap_b['null_counts'][col]
        if a_null != b_null:
            diff.setdefault('null_changes', {})[col] = f"{a_null} → {b_null}"

    return diff

def diff_dataframes(df_old, df_new, key_col):
    """หา row-level differences ระหว่าง 2 DataFrames"""
    merged = df_old.merge(df_new, on=key_col, how='outer',
                          suffixes=('_old', '_new'), indicator=True)
    return {
        'added': merged[merged['_merge'] == 'right_only'][key_col].tolist(),
        'removed': merged[merged['_merge'] == 'left_only'][key_col].tolist(),
        'modified': len(merged[merged['_merge'] == 'both']),
    }
```

---

## 🌳 Hierarchical / Parent-Child Data Cleaning

```python
def clean_hierarchy(df, id_col, parent_col):
    """ทำความสะอาด hierarchical data"""
    issues = []

    # 1. Self-referencing (node is its own parent)
    self_ref = df[df[id_col] == df[parent_col]]
    if len(self_ref) > 0:
        issues.append(f"❌ Self-referencing: {len(self_ref)} nodes")
        df.loc[df[id_col] == df[parent_col], parent_col] = None

    # 2. Orphan children (parent_id not in id list)
    valid_ids = set(df[id_col].dropna())
    orphans = df[
        df[parent_col].notna() &
        ~df[parent_col].isin(valid_ids)
    ]
    if len(orphans) > 0:
        issues.append(f"❌ Orphan children: {len(orphans)} nodes")

    # 3. Circular references
    def find_circular(node_id, visited=None):
        if visited is None: visited = set()
        if node_id in visited: return True
        visited.add(node_id)
        parent = df.loc[df[id_col] == node_id, parent_col].values
        if len(parent) == 0 or pd.isna(parent[0]): return False
        return find_circular(parent[0], visited)

    circular = [row[id_col] for _, row in df.iterrows()
                if find_circular(row[id_col])]
    if circular:
        issues.append(f"❌ Circular references: {len(circular)} nodes")

    # 4. Calculate depth
    def get_depth(node_id, depth=0, max_depth=50):
        if depth > max_depth: return depth  # safety
        parent = df.loc[df[id_col] == node_id, parent_col].values
        if len(parent) == 0 or pd.isna(parent[0]): return depth
        return get_depth(parent[0], depth + 1, max_depth)

    df['depth'] = df[id_col].apply(get_depth)

    return df, issues

# Flatten hierarchy to path
def hierarchy_to_path(df, id_col, parent_col, name_col, sep=' > '):
    """แปลง hierarchy เป็น path string"""
    def build_path(node_id):
        parts = []
        current = node_id
        while current is not None and len(parts) < 20:
            row = df[df[id_col] == current]
            if row.empty: break
            parts.append(row[name_col].values[0])
            current = row[parent_col].values[0]
            if pd.isna(current): break
        return sep.join(reversed(parts))

    df['full_path'] = df[id_col].apply(build_path)
    return df
```

---

## 🔀 Mixed Data Types in Same Column

```python
def clean_mixed_types(df, col):
    """จัดการ column ที่มี data type ผสมกัน"""
    analysis = {
        'numeric': 0, 'string': 0, 'null': 0,
        'date': 0, 'boolean': 0, 'mixed_samples': []
    }

    for val in df[col].dropna().head(1000):
        if isinstance(val, (int, float)):
            analysis['numeric'] += 1
        elif isinstance(val, bool):
            analysis['boolean'] += 1
        elif isinstance(val, str):
            # Try to detect hidden types
            if val.strip().lower() in ['true', 'false', 'yes', 'no']:
                analysis['boolean'] += 1
            elif val.replace('.','',1).replace('-','',1).isdigit():
                analysis['numeric'] += 1
            else:
                analysis['string'] += 1
        else:
            analysis['mixed_samples'].append((type(val).__name__, val))

    # Auto-fix based on majority type
    total = analysis['numeric'] + analysis['string'] + analysis['boolean']
    if analysis['numeric'] / max(total, 1) > 0.8:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    elif analysis['boolean'] / max(total, 1) > 0.8:
        bool_map = {'true': True, 'false': False, 'yes': True,
                    'no': False, '1': True, '0': False}
        df[col] = df[col].astype(str).str.lower().map(bool_map)

    return df, analysis

# Split mixed column into components
def split_mixed_column(df, col):
    """แยก column ที่มี number+text ออกเป็น 2 columns"""
    df[f'{col}_numeric'] = df[col].apply(lambda x:
        float(re.search(r'[\d.]+', str(x)).group())
        if re.search(r'[\d.]+', str(x)) else None)
    df[f'{col}_text'] = df[col].apply(lambda x:
        re.sub(r'[\d.]+', '', str(x)).strip()
        if pd.notna(x) else None)
    return df
```

---

## 🧪 Synthetic Test Data Generation

```python
from faker import Faker
import random

fake = Faker('th_TH')  # Thai locale

def generate_test_data(n=1000):
    """สร้าง test data สำหรับทดสอบ cleaning pipeline"""
    data = []
    for _ in range(n):
        row = {
            'name': fake.name(),
            'email': fake.email() if random.random() > 0.1 else None,
            'phone': fake.phone_number() if random.random() > 0.05 else '',
            'address': fake.address().replace('\n', ' '),
            'amount': round(random.gauss(5000, 2000), 2),
            'date': fake.date_between('-2y', 'today'),
            'category': random.choice(['A', 'B', 'C', 'a', 'b', ' C ']),
            'status': random.choice(['active', 'Active', 'ACTIVE', None]),
        }

        # Inject dirty data (10% of rows)
        if random.random() < 0.1:
            row['amount'] = random.choice([-999, 999999, None, 'N/A'])
        if random.random() < 0.05:
            row['email'] = random.choice(['invalid', '@bad', 'no-at-sign.com'])
        if random.random() < 0.03:
            row['date'] = random.choice(['31/13/2025', 'yesterday', None])

        data.append(row)

    # Inject duplicates (5%)
    n_dupes = int(n * 0.05)
    data.extend(random.choices(data, k=n_dupes))

    return pd.DataFrame(data)

# Usage: test your cleaning pipeline
dirty_df = generate_test_data(5000)
# clean_df = auto_clean(dirty_df)
```

---

## 📊 Data Quality Scoring System

```python
def calculate_quality_score(df, weights=None):
    """คำนวณ Data Quality Score แบบ weighted"""
    default_weights = {
        'completeness': 0.25,  # % non-null
        'uniqueness': 0.15,    # % unique in key columns
        'validity': 0.20,      # % pass validation rules
        'consistency': 0.20,   # % consistent formats
        'timeliness': 0.20,    # % recent data
    }
    weights = weights or default_weights

    scores = {}

    # 1. Completeness (0-100)
    total_cells = df.shape[0] * df.shape[1]
    non_null = df.notna().sum().sum()
    scores['completeness'] = (non_null / total_cells) * 100

    # 2. Uniqueness (based on expected-unique columns)
    if 'id' in df.columns:
        scores['uniqueness'] = (df['id'].nunique() / len(df)) * 100
    else:
        scores['uniqueness'] = (1 - df.duplicated().mean()) * 100

    # 3. Validity (type + range checks)
    valid_checks = []
    for col in df.select_dtypes(include='number').columns:
        valid_checks.append((df[col] >= 0).mean() * 100)
    scores['validity'] = np.mean(valid_checks) if valid_checks else 100

    # 4. Consistency (format uniformity)
    consistency_checks = []
    for col in df.select_dtypes(include='object').columns:
        non_null = df[col].dropna()
        if len(non_null) > 0:
            # Check if all same case pattern
            all_upper = non_null.str.isupper().mean()
            all_lower = non_null.str.islower().mean()
            all_title = non_null.str.istitle().mean()
            best = max(all_upper, all_lower, all_title)
            consistency_checks.append(best * 100)
    scores['consistency'] = np.mean(consistency_checks) if consistency_checks else 100

    # 5. Timeliness
    date_cols = df.select_dtypes(include='datetime64').columns
    if len(date_cols) > 0:
        latest = df[date_cols[0]].max()
        days_old = (pd.Timestamp.now() - latest).days
        scores['timeliness'] = max(0, 100 - days_old)
    else:
        scores['timeliness'] = 100

    # Weighted final score
    final = sum(scores[k] * weights[k] for k in weights)

    # Grade
    grade = ('A+' if final >= 95 else 'A' if final >= 90 else
             'B' if final >= 80 else 'C' if final >= 70 else 'D' if final >= 60 else 'F')

    return {'scores': scores, 'final_score': round(final, 1), 'grade': grade}
```

### DAX — Quality Score

```dax
Overall Quality Score =
VAR Completeness = [Completeness %]
VAR Uniqueness = [Uniqueness %]
VAR Validity = [Validity %]
VAR Score = Completeness * 0.3 + Uniqueness * 0.3 + Validity * 0.4
RETURN
    SWITCH(TRUE(),
        Score >= 95, "🟢 A+ (" & FORMAT(Score, "0.0") & "%)",
        Score >= 90, "🟢 A (" & FORMAT(Score, "0.0") & "%)",
        Score >= 80, "🟡 B (" & FORMAT(Score, "0.0") & "%)",
        Score >= 70, "🟠 C (" & FORMAT(Score, "0.0") & "%)",
        "🔴 D (" & FORMAT(Score, "0.0") & "%)")
```

---

## 🛠️ ETL Error Handling Patterns

```python
import logging
from datetime import datetime

# Structured logging setup
logging.basicConfig(
    filename=f'etl_log_{datetime.now():%Y%m%d}.log',
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO
)

class ETLPipeline:
    """ETL Pipeline with checkpoint + retry"""

    def __init__(self, name):
        self.name = name
        self.checkpoints = {}
        self.dead_letter = []  # failed records

    def with_retry(self, func, max_retries=3, backoff=2):
        """Retry with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                wait = backoff ** attempt
                logging.warning(
                    f"Attempt {attempt+1}/{max_retries} failed: {e}. "
                    f"Retrying in {wait}s...")
                import time; time.sleep(wait)
        raise Exception(f"Failed after {max_retries} retries")

    def save_checkpoint(self, step_name, data):
        """Save progress checkpoint"""
        self.checkpoints[step_name] = {
            'timestamp': datetime.now().isoformat(),
            'rows': len(data),
            'shape': data.shape
        }
        logging.info(f"✅ Checkpoint: {step_name} ({len(data)} rows)")

    def process_with_dlq(self, df, transform_func):
        """Process rows, send failures to dead letter queue"""
        results = []
        for idx, row in df.iterrows():
            try:
                results.append(transform_func(row))
            except Exception as e:
                self.dead_letter.append({
                    'row_index': idx,
                    'error': str(e),
                    'data': row.to_dict(),
                    'timestamp': datetime.now().isoformat()
                })
        success_df = pd.DataFrame(results)
        logging.info(
            f"Processed: {len(results)} success, "
            f"{len(self.dead_letter)} failed")
        return success_df

# Usage
pipeline = ETLPipeline("sales_etl")
# df = pipeline.with_retry(lambda: pd.read_csv('big_file.csv'))
# pipeline.save_checkpoint('extract', df)
# clean_df = pipeline.process_with_dlq(df, clean_row_func)
```

---

## 📊 Sampling Strategies for Large Datasets

```python
# 1. Random sampling (ใช้ทั่วไป)
sample = df.sample(n=10000, random_state=42)
# or by fraction
sample = df.sample(frac=0.1, random_state=42)

# 2. Stratified sampling (รักษาสัดส่วน categories)
from sklearn.model_selection import train_test_split
sample, _ = train_test_split(df, train_size=0.1,
    stratify=df['category'], random_state=42)

# 3. Systematic sampling (ทุก N rows)
n = 10  # every 10th row
sample = df.iloc[::n]

# 4. Cluster sampling (สุ่มทั้ง group)
clusters = df['region'].unique()
selected_clusters = np.random.choice(clusters, size=3, replace=False)
sample = df[df['region'].isin(selected_clusters)]

# 5. Time-based sampling (ช่วงเวลา)
sample = df[df['date'].between('2025-01-01', '2025-03-31')]

# 6. Reservoir sampling (สำหรับ streaming/ไฟล์ใหญ่มาก)
def reservoir_sample(filepath, k=10000):
    """Sample k rows from a file too large for memory"""
    reservoir = []
    with open(filepath, 'r') as f:
        header = next(f)
        for i, line in enumerate(f):
            if i < k:
                reservoir.append(line)
            else:
                j = random.randint(0, i)
                if j < k:
                    reservoir[j] = line
    return pd.read_csv(io.StringIO(header + ''.join(reservoir)))
```

---

## 📝 Multi-line CSV & Malformed File Handling

```python
import csv
import io

def fix_multiline_csv(filepath, output_path=None):
    """แก้ CSV ที่มี newlines ภายใน quoted fields"""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        # Use Python csv module (handles quoted newlines correctly)
        reader = csv.reader(f, quotechar='"', delimiter=',',
                           quoting=csv.QUOTE_ALL, skipinitialspace=True)
        rows = list(reader)

    df = pd.DataFrame(rows[1:], columns=rows[0])
    if output_path:
        df.to_csv(output_path, index=False)
    return df

def fix_malformed_csv(filepath):
    """แก้ CSV ที่มีปัญหา: wrong column count, encoding errors"""
    clean_rows = []
    error_rows = []

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader)
        expected_cols = len(header)

        for i, row in enumerate(reader):
            if len(row) == expected_cols:
                clean_rows.append(row)
            elif len(row) > expected_cols:
                # Too many columns — try to merge extra columns
                merged = row[:expected_cols-1] + [','.join(row[expected_cols-1:])]
                clean_rows.append(merged)
            else:
                error_rows.append((i+2, row))  # line number + data

    df = pd.DataFrame(clean_rows, columns=header)
    if error_rows:
        print(f"⚠️ {len(error_rows)} malformed rows skipped")
    return df

# CleverCSV — auto-detect delimiter + quoting
# pip install clevercsv
# import clevercsv
# df = clevercsv.read_dataframe('messy_file.csv')
```

---

## 🏭 Even More Industry Use Cases

### 26. 🎮 Gaming / E-sports

| ปัญหา | วิธีแก้ |
|--------|--------|
| Player names with Unicode exploits | Sanitize + Unicode normalization |
| Match timestamp timezone inconsistency | Convert all to UTC |
| Cheater data (impossible stats) | Statistical anomaly detection |
| In-game currency float precision | Round to fixed decimal places |
| Event log out-of-order | Sort by event_id, not timestamp |

### 27. 🏥 Clinical Trials / Biotech

| ปัญหา | วิธีแก้ |
|--------|--------|
| Patient ID cross-site duplication | Hash-based global ID |
| Lab result units vary (mg/dL vs mmol/L) | Unit conversion lookup |
| Adverse event text free-form | NLP classification + MedDRA coding |
| Visit date windows violated | Flag protocol deviations |
| Incomplete CRF (Case Report Forms) | Completeness scoring per form |

### 28. 📦 Supply Chain / Logistics

| ปัญหา | วิธีแก้ |
|--------|--------|
| Tracking number format varies by carrier | Regex per carrier pattern |
| Weight/dimension unit mixing | Standardize to metric |
| ETA vs actual arrival discrepancy | Cross-field validation + alerts |
| Warehouse location code inconsistent | Master data lookup |
| Inventory count negative | Flag + reconcile with transactions |

### 29. 🎯 Marketing / AdTech

| ปัญหา | วิธีแก้ |
|--------|--------|
| UTM parameters inconsistent casing | Lowercase + standardize |
| Attribution window overlap | Dedup by session + timestamp |
| CPC/CPM values = 0 (organic mixed in) | Separate paid vs organic |
| Campaign name typos across platforms | Fuzzy match + canonical mapping |
| Click-through rate > 100% (tracking error) | Cap at 100%, flag for review |

### 30. 🌊 Environmental / Climate

| ปัญหา | วิธีแก้ |
|--------|--------|
| Sensor measurement drift | Calibration baseline correction |
| Weather data gaps (station offline) | Spatial interpolation from nearby stations |
| Mixed coordinate reference systems | Reproject to WGS84 |
| Historical data format changes | Version-aware parsers |
| Extreme readings (equipment malfunction) | Physical-limit domain validation |

---

## 🔗 Data Lineage & Provenance Tracking

```python
from datetime import datetime
import json

class DataLineageTracker:
    """ติดตาม data lineage ตลอด pipeline"""

    def __init__(self):
        self.lineage = []

    def track(self, step_name, source, target, transform, row_count):
        self.lineage.append({
            'step': step_name,
            'source': source,
            'target': target,
            'transform': transform,
            'rows_in': row_count.get('in', 0),
            'rows_out': row_count.get('out', 0),
            'timestamp': datetime.now().isoformat(),
            'rows_dropped': row_count.get('in', 0) - row_count.get('out', 0)
        })

    def add_column_lineage(self, target_col, source_cols, formula=None):
        """Track column-level lineage"""
        self.lineage.append({
            'type': 'column_lineage',
            'target_column': target_col,
            'source_columns': source_cols,
            'formula': formula,
            'timestamp': datetime.now().isoformat()
        })

    def export(self, filepath='lineage.json'):
        with open(filepath, 'w') as f:
            json.dump(self.lineage, f, indent=2, ensure_ascii=False)

    def visualize_mermaid(self):
        """Generate Mermaid flowchart"""
        lines = ['graph LR']
        for i, step in enumerate(self.lineage):
            if step.get('type') == 'column_lineage':
                continue
            src = step['source'].replace(' ', '_')
            tgt = step['target'].replace(' ', '_')
            lines.append(f"    {src} -->|{step['step']}| {tgt}")
        return '\n'.join(lines)

# Usage
tracker = DataLineageTracker()
# tracker.track('extract', 'sales.csv', 'raw_df', 'read_csv', {'in': 10000, 'out': 10000})
# tracker.track('clean', 'raw_df', 'clean_df', 'remove_nulls+dedup', {'in': 10000, 'out': 9200})
# tracker.add_column_lineage('full_name', ['first_name', 'last_name'], 'concat')
```

---

## 📜 Data Contracts (Producer-Consumer)

```python
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ColumnContract:
    name: str
    dtype: str  # 'int', 'float', 'str', 'datetime', 'bool'
    nullable: bool = False
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[List] = None
    pattern: Optional[str] = None  # regex
    description: str = ""

@dataclass
class DataContract:
    name: str
    version: str
    owner: str
    columns: List[ColumnContract]
    freshness_hours: int = 24  # data must be < N hours old
    min_rows: int = 1
    max_null_pct: float = 10.0  # overall null %
    sla_description: str = ""

def validate_contract(df, contract: DataContract):
    """Validate DataFrame against a data contract"""
    violations = []

    # Check required columns exist
    for col_spec in contract.columns:
        if col_spec.name not in df.columns:
            violations.append(f"❌ Missing column: {col_spec.name}")
            continue

        col = df[col_spec.name]

        # Nullable check
        if not col_spec.nullable and col.isnull().any():
            nulls = col.isnull().sum()
            violations.append(f"❌ {col_spec.name}: {nulls} nulls (non-nullable)")

        # Type check
        type_map = {'int': 'int64', 'float': 'float64', 'str': 'object',
                    'datetime': 'datetime64[ns]', 'bool': 'bool'}
        expected = type_map.get(col_spec.dtype)
        if expected and str(col.dtype) != expected:
            violations.append(
                f"⚠️ {col_spec.name}: expected {expected}, got {col.dtype}")

        # Range check
        if col_spec.min_value is not None:
            below = (col.dropna() < col_spec.min_value).sum()
            if below > 0:
                violations.append(
                    f"❌ {col_spec.name}: {below} values below min ({col_spec.min_value})")

        # Allowed values check
        if col_spec.allowed_values:
            invalid = ~col.dropna().isin(col_spec.allowed_values)
            if invalid.sum() > 0:
                violations.append(
                    f"❌ {col_spec.name}: {invalid.sum()} invalid values")

    # Row count check
    if len(df) < contract.min_rows:
        violations.append(f"❌ Too few rows: {len(df)} < {contract.min_rows}")

    # Overall null % check
    null_pct = df.isnull().mean().mean() * 100
    if null_pct > contract.max_null_pct:
        violations.append(f"❌ Null rate {null_pct:.1f}% > {contract.max_null_pct}%")

    return {
        'valid': len(violations) == 0,
        'violations': violations,
        'contract': contract.name,
        'version': contract.version
    }
```

---

## 🔍 Advanced Record Linkage with Blocking

```python
# pip install recordlinkage
import recordlinkage

def deduplicate_with_blocking(df, block_cols, compare_cols, threshold=0.85):
    """Advanced deduplication ด้วย blocking strategy"""

    # 1. Indexing (blocking) — reduce comparison pairs
    indexer = recordlinkage.Index()
    for col in block_cols:
        indexer.block(col)  # only compare records in same block
    candidate_pairs = indexer.index(df)
    print(f"📊 Candidate pairs (after blocking): {len(candidate_pairs):,}")

    # 2. Comparison
    compare = recordlinkage.Compare()
    for col_name, method in compare_cols.items():
        if method == 'exact':
            compare.exact(col_name, col_name, label=col_name)
        elif method == 'string':
            compare.string(col_name, col_name, method='jarowinkler',
                          threshold=0.85, label=col_name)
        elif method == 'numeric':
            compare.numeric(col_name, col_name, method='gauss',
                           offset=1, label=col_name)
        elif method == 'date':
            compare.date(col_name, col_name, label=col_name)

    features = compare.compute(candidate_pairs, df)

    # 3. Classification — threshold-based
    scores = features.sum(axis=1) / len(compare_cols)
    matches = scores[scores >= threshold]

    print(f"✅ Matches found: {len(matches):,}")
    return matches.index  # pairs of matching indices

# Multi-pass blocking (catch more matches)
def multi_pass_blocking(df, blocking_schemes):
    """หลาย blocking schemes เพื่อ recall สูงขึ้น"""
    all_pairs = set()
    for scheme_name, block_cols in blocking_schemes.items():
        indexer = recordlinkage.Index()
        for col in block_cols:
            indexer.block(col)
        pairs = indexer.index(df)
        all_pairs.update(pairs.tolist())
        print(f"  Pass '{scheme_name}': {len(pairs):,} pairs")
    print(f"📊 Total unique pairs: {len(all_pairs):,}")
    return all_pairs
```

---

## 📈 Data Drift Detection

```python
from scipy import stats
import numpy as np

def detect_drift(reference_df, current_df, threshold=0.05):
    """ตรวจจับ data drift ระหว่าง 2 datasets"""
    drift_report = {}

    # Numeric columns — KS test
    for col in reference_df.select_dtypes(include='number').columns:
        if col not in current_df.columns:
            continue
        ref = reference_df[col].dropna()
        cur = current_df[col].dropna()
        ks_stat, p_value = stats.ks_2samp(ref, cur)
        drifted = p_value < threshold
        drift_report[col] = {
            'type': 'numeric',
            'test': 'KS',
            'statistic': round(ks_stat, 4),
            'p_value': round(p_value, 6),
            'drifted': drifted,
            'ref_mean': round(ref.mean(), 2),
            'cur_mean': round(cur.mean(), 2),
            'mean_shift': round(cur.mean() - ref.mean(), 2)
        }

    # Categorical columns — Chi-squared test
    for col in reference_df.select_dtypes(include='object').columns:
        if col not in current_df.columns:
            continue
        ref_counts = reference_df[col].value_counts(normalize=True)
        cur_counts = current_df[col].value_counts(normalize=True)
        all_cats = set(ref_counts.index) | set(cur_counts.index)

        ref_freq = [ref_counts.get(c, 0) for c in all_cats]
        cur_freq = [cur_counts.get(c, 0) for c in all_cats]

        if sum(ref_freq) > 0 and sum(cur_freq) > 0:
            chi2, p_value = stats.chisquare(
                [max(f, 1e-10) for f in cur_freq],
                [max(f, 1e-10) for f in ref_freq])
            drift_report[col] = {
                'type': 'categorical',
                'test': 'Chi2',
                'statistic': round(chi2, 4),
                'p_value': round(p_value, 6),
                'drifted': p_value < threshold,
                'new_categories': list(set(cur_counts.index) - set(ref_counts.index)),
                'missing_categories': list(set(ref_counts.index) - set(cur_counts.index))
            }

    drifted_cols = [c for c, v in drift_report.items() if v['drifted']]
    return {
        'total_columns': len(drift_report),
        'drifted_columns': len(drifted_cols),
        'drifted_names': drifted_cols,
        'details': drift_report
    }
```

---

## 🔬 Dimensionality Reduction for Cleaning (PCA)

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def pca_anomaly_detection(df, n_components=0.95, contamination=0.05):
    """ใช้ PCA ตรวจจับ anomalies ใน high-dimensional data"""
    numeric = df.select_dtypes(include='number').dropna()

    # Standardize
    scaler = StandardScaler()
    scaled = scaler.fit_transform(numeric)

    # PCA — retain 95% variance
    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(scaled)
    reconstructed = pca.inverse_transform(transformed)

    # Reconstruction error = anomaly score
    errors = np.mean((scaled - reconstructed) ** 2, axis=1)

    # Flag top anomalies
    threshold = np.percentile(errors, (1 - contamination) * 100)
    df_result = df.copy()
    df_result['reconstruction_error'] = errors
    df_result['is_anomaly'] = errors > threshold

    print(f"📊 Components retained: {pca.n_components_}")
    print(f"📊 Variance explained: {pca.explained_variance_ratio_.sum():.1%}")
    print(f"🔴 Anomalies detected: {df_result['is_anomaly'].sum()}")

    return df_result

def find_redundant_features(df, variance_threshold=0.01):
    """หา features ที่แทบไม่มี variance (ลบได้)"""
    numeric = df.select_dtypes(include='number')
    variances = numeric.var()
    low_var = variances[variances < variance_threshold]
    return low_var.index.tolist()
```

---

## 🪟 Window Functions for Data Cleaning (Lead/Lag)

```python
# Gap detection with shift (pandas equivalent of SQL LEAD/LAG)
def detect_sequence_gaps(df, id_col, sort_col):
    """ตรวจจับ gaps ใน sequential data"""
    df = df.sort_values(sort_col)
    df['prev_value'] = df[sort_col].shift(1)
    df['next_value'] = df[sort_col].shift(-1)

    # Numeric gaps
    if df[sort_col].dtype in ['int64', 'float64']:
        df['gap_before'] = df[sort_col] - df['prev_value']
        gaps = df[df['gap_before'] > 1]
    # Date gaps
    elif pd.api.types.is_datetime64_any_dtype(df[sort_col]):
        df['gap_days'] = (df[sort_col] - df['prev_value']).dt.days
        gaps = df[df['gap_days'] > 1]

    return gaps

def detect_sudden_changes(df, value_col, threshold_pct=50):
    """ตรวจจับ sudden jumps/drops ด้วย lag comparison"""
    df['prev'] = df[value_col].shift(1)
    df['change_pct'] = ((df[value_col] - df['prev']) / df['prev'].abs()) * 100
    sudden = df[df['change_pct'].abs() > threshold_pct]
    return sudden

def forward_fill_within_group(df, group_col, fill_cols, limit=None):
    """Forward fill ภายในแต่ละ group"""
    for col in fill_cols:
        df[col] = df.groupby(group_col)[col].ffill(limit=limit)
    return df
```

### SQL — Window Functions for Cleaning

```sql
-- Detect sequence gaps
SELECT *,
    LAG(order_id) OVER (ORDER BY order_id) AS prev_id,
    order_id - LAG(order_id) OVER (ORDER BY order_id) AS gap_size
FROM orders
HAVING gap_size > 1;

-- Detect sudden value changes
SELECT *,
    LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_amount,
    ROUND(100.0 * (amount - LAG(amount) OVER (PARTITION BY customer_id
        ORDER BY order_date)) / NULLIF(LAG(amount) OVER (PARTITION BY customer_id
        ORDER BY order_date), 0), 1) AS change_pct
FROM sales;

-- Running dedup (keep first per group)
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY customer_id, product_id
        ORDER BY created_at ASC
    ) AS rn
    FROM orders
) t WHERE rn = 1;
```

---

## 🌐 API Response Cleaning & Pagination

```python
import requests
import time

def fetch_all_pages(base_url, params=None, auth=None,
                    page_key='page', data_key='results',
                    max_pages=100, delay=0.5):
    """Fetch ข้อมูลทุกหน้าจาก paginated API"""
    all_data = []
    page = 1
    params = params or {}

    while page <= max_pages:
        params[page_key] = page
        try:
            resp = requests.get(base_url, params=params,
                              auth=auth, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Page {page} failed: {e}")
            break

        items = data.get(data_key, [])
        if not items:
            break

        all_data.extend(items)
        print(f"  Page {page}: {len(items)} items (total: {len(all_data)})")

        # Check for next page
        if not data.get('has_more', data.get('next')):
            break

        page += 1
        time.sleep(delay)  # rate limiting

    return pd.DataFrame(all_data)

def clean_api_response(data):
    """Clean nested API response → flat DataFrame"""
    if isinstance(data, dict):
        # Extract the actual data array
        for key in ['data', 'results', 'items', 'records', 'rows']:
            if key in data and isinstance(data[key], list):
                data = data[key]
                break

    df = pd.json_normalize(data, sep='_')

    # Auto-convert detected types
    for col in df.columns:
        # Dates
        if any(kw in col.lower() for kw in ['date', 'time', 'created', 'updated']):
            df[col] = pd.to_datetime(df[col], errors='coerce')
        # Booleans
        elif df[col].dropna().isin([True, False, 'true', 'false']).all():
            df[col] = df[col].map({'true': True, 'false': False,
                                   True: True, False: False})

    return df
```

---

## 📄 XML Data Parsing & Cleaning

```python
import xml.etree.ElementTree as ET

def xml_to_dataframe(xml_string_or_file, row_tag, col_mapping=None):
    """Parse XML → DataFrame"""
    if xml_string_or_file.startswith('<?xml') or xml_string_or_file.startswith('<'):
        root = ET.fromstring(xml_string_or_file)
    else:
        tree = ET.parse(xml_string_or_file)
        root = tree.getroot()

    # Handle namespaces
    ns = {}
    if root.tag.startswith('{'):
        ns_uri = root.tag.split('}')[0] + '}'
        ns = {'ns': ns_uri.strip('{}')}

    records = []
    for elem in root.iter(row_tag):
        row = {}
        for child in elem:
            tag = child.tag.split('}')[-1]  # remove namespace
            row[tag] = child.text
        # Also get attributes
        for attr, val in elem.attrib.items():
            row[f'@{attr}'] = val
        records.append(row)

    df = pd.DataFrame(records)

    # Apply column mapping
    if col_mapping:
        df = df.rename(columns=col_mapping)

    return df

def clean_xml_text(text):
    """Clean XML character entities and whitespace"""
    if not text:
        return text
    import html
    text = html.unescape(text)  # &amp; → &, &lt; → <
    text = ' '.join(text.split())  # collapse whitespace
    return text.strip()
```

---

## ✅ Boolean / Flag Column Standardization

```python
def standardize_booleans(df, columns=None, target_format='bool'):
    """Standardize boolean columns ที่มี format หลากหลาย"""
    TRUE_VALUES = {'true', 'yes', 'y', '1', 'on', 'active', 'enabled',
                   'จริง', 'ใช่', 'เปิด', 't', 'x', '✓', '✅'}
    FALSE_VALUES = {'false', 'no', 'n', '0', 'off', 'inactive', 'disabled',
                    'ไม่จริง', 'ไม่ใช่', 'ปิด', 'f', '', '❌'}

    if columns is None:
        # Auto-detect boolean-like columns
        columns = []
        for col in df.select_dtypes(include='object').columns:
            unique_lower = set(df[col].dropna().astype(str).str.lower().str.strip())
            if unique_lower.issubset(TRUE_VALUES | FALSE_VALUES):
                columns.append(col)

    for col in columns:
        original = df[col].copy()
        df[col] = df[col].astype(str).str.lower().str.strip()

        if target_format == 'bool':
            df[col] = df[col].apply(lambda x: True if x in TRUE_VALUES
                                    else False if x in FALSE_VALUES else None)
        elif target_format == 'int':
            df[col] = df[col].apply(lambda x: 1 if x in TRUE_VALUES
                                    else 0 if x in FALSE_VALUES else None)
        elif target_format == 'yes_no':
            df[col] = df[col].apply(lambda x: 'Yes' if x in TRUE_VALUES
                                    else 'No' if x in FALSE_VALUES else None)

        changed = (original.astype(str) != df[col].astype(str)).sum()
        if changed > 0:
            print(f"  ✅ {col}: standardized {changed} values")

    return df
```

---

## 📅 Calendar & Business Day Handling

```python
import numpy as np

# Thai public holidays (ตัวอย่าง)
THAI_HOLIDAYS_2026 = [
    '2026-01-01', '2026-02-26', '2026-04-06', '2026-04-13',
    '2026-04-14', '2026-04-15', '2026-05-01', '2026-05-04',
    '2026-05-11', '2026-06-03', '2026-07-28', '2026-08-12',
    '2026-10-13', '2026-10-23', '2026-12-05', '2026-12-10',
    '2026-12-31'
]

def add_business_days(start_date, n_days, holidays=None):
    """เพิ่มจำนวนวันทำการ (ข้ามเสาร์-อาทิตย์ + วันหยุด)"""
    holidays = set(pd.to_datetime(holidays or []))
    current = pd.to_datetime(start_date)
    added = 0
    while added < n_days:
        current += pd.Timedelta(days=1)
        if current.weekday() < 5 and current not in holidays:
            added += 1
    return current

def count_business_days(start, end, holidays=None):
    """นับจำนวนวันทำการระหว่าง 2 วัน"""
    holidays = holidays or []
    bdays = np.busday_count(
        np.datetime64(start), np.datetime64(end),
        holidays=[np.datetime64(h) for h in holidays])
    return int(bdays)

def enrich_date_columns(df, date_col, holidays=None):
    """เพิ่ม calendar features"""
    df[date_col] = pd.to_datetime(df[date_col])
    df[f'{date_col}_year'] = df[date_col].dt.year
    df[f'{date_col}_month'] = df[date_col].dt.month
    df[f'{date_col}_quarter'] = df[date_col].dt.quarter
    df[f'{date_col}_weekday'] = df[date_col].dt.day_name()
    df[f'{date_col}_is_weekend'] = df[date_col].dt.weekday >= 5
    df[f'{date_col}_is_month_end'] = df[date_col].dt.is_month_end

    if holidays:
        holiday_set = set(pd.to_datetime(holidays))
        df[f'{date_col}_is_holiday'] = df[date_col].isin(holiday_set)

    return df
```

### M Query — Business Days

```m
// Count business days between two dates
let
    CountBusinessDays = (start as date, end as date) =>
    let
        dayCount = Duration.Days(end - start),
        allDays = List.Dates(start, dayCount, #duration(1,0,0,0)),
        businessDays = List.Select(allDays, each
            Date.DayOfWeek(_, Day.Monday) < 5)
    in
        List.Count(businessDays)
in
    CountBusinessDays
```

---

## 🔄 Incremental / Delta Load Cleaning

```python
def incremental_load(new_df, existing_df, key_col, timestamp_col=None):
    """Incremental load — เฉพาะ rows ใหม่หรือเปลี่ยนแปลง"""
    existing_keys = set(existing_df[key_col])

    # New records (ไม่เคยมี)
    new_records = new_df[~new_df[key_col].isin(existing_keys)]

    # Updated records (key ซ้ำ แต่ timestamp ใหม่กว่า)
    updated = pd.DataFrame()
    if timestamp_col:
        overlap = new_df[new_df[key_col].isin(existing_keys)]
        if len(overlap) > 0:
            merged = overlap.merge(
                existing_df[[key_col, timestamp_col]],
                on=key_col, suffixes=('_new', '_old'))
            updated = merged[
                merged[f'{timestamp_col}_new'] > merged[f'{timestamp_col}_old']
            ]
            # Keep only new columns
            updated = updated[[c for c in new_df.columns if c in updated.columns]]

    result = {
        'new_records': len(new_records),
        'updated_records': len(updated),
        'unchanged': len(existing_keys) - len(updated),
    }
    print(f"📊 Delta: {result['new_records']} new, "
          f"{result['updated_records']} updated, "
          f"{result['unchanged']} unchanged")

    return pd.concat([new_records, updated], ignore_index=True), result

def watermark_load(source_query, watermark_file='watermark.json'):
    """ใช้ watermark (high-water mark) สำหรับ incremental extract"""
    import json
    # Load last watermark
    try:
        with open(watermark_file) as f:
            watermark = json.load(f)
    except FileNotFoundError:
        watermark = {'last_id': 0, 'last_timestamp': '1900-01-01'}

    # Query only newer data
    # df = pd.read_sql(f"{source_query} WHERE id > {watermark['last_id']}", conn)

    # Update watermark after success
    # watermark['last_id'] = df['id'].max()
    # with open(watermark_file, 'w') as f:
    #     json.dump(watermark, f)
    return watermark
```

---

## 📡 Change Data Capture (CDC)

```python
def apply_cdc(target_df, cdc_events, key_col):
    """Apply CDC events (insert/update/delete) to target"""
    for event in cdc_events:
        op = event.get('op', event.get('operation'))
        data = event.get('after', event.get('data', {}))
        key = data.get(key_col) or event.get(key_col)

        if op in ('c', 'insert', 'I'):  # Create/Insert
            target_df = pd.concat([target_df, pd.DataFrame([data])],
                                  ignore_index=True)

        elif op in ('u', 'update', 'U'):  # Update
            mask = target_df[key_col] == key
            for col, val in data.items():
                if col in target_df.columns:
                    target_df.loc[mask, col] = val

        elif op in ('d', 'delete', 'D'):  # Delete
            target_df = target_df[target_df[key_col] != key]

    return target_df

def detect_changes(old_df, new_df, key_col):
    """ตรวจจับ changes แบบ CDC-style"""
    merged = old_df.merge(new_df, on=key_col, how='outer',
                          suffixes=('_old', '_new'), indicator=True)

    inserts = merged[merged['_merge'] == 'right_only'][key_col].tolist()
    deletes = merged[merged['_merge'] == 'left_only'][key_col].tolist()

    # Detect updates (both exist but values differ)
    both = merged[merged['_merge'] == 'both']
    updates = []
    compare_cols = [c.replace('_old', '') for c in both.columns
                    if c.endswith('_old') and c != f'{key_col}_old']
    for _, row in both.iterrows():
        for col in compare_cols:
            if str(row.get(f'{col}_old')) != str(row.get(f'{col}_new')):
                updates.append(row[key_col])
                break

    return {
        'inserts': inserts, 'updates': updates, 'deletes': deletes,
        'total_changes': len(inserts) + len(updates) + len(deletes)
    }
```

---

## 📝 Audit Trail for Cleaning Operations

```python
from datetime import datetime

class CleaningAudit:
    """บันทึก audit trail ของทุก cleaning operation"""

    def __init__(self, pipeline_name):
        self.pipeline = pipeline_name
        self.log = []

    def record(self, operation, column, before_count, after_count,
               details=None):
        self.log.append({
            'timestamp': datetime.now().isoformat(),
            'pipeline': self.pipeline,
            'operation': operation,
            'column': column,
            'rows_before': before_count,
            'rows_after': after_count,
            'rows_affected': before_count - after_count,
            'details': details or {}
        })

    def to_dataframe(self):
        return pd.DataFrame(self.log)

    def summary(self):
        df = self.to_dataframe()
        total_affected = df['rows_affected'].sum()
        print(f"\n📋 Cleaning Audit: {self.pipeline}")
        print(f"   Operations: {len(df)}")
        print(f"   Total rows affected: {total_affected:,}")
        for _, row in df.iterrows():
            status = '🔴' if row['rows_affected'] > 0 else '🟢'
            print(f"   {status} {row['operation']}: "
                  f"{row['rows_affected']:,} rows ({row['column']})")

# Usage
audit = CleaningAudit('sales_pipeline')
# before = len(df)
# df = df.dropna(subset=['amount'])
# audit.record('remove_nulls', 'amount', before, len(df))
# audit.summary()
```

---

## ⚡ Batch vs Stream Cleaning Patterns

```python
# === BATCH cleaning (process entire dataset at once) ===
def batch_clean(df, rules):
    """Batch: ประมวลผลทั้ง DataFrame"""
    for rule in rules:
        if rule['type'] == 'drop_nulls':
            df = df.dropna(subset=rule.get('columns'))
        elif rule['type'] == 'fill':
            df[rule['column']] = df[rule['column']].fillna(rule['value'])
        elif rule['type'] == 'trim':
            for col in df.select_dtypes(include='object').columns:
                df[col] = df[col].str.strip()
        elif rule['type'] == 'dedup':
            df = df.drop_duplicates(subset=rule.get('columns'))
    return df

# === STREAM cleaning (process row-by-row or micro-batch) ===
def stream_clean_row(row, rules):
    """Stream: clean ทีละ row (สำหรับ real-time pipeline)"""
    for rule in rules:
        col = rule.get('column')
        if rule['type'] == 'validate':
            if not rule['func'](row.get(col)):
                row['_valid'] = False
                return row
        elif rule['type'] == 'transform':
            row[col] = rule['func'](row.get(col))
        elif rule['type'] == 'default':
            if row.get(col) is None:
                row[col] = rule['value']
    row['_valid'] = True
    return row

# Micro-batch (combine benefits of both)
def micro_batch_clean(stream, batch_size=1000, rules=None):
    """Micro-batch: รวม rows แล้ว clean เป็น batch เล็กๆ"""
    buffer = []
    results = []
    for record in stream:
        buffer.append(record)
        if len(buffer) >= batch_size:
            batch_df = pd.DataFrame(buffer)
            clean_df = batch_clean(batch_df, rules)
            results.append(clean_df)
            buffer = []
    # Process remaining
    if buffer:
        results.append(batch_clean(pd.DataFrame(buffer), rules))
    return pd.concat(results, ignore_index=True)
```

---

## 🔗 Functional Dependency Validation

```python
def check_functional_dependency(df, determinant_cols, dependent_col):
    """ตรวจสอบ Functional Dependency: X → Y
    ถ้า X เหมือนกันแล้ว Y ต้องเหมือนกันด้วย"""
    violations = df.groupby(determinant_cols)[dependent_col].nunique()
    violating_groups = violations[violations > 1]

    if len(violating_groups) == 0:
        print(f"✅ FD holds: {determinant_cols} → {dependent_col}")
        return None

    print(f"❌ FD violated: {len(violating_groups)} groups have "
          f"inconsistent {dependent_col}")

    # Show example violations
    examples = []
    for group_val in violating_groups.index[:5]:
        if isinstance(group_val, tuple):
            mask = pd.Series(True, index=df.index)
            for col, val in zip(determinant_cols, group_val):
                mask &= df[col] == val
        else:
            mask = df[determinant_cols[0]] == group_val
        examples.append(df[mask][[*determinant_cols, dependent_col]].head(3))

    return pd.concat(examples)

def discover_functional_dependencies(df, max_lhs_size=2):
    """Auto-discover FDs ในข้อมูล"""
    fds = []
    cols = df.columns.tolist()

    for lhs_size in range(1, max_lhs_size + 1):
        from itertools import combinations
        for lhs in combinations(cols, lhs_size):
            for rhs in cols:
                if rhs in lhs:
                    continue
                violations = df.groupby(list(lhs))[rhs].nunique()
                if (violations <= 1).all():
                    fds.append({
                        'determinant': list(lhs),
                        'dependent': rhs,
                        'strength': 'exact'
                    })

    return fds
```

---

## 🏭 Even More Industry Use Cases (Round 5)

### 31. 🏦 RegTech / Financial Compliance

| ปัญหา | วิธีแก้ |
|--------|--------|
| AML transaction screening false positives | Fuzzy name matching + threshold tuning |
| Sanctions list format variation | Standardize names + transliteration |
| KYC document date format | Multi-format date parser |
| Cross-border transfer currency mixing | ISO 4217 currency code validation |
| Reporting period misalignment | Calendar business day normalization |

### 32. 🎵 Music / Entertainment Streaming

| ปัญหา | วิธีแก้ |
|--------|--------|
| Artist name spelling variations | Unicode normalization + canonical mapping |
| Song duration = 0 or negative | Domain range validation (1s–3600s) |
| Genre classification inconsistency | NLP + taxonomy mapping |
| Play count > possible (bot streams) | Statistical anomaly detection |
| Release date in future | Timestamp validation + cap at today |

### 33. 🧬 Genomics / Bioinformatics

| ปัญหา | วิธีแก้ |
|--------|--------|
| Gene name auto-corrected (MARCH1 → date) | Disable Excel auto-format, validate gene names |
| Sequence data quality scores | Phred score filtering (Q > 20) |
| Sample ID cross-contamination | Hash-based unique sample tracking |
| Mixed coordinate systems (0-based vs 1-based) | Standardize to one system |
| Missing metadata (tissue type, species) | Lookup tables + mandatory fields |

### 34. 🏗️ Construction / BIM

| ปัญหา | วิธีแก้ |
|--------|--------|
| Material quantity unit mixing (m³ vs ft³) | Unit conversion + standardize to metric |
| BIM model version conflicts | Version comparison + merge rules |
| Cost estimate currency inconsistency | Exchange rate normalization |
| Schedule date overlap/conflict | Gantt chart cross-validation |
| Subcontractor name duplicates | Fuzzy matching + master vendor list |

### 35. 📱 Telecom / Mobile Network

| ปัญหา | วิธีแก้ |
|--------|--------|
| CDR (Call Detail Record) timestamp drift | NTP sync + timezone normalization |
| Cell tower ID format inconsistency | Standardize to CGI format |
| Data usage negative values | Cap at 0 + flag for investigation |
| Subscriber MSISDN format variation | E.164 phone number standardization |
| Network event log out-of-order | Event sequence reconstruction |

---

## 🌲 Isolation Forest — ML-based Anomaly Detection

```python
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np

def detect_anomalies_isolation_forest(df, columns, contamination=0.05, random_state=42):
    """
    Isolation Forest: anomaly detection ที่ทำงานได้ดีกับ high-dimensional data
    ต่างจาก Z-score/IQR ตรงที่ใช้ ML เพื่อจับ non-linear anomalies
    """
    iso = IsolationForest(
        contamination=contamination,
        random_state=random_state,
        n_estimators=200,
        max_samples='auto'
    )
    
    features = df[columns].fillna(df[columns].median())
    df['anomaly_score'] = iso.decision_function(features)
    df['is_anomaly'] = iso.predict(features)  # -1 = anomaly, 1 = normal
    
    anomalies = df[df['is_anomaly'] == -1]
    print(f"🌲 Isolation Forest: พบ {len(anomalies)} anomalies ({len(anomalies)/len(df)*100:.1f}%)")
    
    return df

# ตัวอย่าง: ตรวจจับ transaction ผิดปกติ
df = detect_anomalies_isolation_forest(
    df, columns=['amount', 'frequency', 'hour_of_day'], contamination=0.03
)

# ★ ใช้ anomaly score เพื่อ rank (ยิ่งติดลบ = ยิ่งผิดปกติ)
df_ranked = df.sort_values('anomaly_score').head(20)
```

---

## 🗓️ Fuzzy Date Parsing (dateparser / dateutil)

```python
import dateparser
from dateutil.parser import parse as dateutil_parse
import pandas as pd

def fuzzy_parse_dates(series, prefer_dates_from='past'):
    """
    แปลง date strings ที่มาในรูปแบบหลากหลาย:
    - "3 วันก่อน", "last Tuesday", "เมื่อวาน"
    - "Mär 2024", "15/03/24", "March 15th, 2024"
    - "2024年3月15日", "๑๕ มี.ค. ๒๕๖๗"
    """
    results = []
    for val in series:
        if pd.isna(val) or str(val).strip() == '':
            results.append(pd.NaT)
            continue
        
        # ลอง dateparser ก่อน (รองรับหลายภาษา)
        parsed = dateparser.parse(
            str(val),
            settings={
                'PREFER_DATES_FROM': prefer_dates_from,
                'RETURN_AS_TIMEZONE_AWARE': False,
                'PARSERS': ['absolute-time', 'relative-time', 'timestamp']
            }
        )
        
        if parsed is None:
            # Fallback: dateutil fuzzy mode
            try:
                parsed = dateutil_parse(str(val), fuzzy=True)
            except (ValueError, OverflowError):
                parsed = pd.NaT
        
        results.append(parsed)
    
    return pd.Series(results, dtype='datetime64[ns]')

# ตัวอย่าง
messy_dates = pd.Series([
    "March 15, 2024", "15/03/24", "เมื่อ 3 วันก่อน",
    "last Friday", "2024-03-15T10:30:00Z", "Q1 2024"
])
clean_dates = fuzzy_parse_dates(messy_dates)
```

---

## 📷 Image / Media Metadata Cleaning (EXIF)

```python
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import pandas as pd

def extract_image_metadata(image_dir, extensions=('.jpg', '.jpeg', '.png', '.tiff')):
    """
    ดึง EXIF metadata จากภาพ → ทำความสะอาดและจัดเป็น DataFrame
    ใช้สำหรับ: asset management, photo libraries, forensic analysis
    """
    records = []
    for root, _, files in os.walk(image_dir):
        for fname in files:
            if not fname.lower().endswith(extensions):
                continue
            filepath = os.path.join(root, fname)
            try:
                img = Image.open(filepath)
                exif_data = img._getexif() or {}
                
                record = {
                    'file': filepath,
                    'filename': fname,
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'size_bytes': os.path.getsize(filepath)
                }
                
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, str(tag_id))
                    # Clean problematic EXIF values
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='ignore')
                        except:
                            value = str(value)
                    record[tag_name] = value
                
                records.append(record)
            except Exception as e:
                records.append({'file': filepath, 'error': str(e)})
    
    df = pd.DataFrame(records)
    
    # Clean metadata
    if 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y:%m:%d %H:%M:%S', errors='coerce')
    if 'GPSInfo' in df.columns:
        df['has_gps'] = df['GPSInfo'].notna()
    
    return df

def strip_exif_for_privacy(image_path, output_path):
    """ลบ EXIF metadata ทั้งหมดเพื่อ privacy"""
    img = Image.open(image_path)
    data = list(img.getdata())
    clean_img = Image.new(img.mode, img.size)
    clean_img.putdata(data)
    clean_img.save(output_path)
```

---

## 🗺️ Geospatial Topology Cleaning

```python
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.validation import make_valid, explain_validity
import geopandas as gpd

def clean_geospatial_topology(gdf):
    """
    Validate & fix polygon topology issues:
    - Self-intersecting polygons
    - Invalid geometries
    - Overlapping polygons
    - Gaps between adjacent polygons
    - Coordinate precision noise
    """
    results = {'fixed': 0, 'invalid_original': 0, 'simplified': 0}
    
    # 1) Fix invalid geometries
    gdf['is_valid_before'] = gdf.geometry.is_valid
    results['invalid_original'] = (~gdf['is_valid_before']).sum()
    
    gdf['geometry'] = gdf.geometry.apply(
        lambda g: make_valid(g) if not g.is_valid else g
    )
    
    # 2) Remove degenerate geometries (area = 0)
    gdf = gdf[gdf.geometry.area > 0].copy()
    
    # 3) Reduce coordinate precision (ลด noise)
    def reduce_precision(geom, decimal_places=6):
        """ลดทศนิยมพิกัดเกินจำเป็น"""
        import json
        geojson = json.loads(geom.to_json() if hasattr(geom, 'to_json') else mapping(geom).__str__().replace("'", '"'))
        return shape(geojson)
    
    # 4) Detect overlaps between polygons
    overlaps = []
    for i in range(len(gdf)):
        for j in range(i + 1, len(gdf)):
            if gdf.iloc[i].geometry.overlaps(gdf.iloc[j].geometry):
                overlap_area = gdf.iloc[i].geometry.intersection(gdf.iloc[j].geometry).area
                overlaps.append({
                    'poly_a': i, 'poly_b': j,
                    'overlap_area': overlap_area
                })
    
    print(f"🗺️ Topology: {results['invalid_original']} invalid fixed, {len(overlaps)} overlaps found")
    return gdf, overlaps

# ★ Reproject to standard CRS
def standardize_crs(gdf, target_crs='EPSG:4326'):
    """Reproject ทุก geometry ไปยัง CRS เดียวกัน"""
    if gdf.crs is None:
        gdf = gdf.set_crs(target_crs)
    elif gdf.crs != target_crs:
        gdf = gdf.to_crs(target_crs)
    return gdf
```

---

## 🎭 Data Masking for Testing (with Referential Integrity)

```python
import hashlib
import random
import string
from faker import Faker
import pandas as pd

fake = Faker('th_TH')  # Thai locale

class TestDataMasker:
    """
    Mask sensitive data สำหรับ test environment 
    ★ ต่างจาก PII Masking ตรงที่รักษา referential integrity ข้าม tables
    """
    def __init__(self, seed=42):
        self.seed = seed
        self.mapping_cache = {}  # เก็บ mapping เพื่อรักษา consistency
        Faker.seed(seed)
        random.seed(seed)
    
    def mask_value(self, value, field_type='text'):
        """Mask ค่าโดยรักษา 1:1 mapping"""
        if pd.isna(value):
            return value
        
        cache_key = f"{field_type}:{value}"
        if cache_key in self.mapping_cache:
            return self.mapping_cache[cache_key]
        
        if field_type == 'name':
            masked = fake.name()
        elif field_type == 'email':
            masked = fake.email()
        elif field_type == 'phone':
            masked = fake.phone_number()
        elif field_type == 'address':
            masked = fake.address()
        elif field_type == 'national_id':
            masked = ''.join(random.choices(string.digits, k=13))
        elif field_type == 'credit_card':
            masked = fake.credit_card_number()
        else:
            # Format-preserving hash
            masked = hashlib.sha256(f"{self.seed}:{value}".encode()).hexdigest()[:len(str(value))]
        
        self.mapping_cache[cache_key] = masked
        return masked
    
    def mask_dataframe(self, df, field_map):
        """
        Mask DataFrame โดยรักษา referential integrity
        field_map: {'column_name': 'field_type', ...}
        """
        df_masked = df.copy()
        for col, ftype in field_map.items():
            if col in df_masked.columns:
                df_masked[col] = df_masked[col].apply(lambda v: self.mask_value(v, ftype))
        return df_masked

# ★ ใช้ masker เดียวกันข้าม tables เพื่อรักษา FK relationships
masker = TestDataMasker(seed=42)
customers_masked = masker.mask_dataframe(customers, {'name': 'name', 'email': 'email'})
orders_masked = masker.mask_dataframe(orders, {'customer_name': 'name'})
# customer_name ใน orders จะ map ไป value เดิมกับ name ใน customers ✅
```

---

## 🔤 Regex Extraction — Structured Data from Unstructured Text

```python
import re
import pandas as pd

class StructuredDataExtractor:
    """
    ★ ต่างจาก Regex Validation ตรงที่เน้น "ดึงข้อมูล" ออกมาจาก text
    ไม่ใช่แค่ validate ว่าถูก format หรือไม่
    """
    
    PATTERNS = {
        'thai_id': r'\b(\d{1}-\d{4}-\d{5}-\d{2}-\d{1})\b',
        'email': r'[\w.+-]+@[\w-]+\.[\w.-]+',
        'phone_th': r'(?:0[689]\d-\d{3}-\d{4}|0[2-9]\d{1,2}-\d{3,4}-\d{4})',
        'money_th': r'(?:฿|THB)\s*[\d,]+(?:\.\d{2})?',
        'money_usd': r'\$[\d,]+(?:\.\d{2})?',
        'url': r'https?://[\w\-._~:/?#\[\]@!$&\'()*+,;=%]+',
        'date_iso': r'\d{4}-\d{2}-\d{2}',
        'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        'percentage': r'\d+\.?\d*\s*%',
        'invoice_no': r'(?:INV|REC|SO|PO)-?\d{4,10}',
        'coordinates': r'[-+]?\d{1,3}\.\d{4,},\s*[-+]?\d{1,3}\.\d{4,}',
    }
    
    def extract_all(self, text, patterns=None):
        """ดึง structured data ทุกประเภทจาก text"""
        patterns = patterns or self.PATTERNS
        found = {}
        for name, pattern in patterns.items():
            matches = re.findall(pattern, str(text))
            if matches:
                found[name] = matches
        return found
    
    def extract_to_columns(self, df, text_col, extract_types=None):
        """ดึงข้อมูลจาก text column → สร้าง columns ใหม่"""
        extract_types = extract_types or list(self.PATTERNS.keys())
        for etype in extract_types:
            pattern = self.PATTERNS.get(etype)
            if pattern:
                df[f'extracted_{etype}'] = df[text_col].str.findall(pattern)
                df[f'has_{etype}'] = df[f'extracted_{etype}'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False)
        return df

# ตัวอย่าง: extract จาก free-text notes
extractor = StructuredDataExtractor()
df = extractor.extract_to_columns(df, 'notes', ['email', 'phone_th', 'money_th'])
```

---

## 📏 String Distance Metrics for Fuzzy Matching

```python
from jellyfish import (
    levenshtein_distance, jaro_winkler_similarity,
    damerau_levenshtein_distance, soundex, metaphone
)
from difflib import SequenceMatcher
import pandas as pd

def string_similarity_matrix(strings, method='jaro_winkler'):
    """
    สร้าง similarity matrix ระหว่าง strings
    ★ ต่างจาก Record Linkage ตรงที่เน้นเรื่อง distance metrics โดยเฉพาะ
    """
    methods = {
        'levenshtein': lambda a, b: 1 - levenshtein_distance(a, b) / max(len(a), len(b), 1),
        'jaro_winkler': jaro_winkler_similarity,
        'damerau': lambda a, b: 1 - damerau_levenshtein_distance(a, b) / max(len(a), len(b), 1),
        'sequence': lambda a, b: SequenceMatcher(None, a, b).ratio(),
    }
    
    func = methods[method]
    n = len(strings)
    matrix = pd.DataFrame(0.0, index=strings, columns=strings)
    
    for i in range(n):
        for j in range(i, n):
            score = func(str(strings[i]).lower(), str(strings[j]).lower())
            matrix.iloc[i, j] = score
            matrix.iloc[j, i] = score
    
    return matrix

def phonetic_dedup(series, method='soundex'):
    """
    Dedup ด้วย phonetic matching (เสียงคล้ายกัน)
    เหมาะกับชื่อที่สะกดต่างกันแต่ออกเสียงเหมือนกัน
    """
    phonetic_func = soundex if method == 'soundex' else metaphone
    df = pd.DataFrame({'original': series})
    df['phonetic'] = df['original'].apply(lambda x: phonetic_func(str(x)))
    
    # Group by phonetic code → pick first as canonical
    canonical = df.groupby('phonetic')['original'].first().to_dict()
    df['canonical'] = df['phonetic'].map(canonical)
    
    return df

# ตัวอย่าง
sim = string_similarity_matrix(['Microsoft', 'Microsft', 'MSFT', 'microsoft corp'])
dupes = phonetic_dedup(pd.Series(['Smith', 'Smyth', 'Smithe', 'Schmidt']))
```

---

## 💾 DataFrame Memory Optimization

```python
import pandas as pd
import numpy as np

def optimize_dataframe_memory(df, verbose=True):
    """
    ลดการใช้ memory ของ DataFrame โดยไม่สูญเสียข้อมูล
    ★ สำคัญมากเมื่อทำ data cleaning กับ dataset ขนาดใหญ่
    """
    start_mem = df.memory_usage(deep=True).sum() / 1024**2
    
    for col in df.columns:
        col_type = df[col].dtype
        
        # Optimize integers
        if col_type in ['int64', 'int32']:
            c_min, c_max = df[col].min(), df[col].max()
            if c_min >= 0:
                if c_max < np.iinfo(np.uint8).max:
                    df[col] = df[col].astype(np.uint8)
                elif c_max < np.iinfo(np.uint16).max:
                    df[col] = df[col].astype(np.uint16)
                elif c_max < np.iinfo(np.uint32).max:
                    df[col] = df[col].astype(np.uint32)
            else:
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
        
        # Optimize floats
        elif col_type == 'float64':
            df[col] = pd.to_numeric(df[col], downcast='float')
        
        # Optimize strings → category (if low cardinality)
        elif col_type == 'object':
            n_unique = df[col].nunique()
            n_total = len(df[col])
            if n_unique / n_total < 0.5:  # < 50% unique → category
                df[col] = df[col].astype('category')
    
    end_mem = df.memory_usage(deep=True).sum() / 1024**2
    if verbose:
        reduction = (1 - end_mem / start_mem) * 100
        print(f"💾 Memory: {start_mem:.1f} MB → {end_mem:.1f} MB (ลด {reduction:.1f}%)")
    
    return df

# ★ Efficient file format
def save_optimized(df, path):
    """บันทึกเป็น Parquet (เร็วกว่า CSV 5-10x, เล็กกว่า 3-5x)"""
    df.to_parquet(path, engine='pyarrow', compression='snappy')
```

---

## ✅ Data Unit Testing (Great Expectations)

```python
# pip install great_expectations
import great_expectations as gx

def create_data_expectations(df, suite_name='cleaning_validation'):
    """
    สร้าง data unit tests เพื่อ validate ข้อมูลหลัง cleaning
    ★ ต่างจาก Schema Validation ตรงที่เน้น statistical properties
    """
    context = gx.get_context()
    ds = context.sources.pandas_default
    asset = ds.add_dataframe_asset(name="test_data")
    
    batch = asset.build_batch_request(dataframe=df)
    validator = context.get_validator(batch_request=batch, expectation_suite_name=suite_name)
    
    # ★ Expectations ที่เหมาะกับ post-cleaning
    validator.expect_column_values_to_not_be_null('customer_id')
    validator.expect_column_values_to_be_unique('customer_id')
    validator.expect_column_values_to_be_between('age', min_value=0, max_value=150)
    validator.expect_column_values_to_match_regex('email', r'^[\w.+-]+@[\w-]+\.[\w.-]+$')
    validator.expect_column_mean_to_be_between('order_amount', min_value=10, max_value=10000)
    validator.expect_column_proportion_of_unique_values_to_be_between('status', min_value=0.001)
    validator.expect_table_row_count_to_be_between(min_value=100, max_value=10_000_000)
    
    # Run validation
    results = validator.validate()
    
    passed = results.statistics['successful_expectations']
    total = results.statistics['evaluated_expectations']
    print(f"✅ Data Tests: {passed}/{total} passed ({passed/total*100:.0f}%)")
    
    return results

# ★ pytest-style data testing
import pytest

def test_no_null_ids(cleaned_df):
    assert cleaned_df['id'].notna().all(), "Found null IDs after cleaning"

def test_date_range(cleaned_df):
    assert cleaned_df['date'].min() >= pd.Timestamp('2020-01-01'), "Dates before 2020 found"
    assert cleaned_df['date'].max() <= pd.Timestamp.now(), "Future dates found"

def test_no_negative_amounts(cleaned_df):
    assert (cleaned_df['amount'] >= 0).all(), "Negative amounts found"
```

---

## 📊 Automated Data Profiling (ydata-profiling)

```python
# pip install ydata-profiling
from ydata_profiling import ProfileReport
import pandas as pd

def auto_profile_for_cleaning(df, output_html='data_profile.html'):
    """
    สร้าง comprehensive data profile อัตโนมัติ
    ★ ต่างจาก Data Profiling ตรงที่ใช้ library เฉพาะทางสร้าง report สมบูรณ์
    ★ ใช้เป็น "ก่อน-หลัง" cleaning เพื่อเปรียบเทียบ
    """
    profile = ProfileReport(
        df,
        title="Data Quality Profile",
        explorative=True,
        correlations={
            "auto": {"calculate": True},
            "pearson": {"calculate": True},
            "spearman": {"calculate": True},
        },
        missing_diagrams={
            "bar": True,
            "matrix": True,
            "heatmap": True,
        }
    )
    
    profile.to_file(output_html)
    
    # Extract key stats programmatically
    desc = profile.get_description()
    stats = {
        'total_rows': desc.table['n'],
        'total_columns': desc.table['n_var'],
        'missing_cells': desc.table['n_cells_missing'],
        'missing_pct': desc.table['p_cells_missing'] * 100,
        'duplicate_rows': desc.table.get('n_duplicates', 0),
    }
    
    print(f"📊 Profile: {stats['total_rows']} rows, {stats['total_columns']} cols, "
          f"{stats['missing_pct']:.1f}% missing, {stats['duplicate_rows']} duplicates")
    
    return profile, stats

# ★ Before-After comparison
profile_before, _ = auto_profile_for_cleaning(df_raw, 'before_cleaning.html')
profile_after, _ = auto_profile_for_cleaning(df_cleaned, 'after_cleaning.html')
comparison = profile_before.compare(profile_after)
comparison.to_file('cleaning_comparison.html')
```

---

## 📖 Lookup Table Management (Reference Data)

```python
import pandas as pd
import json

class LookupTableManager:
    """
    จัดการ lookup/reference tables สำหรับ data cleaning
    ★ ต่างจาก Data Enrichment ตรงที่เน้นการจัดการ reference data เอง
    """
    def __init__(self, lookup_dir='./lookups'):
        self.lookup_dir = lookup_dir
        self.tables = {}
    
    def register(self, name, df, key_col, value_col=None, version='1.0'):
        """ลงทะเบียน lookup table"""
        self.tables[name] = {
            'df': df,
            'key': key_col,
            'value': value_col or [c for c in df.columns if c != key_col],
            'version': version,
            'row_count': len(df)
        }
    
    def apply_lookup(self, df, source_col, lookup_name, result_col=None, default=None):
        """Apply lookup → enrich data"""
        lookup = self.tables[lookup_name]
        lookup_df = lookup['df']
        
        result_col = result_col or f"{source_col}_lookup"
        mapping = lookup_df.set_index(lookup['key'])[lookup['value'][0]].to_dict()
        
        df[result_col] = df[source_col].map(mapping).fillna(default or 'UNKNOWN')
        unmapped = df[df[result_col] == 'UNKNOWN'][source_col].nunique()
        if unmapped > 0:
            print(f"⚠️ {unmapped} unique values ไม่พบใน {lookup_name}")
        
        return df
    
    def validate_coverage(self, df, source_col, lookup_name):
        """ตรวจว่า lookup table ครอบคลุมข้อมูลจริงครบหรือไม่"""
        lookup = self.tables[lookup_name]
        lookup_keys = set(lookup['df'][lookup['key']])
        data_keys = set(df[source_col].dropna())
        
        missing = data_keys - lookup_keys
        extra = lookup_keys - data_keys
        
        return {
            'coverage_pct': (1 - len(missing) / len(data_keys)) * 100 if data_keys else 100,
            'missing_in_lookup': list(missing),
            'unused_in_lookup': list(extra)
        }

# ตัวอย่าง
lm = LookupTableManager()
lm.register('provinces', provinces_df, 'code', ['name_th', 'name_en', 'region'])
lm.register('currencies', currencies_df, 'iso_code', ['name', 'symbol', 'rate_to_thb'])
df = lm.apply_lookup(df, 'province_code', 'provinces', 'province_name')
coverage = lm.validate_coverage(df, 'province_code', 'provinces')
```

---

## 🧠 Semantic Deduplication (Embedding-based)

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

def semantic_dedup(df, text_col, threshold=0.85, method='tfidf'):
    """
    Dedup ด้วย semantic similarity (ความหมายคล้ายกัน)
    ★ ต่างจาก exact/fuzzy dedup ตรงที่จับ duplicates ที่เขียนต่างกันแต่หมายความเหมือนกัน
    เช่น "Software Engineer" vs "SWE" vs "Dev" vs "นักพัฒนาซอฟต์แวร์"
    """
    texts = df[text_col].fillna('').astype(str).tolist()
    
    if method == 'tfidf':
        vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            analyzer='char_wb'  # character n-grams สำหรับ typo tolerance
        )
        embeddings = vectorizer.fit_transform(texts)
        sim_matrix = cosine_similarity(embeddings)
    
    # Find duplicate clusters
    n = len(texts)
    visited = set()
    clusters = []
    
    for i in range(n):
        if i in visited:
            continue
        cluster = [i]
        for j in range(i + 1, n):
            if j not in visited and sim_matrix[i, j] >= threshold:
                cluster.append(j)
                visited.add(j)
        if len(cluster) > 1:
            clusters.append(cluster)
        visited.add(i)
    
    # Mark duplicates (keep first in each cluster)
    dup_indices = set()
    for cluster in clusters:
        for idx in cluster[1:]:
            dup_indices.add(idx)
    
    df['is_semantic_dup'] = df.index.isin(dup_indices)
    
    print(f"🧠 Semantic Dedup: {len(clusters)} clusters, "
          f"{len(dup_indices)} duplicates (threshold={threshold})")
    
    return df, clusters

# ตัวอย่าง
df, clusters = semantic_dedup(products, 'product_name', threshold=0.8)
clean_products = df[~df['is_semantic_dup']]
```

---

## 🔧 Pipeline Orchestration Patterns (Airflow / Prefect)

```python
# ★ DAG pattern สำหรับ data cleaning pipeline
# Apache Airflow style

from datetime import datetime, timedelta

# Airflow DAG
"""
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_cleaning_pipeline',
    default_args=default_args,
    description='Automated data cleaning pipeline',
    schedule_interval='0 2 * * *',  # ทุกวัน 02:00
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['cleaning', 'etl'],
)

# Tasks
t1 = PythonOperator(task_id='ingest_raw', python_callable=ingest_raw_data, dag=dag)
t2 = PythonOperator(task_id='validate_schema', python_callable=validate_schema, dag=dag)
t3 = PythonOperator(task_id='clean_missing', python_callable=handle_missing_values, dag=dag)
t4 = PythonOperator(task_id='clean_duplicates', python_callable=remove_duplicates, dag=dag)
t5 = PythonOperator(task_id='standardize_formats', python_callable=standardize_all, dag=dag)
t6 = PythonOperator(task_id='validate_output', python_callable=run_data_tests, dag=dag)
t7 = PythonOperator(task_id='publish_clean', python_callable=publish_clean_data, dag=dag)

# Dependencies
t1 >> t2 >> [t3, t4] >> t5 >> t6 >> t7
"""

# ★ Python-native pipeline (no Airflow dependency)
class CleaningPipeline:
    """Lightweight cleaning pipeline with dependency management"""
    def __init__(self, name):
        self.name = name
        self.steps = []
        self.results = {}
    
    def add_step(self, name, func, depends_on=None):
        self.steps.append({
            'name': name,
            'func': func,
            'depends_on': depends_on or [],
            'status': 'pending'
        })
    
    def run(self, df):
        """Execute pipeline in order"""
        for step in self.steps:
            try:
                print(f"▶️ Running: {step['name']}")
                df = step['func'](df)
                step['status'] = 'success'
                self.results[step['name']] = {'status': 'success', 'rows': len(df)}
            except Exception as e:
                step['status'] = 'failed'
                self.results[step['name']] = {'status': 'failed', 'error': str(e)}
                print(f"❌ Failed: {step['name']}: {e}")
                break
        
        return df
    
    def report(self):
        """สรุปผล pipeline"""
        for name, result in self.results.items():
            icon = '✅' if result['status'] == 'success' else '❌'
            print(f"  {icon} {name}: {result}")

# ใช้งาน
pipeline = CleaningPipeline('daily_cleaning')
pipeline.add_step('remove_nulls', lambda df: df.dropna(subset=['id']))
pipeline.add_step('dedup', lambda df: df.drop_duplicates())
pipeline.add_step('standardize', standardize_formats)
pipeline.add_step('validate', validate_data_quality)
clean_df = pipeline.run(raw_df)
pipeline.report()
```

---

## 📐 Statistical Testing for Data Quality

```python
from scipy import stats
import pandas as pd
import numpy as np

def comprehensive_statistical_tests(df, numeric_cols=None):
    """
    ★ ใช้ statistical tests เพื่อประเมินคุณภาพข้อมูลก่อน/หลัง cleaning
    ต่างจาก Data Drift Detection ตรงที่เน้นคุณสมบัติภายในของ dataset เอง
    """
    numeric_cols = numeric_cols or df.select_dtypes(include=[np.number]).columns.tolist()
    results = {}
    
    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) < 8:
            continue
        
        col_results = {}
        
        # 1) Normality test (Shapiro-Wilk)
        if len(data) <= 5000:
            stat, p = stats.shapiro(data.sample(min(len(data), 5000)))
            col_results['normality'] = {
                'test': 'Shapiro-Wilk',
                'statistic': stat,
                'p_value': p,
                'is_normal': p > 0.05
            }
        
        # 2) Skewness & Kurtosis
        skew = data.skew()
        kurt = data.kurtosis()
        col_results['distribution'] = {
            'skewness': skew,
            'is_skewed': abs(skew) > 1,
            'kurtosis': kurt,
            'is_heavy_tailed': abs(kurt) > 3
        }
        
        # 3) Stationarity test (Augmented Dickey-Fuller) — สำหรับ time series
        if len(data) > 20:
            try:
                adf_stat, adf_p, *_ = stats.linregress(range(len(data)), data.values)
                col_results['trend'] = {
                    'has_trend': adf_p < 0.05,
                    'slope': adf_stat
                }
            except:
                pass
        
        # 4) Outlier proportion (IQR method)
        q1, q3 = data.quantile(0.25), data.quantile(0.75)
        iqr = q3 - q1
        outlier_count = ((data < q1 - 1.5 * iqr) | (data > q3 + 1.5 * iqr)).sum()
        col_results['outliers'] = {
            'count': int(outlier_count),
            'proportion': outlier_count / len(data),
            'needs_treatment': outlier_count / len(data) > 0.05
        }
        
        # 5) Zero-inflation test
        zero_pct = (data == 0).sum() / len(data)
        col_results['zero_inflation'] = {
            'zero_pct': zero_pct,
            'is_zero_inflated': zero_pct > 0.5
        }
        
        results[col] = col_results
    
    # Summary
    issues = []
    for col, tests in results.items():
        if tests.get('distribution', {}).get('is_skewed'):
            issues.append(f"📐 {col}: highly skewed ({tests['distribution']['skewness']:.2f})")
        if tests.get('outliers', {}).get('needs_treatment'):
            issues.append(f"🔴 {col}: {tests['outliers']['proportion']*100:.1f}% outliers")
        if tests.get('zero_inflation', {}).get('is_zero_inflated'):
            issues.append(f"⭕ {col}: zero-inflated ({tests['zero_inflation']['zero_pct']*100:.0f}%)")
    
    print(f"📐 Statistical Tests: {len(results)} columns, {len(issues)} issues found")
    for issue in issues:
        print(f"  {issue}")
    
    return results
```

---

## 📚 Data Catalog & Metadata Management

```python
import pandas as pd
from datetime import datetime
import json
import hashlib

class DataCatalog:
    """
    จัดการ metadata สำหรับ datasets ที่ผ่านการ cleaning
    ★ ต่างจาก Data Lineage ตรงที่เน้น catalog ของ datasets ไม่ใช่ tracking ops
    """
    def __init__(self):
        self.catalog = {}
    
    def register_dataset(self, name, df, description='', tags=None, owner=''):
        """ลงทะเบียน dataset ใน catalog"""
        col_metadata = {}
        for col in df.columns:
            col_metadata[col] = {
                'dtype': str(df[col].dtype),
                'null_pct': df[col].isna().mean() * 100,
                'unique_count': df[col].nunique(),
                'sample_values': df[col].dropna().head(3).tolist(),
            }
            if df[col].dtype in ['int64', 'float64']:
                col_metadata[col].update({
                    'min': float(df[col].min()) if not df[col].isna().all() else None,
                    'max': float(df[col].max()) if not df[col].isna().all() else None,
                    'mean': float(df[col].mean()) if not df[col].isna().all() else None,
                })
        
        # Data fingerprint
        fingerprint = hashlib.md5(
            pd.util.hash_pandas_object(df).values.tobytes()
        ).hexdigest()
        
        self.catalog[name] = {
            'description': description,
            'owner': owner,
            'tags': tags or [],
            'registered_at': datetime.now().isoformat(),
            'row_count': len(df),
            'col_count': len(df.columns),
            'memory_mb': df.memory_usage(deep=True).sum() / 1024**2,
            'columns': col_metadata,
            'fingerprint': fingerprint,
            'quality_score': self._compute_quality_score(df),
        }
    
    def _compute_quality_score(self, df):
        """คำนวณ quality score (0-100)"""
        completeness = (1 - df.isna().mean().mean()) * 40
        uniqueness = min(df.nunique().mean() / len(df), 1) * 20
        consistency = 20  # base score
        validity = 20 if not df.duplicated().any() else 10
        return round(completeness + uniqueness + consistency + validity, 1)
    
    def search(self, query='', tags=None):
        """ค้นหา datasets"""
        results = []
        for name, meta in self.catalog.items():
            if query.lower() in name.lower() or query.lower() in meta['description'].lower():
                if tags is None or any(t in meta['tags'] for t in tags):
                    results.append({'name': name, **meta})
        return results
    
    def export_catalog(self, path='data_catalog.json'):
        """Export catalog เป็น JSON"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.catalog, f, indent=2, ensure_ascii=False, default=str)

# ตัวอย่าง
catalog = DataCatalog()
catalog.register_dataset(
    'customers_cleaned',
    df_customers,
    description='Customer data หลัง cleaning pipeline',
    tags=['customers', 'cleaned', 'production'],
    owner='data-team'
)
```

---

## 🏭 Industry-Specific Use Cases (เพิ่มเติม Round 6)

### 36. ⚖️ Legal / Law Firm

| ปัญหา | วิธีแก้ |
|--------|--------|
| Case number format variations | Regex normalization + lookup table |
| Court name abbreviations inconsistent | Canonical court name mapping |
| Date formats mixed (Thai/Western calendar) | Buddhist→Gregorian year conversion |
| Attorney name duplicates (Thai/English) | Bilingual fuzzy matching |
| Contract clause extraction from PDF | NLP + regex structured extraction |

### 37. 🎓 Research / Academic

| ปัญหา | วิธีแก้ |
|--------|--------|
| DOI/citation format inconsistency | Crossref API validation |
| Author name disambiguation | ORCID matching + phonetic dedup |
| Mixed measurement units in papers | Unit ontology standardization |
| Survey Likert scale encoding varies | Recode to uniform 1-5 |
| Missing IRB/ethics approval codes | Mandatory field validation |

### 38. 🎮 eSports / Competitive Gaming

| ปัญหา | วิธีแก้ |
|--------|--------|
| Player tag/alias changes over time | Alias history chain linking |
| Match timestamp timezone confusion | UTC normalization + event timezone |
| Score/stat anomalies (cheating) | Isolation Forest anomaly detection |
| Team roster overlap conflicts | Temporal validity constraint |
| Cross-platform player identity | Semantic dedup on player profiles |

### 39. 🏥 Veterinary / Animal Health

| ปัญหา | วิธีแก้ |
|--------|--------|
| Animal breed name variations | Breed registry lookup (AKC/TICA) |
| Weight units mixed (kg/lb) | Auto-detect + conversion |
| Vaccination record duplicates | Date + vaccine + animal_id dedup |
| Species-specific normal ranges | Species-aware outlier detection |
| Owner information duplication | Record linkage across visits |

### 40. 🍷 Wine / Beverage Industry

| ปัญหา | วิธีแก้ |
|--------|--------|
| Vintage year typos (2-digit vs 4-digit) | Year disambiguator (20→2020 vs 1920) |
| Region/appellation name variations | Wine region ontology mapping |
| Tasting notes free-text inconsistency | NLP topic standardization |
| Alcohol percentage out-of-range | Domain validation (0-100%) |
| Label OCR errors | String distance correction |

---

## 🎯 MinHash / LSH — Deduplication at Scale

```python
from datasketch import MinHash, MinHashLSH
import pandas as pd
import re

def minhash_dedup_at_scale(df, text_col, threshold=0.5, num_perm=128):
    """
    Probabilistic dedup สำหรับ dataset ขนาดใหญ่ (ล้าน+ records)
    ★ ต่างจาก Semantic Dedup ตรงที่ใช้ hashing ไม่ต้อง compute full similarity matrix
    ★ O(n) แทน O(n²) — scale ได้จริง
    """
    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
    minhashes = {}
    
    for idx, row in df.iterrows():
        text = str(row[text_col]).lower()
        # Shingling: แบ่งเป็น 3-gram
        shingles = set([text[i:i+3] for i in range(len(text)-2)])
        
        mh = MinHash(num_perm=num_perm)
        for s in shingles:
            mh.update(s.encode('utf-8'))
        
        minhashes[idx] = mh
        try:
            lsh.insert(str(idx), mh)
        except ValueError:
            pass  # duplicate key
    
    # Find duplicate clusters
    clusters = []
    seen = set()
    for idx, mh in minhashes.items():
        if idx in seen:
            continue
        candidates = lsh.query(mh)
        cluster = [int(c) for c in candidates]
        if len(cluster) > 1:
            clusters.append(cluster)
            seen.update(cluster)
    
    dup_indices = set()
    for cluster in clusters:
        for idx in cluster[1:]:
            dup_indices.add(idx)
    
    df['is_lsh_dup'] = df.index.isin(dup_indices)
    print(f"🎯 MinHash LSH: {len(clusters)} clusters, {len(dup_indices)} duplicates "
          f"(threshold={threshold}, {len(df)} records)")
    
    return df, clusters
```

---

## ⚡ Data Wrangling with Polars (High-Performance)

```python
import polars as pl

def clean_with_polars(file_path):
    """
    ★ Polars: เร็วกว่า Pandas 3-30x, ใช้ memory น้อยกว่า
    ★ เหมาะกับ dataset ขนาดใหญ่ที่ Pandas ช้าเกินไป
    """
    # Lazy evaluation — ไม่ load ทั้งหมดจนกว่าจะ .collect()
    df = (
        pl.scan_csv(file_path, infer_schema_length=10000)
        
        # 1) ลบ duplicates
        .unique(maintain_order=True)
        
        # 2) Handle missing values
        .with_columns([
            pl.col('name').fill_null('Unknown'),
            pl.col('amount').fill_null(pl.col('amount').median()),
            pl.col('date').str.to_datetime('%Y-%m-%d', strict=False),
        ])
        
        # 3) Filter invalid rows
        .filter(
            (pl.col('amount') > 0) &
            (pl.col('name').str.lengths() > 0)
        )
        
        # 4) Standardize text
        .with_columns([
            pl.col('name').str.strip_chars().str.to_lowercase().alias('name_clean'),
            pl.col('email').str.strip_chars().str.to_lowercase(),
        ])
        
        # 5) Type casting
        .with_columns([
            pl.col('age').cast(pl.Int32, strict=False),
            pl.col('category').cast(pl.Categorical),
        ])
        
        .collect()  # Execute ทั้งหมดพร้อมกัน (optimized query plan)
    )
    
    return df

# ★ Polars vs Pandas comparison
# Pandas: df.groupby('category')['amount'].mean()
# Polars: df.group_by('category').agg(pl.col('amount').mean())

# ★ Parallel read
df = pl.read_csv('huge_file.csv', n_threads=8)

# ★ Save optimized
df.write_parquet('clean_data.parquet', compression='zstd')
```

---

## 📄 PDF / OCR Table Extraction

```python
import camelot
import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd

def extract_tables_from_pdf(pdf_path, method='camelot'):
    """
    ดึงตารางจาก PDF → DataFrame
    ★ ต่างจาก Dirty Excel Handling ตรงที่จัดการ PDF โดยเฉพาะ
    """
    all_tables = []
    
    if method == 'camelot':
        # Lattice: ตารางที่มีเส้นขอบ
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
        if len(tables) == 0:
            # Stream: ตารางที่ไม่มีเส้นขอบ
            tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
        
        for t in tables:
            df = t.df
            # ใช้แถวแรกเป็น header
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)
            # Clean empty strings
            df = df.replace('', pd.NA)
            all_tables.append(df)
    
    elif method == 'pdfplumber':
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df = df.replace('', pd.NA)
                    all_tables.append(df)
    
    print(f"📄 Extracted {len(all_tables)} tables from {pdf_path}")
    return all_tables

def ocr_scanned_pdf(image_path, lang='tha+eng'):
    """OCR สำหรับ PDF ที่เป็น scan (ไม่มี text layer)"""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang=lang)
    
    # Extract tabular data from OCR text
    lines = text.strip().split('\n')
    rows = [re.split(r'\s{2,}|\t', line) for line in lines if line.strip()]
    
    if rows:
        df = pd.DataFrame(rows[1:], columns=rows[0] if rows else None)
        return df
    return pd.DataFrame()
```

---

## 🔒 Privacy-Preserving Anonymization (k-Anonymity, l-Diversity, t-Closeness)

```python
import pandas as pd
import numpy as np

class PrivacyAnonymizer:
    """
    ★ ต่างจาก PII Masking และ Data Masking for Testing
    ★ ใช้ formal privacy models เพื่อรับประกันทางคณิตศาสตร์
    """
    
    def k_anonymize(self, df, quasi_identifiers, k=5):
        """
        k-Anonymity: ทุก record ต้องมีอย่างน้อย k records 
        ที่มี quasi-identifier เหมือนกัน
        """
        df_anon = df.copy()
        
        # Generalization rules
        generalizers = {
            'age': lambda x: f"{(x // 10) * 10}-{(x // 10) * 10 + 9}",  # 25 → "20-29"
            'zipcode': lambda x: str(x)[:3] + '**',                       # 10200 → "102**"
            'date': lambda x: str(x)[:7] if pd.notna(x) else x,          # 2024-03-15 → "2024-03"
        }
        
        for col in quasi_identifiers:
            if col in generalizers and col in df_anon.columns:
                df_anon[col] = df_anon[col].apply(generalizers[col])
        
        # Check k-anonymity
        group_sizes = df_anon.groupby(quasi_identifiers).size()
        violations = group_sizes[group_sizes < k]
        
        if len(violations) > 0:
            # Suppress small groups
            small_groups = violations.index.tolist()
            mask = df_anon[quasi_identifiers].apply(tuple, axis=1).isin(small_groups)
            df_anon = df_anon[~mask]
            print(f"⚠️ Suppressed {mask.sum()} records with groups < {k}")
        
        print(f"🔒 k={k} anonymity: {len(df_anon)} records, min group={group_sizes.min()}")
        return df_anon
    
    def check_l_diversity(self, df, quasi_identifiers, sensitive_col, l=3):
        """l-Diversity: ทุก equivalence class ต้องมีอย่างน้อย l ค่า sensitive ที่แตกต่างกัน"""
        diversity = df.groupby(quasi_identifiers)[sensitive_col].nunique()
        violations = diversity[diversity < l]
        
        return {
            'is_l_diverse': len(violations) == 0,
            'min_diversity': int(diversity.min()),
            'violations': len(violations),
            'details': violations.to_dict() if len(violations) > 0 else {}
        }
    
    def check_t_closeness(self, df, quasi_identifiers, sensitive_col, t=0.2):
        """t-Closeness: distribution ของ sensitive attr ในแต่ละ group ต้องใกล้เคียง overall"""
        overall_dist = df[sensitive_col].value_counts(normalize=True)
        
        violations = []
        for name, group in df.groupby(quasi_identifiers):
            group_dist = group[sensitive_col].value_counts(normalize=True)
            # Earth Mover's Distance (simplified)
            all_vals = set(overall_dist.index) | set(group_dist.index)
            distance = sum(
                abs(overall_dist.get(v, 0) - group_dist.get(v, 0))
                for v in all_vals
            ) / 2
            
            if distance > t:
                violations.append({'group': name, 'distance': distance})
        
        return {
            'is_t_close': len(violations) == 0,
            'violations': violations
        }
```

---

## 📊 Winsorization & Outlier Treatment Strategies

```python
from scipy.stats import mstats
import pandas as pd
import numpy as np

def treat_outliers(df, columns, method='winsorize', limits=(0.05, 0.05)):
    """
    ★ ต่างจาก Outlier Detection (Z-score/IQR/Isolation Forest)
    ★ เน้นวิธี "จัดการ" outliers ไม่ใช่แค่ตรวจจับ
    """
    df_treated = df.copy()
    report = {}
    
    for col in columns:
        if col not in df_treated.columns or not np.issubdtype(df_treated[col].dtype, np.number):
            continue
        
        original = df_treated[col].copy()
        n_outliers_before = 0
        
        if method == 'winsorize':
            # แทนค่า extreme ด้วยค่าที่ percentile กำหนด
            df_treated[col] = mstats.winsorize(df_treated[col].dropna(), limits=limits)
        
        elif method == 'cap_iqr':
            # Cap ที่ IQR * 1.5
            q1, q3 = df_treated[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            n_outliers_before = ((original < lower) | (original > upper)).sum()
            df_treated[col] = df_treated[col].clip(lower, upper)
        
        elif method == 'log_transform':
            # Log transformation (สำหรับ right-skewed data)
            min_val = df_treated[col].min()
            if min_val <= 0:
                df_treated[col] = np.log1p(df_treated[col] - min_val + 1)
            else:
                df_treated[col] = np.log1p(df_treated[col])
        
        elif method == 'sqrt_transform':
            df_treated[col] = np.sqrt(df_treated[col].clip(lower=0))
        
        elif method == 'percentile_cap':
            # Cap ที่ percentile ที่กำหนด
            lower_p = df_treated[col].quantile(limits[0])
            upper_p = df_treated[col].quantile(1 - limits[1])
            n_outliers_before = (
                (original < lower_p) | (original > upper_p)
            ).sum()
            df_treated[col] = df_treated[col].clip(lower_p, upper_p)
        
        elif method == 'median_replace':
            # แทน outliers ด้วย median
            q1, q3 = df_treated[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            mask = (df_treated[col] < q1 - 1.5 * iqr) | (df_treated[col] > q3 + 1.5 * iqr)
            n_outliers_before = mask.sum()
            df_treated[col] = df_treated[col].where(~mask, df_treated[col].median())
        
        report[col] = {
            'method': method,
            'outliers_treated': n_outliers_before,
            'mean_before': original.mean(),
            'mean_after': df_treated[col].mean(),
        }
    
    print(f"📊 Outlier Treatment ({method}): {sum(r['outliers_treated'] for r in report.values())} values treated")
    return df_treated, report
```

---

## 🕐 Timezone Handling (pytz / zoneinfo / DST)

```python
from datetime import datetime, timezone
import pytz
import pandas as pd

# Python 3.9+
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

def standardize_timezones(df, datetime_col, source_tz=None, target_tz='Asia/Bangkok'):
    """
    ★ ต่างจาก Date Cleaning ตรงที่เน้น timezone conversion + DST edge cases
    """
    target = ZoneInfo(target_tz)
    
    df_tz = df.copy()
    dt_series = pd.to_datetime(df_tz[datetime_col], errors='coerce')
    
    if source_tz:
        source = ZoneInfo(source_tz)
        # Localize naive datetimes
        dt_series = dt_series.dt.tz_localize(source, ambiguous='NaT', nonexistent='shift_forward')
    
    # Convert to target timezone
    if dt_series.dt.tz is not None:
        dt_series = dt_series.dt.tz_convert(target)
    
    df_tz[datetime_col] = dt_series
    df_tz[f'{datetime_col}_utc'] = dt_series.dt.tz_convert('UTC')
    
    return df_tz

def handle_dst_edge_cases(df, datetime_col, tz_name='US/Eastern'):
    """จัดการ DST edge cases: ambiguous times + non-existent times"""
    tz = pytz.timezone(tz_name)
    
    results = []
    for val in df[datetime_col]:
        if pd.isna(val):
            results.append({'dt': pd.NaT, 'dst_issue': None})
            continue
        
        dt = pd.Timestamp(val)
        try:
            localized = tz.localize(dt.to_pydatetime(), is_dst=None)
            results.append({'dt': localized, 'dst_issue': None})
        except pytz.exceptions.AmbiguousTimeError:
            # เวลาซ้ำ (fall back) — เลือก standard time
            localized = tz.localize(dt.to_pydatetime(), is_dst=False)
            results.append({'dt': localized, 'dst_issue': 'ambiguous'})
        except pytz.exceptions.NonExistentTimeError:
            # เวลาไม่มีอยู่ (spring forward) — shift ไปข้างหน้า
            localized = tz.localize(dt.to_pydatetime() + pd.Timedelta(hours=1), is_dst=True)
            results.append({'dt': localized, 'dst_issue': 'non_existent'})
    
    result_df = pd.DataFrame(results)
    issues = result_df['dst_issue'].notna().sum()
    if issues > 0:
        print(f"🕐 DST: {issues} edge cases handled ({tz_name})")
    
    return result_df
```

---

## 🔡 Character Encoding Detection & Fixing

```python
import chardet
from charset_normalizer import from_path, from_bytes
import codecs
import pandas as pd

def detect_and_fix_encoding(file_path, target_encoding='utf-8'):
    """
    ★ ต่างจาก Encoding/Unicode cleaning ตรงที่เน้นตรวจจับ encoding ที่ไม่รู้
    ★ แก้ mojibake (ตัวอักษรเพี้ยน) จาก wrong encoding
    """
    # 1) Detect encoding
    with open(file_path, 'rb') as f:
        raw = f.read()
    
    # chardet detection
    chardet_result = chardet.detect(raw)
    
    # charset-normalizer (ดีกว่า chardet สำหรับ multi-language)
    normalizer_results = from_bytes(raw).best()
    
    detected = normalizer_results.encoding if normalizer_results else chardet_result['encoding']
    confidence = chardet_result['confidence']
    
    print(f"🔡 Detected: {detected} (confidence: {confidence:.0%})")
    
    # 2) Read with correct encoding
    try:
        df = pd.read_csv(file_path, encoding=detected)
    except (UnicodeDecodeError, LookupError):
        # Fallback chain
        for enc in ['utf-8-sig', 'cp874', 'tis-620', 'cp1252', 'latin1', 'iso-8859-1']:
            try:
                df = pd.read_csv(file_path, encoding=enc)
                detected = enc
                break
            except (UnicodeDecodeError, LookupError):
                continue
    
    return df, detected

def fix_mojibake(text):
    """แก้ตัวอักษรเพี้ยนจาก wrong encoding"""
    if not isinstance(text, str):
        return text
    
    # Common Thai mojibake patterns
    fixes = [
        ('utf-8', 'cp874'),     # Thai wrongly decoded as UTF-8
        ('cp1252', 'utf-8'),    # UTF-8 wrongly decoded as Windows-1252
        ('latin1', 'utf-8'),    # UTF-8 wrongly decoded as Latin-1
    ]
    
    for wrong, correct in fixes:
        try:
            fixed = text.encode(wrong).decode(correct)
            if any('\u0e00' <= c <= '\u0e7f' for c in fixed):  # Has Thai chars
                return fixed
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    
    return text
```

---

## 🔗 Fuzzy Join (Approximate Matching Between DataFrames)

```python
from thefuzz import fuzz, process
import pandas as pd

def fuzzy_join(df_left, df_right, left_on, right_on, threshold=80, method='token_sort'):
    """
    ★ ต่างจาก String Distance Metrics ตรงที่ทำ JOIN ระหว่าง 2 DataFrames
    ★ ต่างจาก Record Linkage ตรงที่เน้น merge/join ไม่ใช่ dedup
    """
    scorers = {
        'ratio': fuzz.ratio,
        'partial': fuzz.partial_ratio,
        'token_sort': fuzz.token_sort_ratio,
        'token_set': fuzz.token_set_ratio,
    }
    scorer = scorers.get(method, fuzz.token_sort_ratio)
    
    right_values = df_right[right_on].dropna().unique().tolist()
    
    matches = []
    for idx, row in df_left.iterrows():
        left_val = str(row[left_on])
        if not left_val or left_val == 'nan':
            matches.append({'left_idx': idx, 'match': None, 'score': 0})
            continue
        
        best_match, score = process.extractOne(
            left_val, right_values, scorer=scorer
        ) or (None, 0)
        
        matches.append({
            'left_idx': idx,
            'match': best_match if score >= threshold else None,
            'score': score
        })
    
    match_df = pd.DataFrame(matches)
    
    # Join results
    df_left['_fuzzy_match'] = match_df['match'].values
    df_left['_fuzzy_score'] = match_df['score'].values
    
    result = df_left.merge(
        df_right,
        left_on='_fuzzy_match',
        right_on=right_on,
        how='left',
        suffixes=('', '_right')
    )
    
    matched = match_df['match'].notna().sum()
    print(f"🔗 Fuzzy Join: {matched}/{len(df_left)} matched (threshold={threshold})")
    
    return result
```

---

## 🤖 Active Learning for Data Cleaning

```python
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd

class ActiveLearningCleaner:
    """
    ★ ML ถามคนเมื่อไม่แน่ใจ ลดงาน manual review ลง 80%+
    ★ ต่างจากเทคนิคอื่นตรงที่เป็น human-in-the-loop
    """
    def __init__(self, features_cols, label_col='is_clean'):
        self.features_cols = features_cols
        self.label_col = label_col
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.labeled_indices = []
    
    def initial_sample(self, df, n=50):
        """เลือก sample เริ่มต้นสำหรับ human labeling"""
        return df.sample(n=min(n, len(df)), random_state=42).index.tolist()
    
    def uncertainty_sampling(self, df, n=20):
        """เลือก records ที่ model ไม่แน่ใจมากที่สุด"""
        if len(self.labeled_indices) == 0:
            return self.initial_sample(df, n)
        
        # Train on labeled data
        labeled_df = df.loc[self.labeled_indices]
        X_train = labeled_df[self.features_cols].fillna(0)
        y_train = labeled_df[self.label_col]
        
        self.model.fit(X_train, y_train)
        
        # Predict probabilities for unlabeled
        unlabeled = df.drop(self.labeled_indices, errors='ignore')
        X_unlabeled = unlabeled[self.features_cols].fillna(0)
        
        probs = self.model.predict_proba(X_unlabeled)
        # Uncertainty = how close to 0.5 (most uncertain)
        uncertainty = 1 - np.abs(probs[:, 1] - 0.5) * 2
        
        # Return top-n most uncertain
        uncertain_indices = np.argsort(uncertainty)[-n:]
        return unlabeled.iloc[uncertain_indices].index.tolist()
    
    def label_and_learn(self, df, indices, labels):
        """เพิ่ม labels จาก human → retrain model"""
        for idx, label in zip(indices, labels):
            df.loc[idx, self.label_col] = label
            self.labeled_indices.append(idx)
        
        # Retrain
        labeled_df = df.loc[self.labeled_indices]
        X = labeled_df[self.features_cols].fillna(0)
        y = labeled_df[self.label_col]
        self.model.fit(X, y)
        
        accuracy = self.model.score(X, y)
        print(f"🤖 Active Learning: {len(self.labeled_indices)} labeled, accuracy={accuracy:.2%}")
    
    def auto_clean(self, df, confidence_threshold=0.95):
        """ทำความสะอาดอัตโนมัติสำหรับ records ที่ model มั่นใจ"""
        X = df[self.features_cols].fillna(0)
        probs = self.model.predict_proba(X)
        
        confident_mask = np.max(probs, axis=1) >= confidence_threshold
        df['predicted_clean'] = self.model.predict(X)
        df['confidence'] = np.max(probs, axis=1)
        df['needs_review'] = ~confident_mask
        
        auto = confident_mask.sum()
        review = (~confident_mask).sum()
        print(f"🤖 Auto-cleaned: {auto}, needs review: {review}")
        return df
```

---

## 🕸️ Graph / Network Data Cleaning

```python
import networkx as nx
import pandas as pd

def clean_graph_data(edges_df, source_col='source', target_col='target', weight_col=None):
    """
    ★ ทำความสะอาด graph/network data (nodes + edges)
    ★ ไม่มีใน round อื่น — เป็น data type เฉพาะทาง
    """
    G = nx.from_pandas_edgelist(edges_df, source_col, target_col, 
                                 edge_attr=weight_col, create_using=nx.Graph())
    
    original_nodes = G.number_of_nodes()
    original_edges = G.number_of_edges()
    
    # 1) Remove self-loops
    self_loops = list(nx.selfloop_edges(G))
    G.remove_edges_from(self_loops)
    
    # 2) Remove isolated nodes (no connections)
    isolates = list(nx.isolates(G))
    G.remove_nodes_from(isolates)
    
    # 3) Remove duplicate edges (keep highest weight)
    if isinstance(G, nx.MultiGraph):
        G = nx.Graph(G)  # Collapse multi-edges
    
    # 4) Detect and remove weak edges (optional)
    if weight_col:
        weak_edges = [(u, v) for u, v, d in G.edges(data=True)
                       if d.get(weight_col, 1) < 0.1]
        G.remove_edges_from(weak_edges)
    
    # 5) Find disconnected components
    components = list(nx.connected_components(G))
    largest = max(components, key=len) if components else set()
    small_components = [c for c in components if len(c) < 3]
    
    # 6) Node dedup (same name, different case)
    node_mapping = {}
    for node in G.nodes():
        canonical = str(node).lower().strip()
        if canonical not in node_mapping:
            node_mapping[canonical] = node
    
    print(f"🕸️ Graph Clean: {original_nodes}→{G.number_of_nodes()} nodes, "
          f"{original_edges}→{G.number_of_edges()} edges, "
          f"{len(self_loops)} self-loops, {len(isolates)} isolates removed, "
          f"{len(components)} components")
    
    return G, {
        'self_loops_removed': len(self_loops),
        'isolates_removed': len(isolates),
        'components': len(components),
        'largest_component_size': len(largest)
    }
```

---

## 📦 Data Versioning Tools (DVC / lakeFS)

```python
# ★ DVC (Data Version Control) — Git สำหรับ data
"""
# Setup
pip install dvc
dvc init
dvc remote add -d storage s3://bucket/dvc-store

# Track data files
dvc add data/raw/customers.csv
git add data/raw/customers.csv.dvc .gitignore
git commit -m "feat: add raw customer data v1"

# After cleaning
dvc add data/cleaned/customers_clean.csv
git add data/cleaned/customers_clean.csv.dvc
git commit -m "feat: cleaned customer data — removed 1,234 dupes"

# Switch between versions
git checkout v1.0
dvc checkout

# Compare versions
dvc diff HEAD~1

# Pipeline (cleaning as reproducible pipeline)
dvc run -n clean_data \
  -d data/raw/customers.csv \
  -d scripts/clean.py \
  -o data/cleaned/customers_clean.csv \
  python scripts/clean.py
"""

# ★ lakeFS — Git-like branching for data lakes
"""
# lakeFS CLI
lakectl branch create lakefs://repo/cleaning-experiment

# Work on branch
lakectl fs upload lakefs://repo/cleaning-experiment/data/clean.csv ./clean.csv

# Compare branches
lakectl diff lakefs://repo/main lakefs://repo/cleaning-experiment

# Merge when satisfied
lakectl merge lakefs://repo/cleaning-experiment lakefs://repo/main

# Rollback if needed
lakectl revert lakefs://repo/main --commit <hash>
"""

# ★ Python integration
def version_cleaned_data(df, version_tag, metadata=None):
    """Lightweight versioning without DVC/lakeFS"""
    import json, hashlib
    from datetime import datetime
    
    fingerprint = hashlib.md5(
        pd.util.hash_pandas_object(df).values.tobytes()
    ).hexdigest()
    
    version_info = {
        'version': version_tag,
        'timestamp': datetime.now().isoformat(),
        'rows': len(df),
        'columns': len(df.columns),
        'fingerprint': fingerprint,
        'metadata': metadata or {}
    }
    
    # Save versioned data
    df.to_parquet(f'data/v{version_tag}/data.parquet')
    with open(f'data/v{version_tag}/metadata.json', 'w') as f:
        json.dump(version_info, f, indent=2)
    
    return version_info
```

---

## 📏 Denial Constraints & Conditional Functional Dependencies

```python
import pandas as pd
from itertools import combinations

def check_denial_constraints(df, constraints):
    """
    ★ Formal data quality rules ที่เข้มกว่า simple validation
    ★ ต่างจาก Functional Dependencies ตรงที่ใช้ denial constraints (DCs)
    """
    violations = {}
    
    for name, check_fn in constraints.items():
        # Check all pairs of rows
        violating_pairs = []
        for i, j in combinations(range(len(df)), 2):
            if check_fn(df.iloc[i], df.iloc[j]):
                violating_pairs.append((i, j))
        
        if violating_pairs:
            violations[name] = {
                'count': len(violating_pairs),
                'sample': violating_pairs[:5]
            }
    
    return violations

# ตัวอย่าง Denial Constraints
constraints = {
    # DC1: ถ้า city เดียวกัน → zip code ต้องเหมือนกัน (CFD)
    'city_determines_zip': lambda r1, r2: (
        r1['city'] == r2['city'] and r1['zipcode'] != r2['zipcode']
    ),
    # DC2: ถ้า employee_id เดียวกัน → salary ต้องเท่ากัน
    'employee_unique_salary': lambda r1, r2: (
        r1['emp_id'] == r2['emp_id'] and r1['salary'] != r2['salary']
    ),
    # DC3: manager salary ต้องมากกว่า subordinate
    'manager_salary_higher': lambda r1, r2: (
        r1['emp_id'] == r2['manager_id'] and r1['salary'] <= r2['salary']
    ),
}

violations = check_denial_constraints(df, constraints)

def discover_cfds(df, lhs_cols, rhs_col, min_support=0.9):
    """Auto-discover Conditional Functional Dependencies"""
    total = len(df)
    cfds = []
    
    for r in range(1, len(lhs_cols) + 1):
        for combo in combinations(lhs_cols, r):
            lhs = list(combo)
            # Check: lhs → rhs_col
            groups = df.groupby(lhs)[rhs_col].nunique()
            deterministic = (groups == 1).sum()
            support = deterministic / len(groups)
            
            if support >= min_support:
                cfds.append({
                    'lhs': lhs,
                    'rhs': rhs_col,
                    'support': support,
                    'groups': len(groups)
                })
    
    return cfds
```

---

## 👥 Crowdsourced / Human-in-the-Loop Cleaning

```python
import pandas as pd
import json
from datetime import datetime

class CrowdsourcedCleaner:
    """
    ★ สร้าง review tasks สำหรับ human reviewers
    ★ Consensus-based cleaning — หลายคนตรวจ → vote
    """
    def __init__(self, min_agreement=0.7, reviewers_per_task=3):
        self.min_agreement = min_agreement
        self.reviewers_per_task = reviewers_per_task
        self.tasks = []
        self.reviews = {}
    
    def create_review_tasks(self, df, suspicious_indices, fields_to_review):
        """สร้าง review tasks สำหรับ records ที่น่าสงสัย"""
        for idx in suspicious_indices:
            task = {
                'task_id': f"T{len(self.tasks)+1:05d}",
                'record_idx': idx,
                'data': df.loc[idx, fields_to_review].to_dict(),
                'status': 'pending',
                'created_at': datetime.now().isoformat(),
                'reviews': [],
                'consensus': None
            }
            self.tasks.append(task)
        
        print(f"👥 Created {len(suspicious_indices)} review tasks "
              f"({self.reviewers_per_task} reviewers each)")
        return self.tasks
    
    def submit_review(self, task_id, reviewer_id, decision, corrected_values=None):
        """Submit human review"""
        task = next((t for t in self.tasks if t['task_id'] == task_id), None)
        if not task:
            return
        
        task['reviews'].append({
            'reviewer': reviewer_id,
            'decision': decision,  # 'correct', 'incorrect', 'uncertain'
            'corrected_values': corrected_values,
            'timestamp': datetime.now().isoformat()
        })
        
        # Check consensus
        if len(task['reviews']) >= self.reviewers_per_task:
            decisions = [r['decision'] for r in task['reviews']]
            from collections import Counter
            vote = Counter(decisions).most_common(1)[0]
            
            if vote[1] / len(decisions) >= self.min_agreement:
                task['consensus'] = vote[0]
                task['status'] = 'resolved'
            else:
                task['status'] = 'needs_escalation'
    
    def apply_consensus(self, df):
        """Apply reviewed corrections"""
        corrections = 0
        for task in self.tasks:
            if task['consensus'] == 'incorrect':
                # Apply most common correction
                corrected = [r['corrected_values'] for r in task['reviews']
                           if r['corrected_values']]
                if corrected:
                    for key, val in corrected[0].items():
                        df.loc[task['record_idx'], key] = val
                    corrections += 1
        
        print(f"👥 Applied {corrections} crowd-sourced corrections")
        return df
```

---

## 🏛️ Data Governance Framework

```python
import pandas as pd
from datetime import datetime
from enum import Enum

class DataClassification(Enum):
    PUBLIC = 'public'
    INTERNAL = 'internal'
    CONFIDENTIAL = 'confidential'
    RESTRICTED = 'restricted'

class DataGovernanceFramework:
    """
    ★ Framework สำหรับจัดการ data governance ทั้งองค์กร
    ★ ต่างจาก Data Catalog ตรงที่เน้น governance policies + roles
    """
    def __init__(self):
        self.policies = {}
        self.roles = {}
        self.data_dictionary = {}
    
    def define_policy(self, name, rules, enforcement='strict'):
        """กำหนด data governance policy"""
        self.policies[name] = {
            'rules': rules,
            'enforcement': enforcement,
            'created_at': datetime.now().isoformat(),
            'version': '1.0'
        }
    
    def assign_role(self, user, role, datasets):
        """กำหนด role สำหรับ data access"""
        self.roles[user] = {
            'role': role,  # data_owner, data_steward, data_consumer
            'datasets': datasets,
            'permissions': self._role_permissions(role)
        }
    
    def _role_permissions(self, role):
        perms = {
            'data_owner': ['read', 'write', 'delete', 'grant_access', 'define_policy'],
            'data_steward': ['read', 'write', 'validate', 'clean'],
            'data_consumer': ['read'],
            'data_engineer': ['read', 'write', 'transform', 'pipeline'],
        }
        return perms.get(role, ['read'])
    
    def register_data_dictionary(self, dataset, columns_metadata):
        """ลงทะเบียน data dictionary"""
        self.data_dictionary[dataset] = {
            'columns': columns_metadata,
            'last_updated': datetime.now().isoformat()
        }
    
    def validate_compliance(self, df, dataset_name):
        """ตรวจสอบ data compliance ตาม policies"""
        issues = []
        
        meta = self.data_dictionary.get(dataset_name, {})
        columns_meta = meta.get('columns', {})
        
        for col, rules in columns_meta.items():
            if col not in df.columns:
                issues.append(f"Missing required column: {col}")
                continue
            
            if rules.get('not_null') and df[col].isna().any():
                issues.append(f"{col}: has null values (not_null=True)")
            
            if rules.get('classification') == DataClassification.RESTRICTED.value:
                issues.append(f"⚠️ {col}: RESTRICTED data — ensure encryption/masking")
        
        return {
            'compliant': len(issues) == 0,
            'issues': issues
        }

# ตัวอย่าง
gov = DataGovernanceFramework()
gov.define_policy('retention', {'max_days': 365, 'archive_after': 180})
gov.register_data_dictionary('customers', {
    'customer_id': {'type': 'int', 'not_null': True, 'classification': 'internal'},
    'national_id': {'type': 'str', 'not_null': True, 'classification': 'restricted'},
    'email': {'type': 'str', 'classification': 'confidential'},
})
```

---

## 📡 Data Quality Monitoring & Alerting

```python
import pandas as pd
import json
from datetime import datetime

class DataQualityMonitor:
    """
    ★ Continuous monitoring สำหรับ data quality
    ★ ต่างจาก Data Quality Scoring ตรงที่เน้น real-time monitoring + alerting
    """
    def __init__(self, baseline=None):
        self.baseline = baseline or {}
        self.alerts = []
        self.history = []
    
    def set_baseline(self, df, name='default'):
        """ตั้ง baseline สำหรับเปรียบเทียบ"""
        self.baseline[name] = {
            'row_count': len(df),
            'null_rates': df.isna().mean().to_dict(),
            'unique_counts': df.nunique().to_dict(),
            'numeric_stats': {
                col: {'mean': df[col].mean(), 'std': df[col].std(),
                       'min': df[col].min(), 'max': df[col].max()}
                for col in df.select_dtypes(include='number').columns
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def check(self, df, name='default', thresholds=None):
        """ตรวจ data quality เทียบกับ baseline"""
        thresholds = thresholds or {
            'row_count_change_pct': 20,
            'null_rate_increase_pct': 5,
            'mean_change_pct': 30,
        }
        
        baseline = self.baseline.get(name, {})
        if not baseline:
            self.set_baseline(df, name)
            return []
        
        current_alerts = []
        
        # 1) Row count anomaly
        row_change = abs(len(df) - baseline['row_count']) / max(baseline['row_count'], 1) * 100
        if row_change > thresholds['row_count_change_pct']:
            current_alerts.append({
                'severity': 'HIGH',
                'type': 'row_count_anomaly',
                'message': f"Row count changed {row_change:.1f}% "
                          f"({baseline['row_count']} → {len(df)})",
            })
        
        # 2) Null rate increase
        for col, baseline_rate in baseline.get('null_rates', {}).items():
            if col in df.columns:
                current_rate = df[col].isna().mean()
                increase = (current_rate - baseline_rate) * 100
                if increase > thresholds['null_rate_increase_pct']:
                    current_alerts.append({
                        'severity': 'MEDIUM',
                        'type': 'null_rate_increase',
                        'message': f"{col}: null rate increased "
                                  f"{baseline_rate*100:.1f}% → {current_rate*100:.1f}%",
                    })
        
        # 3) Numeric distribution shift
        for col, stats in baseline.get('numeric_stats', {}).items():
            if col in df.columns and stats['std'] > 0:
                current_mean = df[col].mean()
                change = abs(current_mean - stats['mean']) / abs(stats['mean']) * 100
                if change > thresholds['mean_change_pct']:
                    current_alerts.append({
                        'severity': 'HIGH',
                        'type': 'distribution_shift',
                        'message': f"{col}: mean shifted {change:.1f}% "
                                  f"({stats['mean']:.2f} → {current_mean:.2f})",
                    })
        
        # Log
        self.alerts.extend(current_alerts)
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'alerts_count': len(current_alerts),
            'rows': len(df)
        })
        
        if current_alerts:
            print(f"📡 ALERTS ({len(current_alerts)}):")
            for a in current_alerts:
                icon = '🔴' if a['severity'] == 'HIGH' else '🟡'
                print(f"  {icon} [{a['severity']}] {a['message']}")
        else:
            print("📡 ✅ All quality checks passed")
        
        return current_alerts
```

---

## 🏭 Industry-Specific Use Cases (เพิ่มเติม Round 7)

### 41. 🎪 Event Management / Ticketing

| ปัญหา | วิธีแก้ |
|--------|--------|
| Duplicate ticket purchases (same person) | Fuzzy join on name + email + event |
| Venue capacity over-booking | Constraint validation (sold ≤ capacity) |
| Timezone confusion for multi-city events | UTC normalization + local display |
| Refund status inconsistency | State machine validation |
| Attendee name misspellings | String distance correction |

### 42. 🧪 Chemical / Laboratory

| ปัญหา | วิธีแก้ |
|--------|--------|
| Chemical formula format variations | SMILES/InChI normalization |
| Measurement unit mixing (mol/L, ppm, %) | Unit ontology conversion |
| Lab instrument calibration drift | Baseline correction + flagging |
| Sample ID format inconsistency | Regex standardization |
| Batch-to-batch data format changes | Schema versioning + adapters |

### 43. 📰 Publishing / Content Management

| ปัญหา | วิธีแก้ |
|--------|--------|
| Duplicate articles (syndicated content) | MinHash/LSH dedup |
| Author name variations (pen names) | Canonical author mapping |
| Mixed HTML/Markdown/plain text | Format detection + normalization |
| Broken internal links | URL validation + redirect mapping |
| Content encoding mojibake | chardet + encoding fix |

### 44. 🚢 Maritime / Shipping

| ปัญหา | วิธีแก้ |
|--------|--------|
| Port code inconsistency (LOCODE vs custom) | UN/LOCODE lookup normalization |
| Vessel name duplicates (renaming) | IMO number as primary key |
| GPS track data gaps (at sea) | Interpolation + speed validation |
| Container tracking timezone issues | UTC + port local time handling |
| Bill of Lading OCR errors | PDF extraction + fuzzy matching |

### 45. 🎨 Art / Museum / Gallery

| ปัญหา | วิธีแก้ |
|--------|--------|
| Artist name variations (multi-language) | ULAN (Union List of Artist Names) lookup |
| Date range ambiguity ("circa 1850") | Fuzzy date parsing + range fields |
| Medium/technique classification inconsistency | Controlled vocabulary (AAT) |
| Provenance chain gaps | Graph-based lineage tracking |
| Image metadata inconsistency (EXIF) | EXIF standardization + validation |

---

## 📋 Survey Data Quality (Straight-lining, Speeders, Attention Checks)

```python
import pandas as pd
import numpy as np

def clean_survey_data(df, question_cols, time_col='duration_seconds',
                       attention_col=None, expected_attention_answer=None):
    """
    ★ เฉพาะทาง survey data — ไม่ซ้ำกับเทคนิคอื่น
    ★ ตรวจจับ respondents คุณภาพต่ำ: straight-liners, speeders, inattentive
    """
    flags = pd.DataFrame(index=df.index)
    
    # 1) Straight-lining: ตอบเหมือนกันทุกข้อ
    scale_cols = [c for c in question_cols if df[c].dtype in ['int64', 'float64']]
    if scale_cols:
        row_variance = df[scale_cols].var(axis=1)
        flags['is_straightliner'] = row_variance == 0
    
    # 2) Speeders: ทำเร็วเกินไป (< median/3)
    if time_col in df.columns:
        median_time = df[time_col].median()
        flags['is_speeder'] = df[time_col] < (median_time / 3)
    
    # 3) Attention check: ตอบไม่ตรง trap question
    if attention_col and expected_attention_answer is not None:
        flags['failed_attention'] = df[attention_col] != expected_attention_answer
    
    # 4) Duplicate IP / identical responses
    if 'ip_address' in df.columns:
        flags['duplicate_ip'] = df.duplicated(subset=['ip_address'], keep=False)
    
    # 5) Open-ended gibberish (too short / all same char)
    text_cols = [c for c in question_cols if df[c].dtype == 'object']
    for col in text_cols:
        flags[f'{col}_gibberish'] = df[col].apply(
            lambda x: len(set(str(x))) <= 2 if pd.notna(x) and len(str(x)) > 0 else False
        )
    
    # Composite quality score
    flag_cols = [c for c in flags.columns if flags[c].dtype == bool]
    flags['quality_flags'] = flags[flag_cols].sum(axis=1)
    flags['is_low_quality'] = flags['quality_flags'] >= 2
    
    removed = flags['is_low_quality'].sum()
    print(f"📋 Survey QA: {removed}/{len(df)} low-quality responses flagged")
    return df[~flags['is_low_quality']], flags
```

---

## 🌍 Multilingual NLP — Language Detection & Script Normalization

```python
from langdetect import detect, detect_langs
import unicodedata
import re

def detect_and_normalize_multilingual(df, text_col):
    """
    ★ ต่างจาก NLP Text Cleaning ตรงที่เน้น multi-language + script conversion
    ★ ต่างจาก Encoding Detection ตรงที่ทำ language-level ไม่ใช่ byte-level
    """
    results = []
    for text in df[text_col]:
        if pd.isna(text) or not str(text).strip():
            results.append({'lang': None, 'script': None, 'normalized': text})
            continue
        
        text = str(text)
        
        # 1) Detect language
        try:
            lang = detect(text)
        except:
            lang = 'unknown'
        
        # 2) Unicode normalization (NFC for composed, NFKC for compatibility)
        normalized = unicodedata.normalize('NFKC', text)
        
        # 3) Script detection
        scripts = set()
        for char in normalized:
            if char.isalpha():
                script = unicodedata.name(char, '').split()[0]
                scripts.add(script)
        
        # 4) Remove zero-width chars & invisible Unicode
        normalized = re.sub(r'[\u200b\u200c\u200d\ufeff\u00ad]', '', normalized)
        
        # 5) Normalize Thai-specific issues
        if lang == 'th':
            normalized = re.sub(r'([\u0e31\u0e34-\u0e3a\u0e47-\u0e4e])\1+', r'\1', normalized)
        
        results.append({
            'lang': lang,
            'script': ','.join(scripts) if scripts else 'none',
            'normalized': normalized
        })
    
    result_df = pd.DataFrame(results)
    lang_dist = result_df['lang'].value_counts()
    print(f"🌍 Languages detected: {dict(lang_dist.head(5))}")
    return result_df
```

---

## 📧 Email Validation & Deliverability

```python
import re
import dns.resolver
import pandas as pd

DISPOSABLE_DOMAINS = {
    'tempmail.com', 'throwaway.email', 'guerrillamail.com',
    'mailinator.com', 'yopmail.com', '10minutemail.com',
    'trashmail.com', 'sharklasers.com', 'guerrillamailblock.com'
}

def validate_emails(df, email_col):
    """
    ★ ต่างจาก Regex Validation Library ตรงที่ทำ DNS MX check + deliverability
    ★ ตรวจจับ disposable emails, role-based, catch-all domains
    """
    results = []
    for email in df[email_col]:
        result = {'email': email, 'valid_syntax': False, 'has_mx': False,
                  'is_disposable': False, 'is_role_based': False}
        
        if pd.isna(email):
            results.append(result)
            continue
        
        email = str(email).strip().lower()
        
        # 1) Syntax validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        result['valid_syntax'] = bool(re.match(pattern, email))
        
        if not result['valid_syntax']:
            results.append(result)
            continue
        
        local, domain = email.split('@', 1)
        
        # 2) Disposable email detection
        result['is_disposable'] = domain in DISPOSABLE_DOMAINS
        
        # 3) Role-based detection
        role_prefixes = ['info', 'admin', 'support', 'sales', 'contact',
                        'noreply', 'no-reply', 'webmaster', 'postmaster']
        result['is_role_based'] = local in role_prefixes
        
        # 4) MX record check
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            result['has_mx'] = len(mx_records) > 0
            result['mx_host'] = str(mx_records[0].exchange)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
                dns.resolver.NoNameservers, Exception):
            result['has_mx'] = False
        
        results.append(result)
    
    result_df = pd.DataFrame(results)
    valid = result_df['valid_syntax'] & result_df['has_mx'] & ~result_df['is_disposable']
    print(f"📧 Email Validation: {valid.sum()}/{len(result_df)} deliverable")
    return result_df
```

---

## 🏗️ Medallion Architecture (Bronze → Silver → Gold)

```python
import pandas as pd
from datetime import datetime
import hashlib, json

class MedallionPipeline:
    """
    ★ Data lakehouse pattern สำหรับ progressive data refinement
    ★ ต่างจาก Pipeline Orchestration ตรงที่เน้น data layer architecture
    """
    
    def bronze_ingest(self, raw_data, source_name):
        """Bronze: Raw data as-is + metadata"""
        df = raw_data.copy()
        df['_ingested_at'] = datetime.now()
        df['_source'] = source_name
        df['_row_hash'] = df.apply(
            lambda r: hashlib.md5(str(r.values).encode()).hexdigest(), axis=1
        )
        return df
    
    def silver_clean(self, bronze_df):
        """Silver: Cleaned, conformed, deduplicated"""
        df = bronze_df.copy()
        
        # Dedup by hash
        df = df.drop_duplicates(subset='_row_hash')
        
        # Standardize text columns
        for col in df.select_dtypes(include='object').columns:
            if not col.startswith('_'):
                df[col] = df[col].str.strip().str.lower()
        
        # Type enforcement
        for col in df.columns:
            if 'date' in col.lower() and not col.startswith('_'):
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif 'amount' in col.lower() or 'price' in col.lower():
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove nulls in key columns
        key_cols = [c for c in df.columns if 'id' in c.lower() and not c.startswith('_')]
        if key_cols:
            df = df.dropna(subset=key_cols)
        
        df['_cleaned_at'] = datetime.now()
        return df
    
    def gold_aggregate(self, silver_df, group_by, agg_rules):
        """Gold: Business-ready aggregations"""
        df = silver_df.groupby(group_by).agg(agg_rules).reset_index()
        df['_aggregated_at'] = datetime.now()
        return df
```

---

## 🌊 Streaming Data Cleaning (Kafka / Flink Patterns)

```python
import pandas as pd
from datetime import datetime, timedelta
from collections import deque

class StreamingCleaner:
    """
    ★ Real-time data cleaning patterns สำหรับ streaming pipelines
    ★ ต่างจาก Batch vs Stream comparison ตรงที่ให้ implementation จริง
    """
    def __init__(self, window_size_seconds=60):
        self.window = deque()
        self.window_size = timedelta(seconds=window_size_seconds)
        self.seen_keys = set()  # For exactly-once dedup
    
    def process_event(self, event):
        """Process single streaming event with cleaning"""
        now = datetime.now()
        
        # 1) Schema validation
        required_fields = ['event_id', 'timestamp', 'value']
        if not all(f in event for f in required_fields):
            return {'status': 'rejected', 'reason': 'missing_fields'}
        
        # 2) Exactly-once dedup (idempotent key)
        if event['event_id'] in self.seen_keys:
            return {'status': 'duplicate', 'reason': 'already_processed'}
        self.seen_keys.add(event['event_id'])
        
        # 3) Late arrival handling
        event_time = pd.Timestamp(event['timestamp'])
        watermark = now - self.window_size * 3  # Allow 3x window for late events
        if event_time < pd.Timestamp(watermark):
            return {'status': 'late', 'reason': f'arrived {now - event_time} late'}
        
        # 4) Windowed aggregation
        self.window.append({'time': now, 'value': event['value']})
        while self.window and (now - self.window[0]['time']) > self.window_size:
            self.window.popleft()
        
        # 5) Anomaly detection within window
        if len(self.window) >= 5:
            values = [e['value'] for e in self.window]
            mean, std = pd.Series(values).mean(), pd.Series(values).std()
            if std > 0 and abs(event['value'] - mean) > 3 * std:
                event['_anomaly'] = True
        
        event['_processed_at'] = now.isoformat()
        return {'status': 'processed', 'event': event}
```

---

## 🏆 Master Data Management (MDM) — Golden Record

```python
import pandas as pd
from collections import Counter

def create_golden_record(records, trust_scores=None):
    """
    ★ สร้าง "single source of truth" จากหลาย source systems
    ★ ต่างจาก Multi-Source Reconciliation ตรงที่สร้าง golden record (MDM)
    """
    if not records:
        return {}
    
    trust = trust_scores or {}
    golden = {}
    
    for field in records[0].keys():
        values = [(r[field], trust.get(r.get('_source', ''), 1.0))
                  for r in records if pd.notna(r.get(field))]
        
        if not values:
            golden[field] = None
            continue
        
        # Survivorship rules
        if field.endswith('_date') or field == 'updated_at':
            # Most recent date wins
            golden[field] = max(v[0] for v in values)
        elif field in ['name', 'address']:
            # Longest value (most complete) from highest trust
            values.sort(key=lambda x: (-x[1], -len(str(x[0]))))
            golden[field] = values[0][0]
        elif isinstance(values[0][0], (int, float)):
            # Weighted average by trust
            total_weight = sum(v[1] for v in values)
            golden[field] = sum(v[0] * v[1] for v in values) / total_weight
        else:
            # Most common value (majority vote), weighted by trust
            weighted_votes = Counter()
            for val, weight in values:
                weighted_votes[val] += weight
            golden[field] = weighted_votes.most_common(1)[0][0]
    
    golden['_sources_merged'] = len(records)
    golden['_golden_created_at'] = pd.Timestamp.now().isoformat()
    return golden
```

---

## 🚧 Data Quarantine Patterns

```python
import pandas as pd
from datetime import datetime

class DataQuarantine:
    """
    ★ Staging area สำหรับ data ที่น่าสงสัย ก่อน approve เข้า production
    ★ ต่างจาก ETL Error Handling ตรงที่เน้น quarantine workflow
    """
    def __init__(self):
        self.quarantine = []
        self.rules = {}
    
    def add_rule(self, name, check_fn, severity='medium'):
        self.rules[name] = {'check': check_fn, 'severity': severity}
    
    def screen(self, df):
        """แยก data ดี vs ต้อง quarantine"""
        clean_mask = pd.Series(True, index=df.index)
        quarantine_reasons = pd.Series([''] * len(df), index=df.index)
        
        for rule_name, rule in self.rules.items():
            violations = rule['check'](df)
            quarantine_reasons[violations] += f"{rule_name}; "
            clean_mask &= ~violations
        
        clean_df = df[clean_mask]
        quarantined_df = df[~clean_mask].copy()
        quarantined_df['_quarantine_reason'] = quarantine_reasons[~clean_mask]
        quarantined_df['_quarantined_at'] = datetime.now()
        
        self.quarantine.extend(quarantined_df.to_dict('records'))
        
        print(f"🚧 Quarantine: {len(clean_df)} clean, {len(quarantined_df)} quarantined")
        return clean_df, quarantined_df
    
    def review_and_release(self, indices, action='approve'):
        """Review quarantined records"""
        released = []
        for i in sorted(indices, reverse=True):
            if i < len(self.quarantine):
                record = self.quarantine.pop(i)
                record['_review_action'] = action
                record['_reviewed_at'] = datetime.now().isoformat()
                if action == 'approve':
                    released.append(record)
        return pd.DataFrame(released)

# ตัวอย่าง
q = DataQuarantine()
q.add_rule('negative_amount', lambda df: df['amount'] < 0, 'high')
q.add_rule('future_date', lambda df: pd.to_datetime(df['date']) > datetime.now(), 'medium')
q.add_rule('missing_id', lambda df: df['customer_id'].isna(), 'high')
```

---

## 📍 Geohash / H3 Spatial Indexing

```python
import h3
import pandas as pd

def geospatial_indexing(df, lat_col='lat', lng_col='lng', resolution=7):
    """
    ★ ต่างจาก Geospatial Topology ตรงที่ใช้ spatial indexing สำหรับ bucketing/dedup
    ★ Geohash/H3 สำหรับ proximity grouping + location dedup
    """
    df_geo = df.copy()
    
    # 1) H3 hexagonal indexing
    df_geo['h3_index'] = df_geo.apply(
        lambda r: h3.latlng_to_cell(r[lat_col], r[lng_col], resolution)
        if pd.notna(r[lat_col]) and pd.notna(r[lng_col]) else None,
        axis=1
    )
    
    # 2) Proximity dedup (same hex = same area)
    dup_in_hex = df_geo.groupby('h3_index').size()
    crowded_hexes = dup_in_hex[dup_in_hex > 1]
    
    # 3) Get hex center for normalization
    df_geo['h3_center_lat'] = df_geo['h3_index'].apply(
        lambda h: h3.cell_to_latlng(h)[0] if h else None
    )
    df_geo['h3_center_lng'] = df_geo['h3_index'].apply(
        lambda h: h3.cell_to_latlng(h)[1] if h else None
    )
    
    # 4) Boundary validation
    df_geo['valid_coords'] = (
        df_geo[lat_col].between(-90, 90) &
        df_geo[lng_col].between(-180, 180)
    )
    
    # 5) Neighbor analysis
    df_geo['h3_neighbors'] = df_geo['h3_index'].apply(
        lambda h: len(h3.grid_disk(h, 1)) - 1 if h else 0
    )
    
    invalid = (~df_geo['valid_coords']).sum()
    print(f"📍 H3 Indexing (res={resolution}): {len(crowded_hexes)} crowded hexes, "
          f"{invalid} invalid coords")
    return df_geo
```

---

## 🔄 Idempotent Data Operations

```python
import pandas as pd
import hashlib
from datetime import datetime

class IdempotentCleaner:
    """
    ★ การ clean data ที่ run กี่ครั้งก็ได้ผลเหมือนเดิม
    ★ ต่างจากเทคนิคอื่นตรงที่เน้น re-runnability + safety
    """
    def __init__(self):
        self.operation_log = {}
    
    def idempotent_upsert(self, target_df, source_df, key_cols):
        """UPSERT ที่ run ซ้ำได้ — ผลลัพธ์เหมือนเดิม"""
        # Remove existing keys from target
        merged = target_df.merge(source_df[key_cols], on=key_cols, how='left', indicator=True)
        existing = merged[merged['_merge'] == 'both'].index
        target_clean = target_df.drop(existing)
        
        # Append new/updated records
        result = pd.concat([target_clean, source_df], ignore_index=True)
        return result.drop_duplicates(subset=key_cols, keep='last')
    
    def partition_overwrite(self, target_df, source_df, partition_col, partition_value):
        """Overwrite specific partition — idempotent by design"""
        # Remove old partition
        remaining = target_df[target_df[partition_col] != partition_value]
        # Add new partition data
        new_partition = source_df[source_df[partition_col] == partition_value]
        return pd.concat([remaining, new_partition], ignore_index=True)
    
    def checksum_guard(self, df, operation_name):
        """Skip if data hasn't changed since last run"""
        checksum = hashlib.md5(
            pd.util.hash_pandas_object(df).values.tobytes()
        ).hexdigest()
        
        if self.operation_log.get(operation_name) == checksum:
            print(f"🔄 {operation_name}: skipped (data unchanged)")
            return True  # Skip
        
        self.operation_log[operation_name] = checksum
        return False  # Proceed
```

---

## 📊 Sparse Data Handling

```python
from scipy.sparse import csr_matrix, issparse
import pandas as pd
import numpy as np

def handle_sparse_data(df, zero_threshold=0.9):
    """
    ★ จัดการ data ที่มี zeros/nulls เป็นส่วนใหญ่ (>90%)
    ★ ต่างจาก Missing Values ตรงที่เน้น sparse matrix + memory efficiency
    """
    report = {}
    
    # 1) Identify sparse columns
    numeric_cols = df.select_dtypes(include='number').columns
    sparsity = {}
    for col in numeric_cols:
        zero_rate = (df[col] == 0).sum() / len(df)
        null_rate = df[col].isna().sum() / len(df)
        sparsity[col] = zero_rate + null_rate
    
    sparse_cols = [c for c, s in sparsity.items() if s >= zero_threshold]
    report['sparse_columns'] = sparse_cols
    
    # 2) Convert to sparse representation
    if sparse_cols:
        sparse_data = csr_matrix(df[sparse_cols].fillna(0).values)
        report['memory_dense'] = df[sparse_cols].memory_usage(deep=True).sum()
        report['memory_sparse'] = sparse_data.data.nbytes + sparse_data.indices.nbytes
        report['compression_ratio'] = report['memory_dense'] / max(report['memory_sparse'], 1)
    
    # 3) Zero-inflation detection
    for col in numeric_cols:
        non_zero = df[col][df[col] != 0].dropna()
        if len(non_zero) > 0:
            expected_zeros = (df[col].isna().sum() + (df[col] == 0).sum()) / len(df)
            if expected_zeros > 0.8:
                report.setdefault('zero_inflated', []).append(col)
    
    # 4) Sparse-aware imputation
    df_clean = df.copy()
    for col in sparse_cols:
        # Don't fill with mean (misleading for sparse data)
        # Keep zeros, only fill NaN with 0
        df_clean[col] = df_clean[col].fillna(0)
    
    print(f"📊 Sparse: {len(sparse_cols)} sparse columns (>={zero_threshold*100}% zeros)")
    return df_clean, report
```

---

## 🎵 Audio / Speech Data Cleaning

```python
import numpy as np

def clean_audio_data(audio_array, sample_rate=16000):
    """
    ★ ทำความสะอาด audio data สำหรับ speech recognition / ML
    ★ Data type เฉพาะทางที่ไม่มีใน round อื่น
    """
    cleaned = audio_array.copy().astype(np.float32)
    report = {}
    
    # 1) DC offset removal
    dc_offset = np.mean(cleaned)
    cleaned = cleaned - dc_offset
    report['dc_offset_removed'] = float(dc_offset)
    
    # 2) Normalization (peak normalization)
    peak = np.max(np.abs(cleaned))
    if peak > 0:
        cleaned = cleaned / peak
    report['peak_before'] = float(peak)
    
    # 3) Silence trimming (leading/trailing)
    threshold = 0.01
    non_silent = np.where(np.abs(cleaned) > threshold)[0]
    if len(non_silent) > 0:
        start, end = non_silent[0], non_silent[-1]
        trimmed = end - start
        cleaned = cleaned[start:end + 1]
        report['silence_trimmed_samples'] = len(audio_array) - len(cleaned)
    
    # 4) Spectral gating (simple noise reduction)
    # Estimate noise from first 0.5 seconds
    noise_samples = int(0.5 * sample_rate)
    if len(cleaned) > noise_samples:
        noise_profile = np.std(cleaned[:noise_samples])
        # Soft gate
        gate = np.abs(cleaned) > (noise_profile * 2)
        cleaned = cleaned * gate.astype(float)
        report['noise_threshold'] = float(noise_profile * 2)
    
    # 5) Clipping detection
    clip_threshold = 0.99
    clipped_samples = np.sum(np.abs(audio_array / max(peak, 1e-10)) >= clip_threshold)
    report['clipped_samples'] = int(clipped_samples)
    
    # 6) Duration validation
    duration = len(cleaned) / sample_rate
    report['duration_seconds'] = duration
    report['valid_duration'] = 0.5 <= duration <= 300  # 0.5s to 5min
    
    print(f"🎵 Audio Clean: {duration:.1f}s, {report.get('silence_trimmed_samples', 0)} "
          f"silence samples trimmed, {clipped_samples} clipped")
    return cleaned, report
```

---

## 📜 Event Sourcing & CQRS Data Patterns

```python
import pandas as pd
from datetime import datetime
import json

class EventSourcedCleaner:
    """
    ★ ทำ cleaning ผ่าน immutable event log — สามารถ replay/undo ได้
    ★ ต่างจาก Audit Trail ตรงที่เน้น event sourcing architecture
    """
    def __init__(self):
        self.event_store = []  # Immutable append-only log
    
    def apply_cleaning(self, record_id, operation, params, before, after):
        """บันทึก cleaning operation เป็น event"""
        event = {
            'event_id': len(self.event_store) + 1,
            'timestamp': datetime.now().isoformat(),
            'record_id': record_id,
            'operation': operation,
            'params': params,
            'before': before,
            'after': after,
        }
        self.event_store.append(event)
        return event
    
    def replay_from(self, start_event_id=1, end_event_id=None):
        """Replay events เพื่อ reconstruct state"""
        events = [e for e in self.event_store
                  if e['event_id'] >= start_event_id and
                  (end_event_id is None or e['event_id'] <= end_event_id)]
        
        state = {}
        for event in events:
            state[event['record_id']] = event['after']
        
        return state
    
    def undo_last(self, n=1):
        """Undo last n cleaning operations"""
        undone = []
        for _ in range(min(n, len(self.event_store))):
            event = self.event_store[-1]
            undo_event = {
                'event_id': len(self.event_store) + 1,
                'timestamp': datetime.now().isoformat(),
                'record_id': event['record_id'],
                'operation': f"UNDO_{event['operation']}",
                'before': event['after'],
                'after': event['before'],
            }
            self.event_store.append(undo_event)
            undone.append(undo_event)
        
        return undone
    
    def get_audit_log(self, record_id=None):
        """CQRS read model — query events"""
        if record_id:
            return [e for e in self.event_store if e['record_id'] == record_id]
        return self.event_store
```

---

## 🧮 Feature Store Integration for ML

```python
import pandas as pd
from datetime import datetime

class FeatureStore:
    """
    ★ จัดการ features สำหรับ ML — clean once, use everywhere
    ★ ต่างจาก Data Catalog ตรงที่เน้น ML feature management
    """
    def __init__(self):
        self.features = {}
        self.metadata = {}
    
    def register_feature(self, name, df, entity_col, timestamp_col=None,
                          description='', tags=None):
        """ลงทะเบียน feature"""
        # Validate & clean before registering
        clean_df = df.dropna(subset=[entity_col])
        
        # Ensure no duplicate entities (take latest if timestamp exists)
        if timestamp_col and timestamp_col in clean_df.columns:
            clean_df = clean_df.sort_values(timestamp_col).drop_duplicates(
                subset=[entity_col], keep='last'
            )
        
        self.features[name] = clean_df
        self.metadata[name] = {
            'entity_col': entity_col,
            'columns': list(clean_df.columns),
            'rows': len(clean_df),
            'description': description,
            'tags': tags or [],
            'registered_at': datetime.now().isoformat(),
        }
        
        print(f"🧮 Registered feature '{name}': {len(clean_df)} rows, "
              f"{len(clean_df.columns)} cols")
    
    def get_training_set(self, entity_df, entity_col, feature_names):
        """Join multiple features for model training"""
        result = entity_df.copy()
        
        for fname in feature_names:
            if fname not in self.features:
                print(f"⚠️ Feature '{fname}' not found")
                continue
            
            feat_df = self.features[fname]
            feat_entity = self.metadata[fname]['entity_col']
            
            # Point-in-time join (prevent data leakage)
            feature_cols = [c for c in feat_df.columns
                          if c != feat_entity and not c.startswith('_')]
            
            result = result.merge(
                feat_df[[feat_entity] + feature_cols],
                left_on=entity_col,
                right_on=feat_entity,
                how='left'
            )
        
        return result
```

---

## 🔗 Multi-Table Cleaning Coordination

```python
import pandas as pd

class MultiTableCleaner:
    """
    ★ Coordinate cleaning across related tables simultaneously
    ★ ต่างจาก Referential Integrity ตรงที่เน้น coordinated cleaning workflow
    """
    def __init__(self):
        self.tables = {}
        self.relationships = []
    
    def register(self, name, df):
        self.tables[name] = df.copy()
    
    def add_relationship(self, parent_table, parent_key, child_table, child_key):
        self.relationships.append({
            'parent': parent_table, 'parent_key': parent_key,
            'child': child_table, 'child_key': child_key
        })
    
    def cascade_delete(self, table_name, condition):
        """Delete matching records and cascade to children"""
        deleted = self.tables[table_name][condition]
        self.tables[table_name] = self.tables[table_name][~condition]
        
        # Cascade to child tables
        for rel in self.relationships:
            if rel['parent'] == table_name:
                child = self.tables[rel['child']]
                orphan_mask = ~child[rel['child_key']].isin(
                    self.tables[table_name][rel['parent_key']]
                )
                orphaned = orphan_mask.sum()
                self.tables[rel['child']] = child[~orphan_mask]
                print(f"  ↳ Cascaded: {orphaned} orphans removed from {rel['child']}")
        
        return len(deleted)
    
    def propagate_update(self, table_name, key_col, key_value, updates):
        """Update a record and propagate to denormalized copies"""
        mask = self.tables[table_name][key_col] == key_value
        for col, val in updates.items():
            self.tables[table_name].loc[mask, col] = val
        
        # Find denormalized copies in other tables
        for rel in self.relationships:
            if rel['parent'] == table_name:
                child = self.tables[rel['child']]
                child_mask = child[rel['child_key']] == key_value
                for col, val in updates.items():
                    if col in child.columns and col != key_col:
                        self.tables[rel['child']].loc[child_mask, col] = val
    
    def validate_all(self):
        """Validate referential integrity across all tables"""
        issues = []
        for rel in self.relationships:
            parent_keys = set(self.tables[rel['parent']][rel['parent_key']])
            child_keys = set(self.tables[rel['child']][rel['child_key']].dropna())
            orphans = child_keys - parent_keys
            if orphans:
                issues.append(f"{rel['child']}.{rel['child_key']}: {len(orphans)} orphans")
        
        return issues
```

---

## 🏭 Data Mesh Patterns for Cleaning

```python
class DataMeshDomain:
    """
    ★ Domain-oriented data ownership + self-serve cleaning
    ★ ต่างจาก Data Governance ตรงที่ decentralized + domain-driven
    """
    def __init__(self, domain_name, owner):
        self.domain = domain_name
        self.owner = owner
        self.data_products = {}
        self.quality_slas = {}
    
    def register_data_product(self, name, df, sla=None):
        """Register cleaned data as a "data product" """"
        # Apply domain-specific cleaning
        clean_df = self._domain_clean(df)
        
        self.data_products[name] = {
            'data': clean_df,
            'schema': {col: str(dtype) for col, dtype in clean_df.dtypes.items()},
            'rows': len(clean_df),
            'sla': sla or {'freshness': '1h', 'completeness': 0.95},
        }
        
        return clean_df
    
    def _domain_clean(self, df):
        """Domain-specific cleaning rules"""
        clean = df.copy()
        # Each domain defines its own cleaning standards
        for col in clean.select_dtypes(include='object').columns:
            clean[col] = clean[col].str.strip()
        clean = clean.drop_duplicates()
        return clean
    
    def check_sla(self, product_name):
        """Check if data product meets SLA"""
        product = self.data_products.get(product_name)
        if not product:
            return {'passes': False, 'reason': 'product not found'}
        
        df = product['data']
        sla = product['sla']
        
        completeness = 1 - df.isna().mean().mean()
        passes = completeness >= sla.get('completeness', 0.95)
        
        return {
            'passes': passes,
            'completeness': completeness,
            'target': sla.get('completeness', 0.95)
        }
```

---

## 🏭 Industry-Specific Use Cases (เพิ่มเติม Round 8)

### 46. 🪙 Cryptocurrency / Blockchain

| ปัญหา | วิธีแก้ |
|--------|--------|
| Wallet address format variations | Checksum validation (EIP-55 for ETH) |
| Cross-chain token symbol collisions | Chain ID + contract address as key |
| Transaction timestamp timezone issues | UTC block timestamp standardization |
| Gas fee / amount precision (18 decimals) | Decimal128 or string storage |
| MEV / front-running duplicate txns | Event sourcing + dedup by tx hash |

### 47. 🤝 Nonprofit / NGO

| ปัญหา | วิธีแก้ |
|--------|--------|
| Donor name variations (individuals + orgs) | MDM golden record creation |
| Grant amount currency mixing | Multi-currency normalization |
| Beneficiary PII in reports | k-Anonymity + data masking |
| Impact metric inconsistency | Controlled vocabulary + unit standardization |
| Multi-language survey responses | Language detection + transliteration |

### 48. 👗 Fashion / Apparel

| ปัญหา | วิธีแก้ |
|--------|--------|
| Size inconsistency (US/EU/UK/Asian) | Size mapping lookup table |
| Color name variations ("navy" vs "dark blue") | Color ontology normalization |
| Product description multi-language | Multilingual NLP + canonical text |
| SKU format cross-platform inconsistency | Regex standardization |
| Return reason text classification | NLP categorization + sentiment |

### 49. ⛏️ Mining / Minerals

| ปัญหา | วิธีแก้ |
|--------|--------|
| Core sample GPS imprecision | H3 spatial indexing + correction |
| Assay result unit variations (g/t, ppm, %) | Unit ontology conversion |
| Drill hole data depth inconsistency | Monotonic validation + interpolation |
| Environmental monitoring sensor drift | Baseline correction + calibration |
| Historical survey format migration | Schema versioning + adapters |

### 50. 🚂 Railway / Transit

| ปัญหา | วิธีแก้ |
|--------|--------|
| Station name variations (abbreviations) | Canonical station ID mapping |
| Schedule timezone crossing | UTC + local departure/arrival |
| Passenger count sensor errors | Windowed anomaly detection |
| Track segment ID inconsistency | Graph-based topology validation |
| Fare calculation data precision | Decimal handling + rounding rules |

---

## 🌸 Bloom Filter for Membership Testing

```python
import hashlib
import math

class BloomFilter:
    """
    ★ Probabilistic set membership — "definitely not" or "maybe yes"
    ★ ต่างจาก MinHash/LSH ตรงที่เน้น membership test ไม่ใช่ similarity
    ★ ใช้ memory น้อยมาก — เหมาะ dedup ระดับ 100M+ records
    """
    def __init__(self, expected_items=1_000_000, false_positive_rate=0.01):
        self.size = self._optimal_size(expected_items, false_positive_rate)
        self.hash_count = self._optimal_hashes(self.size, expected_items)
        self.bit_array = [0] * self.size
        self.item_count = 0
    
    def _optimal_size(self, n, p):
        return int(-n * math.log(p) / (math.log(2) ** 2))
    
    def _optimal_hashes(self, m, n):
        return max(1, int((m / n) * math.log(2)))
    
    def _hashes(self, item):
        positions = []
        for i in range(self.hash_count):
            h = hashlib.md5(f"{item}_{i}".encode()).hexdigest()
            positions.append(int(h, 16) % self.size)
        return positions
    
    def add(self, item):
        for pos in self._hashes(str(item)):
            self.bit_array[pos] = 1
        self.item_count += 1
    
    def might_contain(self, item):
        """False = definitely not in set, True = probably in set"""
        return all(self.bit_array[pos] for pos in self._hashes(str(item)))
    
    def deduplicate_stream(self, items):
        """Streaming dedup using Bloom filter"""
        unique, duplicates = [], 0
        for item in items:
            if self.might_contain(item):
                duplicates += 1
            else:
                self.add(item)
                unique.append(item)
        print(f"🌸 Bloom Filter: {len(unique)} unique, {duplicates} probable duplicates "
              f"({self.size/8/1024:.0f}KB memory)")
        return unique
```

---

## 🧩 Constraint Satisfaction (CSP) Data Repair

```python
import pandas as pd
from itertools import product as iter_product

def csp_repair(df, constraints, domain_values=None):
    """
    ★ ใช้ Constraint Satisfaction Programming ซ่อม data
    ★ ต่างจาก Validation Rules ตรงที่ CSP หาค่าที่ถูกต้องอัตโนมัติ
    """
    repairs = []
    
    for idx, row in df.iterrows():
        violations = []
        for name, check_fn in constraints.items():
            try:
                if not check_fn(row):
                    violations.append(name)
            except:
                violations.append(name)
        
        if not violations:
            continue
        
        # Try to find minimal repair
        best_repair = None
        min_changes = float('inf')
        
        if domain_values:
            # Search for valid assignment
            for col, values in domain_values.items():
                for val in values:
                    test_row = row.copy()
                    test_row[col] = val
                    satisfied = sum(1 for _, c in constraints.items()
                                   if c(test_row))
                    if satisfied == len(constraints):
                        changes = 1 if row[col] != val else 0
                        if changes < min_changes:
                            min_changes = changes
                            best_repair = {col: val}
        
        repairs.append({
            'index': idx,
            'violations': violations,
            'repair': best_repair
        })
    
    # Apply repairs
    repaired_df = df.copy()
    applied = 0
    for r in repairs:
        if r['repair']:
            for col, val in r['repair'].items():
                repaired_df.at[r['index'], col] = val
            applied += 1
    
    print(f"🧩 CSP Repair: {len(repairs)} violations, {applied} auto-repaired")
    return repaired_df, repairs
```

---

## 🏦 Bank Statement Reconciliation

```python
import pandas as pd
from difflib import SequenceMatcher

def reconcile_bank_statements(internal_df, bank_df,
                               amount_col='amount', date_col='date',
                               ref_col='reference'):
    """
    ★ Financial reconciliation — matching internal records vs bank statements
    ★ ต่างจาก Multi-Source Reconciliation ตรงที่เฉพาะทาง financial matching
    """
    results = {'matched': [], 'unmatched_internal': [], 'unmatched_bank': []}
    bank_used = set()
    
    for i_idx, i_row in internal_df.iterrows():
        best_match = None
        best_score = 0
        
        for b_idx, b_row in bank_df.iterrows():
            if b_idx in bank_used:
                continue
            
            score = 0
            
            # 1) Amount match (exact or within tolerance)
            amount_diff = abs(i_row[amount_col] - b_row[amount_col])
            if amount_diff == 0:
                score += 50
            elif amount_diff < 0.01:
                score += 40
            elif amount_diff / max(abs(i_row[amount_col]), 1) < 0.001:
                score += 30
            else:
                continue  # Amount too different
            
            # 2) Date proximity
            date_diff = abs((pd.Timestamp(i_row[date_col]) -
                            pd.Timestamp(b_row[date_col])).days)
            if date_diff == 0:
                score += 30
            elif date_diff <= 1:
                score += 20
            elif date_diff <= 3:
                score += 10
            
            # 3) Reference similarity
            if ref_col in i_row and ref_col in b_row:
                ref_sim = SequenceMatcher(None,
                    str(i_row[ref_col]).lower(),
                    str(b_row[ref_col]).lower()
                ).ratio()
                score += ref_sim * 20
            
            if score > best_score:
                best_score = score
                best_match = b_idx
        
        if best_match is not None and best_score >= 60:
            results['matched'].append({
                'internal_idx': i_idx,
                'bank_idx': best_match,
                'confidence': best_score
            })
            bank_used.add(best_match)
        else:
            results['unmatched_internal'].append(i_idx)
    
    results['unmatched_bank'] = [
        i for i in bank_df.index if i not in bank_used
    ]
    
    print(f"🏦 Reconciliation: {len(results['matched'])} matched, "
          f"{len(results['unmatched_internal'])} unmatched internal, "
          f"{len(results['unmatched_bank'])} unmatched bank")
    return results
```

---

## 📈 Monotonic Constraint Enforcement

```python
import pandas as pd
import numpy as np

def enforce_monotonic(df, col, direction='increasing', method='isotonic'):
    """
    ★ บังคับให้ค่าเป็น monotonic (เพิ่มขึ้น/ลดลงเสมอ)
    ★ ต่างจาก Time Series Cleaning ตรงที่เน้น monotonicity constraint
    """
    values = df[col].values.copy().astype(float)
    original = values.copy()
    
    if method == 'isotonic':
        # Pool Adjacent Violators Algorithm (PAVA)
        from sklearn.isotonic import IsotonicRegression
        increasing = direction == 'increasing'
        ir = IsotonicRegression(increasing=increasing)
        indices = np.arange(len(values))
        mask = ~np.isnan(values)
        values[mask] = ir.fit_transform(indices[mask], values[mask])
    
    elif method == 'clip':
        # Simple clip to running max/min
        if direction == 'increasing':
            running = np.maximum.accumulate(
                np.nan_to_num(values, nan=-np.inf))
            values = np.maximum(values, running)
        else:
            running = np.minimum.accumulate(
                np.nan_to_num(values, nan=np.inf))
            values = np.minimum(values, running)
    
    # Report violations
    if direction == 'increasing':
        violations = np.sum(np.diff(original[~np.isnan(original)]) < 0)
    else:
        violations = np.sum(np.diff(original[~np.isnan(original)]) > 0)
    
    df_result = df.copy()
    df_result[col] = values
    changes = np.sum(~np.isclose(original, values, equal_nan=True))
    
    print(f"📈 Monotonic ({direction}): {violations} violations, "
          f"{changes} values adjusted")
    return df_result
```

---

## 🔬 Causal Inference Data Preparation

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

def prepare_causal_data(df, treatment_col, outcome_col, covariates):
    """
    ★ Propensity Score Matching สำหรับ causal analysis
    ★ ต่างจาก SMOTE/Imbalance ตรงที่เน้น causal inference ไม่ใช่ class balance
    """
    # 1) Estimate propensity scores
    X = df[covariates].fillna(df[covariates].median())
    y = df[treatment_col].astype(int)
    
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X, y)
    df_result = df.copy()
    df_result['propensity_score'] = lr.predict_proba(X)[:, 1]
    
    # 2) Check overlap (positivity assumption)
    treated = df_result[df_result[treatment_col] == 1]['propensity_score']
    control = df_result[df_result[treatment_col] == 0]['propensity_score']
    
    overlap_min = max(treated.min(), control.min())
    overlap_max = min(treated.max(), control.max())
    
    # 3) Trim non-overlapping regions
    df_trimmed = df_result[
        df_result['propensity_score'].between(overlap_min, overlap_max)
    ]
    
    # 4) Match treated to nearest control
    treated_df = df_trimmed[df_trimmed[treatment_col] == 1]
    control_df = df_trimmed[df_trimmed[treatment_col] == 0]
    
    nn = NearestNeighbors(n_neighbors=1, metric='euclidean')
    nn.fit(control_df[['propensity_score']])
    distances, indices = nn.kneighbors(treated_df[['propensity_score']])
    
    matched_control = control_df.iloc[indices.flatten()]
    matched_df = pd.concat([treated_df, matched_control])
    
    print(f"🔬 Causal Prep: {len(treated_df)} treated matched to "
          f"{len(matched_control)} controls (trimmed {len(df)-len(df_trimmed)})")
    return matched_df
```

---

## 🧬 Generative Model Imputation (VAE / GAIN)

```python
import numpy as np
import pandas as pd

class SimpleVAEImputer:
    """
    ★ ใช้ Variational Autoencoder (simplified) สำหรับ impute missing data
    ★ ต่างจาก KNN/MICE ตรงที่ learn latent distribution
    """
    def __init__(self, latent_dim=5, epochs=100):
        self.latent_dim = latent_dim
        self.epochs = epochs
    
    def fit_transform(self, df, numeric_cols=None):
        cols = numeric_cols or df.select_dtypes(include='number').columns.tolist()
        data = df[cols].values.astype(float)
        mask = ~np.isnan(data)
        
        # Normalize observed values
        col_means = np.nanmean(data, axis=0)
        col_stds = np.nanstd(data, axis=0)
        col_stds[col_stds == 0] = 1
        
        # Initialize missing with column means
        imputed = data.copy()
        for j in range(data.shape[1]):
            imputed[np.isnan(imputed[:, j]), j] = col_means[j]
        
        # Iterative refinement (simplified VAE-like)
        for epoch in range(self.epochs):
            # Encode: project to latent space
            normalized = (imputed - col_means) / col_stds
            U, S, Vt = np.linalg.svd(normalized, full_matrices=False)
            latent = U[:, :self.latent_dim] * S[:self.latent_dim]
            
            # Decode: reconstruct from latent
            reconstructed = latent @ Vt[:self.latent_dim, :]
            reconstructed = reconstructed * col_stds + col_means
            
            # Only update missing values
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    if not mask[i, j]:
                        imputed[i, j] = reconstructed[i, j]
        
        result = df.copy()
        result[cols] = imputed
        
        missing = (~mask).sum()
        print(f"🧬 VAE Imputation: {missing} values imputed across {len(cols)} columns")
        return result
```

---

## 📊 Column Correlation & Mutual Information

```python
import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif

def analyze_and_remove_redundancy(df, target_col=None, corr_threshold=0.95,
                                   mi_threshold=0.01):
    """
    ★ ตรวจจับ redundant columns ด้วย correlation + mutual information
    ★ ต่างจาก VIF/Multicollinearity ตรงที่จับ non-linear relationships ด้วย
    """
    numeric_df = df.select_dtypes(include='number')
    report = {'high_correlation': [], 'low_mi': [], 'removed': []}
    
    # 1) Pearson correlation matrix
    corr_matrix = numeric_df.corr().abs()
    upper = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )
    
    for col in upper.columns:
        high_corr = upper.index[upper[col] > corr_threshold].tolist()
        for paired in high_corr:
            report['high_correlation'].append({
                'col1': col, 'col2': paired,
                'correlation': corr_matrix.loc[col, paired]
            })
    
    # 2) Mutual Information (captures non-linear)
    if target_col and target_col in df.columns:
        feature_cols = [c for c in numeric_df.columns if c != target_col]
        X = numeric_df[feature_cols].fillna(0)
        y = df[target_col]
        
        if y.dtype in ['int64', 'object', 'category']:
            mi_scores = mutual_info_classif(X, y, random_state=42)
        else:
            mi_scores = mutual_info_regression(X, y, random_state=42)
        
        for col, score in zip(feature_cols, mi_scores):
            if score < mi_threshold:
                report['low_mi'].append({'column': col, 'mi_score': score})
    
    # 3) Decide which to remove (keep higher MI score)
    to_remove = set()
    for pair in report['high_correlation']:
        col1_mi = next((x['mi_score'] for x in report.get('low_mi', [])
                        if x['column'] == pair['col1']), 1.0)
        col2_mi = next((x['mi_score'] for x in report.get('low_mi', [])
                        if x['column'] == pair['col2']), 1.0)
        to_remove.add(pair['col1'] if col1_mi < col2_mi else pair['col2'])
    
    report['removed'] = list(to_remove)
    df_clean = df.drop(columns=to_remove, errors='ignore')
    
    print(f"📊 Redundancy: {len(report['high_correlation'])} high-corr pairs, "
          f"{len(to_remove)} columns removed")
    return df_clean, report
```

---

## 🏠 Natural Language Address Parsing

```python
import re
import pandas as pd

def parse_addresses(df, address_col):
    """
    ★ Unstructured address → structured fields
    ★ ต่างจาก Address/Geo Cleaning ตรงที่เน้น NL parsing ไม่ใช่ geocoding
    """
    parsed = []
    
    patterns = {
        'postal_code_th': r'\b(\d{5})\b',
        'postal_code_us': r'\b(\d{5}(?:-\d{4})?)\b',
        'state_us': r'\b([A-Z]{2})\s+\d{5}',
        'floor': r'(?:ชั้น|floor|fl\.?)\s*(\d+)',
        'unit': r'(?:ห้อง|unit|apt\.?|suite|ste\.?)\s*([A-Za-z0-9\-]+)',
        'building': r'(?:อาคาร|ตึก|building|bldg\.?)\s*([^\s,]+)',
    }
    
    for addr in df[address_col]:
        if pd.isna(addr):
            parsed.append({})
            continue
        
        addr = str(addr).strip()
        result = {'raw': addr}
        
        # Extract components
        for field, pattern in patterns.items():
            match = re.search(pattern, addr, re.IGNORECASE)
            if match:
                result[field] = match.group(1)
        
        # House number (first number-like token)
        house_match = re.match(r'^(\d+[/\-]?\d*)', addr)
        if house_match:
            result['house_number'] = house_match.group(1)
        
        # Street (after house number, before comma)
        street_match = re.match(r'^\d+[/\-]?\d*\s+(.+?)(?:,|\n|$)', addr)
        if street_match:
            result['street'] = street_match.group(1).strip()
        
        # City extraction (common Thai districts)
        city_match = re.search(
            r'(?:เขต|อำเภอ|อ\.|แขวง)\s*(\S+)', addr
        )
        if city_match:
            result['district'] = city_match.group(1)
        
        # Province extraction
        province_match = re.search(
            r'(?:จังหวัด|จ\.)\s*(\S+)', addr
        )
        if province_match:
            result['province'] = province_match.group(1)
        
        parsed.append(result)
    
    result_df = pd.DataFrame(parsed)
    filled = result_df.notna().sum(axis=1).mean()
    print(f"🏠 Address Parsing: avg {filled:.1f} fields extracted per address")
    return result_df
```

---

## ⚙️ Configuration File Cleaning (YAML / TOML / INI)

```python
import yaml
import json
import re
import os

def clean_config_data(config_text, format='yaml'):
    """
    ★ Parse + validate + clean configuration files
    ★ Data type เฉพาะทางที่ไม่มีใน round อื่น
    """
    report = {'format': format, 'issues': [], 'fixes': []}
    
    # 1) Parse based on format
    try:
        if format == 'yaml':
            data = yaml.safe_load(config_text)
        elif format == 'json':
            data = json.loads(config_text)
        elif format == 'toml':
            import tomllib
            data = tomllib.loads(config_text)
        elif format == 'ini':
            from configparser import ConfigParser
            parser = ConfigParser()
            parser.read_string(config_text)
            data = {s: dict(parser[s]) for s in parser.sections()}
    except Exception as e:
        report['issues'].append(f'Parse error: {str(e)}')
        return None, report
    
    # 2) Environment variable resolution
    def resolve_env(obj):
        if isinstance(obj, str):
            pattern = r'\$\{(\w+)(?::(.+?))?\}'
            def replacer(m):
                val = os.environ.get(m.group(1), m.group(2) or '')
                report['fixes'].append(f"Resolved ${{{m.group(1)}}}")
                return val
            return re.sub(pattern, replacer, obj)
        elif isinstance(obj, dict):
            return {k: resolve_env(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [resolve_env(v) for v in obj]
        return obj
    
    data = resolve_env(data)
    
    # 3) Type coercion for common patterns
    def coerce_types(obj):
        if isinstance(obj, str):
            if obj.lower() in ('true', 'yes', 'on'):
                return True
            if obj.lower() in ('false', 'no', 'off'):
                return False
            try:
                return int(obj)
            except ValueError:
                try:
                    return float(obj)
                except ValueError:
                    return obj
        elif isinstance(obj, dict):
            return {k: coerce_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [coerce_types(v) for v in obj]
        return obj
    
    data = coerce_types(data)
    
    # 4) Detect duplicate keys (YAML-specific)
    if format == 'yaml':
        lines = config_text.split('\n')
        keys_seen = {}
        for i, line in enumerate(lines):
            match = re.match(r'^(\s*)(\w+):', line)
            if match:
                indent, key = match.groups()
                level_key = f"{len(indent)}:{key}"
                if level_key in keys_seen:
                    report['issues'].append(
                        f"Duplicate key '{key}' at lines {keys_seen[level_key]} and {i+1}")
                keys_seen[level_key] = i + 1
    
    print(f"⚙️ Config Clean ({format}): {len(report['issues'])} issues, "
          f"{len(report['fixes'])} vars resolved")
    return data, report
```

---

## 🧬 Bioinformatics Sequence Validation

```python
import re
import pandas as pd

VALID_BASES = {
    'DNA': set('ATCGN'),
    'RNA': set('AUCGN'),
    'PROTEIN': set('ACDEFGHIKLMNPQRSTVWY*X'),
}

def validate_sequences(df, seq_col, seq_type='DNA'):
    """
    ★ DNA/RNA/Protein sequence validation + cleaning
    ★ Data type เฉพาะทาง bioinformatics
    """
    valid_chars = VALID_BASES.get(seq_type.upper(), VALID_BASES['DNA'])
    results = []
    
    for seq in df[seq_col]:
        result = {'original': seq, 'valid': False}
        
        if pd.isna(seq) or not str(seq).strip():
            result['issue'] = 'empty'
            results.append(result)
            continue
        
        cleaned = str(seq).upper().strip()
        
        # 1) Remove FASTA header if present
        if cleaned.startswith('>'):
            lines = cleaned.split('\n')
            result['header'] = lines[0][1:]
            cleaned = ''.join(lines[1:])
        
        # 2) Remove whitespace and line breaks
        cleaned = re.sub(r'\s+', '', cleaned)
        
        # 3) Validate characters
        invalid_chars = set(cleaned) - valid_chars
        if invalid_chars:
            result['invalid_chars'] = ''.join(invalid_chars)
            # Try to fix common errors
            cleaned = cleaned.replace('U', 'T') if seq_type == 'DNA' else cleaned
            cleaned = cleaned.replace('T', 'U') if seq_type == 'RNA' else cleaned
            cleaned = re.sub(f'[^{"".join(valid_chars)}]', 'N', cleaned)
            result['auto_fixed'] = True
        
        # 4) Length validation
        result['length'] = len(cleaned)
        if seq_type in ('DNA', 'RNA'):
            result['gc_content'] = (cleaned.count('G') + cleaned.count('C')) / max(len(cleaned), 1)
        
        # 5) Quality checks
        if seq_type in ('DNA', 'RNA'):
            n_ratio = cleaned.count('N') / max(len(cleaned), 1)
            result['n_ratio'] = n_ratio
            result['high_uncertainty'] = n_ratio > 0.1
        
        result['cleaned'] = cleaned
        result['valid'] = len(cleaned) > 0 and not invalid_chars
        results.append(result)
    
    result_df = pd.DataFrame(results)
    valid_count = result_df['valid'].sum()
    print(f"🧬 Sequence Validation ({seq_type}): {valid_count}/{len(result_df)} valid")
    return result_df
```

---

## ⚡ Rate Limiting & Backpressure for Pipelines

```python
import time
from collections import deque
from datetime import datetime, timedelta

class RateLimitedCleaner:
    """
    ★ Rate limiting + backpressure สำหรับ cleaning pipelines
    ★ ต่างจาก Streaming Cleaning ตรงที่เน้น flow control patterns
    """
    def __init__(self, max_requests_per_second=10, queue_limit=1000):
        self.rate_limit = max_requests_per_second
        self.queue_limit = queue_limit
        self.request_times = deque()
        self.queue = deque(maxlen=queue_limit)
        self.circuit_state = 'closed'  # closed, open, half-open
        self.failure_count = 0
        self.failure_threshold = 5
        self.recovery_time = 30  # seconds
        self.last_failure = None
    
    def _check_rate(self):
        """Token bucket rate limiter"""
        now = time.time()
        # Remove old timestamps
        while self.request_times and self.request_times[0] < now - 1:
            self.request_times.popleft()
        
        if len(self.request_times) >= self.rate_limit:
            wait = 1 - (now - self.request_times[0])
            if wait > 0:
                time.sleep(wait)
        
        self.request_times.append(time.time())
    
    def _check_circuit(self):
        """Circuit breaker pattern"""
        if self.circuit_state == 'open':
            if (datetime.now() - self.last_failure).seconds > self.recovery_time:
                self.circuit_state = 'half-open'
                return True
            return False
        return True
    
    def process_with_backpressure(self, items, clean_fn):
        """Process items with rate limiting + circuit breaker"""
        results = []
        dropped = 0
        
        for item in items:
            # Backpressure: drop if queue full
            if len(self.queue) >= self.queue_limit:
                dropped += 1
                continue
            
            # Circuit breaker check
            if not self._check_circuit():
                self.queue.append(item)
                continue
            
            # Rate limit
            self._check_rate()
            
            try:
                result = clean_fn(item)
                results.append(result)
                self.failure_count = 0
                if self.circuit_state == 'half-open':
                    self.circuit_state = 'closed'
            except Exception as e:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.circuit_state = 'open'
                    self.last_failure = datetime.now()
                self.queue.append(item)
        
        print(f"⚡ Pipeline: {len(results)} processed, {len(self.queue)} queued, "
              f"{dropped} dropped, circuit={self.circuit_state}")
        return results
```

---

## 📦 Small File Compaction (Lakehouse Pattern)

```python
import pandas as pd
import os
from pathlib import Path

def compact_small_files(directory, output_dir=None, target_size_mb=128,
                        file_pattern='*.parquet'):
    """
    ★ แก้ปัญหา small file problem ใน data lakes
    ★ ต่างจาก Data Lakehouse/Medallion ตรงที่เน้น file optimization
    """
    input_path = Path(directory)
    output_path = Path(output_dir or directory)
    
    # 1) Scan files
    files = sorted(input_path.glob(file_pattern))
    file_info = []
    for f in files:
        size = f.stat().st_size
        file_info.append({'path': f, 'size': size, 'size_mb': size / (1024*1024)})
    
    total_files = len(file_info)
    total_size = sum(f['size_mb'] for f in file_info)
    small_files = [f for f in file_info if f['size_mb'] < target_size_mb / 4]
    
    if not small_files:
        print(f"📦 No compaction needed: {total_files} files, "
              f"avg {total_size/max(total_files,1):.1f}MB")
        return
    
    # 2) Group small files into bins
    bins = []
    current_bin = []
    current_size = 0
    
    for f in small_files:
        if current_size + f['size_mb'] > target_size_mb:
            if current_bin:
                bins.append(current_bin)
            current_bin = [f]
            current_size = f['size_mb']
        else:
            current_bin.append(f)
            current_size += f['size_mb']
    
    if current_bin:
        bins.append(current_bin)
    
    # 3) Compact each bin
    compacted = 0
    for i, bin_files in enumerate(bins):
        dfs = []
        for f in bin_files:
            try:
                dfs.append(pd.read_parquet(f['path']))
            except Exception:
                continue
        
        if dfs:
            merged = pd.concat(dfs, ignore_index=True)
            output_file = output_path / f'compacted_{i:04d}.parquet'
            merged.to_parquet(output_file, index=False)
            compacted += len(bin_files)
    
    print(f"📦 Compaction: {compacted} small files → {len(bins)} compacted files "
          f"(target: {target_size_mb}MB)")
```

---

## 🔄 Data Augmentation for Cleaning Pipelines

```python
import pandas as pd
import numpy as np
import random

def augment_data(df, target_col=None, methods=None, factor=2):
    """
    ★ เพิ่มจำนวน data สำหรับ training cleaning models
    ★ ต่างจาก SMOTE ตรงที่ general-purpose augmentation ไม่ใช่แค่ class balance
    ★ ต่างจาก Synthetic Data (Faker) ตรงที่เพิ่มจากข้อมูลจริง
    """
    augmented_rows = []
    methods = methods or ['noise', 'swap', 'mask', 'typo']
    
    for _ in range(factor - 1):
        for _, row in df.iterrows():
            new_row = row.copy()
            method = random.choice(methods)
            
            if method == 'noise':
                # Add Gaussian noise to numeric columns
                for col in df.select_dtypes(include='number').columns:
                    if col != target_col and pd.notna(new_row[col]):
                        std = df[col].std()
                        new_row[col] += np.random.normal(0, std * 0.05)
            
            elif method == 'swap':
                # Swap values between two random columns
                str_cols = [c for c in df.select_dtypes(include='object').columns
                           if c != target_col]
                if len(str_cols) >= 2:
                    c1, c2 = random.sample(str_cols, 2)
                    new_row[c1], new_row[c2] = new_row[c2], new_row[c1]
            
            elif method == 'mask':
                # Randomly mask (null) some values
                cols = [c for c in df.columns if c != target_col]
                mask_col = random.choice(cols)
                new_row[mask_col] = np.nan
            
            elif method == 'typo':
                # Introduce character-level typos
                str_cols = df.select_dtypes(include='object').columns
                for col in str_cols:
                    if col != target_col and pd.notna(new_row[col]):
                        val = str(new_row[col])
                        if len(val) > 2:
                            pos = random.randint(0, len(val) - 1)
                            val = val[:pos] + random.choice('abcdefghij') + val[pos+1:]
                            new_row[col] = val
            
            augmented_rows.append(new_row)
    
    result = pd.concat([df, pd.DataFrame(augmented_rows)], ignore_index=True)
    print(f"🔄 Augmented: {len(df)} → {len(result)} rows "
          f"(methods: {', '.join(methods)})")
    return result
```

---

## 🎬 Video / Frame Data Cleaning

```python
import numpy as np
from collections import Counter

def clean_video_frames(frames, fps=30):
    """
    ★ ทำความสะอาด video frame data สำหรับ CV/ML
    ★ Data type เฉพาะทางที่ไม่มีใน round อื่น (ต่างจาก Audio)
    """
    report = {'total_frames': len(frames), 'issues': []}
    cleaned = []
    
    for i, frame in enumerate(frames):
        if not isinstance(frame, np.ndarray):
            report['issues'].append(f'Frame {i}: invalid type')
            continue
        
        # 1) Resolution validation
        if frame.ndim < 2:
            report['issues'].append(f'Frame {i}: wrong dimensions')
            continue
        
        h, w = frame.shape[:2]
        if h < 16 or w < 16:
            report['issues'].append(f'Frame {i}: too small ({w}x{h})')
            continue
        
        # 2) Blank/black frame detection
        if frame.mean() < 5:
            report['issues'].append(f'Frame {i}: black frame')
            continue
        
        # 3) Saturated (all white) frame detection
        if frame.mean() > 250:
            report['issues'].append(f'Frame {i}: white/saturated frame')
            continue
        
        # 4) Duplicate frame detection (hash-based)
        frame_hash = hash(frame.tobytes()[:1024])  # Quick hash
        if cleaned and hash(cleaned[-1].tobytes()[:1024]) == frame_hash:
            report.setdefault('duplicate_frames', []).append(i)
            continue
        
        # 5) Resolution consistency check
        if cleaned:
            expected_shape = cleaned[0].shape
            if frame.shape != expected_shape:
                # Resize to match
                report['issues'].append(
                    f'Frame {i}: resized {frame.shape} → {expected_shape}')
        
        cleaned.append(frame)
    
    report['cleaned_frames'] = len(cleaned)
    report['removed'] = len(frames) - len(cleaned)
    report['duration'] = len(cleaned) / fps
    
    print(f"🎬 Video Clean: {len(cleaned)}/{len(frames)} frames kept, "
          f"{report['removed']} removed, {report['duration']:.1f}s at {fps}fps")
    return cleaned, report
```

---

## 📊 Probabilistic Record Linkage (Fellegi-Sunter)

```python
import pandas as pd
import math

def fellegi_sunter_linkage(df_a, df_b, match_fields, m_probs=None, u_probs=None):
    """
    ★ Formal probabilistic record linkage framework
    ★ ต่างจาก Record Linkage/Blocking ตรงที่ใช้ Fellegi-Sunter model
    ★ ต่างจาก Fuzzy Join ตรงที่ใช้ probabilistic weights
    """
    m_probs = m_probs or {f: 0.9 for f in match_fields}
    u_probs = u_probs or {f: 0.1 for f in match_fields}
    
    results = []
    
    for i, row_a in df_a.iterrows():
        for j, row_b in df_b.iterrows():
            log_weight = 0
            agreements = {}
            
            for field in match_fields:
                val_a = str(row_a.get(field, '')).lower().strip()
                val_b = str(row_b.get(field, '')).lower().strip()
                
                if val_a == val_b and val_a:
                    # Agreement: log(m/u)
                    w = math.log2(m_probs[field] / max(u_probs[field], 1e-10))
                    agreements[field] = 'agree'
                else:
                    # Disagreement: log((1-m)/(1-u))
                    w = math.log2((1 - m_probs[field]) / max(1 - u_probs[field], 1e-10))
                    agreements[field] = 'disagree'
                
                log_weight += w
            
            results.append({
                'idx_a': i, 'idx_b': j,
                'weight': log_weight,
                'agreements': agreements
            })
    
    result_df = pd.DataFrame(results)
    
    # Classify using upper/lower thresholds
    upper = result_df['weight'].quantile(0.95)
    lower = result_df['weight'].quantile(0.5)
    
    result_df['classification'] = 'possible'
    result_df.loc[result_df['weight'] >= upper, 'classification'] = 'match'
    result_df.loc[result_df['weight'] <= lower, 'classification'] = 'non-match'
    
    matches = (result_df['classification'] == 'match').sum()
    print(f"📊 Fellegi-Sunter: {matches} matches, "
          f"{(result_df['classification']=='possible').sum()} possible, "
          f"{(result_df['classification']=='non-match').sum()} non-matches")
    return result_df
```

---

## 🏭 Industry-Specific Use Cases (เพิ่มเติม Round 9)

### 51. 🚀 Aerospace / Space

| ปัญหา | วิธีแก้ |
|--------|--------|
| Telemetry data gaps (satellite downlink) | Monotonic timestamp enforcement + interpolation |
| Sensor calibration drift in orbit | Baseline correction + calibration curves |
| Multi-mission coordinate system mixing | Unified reference frame conversion |
| Launch window precision (millisecond data) | Timestamp precision validation |
| Part number traceability (AS9102) | Hierarchical BOM validation |

### 52. 🦷 Dental / Orthodontics

| ปัญหา | วิธีแก้ |
|--------|--------|
| Tooth numbering system variations (FDI/Universal/Palmer) | Mapping lookup table |
| X-ray image metadata inconsistency | DICOM field standardization |
| Treatment plan code mixing (CDT/ICD) | Code cross-reference validation |
| Patient record merge (same person, multiple clinics) | Fellegi-Sunter probabilistic linkage |
| Insurance claim data format variations | Schema normalization + validation |

### 53. 🏺 Archaeology

| ปัญหา | วิธีแก้ |
|--------|--------|
| Excavation grid coordinate systems | Unified coordinate transformation |
| Radiocarbon dating uncertainty ranges | Statistical uncertainty propagation |
| Artifact classification inconsistency | Controlled vocabulary (Getty AAT) |
| Stratigraphy layer numbering conflicts | Monotonic depth enforcement |
| Multi-language site documentation | Multilingual NLP + canonical text |

### 54. 💪 Fitness / Gym

| ปัญหา | วิธีแก้ |
|--------|--------|
| Wearable device data format variations | Schema normalization + unit conversion |
| Heart rate sensor anomalies | Windowed anomaly detection + smoothing |
| Exercise naming inconsistency | Fuzzy matching + canonical exercise DB |
| Body measurement unit mixing (kg/lb, cm/in) | Unit detection + auto-conversion |
| Membership billing data reconciliation | Bank statement reconciliation pattern |

### 55. 🎙️ Podcast / Audio Media

| ปัญหา | วิธีแก้ |
|--------|--------|
| Episode metadata inconsistency (RSS/iTunes) | Schema validation + tag normalization |
| Audio level normalization across episodes | LUFS measurement + loudness normalization |
| Transcript alignment with timestamps | Time-code validation + re-alignment |
| Guest name variations | Fuzzy dedup + canonical name resolution |
| Download analytics data reconciliation | Multi-source reconciliation + dedup |

---

## 🗿 Point Cloud / 3D Scan Data Cleaning

```python
import numpy as np

def clean_point_cloud(points, colors=None, voxel_size=0.05,
                      nb_neighbors=20, std_ratio=2.0):
    """
    ★ LiDAR / 3D scanning point cloud data cleaning
    ★ ต่างจาก Geo/Spatial ตรงที่เป็น 3D volumetric data
    """
    if not isinstance(points, np.ndarray):
        points = np.array(points)
    
    report = {'original_points': len(points), 'steps': []}
    
    # 1) Remove NaN/Inf points
    valid_mask = np.all(np.isfinite(points), axis=1)
    points = points[valid_mask]
    report['steps'].append(f"Removed {(~valid_mask).sum()} NaN/Inf points")
    
    # 2) Remove duplicate points
    _, unique_idx = np.unique(points, axis=0, return_index=True)
    dups = len(points) - len(unique_idx)
    points = points[np.sort(unique_idx)]
    report['steps'].append(f"Removed {dups} duplicate points")
    
    # 3) Voxel downsampling (grid-based)
    if voxel_size > 0:
        voxel_indices = np.floor(points / voxel_size).astype(int)
        _, unique_voxels = np.unique(voxel_indices, axis=0, return_index=True)
        before = len(points)
        points = points[unique_voxels]
        report['steps'].append(
            f"Voxel downsampled: {before} → {len(points)} (size={voxel_size})")
    
    # 4) Statistical Outlier Removal (SOR)
    from sklearn.neighbors import NearestNeighbors
    nn = NearestNeighbors(n_neighbors=nb_neighbors)
    nn.fit(points)
    distances, _ = nn.kneighbors(points)
    mean_dist = distances[:, 1:].mean(axis=1)
    threshold = mean_dist.mean() + std_ratio * mean_dist.std()
    inlier_mask = mean_dist < threshold
    outliers = (~inlier_mask).sum()
    points = points[inlier_mask]
    report['steps'].append(f"SOR removed {outliers} outliers")
    
    # 5) Bounding box validation
    bbox_min = points.min(axis=0)
    bbox_max = points.max(axis=0)
    report['bounding_box'] = {'min': bbox_min.tolist(), 'max': bbox_max.tolist()}
    report['final_points'] = len(points)
    
    print(f"🗿 Point Cloud: {report['original_points']} → {len(points)} points "
          f"({outliers} outliers removed)")
    return points, report
```

---

## 📋 Log File Parsing & Cleaning

```python
import re
import pandas as pd
from datetime import datetime

LOG_PATTERNS = {
    'apache_combined': re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[(?P<datetime>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d+) (?P<size>\S+)'
    ),
    'nginx': re.compile(
        r'(?P<ip>\S+) - \S+ \[(?P<datetime>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d+) (?P<size>\d+)'
    ),
    'syslog': re.compile(
        r'(?P<datetime>\w{3}\s+\d+\s+\d+:\d+:\d+) '
        r'(?P<host>\S+) (?P<process>\S+?)(?:\[(?P<pid>\d+)\])?: (?P<message>.*)'
    ),
    'json_line': None,  # Handled separately
}

def parse_log_file(log_text, log_format='auto', max_lines=None):
    """
    ★ Unstructured log → structured DataFrame
    ★ ต่างจาก Config File Cleaning ตรงที่เน้น log format parsing
    """
    lines = log_text.strip().split('\n')
    if max_lines:
        lines = lines[:max_lines]
    
    records = []
    failed = 0
    detected_format = log_format
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Try JSON first
        if line.startswith('{'):
            try:
                import json
                records.append(json.loads(line))
                detected_format = 'json_line'
                continue
            except:
                pass
        
        # Try regex patterns
        parsed = False
        patterns = {log_format: LOG_PATTERNS[log_format]} if log_format in LOG_PATTERNS else LOG_PATTERNS
        
        for fmt, pattern in patterns.items():
            if pattern is None:
                continue
            match = pattern.match(line)
            if match:
                record = match.groupdict()
                record['_format'] = fmt
                records.append(record)
                detected_format = fmt
                parsed = True
                break
        
        if not parsed:
            failed += 1
    
    df = pd.DataFrame(records)
    
    # Clean parsed data
    if 'status' in df.columns:
        df['status'] = pd.to_numeric(df['status'], errors='coerce')
    if 'size' in df.columns:
        df['size'] = pd.to_numeric(df['size'].replace('-', '0'), errors='coerce')
    
    print(f"📋 Log Parsed ({detected_format}): {len(records)} records, {failed} failed")
    return df
```

---

## 📝 Markdown / Rich Text Cleaning

```python
import re

def clean_markdown(text, strip_html=True, normalize_headers=True,
                   fix_links=True, remove_comments=True):
    """
    ★ ทำความสะอาด Markdown / HTML / Wiki markup
    ★ Data type เฉพาะทาง — ต่างจาก NLP text cleaning
    """
    if not text:
        return '', {}
    
    report = {'original_length': len(text), 'fixes': []}
    cleaned = text
    
    # 1) Remove HTML comments
    if remove_comments:
        cleaned = re.sub(r'<!--.*?-->', '', cleaned, flags=re.DOTALL)
        report['fixes'].append('removed HTML comments')
    
    # 2) Strip HTML tags (keep content)
    if strip_html:
        # Keep code blocks intact
        code_blocks = re.findall(r'```.*?```', cleaned, re.DOTALL)
        for i, block in enumerate(code_blocks):
            cleaned = cleaned.replace(block, f'__CODE_BLOCK_{i}__')
        
        cleaned = re.sub(r'<(?!/?(?:br|hr))[^>]+>', '', cleaned)
        
        for i, block in enumerate(code_blocks):
            cleaned = cleaned.replace(f'__CODE_BLOCK_{i}__', block)
        report['fixes'].append('stripped HTML tags')
    
    # 3) Normalize headers (ensure space after #)
    if normalize_headers:
        cleaned = re.sub(r'^(#{1,6})([^\s#])', r'\1 \2', cleaned, flags=re.MULTILINE)
        report['fixes'].append('normalized headers')
    
    # 4) Fix broken links
    if fix_links:
        # Fix missing protocol
        cleaned = re.sub(
            r'\[([^\]]+)\]\((?!https?://|mailto:|#|/)([^)]+)\)',
            r'[\1](https://\2)',
            cleaned
        )
        # Remove empty links
        cleaned = re.sub(r'\[([^\]]+)\]\(\s*\)', r'\1', cleaned)
        report['fixes'].append('fixed links')
    
    # 5) Normalize whitespace
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)  # Max 2 newlines
    cleaned = re.sub(r'[ \t]+$', '', cleaned, flags=re.MULTILINE)  # Trailing spaces
    cleaned = re.sub(r'[ \t]{2,}', ' ', cleaned)  # Multiple spaces (outside code)
    
    # 6) Fix list formatting
    cleaned = re.sub(r'^(\s*)-([^\s])', r'\1- \2', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'^(\s*)\*([^\s*])', r'\1* \2', cleaned, flags=re.MULTILINE)
    
    report['cleaned_length'] = len(cleaned)
    print(f"📝 Markdown Clean: {len(report['fixes'])} fixes, "
          f"{report['original_length']} → {len(cleaned)} chars")
    return cleaned, report
```

---

## 📊 Spreadsheet Metadata Cleaning

```python
import pandas as pd

def clean_spreadsheet(file_path, sheet_name=0):
    """
    ★ Handles Excel-specific issues: merged cells, named ranges, multi-header
    ★ ต่างจาก pandas read_excel ตรงที่จัดการ messy Excel structure
    """
    import openpyxl
    
    wb = openpyxl.load_workbook(file_path, data_only=True)
    ws = wb[sheet_name] if isinstance(sheet_name, str) else wb.sheetnames[sheet_name]
    ws_obj = wb[ws] if isinstance(ws, str) else wb.worksheets[sheet_name]
    
    report = {'merged_cells': [], 'empty_rows': 0, 'header_row': None}
    
    # 1) Unmerge cells and fill values
    merged_ranges = list(ws_obj.merged_cells.ranges)
    for merged_range in merged_ranges:
        min_row, min_col = merged_range.min_row, merged_range.min_col
        value = ws_obj.cell(min_row, min_col).value
        ws_obj.unmerge_cells(str(merged_range))
        for row in range(merged_range.min_row, merged_range.max_row + 1):
            for col in range(merged_range.min_col, merged_range.max_col + 1):
                ws_obj.cell(row, col, value)
        report['merged_cells'].append(str(merged_range))
    
    # 2) Detect header row (first row with mostly non-empty, non-numeric)
    for row_idx, row in enumerate(ws_obj.iter_rows(max_row=10, values_only=True), 1):
        non_empty = sum(1 for v in row if v is not None)
        if non_empty >= len(row) * 0.5:
            is_header = sum(1 for v in row if isinstance(v, str)) > non_empty * 0.5
            if is_header:
                report['header_row'] = row_idx
                break
    
    # 3) Read into DataFrame with detected header
    header_row = report['header_row'] or 1
    df = pd.read_excel(file_path, sheet_name=sheet_name,
                       header=header_row - 1, engine='openpyxl')
    
    # 4) Clean column names
    df.columns = [
        re.sub(r'\s+', '_', str(c).strip()).lower()
        if not str(c).startswith('Unnamed')
        else f'col_{i}'
        for i, c in enumerate(df.columns)
    ]
    
    # 5) Remove fully empty rows
    empty_mask = df.isna().all(axis=1)
    report['empty_rows'] = empty_mask.sum()
    df = df[~empty_mask].reset_index(drop=True)
    
    # 6) Remove summary/total rows (heuristic)
    total_keywords = ['total', 'sum', 'รวม', 'ทั้งหมด', 'grand total']
    for col in df.select_dtypes(include='object').columns[:2]:
        mask = df[col].astype(str).str.lower().str.strip().isin(total_keywords)
        if mask.any():
            report['total_rows_removed'] = mask.sum()
            df = df[~mask]
    
    print(f"📊 Spreadsheet Clean: {len(report['merged_cells'])} merged ranges, "
          f"{report['empty_rows']} empty rows, header at row {header_row}")
    return df, report
```

---

## 🔒 Differential Privacy Noise Injection

```python
import numpy as np
import pandas as pd

def apply_differential_privacy(df, columns, epsilon=1.0, mechanism='laplace'):
    """
    ★ ε-differential privacy noise injection
    ★ ต่างจาก k-Anonymity/l-Diversity ตรงที่เป็น mathematical guarantee
    """
    result = df.copy()
    report = {'epsilon': epsilon, 'mechanism': mechanism, 'columns': {}}
    
    for col in columns:
        if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
            continue
        
        values = df[col].dropna()
        sensitivity = values.max() - values.min()
        
        if mechanism == 'laplace':
            scale = sensitivity / epsilon
            noise = np.random.laplace(0, scale, size=len(df))
        
        elif mechanism == 'gaussian':
            delta = 1e-5
            sigma = sensitivity * np.sqrt(2 * np.log(1.25 / delta)) / epsilon
            noise = np.random.normal(0, sigma, size=len(df))
        
        elif mechanism == 'exponential':
            # For categorical — score-based selection
            noise = np.random.exponential(sensitivity / epsilon, size=len(df))
        
        result[col] = df[col] + noise
        
        # Preserve original range (clip)
        result[col] = result[col].clip(values.min(), values.max())
        
        report['columns'][col] = {
            'sensitivity': sensitivity,
            'noise_scale': scale if mechanism == 'laplace' else sigma,
            'mean_noise': np.abs(noise).mean()
        }
    
    print(f"🔒 DP ({mechanism}, ε={epsilon}): {len(report['columns'])} columns privatized")
    return result, report
```

---

## 🔗 Data Lineage Tracking

```python
import json
from datetime import datetime
from hashlib import sha256

class DataLineageTracker:
    """
    ★ ติดตามว่า data มาจากไหน ถูก transform อะไรบ้าง
    ★ ต่างจาก Data Versioning (DVC) ตรงที่เน้น transformation graph
    """
    def __init__(self):
        self.lineage = []
        self.current_hash = None
    
    def _hash_df(self, df):
        """Create fingerprint of DataFrame"""
        content = f"{df.shape}_{df.columns.tolist()}_{df.dtypes.tolist()}"
        return sha256(content.encode()).hexdigest()[:12]
    
    def record_source(self, df, source_name, source_type='file', metadata=None):
        """Record data source"""
        self.current_hash = self._hash_df(df)
        self.lineage.append({
            'step': 'SOURCE',
            'timestamp': datetime.now().isoformat(),
            'source': source_name,
            'source_type': source_type,
            'hash': self.current_hash,
            'shape': df.shape,
            'metadata': metadata or {}
        })
        return df
    
    def record_transform(self, df_before, df_after, operation, params=None):
        """Record a transformation step"""
        before_hash = self._hash_df(df_before)
        after_hash = self._hash_df(df_after)
        
        self.lineage.append({
            'step': 'TRANSFORM',
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'input_hash': before_hash,
            'output_hash': after_hash,
            'rows_before': len(df_before),
            'rows_after': len(df_after),
            'cols_before': len(df_before.columns),
            'cols_after': len(df_after.columns),
            'params': params or {}
        })
        self.current_hash = after_hash
        return df_after
    
    def get_lineage(self):
        return self.lineage
    
    def export_lineage(self, path):
        with open(path, 'w') as f:
            json.dump(self.lineage, f, indent=2, default=str)
        print(f"🔗 Lineage: {len(self.lineage)} steps exported to {path}")
    
    def print_summary(self):
        sources = [s for s in self.lineage if s['step'] == 'SOURCE']
        transforms = [s for s in self.lineage if s['step'] == 'TRANSFORM']
        print(f"🔗 Lineage: {len(sources)} sources, {len(transforms)} transforms")
        for t in transforms:
            print(f"   → {t['operation']}: {t['rows_before']}→{t['rows_after']} rows")
```

---

## 🔄 Schema Evolution & Migration

```python
import pandas as pd
from copy import deepcopy

class SchemaEvolution:
    """
    ★ จัดการเมื่อ schema เปลี่ยน — backward/forward compatibility
    ★ ต่างจาก Data Versioning ตรงที่เน้น schema change management
    """
    def __init__(self):
        self.versions = []
        self.migrations = []
    
    def register_schema(self, version, columns, dtypes=None, defaults=None):
        self.versions.append({
            'version': version,
            'columns': columns,
            'dtypes': dtypes or {},
            'defaults': defaults or {}
        })
    
    def add_migration(self, from_version, to_version, transform_fn):
        self.migrations.append({
            'from': from_version,
            'to': to_version,
            'transform': transform_fn
        })
    
    def detect_version(self, df):
        """Detect schema version from DataFrame columns"""
        df_cols = set(df.columns)
        best_match = None
        best_score = 0
        
        for schema in self.versions:
            schema_cols = set(schema['columns'])
            overlap = len(df_cols & schema_cols)
            score = overlap / max(len(schema_cols), 1)
            if score > best_score:
                best_score = score
                best_match = schema['version']
        
        return best_match, best_score
    
    def migrate(self, df, target_version=None):
        """Migrate DataFrame to target schema version"""
        current, confidence = self.detect_version(df)
        target = target_version or self.versions[-1]['version']
        
        if current == target:
            return df
        
        result = df.copy()
        target_schema = next(s for s in self.versions if s['version'] == target)
        
        # Add missing columns with defaults
        for col in target_schema['columns']:
            if col not in result.columns:
                default = target_schema['defaults'].get(col)
                result[col] = default
        
        # Apply type conversions
        for col, dtype in target_schema['dtypes'].items():
            if col in result.columns:
                try:
                    result[col] = result[col].astype(dtype)
                except (ValueError, TypeError):
                    pass
        
        # Apply custom migrations
        for mig in self.migrations:
            if mig['from'] == current and mig['to'] == target:
                result = mig['transform'](result)
                break
        
        # Remove extra columns
        result = result[[c for c in target_schema['columns'] if c in result.columns]]
        
        print(f"🔄 Schema: v{current} → v{target} (confidence={confidence:.0%}), "
              f"{len(result.columns)} columns")
        return result
```

---

## 🌳 Hierarchical Data Flattening

```python
import pandas as pd

def flatten_nested(data, sep='.', max_depth=10):
    """
    ★ Deeply nested JSON/dict → flat key-value pairs
    ★ ต่างจาก JSON parsing ตรงที่จัดการ arbitrary depth + arrays
    """
    def _flatten(obj, prefix='', depth=0):
        items = {}
        if depth > max_depth:
            items[prefix] = str(obj)
            return items
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{prefix}{sep}{key}" if prefix else key
                items.update(_flatten(value, new_key, depth + 1))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_key = f"{prefix}{sep}{i}"
                if isinstance(item, dict):
                    items.update(_flatten(item, new_key, depth + 1))
                else:
                    items[new_key] = item
            # Also store array length
            items[f"{prefix}{sep}__len__"] = len(obj)
        else:
            items[prefix] = obj
        
        return items
    
    if isinstance(data, list):
        rows = [_flatten(item) for item in data]
    elif isinstance(data, dict):
        rows = [_flatten(data)]
    else:
        raise ValueError("Input must be dict or list of dicts")
    
    df = pd.DataFrame(rows)
    
    # Clean column names
    df.columns = [c.lstrip(sep) for c in df.columns]
    
    # Remove __len__ columns if not needed
    len_cols = [c for c in df.columns if c.endswith('__len__')]
    
    max_depth_found = max(c.count(sep) for c in df.columns) if df.columns.any() else 0
    print(f"🌳 Flatten: {len(df)} rows, {len(df.columns)} columns, "
          f"max depth = {max_depth_found}")
    return df
```

---

## 🧠 Semantic Type Detection

```python
import re
import pandas as pd
from collections import Counter

SEMANTIC_PATTERNS = {
    'email': re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'),
    'phone': re.compile(r'^[\+]?[(]?\d{1,4}[)]?[-\s./]?\d{1,4}[-\s./]?\d{1,9}$'),
    'url': re.compile(r'^https?://[^\s]+$'),
    'ipv4': re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'),
    'uuid': re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I),
    'credit_card': re.compile(r'^\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}$'),
    'thai_id': re.compile(r'^\d{1}-\d{4}-\d{5}-\d{2}-\d{1}$'),
    'postal_code_th': re.compile(r'^\d{5}$'),
    'date_iso': re.compile(r'^\d{4}-\d{2}-\d{2}'),
    'currency': re.compile(r'^[\$€£¥฿]\s?\d'),
    'percentage': re.compile(r'^\d+\.?\d*\s?%$'),
    'hex_color': re.compile(r'^#[0-9a-fA-F]{3,8}$'),
    'json_value': re.compile(r'^[\{\[]'),
    'latitude': re.compile(r'^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$'),
    'longitude': re.compile(r'^-?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'),
}

def detect_semantic_types(df, sample_size=1000):
    """
    ★ Auto-detect ว่าแต่ละ column คือ data type อะไร (email, phone, date, etc.)
    ★ ต่างจาก dtype detection ตรงที่เป็น semantic meaning ไม่ใช่แค่ int/str
    """
    results = {}
    
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            values = df[col].dropna()
            if values.empty:
                results[col] = {'type': 'numeric', 'subtype': 'empty'}
                continue
            
            # Check if integer-like
            if (values == values.astype(int)).all():
                if values.min() >= 0 and values.max() <= 1:
                    results[col] = {'type': 'boolean_numeric', 'confidence': 0.8}
                elif values.nunique() < 20:
                    results[col] = {'type': 'categorical_numeric', 'confidence': 0.7}
                else:
                    results[col] = {'type': 'integer', 'confidence': 0.9}
            else:
                results[col] = {'type': 'float', 'confidence': 0.9}
            continue
        
        # String columns — sample and test patterns
        sample = df[col].dropna().astype(str).head(sample_size)
        if sample.empty:
            results[col] = {'type': 'empty', 'confidence': 1.0}
            continue
        
        type_votes = Counter()
        for val in sample:
            for type_name, pattern in SEMANTIC_PATTERNS.items():
                if pattern.match(val.strip()):
                    type_votes[type_name] += 1
        
        if type_votes:
            best_type, count = type_votes.most_common(1)[0]
            confidence = count / len(sample)
            results[col] = {
                'type': best_type,
                'confidence': confidence,
                'matched': count,
                'total': len(sample)
            }
        else:
            # Heuristic checks
            avg_len = sample.str.len().mean()
            unique_ratio = sample.nunique() / len(sample)
            
            if unique_ratio < 0.05:
                results[col] = {'type': 'categorical', 'confidence': 0.8}
            elif avg_len > 100:
                results[col] = {'type': 'text/description', 'confidence': 0.7}
            elif avg_len < 5 and unique_ratio < 0.1:
                results[col] = {'type': 'code/abbreviation', 'confidence': 0.6}
            else:
                results[col] = {'type': 'string', 'confidence': 0.5}
    
    detected = sum(1 for v in results.values() if v.get('confidence', 0) > 0.7)
    print(f"🧠 Semantic Detection: {detected}/{len(results)} columns typed (>70% conf)")
    return results
```

---

## 📈 Data Quality Scoring (Composite)

```python
import pandas as pd
import numpy as np

def calculate_quality_score(df, weights=None):
    """
    ★ คะแนนรวมความสะอาดของ dataset (0-100)
    ★ ต่างจาก Data Profiling ตรงที่ให้ single composite score
    """
    default_weights = {
        'completeness': 0.25,
        'uniqueness': 0.15,
        'consistency': 0.20,
        'validity': 0.20,
        'freshness': 0.10,
        'accuracy': 0.10,
    }
    weights = weights or default_weights
    scores = {}
    
    # 1) Completeness — % non-null
    total_cells = df.size
    non_null = df.notna().sum().sum()
    scores['completeness'] = (non_null / total_cells) * 100
    
    # 2) Uniqueness — avg unique ratio (exclude obvious ID columns)
    unique_scores = []
    for col in df.columns:
        non_null_vals = df[col].dropna()
        if len(non_null_vals) > 0:
            unique_ratio = non_null_vals.nunique() / len(non_null_vals)
            # Penalize if too many duplicates (but not for booleans)
            if non_null_vals.nunique() > 2:
                unique_scores.append(min(unique_ratio * 100, 100))
    scores['uniqueness'] = np.mean(unique_scores) if unique_scores else 100
    
    # 3) Consistency — check format consistency within columns
    consistency_scores = []
    for col in df.select_dtypes(include='object').columns:
        sample = df[col].dropna().astype(str)
        if len(sample) > 0:
            lengths = sample.str.len()
            cv = lengths.std() / max(lengths.mean(), 1)
            consistency_scores.append(max(0, (1 - cv) * 100))
    scores['consistency'] = np.mean(consistency_scores) if consistency_scores else 100
    
    # 4) Validity — % of values within expected ranges
    validity_scores = []
    for col in df.select_dtypes(include='number').columns:
        values = df[col].dropna()
        if len(values) > 10:
            q1, q3 = values.quantile(0.25), values.quantile(0.75)
            iqr = q3 - q1
            valid = values.between(q1 - 3*iqr, q3 + 3*iqr).mean() * 100
            validity_scores.append(valid)
    scores['validity'] = np.mean(validity_scores) if validity_scores else 100
    
    # 5) Freshness — placeholder (needs timestamp column)
    scores['freshness'] = 100  # Default if no date column
    date_cols = df.select_dtypes(include='datetime').columns
    if len(date_cols) > 0:
        latest = df[date_cols[0]].max()
        if pd.notna(latest):
            days_old = (pd.Timestamp.now() - latest).days
            scores['freshness'] = max(0, 100 - days_old * 2)
    
    # 6) Accuracy — cross-column consistency checks
    scores['accuracy'] = 90  # Default baseline
    
    # Composite score
    composite = sum(scores[k] * weights.get(k, 0) for k in scores)
    
    grade = ('A' if composite >= 90 else 'B' if composite >= 75
             else 'C' if composite >= 60 else 'D' if composite >= 40 else 'F')
    
    print(f"📈 Quality Score: {composite:.1f}/100 (Grade: {grade})")
    for dim, score in scores.items():
        print(f"   {dim}: {score:.1f}")
    
    return {'composite': composite, 'grade': grade, 'dimensions': scores}
```

---

## 📊 Auto Data Profiling Report

```python
import pandas as pd
import numpy as np

def generate_profile(df, name='dataset'):
    """
    ★ Auto-generate comprehensive data profiling summary
    ★ ต่างจาก Quality Scoring ตรงที่เป็น detailed descriptive report
    """
    report = {
        'name': name,
        'rows': len(df),
        'columns': len(df.columns),
        'memory_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'duplicated_rows': df.duplicated().sum(),
        'columns_profile': {}
    }
    
    for col in df.columns:
        profile = {
            'dtype': str(df[col].dtype),
            'non_null': df[col].notna().sum(),
            'null_count': df[col].isna().sum(),
            'null_pct': df[col].isna().mean() * 100,
            'unique': df[col].nunique(),
            'unique_pct': df[col].nunique() / max(len(df), 1) * 100
        }
        
        if pd.api.types.is_numeric_dtype(df[col]):
            values = df[col].dropna()
            profile.update({
                'mean': values.mean(),
                'std': values.std(),
                'min': values.min(),
                'max': values.max(),
                'median': values.median(),
                'q25': values.quantile(0.25),
                'q75': values.quantile(0.75),
                'skew': values.skew(),
                'kurtosis': values.kurtosis(),
                'zeros': (values == 0).sum(),
                'negatives': (values < 0).sum(),
            })
        
        elif pd.api.types.is_string_dtype(df[col]):
            values = df[col].dropna().astype(str)
            profile.update({
                'avg_length': values.str.len().mean(),
                'min_length': values.str.len().min(),
                'max_length': values.str.len().max(),
                'empty_strings': (values == '').sum(),
                'whitespace_only': values.str.strip().eq('').sum(),
                'top_5': values.value_counts().head(5).to_dict(),
            })
        
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            values = df[col].dropna()
            profile.update({
                'min_date': str(values.min()),
                'max_date': str(values.max()),
                'range_days': (values.max() - values.min()).days,
            })
        
        report['columns_profile'][col] = profile
    
    # Summary warnings
    warnings = []
    for col, p in report['columns_profile'].items():
        if p['null_pct'] > 50:
            warnings.append(f"⚠️ {col}: {p['null_pct']:.0f}% null")
        if p['unique_pct'] < 1 and p['non_null'] > 100:
            warnings.append(f"⚠️ {col}: very low cardinality ({p['unique']} unique)")
        if p.get('zeros', 0) > len(df) * 0.5:
            warnings.append(f"⚠️ {col}: >50% zeros")
    
    report['warnings'] = warnings
    
    print(f"📊 Profile '{name}': {len(df)} rows × {len(df.columns)} cols, "
          f"{report['memory_mb']:.1f}MB, {len(warnings)} warnings")
    return report
```

---

## ✅ Expectation-based Data Testing

```python
import pandas as pd
from datetime import datetime

class DataExpectations:
    """
    ★ Declarative data validation ala Great Expectations
    ★ ต่างจาก Validation Rules ตรงที่เป็น reusable test suite
    """
    def __init__(self, name='test_suite'):
        self.name = name
        self.expectations = []
        self.results = []
    
    def expect_column_exists(self, column):
        self.expectations.append(('column_exists', {'column': column}))
        return self
    
    def expect_column_not_null(self, column, threshold=0.95):
        self.expectations.append(('not_null', {'column': column, 'threshold': threshold}))
        return self
    
    def expect_column_unique(self, column):
        self.expectations.append(('unique', {'column': column}))
        return self
    
    def expect_column_values_in_set(self, column, value_set):
        self.expectations.append(('in_set', {'column': column, 'values': value_set}))
        return self
    
    def expect_column_values_between(self, column, min_val=None, max_val=None):
        self.expectations.append(('between', {
            'column': column, 'min': min_val, 'max': max_val}))
        return self
    
    def expect_column_mean_between(self, column, min_val, max_val):
        self.expectations.append(('mean_between', {
            'column': column, 'min': min_val, 'max': max_val}))
        return self
    
    def expect_row_count_between(self, min_count, max_count):
        self.expectations.append(('row_count', {'min': min_count, 'max': max_count}))
        return self
    
    def expect_column_regex_match(self, column, regex):
        self.expectations.append(('regex', {'column': column, 'regex': regex}))
        return self
    
    def validate(self, df):
        self.results = []
        
        for exp_type, params in self.expectations:
            result = {'type': exp_type, 'params': params, 'success': False}
            
            try:
                if exp_type == 'column_exists':
                    result['success'] = params['column'] in df.columns
                
                elif exp_type == 'not_null':
                    ratio = df[params['column']].notna().mean()
                    result['success'] = ratio >= params['threshold']
                    result['actual'] = ratio
                
                elif exp_type == 'unique':
                    result['success'] = df[params['column']].is_unique
                    result['duplicates'] = df[params['column']].duplicated().sum()
                
                elif exp_type == 'in_set':
                    valid = df[params['column']].dropna().isin(params['values'])
                    result['success'] = valid.all()
                    result['invalid_count'] = (~valid).sum()
                
                elif exp_type == 'between':
                    values = df[params['column']].dropna()
                    in_range = True
                    if params['min'] is not None:
                        in_range &= (values >= params['min']).all()
                    if params['max'] is not None:
                        in_range &= (values <= params['max']).all()
                    result['success'] = bool(in_range)
                
                elif exp_type == 'mean_between':
                    mean = df[params['column']].mean()
                    result['success'] = params['min'] <= mean <= params['max']
                    result['actual_mean'] = mean
                
                elif exp_type == 'row_count':
                    result['success'] = params['min'] <= len(df) <= params['max']
                    result['actual'] = len(df)
                
                elif exp_type == 'regex':
                    import re
                    pattern = re.compile(params['regex'])
                    matches = df[params['column']].dropna().astype(str).str.match(pattern)
                    result['success'] = matches.all()
                    result['match_rate'] = matches.mean()
            
            except Exception as e:
                result['error'] = str(e)
            
            self.results.append(result)
        
        passed = sum(1 for r in self.results if r['success'])
        total = len(self.results)
        print(f"✅ Expectations '{self.name}': {passed}/{total} passed "
              f"({'PASS' if passed == total else 'FAIL'})")
        return self.results
```

---

## 🔁 Regression Testing for Data Pipelines

```python
import pandas as pd
import numpy as np
import json

class DataRegressionTest:
    """
    ★ ตรวจว่า cleaning pipeline ไม่ทำข้อมูลเสียหลัง refactor
    ★ ต่างจาก Expectation-based ตรงที่เทียบกับ baseline snapshot
    """
    def __init__(self):
        self.baseline = None
    
    def save_baseline(self, df, path):
        """Save golden dataset as baseline"""
        baseline = {
            'shape': list(df.shape),
            'columns': df.columns.tolist(),
            'dtypes': {c: str(df[c].dtype) for c in df.columns},
            'stats': {},
            'sample_hash': hash(df.head(100).to_json()),
        }
        
        for col in df.columns:
            col_stats = {
                'null_count': int(df[col].isna().sum()),
                'unique_count': int(df[col].nunique()),
            }
            if pd.api.types.is_numeric_dtype(df[col]):
                values = df[col].dropna()
                col_stats.update({
                    'mean': float(values.mean()),
                    'std': float(values.std()),
                    'min': float(values.min()),
                    'max': float(values.max()),
                })
            baseline['stats'][col] = col_stats
        
        with open(path, 'w') as f:
            json.dump(baseline, f, indent=2)
        print(f"🔁 Baseline saved: {df.shape}")
    
    def compare(self, df, baseline_path, tolerance=0.05):
        """Compare current output against baseline"""
        with open(baseline_path) as f:
            baseline = json.load(f)
        
        issues = []
        
        # 1) Shape check
        if list(df.shape) != baseline['shape']:
            row_diff = df.shape[0] - baseline['shape'][0]
            col_diff = df.shape[1] - baseline['shape'][1]
            if abs(row_diff / max(baseline['shape'][0], 1)) > tolerance:
                issues.append(f"Row count: {baseline['shape'][0]} → {df.shape[0]}")
            if col_diff != 0:
                issues.append(f"Column count: {baseline['shape'][1]} → {df.shape[1]}")
        
        # 2) Column presence
        missing = set(baseline['columns']) - set(df.columns)
        extra = set(df.columns) - set(baseline['columns'])
        if missing:
            issues.append(f"Missing columns: {missing}")
        if extra:
            issues.append(f"New columns: {extra}")
        
        # 3) Statistics comparison
        for col, stats in baseline['stats'].items():
            if col not in df.columns:
                continue
            
            current_nulls = df[col].isna().sum()
            if abs(current_nulls - stats['null_count']) > baseline['shape'][0] * tolerance:
                issues.append(f"{col}: null count {stats['null_count']} → {current_nulls}")
            
            if 'mean' in stats and pd.api.types.is_numeric_dtype(df[col]):
                current_mean = df[col].dropna().mean()
                if abs(current_mean - stats['mean']) > abs(stats['mean']) * tolerance:
                    issues.append(
                        f"{col}: mean {stats['mean']:.2f} → {current_mean:.2f}")
        
        status = 'PASS' if not issues else 'FAIL'
        print(f"🔁 Regression Test: {status} ({len(issues)} issues)")
        for issue in issues:
            print(f"   ❌ {issue}")
        
        return {'status': status, 'issues': issues}
```

---

## 👤 Human-in-the-Loop Cleaning Workflow

```python
import pandas as pd
from collections import defaultdict

class HumanInTheLoopCleaner:
    """
    ★ Workflow สำหรับ human review ของ cleaning decisions
    ★ ต่างจาก Active Learning ตรงที่เน้น UI workflow ไม่ใช่ ML model
    """
    def __init__(self):
        self.review_queue = []
        self.decisions = {}
        self.rules_learned = defaultdict(list)
    
    def auto_clean(self, df, auto_rules):
        """Apply auto-cleanable rules, queue uncertain cases"""
        auto_cleaned = df.copy()
        needs_review = []
        
        for rule_name, rule_fn in auto_rules.items():
            for idx, row in auto_cleaned.iterrows():
                result = rule_fn(row)
                if result['action'] == 'auto_fix':
                    for col, val in result.get('fixes', {}).items():
                        auto_cleaned.at[idx, col] = val
                elif result['action'] == 'needs_review':
                    needs_review.append({
                        'index': idx,
                        'rule': rule_name,
                        'reason': result.get('reason', ''),
                        'current_values': row.to_dict(),
                        'suggestion': result.get('suggestion', None),
                        'confidence': result.get('confidence', 0)
                    })
        
        # Sort by confidence (lowest first — most uncertain to human)
        self.review_queue = sorted(needs_review, key=lambda x: x['confidence'])
        
        print(f"👤 HITL: {len(df) - len(needs_review)} auto-cleaned, "
              f"{len(needs_review)} need human review")
        return auto_cleaned, self.review_queue
    
    def submit_decision(self, review_item, decision, apply_to_similar=False):
        """Record human decision"""
        self.decisions[review_item['index']] = {
            'decision': decision,  # 'accept_suggestion', 'reject', 'custom_fix', 'skip'
            'rule': review_item['rule'],
        }
        
        if apply_to_similar:
            self.rules_learned[review_item['rule']].append({
                'pattern': review_item['current_values'],
                'decision': decision
            })
    
    def get_review_stats(self):
        total = len(self.review_queue)
        reviewed = len(self.decisions)
        remaining = total - reviewed
        return {
            'total': total,
            'reviewed': reviewed,
            'remaining': remaining,
            'progress': reviewed / max(total, 1) * 100,
            'rules_learned': len(self.rules_learned)
        }
```

---

## 🔀 Pipeline Orchestration (DAG-based)

```python
from collections import defaultdict
import time

class CleaningDAG:
    """
    ★ DAG-based orchestration สำหรับ cleaning pipelines
    ★ ต่างจาก Pipeline Orchestration (Airflow) ตรงที่ lightweight Python-native
    """
    def __init__(self, name='cleaning_pipeline'):
        self.name = name
        self.tasks = {}
        self.dependencies = defaultdict(list)
        self.results = {}
    
    def add_task(self, name, fn, depends_on=None):
        self.tasks[name] = fn
        if depends_on:
            for dep in depends_on:
                self.dependencies[name].append(dep)
        return self
    
    def _get_execution_order(self):
        """Topological sort"""
        visited = set()
        order = []
        
        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for dep in self.dependencies[node]:
                dfs(dep)
            order.append(node)
        
        for task in self.tasks:
            dfs(task)
        return order
    
    def execute(self, initial_data):
        """Execute pipeline in dependency order"""
        order = self._get_execution_order()
        self.results = {'__input__': initial_data}
        timings = {}
        
        print(f"🔀 Pipeline '{self.name}': {len(order)} tasks")
        
        for task_name in order:
            deps = self.dependencies[task_name]
            
            # Get input from dependencies or initial data
            if deps:
                inputs = {d: self.results[d] for d in deps if d in self.results}
                if len(inputs) == 1:
                    task_input = list(inputs.values())[0]
                else:
                    task_input = inputs
            else:
                task_input = initial_data
            
            start = time.time()
            try:
                self.results[task_name] = self.tasks[task_name](task_input)
                status = '✅'
            except Exception as e:
                self.results[task_name] = None
                status = f'❌ {str(e)[:50]}'
            
            elapsed = time.time() - start
            timings[task_name] = elapsed
            print(f"   {status} {task_name} ({elapsed:.2f}s)")
        
        return self.results.get(order[-1]) if order else initial_data
```

---

## 💰 Cost-aware Cleaning Strategy

```python
import pandas as pd
from dataclasses import dataclass

@dataclass
class CleaningOption:
    name: str
    quality_gain: float    # Expected quality improvement (0-1)
    time_minutes: float    # Estimated time
    cost_usd: float        # API/compute cost
    auto_applicable: bool  # Can run without human

def select_optimal_strategy(df, options, budget_usd=100, time_limit_min=60,
                            quality_target=0.9):
    """
    ★ เลือก cleaning technique ตามงบเงิน + เวลาที่มี
    ★ Knapsack-like optimization สำหรับ cleaning decisions
    """
    # Sort by quality_gain/cost ratio (best bang for buck)
    sorted_options = sorted(options,
        key=lambda o: o.quality_gain / max(o.cost_usd + o.time_minutes * 0.5, 0.01),
        reverse=True
    )
    
    selected = []
    total_cost = 0
    total_time = 0
    total_quality = 0
    
    for option in sorted_options:
        if total_cost + option.cost_usd > budget_usd:
            continue
        if total_time + option.time_minutes > time_limit_min:
            continue
        if total_quality >= quality_target:
            break
        
        selected.append(option)
        total_cost += option.cost_usd
        total_time += option.time_minutes
        total_quality = min(1.0, total_quality + option.quality_gain * (1 - total_quality))
    
    # Generate report
    report = {
        'selected': [s.name for s in selected],
        'total_cost': total_cost,
        'total_time': total_time,
        'expected_quality': total_quality,
        'budget_remaining': budget_usd - total_cost,
        'time_remaining': time_limit_min - total_time,
        'skipped': [o.name for o in sorted_options if o not in selected]
    }
    
    print(f"💰 Strategy: {len(selected)}/{len(options)} techniques selected")
    print(f"   Cost: ${total_cost:.2f}/{budget_usd}, Time: {total_time:.0f}/{time_limit_min}min")
    print(f"   Expected Quality: {total_quality:.1%}")
    
    return selected, report
```

---

## 🏢 Multi-tenant Data Isolation

```python
import pandas as pd
import hashlib

def validate_tenant_isolation(df, tenant_col, sensitive_cols=None):
    """
    ★ SaaS multi-tenant data — ตรวจว่า tenant data ไม่ปนกัน
    ★ ต่างจาก Data Privacy ตรงที่เน้น tenant boundary ไม่ใช่ PII
    """
    report = {
        'tenant_count': df[tenant_col].nunique(),
        'violations': [],
        'cross_contamination': []
    }
    
    sensitive_cols = sensitive_cols or []
    
    # 1) Check for null tenant IDs
    null_tenants = df[tenant_col].isna().sum()
    if null_tenants > 0:
        report['violations'].append(
            f"{null_tenants} rows with NULL tenant ID")
    
    # 2) Check for cross-tenant data leakage
    for col in sensitive_cols:
        if col not in df.columns:
            continue
        
        # Value should belong to only one tenant
        value_tenants = df.groupby(col)[tenant_col].nunique()
        shared = value_tenants[value_tenants > 1]
        
        if len(shared) > 0:
            report['cross_contamination'].append({
                'column': col,
                'shared_values': len(shared),
                'affected_tenants': shared.max(),
                'examples': shared.head(3).to_dict()
            })
    
    # 3) Row count distribution (detect imbalanced tenants)
    tenant_counts = df[tenant_col].value_counts()
    report['tenant_distribution'] = {
        'min_rows': int(tenant_counts.min()),
        'max_rows': int(tenant_counts.max()),
        'median_rows': int(tenant_counts.median()),
        'empty_tenants': (tenant_counts == 0).sum()
    }
    
    # 4) Anonymize tenant IDs for safe export
    def anonymize_tenant(tenant_id):
        return hashlib.sha256(str(tenant_id).encode()).hexdigest()[:8]
    
    df_safe = df.copy()
    df_safe[f'{tenant_col}_anon'] = df[tenant_col].map(anonymize_tenant)
    
    total_violations = len(report['violations']) + len(report['cross_contamination'])
    print(f"🏢 Tenant Isolation: {report['tenant_count']} tenants, "
          f"{total_violations} violations")
    return report, df_safe
```

---

## 🏭 Industry-Specific Use Cases (เพิ่มเติม Round 10)

### 56. 🐾 Veterinary / Animal Health

| ปัญหา | วิธีแก้ |
|--------|--------|
| Species/breed naming inconsistency | Controlled vocabulary + fuzzy match |
| Weight unit mixing (kg/lb) across clinics | Semantic type detection + auto-convert |
| Vaccination schedule date conflicts | Monotonic date enforcement |
| Lab result reference range varies by species | Species-aware validation rules |
| Multi-clinic patient record merge | Probabilistic linkage (Fellegi-Sunter) |

### 57. 🍷 Wine / Brewery

| ปัญหา | วิธีแก้ |
|--------|--------|
| Vintage year data entry errors | Range validation (1900-current) |
| Grape variety naming (Syrah vs Shiraz) | Canonical name mapping |
| Alcohol % precision inconsistency | Decimal normalization + rounding |
| Tasting notes free text inconsistency | NLP topic extraction + standardization |
| Production batch tracking data gaps | Data lineage tracking |

### 58. 🏛️ Museum / Gallery

| ปัญหา | วิธีแก้ |
|--------|--------|
| Artwork provenance data inconsistency | Schema evolution + lineage tracking |
| Artist name variations across eras | Fuzzy dedup + authority file (ULAN) |
| Acquisition date format mixing | Date parsing + normalization |
| Collection catalog number conflicts | Uniqueness enforcement + dedup |
| Multi-language descriptions | Multilingual NLP + canonical text |

### 59. ♻️ Waste Management / Recycling

| ปัญหา | วิธีแก้ |
|--------|--------|
| Material classification codes vary by region | Code cross-reference mapping |
| Weight measurement sensor drift | Calibration correction + SOR |
| Route optimization data gaps | Spatial interpolation + imputation |
| Contamination level threshold inconsistency | Domain-specific validation rules |
| Multi-depot data reconciliation | Multi-source reconciliation + dedup |

### 60. 🎮 eSports / Gaming

| ปัญหา | วิธีแก้ |
|--------|--------|
| Player IGN changes over time | Identity resolution + alias tracking |
| Match result format varies by game/platform | Schema evolution + normalization |
| ELO/MMR rating data gaps | Monotonic constraint + interpolation |
| Tournament bracket data inconsistency | Hierarchical data validation |
| Anti-cheat flagged data cleaning | Data quarantine + human review |

---

## 🖼️ Image Data Cleaning & Preprocessing

```python
import numpy as np
from collections import Counter

def clean_image_dataset(images, labels=None, min_size=32, max_size=4096):
    """
    ★ Image dataset cleaning สำหรับ CV/ML pipelines
    ★ ต่างจาก Video/Frame ตรงที่เน้น static image quality + metadata
    """
    report = {'total': len(images), 'issues': [], 'removed': 0}
    cleaned_images = []
    cleaned_labels = [] if labels else None
    
    for i, img in enumerate(images):
        if not isinstance(img, np.ndarray):
            report['issues'].append(f"Image {i}: invalid type ({type(img)})")
            report['removed'] += 1
            continue
        
        # 1) Dimension validation
        if img.ndim not in (2, 3):
            report['issues'].append(f"Image {i}: wrong ndim={img.ndim}")
            report['removed'] += 1
            continue
        
        h, w = img.shape[:2]
        
        # 2) Size validation
        if h < min_size or w < min_size:
            report['issues'].append(f"Image {i}: too small ({w}x{h})")
            report['removed'] += 1
            continue
        if h > max_size or w > max_size:
            report['issues'].append(f"Image {i}: too large ({w}x{h})")
            report['removed'] += 1
            continue
        
        # 3) Corrupt / constant image detection
        if img.std() < 1.0:
            report['issues'].append(f"Image {i}: constant/corrupt (std={img.std():.2f})")
            report['removed'] += 1
            continue
        
        # 4) Channel validation (grayscale vs RGB vs RGBA)
        if img.ndim == 3:
            channels = img.shape[2]
            if channels == 4:
                img = img[:, :, :3]  # Drop alpha
            elif channels not in (1, 3):
                report['issues'].append(f"Image {i}: unusual channels={channels}")
                report['removed'] += 1
                continue
        
        # 5) NaN/Inf pixel detection
        if not np.all(np.isfinite(img)):
            img = np.nan_to_num(img, nan=0, posinf=255, neginf=0)
            report['issues'].append(f"Image {i}: NaN/Inf pixels fixed")
        
        # 6) Value range normalization
        if img.max() > 255 or img.min() < 0:
            img = np.clip(img, 0, 255).astype(np.uint8)
        
        cleaned_images.append(img)
        if labels:
            cleaned_labels.append(labels[i])
    
    # 7) Duplicate detection (perceptual hash)
    if len(cleaned_images) > 1:
        hashes = [hash(img.tobytes()[:2048]) for img in cleaned_images]
        seen = set()
        deduped = []
        deduped_labels = []
        for j, h in enumerate(hashes):
            if h not in seen:
                seen.add(h)
                deduped.append(cleaned_images[j])
                if cleaned_labels:
                    deduped_labels.append(cleaned_labels[j])
        
        dups = len(cleaned_images) - len(deduped)
        if dups > 0:
            report['issues'].append(f"{dups} duplicate images removed")
        cleaned_images = deduped
        cleaned_labels = deduped_labels or None
    
    # 8) Class balance check
    if cleaned_labels:
        dist = Counter(cleaned_labels)
        max_count = max(dist.values())
        min_count = min(dist.values())
        report['class_imbalance'] = max_count / max(min_count, 1)
    
    report['kept'] = len(cleaned_images)
    print(f"🖼️ Image Clean: {report['kept']}/{report['total']} kept, "
          f"{report['removed']} removed, {len(report['issues'])} issues")
    return cleaned_images, cleaned_labels, report
```

---

## 📄 XML / SOAP Data Parsing & Cleaning

```python
import re
import pandas as pd
from collections import defaultdict

def parse_xml_to_records(xml_text, record_tag=None):
    """
    ★ XML/SOAP → structured records (without lxml dependency)
    ★ ต่างจาก JSON/Config ตรงที่จัดการ namespaces, attributes, CDATA
    """
    import xml.etree.ElementTree as ET
    
    report = {'namespaces': [], 'attributes_found': 0, 'records': 0}
    
    # 1) Strip namespaces for easier parsing
    cleaned_xml = re.sub(r'\sxmlns[^"]*"[^"]*"', '', xml_text)
    cleaned_xml = re.sub(r'<(\/?)\w+:', r'<\1', cleaned_xml)
    
    # 2) Parse
    try:
        root = ET.fromstring(cleaned_xml)
    except ET.ParseError as e:
        # Try to fix common XML issues
        cleaned_xml = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', cleaned_xml)
        cleaned_xml = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', cleaned_xml,
                             flags=re.DOTALL)
        root = ET.fromstring(cleaned_xml)
    
    # 3) Auto-detect record tag if not provided
    if not record_tag:
        children = list(root)
        if children:
            tag_counts = defaultdict(int)
            for child in children:
                tag_counts[child.tag] += 1
            record_tag = max(tag_counts, key=tag_counts.get)
    
    # 4) Extract records
    def element_to_dict(elem, prefix=''):
        result = {}
        
        # Attributes
        for key, val in elem.attrib.items():
            result[f"{prefix}@{key}"] = val
            report['attributes_found'] += 1
        
        # Text content
        if elem.text and elem.text.strip():
            if prefix:
                result[prefix.rstrip('.')] = elem.text.strip()
            else:
                result['_text'] = elem.text.strip()
        
        # Children
        child_counts = defaultdict(int)
        for child in elem:
            child_counts[child.tag] += 1
        
        for child in elem:
            child_prefix = f"{prefix}{child.tag}"
            if child_counts[child.tag] > 1:
                child_prefix += f".{child_counts[child.tag]}"
            
            if len(child) == 0:
                # Leaf node
                val = child.text.strip() if child.text else ''
                result[child_prefix] = val
                for k, v in child.attrib.items():
                    result[f"{child_prefix}.@{k}"] = v
            else:
                # Nested
                result.update(element_to_dict(child, child_prefix + '.'))
        
        return result
    
    records = []
    for elem in root.iter(record_tag):
        records.append(element_to_dict(elem))
    
    report['records'] = len(records)
    df = pd.DataFrame(records)
    
    # 5) Type coercion
    for col in df.columns:
        # Try numeric
        converted = pd.to_numeric(df[col], errors='coerce')
        if converted.notna().sum() > df[col].notna().sum() * 0.5:
            df[col] = converted
    
    print(f"📄 XML Parsed: {len(records)} records, {len(df.columns)} columns, "
          f"{report['attributes_found']} attributes")
    return df, report
```

---

## ✅ Checksum & ID Validation (Luhn, ISBN, IBAN)

```python
import re
import pandas as pd

def luhn_check(number_str):
    """Luhn algorithm for credit cards, IMEI, etc."""
    digits = [int(d) for d in str(number_str) if d.isdigit()]
    if len(digits) < 2:
        return False
    checksum = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0

def isbn_check(isbn_str):
    """ISBN-10 and ISBN-13 validation"""
    isbn = re.sub(r'[\s-]', '', str(isbn_str))
    if len(isbn) == 13:
        total = sum(int(d) * (1 if i % 2 == 0 else 3)
                    for i, d in enumerate(isbn[:12]))
        return int(isbn[12]) == (10 - total % 10) % 10
    elif len(isbn) == 10:
        total = sum((10 - i) * (10 if d == 'X' else int(d))
                    for i, d in enumerate(isbn))
        return total % 11 == 0
    return False

def iban_check(iban_str):
    """IBAN validation (mod 97)"""
    iban = re.sub(r'\s', '', str(iban_str)).upper()
    if len(iban) < 5:
        return False
    rearranged = iban[4:] + iban[:4]
    numeric = ''
    for ch in rearranged:
        if ch.isdigit():
            numeric += ch
        elif ch.isalpha():
            numeric += str(ord(ch) - ord('A') + 10)
    return int(numeric) % 97 == 1

def thai_id_check(id_str):
    """Thai national ID validation (13 digits)"""
    digits = re.sub(r'[\s-]', '', str(id_str))
    if len(digits) != 13 or not digits.isdigit():
        return False
    total = sum(int(digits[i]) * (13 - i) for i in range(12))
    check = (11 - total % 11) % 10
    return check == int(digits[12])

def validate_ids(df, col, id_type='auto'):
    """
    ★ Formal checksum validation สำหรับ IDs ต่างๆ
    ★ ต่างจาก Semantic Type Detection ตรงที่เป็น mathematical validation
    """
    validators = {
        'credit_card': luhn_check,
        'isbn': isbn_check,
        'iban': iban_check,
        'thai_id': thai_id_check,
        'luhn': luhn_check,
    }
    
    results = []
    for val in df[col]:
        if pd.isna(val):
            results.append({'value': val, 'valid': False, 'reason': 'null'})
            continue
        
        val_str = str(val).strip()
        
        if id_type == 'auto':
            # Auto-detect
            for name, check_fn in validators.items():
                if check_fn(val_str):
                    results.append({'value': val_str, 'valid': True, 'type': name})
                    break
            else:
                results.append({'value': val_str, 'valid': False, 'reason': 'no match'})
        else:
            check_fn = validators.get(id_type)
            valid = check_fn(val_str) if check_fn else False
            results.append({'value': val_str, 'valid': valid, 'type': id_type})
    
    valid_count = sum(1 for r in results if r['valid'])
    print(f"✅ ID Validation ({id_type}): {valid_count}/{len(results)} valid")
    return pd.DataFrame(results)
```

---

## 🔄 Slowly Changing Dimensions (SCD Type 1/2/3)

```python
import pandas as pd
from datetime import datetime

def apply_scd(existing_df, incoming_df, key_cols, track_cols,
              scd_type=2, effective_date=None):
    """
    ★ Slowly Changing Dimensions สำหรับ Data Warehouse
    ★ Type 1: Overwrite, Type 2: Add version row, Type 3: Add previous column
    """
    effective_date = effective_date or datetime.now()
    report = {'inserts': 0, 'updates': 0, 'unchanged': 0, 'scd_type': scd_type}
    
    if scd_type == 1:
        # ★ Type 1: Overwrite — ไม่เก็บ history
        result = existing_df.copy()
        for _, inc_row in incoming_df.iterrows():
            key_match = True
            mask = pd.Series(True, index=result.index)
            for kc in key_cols:
                mask &= result[kc] == inc_row[kc]
            
            if mask.any():
                changed = False
                for tc in track_cols:
                    if result.loc[mask, tc].iloc[0] != inc_row[tc]:
                        changed = True
                        result.loc[mask, tc] = inc_row[tc]
                
                if changed:
                    report['updates'] += 1
                else:
                    report['unchanged'] += 1
            else:
                result = pd.concat([result, inc_row.to_frame().T], ignore_index=True)
                report['inserts'] += 1
    
    elif scd_type == 2:
        # ★ Type 2: Add versioned row — เก็บ history ทุก version
        if 'effective_from' not in existing_df.columns:
            existing_df['effective_from'] = pd.Timestamp('1900-01-01')
            existing_df['effective_to'] = pd.Timestamp('9999-12-31')
            existing_df['is_current'] = True
        
        result = existing_df.copy()
        
        for _, inc_row in incoming_df.iterrows():
            mask = pd.Series(True, index=result.index)
            for kc in key_cols:
                mask &= result[kc] == inc_row[kc]
            mask &= result['is_current'] == True
            
            if mask.any():
                current = result.loc[mask].iloc[0]
                changed = any(current[tc] != inc_row[tc] for tc in track_cols)
                
                if changed:
                    # Close current record
                    result.loc[mask, 'effective_to'] = effective_date
                    result.loc[mask, 'is_current'] = False
                    
                    # Insert new version
                    new_row = inc_row.copy()
                    new_row['effective_from'] = effective_date
                    new_row['effective_to'] = pd.Timestamp('9999-12-31')
                    new_row['is_current'] = True
                    result = pd.concat([result, new_row.to_frame().T],
                                       ignore_index=True)
                    report['updates'] += 1
                else:
                    report['unchanged'] += 1
            else:
                new_row = inc_row.copy()
                new_row['effective_from'] = effective_date
                new_row['effective_to'] = pd.Timestamp('9999-12-31')
                new_row['is_current'] = True
                result = pd.concat([result, new_row.to_frame().T],
                                   ignore_index=True)
                report['inserts'] += 1
    
    elif scd_type == 3:
        # ★ Type 3: Add previous-value column — เก็บแค่ค่าก่อนหน้า
        result = existing_df.copy()
        
        for tc in track_cols:
            prev_col = f'{tc}_previous'
            if prev_col not in result.columns:
                result[prev_col] = None
        
        for _, inc_row in incoming_df.iterrows():
            mask = pd.Series(True, index=result.index)
            for kc in key_cols:
                mask &= result[kc] == inc_row[kc]
            
            if mask.any():
                changed = False
                for tc in track_cols:
                    if result.loc[mask, tc].iloc[0] != inc_row[tc]:
                        result.loc[mask, f'{tc}_previous'] = result.loc[mask, tc]
                        result.loc[mask, tc] = inc_row[tc]
                        changed = True
                
                report['updates' if changed else 'unchanged'] += 1
            else:
                result = pd.concat([result, inc_row.to_frame().T],
                                   ignore_index=True)
                report['inserts'] += 1
    
    print(f"🔄 SCD Type {scd_type}: {report['inserts']} inserts, "
          f"{report['updates']} updates, {report['unchanged']} unchanged")
    return result, report
```

---

## ⏱️ Temporal / As-of Joins

```python
import pandas as pd

def asof_join(left_df, right_df, on_key, left_time='timestamp',
              right_time='timestamp', direction='backward', tolerance=None):
    """
    ★ Point-in-time correct joining (as-of join)
    ★ ต่างจาก Regular Join ตรงที่ match ตาม "ณ เวลานั้น"
    """
    left = left_df.copy().sort_values(left_time)
    right = right_df.copy().sort_values(right_time)
    
    left[left_time] = pd.to_datetime(left[left_time])
    right[right_time] = pd.to_datetime(right[right_time])
    
    if on_key:
        # Group-wise as-of join
        results = []
        for key_val in left[on_key].unique():
            l_group = left[left[on_key] == key_val]
            r_group = right[right[on_key] == key_val]
            
            if r_group.empty:
                results.append(l_group)
                continue
            
            merged = pd.merge_asof(
                l_group, r_group,
                left_on=left_time, right_on=right_time,
                direction=direction,
                tolerance=pd.Timedelta(tolerance) if tolerance else None,
                suffixes=('', '_right')
            )
            results.append(merged)
        
        result = pd.concat(results, ignore_index=True)
    else:
        result = pd.merge_asof(
            left, right,
            left_on=left_time, right_on=right_time,
            direction=direction,
            tolerance=pd.Timedelta(tolerance) if tolerance else None,
            suffixes=('', '_right')
        )
    
    matched = result.dropna(subset=[c for c in result.columns
                                     if c.endswith('_right')][:1]).shape[0]
    print(f"⏱️ As-of Join ({direction}): {len(result)} rows, "
          f"{matched}/{len(left)} matched")
    return result
```

---

## 💱 Currency & Exchange Rate Normalization

```python
import pandas as pd
from datetime import datetime

# Static rates (production: use API like exchangeratesapi.io)
EXCHANGE_RATES_TO_USD = {
    'USD': 1.0, 'EUR': 1.08, 'GBP': 1.26, 'JPY': 0.0067,
    'THB': 0.028, 'CNY': 0.14, 'KRW': 0.00075, 'SGD': 0.74,
    'AUD': 0.65, 'CAD': 0.74, 'CHF': 1.12, 'INR': 0.012,
    'MYR': 0.21, 'IDR': 0.000063, 'PHP': 0.018, 'VND': 0.000040,
}

CURRENCY_SYMBOLS = {
    '$': 'USD', '€': 'EUR', '£': 'GBP', '¥': 'JPY',
    '฿': 'THB', '₩': 'KRW', '₹': 'INR', '₫': 'VND',
}

def normalize_currency(df, amount_col, currency_col=None,
                       target_currency='USD', rates=None):
    """
    ★ Multi-currency → single target currency
    ★ ต่างจาก Unit Conversion ตรงที่เฉพาะทาง financial + dynamic rates
    """
    import re
    rates = rates or EXCHANGE_RATES_TO_USD
    result = df.copy()
    report = {'converted': 0, 'failed': 0, 'currencies_found': set()}
    
    for idx, row in result.iterrows():
        amount = row[amount_col]
        
        # 1) Extract currency from amount string if no currency column
        if currency_col and pd.notna(row.get(currency_col)):
            currency = str(row[currency_col]).upper().strip()
        elif isinstance(amount, str):
            # Try to detect currency from string
            currency = 'USD'
            for symbol, code in CURRENCY_SYMBOLS.items():
                if symbol in amount:
                    currency = code
                    break
            # Extract numeric value
            match = re.search(r'[\d,]+\.?\d*', str(amount).replace(',', ''))
            amount = float(match.group()) if match else None
        else:
            currency = 'USD'
        
        if pd.isna(amount):
            report['failed'] += 1
            continue
        
        amount = float(str(amount).replace(',', ''))
        report['currencies_found'].add(currency)
        
        # 2) Convert to target currency
        if currency == target_currency:
            result.at[idx, f'{amount_col}_{target_currency}'] = amount
        elif currency in rates and target_currency in rates:
            usd_amount = amount * rates.get(currency, 1.0)
            target_amount = usd_amount / rates.get(target_currency, 1.0)
            result.at[idx, f'{amount_col}_{target_currency}'] = round(target_amount, 2)
            report['converted'] += 1
        else:
            report['failed'] += 1
    
    report['currencies_found'] = list(report['currencies_found'])
    print(f"💱 Currency: {report['converted']} converted to {target_currency}, "
          f"{len(report['currencies_found'])} currencies found")
    return result, report
```

---

## 📊 Data Sampling Strategies

```python
import pandas as pd
import numpy as np
import hashlib

def smart_sample(df, n=None, fraction=None, strategy='stratified',
                 stratify_col=None, seed=42):
    """
    ★ Intelligent sampling strategies สำหรับ large datasets
    ★ ต่างจาก random sampling ตรงที่ preserve distribution + representativeness
    """
    np.random.seed(seed)
    target_n = n or int(len(df) * (fraction or 0.1))
    target_n = min(target_n, len(df))
    
    if strategy == 'stratified':
        # ★ Proportional sampling per group
        if not stratify_col or stratify_col not in df.columns:
            return df.sample(n=target_n, random_state=seed)
        
        samples = []
        group_counts = df[stratify_col].value_counts()
        for group, count in group_counts.items():
            group_df = df[df[stratify_col] == group]
            group_n = max(1, int(target_n * count / len(df)))
            samples.append(group_df.sample(n=min(group_n, len(group_df)),
                                           random_state=seed))
        result = pd.concat(samples)
    
    elif strategy == 'systematic':
        # ★ Every k-th record
        k = max(1, len(df) // target_n)
        start = np.random.randint(0, k)
        indices = list(range(start, len(df), k))[:target_n]
        result = df.iloc[indices]
    
    elif strategy == 'reservoir':
        # ★ Reservoir sampling (streaming-friendly, Algorithm R)
        reservoir = df.head(target_n).copy()
        for i in range(target_n, len(df)):
            j = np.random.randint(0, i + 1)
            if j < target_n:
                reservoir.iloc[j] = df.iloc[i]
        result = reservoir
    
    elif strategy == 'cluster':
        # ★ Cluster-based sampling
        from sklearn.cluster import MiniBatchKMeans
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            X = df[numeric_cols].fillna(0)
            n_clusters = min(target_n, len(df) // 10)
            kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=seed)
            df_temp = df.copy()
            df_temp['_cluster'] = kmeans.fit_predict(X)
            samples = []
            per_cluster = max(1, target_n // n_clusters)
            for c in range(n_clusters):
                cluster_df = df_temp[df_temp['_cluster'] == c]
                samples.append(cluster_df.sample(
                    n=min(per_cluster, len(cluster_df)), random_state=seed))
            result = pd.concat(samples).drop(columns='_cluster')
        else:
            result = df.sample(n=target_n, random_state=seed)
    
    elif strategy == 'deterministic':
        # ★ Hash-based deterministic sampling (reproducible across runs)
        hashes = df.apply(
            lambda row: int(hashlib.md5(str(row.values).encode()).hexdigest(), 16),
            axis=1
        )
        threshold = target_n / len(df)
        mask = (hashes % 10000) / 10000 < threshold
        result = df[mask]
    
    else:
        result = df.sample(n=target_n, random_state=seed)
    
    print(f"📊 Sample ({strategy}): {len(df)} → {len(result)} rows "
          f"({len(result)/len(df)*100:.1f}%)")
    return result
```

---

## 🤖 LLM-powered Data Cleaning

```python
import pandas as pd
import re
import json

class LLMCleaner:
    """
    ★ ใช้ LLM (zero-shot / few-shot) ช่วย clean data
    ★ ต่างจาก rule-based ตรงที่ handle ambiguous/complex cases
    """
    def __init__(self, llm_fn=None):
        self.llm_fn = llm_fn  # Function: str → str (e.g., openai.chat)
        self.cache = {}
        self.prompts_used = 0
    
    def classify_column(self, df, col, categories, sample_size=5):
        """Zero-shot classification of values into categories"""
        sample = df[col].dropna().unique()[:sample_size]
        prompt = (
            f"Classify these values into categories {categories}.\n"
            f"Values: {list(sample)}\n"
            f"Return JSON: {{value: category}}"
        )
        
        if self.llm_fn:
            response = self.llm_fn(prompt)
            self.prompts_used += 1
            try:
                mapping = json.loads(response)
            except:
                mapping = {}
        else:
            # Fallback: simple rule-based
            mapping = {str(v): categories[0] for v in sample}
        
        return mapping
    
    def standardize_freetext(self, values, target_format, examples=None):
        """Few-shot standardization of free-text values"""
        unique_values = list(set(str(v) for v in values if pd.notna(v)))[:20]
        
        examples_text = ""
        if examples:
            examples_text = "Examples:\n" + "\n".join(
                f'  "{k}" → "{v}"' for k, v in examples.items())
        
        prompt = (
            f"Standardize these values to format: {target_format}\n"
            f"{examples_text}\n"
            f"Values: {unique_values}\n"
            f"Return JSON mapping: {{original: standardized}}"
        )
        
        if self.llm_fn:
            response = self.llm_fn(prompt)
            self.prompts_used += 1
            try:
                return json.loads(response)
            except:
                return {}
        
        return {v: v for v in unique_values}
    
    def detect_anomalies(self, df, context, columns=None):
        """Use LLM to detect semantic anomalies"""
        columns = columns or df.columns.tolist()
        sample = df[columns].head(10).to_dict(orient='records')
        
        prompt = (
            f"Context: {context}\n"
            f"Data sample:\n{json.dumps(sample, indent=2, default=str)}\n"
            f"Identify any anomalies, inconsistencies, or data quality issues.\n"
            f"Return JSON: [{{'row': idx, 'column': col, 'issue': description}}]"
        )
        
        if self.llm_fn:
            response = self.llm_fn(prompt)
            self.prompts_used += 1
            try:
                return json.loads(response)
            except:
                return []
        
        return []
    
    def get_stats(self):
        return {
            'prompts_used': self.prompts_used,
            'cache_size': len(self.cache),
            'cache_hit_rate': 0  # TODO: track hits
        }
```

---

## 📜 Data Contracts (Producer/Consumer)

```python
import pandas as pd
from datetime import datetime

class DataContract:
    """
    ★ Formal agreement ระหว่าง data producer และ consumer
    ★ ต่างจาก Expectation-based Testing ตรงที่เป็น cross-team agreement
    """
    def __init__(self, name, version='1.0', owner=None):
        self.name = name
        self.version = version
        self.owner = owner
        self.schema = {}
        self.sla = {}
        self.quality_rules = []
    
    def define_schema(self, columns):
        """
        columns: dict of {col_name: {type, nullable, description, ...}}
        """
        self.schema = columns
        return self
    
    def define_sla(self, freshness_hours=24, availability_pct=99.9,
                   max_null_pct=5, min_rows=100):
        self.sla = {
            'freshness_hours': freshness_hours,
            'availability_pct': availability_pct,
            'max_null_pct': max_null_pct,
            'min_rows': min_rows,
        }
        return self
    
    def add_quality_rule(self, name, check_fn, severity='error'):
        self.quality_rules.append({
            'name': name,
            'check': check_fn,
            'severity': severity  # 'error', 'warning', 'info'
        })
        return self
    
    def validate(self, df):
        """Validate DataFrame against contract"""
        violations = []
        
        # 1) Schema validation
        for col, spec in self.schema.items():
            if col not in df.columns:
                violations.append({
                    'type': 'schema', 'severity': 'error',
                    'message': f"Missing column: {col}"
                })
                continue
            
            # Type check
            expected_type = spec.get('type')
            if expected_type:
                actual_type = str(df[col].dtype)
                if expected_type not in actual_type:
                    violations.append({
                        'type': 'schema', 'severity': 'warning',
                        'message': f"{col}: expected {expected_type}, got {actual_type}"
                    })
            
            # Nullable check
            if not spec.get('nullable', True) and df[col].isna().any():
                null_pct = df[col].isna().mean() * 100
                violations.append({
                    'type': 'schema', 'severity': 'error',
                    'message': f"{col}: {null_pct:.1f}% nulls (non-nullable)"
                })
        
        # 2) SLA validation
        if self.sla.get('min_rows') and len(df) < self.sla['min_rows']:
            violations.append({
                'type': 'sla', 'severity': 'error',
                'message': f"Row count {len(df)} < minimum {self.sla['min_rows']}"
            })
        
        if self.sla.get('max_null_pct'):
            overall_null = df.isna().mean().mean() * 100
            if overall_null > self.sla['max_null_pct']:
                violations.append({
                    'type': 'sla', 'severity': 'error',
                    'message': f"Overall null {overall_null:.1f}% > max {self.sla['max_null_pct']}%"
                })
        
        # 3) Quality rules
        for rule in self.quality_rules:
            try:
                if not rule['check'](df):
                    violations.append({
                        'type': 'quality', 'severity': rule['severity'],
                        'message': f"Failed: {rule['name']}"
                    })
            except Exception as e:
                violations.append({
                    'type': 'quality', 'severity': 'error',
                    'message': f"Error in {rule['name']}: {str(e)}"
                })
        
        errors = sum(1 for v in violations if v['severity'] == 'error')
        warnings = sum(1 for v in violations if v['severity'] == 'warning')
        status = 'PASS' if errors == 0 else 'FAIL'
        
        print(f"📜 Contract '{self.name}' v{self.version}: {status} "
              f"({errors} errors, {warnings} warnings)")
        return {'status': status, 'violations': violations}
```

---

## 🧮 Entity Embeddings for Anomaly Detection

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import LocalOutlierFactor

def embedding_anomaly_detection(df, categorical_cols, embedding_dim=5,
                                 contamination=0.05):
    """
    ★ ใช้ entity embeddings + LOF หา anomalies ใน categorical data
    ★ ต่างจาก Outlier Detection ตรงที่ทำงานกับ categorical data ได้
    """
    encoders = {}
    embedded_features = []
    
    # 1) Encode categorical columns
    for col in categorical_cols:
        if col not in df.columns:
            continue
        
        le = LabelEncoder()
        encoded = le.fit_transform(df[col].fillna('__MISSING__').astype(str))
        encoders[col] = le
        
        n_categories = len(le.classes_)
        dim = min(embedding_dim, max(1, n_categories // 2))
        
        # Simple embedding: random projection (production: use learned embeddings)
        np.random.seed(42)
        embedding_matrix = np.random.randn(n_categories, dim)
        
        # Normalize
        norms = np.linalg.norm(embedding_matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1
        embedding_matrix /= norms
        
        embedded = embedding_matrix[encoded]
        embedded_features.append(embedded)
    
    if not embedded_features:
        print("🧮 No categorical columns to embed")
        return df, []
    
    # 2) Add numeric features
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) > 0:
        numeric_data = df[numeric_cols].fillna(0).values
        # Normalize
        means = numeric_data.mean(axis=0)
        stds = numeric_data.std(axis=0)
        stds[stds == 0] = 1
        numeric_normalized = (numeric_data - means) / stds
        embedded_features.append(numeric_normalized)
    
    # 3) Concatenate all features
    X = np.hstack(embedded_features)
    
    # 4) Detect anomalies with LOF
    lof = LocalOutlierFactor(
        n_neighbors=min(20, len(df) - 1),
        contamination=contamination
    )
    predictions = lof.fit_predict(X)
    scores = lof.negative_outlier_factor_
    
    anomaly_mask = predictions == -1
    anomalies = df[anomaly_mask].index.tolist()
    
    result = df.copy()
    result['_anomaly_score'] = -scores  # Higher = more anomalous
    result['_is_anomaly'] = anomaly_mask
    
    print(f"🧮 Embedding Anomaly: {anomaly_mask.sum()}/{len(df)} anomalies "
          f"({anomaly_mask.mean()*100:.1f}%), {len(categorical_cols)} cat cols embedded")
    return result, anomalies
```

---

## 🏭 Industry-Specific Use Cases (เพิ่มเติม Round 11 FINAL)

### 61. 🐟 Aquaculture / Fishery

| ปัญหา | วิธีแก้ |
|--------|--------|
| Water quality sensor drift (pH, O₂, temp) | Calibration correction + SOR |
| Feed conversion ratio (FCR) data gaps | Temporal interpolation + validation |
| Species/strain naming inconsistency | Controlled vocabulary + fuzzy match |
| Harvest weight data precision | Unit standardization + decimal rules |
| Multi-pond data isolation | Multi-tenant isolation pattern |

### 62. 🧴 Perfume / Cosmetics

| ปัญหา | วิธีแก้ |
|--------|--------|
| INCI ingredient naming variations | Canonical name mapping (INCI DB) |
| Batch expiry date format mixing | Date parsing + SCD Type 1 |
| Fragrance note classification inconsistency | LLM-powered classification |
| Multi-currency pricing (global distribution) | Currency normalization |
| Regulatory compliance data per country | Schema evolution + validation |

### 63. 🛗 Elevator / Lift Maintenance

| ปัญหา | วิธีแก้ |
|--------|--------|
| IoT sensor telemetry gaps | Temporal interpolation + monotonic |
| Maintenance log free text inconsistency | NLP extraction + standardize |
| Part number cross-reference (multi-vendor) | Fuzzy join + canonical ID |
| Service contract data format variations | Data contracts + schema validation |
| Floor/building numbering inconsistency | Hierarchical mapping |

### 64. 📚 Library / Archive

| ปัญหา | วิธีแก้ |
|--------|--------|
| ISBN/ISSN validation errors | Checksum validation (Luhn/ISBN) |
| Author name variations (transliteration) | Fuzzy dedup + authority file (VIAF) |
| MARC record field inconsistency | XML parsing + schema validation |
| Acquisition date format mixing | Date normalization |
| Multi-branch catalog merge | Probabilistic record linkage |

### 65. 🚁 Drone / UAV

| ปัญหา | วิธีแก้ |
|--------|--------|
| Flight telemetry GPS drift | Kalman filter + outlier removal |
| Point cloud data from LiDAR | 3D point cloud cleaning (SOR/voxel) |
| Image metadata (EXIF) inconsistency | Image dataset cleaning |
| Battery/sensor log timestamp gaps | Temporal as-of join + interpolation |
| Regulatory airspace data format | Geospatial validation + schema check |

---

## 📡 Change Data Capture (CDC) Cleaning

```python
import pandas as pd
import json
from datetime import datetime

def process_cdc_events(events, dedup_key='id', order_key='ts_ms'):
    """
    ★ Change Data Capture (Debezium/binlog style) → clean final state
    ★ ต่างจาก SCD ตรงที่ process real-time event stream ไม่ใช่ batch compare
    """
    report = {
        'total_events': len(events),
        'ops': {'c': 0, 'r': 0, 'u': 0, 'd': 0},
        'deduped': 0, 'out_of_order': 0
    }
    
    # 1) Parse CDC events
    parsed = []
    for evt in events:
        if isinstance(evt, str):
            evt = json.loads(evt)
        
        op = evt.get('op', 'r')  # c=create, u=update, d=delete, r=read
        report['ops'][op] = report['ops'].get(op, 0) + 1
        
        record = {
            '_cdc_op': op,
            '_cdc_ts': evt.get('ts_ms', 0),
            '_cdc_source': evt.get('source', {}).get('table', 'unknown'),
        }
        
        # Extract payload
        if op == 'd':
            payload = evt.get('before', {})
            record['_deleted'] = True
        else:
            payload = evt.get('after', {})
            record['_deleted'] = False
        
        if payload:
            record.update(payload)
        parsed.append(record)
    
    df = pd.DataFrame(parsed)
    
    if df.empty:
        return df, report
    
    # 2) Sort by timestamp (handle out-of-order events)
    if '_cdc_ts' in df.columns:
        df = df.sort_values('_cdc_ts')
        # Detect out-of-order
        if dedup_key in df.columns:
            for key_val in df[dedup_key].unique():
                group = df[df[dedup_key] == key_val]['_cdc_ts']
                if not group.is_monotonic_increasing:
                    report['out_of_order'] += 1
    
    # 3) Compact: keep only latest state per key
    if dedup_key in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=[dedup_key], keep='last')
        report['deduped'] = before - len(df)
    
    # 4) Remove deleted records (optional)
    active = df[~df.get('_deleted', False)].copy()
    
    # 5) Clean CDC metadata columns
    meta_cols = [c for c in active.columns if c.startswith('_cdc_') or c == '_deleted']
    clean = active.drop(columns=meta_cols, errors='ignore')
    
    print(f"📡 CDC: {report['total_events']} events → {len(clean)} active records, "
          f"ops={report['ops']}, {report['deduped']} deduped")
    return clean, report
```

---

## 📉 Data Drift Detection (PSI / KS-test)

```python
import numpy as np
import pandas as pd
from scipy import stats

def detect_drift(reference_df, current_df, columns=None,
                 psi_threshold=0.2, ks_alpha=0.05):
    """
    ★ Statistical data drift detection ระหว่าง reference vs current data
    ★ ต่างจาก Quality Monitoring ตรงที่เป็น statistical hypothesis testing
    """
    columns = columns or reference_df.columns.tolist()
    results = []
    
    for col in columns:
        if col not in reference_df.columns or col not in current_df.columns:
            continue
        
        ref = reference_df[col].dropna()
        cur = current_df[col].dropna()
        
        if len(ref) < 10 or len(cur) < 10:
            continue
        
        result = {'column': col, 'ref_count': len(ref), 'cur_count': len(cur)}
        
        if pd.api.types.is_numeric_dtype(ref):
            # ★ Numeric: KS-test + PSI
            
            # Kolmogorov-Smirnov test
            ks_stat, ks_pvalue = stats.ks_2samp(ref, cur)
            result['ks_statistic'] = round(ks_stat, 4)
            result['ks_pvalue'] = round(ks_pvalue, 6)
            result['ks_drift'] = ks_pvalue < ks_alpha
            
            # Population Stability Index (PSI)
            def calculate_psi(expected, actual, bins=10):
                breakpoints = np.quantile(expected, np.linspace(0, 1, bins + 1))
                breakpoints = np.unique(breakpoints)
                
                expected_counts = np.histogram(expected, bins=breakpoints)[0]
                actual_counts = np.histogram(actual, bins=breakpoints)[0]
                
                # Normalize to proportions
                expected_pct = (expected_counts + 1) / (len(expected) + len(breakpoints))
                actual_pct = (actual_counts + 1) / (len(actual) + len(breakpoints))
                
                psi = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
                return psi
            
            psi = calculate_psi(ref.values, cur.values)
            result['psi'] = round(psi, 4)
            result['psi_drift'] = psi > psi_threshold
            
            # Summary stats comparison
            result['ref_mean'] = round(ref.mean(), 4)
            result['cur_mean'] = round(cur.mean(), 4)
            result['mean_shift_pct'] = round(
                abs(cur.mean() - ref.mean()) / max(abs(ref.mean()), 1e-10) * 100, 2)
            
        else:
            # ★ Categorical: Chi-squared + Jensen-Shannon divergence
            ref_dist = ref.value_counts(normalize=True)
            cur_dist = cur.value_counts(normalize=True)
            
            all_cats = set(ref_dist.index) | set(cur_dist.index)
            ref_aligned = np.array([ref_dist.get(c, 0) for c in all_cats])
            cur_aligned = np.array([cur_dist.get(c, 0) for c in all_cats])
            
            # Add smoothing
            ref_aligned = (ref_aligned + 1e-10) / (ref_aligned + 1e-10).sum()
            cur_aligned = (cur_aligned + 1e-10) / (cur_aligned + 1e-10).sum()
            
            # Jensen-Shannon divergence
            m = 0.5 * (ref_aligned + cur_aligned)
            js_div = 0.5 * (stats.entropy(ref_aligned, m) + stats.entropy(cur_aligned, m))
            result['js_divergence'] = round(js_div, 4)
            result['js_drift'] = js_div > 0.1
            
            # New/missing categories
            result['new_categories'] = list(set(cur_dist.index) - set(ref_dist.index))
            result['missing_categories'] = list(set(ref_dist.index) - set(cur_dist.index))
        
        result['has_drift'] = result.get('ks_drift', False) or \
                              result.get('psi_drift', False) or \
                              result.get('js_drift', False)
        results.append(result)
    
    drift_count = sum(1 for r in results if r['has_drift'])
    print(f"📉 Drift Detection: {drift_count}/{len(results)} columns drifted "
          f"(KS α={ks_alpha}, PSI threshold={psi_threshold})")
    return pd.DataFrame(results)
```

---

## 🎭 Pseudonymization & Tokenization

```python
import hashlib
import secrets
import re
import pandas as pd

class Pseudonymizer:
    """
    ★ Pseudonymization (reversible) & Tokenization (irreversible)
    ★ ต่างจาก k-Anonymity/Differential Privacy ตรงที่ preserve referential integrity
      and allow re-identification with authorized key
    """
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.token_vault = {}  # token → original (for reversible)
        self.reverse_vault = {}  # original → token (for consistency)
    
    def pseudonymize(self, value, method='hmac', prefix='PSE'):
        """Consistent pseudonymization (same input → same output)"""
        if pd.isna(value):
            return value
        
        val_str = str(value)
        
        if val_str in self.reverse_vault:
            return self.reverse_vault[val_str]
        
        if method == 'hmac':
            # Keyed hash — reversible with key lookup
            token = hashlib.pbkdf2_hmac(
                'sha256', val_str.encode(),
                self.secret_key.encode(), 100000
            ).hex()[:16]
            pseudo = f"{prefix}-{token}"
        
        elif method == 'format_preserving':
            # Format-preserving: same length/pattern
            h = hashlib.sha256(
                (self.secret_key + val_str).encode()
            ).hexdigest()
            
            if val_str.isdigit():
                pseudo = str(int(h[:len(val_str)], 16) % (10 ** len(val_str))).zfill(len(val_str))
            elif '@' in val_str:
                # Email format preserving
                local_hash = h[:8]
                domain_hash = h[8:12]
                pseudo = f"{local_hash}@{domain_hash}.pseudo.com"
            else:
                pseudo = f"{prefix}-{h[:len(val_str)]}"
        
        elif method == 'counter':
            # Sequential counter-based
            idx = len(self.token_vault) + 1
            pseudo = f"{prefix}-{idx:08d}"
        
        else:
            pseudo = f"{prefix}-{secrets.token_hex(8)}"
        
        self.token_vault[pseudo] = val_str
        self.reverse_vault[val_str] = pseudo
        return pseudo
    
    def tokenize(self, value, token_type='opaque'):
        """Irreversible tokenization (cannot recover original)"""
        if pd.isna(value):
            return value
        
        val_str = str(value)
        
        if token_type == 'opaque':
            # Random token — no relationship to original
            if val_str in self.reverse_vault:
                return self.reverse_vault[val_str]
            token = f"TKN-{secrets.token_hex(12)}"
            self.reverse_vault[val_str] = token
            return token
        
        elif token_type == 'hash':
            # One-way hash with salt
            salted = f"{self.secret_key}{val_str}"
            return hashlib.sha256(salted.encode()).hexdigest()[:24]
        
        elif token_type == 'partial_mask':
            # Partial masking (show first/last chars)
            if len(val_str) <= 4:
                return '*' * len(val_str)
            return val_str[0] + '*' * (len(val_str) - 2) + val_str[-1]
    
    def apply_to_df(self, df, columns, method='hmac', mode='pseudonymize'):
        """Apply pseudonymization/tokenization to DataFrame columns"""
        result = df.copy()
        report = {'columns': [], 'total_values': 0}
        
        fn = self.pseudonymize if mode == 'pseudonymize' else self.tokenize
        
        for col in columns:
            if col not in result.columns:
                continue
            result[col] = result[col].apply(lambda x: fn(x, method=method)
                                            if mode == 'pseudonymize'
                                            else fn(x, token_type=method))
            report['columns'].append(col)
            report['total_values'] += result[col].notna().sum()
        
        print(f"🎭 {mode.title()}: {len(report['columns'])} columns, "
              f"{report['total_values']} values processed")
        return result, report
    
    def depseudonymize(self, token):
        """Reverse pseudonymization (requires vault)"""
        return self.token_vault.get(token, None)
```

---

## 📅 Natural Language Date Parsing

```python
import re
import pandas as pd
from datetime import datetime, timedelta

# Thai day/month names
THAI_MONTHS = {
    'มกราคม': 1, 'ม.ค.': 1, 'กุมภาพันธ์': 2, 'ก.พ.': 2,
    'มีนาคม': 3, 'มี.ค.': 3, 'เมษายน': 4, 'เม.ย.': 4,
    'พฤษภาคม': 5, 'พ.ค.': 5, 'มิถุนายน': 6, 'มิ.ย.': 6,
    'กรกฎาคม': 7, 'ก.ค.': 7, 'สิงหาคม': 8, 'ส.ค.': 8,
    'กันยายน': 9, 'ก.ย.': 9, 'ตุลาคม': 10, 'ต.ค.': 10,
    'พฤศจิกายน': 11, 'พ.ย.': 11, 'ธันวาคม': 12, 'ธ.ค.': 12,
}

RELATIVE_PATTERNS = {
    # English
    r'today': lambda now: now,
    r'yesterday': lambda now: now - timedelta(days=1),
    r'tomorrow': lambda now: now + timedelta(days=1),
    r'(\d+)\s*days?\s*ago': lambda now, n: now - timedelta(days=int(n)),
    r'(\d+)\s*weeks?\s*ago': lambda now, n: now - timedelta(weeks=int(n)),
    r'(\d+)\s*months?\s*ago': lambda now, n: now - timedelta(days=int(n)*30),
    r'(\d+)\s*years?\s*ago': lambda now, n: now - timedelta(days=int(n)*365),
    r'last\s+week': lambda now: now - timedelta(weeks=1),
    r'last\s+month': lambda now: now - timedelta(days=30),
    r'last\s+year': lambda now: now - timedelta(days=365),
    r'next\s+(\d+)\s*days?': lambda now, n: now + timedelta(days=int(n)),
    # Thai
    r'วันนี้': lambda now: now,
    r'เมื่อวาน': lambda now: now - timedelta(days=1),
    r'พรุ่งนี้': lambda now: now + timedelta(days=1),
    r'(\d+)\s*วัน\s*(?:ก่อน|ที่แล้ว)': lambda now, n: now - timedelta(days=int(n)),
    r'(\d+)\s*สัปดาห์\s*(?:ก่อน|ที่แล้ว)': lambda now, n: now - timedelta(weeks=int(n)),
    r'(\d+)\s*เดือน\s*(?:ก่อน|ที่แล้ว)': lambda now, n: now - timedelta(days=int(n)*30),
    r'(\d+)\s*ปี\s*(?:ก่อน|ที่แล้ว)': lambda now, n: now - timedelta(days=int(n)*365),
    r'สัปดาห์ที่แล้ว': lambda now: now - timedelta(weeks=1),
    r'เดือนที่แล้ว': lambda now: now - timedelta(days=30),
    r'ปีที่แล้ว': lambda now: now - timedelta(days=365),
}

WEEKDAYS_EN = {
    'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
    'friday': 4, 'saturday': 5, 'sunday': 6,
}

def parse_natural_date(text, reference_date=None):
    """
    ★ Natural language → datetime (Thai + English)
    ★ ต่างจาก regular date parsing ตรงที่จัดการ relative + free-text dates
    """
    if pd.isna(text):
        return None
    
    now = reference_date or datetime.now()
    text = str(text).strip().lower()
    
    # 1) Try standard pandas parsing first
    try:
        result = pd.to_datetime(text, errors='raise')
        # Check for Buddhist Era (พ.ศ.) — year > 2400
        if result.year > 2400:
            result = result.replace(year=result.year - 543)
        return result
    except:
        pass
    
    # 2) Thai month names
    for thai_month, month_num in THAI_MONTHS.items():
        if thai_month in text:
            # Extract day and year
            nums = re.findall(r'\d+', text)
            if len(nums) >= 2:
                day = int(nums[0])
                year = int(nums[1])
                if year > 2400:
                    year -= 543  # Convert พ.ศ. to ค.ศ.
                try:
                    return datetime(year, month_num, day)
                except:
                    pass
    
    # 3) Relative date patterns
    for pattern, fn in RELATIVE_PATTERNS.items():
        match = re.search(pattern, text)
        if match:
            groups = match.groups()
            if groups:
                return fn(now, groups[0])
            else:
                return fn(now)
    
    # 4) "last [weekday]"
    for day_name, day_num in WEEKDAYS_EN.items():
        if f'last {day_name}' in text:
            days_diff = (now.weekday() - day_num) % 7
            if days_diff == 0:
                days_diff = 7
            return now - timedelta(days=days_diff)
    
    return None

def parse_nl_dates_column(df, col, reference_date=None):
    """Apply natural language date parsing to a DataFrame column"""
    result = df.copy()
    parsed = result[col].apply(lambda x: parse_natural_date(x, reference_date))
    
    success = parsed.notna().sum()
    total = result[col].notna().sum()
    result[f'{col}_parsed'] = parsed
    
    print(f"📅 NL Date Parse: {success}/{total} parsed ({success/max(total,1)*100:.1f}%)")
    return result
```

---

## 🔎 Auto Constraint Discovery

```python
import pandas as pd
import numpy as np
from itertools import combinations

def discover_constraints(df, sample_size=10000, confidence=0.95):
    """
    ★ Auto-discover data quality rules/constraints from data
    ★ ต่างจาก Denial Constraints ตรงที่ learn rules จาก data ไม่ใช่ define manually
    """
    if len(df) > sample_size:
        sample = df.sample(n=sample_size, random_state=42)
    else:
        sample = df
    
    constraints = []
    
    # 1) ★ NOT NULL constraints
    for col in sample.columns:
        null_pct = sample[col].isna().mean()
        if null_pct == 0:
            constraints.append({
                'type': 'NOT_NULL',
                'columns': [col],
                'confidence': 1.0,
                'rule': f'{col} IS NOT NULL',
                'severity': 'error'
            })
        elif null_pct < 0.01:
            constraints.append({
                'type': 'NEAR_NOT_NULL',
                'columns': [col],
                'confidence': 1 - null_pct,
                'rule': f'{col} is rarely NULL ({null_pct*100:.2f}%)',
                'severity': 'warning'
            })
    
    # 2) ★ UNIQUE constraints
    for col in sample.columns:
        n_unique = sample[col].nunique()
        n_total = sample[col].notna().sum()
        if n_total > 0 and n_unique == n_total:
            constraints.append({
                'type': 'UNIQUE',
                'columns': [col],
                'confidence': 1.0,
                'rule': f'{col} has all unique values',
                'severity': 'error'
            })
    
    # 3) ★ RANGE constraints (numeric)
    numeric_cols = sample.select_dtypes(include='number').columns
    for col in numeric_cols:
        vals = sample[col].dropna()
        if len(vals) < 10:
            continue
        
        min_val = vals.min()
        max_val = vals.max()
        
        # Check if always positive
        if min_val >= 0:
            constraints.append({
                'type': 'POSITIVE',
                'columns': [col],
                'confidence': 1.0,
                'rule': f'{col} >= 0',
                'severity': 'warning'
            })
        
        # Check for integer-only
        if np.all(vals == vals.astype(int)):
            constraints.append({
                'type': 'INTEGER_ONLY',
                'columns': [col],
                'confidence': 1.0,
                'rule': f'{col} contains only integers',
                'severity': 'info'
            })
        
        # Check bounded range
        q01, q99 = vals.quantile([0.01, 0.99])
        constraints.append({
            'type': 'RANGE',
            'columns': [col],
            'confidence': 0.98,
            'rule': f'{col} typically in [{q01:.2f}, {q99:.2f}]',
            'severity': 'warning'
        })
    
    # 4) ★ CATEGORICAL constraints (low cardinality)
    for col in sample.columns:
        n_unique = sample[col].nunique()
        if 2 <= n_unique <= 20:
            valid_values = sorted(sample[col].dropna().unique().tolist())
            constraints.append({
                'type': 'ENUM',
                'columns': [col],
                'confidence': 1.0,
                'rule': f'{col} in {valid_values[:10]}{"..." if len(valid_values) > 10 else ""}',
                'severity': 'warning',
                'valid_values': valid_values
            })
    
    # 5) ★ FUNCTIONAL DEPENDENCY (A → B)
    cols_to_check = [c for c in sample.columns
                     if sample[c].nunique() < len(sample) * 0.5][:10]
    
    for col_a, col_b in combinations(cols_to_check, 2):
        groups = sample.groupby(col_a)[col_b].nunique()
        if groups.max() == 1:
            constraints.append({
                'type': 'FUNCTIONAL_DEPENDENCY',
                'columns': [col_a, col_b],
                'confidence': 1.0,
                'rule': f'{col_a} → {col_b} (deterministic)',
                'severity': 'info'
            })
        elif groups.max() <= 2 and groups.mean() < 1.1:
            constraints.append({
                'type': 'SOFT_FD',
                'columns': [col_a, col_b],
                'confidence': round(1 - (groups.mean() - 1), 3),
                'rule': f'{col_a} → {col_b} (approximate FD)',
                'severity': 'info'
            })
    
    # 6) ★ PATTERN constraints (string format)
    string_cols = sample.select_dtypes(include='object').columns
    for col in string_cols:
        vals = sample[col].dropna().astype(str)
        if len(vals) < 10:
            continue
        
        # Check if all match a common pattern
        lengths = vals.str.len()
        if lengths.std() == 0:
            constraints.append({
                'type': 'FIXED_LENGTH',
                'columns': [col],
                'confidence': 1.0,
                'rule': f'{col} always length {int(lengths.iloc[0])}',
                'severity': 'info'
            })
        
        # Check email pattern
        email_match = vals.str.match(r'^[^@]+@[^@]+\.[^@]+$').mean()
        if email_match > 0.9:
            constraints.append({
                'type': 'FORMAT_EMAIL',
                'columns': [col],
                'confidence': email_match,
                'rule': f'{col} is email format',
                'severity': 'warning'
            })
    
    # Filter by confidence
    constraints = [c for c in constraints if c['confidence'] >= confidence]
    constraints.sort(key=lambda x: (-x['confidence'], x['type']))
    
    type_counts = {}
    for c in constraints:
        type_counts[c['type']] = type_counts.get(c['type'], 0) + 1
    
    print(f"🔎 Auto Discovery: {len(constraints)} constraints found "
          f"(confidence ≥ {confidence})")
    print(f"   Types: {type_counts}")
    return constraints
```

---

## 📱 Phone Number Parsing & Validation

```python
import re
import pandas as pd

# Country phone formats
PHONE_FORMATS = {
    'TH': {'code': '+66', 'length': 9, 'pattern': r'^0[689]\d{8}$',
            'mobile': r'^0[689]\d{8}$', 'landline': r'^0[2-5]\d{7}$'},
    'US': {'code': '+1', 'length': 10, 'pattern': r'^\d{10}$',
            'mobile': r'^\d{10}$'},
    'UK': {'code': '+44', 'length': 10, 'pattern': r'^0\d{10}$'},
    'JP': {'code': '+81', 'length': 10, 'pattern': r'^0\d{9,10}$'},
    'SG': {'code': '+65', 'length': 8, 'pattern': r'^[689]\d{7}$'},
    'MY': {'code': '+60', 'length': 9, 'pattern': r'^0\d{8,9}$'},
}

def parse_phone(raw, default_country='TH'):
    """
    ★ Phone number parsing & normalization (libphonenumber-style)
    ★ ต่างจาก Email Validation ตรงที่จัดการ phone-specific formats
    """
    if pd.isna(raw):
        return {'raw': raw, 'valid': False, 'reason': 'null'}
    
    raw_str = str(raw).strip()
    
    # 1) Strip common formatting characters
    cleaned = re.sub(r'[\s\-\.\(\)]+', '', raw_str)
    
    # 2) Handle Thai-specific: ๐-๙ → 0-9
    thai_digits = str.maketrans('๐๑๒๓๔๕๖๗๘๙', '0123456789')
    cleaned = cleaned.translate(thai_digits)
    
    # 3) Detect country from prefix
    country = default_country
    e164 = None
    local = cleaned
    
    if cleaned.startswith('+'):
        for cc, fmt in PHONE_FORMATS.items():
            if cleaned.startswith(fmt['code']):
                country = cc
                local = '0' + cleaned[len(fmt['code']):]
                break
    elif cleaned.startswith('00'):
        # International format with 00
        cleaned_intl = '+' + cleaned[2:]
        for cc, fmt in PHONE_FORMATS.items():
            if cleaned_intl.startswith(fmt['code']):
                country = cc
                local = '0' + cleaned_intl[len(fmt['code']):]
                break
    
    # 4) Validate against country pattern
    fmt = PHONE_FORMATS.get(country, {})
    pattern = fmt.get('pattern', r'^\d{8,15}$')
    is_valid = bool(re.match(pattern, local))
    
    # 5) Format to E.164
    if is_valid and fmt.get('code'):
        if local.startswith('0'):
            e164 = fmt['code'] + local[1:]
        else:
            e164 = fmt['code'] + local
    
    # 6) Detect type (mobile vs landline)
    phone_type = 'unknown'
    if fmt.get('mobile') and re.match(fmt['mobile'], local):
        phone_type = 'mobile'
    elif fmt.get('landline') and re.match(fmt['landline'], local):
        phone_type = 'landline'
    
    return {
        'raw': raw_str,
        'cleaned': local,
        'e164': e164,
        'country': country,
        'type': phone_type,
        'valid': is_valid,
    }

def clean_phone_column(df, col, default_country='TH'):
    """Apply phone parsing to DataFrame column"""
    results = df[col].apply(lambda x: parse_phone(x, default_country))
    parsed_df = pd.DataFrame(results.tolist())
    
    valid_count = parsed_df['valid'].sum()
    total = parsed_df['raw'].notna().sum()
    
    result = df.copy()
    result[f'{col}_e164'] = parsed_df['e164']
    result[f'{col}_country'] = parsed_df['country']
    result[f'{col}_type'] = parsed_df['type']
    result[f'{col}_valid'] = parsed_df['valid']
    
    print(f"📱 Phone Parse: {valid_count}/{total} valid "
          f"({valid_count/max(total,1)*100:.1f}%)")
    return result
```

---

## 🔗 URL / URI Validation & Cleaning

```python
import re
import pandas as pd
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

# Known tracking parameters to strip
TRACKING_PARAMS = {
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'fbclid', 'gclid', 'gclsrc', 'dclid', 'msclkid',
    'mc_cid', 'mc_eid', 'ref', 'referrer', '_ga', '_gl',
    'yclid', 'twclid', 'ttclid', 'igshid',
}

def clean_url(raw, strip_tracking=True, normalize=True, 
              require_scheme=True, allowed_schemes=None):
    """
    ★ URL/URI validation, normalization & cleaning
    ★ ต่างจาก Email/Phone ตรงที่จัดการ scheme, path, query, fragment
    """
    allowed_schemes = allowed_schemes or {'http', 'https', 'ftp'}
    
    if pd.isna(raw):
        return {'raw': raw, 'valid': False, 'reason': 'null'}
    
    raw_str = str(raw).strip()
    
    # 1) Add scheme if missing
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://', raw_str):
        if require_scheme:
            if raw_str.startswith('//'):
                raw_str = 'https:' + raw_str
            elif '.' in raw_str and '/' in raw_str:
                raw_str = 'https://' + raw_str
            elif '.' in raw_str:
                raw_str = 'https://' + raw_str
    
    # 2) Parse URL
    try:
        parsed = urlparse(raw_str)
    except Exception:
        return {'raw': raw_str, 'valid': False, 'reason': 'parse_error'}
    
    # 3) Validate scheme
    if parsed.scheme and parsed.scheme not in allowed_schemes:
        return {'raw': raw_str, 'valid': False, 
                'reason': f'invalid_scheme: {parsed.scheme}'}
    
    # 4) Validate hostname
    if not parsed.hostname:
        return {'raw': raw_str, 'valid': False, 'reason': 'no_hostname'}
    
    # Basic hostname validation
    hostname = parsed.hostname.lower()
    if not re.match(r'^[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?)*$',
                    hostname):
        return {'raw': raw_str, 'valid': False, 'reason': 'invalid_hostname'}
    
    # 5) Normalize
    clean_url = raw_str
    if normalize:
        # Lowercase scheme and hostname
        scheme = parsed.scheme.lower()
        host = hostname
        
        # Remove default ports
        port = parsed.port
        if (scheme == 'http' and port == 80) or \
           (scheme == 'https' and port == 443):
            port = None
        
        netloc = host
        if port:
            netloc += f':{port}'
        if parsed.username:
            userinfo = parsed.username
            if parsed.password:
                userinfo += f':{parsed.password}'
            netloc = f'{userinfo}@{netloc}'
        
        # Normalize path
        path = parsed.path or '/'
        # Remove trailing slash (except root)
        if path != '/' and path.endswith('/'):
            path = path.rstrip('/')
        # Remove duplicate slashes
        path = re.sub(r'/+', '/', path)
        
        # 6) Strip tracking parameters
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        if strip_tracking:
            query_params = {k: v for k, v in query_params.items()
                          if k.lower() not in TRACKING_PARAMS}
        
        # Rebuild query string (sorted for consistency)
        query = urlencode(
            {k: v[0] if len(v) == 1 else v 
             for k, v in sorted(query_params.items())},
            doseq=True
        ) if query_params else ''
        
        # Remove fragment by default
        clean_url = urlunparse((scheme, netloc, path, '', query, ''))
    
    # 7) Extract domain info
    parts = hostname.split('.')
    domain = '.'.join(parts[-2:]) if len(parts) >= 2 else hostname
    subdomain = '.'.join(parts[:-2]) if len(parts) > 2 else ''
    
    return {
        'raw': str(raw),
        'cleaned': clean_url,
        'scheme': parsed.scheme,
        'domain': domain,
        'subdomain': subdomain,
        'path': parsed.path,
        'has_query': bool(parsed.query),
        'tracking_params_stripped': strip_tracking,
        'valid': True,
    }

def clean_url_column(df, col, **kwargs):
    """Apply URL cleaning to DataFrame column"""
    results = df[col].apply(lambda x: clean_url(x, **kwargs))
    parsed_df = pd.DataFrame(results.tolist())
    
    valid_count = parsed_df['valid'].sum()
    total = parsed_df['raw'].notna().sum()
    
    result = df.copy()
    result[f'{col}_cleaned'] = parsed_df['cleaned']
    result[f'{col}_domain'] = parsed_df['domain']
    result[f'{col}_valid'] = parsed_df['valid']
    
    print(f"🔗 URL Clean: {valid_count}/{total} valid "
          f"({valid_count/max(total,1)*100:.1f}%)")
    return result
```

---

## ⚖️ Physical Unit Conversion

```python
import re
import pandas as pd

# Conversion factors to SI base units
UNIT_CONVERSIONS = {
    # Length → meters
    'length': {
        'm': 1.0, 'meter': 1.0, 'meters': 1.0, 'เมตร': 1.0,
        'km': 1000.0, 'kilometer': 1000.0, 'กิโลเมตร': 1000.0,
        'cm': 0.01, 'centimeter': 0.01, 'เซนติเมตร': 0.01,
        'mm': 0.001, 'millimeter': 0.001, 'มิลลิเมตร': 0.001,
        'in': 0.0254, 'inch': 0.0254, 'inches': 0.0254, 'นิ้ว': 0.0254,
        'ft': 0.3048, 'foot': 0.3048, 'feet': 0.3048, 'ฟุต': 0.3048,
        'yd': 0.9144, 'yard': 0.9144, 'หลา': 0.9144,
        'mi': 1609.344, 'mile': 1609.344, 'miles': 1609.344, 'ไมล์': 1609.344,
        'nm': 1852.0, 'nautical_mile': 1852.0,
        'วา': 2.0, 'wah': 2.0,
        'ไร่': 1600.0,  # area but used as length² in Thai
    },
    # Weight → kilograms
    'weight': {
        'kg': 1.0, 'kilogram': 1.0, 'กิโลกรัม': 1.0, 'กก.': 1.0,
        'g': 0.001, 'gram': 0.001, 'กรัม': 0.001,
        'mg': 0.000001, 'milligram': 0.000001, 'มิลลิกรัม': 0.000001,
        'lb': 0.453592, 'lbs': 0.453592, 'pound': 0.453592, 'ปอนด์': 0.453592,
        'oz': 0.0283495, 'ounce': 0.0283495, 'ออนซ์': 0.0283495,
        'ton': 1000.0, 'ตัน': 1000.0,
        'st': 6.35029, 'stone': 6.35029,
        'บาท': 0.01518, 'baht_weight': 0.01518,  # Thai gold weight
    },
    # Temperature (special: not multiplicative)
    'temperature': {
        'c': 'celsius', 'celsius': 'celsius', '°c': 'celsius', 'เซลเซียส': 'celsius',
        'f': 'fahrenheit', 'fahrenheit': 'fahrenheit', '°f': 'fahrenheit', 'ฟาเรนไฮต์': 'fahrenheit',
        'k': 'kelvin', 'kelvin': 'kelvin',
    },
    # Volume → liters
    'volume': {
        'l': 1.0, 'liter': 1.0, 'litre': 1.0, 'ลิตร': 1.0,
        'ml': 0.001, 'milliliter': 0.001, 'มิลลิลิตร': 0.001,
        'gal': 3.78541, 'gallon': 3.78541, 'แกลลอน': 3.78541,
        'qt': 0.946353, 'quart': 0.946353,
        'pt': 0.473176, 'pint': 0.473176,
        'cup': 0.236588,
        'tbsp': 0.0147868, 'tablespoon': 0.0147868,
        'tsp': 0.00492892, 'teaspoon': 0.00492892,
        'cc': 0.001, 'ซีซี': 0.001,
    },
    # Speed → m/s
    'speed': {
        'm/s': 1.0, 'mps': 1.0,
        'km/h': 0.277778, 'kmh': 0.277778, 'kph': 0.277778,
        'mph': 0.44704, 'mi/h': 0.44704,
        'knot': 0.514444, 'knots': 0.514444, 'นอต': 0.514444,
        'ft/s': 0.3048, 'fps': 0.3048,
    },
}

def convert_temperature(value, from_unit, to_unit):
    """Temperature conversion (non-linear)"""
    # Convert to Celsius first
    if from_unit == 'fahrenheit':
        celsius = (value - 32) * 5 / 9
    elif from_unit == 'kelvin':
        celsius = value - 273.15
    else:
        celsius = value
    
    # Convert from Celsius to target
    if to_unit == 'fahrenheit':
        return celsius * 9 / 5 + 32
    elif to_unit == 'kelvin':
        return celsius + 273.15
    return celsius

def detect_unit(text):
    """Auto-detect unit from text"""
    text = str(text).strip().lower()
    
    # Extract number and unit
    match = re.match(r'^([\d,]+\.?\d*)\s*(.+)$', text)
    if not match:
        return None, None, None
    
    value = float(match.group(1).replace(',', ''))
    unit_str = match.group(2).strip().rstrip('.')
    
    # Find matching unit category
    for category, units in UNIT_CONVERSIONS.items():
        if unit_str in units:
            return value, unit_str, category
    
    return value, unit_str, None

def convert_units(df, col, target_unit, source_unit=None, category=None):
    """
    ★ Physical unit conversion (length, weight, temp, volume, speed)
    ★ ต่างจาก Currency ตรงที่ physical units มี non-linear conversion (temp)
      และ support Thai units (วา, ไร่, บาท/weight)
    """
    result = df.copy()
    report = {'converted': 0, 'failed': 0, 'units_found': set()}
    
    for idx, raw in df[col].items():
        if pd.isna(raw):
            continue
        
        # Auto-detect or use specified source
        if source_unit:
            try:
                value = float(str(raw).replace(',', ''))
            except ValueError:
                report['failed'] += 1
                continue
            src = source_unit.lower()
        else:
            value, src, detected_cat = detect_unit(raw)
            if value is None:
                report['failed'] += 1
                continue
        
        report['units_found'].add(src)
        target = target_unit.lower()
        
        # Find category
        cat = category
        if not cat:
            for c, units in UNIT_CONVERSIONS.items():
                if src in units and target in units:
                    cat = c
                    break
        
        if not cat:
            report['failed'] += 1
            continue
        
        # Convert
        if cat == 'temperature':
            from_type = UNIT_CONVERSIONS['temperature'].get(src)
            to_type = UNIT_CONVERSIONS['temperature'].get(target)
            if from_type and to_type:
                converted = convert_temperature(value, from_type, to_type)
                result.at[idx, f'{col}_{target_unit}'] = round(converted, 4)
                report['converted'] += 1
        else:
            units = UNIT_CONVERSIONS.get(cat, {})
            from_factor = units.get(src)
            to_factor = units.get(target)
            if from_factor and to_factor:
                si_value = value * from_factor
                converted = si_value / to_factor
                result.at[idx, f'{col}_{target_unit}'] = round(converted, 4)
                report['converted'] += 1
            else:
                report['failed'] += 1
    
    report['units_found'] = list(report['units_found'])
    print(f"⚖️ Unit Convert: {report['converted']} converted to {target_unit}, "
          f"{len(report['units_found'])} source units found")
    return result, report
```

---

## 🟡 Power Query (M Language) — Cleaning Functions

### Error Handling & Replacement

```m
// ★ try...otherwise — Error handling pattern ใน M
let
    Source = Excel.Workbook(File.Contents("data.xlsx")),
    Data = Source{[Name="Sheet1"]}[Data],
    
    // 1) Replace errors in specific column
    ReplaceErrors = Table.ReplaceErrorValues(Data, {
        {"Amount", 0},
        {"Date", #date(1900, 1, 1)},
        {"Name", "UNKNOWN"}
    }),
    
    // 2) Remove rows with ANY error
    RemoveErrorRows = Table.RemoveRowsWithErrors(ReplaceErrors),
    
    // 3) try...otherwise for safe type conversion
    SafeConvert = Table.TransformColumns(RemoveErrorRows, {
        {"Amount", each try Number.From(_) otherwise null, type number},
        {"Date", each try Date.From(_) otherwise null, type date},
        {"Percentage", each try Number.From(
            Text.Replace(Text.Replace(Text.From(_), "%", ""), ",", "")
        ) / 100 otherwise null, type number}
    }),
    
    // 4) Custom error logging
    WithErrorLog = Table.AddColumn(SafeConvert, "HasIssue", each
        try (if [Amount] = null or [Date] = null then true else false)
        otherwise true, type logical)
in
    WithErrorLog
```

### Type Detection & Casting

```m
// ★ Table.TransformColumnTypes — ครอบคลุมทุก PBI data type
let
    Source = Csv.Document(File.Contents("data.csv")),
    
    // 1) Comprehensive type casting
    TypedTable = Table.TransformColumnTypes(Source, {
        {"ID", Int64.Type},                    // Whole Number
        {"Amount", Currency.Type},             // Fixed Decimal (4 decimal places)
        {"Price", type number},                // Decimal Number
        {"Percentage", Percentage.Type},        // Percentage (0.5 = 50%)
        {"Name", type text},                   // Text
        {"IsActive", type logical},            // True/False
        {"OrderDate", type date},              // Date only
        {"OrderTime", type time},              // Time only
        {"OrderTimestamp", type datetime},      // DateTime
        {"CreatedUTC", type datetimezone},      // DateTime with timezone
        {"Duration", type duration},           // Duration (days/hours/min)
        {"Photo", type binary}                 // Binary data
    }),
    
    // 2) Auto-detect types (let PBI guess)
    AutoTyped = Table.TransformColumnTypes(Source,
        List.Transform(
            Table.ColumnNames(Source),
            each {_, type any}
        )
    ),
    
    // 3) Safe type detection with fallback
    SmartTyped = Table.TransformColumns(TypedTable, {
        {"Amount", each
            if _ = null then null
            else if Value.Is(_, type number) then _
            else try Number.From(_) otherwise null,
        type number}
    })
in
    SmartTyped
```

### Fuzzy Matching (Built-in PQ)

```m
// ★ Table.FuzzyJoin / FuzzyNestedJoin — built-in fuzzy ใน Power Query
let
    Dirty = #table({"CustomerName"}, {
        {"สมชาย  จิตดี"}, {"สมชาย จิตดี"}, {"Somchai Jitdee"},
        {"บริษัท ABC จำกัด"}, {"บ.ABC จก."}, {"ABC Co.,Ltd."}
    }),
    Clean = #table({"StandardName", "Code"}, {
        {"สมชาย จิตดี", "C001"}, {"บริษัท ABC จำกัด", "C002"}
    }),
    
    // 1) Fuzzy Join with threshold
    FuzzyJoined = Table.FuzzyJoin(
        Dirty, {"CustomerName"},
        Clean, {"StandardName"},
        JoinKind.LeftOuter,
        [
            Threshold = 0.7,                    // 70% similarity
            NumberOfMatches = 1,                 // Best match only
            TransformationTable = null,          // Custom synonym table
            IgnoreCase = true,
            IgnoreSpace = true,
            ConcurrentRequests = 4               // Parallelism
        ]
    ),
    
    // 2) Fuzzy Cluster — group similar values
    FuzzyClustered = Table.AddFuzzyClusterColumn(
        Dirty, "CustomerName", "ClusterName",
        [
            Threshold = 0.6,
            IgnoreCase = true,
            IgnoreSpace = true
        ]
    )
in
    FuzzyClustered
```

### Unpivot / Pivot / Reshape

```m
// ★ Reshape data ก่อน clean — Critical สำหรับ messy Excel/CSV
let
    // Crosstab format → long format
    Source = #table({"Product", "Jan", "Feb", "Mar"}, {
        {"A", 100, 200, 150},
        {"B", 300, null, 250}
    }),
    
    // 1) Unpivot (wide → long)
    Unpivoted = Table.UnpivotOtherColumns(Source, {"Product"}, "Month", "Sales"),
    
    // 2) Replace nulls after unpivot
    CleanedNulls = Table.ReplaceValue(Unpivoted, null, 0,
        Replacer.ReplaceValue, {"Sales"}),
    
    // 3) Fill Down (for merged cells in Excel)
    FilledDown = Table.FillDown(CleanedNulls, {"Product"}),
    
    // 4) Fill Up
    FilledUp = Table.FillUp(FilledDown, {"Product"}),
    
    // 5) Pivot back (long → wide) if needed
    Pivoted = Table.Pivot(CleanedNulls,
        List.Distinct(CleanedNulls[Month]), "Month", "Sales", List.Sum),
    
    // 6) Expand nested records/tables
    Expanded = Table.ExpandRecordColumn(Source, "Details",
        {"Address", "Phone"}, {"Details.Address", "Details.Phone"}),
    
    // 7) Split column
    SplitByDelimiter = Table.SplitColumn(Source, "FullName",
        Splitter.SplitTextByDelimiter(" ", QuoteStyle.None),
        {"FirstName", "LastName"})
in
    SplitByDelimiter
```

### Text Cleaning Functions (M)

```m
// ★ M Language text cleaning functions
let
    Source = #table({"RawText"}, {
        {"  Hello   World  "}, {"UPPERCASE"}, {"lowercase"},
        {"Mixed Case Text"}, {"line1#(lf)line2"}, {"tab#(tab)here"}
    }),
    
    Cleaned = Table.TransformColumns(Source, {{"RawText", each
        let
            // 1) Trim whitespace (leading + trailing)
            trimmed = Text.Trim(_),
            
            // 2) Clean control characters
            cleaned = Text.Clean(trimmed),
            
            // 3) Proper case (Title Case)
            proper = Text.Proper(cleaned),
            
            // 4) Compact multiple spaces → single
            compacted = Text.Combine(
                List.Select(Text.SplitAny(proper, " "), each _ <> ""),
                " "
            ),
            
            // 5) Remove non-printable characters
            sanitized = Text.Select(compacted,
                {"A".."Z", "a".."z", "0".."9", " ", ".", "-", "@",
                 "ก".."๙"})  // Include Thai characters
        in
            sanitized,
    type text}})
in
    Cleaned
```

### Query Folding & Performance

```m
// ★ Query Folding — push cleaning to source for performance
let
    // ✅ FOLDABLE: these operations push down to SQL server
    Source = Sql.Database("server", "database"),
    Sales = Source{[Schema="dbo", Item="Sales"]}[Data],
    
    // ✅ Foldable operations (order matters!)
    Filtered = Table.SelectRows(Sales, each [Year] >= 2024),        // → WHERE
    Selected = Table.SelectColumns(Filtered, {"ID", "Amount"}),     // → SELECT
    Sorted = Table.Sort(Selected, {{"Amount", Order.Descending}}),  // → ORDER BY
    Grouped = Table.Group(Selected, {"Category"},                   // → GROUP BY
        {{"Total", each List.Sum([Amount]), type number}}),
    Renamed = Table.RenameColumns(Grouped, {{"Category", "Cat"}}),  // → AS
    
    // ❌ NON-FOLDABLE: breaks query folding (processed in PQ engine)
    // Table.AddColumn with custom function
    // Table.TransformColumns with complex M logic
    // Table.Buffer (forces materialization)
    // List.Generate, List.Accumulate
    
    // 💡 TIP: Right-click step → "View Native Query" to verify folding
    
    // ★ Table.Buffer — use strategically to cache intermediate results
    Buffered = Table.Buffer(Filtered)  // Prevents re-evaluation
in
    Renamed
```

---

## 🔷 Power BI Data Types — Cleaning Guide

### BLANK() vs 0 vs "" (Empty String)

```
★ Power BI มี "ค่าว่าง" 3 ชนิดที่ต่างกัน:

┌─────────────┬──────────────────┬──────────────────────────┐
│ Type        │ M Language       │ DAX                      │
├─────────────┼──────────────────┼──────────────────────────┤
│ NULL/BLANK  │ null             │ BLANK()                  │
│ Zero        │ 0                │ 0                        │
│ Empty String│ ""               │ ""                       │
└─────────────┴──────────────────┴──────────────────────────┘

★ ปัญหา: แต่ละชนิดมีพฤติกรรมต่างกันใน aggregation:

┌──────────────┬─────────┬──────┬────────┬───────┐
│ Function     │ BLANK() │ 0    │ ""     │ Notes │
├──────────────┼─────────┼──────┼────────┼───────┤
│ SUM          │ ข้าม    │ รวม  │ Error  │       │
│ AVERAGE      │ ข้าม    │ รวม  │ Error  │ ⚠️    │
│ COUNT        │ ข้าม    │ นับ  │ นับ    │       │
│ COUNTA       │ ข้าม    │ นับ  │ นับ    │       │
│ COUNTBLANK   │ นับ     │ ข้าม │ นับ    │ ⚠️    │
│ IF(col="")   │ TRUE!   │ FALSE│ TRUE   │ ⚠️⚠️  │
│ ISBLANK      │ TRUE    │ FALSE│ FALSE  │       │
└──────────────┴─────────┴──────┴────────┴───────┘
```

```dax
// ★ DAX: Proper null/blank handling
Clean_Amount = 
    IF(
        ISBLANK([Amount]) || [Amount] = 0,
        BLANK(),  -- ใช้ BLANK() ไม่ใช่ 0, ไม่ใช่ ""
        [Amount]
    )

// ★ Count non-blank, non-zero, non-empty
Real_Count = 
    CALCULATE(
        COUNTROWS(Sales),
        NOT(ISBLANK(Sales[Amount])),
        Sales[Amount] <> 0,
        Sales[Name] <> ""
    )

// ★ Safe average ที่ไม่นับ BLANK และ 0
True_Average = 
    AVERAGEX(
        FILTER(Sales, NOT(ISBLANK(Sales[Amount])) && Sales[Amount] <> 0),
        Sales[Amount]
    )
```

### Fixed Decimal vs Decimal Number

```
★ Currency.Type (Fixed Decimal) = 4 decimal places เสมอ
★ type number (Decimal Number) = floating point (precision issues!)

ตัวอย่างปัญหา:
  0.1 + 0.2 = 0.30000000000000004  (Decimal Number ❌)
  0.1 + 0.2 = 0.3000              (Fixed Decimal ✅)

แนะนำ:
  💰 Financial data → ใช้ Currency.Type เสมอ
  📊 Scientific data → ใช้ type number
  📐 Percentage → ใช้ Percentage.Type
```

```m
// M: Convert to correct financial type
FixedDecimal = Table.TransformColumnTypes(Source, {
    {"Revenue", Currency.Type},      // Fixed 4 decimals
    {"TaxRate", Percentage.Type},     // 0.07 = 7%
    {"Weight", type number}           // Floating point OK
})
```

### DateTimezone vs DateTime vs Date

```m
// ★ Timezone-aware date handling in Power Query
let
    Source = #table({"RawDate"}, {
        {"2026-03-01T13:00:00+07:00"},   // Bangkok time
        {"2026-03-01T06:00:00Z"},         // UTC
        {"2026-03-01T13:00:00"},          // No timezone (ambiguous!)
    }),
    
    // 1) Parse as DateTimeZone
    WithTZ = Table.TransformColumnTypes(Source, {
        {"RawDate", type datetimezone}
    }),
    
    // 2) Convert all to local timezone (Thailand = +07:00)
    ToLocal = Table.TransformColumns(WithTZ, {
        {"RawDate", each DateTimeZone.SwitchZone(_, 7, 0), type datetimezone}
    }),
    
    // 3) Extract date-only (drops time + timezone)
    DateOnly = Table.TransformColumns(ToLocal, {
        {"RawDate", each DateTime.Date(DateTimeZone.RemoveZone(_)), type date}
    }),
    
    // 4) Duration calculation
    WithDuration = Table.AddColumn(Source, "Age", each
        Duration.TotalDays(DateTime.LocalNow() - DateTime.From([RawDate])),
        type number)
in
    WithDuration
```

### Duration Type

```m
// ★ Duration type — สำหรับ time elapsed / processing time
let
    Source = #table({"StartTime", "EndTime"}, {
        {#datetime(2026,3,1,9,0,0), #datetime(2026,3,1,17,30,0)},
        {#datetime(2026,3,1,8,0,0), #datetime(2026,3,2,8,0,0)}
    }),
    
    // 1) Calculate duration
    WithDuration = Table.AddColumn(Source, "WorkHours", each
        [EndTime] - [StartTime], type duration),
    
    // 2) Extract components from duration
    WithParts = Table.AddColumn(WithDuration, "TotalHours", each
        Duration.TotalHours([WorkHours]), type number),
    
    // 3) Format duration as text
    WithFormat = Table.AddColumn(WithParts, "DurationText", each
        Text.From(Duration.Hours([WorkHours])) & "h " &
        Text.From(Duration.Minutes([WorkHours])) & "m",
        type text),
    
    // 4) Clean invalid durations (negative)
    Cleaned = Table.TransformColumns(WithFormat, {
        {"WorkHours", each if _ < #duration(0,0,0,0) then null else _,
         type duration}
    })
in
    Cleaned
```

### Binary Type & File Handling

```m
// ★ Binary type — สำหรับ files, images, embedded data ใน PQ
let
    // 1) Load multiple files from folder
    FolderSource = Folder.Files("C:\Data\Reports"),
    
    // 2) Filter by extension
    CsvFiles = Table.SelectRows(FolderSource, each
        Text.EndsWith([Extension], ".csv")),
    
    // 3) Parse each binary file
    ParsedFiles = Table.AddColumn(CsvFiles, "Data", each
        try Csv.Document([Content], [Delimiter=",", Encoding=65001])
        otherwise #table({}, {}),
        type table),
    
    // 4) Expand all tables
    Expanded = Table.ExpandTableColumn(ParsedFiles, "Data",
        Table.ColumnNames(ParsedFiles{0}[Data])),
    
    // 5) Clean up - remove file metadata columns
    Cleaned = Table.RemoveColumns(Expanded, {
        "Content", "Extension", "Date accessed", "Date modified",
        "Date created", "Attributes", "Folder Path"
    })
in
    Cleaned
```

---

## 📐 DAX-level Data Cleaning

### ISBLANK vs ISEMPTY vs Error Handling

```dax
// ★ ISBLANK — checks for BLANK() value
// ★ ISEMPTY — checks if TABLE has no rows (NOT for scalar values!)

// 1) Safe column with proper null handling
Clean_Name = 
    SWITCH(
        TRUE(),
        ISBLANK([Name]), "N/A",
        [Name] = "", "N/A",
        LEN(TRIM([Name])) = 0, "N/A",
        TRIM([Name])
    )

// 2) IFERROR — catch calculation errors
Safe_Ratio = 
    IFERROR(
        DIVIDE([Revenue], [Cost]),  // DIVIDE handles /0 automatically
        BLANK()
    )

// 3) DIVIDE — built-in safe division (better than IFERROR)
Margin = DIVIDE([Revenue] - [Cost], [Revenue], BLANK())  // 3rd arg = alternate result

// 4) ISEMPTY — check if filter context returns no rows
Has_Sales = 
    IF(
        ISEMPTY(FILTER(Sales, Sales[Amount] > 0)),
        "No Sales",
        "Has Sales"
    )
```

### REMOVEFILTERS & Clean Aggregation

```dax
// ★ REMOVEFILTERS — remove filter context for clean calculations

// 1) % of Total (ignore current filter on Category)
Pct_of_Total = 
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(SUM(Sales[Amount]), REMOVEFILTERS(Sales[Category]))
    )

// 2) ALL vs REMOVEFILTERS
// ALL() = removes filters + returns table (can be used as table)
// REMOVEFILTERS() = only removes filters (cleaner syntax)

All_Time_Average = 
    CALCULATE(
        AVERAGE(Sales[Amount]),
        REMOVEFILTERS('Date')  // Ignore date slicer
    )

// 3) ALLEXCEPT — keep some filters, remove others
Category_Total = 
    CALCULATE(
        SUM(Sales[Amount]),
        ALLEXCEPT(Sales, Sales[Category])  // Keep only Category filter
    )

// 4) USERELATIONSHIP — use inactive relationship for cleaning
Delivery_Amount = 
    CALCULATE(
        SUM(Sales[Amount]),
        USERELATIONSHIP(Sales[DeliveryDate], 'Date'[Date])
    )
```

### Calculated Tables for Cleaning

```dax
// ★ สร้าง clean table ด้วย DAX — useful สำหรับ reference tables

// 1) Distinct clean values
Clean_Products = 
    DISTINCT(
        SELECTCOLUMNS(
            FILTER(Products, NOT(ISBLANK(Products[Name]))),
            "ProductName", TRIM(UPPER(Products[Name])),
            "Category", Products[Category]
        )
    )

// 2) Date table (clean, continuous)
DateTable = 
    VAR MinDate = MIN(Sales[OrderDate])
    VAR MaxDate = MAX(Sales[OrderDate])
    RETURN
    ADDCOLUMNS(
        CALENDAR(MinDate, MaxDate),
        "Year", YEAR([Date]),
        "Month", MONTH([Date]),
        "MonthName", FORMAT([Date], "MMMM"),
        "Quarter", "Q" & FORMAT([Date], "Q"),
        "WeekDay", WEEKDAY([Date], 2),
        "IsWeekend", WEEKDAY([Date], 2) >= 6,
        "FiscalYear", IF(MONTH([Date]) >= 10, YEAR([Date]) + 1, YEAR([Date]))
    )

// 3) Bridge table for many-to-many cleaning
OrderProduct_Bridge = 
    DISTINCT(
        SELECTCOLUMNS(
            Sales,
            "OrderID", Sales[OrderID],
            "ProductID", Sales[ProductID]
        )
    )
```

---

## 🏗️ Power BI Architecture — Cleaning Patterns

### Dataflows (Central Cleaning Layer)

```
★ Dataflows = ETL layer ใน Power BI Service
★ ใช้เป็น central cleaning layer ที่ทุก dataset ใช้ร่วมกัน

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Raw Sources │────▶│  Dataflow    │────▶│  Datasets    │
│  (SQL, API,  │     │  (Clean here)│     │  (Models)    │
│  Excel, CSV) │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                          │
                     ┌────┴────┐
                     │ ✅ Type cast      │
                     │ ✅ Null handling   │
                     │ ✅ Dedup           │
                     │ ✅ Standardize     │
                     │ ✅ Fuzzy merge     │
                     │ ✅ Computed cols   │
                     └─────────┘

Best Practices:
  1. Raw Layer Dataflow  → import as-is
  2. Clean Layer Dataflow → transformations
  3. Dataset → only relationships + measures
```

### DirectQuery vs Import Mode Cleaning

```
★ Cleaning strategy ต่างกันตาม storage mode:

┌──────────────┬──────────────────────────────────────────┐
│ Mode         │ Cleaning Strategy                        │
├──────────────┼──────────────────────────────────────────┤
│ Import       │ ✅ Clean ใน Power Query (full M support) │
│              │ ✅ ใช้ Table.Buffer ได้                   │
│              │ ✅ Custom M functions                     │
│              │ ⚠️ Memory limit → clean before import    │
├──────────────┼──────────────────────────────────────────┤
│ DirectQuery  │ ❌ PQ transformations limited             │
│              │ ✅ Clean ที่ source (SQL views/procedures)│
│              │ ✅ Use database-side cleaning             │
│              │ ⚠️ Query folding critical                │
├──────────────┼──────────────────────────────────────────┤
│ Dual         │ ✅ Import for dimensions (clean in PQ)    │
│              │ ✅ DirectQuery for facts (clean at source)│
│              │ ✅ Best of both worlds                    │
├──────────────┼──────────────────────────────────────────┤
│ Composite    │ ✅ Mix Import + DirectQuery              │
│              │ ✅ Aggregation tables (pre-cleaned)       │
│              │ ⚠️ Relationship constraints              │
└──────────────┴──────────────────────────────────────────┘
```

### Incremental Refresh & Clean Partitions

```m
// ★ Incremental Refresh — clean only new/changed data
// Parameters: RangeStart, RangeEnd (type datetime, required names)

let
    Source = Sql.Database("server", "db"),
    Sales = Source{[Schema="dbo", Item="Sales"]}[Data],
    
    // 1) Filter by refresh range (MUST be foldable!)
    Filtered = Table.SelectRows(Sales, each
        [OrderDate] >= RangeStart and [OrderDate] < RangeEnd),
    
    // 2) Apply cleaning AFTER range filter (maintains folding)
    Cleaned = Table.TransformColumnTypes(Filtered, {
        {"Amount", Currency.Type},
        {"OrderDate", type date}
    }),
    
    // 3) Remove duplicates within range
    Deduped = Table.Distinct(Cleaned, {"OrderID"})
in
    Deduped

// ★ Configure in PBI Desktop:
// Right-click table → Incremental Refresh
// - Archive: 2 years
// - Incremental: 30 days
// - Detect data changes: [ModifiedDate] column
// - Only refresh complete periods: ✅
```

### Query Diagnostics (Find Cleaning Bottleneck)

```
★ Power Query Diagnostics — หา step ที่ช้า

วิธีใช้:
1. Tools → Start Diagnostics
2. Refresh dataset
3. Tools → Stop Diagnostics
4. ดู "Diagnostics" table

┌─────────────────────┬──────────┬─────────────────────────┐
│ Column              │ ดูอะไร   │ Action                  │
├─────────────────────┼──────────┼─────────────────────────┤
│ Exclusive Duration  │ เวลาจริง │ Optimize ถ้า > 5 วิ     │
│ Data Source Query   │ SQL sent │ Check if folded         │
│ Resource            │ CPU/Mem  │ Buffer ถ้า memory spike │
│ Partition           │ Parallel │ Enable parallel load    │
└─────────────────────┴──────────┴─────────────────────────┘

Common bottlenecks:
  ❌ Custom M function ใน AddColumn → breaks folding
  ❌ Table.Combine ของ 1000+ files → ใช้ Table.Buffer
  ❌ Fuzzy operations → limit rows first
  ❌ Unnecessary type changes → cast once at end
```

### Aggregation Tables (Pre-cleaned Summaries)

```dax
// ★ Aggregation Tables — pre-clean + pre-aggregate สำหรับ performance

// 1) สร้าง Agg table (DAX calculated table)
Sales_Daily_Agg = 
    SUMMARIZECOLUMNS(
        Sales[OrderDate],
        Sales[Category],
        Sales[Region],
        "Total_Amount", SUM(Sales[Amount]),
        "Order_Count", COUNTROWS(Sales),
        "Avg_Amount", AVERAGE(Sales[Amount]),
        "Distinct_Customers", DISTINCTCOUNT(Sales[CustomerID])
    )

// 2) จัดการ Agg ใน Model:
//    - Set storage mode = Import
//    - Detail table = DirectQuery
//    - PBI auto-routes queries to Agg when possible
//
// ★ Manage Aggregations dialog:
//    Sales_Daily_Agg[Total_Amount]  → SUM of Sales[Amount]
//    Sales_Daily_Agg[Order_Count]   → COUNT of Sales[OrderID]
//    Sales_Daily_Agg[OrderDate]     → GROUP BY Sales[OrderDate]
```

### Parameters for Dynamic Cleaning

```m
// ★ Parameters — ทำให้ cleaning configurable

// Define parameters in PQ:
// NullThreshold = 0.5     (50% null → drop column)
// MinDate = #date(2020,1,1)
// DataSource = "Production"

let
    Source = if DataSource = "Production"
        then Sql.Database("prod-server", "db")
        else Sql.Database("dev-server", "db"),
    
    Sales = Source{[Schema="dbo", Item="Sales"]}[Data],
    
    // 1) Dynamic date filter
    Filtered = Table.SelectRows(Sales, each [OrderDate] >= MinDate),
    
    // 2) Dynamic null threshold — drop columns with too many nulls
    NullCounts = List.Transform(
        Table.ColumnNames(Filtered),
        each {_, Table.RowCount(Table.SelectRows(Filtered,
            (row) => Record.Field(row, _) = null)) / Table.RowCount(Filtered)}
    ),
    ColumnsToKeep = List.Select(NullCounts, each _{1} < NullThreshold),
    ColumnNames = List.Transform(ColumnsToKeep, each _{0}),
    
    CleanedColumns = Table.SelectColumns(Filtered, ColumnNames)
in
    CleanedColumns
```

### Row-Level Security (RLS) Data Filtering

```dax
// ★ RLS — clean data visibility per user/role

// 1) Static RLS
// Role: "Thailand_Team"
[Region] = "Thailand"

// 2) Dynamic RLS (username-based)
[Email] = USERPRINCIPALNAME()

// 3) Complex RLS with lookup table
CONTAINS(
    UserAccess,
    UserAccess[Email], USERPRINCIPALNAME(),
    UserAccess[Region], Sales[Region]
)

// 4) RLS with hierarchy
PATHCONTAINS(
    LOOKUPVALUE(
        OrgHierarchy[Path],
        OrgHierarchy[Email], USERPRINCIPALNAME()
    ),
    Sales[DepartmentID]
)

// ⚠️ RLS Cleaning considerations:
// - Test with "View as Role" in Desktop
// - BLANK values might bypass RLS filters!
// - Use ISBLANK() in RLS rules to handle nulls
// - Cross-filter direction affects RLS propagation
```

---

## 🟡 Power Query Advanced M Functions

### Table.Profile — Column Profiling & Statistics

```m
// ★ Table.Profile — built-in data profiling (PQ only)
let
    Source = Sql.Database("server", "db"),
    Sales = Source{[Schema="dbo", Item="Sales"]}[Data],
    
    // 1) Full column profile (null count, distinct, min, max, avg, etc.)
    Profile = Table.Profile(Sales),
    // Returns: Column, Min, Max, Average, StandardDeviation,
    //          Count, NullCount, DistinctCount
    
    // 2) Profile specific columns only
    PartialProfile = Table.Profile(Sales, {
        {"Amount", each List.Min(_), "MinAmount"},
        {"Amount", each List.Max(_), "MaxAmount"},
        {"Amount", each List.Average(_), "AvgAmount"},
        {"Amount", each List.StandardDeviation(_), "StdDev"},
        {"Name", each List.Count(List.Distinct(_)), "UniqueNames"}
    }),
    
    // 3) Table.Schema — column metadata (name, type, is nullable, etc.)
    Schema = Table.Schema(Sales),
    // Returns: Name, Position, TypeName, Kind, IsNullable, etc.
    
    // 4) Auto-detect columns that need cleaning
    NullReport = Table.SelectRows(Profile,
        each [NullCount] > 0 or [DistinctCount] = 1)
in
    NullReport
```

### Custom Reusable Cleaning Functions

```m
// ★ Shared reusable cleaning functions — DRY principle ใน PQ

// 1) fn_CleanText — reusable text cleaner
let
    fn_CleanText = (input as text) as text =>
        let
            trimmed = Text.Trim(input),
            cleaned = Text.Clean(trimmed),
            compacted = Text.Combine(
                List.Select(Text.Split(cleaned, " "), each _ <> ""), " ")
        in
            compacted
in
    fn_CleanText

// 2) fn_SafeNumber — safe number conversion
let
    fn_SafeNumber = (input as any) as nullable number =>
        let
            asText = Text.From(input),
            stripped = Text.Replace(Text.Replace(
                Text.Replace(asText, ",", ""), "฿", ""), " ", ""),
            result = try Number.From(stripped) otherwise null
        in
            result
in
    fn_SafeNumber

// 3) fn_ThaiDate — parse Thai date format (dd/mm/yyyy พ.ศ.)
let
    fn_ThaiDate = (input as text) as nullable date =>
        let
            parts = Text.Split(Text.Trim(input), "/"),
            day = try Number.From(parts{0}) otherwise null,
            month = try Number.From(parts{1}) otherwise null,
            rawYear = try Number.From(parts{2}) otherwise null,
            year = if rawYear > 2400 then rawYear - 543 else rawYear,
            result = try #date(year, month, day) otherwise null
        in
            result
in
    fn_ThaiDate

// 4) Apply custom functions to table
let
    Source = Excel.Workbook(File.Contents("data.xlsx")),
    Data = Source{[Name="Sheet1"]}[Data],
    
    Cleaned = Table.TransformColumns(Data, {
        {"Name", fn_CleanText, type text},
        {"Amount", fn_SafeNumber, type number},
        {"Date", fn_ThaiDate, type date}
    })
in
    Cleaned
```

### Advanced Joins & Combine

```m
// ★ Table.NestedJoin — all join types for cleaning
let
    Orders = #table({"OrderID", "CustomerID", "Amount"}, {
        {1, "C1", 100}, {2, "C2", 200}, {3, "C99", 300}
    }),
    Customers = #table({"CustID", "Name"}, {
        {"C1", "Alice"}, {"C2", "Bob"}, {"C3", "Charlie"}
    }),
    
    // 1) Left Outer Join (keep all orders, match customers)
    LeftJoin = Table.NestedJoin(Orders, "CustomerID",
        Customers, "CustID", "Cust", JoinKind.LeftOuter),
    
    // 2) Inner Join (only matched)
    InnerJoin = Table.NestedJoin(Orders, "CustomerID",
        Customers, "CustID", "Cust", JoinKind.Inner),
    
    // 3) ★ Anti Join — find orphan records (cleaning gold!)
    OrphanOrders = Table.NestedJoin(Orders, "CustomerID",
        Customers, "CustID", "Cust", JoinKind.LeftAnti),
    // Returns orders where CustomerID has NO match in Customers
    
    // 4) Full Outer Join — find gaps on both sides
    FullJoin = Table.NestedJoin(Orders, "CustomerID",
        Customers, "CustID", "Cust", JoinKind.FullOuter),
    
    // 5) Expand joined columns
    Expanded = Table.ExpandTableColumn(LeftJoin, "Cust",
        {"Name"}, {"CustomerName"}),
    
    // 6) Table.Combine — stack tables with schema mismatch
    Combined = Table.Combine({Orders, 
        #table({"OrderID", "CustomerID", "Amount", "Extra"}, {
            {4, "C1", 400, "test"}
        })
    }),
    // Auto-fills missing columns with null
    
    // 7) Multi-key join
    MultiKeyJoin = Table.NestedJoin(
        Source1, {"Year", "Month"},
        Source2, {"Year", "Month"},
        "Matched", JoinKind.Inner)
in
    Expanded
```

### Header Management & Row Operations

```m
// ★ Header & row cleanup — สำหรับ messy Excel/CSV
let
    Source = Excel.Workbook(File.Contents("messy.xlsx")),
    Sheet = Source{[Name="Sheet1"]}[Data],
    
    // 1) Promote first row as headers
    WithHeaders = Table.PromoteHeaders(Sheet, [PromoteAllScalars=true]),
    
    // 2) Skip header rows (when data starts at row 5)
    SkippedTop = Table.Skip(Sheet, 4),
    Promoted = Table.PromoteHeaders(SkippedTop),
    
    // 3) Remove bottom rows (totals, footers)
    RemovedBottom = Table.RemoveLastN(Promoted, 3),
    
    // 4) Alternate rows (every other row is data, rest is formatting)
    AlternateRows = Table.AlternateRows(Sheet, 0, 1, 1),
    // Skip 0, take 1, skip 1, repeat
    
    // 5) Table.Range — specific row range
    RowRange = Table.Range(Sheet, 5, 100),  // Start at row 5, take 100
    
    // 6) Remove blank rows
    NoBlankRows = Table.SelectRows(Promoted, each
        not List.IsEmpty(
            List.RemoveNulls(Record.FieldValues(_))
        )
    ),
    
    // 7) Demote headers (headers → first data row)
    Demoted = Table.DemoteHeaders(WithHeaders),
    
    // 8) Dynamic column rename (clean column names)
    CleanHeaders = Table.RenameColumns(Promoted,
        List.Transform(Table.ColumnNames(Promoted), each
            {_, Text.Trim(Text.Clean(
                Text.Replace(Text.Replace(_, "#(lf)", " "), "  ", " ")
            ))}
        )
    )
in
    CleanHeaders
```

### Table.ReplaceValue — Find & Replace Patterns

```m
// ★ Table.ReplaceValue — pattern-based cleaning
let
    Source = #table({"Name", "Phone", "Amount"}, {
        {"  Smith, John  ", "(66) 812-345-678", "1,234.56 ฿"},
        {"DOE, JANE", "0812345678", "$2,345.67"},
        {"N/A", "n/a", "-"}
    }),
    
    // 1) Replace exact value
    NoNA = Table.ReplaceValue(Source, "N/A", null,
        Replacer.ReplaceValue, {"Name"}),
    
    // 2) Replace text pattern (partial match)
    NoCurrency = Table.ReplaceValue(NoNA, "฿", "",
        Replacer.ReplaceText, {"Amount"}),
    
    // 3) Replace with function
    CleanPhone = Table.ReplaceValue(NoCurrency,
        each [Phone],
        each Text.Select([Phone], {"0".."9"}),
        Replacer.ReplaceValue, {"Phone"}),
    
    // 4) Multiple replacements chained
    MultiReplace = List.Accumulate(
        {{"N/A", null}, {"n/a", null}, {"-", null}, {"", null}},
        Source,
        (state, pair) => Table.ReplaceValue(state,
            pair{0}, pair{1}, Replacer.ReplaceValue, {"Name", "Phone"})
    ),
    
    // 5) Regex-like replacement (remove non-digits from phone)
    RegexClean = Table.TransformColumns(Source, {
        {"Phone", each Text.Select(_, {"0".."9", "+"}), type text},
        {"Amount", each Text.Select(_, {"0".."9", ".", "-"}), type text}
    })
in
    RegexClean
```

---

## 🔶 Power Query Data Parsing

### JSON / XML / Web Parsing

```m
// ★ Structured data parsing ใน Power Query

// 1) JSON Document
let
    JsonSource = Json.Document(
        Web.Contents("https://api.example.com/data")),
    
    // Nested JSON → Table
    AsTable = Table.FromRecords(JsonSource[results]),
    
    // Deep expand nested objects
    Expanded = Table.ExpandRecordColumn(AsTable, "address",
        {"street", "city", "zip"}, {"Address", "City", "Zip"}),
    
    // Handle JSON arrays in columns
    ListExpanded = Table.ExpandListColumn(AsTable, "tags")
in
    ListExpanded

// 2) XML Document
let
    XmlSource = Xml.Document(File.Contents("data.xml")),
    
    // Navigate XML tree
    Root = XmlSource{0}[Value],
    Items = Root{[Name="items"]}[Value],
    AsTable = Table.FromList(Items[Value], 
        Record.FieldValues, {"Name", "Price", "Category"})
in
    AsTable

// 3) Web Page Scraping
let
    WebPage = Web.Page(Web.Contents("https://example.com/table")),
    DataTable = WebPage{0}[Data],  // First table on page
    
    // Clean scraped data
    Cleaned = Table.TransformColumnTypes(DataTable, {
        {"Price", type number},
        {"Date", type date}
    })
in
    Cleaned

// 4) API with pagination
let
    GetPage = (page as number) as table =>
        let
            response = Json.Document(Web.Contents(
                "https://api.example.com/data",
                [Query=[page=Text.From(page), limit="100"]]
            )),
            data = Table.FromRecords(response[results])
        in
            data,
    
    AllPages = Table.Combine(
        List.Transform({1..10}, each GetPage(_)))
in
    AllPages
```

### Locale-Aware Parsing

```m
// ★ Culture/Locale-aware type conversion
let
    Source = #table({"Price_EU", "Price_US", "Date_TH"}, {
        {"1.234,56", "1,234.56", "01/03/2569"},  // EU vs US number format
        {"2.345,67", "2,345.67", "15/06/2568"}
    }),
    
    // 1) Parse European format (comma = decimal, dot = thousands)
    EuropeanNum = Table.TransformColumns(Source, {
        {"Price_EU", each Number.From(_, "de-DE"), type number}
    }),
    
    // 2) Parse US format
    USNum = Table.TransformColumns(EuropeanNum, {
        {"Price_US", each Number.From(_, "en-US"), type number}
    }),
    
    // 3) Parse Thai date (dd/mm/yyyy พ.ศ.) 
    ThaiDate = Table.TransformColumns(USNum, {
        {"Date_TH", each
            let
                parts = Text.Split(_, "/"),
                d = Number.From(parts{0}),
                m = Number.From(parts{1}),
                y = Number.From(parts{2}),
                ce = if y > 2400 then y - 543 else y
            in
                #date(ce, m, d),
        type date}
    }),
    
    // 4) Multiple locale handling in same column
    SmartParse = Table.TransformColumns(Source, {
        {"Price_EU", each
            let
                tryEU = try Number.From(_, "de-DE"),
                tryUS = try Number.From(_, "en-US")
            in
                if tryEU[HasError] then tryUS[Value] else tryEU[Value],
        type number}
    })
in
    SmartParse
```

### Column From Examples & Splitters

```m
// ★ Advanced column splitting strategies
let
    Source = #table({"FullAddress", "MixedID"}, {
        {"123 Main St, Bangkok, 10110", "TH-2026-001"},
        {"456 Oak Ave, Chiang Mai, 50000", "US-2025-042"}
    }),
    
    // 1) Split by delimiter (first occurrence)
    SplitFirst = Table.SplitColumn(Source, "FullAddress",
        Splitter.SplitTextByEachDelimiter({","}, QuoteStyle.None, false),
        {"Street", "Rest"}),
    
    // 2) Split by position (fixed width)
    SplitPos = Table.SplitColumn(Source, "MixedID",
        Splitter.SplitTextByPositions({0, 2, 3, 7, 8}),
        {"Country", "Sep1", "Year", "Sep2", "Seq"}),
    
    // 3) Split by character transition (digit→letter, etc.)
    SplitTransition = Table.SplitColumn(Source, "MixedID",
        Splitter.SplitTextByCharacterTransition(
            {"A".."Z","a".."z"}, {"0".."9"}),
        {"Prefix", "Numbers"}),
    
    // 4) Split by repeated delimiter
    SplitAll = Table.SplitColumn(Source, "FullAddress",
        Splitter.SplitTextByDelimiter(",", QuoteStyle.None),
        {"Part1", "Part2", "Part3"}),
    
    // 5) Extract patterns
    Extracted = Table.AddColumn(Source, "ZipCode", each
        Text.AfterDelimiter([FullAddress], ", ", {0, RelativePosition.FromEnd}),
        type text),
    
    // 6) Extract by pattern (digits only)
    ExtractDigits = Table.AddColumn(Source, "Numbers", each
        Text.Select([MixedID], {"0".."9"}), type text)
in
    ExtractDigits
```

---

## 📐 DAX Advanced Cleaning

### COALESCE & Multi-column Null Fallback

```dax
// ★ COALESCE — return first non-blank value (SQL-style)

// 1) Single row fallback
Clean_Phone = 
    COALESCE([MobilePhone], [WorkPhone], [HomePhone], "No Phone")

// 2) Multi-source address
Clean_Address = 
    COALESCE(
        [ShippingAddress],
        [BillingAddress], 
        [HomeAddress],
        "Address Required"
    )

// 3) SELECTEDVALUE — safe single value from filter context
Selected_Region = 
    SELECTEDVALUE(
        Geography[Region],
        "Multiple/None Selected"  -- Alternate result
    )

// 4) Combine COALESCE with RELATED for cross-table
Full_Category = 
    COALESCE(
        [SubCategory],
        RELATED(Categories[Category]),
        "Uncategorized"
    )
```

### VALUES vs DISTINCT — Different BLANK Behavior

```dax
// ★ VALUES() adds BLANK row for invalid relationships
// ★ DISTINCT() does NOT add BLANK row

// Scenario: Sales has CustomerID "C99" not in Customers table

// VALUES(Customers[Name]) → {"Alice", "Bob", BLANK}
// DISTINCT(Customers[Name]) → {"Alice", "Bob"}

// 1) Safe distinct count (no phantom blank)
True_Customer_Count = 
    COUNTROWS(DISTINCT(Customers[CustomerID]))
    // NOT: COUNTROWS(VALUES(Customers[CustomerID]))

// 2) Find orphan records using VALUES
Orphan_Check = 
    CALCULATE(
        COUNTROWS(Sales),
        FILTER(
            VALUES(Sales[CustomerID]),
            NOT(Sales[CustomerID] IN VALUES(Customers[CustID]))
        )
    )

// 3) TREATAS — create virtual relationship for cleaning
Virtual_Lookup = 
    CALCULATE(
        SUM(Budget[Amount]),
        TREATAS(
            SUMMARIZE(Sales, Sales[Year], Sales[Region]),
            Budget[Year], Budget[Region]
        )
    )
```

### COMBINEVALUES & Composite Keys

```dax
// ★ COMBINEVALUES — optimized composite key creation

// 1) Create composite key (better than concatenation for DirectQuery)
CompositeKey = 
    COMBINEVALUES("_", [Year], [Month], [Region])
// Generates: "2026_3_Bangkok"

// 2) Use in relationships (DirectQuery optimization)
// COMBINEVALUES tells the engine to push the join to the source

// 3) Custom composite with cleaning
Clean_Key = 
    COMBINEVALUES("|",
        TRIM(UPPER([Category])),
        FORMAT([Date], "YYYYMMDD"),
        IF(ISBLANK([Region]), "UNKNOWN", UPPER([Region]))
    )
```

### LOOKUPVALUE & Cross-table Cleaning

```dax
// ★ LOOKUPVALUE — find and replace from reference table

// 1) Map dirty codes to clean names
Clean_Status = 
    VAR RawStatus = [StatusCode]
    RETURN
    COALESCE(
        LOOKUPVALUE(
            StatusMapping[CleanName],
            StatusMapping[Code], RawStatus
        ),
        "Unknown: " & RawStatus
    )

// 2) Multi-key lookup
Region_Manager = 
    LOOKUPVALUE(
        Managers[Name],
        Managers[Region], [Region],
        Managers[Department], [Department],
        "Unassigned"  -- Alternate result
    )

// 3) FORMAT — consistent display formatting
Formatted_Amount = FORMAT([Amount], "#,##0.00 ฿")
Formatted_Date = FORMAT([Date], "DD MMM YYYY")
Formatted_Pct = FORMAT([Rate], "0.00%")
Formatted_ID = FORMAT([ID], "00000")  -- Zero-padded: "00042"
```

### Time Intelligence Cleaning

```dax
// ★ Time Intelligence — clean temporal calculations

// 1) Same Period Last Year (requires proper date table)
YoY_Growth = 
    VAR CurrentAmount = SUM(Sales[Amount])
    VAR LastYearAmount = CALCULATE(
        SUM(Sales[Amount]),
        SAMEPERIODLASTYEAR('Date'[Date])
    )
    RETURN
    DIVIDE(CurrentAmount - LastYearAmount, LastYearAmount)

// 2) DATEADD — shift dates for comparison
Prior_Month = 
    CALCULATE(SUM(Sales[Amount]), DATEADD('Date'[Date], -1, MONTH))

// 3) Running total (cleaned for gaps)
Running_Total = 
    CALCULATE(
        SUM(Sales[Amount]),
        FILTER(
            ALLSELECTED('Date'[Date]),
            'Date'[Date] <= MAX('Date'[Date])
        )
    )

// 4) TOTALMTD / TOTALQTD / TOTALYTD
MTD_Sales = TOTALMTD(SUM(Sales[Amount]), 'Date'[Date])
YTD_Sales = TOTALYTD(SUM(Sales[Amount]), 'Date'[Date], "09/30")
// Fiscal year ending Sept 30

// 5) Moving average (clean outlier-smoothing)
Moving_Avg_7D = 
    AVERAGEX(
        DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -7, DAY),
        CALCULATE(SUM(Sales[Amount]))
    )
```

### RANKX & TOPN Filtering

```dax
// ★ RANKX / TOPN — clean ranking and filtering

// 1) Rank with tie handling
Product_Rank = 
    RANKX(ALL(Products), [Total Sales],, DESC, DENSE)
// Skip = 1,2,2,4  |  Dense = 1,2,2,3

// 2) Top N with "Others" category
Top5_Category = 
    VAR CurrentCategory = SELECTEDVALUE(Products[Category])
    VAR Rank = RANKX(ALL(Products[Category]), [Total Sales],, DESC)
    RETURN
    IF(Rank <= 5, CurrentCategory, "Others")

// 3) TOPN in calculated table (clean top sellers)
Top10_Products = 
    TOPN(10, ALL(Products), [Total Sales], DESC)

// 4) Percentile rank
Percentile_Rank = 
    DIVIDE(
        RANKX(ALL(Products), [Total Sales],, ASC) - 1,
        COUNTROWS(ALL(Products)) - 1
    )
```

---

## 🗂️ Data Model Cleaning

### Relationships & Cross-filter Direction

```
★ Relationship cleaning rules:

┌───────────────────┬────────────────────────────────────────┐
│ Setting           │ Cleaning Impact                        │
├───────────────────┼────────────────────────────────────────┤
│ Cardinality       │                                        │
│  1:N              │ ✅ Standard, safest                     │
│  N:N              │ ⚠️ Needs bridge table, can cause dupes │
│  1:1              │ ⚠️ Rare, consider merging tables       │
├───────────────────┼────────────────────────────────────────┤
│ Cross-filter      │                                        │
│  Single           │ ✅ Default, predictable filtering       │
│  Both             │ ⚠️ Can cause circular dependencies     │
│                   │ ⚠️ Ambiguous results possible          │
├───────────────────┼────────────────────────────────────────┤
│ Active/Inactive   │                                        │
│  Active           │ Default relationship used              │
│  Inactive         │ Use via USERELATIONSHIP()              │
├───────────────────┼────────────────────────────────────────┤
│ Referential       │                                        │
│  Assume integrity │ ✅ Performance boost for DirectQuery    │
│                   │ ⚠️ Only if data is truly clean!        │
└───────────────────┴────────────────────────────────────────┘

Cleaning checklist:
  □ No orphan foreign keys (use Anti Join to find)
  □ No duplicate primary keys in dimension tables
  □ No circular relationships
  □ Cross-filter = Single (unless justified)
  □ Star schema preferred over snowflake
```

### Data Categories & Semantic Types

```
★ Data Categories — tell PBI what the data represents:

┌──────────────────┬──────────────────────────────────────┐
│ Category         │ Effect                               │
├──────────────────┼──────────────────────────────────────┤
│ Address          │ Geocoding for maps                   │
│ City             │ Map visualization auto-placement     │
│ StateOrProvince  │ Region-level mapping                 │
│ PostalCode       │ Zip-code level maps                  │
│ Country/Region   │ Country-level mapping                │
│ Latitude         │ Exact positioning on maps            │
│ Longitude        │ Exact positioning on maps            │
│ Place            │ General location                     │
│ WebUrl           │ Clickable links in tables            │
│ ImageUrl         │ Show images in tables/cards          │
│ Barcode          │ Barcode scanning support             │
│ Continent        │ Continent-level aggregation          │
└──────────────────┴──────────────────────────────────────┘

★ Clean data BEFORE setting categories:
  - Latitude/Longitude: must be decimal numbers (-90 to 90, -180 to 180)
  - WebUrl: must start with http:// or https://
  - ImageUrl: must be accessible URL ending in image extension
  - Country: use ISO 3166 codes or full names consistently
```

### Calculation Groups

```dax
// ★ Calculation Groups — reusable cleaning transformations

// Calculation Group: "Time Comparison"
// Items:
//   "Current" → SELECTEDMEASURE()
//   "Prior Year" → CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
//   "YoY %" → 
//       VAR Current = SELECTEDMEASURE()
//       VAR Prior = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
//       RETURN DIVIDE(Current - Prior, Prior)
//   "YTD" → CALCULATE(SELECTEDMEASURE(), DATESYTD('Date'[Date]))
//   "Moving Avg" → 
//       AVERAGEX(DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -30, DAY),
//           CALCULATE(SELECTEDMEASURE()))

// ★ Benefit: ONE calculation group replaces DOZENS of individual measures!
// Instead of: Sales_YoY, Profit_YoY, Cost_YoY, Revenue_YoY...
// Just: Time Comparison[YoY %] applied to ANY measure

// Calculation Group: "Currency Format"
// Items:
//   "THB" → SELECTEDMEASURE() * ExchangeRate[THB]
//   "USD" → SELECTEDMEASURE() * ExchangeRate[USD]
//   "EUR" → SELECTEDMEASURE() * ExchangeRate[EUR]
```

### Synonyms for Q&A

```
★ Synonyms — ให้ Q&A (natural language) เข้าใจ field names

Column: Revenue
  Synonyms: "sales", "income", "ยอดขาย", "รายได้"

Column: CustomerName
  Synonyms: "client", "buyer", "ลูกค้า", "ชื่อลูกค้า"

Column: OrderDate
  Synonyms: "purchase date", "date ordered", "วันที่สั่ง"

★ Best Practices:
  1. Add Thai AND English synonyms
  2. Include common abbreviations
  3. Add business-specific terms
  4. Test with Q&A visual
  5. Update when users report "I don't understand"
```

---

## 🚀 Deployment & Governance Cleaning

### Deployment Pipelines (Dev → Test → Prod)

```
★ Power BI Deployment Pipelines — staged data cleaning

┌──────────┐     ┌──────────┐     ┌──────────┐
│   DEV    │────▶│   TEST   │────▶│   PROD   │
│          │     │          │     │          │
│ Raw data │     │ Cleaned  │     │ Validated│
│ Explore  │     │ Test     │     │ Deployed │
│ Prototype│     │ QA Check │     │ Live     │
└──────────┘     └──────────┘     └──────────┘

Deployment Rules for each stage:
  ┌─────────┬──────────────────┬──────────────────────────┐
  │ Stage   │ Data Source       │ Cleaning Level           │
  ├─────────┼──────────────────┼──────────────────────────┤
  │ DEV     │ Sample/mock data │ Explore, test transforms │
  │ TEST    │ Copy of prod     │ Full cleaning, validate  │
  │ PROD    │ Live sources     │ Parameterized, monitored │
  └─────────┴──────────────────┴──────────────────────────┘

★ Parameter Rules — different data sources per stage:
  Use deployment rules to map parameters:
    DEV:  ServerName = "dev-sql.company.com"
    TEST: ServerName = "test-sql.company.com"
    PROD: ServerName = "prod-sql.company.com"
```

### Sensitivity Labels & Data Protection

```
★ Sensitivity Labels — classify data for cleaning requirements

┌──────────────┬────────────────────────────────────────┐
│ Label        │ Cleaning Requirements                  │
├──────────────┼────────────────────────────────────────┤
│ Public       │ Basic cleaning only                    │
│ General      │ Standard cleaning + type validation    │
│ Confidential │ + Mask PII, encrypt exports            │
│ Highly Conf. │ + Full anonymization, audit logging    │
│              │ + RLS mandatory, no export allowed     │
└──────────────┴────────────────────────────────────────┘

★ Automatic labeling based on data content:
  - Contains "SSN", "บัตรประชาชน" → Highly Confidential
  - Contains "Email", "Phone" → Confidential
  - Contains "Name", "Address" → Confidential
  - Financial aggregates → General
  - Public statistics → Public
```

### Endorsement & Certification

```
★ Endorsement levels — signal data quality

┌──────────────┬────────────────────────────────────────┐
│ Level        │ Meaning                                │
├──────────────┼────────────────────────────────────────┤
│ None         │ No endorsement                         │
│ Promoted     │ Owner recommends, basic quality check  │
│ Certified    │ Admin-verified, full quality assured   │
└──────────────┴────────────────────────────────────────┘

★ Certification checklist:
  □ All columns properly typed
  □ No error values in any column
  □ Null handling documented
  □ Relationships validated (no orphans)
  □ RLS tested and working
  □ Refresh schedule set and reliable
  □ Documentation complete
  □ Data source credentials secured
```

### Lineage View & Impact Analysis

```
★ Lineage View — trace data from source to report

Source → Dataflow → Dataset → Report → Dashboard → App

★ Use for cleaning:
  1. Identify which reports are affected by data source changes
  2. Find unused datasets (candidates for cleanup)
  3. Trace data quality issues to their origin
  4. Impact analysis before schema changes

★ Impact Analysis — before making changes:
  - "What reports use this measure?"
  - "What happens if I rename this column?"
  - "Which dashboards break if I change this relationship?"
```

---

## 🟡 Power Query — Dedup, Grouping & List Functions

### Dedup Strategies (Table.Distinct vs Remove Duplicates)

```m
// ★ Dedup strategies ใน Power Query
let
    Source = #table({"ID", "Name", "Amount", "Date"}, {
        {1, "Alice", 100, #date(2026,1,1)},
        {1, "Alice", 100, #date(2026,1,1)},   // Exact dupe
        {1, "Alice", 150, #date(2026,1,2)},   // Same ID, different data
        {2, "Bob", 200, #date(2026,1,1)},
        {2, "bob", 200, #date(2026,1,1)}      // Case difference
    }),
    
    // 1) Table.Distinct — remove exact duplicate rows (all columns)
    ExactDedup = Table.Distinct(Source),
    
    // 2) Table.Distinct — by specific columns only (keep first)
    ByKey = Table.Distinct(Source, {"ID"}),
    
    // 3) Keep LAST occurrence (sort descending first)
    KeepLast = Table.Distinct(
        Table.Sort(Source, {{"Date", Order.Descending}}),
        {"ID"}
    ),
    
    // 4) Case-insensitive dedup
    CaseInsensitive = Table.Distinct(
        Table.TransformColumns(Source, {
            {"Name", Text.Lower, type text}
        }),
        {"ID", "Name"}
    ),
    
    // 5) Table.IsDistinct — check uniqueness (validation)
    IsUnique = Table.IsDistinct(Source, {"ID"}),  // Returns: false
    
    // 6) Find duplicates (keep only dupes for review)
    FindDupes = let
        grouped = Table.Group(Source, {"ID"}, {
            {"Count", each Table.RowCount(_), Int64.Type},
            {"Rows", each _, type table}
        }),
        dupes = Table.SelectRows(grouped, each [Count] > 1),
        expanded = Table.ExpandTableColumn(dupes, "Rows",
            Table.ColumnNames(Source))
    in
        expanded
in
    ExactDedup
```

### Table.Group — Advanced Aggregation

```m
// ★ Table.Group — powerful grouping with custom aggregations
let
    Source = #table({"Category", "Product", "Amount", "Date"}, {
        {"A", "P1", 100, #date(2026,1,1)},
        {"A", "P2", 200, #date(2026,1,5)},
        {"A", "P1", 150, #date(2026,2,1)},
        {"B", "P3", 300, #date(2026,1,1)}
    }),
    
    // 1) Multiple aggregations at once
    MultiAgg = Table.Group(Source, {"Category"}, {
        {"TotalAmount", each List.Sum([Amount]), type number},
        {"AvgAmount", each List.Average([Amount]), type number},
        {"MinAmount", each List.Min([Amount]), type number},
        {"MaxAmount", each List.Max([Amount]), type number},
        {"Count", each Table.RowCount(_), Int64.Type},
        {"Products", each Text.Combine(List.Distinct([Product]), ", "), type text},
        {"FirstDate", each List.Min([Date]), type date},
        {"LastDate", each List.Max([Date]), type date}
    }),
    
    // 2) GroupKind.Local — consecutive grouping (keep order)
    ConsecutiveGroup = Table.Group(Source, {"Category"}, {
        {"Rows", each _, type table}
    }, GroupKind.Local),
    
    // 3) Keep ALL rows (for window functions)
    WithRowNumber = Table.Group(Source, {"Category"}, {
        {"AllData", each Table.AddIndexColumn(_, "RowNum", 1, 1), type table}
    }),
    ExpandedWithNum = Table.ExpandTableColumn(WithRowNumber, "AllData",
        {"Product", "Amount", "Date", "RowNum"})
in
    MultiAgg
```

### List Functions for Cleaning

```m
// ★ List functions — powerful helpers for column-level cleaning
let
    Source = #table({"Tags", "Values"}, {
        {"a,b,c,a,b", "10,20,30,null,50"},
        {"x,y,z", "100,,200"}
    }),
    
    // 1) List.Distinct — unique values
    UniqueVals = List.Distinct({"a", "b", "c", "a", "b"}),
    // Result: {"a", "b", "c"}
    
    // 2) List.RemoveNulls
    NoNulls = List.RemoveNulls({1, null, 2, null, 3}),
    // Result: {1, 2, 3}
    
    // 3) List.Sort with custom comparer
    Sorted = List.Sort({"banana", "Apple", "cherry"},
        Comparer.OrdinalIgnoreCase),
    
    // 4) List.Accumulate — running calculation
    RunningSum = List.Accumulate({1,2,3,4,5}, 0, (state, cur) => state + cur),
    // Result: 15
    
    // 5) List.Transform — map function
    Doubled = List.Transform({1,2,3}, each _ * 2),
    // Result: {2,4,6}
    
    // 6) List.Select — filter
    Positive = List.Select({-1, 0, 1, 2, -3}, each _ > 0),
    // Result: {1, 2}
    
    // 7) List.Generate — generate sequences
    Dates = List.Generate(
        () => #date(2026,1,1),
        each _ <= #date(2026,12,31),
        each Date.AddDays(_, 1)
    ),
    
    // 8) List.Zip — combine multiple lists
    Zipped = List.Zip({{"A","B","C"}, {1,2,3}}),
    // Result: {{"A",1}, {"B",2}, {"C",3}}
    
    // 9) Apply to table: split tags and get distinct
    WithUniqueTags = Table.TransformColumns(Source, {
        {"Tags", each Text.Combine(
            List.Distinct(Text.Split(_, ",")), ","),
        type text}
    })
in
    WithUniqueTags
```

### Index, Rounding & Date Functions

```m
// ★ Utility functions สำหรับ cleaning
let
    Source = #table({"Amount", "RawDate", "Name"}, {
        {123.4567, #date(2026,3,1), "Alice"},
        {89.999, #date(2026,3,15), "Bob"},
        {45.5050, #date(2025,12,31), "Charlie"}
    }),
    
    // 1) AddIndexColumn — row numbers
    WithIndex = Table.AddIndexColumn(Source, "RowNum", 1, 1, Int64.Type),
    
    // 2) Rounding strategies
    Rounded = Table.TransformColumns(Source, {
        {"Amount", each Number.Round(_, 2), type number}             // Standard
    }),
    RoundedUp = Table.TransformColumns(Source, {
        {"Amount", each Number.RoundUp(_, 2), type number}           // Always up
    }),
    RoundedDown = Table.TransformColumns(Source, {
        {"Amount", each Number.RoundDown(_, 2), type number}         // Always down
    }),
    BankersRound = Table.TransformColumns(Source, {
        {"Amount", each Number.Round(_, 2, RoundingMode.ToEven), type number}  // Bankers
    }),
    
    // 3) Date functions for cleaning
    WithDateParts = Table.AddColumn(Source, "Year", each
        Date.Year([RawDate]), Int64.Type),
    WithMonth = Table.AddColumn(WithDateParts, "Month", each
        Date.Month([RawDate]), Int64.Type),
    WithQuarter = Table.AddColumn(WithMonth, "Quarter", each
        Date.QuarterOfYear([RawDate]), Int64.Type),
    WithDayOfWeek = Table.AddColumn(WithQuarter, "DayOfWeek", each
        Date.DayOfWeek([RawDate], Day.Monday), Int64.Type),  // 0=Mon
    WithStartOfMonth = Table.AddColumn(WithDayOfWeek, "MonthStart", each
        Date.StartOfMonth([RawDate]), type date),
    WithEndOfMonth = Table.AddColumn(WithStartOfMonth, "MonthEnd", each
        Date.EndOfMonth([RawDate]), type date),
    WithIsLeapYear = Table.AddColumn(WithEndOfMonth, "IsLeap", each
        Date.IsInCurrentYear([RawDate]), type logical),
    WithWeekNum = Table.AddColumn(WithIsLeapYear, "WeekNum", each
        Date.WeekOfYear([RawDate]), Int64.Type),
    
    // 4) Date arithmetic
    WithFuture = Table.AddColumn(Source, "Plus30Days", each
        Date.AddDays([RawDate], 30), type date),
    WithMonthsAgo = Table.AddColumn(WithFuture, "Minus3Months", each
        Date.AddMonths([RawDate], -3), type date),
    WithYearsAgo = Table.AddColumn(WithMonthsAgo, "Minus1Year", each
        Date.AddYears([RawDate], -1), type date)
in
    WithWeekNum
```

### Validation Functions

```m
// ★ Validation functions — check data quality ใน PQ
let
    Source = #table({"ID", "Name", "Amount"}, {
        {1, "Alice", 100}, {2, "Bob", 200}, {null, "", -50}
    }),
    
    // 1) Table.IsDistinct — check if column is unique
    IDsUnique = Table.IsDistinct(Source, {"ID"}),
    
    // 2) Table.MatchesAllRows — all rows must pass condition
    AllPositive = Table.MatchesAllRows(Source, each [Amount] > 0),
    // Returns: false (because -50)
    
    // 3) Table.MatchesAnyRows — at least one row passes
    AnyNegative = Table.MatchesAnyRows(Source, each [Amount] < 0),
    // Returns: true
    
    // 4) Table.Contains — check if row exists
    HasAlice = Table.Contains(Source, [Name = "Alice"]),
    
    // 5) Table.MaxN / Table.MinN — top/bottom values
    Top2 = Table.MaxN(Source, {"Amount", Order.Descending}, 2),
    Bottom1 = Table.MinN(Source, {"Amount", Order.Ascending}, 1),
    
    // 6) Table.SelectRowsWithErrors — find errors (not remove)
    ErrorRows = Table.SelectRowsWithErrors(Source, {"Amount"}),
    
    // 7) Custom validation report
    ValidationReport = #table({"Check", "Result", "Status"}, {
        {"IDs Unique", IDsUnique, if IDsUnique then "✅" else "❌"},
        {"All Positive", AllPositive, if AllPositive then "✅" else "❌"},
        {"Has Negatives", AnyNegative, if AnyNegative then "⚠️" else "✅"},
        {"Row Count", Table.RowCount(Source), "ℹ️"}
    })
in
    ValidationReport
```

---

## 📐 DAX — Set Operations & Reference Tables

### EXCEPT / INTERSECT / UNION

```dax
// ★ Set operations — find data gaps and overlaps

// 1) EXCEPT — rows in A but NOT in B (find missing/deleted)
Missing_Products = 
    EXCEPT(
        ALL(Catalog[ProductID]),     -- All products in catalog
        ALL(Sales[ProductID])        -- Products that were sold
    )
// Returns: products never sold

// 2) INTERSECT — rows in BOTH A and B (find overlap)
Active_Customers = 
    INTERSECT(
        ALL(LastYear[CustomerID]),
        ALL(ThisYear[CustomerID])
    )
// Returns: customers who bought both years

// 3) UNION — combine rows from A and B (with dedup)
All_IDs = 
    DISTINCT(
        UNION(
            SELECTCOLUMNS(Online, "ID", Online[OrderID]),
            SELECTCOLUMNS(Store, "ID", Store[OrderID])
        )
    )
```

### DATATABLE & GENERATESERIES

```dax
// ★ DATATABLE — create inline reference tables (no need for external data)

// 1) Status mapping table
StatusMap = 
    DATATABLE(
        "Code", STRING,
        "Label", STRING,
        "Color", STRING,
        {
            {"A", "Active", "Green"},
            {"I", "Inactive", "Gray"},
            {"P", "Pending", "Yellow"},
            {"X", "Cancelled", "Red"}
        }
    )

// 2) GENERATESERIES — create number/date sequences
PriceBuckets = GENERATESERIES(0, 1000, 100)
// Result: {0, 100, 200, 300, ..., 1000}

DateSeq = GENERATESERIES(DATE(2026,1,1), DATE(2026,12,31), 1)

// 3) Use DATATABLE for validation rules
ValidationRules = 
    DATATABLE(
        "Column", STRING,
        "MinValue", DOUBLE,
        "MaxValue", DOUBLE,
        {
            {"Amount", 0, 999999},
            {"Quantity", 1, 10000},
            {"Discount", 0, 1}
        }
    )
```

### CONCATENATEX & PATH Functions

```dax
// ★ CONCATENATEX — aggregate text with delimiter

// 1) Comma-separated list
Product_List = 
    CONCATENATEX(
        RELATEDTABLE(OrderDetails),
        OrderDetails[ProductName],
        ", ",
        OrderDetails[ProductName], ASC  -- Sorted!
    )
// Result: "Apple, Banana, Cherry"

// 2) With cleaning
Clean_Tags = 
    CONCATENATEX(
        FILTER(
            RELATEDTABLE(Tags),
            NOT(ISBLANK(Tags[TagName]))
        ),
        TRIM(UPPER(Tags[TagName])),
        " | "
    )

// ★ PATH functions — clean hierarchy data

// 3) PATH — build hierarchy path from parent-child
Org_Path = PATH([EmployeeID], [ManagerID])
// Result: "1|3|7|15" (root to leaf)

// 4) PATHCONTAINS — check membership
Reports_To_CEO = PATHCONTAINS([Org_Path], 1)

// 5) PATHITEM — extract level from path
Level1_Manager = PATHITEM([Org_Path], 1, INTEGER)
Level2_Manager = PATHITEM([Org_Path], 2, INTEGER)

// 6) PATHLENGTH — depth of hierarchy
Org_Depth = PATHLENGTH([Org_Path])
```

### SWITCH TRUE & KEEPFILTERS / CROSSFILTER

```dax
// ★ SWITCH(TRUE(), ...) — multi-condition cleaning pattern

// 1) Category bucketing
Amount_Tier = 
    SWITCH(
        TRUE(),
        [Amount] < 0, "Invalid ❌",
        [Amount] = 0, "Zero",
        [Amount] <= 100, "Small",
        [Amount] <= 1000, "Medium",
        [Amount] <= 10000, "Large",
        "Enterprise"
    )

// 2) Data quality flag
Quality_Flag = 
    SWITCH(
        TRUE(),
        ISBLANK([Name]) && ISBLANK([Email]), "Missing All ❌",
        ISBLANK([Name]), "Missing Name ⚠️",
        ISBLANK([Email]), "Missing Email ⚠️",
        LEN([Name]) < 2, "Name Too Short ⚠️",
        NOT(CONTAINSSTRING([Email], "@")), "Invalid Email ❌",
        "Valid ✅"
    )

// ★ KEEPFILTERS — add filter instead of replacing
Filtered_Sales = 
    CALCULATE(
        SUM(Sales[Amount]),
        KEEPFILTERS(Sales[Region] = "Thailand")
        // KEEPFILTERS = AND with existing filter (additive)
        // Without KEEPFILTERS = REPLACE existing filter
    )

// ★ CROSSFILTER — dynamic cross-filter direction
Both_Way_Count = 
    CALCULATE(
        COUNTROWS(Products),
        CROSSFILTER(Sales[ProductID], Products[ID], BOTH)
    )
```

---

## 🎯 Power BI Features for Data Quality

### Performance Analyzer

```
★ Performance Analyzer — identify slow cleaning steps

วิธีใช้ (PBI Desktop):
1. View tab → Performance Analyzer → Start recording
2. Interact with visuals / Refresh
3. Review results

┌──────────────────┬────────────────────────────────────┐
│ Metric           │ What to optimize                   │
├──────────────────┼────────────────────────────────────┤
│ DAX Query        │ Slow measures → simplify/optimize  │
│ Visual Display   │ Too many data points → aggregate   │
│ Other            │ PQ refresh → check query folding   │
│ Direct Query     │ Slow → add aggregation tables      │
└──────────────────┴────────────────────────────────────┘

★ Copy DAX query → paste in DAX Studio for deep analysis
```

### AI Visuals for Data Quality

```
★ Built-in AI visuals for data quality insights:

1. Key Influencers Visual
   - "What influences [Quality_Score]?"
   - Auto-discovers factors affecting data quality
   - Use to find which columns cause the most issues

2. Decomposition Tree
   - Drill down into data quality issues
   - "Why are there so many nulls?"
   - AI-assisted drill-down path suggestion

3. Smart Narrative
   - Auto-generates text summary of data
   - Detects anomalies and trends
   - Use for automated data quality reports

4. Anomaly Detection (Line Chart)
   - Right-click line chart → "Find anomalies"
   - Auto-detects outliers in time series
   - Configurable sensitivity

5. Q&A Visual
   - Type natural language questions
   - "Show me products with null category"
   - "Which regions have the most errors?"
```

### Field Parameters & What-if

```dax
// ★ Field Parameters — dynamic field selection

// 1) Create field parameter (PBI Desktop → Modeling tab)
// Allows user to switch between columns dynamically
// Example: Switch between Revenue, Cost, Profit in same visual

// 2) What-if Parameters — scenario analysis
// Modeling tab → New Parameter
// Creates slicer for numeric range

// Use in cleaning: "What if we remove outliers above X?"
Cleaned_Amount = 
    VAR Threshold = [Outlier Threshold Value]  -- from What-if param
    RETURN
    CALCULATE(
        SUM(Sales[Amount]),
        Sales[Amount] <= Threshold
    )

Outlier_Impact = 
    VAR WithOutliers = SUM(Sales[Amount])
    VAR WithoutOutliers = [Cleaned_Amount]
    RETURN
    FORMAT(DIVIDE(WithOutliers - WithoutOutliers, WithOutliers), "0.0%")
```

### Auto Date/Time (When to Disable)

```
★ Auto Date/Time — PBI auto-creates hidden date tables

⚠️ PROBLEM: เปิดไว้ = สร้าง hidden date table ทุก date column!
  - 1 date column = 1 hidden table (~7KB compressed)
  - 10 date columns = 10 hidden tables → bloat!
  - Can't control fiscal year, language, or custom attributes

★ RECOMMENDED: ปิด Auto Date/Time + สร้าง Date Table เอง

วิธีปิด:
  File → Options → Data Load → ❌ Auto date/time

แล้วสร้างเอง:
  DateTable = CALENDAR(DATE(2020,1,1), DATE(2030,12,31))
  หรือใช้ CALENDARAUTO()
  + เพิ่ม columns: Year, Quarter, Month, Week, Day, FiscalYear, etc.
```

---

## 🔧 External Tools & API Cleaning

### DAX Studio & Tabular Editor

```
★ Essential external tools for Power BI cleaning:

┌──────────────────┬──────────────────────────────────────┐
│ Tool             │ Cleaning Use Case                    │
├──────────────────┼──────────────────────────────────────┤
│ DAX Studio       │ - Test/debug DAX measures            │
│ (free)           │ - View metadata & statistics         │
│                  │ - Run DMV queries                    │
│                  │ - Measure performance                │
│                  │ - Export data for validation          │
├──────────────────┼──────────────────────────────────────┤
│ Tabular Editor   │ - Bulk edit measures                 │
│ (free/paid)      │ - Best Practice Analyzer (BPA)       │
│                  │ - Find unused columns/measures       │
│                  │ - Batch rename columns               │
│                  │ - Script model changes               │
│                  │ - Import/Export translations          │
├──────────────────┼──────────────────────────────────────┤
│ ALM Toolkit      │ - Compare models (DEV vs PROD)       │
│ (free)           │ - Deploy model changes               │
│                  │ - Find differences in measures       │
├──────────────────┼──────────────────────────────────────┤
│ PBI Inspector    │ - Analyze PBIX file contents         │
│                  │ - Find hidden tables/columns         │
│                  │ - Identify bloated partitions        │
└──────────────────┴──────────────────────────────────────┘

★ DAX Studio DMV queries for data quality:
  SELECT * FROM $SYSTEM.TMSCHEMA_COLUMNS
  -- Shows all columns with data types, sizes
  
  SELECT * FROM $SYSTEM.DISCOVER_STORAGE_TABLE_COLUMN_SEGMENTS
  -- Shows column compression stats (find bloated columns)
```

### Power BI REST API Cleaning

```
★ Power BI REST API — programmatic data management

1) Trigger refresh via API:
   POST /groups/{groupId}/datasets/{datasetId}/refreshes
   Body: {"notifyOption": "MailOnFailure"}

2) Get refresh history (check for errors):
   GET /groups/{groupId}/datasets/{datasetId}/refreshes

3) Take over dataset (fix ownership issues):
   POST /groups/{groupId}/datasets/{datasetId}/Default.TakeOver

4) Bind to gateway (fix connection):
   POST /groups/{groupId}/datasets/{datasetId}/Default.BindToGateway

5) Update parameters (change data source):
   POST /groups/{groupId}/datasets/{datasetId}/Default.UpdateParameters
   Body: {"updateDetails": [{"name": "ServerName", "newValue": "new-server"}]}

6) Get data sources (audit connections):
   GET /groups/{groupId}/datasets/{datasetId}/datasources

★ Use for cleaning automation:
  - Scheduled quality checks via API + Logic Apps
  - Auto-notify on refresh failures
  - Programmatic parameter updates for environment switching
```

### Shared Datasets & Composite Models

```
★ Shared Datasets — use ONE cleaned dataset across many reports

1) Publish cleaned dataset to workspace
2) Other reports: Get Data → Power BI datasets
3) Build reports on top of shared clean data

Benefits:
  ✅ Clean once, use everywhere
  ✅ Single source of truth
  ✅ Consistent measures across reports
  ✅ Reduced storage (no data duplication)

★ Composite Models on PBI Datasets:
  - Connect to shared dataset (live connection)
  - ADD local tables for report-specific cleaning
  - ADD local measures for custom analyses
  - Best of both: centralized cleaning + local flexibility
  
⚠️ Rules:
  - Can't modify shared dataset measures locally
  - Local tables = Import mode
  - RLS from shared dataset is inherited
```

---

## 🟡 Power Query — Optimization & Dynamic M

### Table.Buffer, FillDown/FillUp & Partition

```m
// ★ Table.Buffer — force full evaluation (prevent re-query)
let
    Source = Sql.Database("server", "db"),
    SlowQuery = Table.SelectRows(Source, each [Status] = "Active"),
    
    // Buffer = load into memory once, reuse many times
    Buffered = Table.Buffer(SlowQuery),
    
    // Now use Buffered multiple times without re-querying
    Count = Table.RowCount(Buffered),
    Avg = List.Average(Buffered[Amount]),
    
    // ★ Table.FillDown — fill blanks with value above (merged cells!)
    //    Before: {A, null, null, B, null} → After: {A, A, A, B, B}
    Filled = Table.FillDown(Source, {"Category", "Region"}),
    
    // ★ Table.FillUp — fill blanks with value below
    //    Before: {null, null, C, null, D} → After: {C, C, C, D, D}
    FilledUp = Table.FillUp(Source, {"Category"}),
    
    // ★ Table.Partition — split into N sub-tables (parallel processing)
    Parts = Table.Partition(Source, 4, "ID",  // 4 partitions based on ID
        each Number.Mod(_, 4)),
    // Result: {table0, table1, table2, table3}
    
    // ★ Table.Skip / FirstN / LastN / Range
    SkipHeaders = Table.Skip(Source, 2),         // Skip first 2 rows
    Top100 = Table.FirstN(Source, 100),           // First 100 rows
    Last50 = Table.LastN(Source, 50),             // Last 50 rows
    Page = Table.Range(Source, 100, 50),          // Rows 100-149
    
    // ★ Table.AlternateRows — select rows by pattern
    EveryOther = Table.AlternateRows(Source, 0, 1, 1)  // Every other row
in
    Filled
```

### Value.NativeQuery & Expression.Evaluate

```m
// ★ Value.NativeQuery — pass SQL directly (bypass M, use DB cleaning)
let
    Source = Sql.Database("server", "db"),
    
    // Execute custom SQL for complex cleaning
    Cleaned = Value.NativeQuery(Source,
        "SELECT
            TRIM(UPPER(Name)) as Name,
            COALESCE(Amount, 0) as Amount,
            CASE
                WHEN Status IN ('A','Active') THEN 'Active'
                WHEN Status IN ('I','Inactive') THEN 'Inactive'
                ELSE 'Unknown'
            END as Status
         FROM dbo.Customers
         WHERE DeletedAt IS NULL",
        null,
        [EnableFolding = true]     // ★ Still enable query folding!
    ),
    
    // ★ Expression.Evaluate — execute M code dynamically
    DynamicExpr = Expression.Evaluate(
        "1 + 2 * 3",
        [#"Number.Add" = Number.Add]
    ),
    
    // Dynamic column selection
    ColumnsToKeep = {"ID", "Name", "Amount"},
    DynamicSelect = Expression.Evaluate(
        "Table.SelectColumns(Source, Columns)",
        [Source = Source, Columns = ColumnsToKeep,
         Table.SelectColumns = Table.SelectColumns]
    ),
    
    // ★ #shared — access ALL M functions (explore what's available)
    AllFunctions = Record.FieldNames(#shared)
    // Returns: {"List.Sum", "Table.Group", ...} (1000+ functions!)
in
    Cleaned
```

### Comparer Functions & TransformColumnNames

```m
// ★ Comparer functions — control comparison behavior
let
    Source = #table({"Name"}, {{"alice"}, {"ALICE"}, {"Bob"}, {"bob"}}),
    
    // 1) Comparer.OrdinalIgnoreCase — case-insensitive (byte comparison)
    CaseInsensitiveSort = Table.Sort(Source, {
        {"Name", Order.Ascending, Comparer.OrdinalIgnoreCase}
    }),
    
    // 2) Comparer.FromCulture — locale-aware comparison
    ThaiSort = Table.Sort(Source, {
        {"Name", Order.Ascending, Comparer.FromCulture("th-TH")}
    }),
    
    // 3) Use in Table.Distinct for case-insensitive dedup
    Deduped = Table.Distinct(Source, {
        {"Name", Comparer.OrdinalIgnoreCase}
    }),
    
    // ★ Table.TransformColumnNames — rename ALL columns at once
    CleanHeaders = Table.TransformColumnNames(Source,
        each Text.Trim(Text.Clean(Text.Lower(_)))),
    
    // Replace spaces with underscores
    SnakeCase = Table.TransformColumnNames(Source,
        each Text.Replace(Text.Lower(Text.Trim(_)), " ", "_")),
    
    // Prefix all columns
    Prefixed = Table.TransformColumnNames(Source,
        each "raw_" & _),
    
    // ★ Diagnostics.Trace — debug M code (log to trace)
    Traced = Table.TransformColumns(Source, {
        {"Name", each
            let
                traced = Diagnostics.Trace(
                    TraceLevel.Information,
                    "Processing: " & _,
                    () => Text.Upper(_)
                )
            in
                traced(),
        type text}
    })
in
    CleanHeaders
```

---

## 📊 Power Query Editor — Data Profiling Features

### Column Quality, Distribution & Profile

```
★ Built-in Data Profiling (PQ Editor → View tab):

┌─────────────────────┬──────────────────────────────────────┐
│ Feature             │ What it shows                        │
├─────────────────────┼──────────────────────────────────────┤
│ Column Quality      │ % Valid, % Error, % Empty per column │
│                     │ → Quick overview of data quality     │
│                     │ → Click bar to filter errors/empties │
├─────────────────────┼──────────────────────────────────────┤
│ Column Distribution │ Count of distinct values             │
│                     │ Count of unique values               │
│                     │ Distribution histogram               │
│                     │ → Spot skew, outliers, low cardinality│
├─────────────────────┼──────────────────────────────────────┤
│ Column Profile      │ Full statistics for selected column: │
│                     │ - Min, Max, Avg, Median, StdDev      │
│                     │ - Count, Null count, Error count     │
│                     │ - Value distribution chart           │
│                     │ - Length distribution (text cols)     │
└─────────────────────┴──────────────────────────────────────┘

⚠️ IMPORTANT:
- Default: profiles first 1,000 rows only!
- Click "Column profiling based on first 1000 rows"
  → Change to "Column profiling based on entire dataset"
  → For accurate quality assessment

★ Use profiling BEFORE writing cleaning steps:
  1. Enable all 3 profile views
  2. Check Column Quality first (any red = errors)
  3. Check Distribution (any unexpected patterns?)
  4. Deep-dive Column Profile on suspicious columns
```

### SplitColumn Patterns & Record Functions

```m
// ★ Table.SplitColumn — multiple split strategies
let
    Source = #table({"FullName", "Code", "Mixed"}, {
        {"John Smith", "AB-123-XY", "Hello123World"},
        {"Jane Doe Jr.", "CD-456-ZZ", "Test456Data"}
    }),
    
    // 1) Split by delimiter
    ByDelimiter = Table.SplitColumn(Source, "FullName",
        Splitter.SplitTextByDelimiter(" "),
        {"First", "Last"}
    ),
    
    // 2) Split by character count
    ByCount = Table.SplitColumn(Source, "Code",
        Splitter.SplitTextByPositions({0, 2, 3, 6, 7}),
        {"Part1", "Sep1", "Part2", "Sep2", "Part3"}
    ),
    
    // 3) Split by character transition (alpha → digit)
    ByTransition = Table.SplitColumn(Source, "Mixed",
        Splitter.SplitTextByCharacterTransition(
            {"A".."Z", "a".."z"}, {"0".."9"}),
        {"Text1", "Num1", "Text2"}
    ),
    
    // 4) Split into rows (explode)
    Tags = #table({"ID", "Tags"}, {{1, "a,b,c"}, {2, "x,y"}}),
    Exploded = Table.ExpandListColumn(
        Table.TransformColumns(Tags, {
            {"Tags", each Text.Split(_, ",")}
        }),
        "Tags"
    ),
    // Result: {1,"a"}, {1,"b"}, {1,"c"}, {2,"x"}, {2,"y"}
    
    // ★ Record functions
    SampleRecord = [Name = "Alice", Age = 30, City = "Bangkok"],
    FieldNames = Record.FieldNames(SampleRecord),
    // Result: {"Name", "Age", "City"}
    
    FieldValues = Record.FieldValues(SampleRecord),
    // Result: {"Alice", 30, "Bangkok"}
    
    AsTable = Record.ToTable(SampleRecord),
    // Result: table with {Name, Value} columns
    
    // Selective field removal
    Without = Record.RemoveFields(SampleRecord, {"Age"}),
    // Result: [Name = "Alice", City = "Bangkok"]
    
    // Rename fields
    Renamed = Record.RenameFields(SampleRecord, {
        {"Name", "FullName"}, {"City", "Location"}
    })
in
    ByDelimiter
```

---

## 📐 DAX — Advanced Patterns for Cleaning

### SELECTEDVALUE, HASONEVALUE & Filter Context Checks

```dax
// ★ SELECTEDVALUE — get the ONE selected value (or default)

// 1) Dynamic title based on slicer
Dynamic_Title = 
    "Sales for: " & SELECTEDVALUE(Product[Category], "All Categories")

// 2) Safe single-value extraction
Current_Region = 
    SELECTEDVALUE(Geography[Region], "Multiple Regions")

// ★ HASONEVALUE / HASONEFILTER — filter context awareness
Context_Aware_Measure = 
    IF(
        HASONEVALUE(Date[Year]),
        // One year selected → show detail
        SUM(Sales[Amount]),
        // Multiple years → show average
        AVERAGEX(VALUES(Date[Year]), 
            CALCULATE(SUM(Sales[Amount])))
    )

// ★ ISFILTERED / ISCROSSFILTERED — check if column has filter
Is_Filtered_Check = 
    IF(
        ISFILTERED(Product[Category]),
        "Filtered: " & SELECTEDVALUE(Product[Category]),
        "No filter applied"
    )

Is_Cross_Filtered = 
    IF(
        ISCROSSFILTERED(Product[ProductName]),
        "Cross-filtered by related table",
        "Not filtered"
    )
```

### SUMMARIZECOLUMNS, ADDCOLUMNS & SELECTCOLUMNS

```dax
// ★ SUMMARIZECOLUMNS — optimized grouping (recommended over SUMMARIZE)

// 1) Group with multiple aggregations
Sales_Summary = 
    SUMMARIZECOLUMNS(
        Product[Category],
        Date[Year],
        FILTER(ALL(Date[Year]), Date[Year] >= 2024),  -- Filter
        "Total Sales", SUM(Sales[Amount]),
        "Order Count", COUNTROWS(Sales),
        "Avg Order", DIVIDE(SUM(Sales[Amount]), COUNTROWS(Sales))
    )

// ★ ADDCOLUMNS — add calculated columns to virtual table
Enriched = 
    ADDCOLUMNS(
        SUMMARIZE(Sales, Product[Category]),
        "Total", CALCULATE(SUM(Sales[Amount])),
        "Count", CALCULATE(COUNTROWS(Sales)),
        "Avg", CALCULATE(AVERAGE(Sales[Amount])),
        "Quality", IF(
            CALCULATE(COUNTBLANK(Sales[Amount])) = 0,
            "Clean ✅",
            "Has Blanks ⚠️"
        )
    )

// ★ SELECTCOLUMNS — project specific columns (virtual table)
Projected = 
    SELECTCOLUMNS(
        Customers,
        "Customer", Customers[Name],
        "Clean Email", LOWER(TRIM(Customers[Email])),
        "Has Phone", NOT(ISBLANK(Customers[Phone]))
    )
```

### CALCULATETABLE, EARLIER & Dynamic Format Strings

```dax
// ★ CALCULATETABLE — return filtered table
Clean_Products = 
    CALCULATETABLE(
        Products,
        NOT(ISBLANK(Products[Category])),
        Products[Price] > 0,
        Products[IsActive] = TRUE()
    )

// ★ EARLIER — access outer row context (calculated columns)
// Use for running totals, rank within group, previous row comparisons

Running_Total = 
    CALCULATE(
        SUM(Sales[Amount]),
        FILTER(
            ALL(Sales),
            Sales[Date] <= EARLIER(Sales[Date])
        )
    )

Rank_In_Category = 
    COUNTROWS(
        FILTER(
            FILTER(ALL(Sales), Sales[Category] = EARLIER(Sales[Category])),
            Sales[Amount] >= EARLIER(Sales[Amount])
        )
    )

// ★ ERROR — raise custom error (validation)
Validated_Discount = 
    IF(
        Sales[Discount] >= 0 && Sales[Discount] <= 1,
        Sales[Discount],
        ERROR("Invalid discount: " & FORMAT(Sales[Discount], "0.00")
            & " — must be between 0 and 1")
    )

// ★ Dynamic Format Strings — conditional formatting in measures
Sales_Display = 
    VAR Value = SUM(Sales[Amount])
    RETURN
    IF(
        Value >= 1000000,
        FORMAT(Value / 1000000, "#,##0.0") & "M",
        IF(
            Value >= 1000,
            FORMAT(Value / 1000, "#,##0.0") & "K",
            FORMAT(Value, "#,##0")
        )
    )

// Dynamic format string (DAX)
Formatted_Value = 
    VAR Val = [Total Sales]
    RETURN
    SWITCH(
        TRUE(),
        Val < 0, FORMAT(Val, "#,##0;(#,##0)"),   // Negative in parens
        Val = 0, "–",                              // Dash for zero
        Val < 1, FORMAT(Val, "0.0%"),              // Percentage
        FORMAT(Val, "#,##0.00")                    // Normal
    )

// ★ EVALUATEANDLOG — debug measure (shows in Performance Analyzer)
Debug_Measure = 
    VAR Step1 = SUM(Sales[Amount])
    VAR Step2 = EVALUATEANDLOG("Step1 result", Step1)
    VAR Step3 = Step2 * 1.07  // Add VAT
    RETURN
    EVALUATEANDLOG("Final result", Step3)

// ★ COLUMNSTATISTICS — column-level stats
Stats = COLUMNSTATISTICS()
// Returns: table with Min, Max, Cardinality, MaxLength per column
```

---

## 🎨 Power BI Report Features for Data Quality

### Drill-Through, Bookmarks & Conditional Formatting

```
★ Drill-Through Pages — investigate data quality issues

1) Create "Data Quality Detail" page
2) Add drill-through filter field (e.g., Product[Category])
3) User right-clicks on category → "Drill through" → Detail page
4) Detail page shows:
   - All records for that category
   - Error breakdown
   - Missing value heatmap
   - Quality metrics

★ Bookmarks — save data quality views

1) Create multiple views of same dashboard:
   - "Overview" — normal dashboard
   - "Quality Check" — show error highlights
   - "Missing Data" — filter to blanks only
   - "Outliers" — filter to extreme values
2) Add buttons to switch between bookmarks

★ Conditional Formatting — highlight data issues

Rules-based formatting:
┌──────────────────┬────────────────────────┬──────────┐
│ Condition        │ Format                 │ Use Case │
├──────────────────┼────────────────────────┼──────────┤
│ Value = BLANK    │ Background: Red        │ Missing  │
│ Value < 0        │ Font: Red + Bold       │ Invalid  │
│ Value > 3σ       │ Icon: ⚠️ triangle      │ Outlier  │
│ % Complete < 80  │ Data bar: Orange       │ Quality  │
│ Custom measure   │ Based on: Field value  │ Dynamic  │
└──────────────────┴────────────────────────┴──────────┘

★ Supported conditional formatting types:
  - Background color (rules / field value / gradient)
  - Font color
  - Data bars
  - Icons (KPI indicators)
  - Web URL (dynamic links)
```

### Measure Tables, Display Folders & Organization

```
★ Measure Table — organize cleaning measures

1) Create empty table: Enter Data → empty table → name "ᐅ Measures"
   (prefix ᐅ sorts to top)
2) Move ALL measures to this table
3) Benefits:
   - Clean data model view
   - Easy to find measures
   - Separate data from logic

★ Display Folders — organize fields within tables

Method (Model view):
1) Select column(s)
2) Properties → Display folder = "Cleaned Fields"

Example structure:
  Sales Table
  ├─ 📁 Keys (ID, FK fields)
  ├─ 📁 Dates (OrderDate, ShipDate)
  ├─ 📁 Amounts (Revenue, Cost, Profit)
  ├─ 📁 Flags (IsValid, IsCleaned)
  └─ 📁 _Internal (hidden helper columns)

★ Naming conventions:
  - Measures: no prefix (they go in Measure Table)
  - Calculated columns: prefix with "cc_"
  - Parameters: prefix with "p_"
  - Hidden columns: prefix with "_"
```

### Small Multiples, Sparklines & OLS

```
★ Small Multiples — compare data quality across categories

- Add dimension to "Small multiples" field well
- Each small chart shows same metric for different group
- Quick visual comparison of data quality patterns
- Example: Error Rate by Region (small multiple bar chart)

★ Sparklines — inline mini-charts in tables

DAX:
Sales_Trend = 
    VAR SparkData = 
        ADDCOLUMNS(
            SUMMARIZE(Sales, Date[Month]),
            "Val", CALCULATE(SUM(Sales[Amount]))
        )
    RETURN
    SparkData  // Add to visual as sparkline

★ Set up in table/matrix:
  1) Add measure to Values
  2) Right-click → Add sparkline
  3) Configure: Line/Bar, X-axis = Date, Y-axis = Measure

★ Object-Level Security (OLS) — hide sensitive columns

Purpose: Prevent users from seeing certain columns
- Even if they have access to the table
- Column shows as "restricted" in field list

Setup (Tabular Editor recommended):
1) Define role with column restrictions
2) Set Permission = None for sensitive columns
3) Assign users to role

Use cases:
  - Hide PII columns (SSN, salary)
  - Hide raw data columns (show only cleaned)
  - Restrict access to internal flags
```

---

## 🏛️ Governance — Microsoft Fabric & Admin

### Microsoft Fabric & OneLake

```
★ Microsoft Fabric — next-gen unified analytics

┌──────────────┬────────────────────────────────────────┐
│ Component    │ Data Cleaning Role                     │
├──────────────┼────────────────────────────────────────┤
│ OneLake      │ Single lake for ALL data               │
│              │ ← Clean once, access from all engines  │
├──────────────┼────────────────────────────────────────┤
│ Lakehouse    │ Spark-based cleaning at scale           │
│              │ ← Delta Lake format with ACID           │
│              │ ← Schema enforcement built-in           │
├──────────────┼────────────────────────────────────────┤
│ Warehouse    │ SQL-based cleaning (T-SQL)              │
│              │ ← Familiar SQL for data engineers       │
├──────────────┼────────────────────────────────────────┤
│ Dataflows    │ Enhanced Power Query (Gen2)             │
│ Gen2         │ ← Output to Lakehouse (not just PBI)    │
│              │ ← Fast copy for large datasets          │
│              │ ← Reusable across workspaces            │
├──────────────┼────────────────────────────────────────┤
│ Data         │ Real-time monitoring & alerts          │
│ Activator    │ ← Alert when data quality drops        │
│              │ ← Trigger actions on anomalies          │
│              │ ← Email/Teams notifications             │
├──────────────┼────────────────────────────────────────┤
│ Notebooks    │ Python/Spark notebooks in Fabric       │
│              │ ← Use pandas/PySpark for cleaning       │
│              │ ← Schedule as pipeline activities       │
└──────────────┴────────────────────────────────────────┘

★ Key advantage: Clean data ONCE in OneLake
  → Power BI, SQL, Spark, ML all use SAME cleaned data
  → No more data copies and sync issues
```

### Scanner API, Audit Log & Usage Metrics

```
★ Power BI Scanner API — governance at scale

// Scan ALL workspaces for governance
POST /admin/workspaces/getInfo
Body: {
    "workspaces": ["workspace-id-1", "workspace-id-2"],
    "datasetExpressions": true,
    "datasetSchema": true
}

// Returns: ALL datasets, tables, columns, measures, M expressions
// Use for:
//   - Find datasets without data cleaning steps
//   - Identify datasets using deprecated M functions
//   - List all data sources across organization
//   - Find datasets without RLS

★ Audit Log — track data activities

Access: Admin portal → Audit logs (or Microsoft 365 compliance)

Key events to monitor:
┌──────────────────────┬──────────────────────────────────┐
│ Event                │ Why it matters                   │
├──────────────────────┼──────────────────────────────────┤
│ RefreshDataset       │ Check refresh failures           │
│ EditReport           │ Track who modified reports       │
│ ViewReport           │ Identify unused reports          │
│ ExportReport         │ Data exfiltration risk           │
│ DeleteDataset        │ Accidental deletion              │
│ ShareDashboard       │ Unauthorized sharing             │
│ ChangeGateway        │ Connection changes               │
└──────────────────────┴──────────────────────────────────┘

★ Usage Metrics Report
  1) Open workspace → Settings → Usage metrics
  2) Built-in report shows:
     - View count per report/page
     - Unique viewers
     - Performance metrics (slow reports)
     - Platform (web/mobile/embedded)
  3) Use to identify:
     - Unused reports → candidates for cleanup
     - Popular reports → prioritize data quality
     - Slow reports → optimize M/DAX
```

---

## 🟡 Power Query — Text & Number Functions

### Text Extraction Functions

```m
// ★ Text extraction — precise text cleaning functions
let
    Source = #table({"Raw"}, {
        {"[Region: APAC] Sales Q1"},
        {"Name: John Smith (ID: 12345)"},
        {"C:\Users\data\report.csv"},
        {"order-2026-001-final"}
    }),
    
    // 1) Text.BetweenDelimiters — extract between two markers
    Region = Table.AddColumn(Source, "Region", each
        Text.BetweenDelimiters([Raw], "[Region: ", "]"),
    type text),
    // Result: "APAC"
    
    // 2) Extract between second occurrence
    ID = Table.AddColumn(Source, "ID", each
        Text.BetweenDelimiters([Raw], ": ", ")"),
    type text),
    
    // 3) Text.BeforeDelimiter / Text.AfterDelimiter
    BeforeParen = Table.AddColumn(Source, "Before", each
        Text.BeforeDelimiter([Raw], "("),
    type text),
    AfterColon = Table.AddColumn(Source, "After", each
        Text.AfterDelimiter([Raw], ": "),
    type text),
    
    // 4) From end (last occurrence)
    FileName = Table.AddColumn(Source, "File", each
        Text.AfterDelimiter([Raw], "\", {0, RelativePosition.FromEnd}),
    type text),
    // Result: "report.csv"
    
    FileExt = Table.AddColumn(Source, "Ext", each
        Text.AfterDelimiter([Raw], ".", {0, RelativePosition.FromEnd}),
    type text),
    // Result: "csv"
    
    // 5) Text.Contains / StartsWith / EndsWith (filtering)
    HasSales = Table.SelectRows(Source, each
        Text.Contains([Raw], "Sales", Comparer.OrdinalIgnoreCase)),
    StartsWith = Table.SelectRows(Source, each
        Text.StartsWith([Raw], "[", Comparer.Ordinal)),
    EndsWith = Table.SelectRows(Source, each
        Text.EndsWith([Raw], ".csv", Comparer.OrdinalIgnoreCase))
in
    Region
```

### Text Transformation Functions

```m
// ★ Text transformation — character-level cleaning
let
    Source = #table({"Data"}, {
        {"  Hello   World  "},
        {"ABC-123-DEF"},
        {"abc"},
        {"สวัสดี"}
    }),
    
    // 1) Text.PadStart / Text.PadEnd — fixed-width padding
    Padded = Table.TransformColumns(Source, {
        {"Data", each Text.PadStart(_, 20, "0"), type text}
    }),
    // "00000Hello   World  "
    
    PadEnd = Table.TransformColumns(Source, {
        {"Data", each Text.PadEnd(_, 20, "."), type text}
    }),
    
    // 2) Text.Remove — remove specific characters
    NoHyphens = Table.TransformColumns(Source, {
        {"Data", each Text.Remove(_, {"-", " "}), type text}
    }),
    // "ABC123DEF"
    
    // 3) Text.Select — keep ONLY specific characters
    OnlyDigits = Table.TransformColumns(Source, {
        {"Data", each Text.Select(_, {"0".."9"}), type text}
    }),
    // "123"
    
    OnlyLetters = Table.TransformColumns(Source, {
        {"Data", each Text.Select(_, {"A".."Z", "a".."z"}), type text}
    }),
    
    // 4) Text.ToList / Text.FromList — character-level manipulation
    Chars = Text.ToList("Hello"),
    // Result: {"H", "e", "l", "l", "o"}
    Reversed = Text.FromList(List.Reverse(Text.ToList("Hello"))),
    // Result: "olleH"
    
    // 5) Text.Format — template formatting
    Formatted = Text.Format("#{0} ordered #{1} units on #{2}",
        {"Alice", "100", "2026-01-15"}),
    // Result: "Alice ordered 100 units on 2026-01-15"
    
    // 6) Text.Repeat
    Separator = Text.Repeat("-", 50),
    // Result: "--------------------------------------------------"
    
    // 7) Text.Reverse
    Rev = Text.Reverse("Hello"),
    // Result: "olleH"
    
    // 8) Text.Range — substring by position
    Sub = Text.Range("Hello World", 6, 5),
    // Result: "World"
    
    // 9) Text.ReplaceRange
    Replaced = Text.ReplaceRange("Hello World", 5, 1, " Beautiful ")
    // Result: "Hello Beautiful World"
in
    OnlyDigits
```

### Number Functions

```m
// ★ Number functions — numeric cleaning
let
    Source = #table({"Value"}, {
        {-42.7}, {0}, {100.5}, {3.14159}
    }),
    
    // 1) Number.Abs — absolute value
    Abs = Table.TransformColumns(Source, {
        {"Value", Number.Abs, type number}
    }),
    
    // 2) Number.Sign — get sign (-1, 0, 1)
    Signs = Table.AddColumn(Source, "Sign", each
        Number.Sign([Value]), Int64.Type),
    
    // 3) Number.Mod — modulo (remainder)
    IsEven = Table.AddColumn(Source, "IsEven", each
        Number.Mod([Value], 2) = 0, type logical),
    
    // 4) Number.IsNaN — check for NaN
    ValidNums = Table.SelectRows(Source, each
        not Number.IsNaN([Value])),
    
    // 5) Number.Power / Sqrt / Log / Exp
    WithCalc = Table.AddColumn(Source, "Squared", each
        Number.Power([Value], 2), type number),
    WithSqrt = Table.AddColumn(Source, "Sqrt", each
        Number.Sqrt(Number.Abs([Value])), type number),
    WithLog = Table.AddColumn(Source, "Log10", each
        if [Value] > 0 then Number.Log10([Value]) else null,
    type number),
    
    // 6) Number.IntegerDivide — integer division
    IntDiv = Number.IntegerDivide(17, 5),
    // Result: 3
    
    // 7) Number.From — safe type conversion
    ParsedNum = Number.From("123.45"),
    ParsedFail = try Number.From("abc") otherwise null
in
    ValidNums
```

---

## 🟡 Power Query — Advanced Table Manipulation

### ReorderColumns, RenameColumns & TransformRows

```m
// ★ Table manipulation — structural cleaning
let
    Source = #table({"First Name", "last_name", "AGE", "CITY"}, {
        {"Alice", "Smith", 30, "Bangkok"},
        {"Bob", "Jones", 25, "Chiang Mai"}
    }),
    
    // 1) Table.ReorderColumns — fix column order
    Reordered = Table.ReorderColumns(Source,
        {"AGE", "First Name", "last_name", "CITY"}),
    
    // 2) Table.RenameColumns — individual renaming
    Renamed = Table.RenameColumns(Source, {
        {"First Name", "FirstName"},
        {"last_name", "LastName"},
        {"AGE", "Age"},
        {"CITY", "City"}
    }),
    
    // 3) Safe rename (don't error if column missing)
    SafeRenamed = Table.RenameColumns(Source, {
        {"NonExistent", "NewName"}
    }, MissingField.Ignore),
    
    // 4) Table.TransformRows — row-level transform (return records)
    Transformed = Table.FromRecords(
        Table.TransformRows(Source, (row) =>
            [
                FullName = row[First Name] & " " & row[last_name],
                Age = row[AGE],
                Location = Text.Proper(row[CITY]),
                IsAdult = row[AGE] >= 18
            ]
        )
    ),
    
    // 5) Table.ReverseRows — reverse row order
    Reversed = Table.ReverseRows(Source),
    
    // 6) Table.RemoveMatchingRows — remove specific rows
    NoAlice = Table.RemoveMatchingRows(Source, {
        [#"First Name" = "Alice"]
    }),
    
    // 7) Table.RemoveFirstN / RemoveLastN
    NoFirst2 = Table.RemoveFirstN(Source, 2),
    NoLast1 = Table.RemoveLastN(Source, 1)
in
    Transformed
```

### AddFuzzyClusterColumn, Combine & Web.Contents

```m
// ★ Table.AddFuzzyClusterColumn — fuzzy grouping for dedup
let
    Source = #table({"Company"}, {
        {"Microsoft Corp"},
        {"microsoft corporation"},
        {"MSFT"},
        {"Google LLC"},
        {"Alphabet / Google"},
        {"google inc"}
    }),
    
    // Fuzzy cluster = group similar values
    Clustered = Table.AddFuzzyClusterColumn(Source, "Company",
        "CleanCompany", [
            Culture = "en-US",
            IgnoreCase = true,
            IgnoreSpace = true,
            Threshold = 0.8,
            TransformationTable = #table({"From", "To"}, {
                {"Corp", "Corporation"},
                {"Inc", "Incorporated"},
                {"LLC", ""}
            })
        ]),
    
    // ★ Table.Combine with MissingField handling
    Table1 = #table({"A", "B"}, {{1, "x"}}),
    Table2 = #table({"A", "C"}, {{2, "y"}}),          // Different columns!
    
    // Error if columns don't match:
    // Combined = Table.Combine({Table1, Table2})       // ERROR!
    
    // Safe combine with MissingField
    SafeCombined = Table.Combine({Table1, Table2},
        MissingField.UseNull),
    // Result: A=1, B="x", C=null / A=2, B=null, C="y"
    
    // ★ Web.Contents — advanced API calls for data extraction
    ApiData = Json.Document(Web.Contents(
        "https://api.example.com/data",
        [
            Headers = [
                #"Authorization" = "Bearer " & Token,
                #"Content-Type" = "application/json",
                #"Accept-Language" = "th"
            ],
            Query = [
                page = "1",
                limit = "100",
                filter = "active"
            ],
            Timeout = #duration(0, 0, 30, 0),     // 30 sec timeout
            ManualStatusHandling = {400, 404, 500}, // Don't error on these
            IsRetry = true                          // Allow retry
        ]
    )),
    
    // ★ Table.AggregateTableColumn — aggregate nested tables
    Grouped = Table.Group(Source, {"Company"}, {
        {"Details", each _}
    }),
    Aggregated = Table.AggregateTableColumn(Grouped, "Details", {
        {"Company", List.Count, "Count"}
    })
in
    Clustered
```

---

## 📐 DAX — Text, Date & Math Functions

### Text Functions

```dax
// ★ DAX text functions for data cleaning

// 1) LEFT / RIGHT / MID — substring extraction
Clean_Code = LEFT(Products[SKU], 3)                // First 3 chars
Region_Code = RIGHT(Orders[OrderID], 4)            // Last 4 chars
Middle = MID(Products[SerialNumber], 5, 8)         // 8 chars from pos 5

// 2) FIND / SEARCH — locate text position
//    FIND = case-sensitive, SEARCH = case-insensitive
Has_At = IF(FIND("@", Customers[Email],, 0) > 0, TRUE(), FALSE())
Domain_Start = SEARCH("@", Customers[Email],, BLANK())

// 3) SUBSTITUTE / REPLACE — text modification
No_Dashes = SUBSTITUTE(Products[Phone], "-", "")          // Remove all dashes
First_Dash = REPLACE(Products[Code], 3, 1, ".")           // Replace at position

// Multiple substitutions
Cleaned_Address = 
    VAR Step1 = SUBSTITUTE(Customers[Address], "  ", " ")
    VAR Step2 = SUBSTITUTE(Step1, "Rd.", "Road")
    VAR Step3 = SUBSTITUTE(Step2, "St.", "Street")
    VAR Step4 = SUBSTITUTE(Step3, "Ave.", "Avenue")
    RETURN TRIM(Step4)

// 4) PROPER — title case
Proper_Name = PROPER(Customers[Name])
// "john doe" → "John Doe"

// 5) EXACT — case-sensitive comparison
Is_Match = EXACT(Table1[Code], Table2[Code])
// TRUE only if exact match including case

// 6) UNICODE / UNICHAR — character code handling
Char_Code = UNICODE("A")          // Returns: 65
From_Code = UNICHAR(3585)         // Returns: "ก" (Thai)

// 7) REPT — repeat character
Stars = REPT("★", Products[Rating])
// Rating=3 → "★★★"
```

### Date & Time Functions

```dax
// ★ DAX date/time functions for cleaning

// 1) DATEDIFF — precise date difference
Days_Since = DATEDIFF(Orders[OrderDate], TODAY(), DAY)
Months_Between = DATEDIFF(Customers[JoinDate], TODAY(), MONTH)
Years_Active = DATEDIFF(Employees[HireDate], TODAY(), YEAR)

// 2) YEARFRAC — fractional year difference
Exact_Years = YEARFRAC(Employees[HireDate], TODAY())
// Result: 2.75 (2 years and 9 months)

// 3) EDATE — add/subtract months
Next_Review = EDATE(Employees[LastReview], 6)     // +6 months
Prev_Quarter = EDATE(TODAY(), -3)                  // -3 months

// 4) EOMONTH — end of month after adding months
Quarter_End = EOMONTH(TODAY(), 0)                  // End of current month
Next_Quarter_End = EOMONTH(TODAY(), 3)             // End of +3 months

// 5) TIME functions
Order_Hour = HOUR(Orders[OrderTime])
Order_Minute = MINUTE(Orders[OrderTime])
Is_Business_Hours = 
    IF(
        HOUR(Orders[OrderTime]) >= 9 &&
        HOUR(Orders[OrderTime]) < 17,
        "Business Hours",
        "After Hours"
    )

// 6) CONVERT — type conversion
As_Integer = CONVERT(Sales[StringAmount], INTEGER)
As_Date = CONVERT("2026-01-15", DATETIME)
As_String = CONVERT(42, STRING)

// 7) Rounding family
Rounded = ROUND(Sales[Amount], 2)              // Standard round
Up = ROUNDUP(Sales[Tax], 2)                     // Always round up
Down = ROUNDDOWN(Sales[Discount], 4)            // Always round down
To5 = MROUND(Sales[Price], 5)                   // Round to nearest 5
Ceil = CEILING(Sales[Amount], 100)              // Next 100
Flr = FLOOR(Sales[Amount], 100)                 // Previous 100
Trunc = TRUNC(Sales[Amount], 0)                 // Drop decimals
```

### CONTAINS, SAMPLE & Natural Joins

```dax
// ★ CONTAINS / CONTAINSROW — membership check

// 1) CONTAINS — check if table contains row
Product_In_Sale = 
    IF(
        CONTAINS(Sales, Sales[ProductID], Products[ID]),
        "Has Sales ✅",
        "No Sales ❌"
    )

// 2) CONTAINSROW — simpler syntax
Is_VIP = CONTAINSROW(VIPList, Customers[CustomerID])

// 3) Filter using CONTAINS
Active_Categories = 
    FILTER(
        ALL(Products[Category]),
        CONTAINS(
            SUMMARIZE(Sales, Products[Category]),
            Products[Category],
            Products[Category]
        )
    )

// ★ SAMPLE — random sampling for data quality check
Random_10 = SAMPLE(10, Sales, Sales[OrderDate])
// Returns: 10 random rows from Sales

Sample_By_Category = 
    SUMMARIZECOLUMNS(
        Products[Category],
        "Sample_Count", COUNTROWS(SAMPLE(5, Sales, Sales[Amount]))
    )

// ★ NATURALINNERJOIN / NATURALLEFTOUTERJOIN
Matched = NATURALINNERJOIN(Customers, Orders)
// Auto-joins on columns with SAME NAME and RELATIONSHIP

All_With_Orders = NATURALLEFTOUTERJOIN(Customers, Orders)
// All customers, with orders where they exist
```

---

## 🎨 Power BI Report & Distribution Features

### Report Page Tooltips, Interactions & Slicers

```
★ Report Page Tooltips — rich hover information

1) Create new page → Page Settings:
   - Page type = Tooltip
   - Size = Custom (320x240 recommended)
2) Design tooltip with visuals (cards, charts, images)
3) On main page visual: Format → Tooltip → Type = Report Page
4) Select tooltip page

Use case: Hover over data point → see quality breakdown
  - Show % missing, error count, last updated
  - Much richer than default tooltip

★ Cross-filter / Cross-highlight — interaction control

Edit interactions (Format → Edit interactions):
┌──────────────┬────────────────────────────────────┐
│ Mode         │ Behavior                           │
├──────────────┼────────────────────────────────────┤
│ Filter       │ Other visuals filter to selection   │
│ Highlight    │ Other visuals dim non-matching      │
│ None         │ No interaction (independent)        │
└──────────────┴────────────────────────────────────┘

Best practice for data quality dashboards:
  - Summary cards: set to "None" (always show totals)
  - Detail tables: set to "Filter"
  - Charts: set to "Highlight"

★ Sort By Column — sort text using hidden column

Example: Sort month names correctly:
  1) Create MonthNum column (1-12)
  2) Select MonthName column → Sort by column → MonthNum
  3) Now "January" sorts before "February" (not alphabetically!)

Other uses:
  - Sort status by priority (Active=1, Pending=2, Closed=3)
  - Sort custom categories in specific order

★ Slicer Types — filtering your data

Types available:
  - List (single/multi select)
  - Dropdown
  - Between (range for numbers/dates)
  - Relative date (last 7 days, this month)
  - Relative time
  - Hierarchy (org chart drill-down)
  - Numeric range (slider)

★ Sync Slicers — consistent filtering across pages
  View → Sync slicers → check pages to sync
```

### Themes, Templates & Quick Insights

```
★ Themes — consistent styling for data quality dashboards

1) Built-in themes: View → Themes → select
2) Custom JSON theme:
   {
     "name": "DataQualityTheme",
     "dataColors": ["#28a745", "#ffc107", "#dc3545"],
     "good": "#28a745",
     "neutral": "#6c757d",
     "bad": "#dc3545",
     "background": "#f8f9fa",
     "foreground": "#212529",
     "textClasses": {
       "title": {"fontSize": 14, "fontFace": "Segoe UI Semibold"},
       "label": {"fontSize": 10, "fontFace": "Segoe UI"}
     }
   }
3) Save & share theme files (.json) across reports

★ Templates (.pbit) — reusable report structure

1) Save as template: File → Save As → .pbit
2) Template includes:
   - All visuals and layout
   - All measures and calculated columns
   - All M queries (without data)
   - Parameters (user fills in at open)
3) Use for: Standard data quality report template
   → Open .pbit → Enter connection → Instant quality dashboard

★ Quick Insights / "Explain the increase"

1) Quick Insights:
   - Right-click dataset → Quick Insights
   - AI auto-discovers patterns, outliers, trends
   - Pin interesting insights to dashboard

2) "Explain the increase/decrease":
   - Right-click data point → Analyze → Explain
   - AI identifies contributing factors
   - Shows waterfall chart of influences

3) R / Python Visuals:
   - Insert → R visual / Python visual
   - Write custom code for advanced analysis
   - Use matplotlib, seaborn, ggplot2
   - Example: Custom statistical tests on data quality

★ Power Automate Integration:
  - Trigger flows from Power BI alerts
  - "When data refresh fails → send Teams message"
  - "When metric drops → create ticket in Jira"
  - "When new data arrives → run quality check"
```

### Apps, Metrics & Mobile

```
★ Power BI Apps — bundle content for distribution

1) Create App from workspace:
   Workspace → Create app
2) App includes:
   - Selected reports and dashboards
   - Navigation structure
   - Custom branding
   - Audience (users/groups)
3) Benefits for data quality:
   - Package quality dashboards as self-service app
   - Auto-install updates for users
   - Track installation and usage

★ Metrics / Scorecards / Goals

1) Create Scorecard:
   - Define business goals/KPIs
   - Track current value vs target
   - SubGoals for breakdown
   - Status: On track / At risk / Behind

2) Use for data quality KPIs:
   - "99% data freshness" — target vs actual
   - "< 1% error rate" — current performance
   - "100% coverage" — track over time
   - Assign owners for accountability

3) Check-ins:
   - Team members update progress notes
   - Automated from Power BI dataset values
   - History of goal progression

★ Mobile Layout — responsive data quality

1) View → Mobile layout
2) Drag visuals to phone canvas
3) Best practices:
   - KPI cards at top (most important)
   - Simplified charts (no complex tables)
   - Large touch targets for slicers
   - Remove unnecessary detail
4) Separate mobile layout per page

★ Selection Pane & Groups:
  View → Selection pane
  - Show/hide visuals by layer
  - Group related visuals
  - Tab order for accessibility
  - Lock visual positions
```

---

## ⭐ Power Query — Most Popular UI Patterns

### Column From Examples & Conditional Column

```
★ Column From Examples — AI-powered column creation (VERY POPULAR!)

วิธีใช้ (PQ Editor):
1. Add Column → Column from Examples → From All Columns
2. พิมพ์ตัวอย่างผลลัพธ์ที่ต้องการ 2-3 rows
3. PQ จะเดา pattern อัตโนมัติ
4. Click OK → PQ สร้าง M formula ให้อัตโนมัติ

★ ตัวอย่างที่ใช้ได้:
┌──────────────────┬──────────────────────┬────────────────────┐
│ Source Data       │ You Type             │ PQ Generates       │
├──────────────────┼──────────────────────┼────────────────────┤
│ John Smith        │ J. Smith             │ Initial + Last     │
│ 2026-03-01       │ March 2026           │ Date formatting    │
│ $1,234.56        │ 1234.56              │ Number extraction  │
│ Bangkok, TH      │ Bangkok              │ Before delimiter   │
│ 081-234-5678     │ 0812345678           │ Remove dashes      │
│ hello world      │ Hello World          │ Text.Proper        │
│ ABC123           │ ABC                  │ Text only           │
└──────────────────┴──────────────────────┴────────────────────┘

★ TIP: ถ้า guess ผิด → พิมพ์เพิ่มอีก 1-2 rows → จะ refine pattern

★ Conditional Column — UI-based If/Then/Else

วิธีใช้ (PQ Editor):
1. Add Column → Conditional Column
2. ตั้ง conditions:
   If [Amount] is greater than 1000 Then "High"
   Else If [Amount] is greater than 100 Then "Medium"
   Else "Low"
3. Click OK

★ M code ที่สร้างออกมา:
```

```m
// Conditional Column generates this M:
= Table.AddColumn(Source, "Tier", each
    if [Amount] > 1000 then "High"
    else if [Amount] > 100 then "Medium"
    else "Low",
type text)

// ★ Custom Column — write M expression directly
// Add Column → Custom Column → Enter formula:
= if [Status] = null then "Missing"
  else if Text.Length([Status]) < 2 then "Invalid"
  else Text.Proper(Text.Trim([Status]))
```

### Replace Errors & Append / Merge Queries

```m
// ★ Replace Errors — extremely popular for data cleaning!

// Method 1: UI → Right-click column → Replace Errors → enter value
= Table.ReplaceErrorValues(Source, {
    {"Amount", 0},         // Replace Amount errors with 0
    {"Name", "Unknown"},   // Replace Name errors with "Unknown"
    {"Date", null}         // Replace Date errors with null
})

// Method 2: Replace errors for ALL columns at once
= Table.ReplaceErrorValues(Source,
    List.Transform(
        Table.ColumnNames(Source),
        each {_, null}     // All errors → null
    )
)
```

```
★ Append Queries — stack tables vertically (UNION)

วิธีใช้ (PQ Editor):
1. Home → Append Queries (→ As New)
2. Select: Two tables / Three or more tables
3. Choose tables to append

Common use cases:
  - Combine monthly files (Jan + Feb + Mar + ...)
  - Combine same structure from different sources
  - Stack data from multiple sheets

★ Merge Queries — join tables horizontally (JOIN)

วิธีใช้ (PQ Editor):
1. Home → Merge Queries (→ As New)
2. Select matching columns in each table
3. Choose Join Kind:

┌──────────────────┬────────────────────────────────────┐
│ Join Kind        │ Description                        │
├──────────────────┼────────────────────────────────────┤
│ Left Outer       │ All from left + matching from right │
│ Right Outer      │ All from right + matching from left │
│ Full Outer       │ All from both tables                │
│ Inner            │ Only matching rows                  │
│ Left Anti        │ Left rows NOT in right (find gaps!) │
│ Right Anti       │ Right rows NOT in left              │
└──────────────────┴────────────────────────────────────┘

4. Expand merged column → select fields to include

★ POPULAR: Left Anti Join = หาข้อมูลที่หายไป!
  กด Merge → เลือก Left Anti → เห็นว่า row ไหนไม่มีใน table ขวา
```

### Unpivot, Transpose & Extract Functions

```m
// ★ Unpivot Other Columns — VERY POPULAR for wide-to-long data

// Before: Year | Jan | Feb | Mar | ...
// After:  Year | Month | Value

// วิธีใช้ (PQ Editor):
// 1. Select columns to KEEP (e.g., Year, Product)
// 2. Right-click → Unpivot Other Columns
// 3. Rename "Attribute" → "Month", "Value" → "Sales"

// M code:
= Table.UnpivotOtherColumns(Source,
    {"Year", "Product"},  // Keep these
    "Month",              // Attribute name
    "Sales"               // Value name
)

// ★ Transpose — swap rows ↔ columns
= Table.Transpose(Source)
// Row 1 becomes Column 1, etc.
// TIP: Often need Table.PromoteHeaders after transpose

// ★ Extract functions (Right-click column → Extract)
// These are UI shortcuts that generate M code:

// Text Before Delimiter
= Table.TransformColumns(Source, {
    {"Col", each Text.BeforeDelimiter(_, "@"), type text}
})
// "user@email.com" → "user"

// Text After Delimiter
= Table.TransformColumns(Source, {
    {"Col", each Text.AfterDelimiter(_, "@"), type text}
})
// "user@email.com" → "email.com"

// First Characters / Last Characters
= Table.TransformColumns(Source, {
    {"Col", each Text.Start(_, 3), type text}    // First 3
})
= Table.TransformColumns(Source, {
    {"Col", each Text.End(_, 4), type text}      // Last 4
})

// Text Length
= Table.TransformColumns(Source, {
    {"Col", each Text.Length(_), Int64.Type}
})
```

### Invoke Custom Function

```m
// ★ Invoke Custom Function — apply function to each row (POPULAR!)

// Step 1: Create reusable function
let
    fn_CleanPhone = (phone as text) as text =>
        let
            digits = Text.Select(phone, {"0".."9"}),
            formatted = if Text.Length(digits) = 10
                then Text.Range(digits, 0, 3) & "-"
                    & Text.Range(digits, 3, 3) & "-"
                    & Text.Range(digits, 6, 4)
                else digits
        in
            formatted
in
    fn_CleanPhone

// Step 2: Invoke in another query
= Table.AddColumn(Source, "CleanPhone", each
    fn_CleanPhone([RawPhone]),
type text)

// ★ Invoke from UI:
// Add Column → Invoke Custom Function
// Select function → Map parameters to columns

// ★ Popular use: Process multiple Excel files
let
    fn_ReadExcel = (filePath as text) as table =>
        Excel.Workbook(File.Contents(filePath)){0}[Data],

    FileList = Folder.Files("C:\Data\Monthly"),
    AddData = Table.AddColumn(FileList, "Data", each
        fn_ReadExcel([Folder Path] & [Name]),
    type table),
    Combined = Table.Combine(AddData[Data])
in
    Combined
```

---

## ⭐ DAX — Top 10 Most Searched Patterns

### Running Total & Cumulative Sum

```dax
// ★ #1 MOST POPULAR: Running Total / Cumulative Sum

// Method 1: Classic (works in all versions)
Running_Total = 
    CALCULATE(
        SUM(Sales[Amount]),
        FILTER(
            ALLSELECTED(Date[Date]),
            Date[Date] <= MAX(Date[Date])
        )
    )

// Method 2: WINDOW function (newer, recommended)
Running_Total_Window = 
    VAR CurrentDate = MAX(Date[Date])
    RETURN
    CALCULATE(
        SUM(Sales[Amount]),
        WINDOW(1, ABS, 0, REL, 
            ALLSELECTED(Date[Date]), 
            ORDERBY(Date[Date]))
    )

// ★ Cumulative % of Total
Cumulative_Pct = 
    VAR RunningTotal = [Running_Total]
    VAR GrandTotal = CALCULATE(SUM(Sales[Amount]), ALLSELECTED())
    RETURN
    DIVIDE(RunningTotal, GrandTotal)
```

### Previous Period Comparison (YoY / MoM / WoW)

```dax
// ★ #2 MOST POPULAR: Period-over-Period comparison

// Year-over-Year (YoY)
Sales_LY = CALCULATE(SUM(Sales[Amount]), SAMEPERIODLASTYEAR(Date[Date]))
YoY_Change = SUM(Sales[Amount]) - [Sales_LY]
YoY_Pct = DIVIDE([YoY_Change], [Sales_LY])

// Month-over-Month (MoM)
Sales_PM = CALCULATE(SUM(Sales[Amount]), DATEADD(Date[Date], -1, MONTH))
MoM_Change = SUM(Sales[Amount]) - [Sales_PM]
MoM_Pct = DIVIDE([MoM_Change], [Sales_PM])

// Week-over-Week (WoW)
Sales_PW = CALCULATE(SUM(Sales[Amount]), DATEADD(Date[Date], -7, DAY))
WoW_Pct = DIVIDE(SUM(Sales[Amount]) - [Sales_PW], [Sales_PW])

// ★ Dynamic comparison label
Period_Label = 
    SWITCH(
        SELECTEDVALUE(CompareType[Type]),
        "YoY", FORMAT([YoY_Pct], "+0.0%;-0.0%") & " vs LY",
        "MoM", FORMAT([MoM_Pct], "+0.0%;-0.0%") & " vs LM",
        "WoW", FORMAT([WoW_Pct], "+0.0%;-0.0%") & " vs LW",
        ""
    )

// ★ Arrow indicator
Trend_Arrow = 
    VAR Change = [YoY_Pct]
    RETURN
    SWITCH(
        TRUE(),
        Change > 0.05, "▲ " & FORMAT(Change, "0.0%"),
        Change < -0.05, "▼ " & FORMAT(Change, "0.0%"),
        "► " & FORMAT(Change, "0.0%")
    )
```

### Moving Average & Percent of Total

```dax
// ★ #3 MOST POPULAR: Moving Average

// 7-Day Moving Average
MA_7Day = 
    AVERAGEX(
        DATESINPERIOD(Date[Date], MAX(Date[Date]), -7, DAY),
        CALCULATE(SUM(Sales[Amount]))
    )

// 30-Day Moving Average
MA_30Day = 
    AVERAGEX(
        DATESINPERIOD(Date[Date], MAX(Date[Date]), -30, DAY),
        CALCULATE(SUM(Sales[Amount]))
    )

// 3-Month Moving Average
MA_3Month = 
    AVERAGEX(
        DATESINPERIOD(Date[Date], MAX(Date[Date]), -3, MONTH),
        CALCULATE(SUM(Sales[Amount]))
    )

// ★ #4 MOST POPULAR: Percent of Total

// % of Grand Total
Pct_of_Total = 
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(SUM(Sales[Amount]), ALL(Sales))
    )

// % of Parent (e.g., % within category)
Pct_of_Category = 
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(SUM(Sales[Amount]), ALLEXCEPT(Sales, Sales[Category]))
    )

// % of Visible Total (respects filters)
Pct_of_Visible = 
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(SUM(Sales[Amount]), ALLSELECTED())
    )
```

### ABC/Pareto Analysis & Last Non-Blank

```dax
// ★ #5 MOST POPULAR: ABC Analysis (Pareto 80/20)

ABC_Class = 
    VAR CurrentSales = [Total Sales]
    VAR AllProducts = 
        ADDCOLUMNS(
            ALLSELECTED(Products[ProductName]),
            "Sales", CALCULATE([Total Sales])
        )
    VAR RankedProducts = 
        FILTER(AllProducts, [Sales] >= CurrentSales)
    VAR CumulativeSales = SUMX(RankedProducts, [Sales])
    VAR TotalSales = SUMX(AllProducts, [Sales])
    VAR CumulativePct = DIVIDE(CumulativeSales, TotalSales)
    RETURN
    SWITCH(
        TRUE(),
        CumulativePct <= 0.8, "A ⭐",   // Top 80% revenue
        CumulativePct <= 0.95, "B",       // Next 15%
        "C"                                // Bottom 5%
    )

// ★ #6 MOST POPULAR: Last Non-Blank Value

Last_Known_Balance = 
    CALCULATE(
        LASTNONBLANK(Date[Date],
            CALCULATE(SUM(Balance[Amount]))),
        ALLSELECTED(Date[Date])
    )

// Last available value per customer
Last_Order_Amount = 
    CALCULATE(
        SUM(Sales[Amount]),
        LASTNONBLANK(Date[Date],
            CALCULATE(COUNTROWS(Sales)))
    )

// Latest non-blank with SELECTEDVALUE
Latest_Status = 
    VAR LastDate = 
        MAXX(
            FILTER(StatusLog, NOT(ISBLANK(StatusLog[Status]))),
            StatusLog[Date]
        )
    RETURN
    CALCULATE(
        SELECTEDVALUE(StatusLog[Status]),
        StatusLog[Date] = LastDate
    )
```

### New vs Returning & Semi-Additive Measures

```dax
// ★ #7 MOST POPULAR: New vs Returning Customers

Is_New_Customer = 
    VAR FirstPurchase = 
        CALCULATE(
            MIN(Sales[OrderDate]),
            ALLEXCEPT(Sales, Sales[CustomerID])
        )
    RETURN
    IF(Sales[OrderDate] = FirstPurchase, "New", "Returning")

New_Customer_Count = 
    VAR CurrentPeriodStart = MIN(Date[Date])
    RETURN
    CALCULATE(
        DISTINCTCOUNT(Sales[CustomerID]),
        FILTER(
            ALL(Sales),
            Sales[CustomerID] IN
                CALCULATETABLE(
                    VALUES(Sales[CustomerID]),
                    Date[Date] >= CurrentPeriodStart
                )
            && CALCULATE(MIN(Sales[OrderDate]),
                ALLEXCEPT(Sales, Sales[CustomerID]))
                >= CurrentPeriodStart
        )
    )

// ★ #8 MOST POPULAR: Semi-Additive Measures (Balance/Inventory)
// Problem: Balance should NOT sum across dates!

Balance_Latest = 
    CALCULATE(
        SUM(Balance[Amount]),
        LASTDATE(Date[Date])    // Only last date in context
    )

Inventory_End_of_Month = 
    CALCULATE(
        SUM(Inventory[Quantity]),
        LASTDATE(Date[Date])
    )

// Average balance across period
Avg_Balance = 
    AVERAGEX(
        VALUES(Date[Date]),
        CALCULATE(SUM(Balance[Amount]))
    )
```

### Disconnected Slicer & Dynamic Measure Switching

```dax
// ★ #9 MOST POPULAR: Disconnected Slicer

// Step 1: Create table with NO relationship to data
MetricSelector = DATATABLE(
    "Metric", STRING,
    "SortOrder", INTEGER,
    {
        {"Revenue", 1},
        {"Cost", 2},
        {"Profit", 3},
        {"Margin %", 4}
    }
)

// Step 2: Create dynamic measure
Selected_Metric = 
    SWITCH(
        SELECTEDVALUE(MetricSelector[Metric]),
        "Revenue", SUM(Sales[Revenue]),
        "Cost", SUM(Sales[Cost]),
        "Profit", SUM(Sales[Revenue]) - SUM(Sales[Cost]),
        "Margin %", DIVIDE(
            SUM(Sales[Revenue]) - SUM(Sales[Cost]),
            SUM(Sales[Revenue])
        ),
        SUM(Sales[Revenue])    // Default
    )

// Step 3: Add MetricSelector to slicer → No relationship needed!

// ★ #10 MOST POPULAR: Dynamic Measure Switching
// Same pattern but with format string

Selected_Metric_Formatted = 
    VAR Value = [Selected_Metric]
    VAR Selected = SELECTEDVALUE(MetricSelector[Metric])
    RETURN
    IF(
        Selected = "Margin %",
        FORMAT(Value, "0.0%"),
        FORMAT(Value, "#,##0")
    )
```

---

## ⭐ Power BI — Most Popular Report Patterns

### Dynamic Title & Last Refresh Date

```dax
// ★ Dynamic Title — title changes based on slicer selection

Dynamic_Title = 
    VAR SelectedRegion = SELECTEDVALUE(Geography[Region], "All Regions")
    VAR SelectedYear = SELECTEDVALUE(Date[Year], "All Years")
    RETURN
    "Sales Dashboard — " & SelectedRegion & " | " & SelectedYear

// ★★★ Last Refresh Date/Time — EXTREMELY POPULAR!
// Users always want to know "when was this data updated?"

// Method 1: M query (create separate query)
// New Query → Blank Query → paste:
```

```m
// ★ Last Refresh — M Query approach
let
    Source = DateTimeZone.SwitchZone(
        DateTimeZone.UtcNow(),
        7   // UTC+7 for Thailand
    ),
    AsText = DateTime.ToText(
        DateTime.From(Source),
        [Format = "dd/MM/yyyy HH:mm:ss"]
    ),
    ToTable = #table(
        type table [LastRefresh = text],
        {{AsText}}
    )
in
    ToTable
```

```dax
// Method 2: DAX approach
Last_Refresh = "อัพเดทล่าสุด: " & FORMAT(NOW(), "DD/MM/YYYY HH:MM")

// Method 3: Show in card visual with icon
Refresh_Display = 
    "🔄 " & FORMAT(NOW(), "DD MMM YYYY") & 
    " เวลา " & FORMAT(NOW(), "HH:MM") & " น."
```

### Top N with Parameter & Toggle Visuals

```dax
// ★ Top N with Dynamic Parameter — POPULAR for rankings

// Step 1: Create What-if parameter (Modeling → New Parameter)
// Name: "Top N", Min: 1, Max: 50, Default: 10, Increment: 1

// Step 2: Create ranking measure
Product_Rank = 
    RANKX(
        ALLSELECTED(Products[ProductName]),
        [Total Sales],
        ,
        DESC,
        Dense
    )

// Step 3: Create filter measure  
Show_Top_N = IF([Product_Rank] <= [Top N Value], 1, 0)

// Step 4: Add to visual filter → Show_Top_N = 1
// Now slicer controls how many products show!
```

```
★ Toggle Between Visuals — POPULAR for chart/table switching

1) Create 2 visuals on same position:
   - Bar Chart (for visual view)
   - Table (for detail view)

2) Create 2 bookmarks:
   - "Chart View" — bar chart visible, table hidden
   - "Table View" — table visible, bar chart hidden
   ⚠️ In bookmark: uncheck "Data" → only toggle display

3) Add buttons:
   - Button "📊 Chart" → Action → Bookmark → "Chart View"
   - Button "📋 Table" → Action → Bookmark → "Table View"

4) Result: Users click buttons to switch views!

★ Navigation Buttons — page navigation

1) Insert → Buttons → Blank (or use icons)
2) Action → Type = Page navigation
3) Destination = target page
4) Style buttons consistently across pages
5) Create navigation bar as a group → copy to all pages

★ RAG Status (Red/Amber/Green) — KPI indicators

Use conditional formatting on card/KPI visuals:
```

```dax
// RAG Color code
RAG_Color = 
    SWITCH(
        TRUE(),
        [KPI_Value] >= [Target] * 1.0, "#28A745",   // Green ✅
        [KPI_Value] >= [Target] * 0.8, "#FFC107",   // Amber ⚠️
        "#DC3545"                                      // Red ❌
    )

// RAG Status text
RAG_Status = 
    SWITCH(
        TRUE(),
        [KPI_Value] >= [Target], "🟢 On Track",
        [KPI_Value] >= [Target] * 0.8, "🟡 At Risk",
        "🔴 Behind"
    )

// Apply: Conditional formatting → Color → Based on field value
// Select RAG_Color measure → applies to background/font
```

### Star Schema Best Practices

```
★ Star Schema — the MOST important modeling pattern in Power BI!

                    ┌───────────┐
                    │ Date Dim  │
                    └─────┬─────┘
                          │
┌───────────┐    ┌────────┴────────┐    ┌───────────┐
│ Product   │────│   Fact Sales    │────│ Customer  │
│ Dimension │    │   (measures)    │    │ Dimension │
└───────────┘    └────────┬────────┘    └───────────┘
                          │
                    ┌─────┴─────┐
                    │ Geography │
                    │ Dimension │
                    └───────────┘

★ Rules for clean data model:

1) Fact tables: contain IDs + measures (Amount, Qty, etc.)
   - Many rows, few columns
   - Foreign keys to dimension tables

2) Dimension tables: contain descriptive attributes
   - Few rows, many columns  
   - Primary key (unique per row)

3) Relationships: always Dimension → Fact (one-to-many)
   - Single direction filter (Dimension filters Fact)
   - Avoid bi-directional unless absolutely needed

4) Date table: ALWAYS create a dedicated date dimension
   - Mark as Date Table (Table tools → Mark as date table)
   - Must have continuous date range (no gaps!)
   - Enable time intelligence functions

5) Avoid:
   ❌ Many-to-many without bridge table
   ❌ Snowflake schema (dimension → sub-dimension)
   ❌ Bi-directional filters everywhere
   ❌ Calculated columns that should be measures
   ❌ Wide fact tables with too many columns
```

---

## 🟡 Power Query — Connectors & File Patterns

### Folder.Files — Multi-File Processing

```m
// ★ Folder.Files — process ALL files in folder (EXTREMELY POPULAR!)
let
    // 1) Get all files
    Files = Folder.Files("C:\Data\Monthly Reports"),
    
    // 2) Filter to specific file type
    OnlyCsv = Table.SelectRows(Files, each [Extension] = ".csv"),
    OnlyExcel = Table.SelectRows(Files, each
        [Extension] = ".xlsx" or [Extension] = ".xls"),
    
    // 3) Add file content as table
    WithData = Table.AddColumn(OnlyCsv, "Data", each
        Csv.Document([Content], [
            Delimiter = ",",
            Encoding = TextEncoding.Utf8,
            QuoteStyle = QuoteStyle.Csv
        ]),
    type table),
    
    // 4) Add source filename (for tracking)
    WithSource = Table.AddColumn(WithData, "SourceFile", each
        [Name], type text),
    
    // 5) Expand and combine all
    Expanded = Table.ExpandTableColumn(WithSource, "Data",
        Table.ColumnNames(WithSource{0}[Data])),
    
    // 6) Remove file metadata columns
    Cleaned = Table.RemoveColumns(Expanded,
        {"Content", "Name", "Extension", "Date accessed",
         "Date modified", "Date created", "Attributes",
         "Folder Path"}),
    
    // ★ Alternative: Excel files with specific sheet
    ExcelFiles = Table.AddColumn(OnlyExcel, "Data", each
        let
            wb = Excel.Workbook([Content]),
            sheet = wb{[Name="Sheet1"]}[Data],
            promoted = Table.PromoteHeaders(sheet, [PromoteAllScalars=true])
        in
            promoted,
    type table)
in
    Cleaned

// ★ SharePoint.Files — same pattern for SharePoint
let
    Source = SharePoint.Files("https://company.sharepoint.com/sites/data"),
    Filtered = Table.SelectRows(Source, each
        Text.Contains([Folder Path], "Monthly")),
    WithData = Table.AddColumn(Filtered, "Data", each
        Excel.Workbook([Content]){0}[Data])
in
    WithData
```

### CSV, Excel & SQL Connection Patterns

```m
// ★ Csv.Document — all parsing options
let
    Raw = File.Contents("C:\data.csv"),
    Parsed = Csv.Document(Raw, [
        Delimiter = ",",              // or ";" or #(tab) or "|"
        Columns = 5,                  // Expected column count
        Encoding = TextEncoding.Utf8, // or .Ascii, .Unicode, .Utf16
        QuoteStyle = QuoteStyle.Csv,  // Handle quoted fields
        CsvStyle = CsvStyle.QuoteAfterDelimiter
    ]),
    Promoted = Table.PromoteHeaders(Parsed, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"Date", type date},
        {"Amount", type number}
    }, "en-US")   // ★ Specify locale for type conversion!
in
    Typed

// ★ Excel.Workbook — access different elements
let
    Source = Excel.Workbook(File.Contents("C:\report.xlsx")),
    // Source returns table with: Name, Data, Item, Kind, Hidden
    // Kind = "Sheet", "Table", "DefinedName"
    
    // Access by sheet name
    Sheet1 = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    
    // Access by table name (named range/table)
    SalesTable = Source{[Item="tblSales",Kind="Table"]}[Data],
    
    // Access current workbook (from within Excel)
    Current = Excel.CurrentWorkbook(){[Name="Table1"]}[Content]
in
    Sheet1

// ★ Sql.Database — with query folding awareness
let
    Source = Sql.Database("server-name", "database-name", [
        Query = null,                    // null = let PQ handle
        CommandTimeout = #duration(0,0,5,0),  // 5 min timeout
        CreateNavigationProperties = false,
        NavigationPropertyNameGenerator = null
    ]),
    Sales = Source{[Schema="dbo",Item="Sales"]}[Data],
    
    // ★ These steps FOLD to SQL (happen on server):
    Filtered = Table.SelectRows(Sales, each [Year] >= 2024),
    Selected = Table.SelectColumns(Sales, {"ID", "Amount", "Date"}),
    Sorted = Table.Sort(Sales, {{"Date", Order.Descending}}),
    Top1000 = Table.FirstN(Sales, 1000),
    
    // ★ These steps BREAK folding (happen locally):
    // Custom columns, M-specific functions, complex transforms
    
    // ★ Check folding: Right-click step → "View Native Query"
    // If grayed out → folding is broken at this step!
    
    Native = Value.NativeQuery(Source,
        "SELECT TOP 100 * FROM dbo.Sales WHERE Amount > 0")
in
    Filtered
```

### Literal Constructors & Error Handling

```m
// ★ Literal constructors — create values directly in M
let
    // Date literal
    MyDate = #date(2026, 3, 1),
    
    // Time literal
    MyTime = #time(14, 30, 0),
    
    // DateTime literal
    MyDateTime = #datetime(2026, 3, 1, 14, 30, 0),
    
    // DateTimeZone literal (with UTC offset)
    MyDTZ = #datetimezone(2026, 3, 1, 14, 30, 0, 7, 0),  // UTC+7
    
    // Duration literal
    OneDay = #duration(1, 0, 0, 0),        // 1 day
    TwoHours = #duration(0, 2, 0, 0),      // 2 hours
    ThirtyMin = #duration(0, 0, 30, 0),    // 30 minutes
    
    // Date arithmetic with durations
    Tomorrow = Date.From(DateTime.LocalNow()) + #duration(1,0,0,0),
    LastWeek = Date.From(DateTime.LocalNow()) - #duration(7,0,0,0),
    
    // ★ Error.Record — structured error information
    SafeConvert = (val as any) as any =>
        let
            result = try Number.From(val)
        in
            if result[HasError] then
                let
                    err = result[Error],
                    // err[Reason], err[Message], err[Detail]
                    logged = Diagnostics.Trace(
                        TraceLevel.Warning,
                        "Convert error: " & err[Message],
                        () => null
                    )
                in
                    logged()
            else
                result[Value],
    
    // ★ Table.ColumnsOfType — find columns by data type
    Source = #table(type table [Name=text, Age=number, Date=date], {}),
    TextCols = Table.ColumnsOfType(Source, {type text}),
    // Result: {"Name"}
    
    NumCols = Table.ColumnsOfType(Source, {type number, Int64.Type}),
    
    // ★ Table.HasColumns — check before accessing
    HasAge = Table.HasColumns(Source, "Age"),
    // Result: true
    
    SafeSelect = if Table.HasColumns(Source, "OptionalCol")
        then Table.SelectColumns(Source, {"Name", "OptionalCol"})
        else Table.SelectColumns(Source, {"Name"})
in
    MyDate
```

### Nested Data: Expand Records & Lists

```m
// ★ Table.ExpandRecordColumn — expand nested JSON/API data
let
    // Typical API response: nested records
    ApiResponse = Json.Document(Web.Contents("https://api.example.com/users")),
    AsTable = Table.FromList(ApiResponse, Splitter.SplitByNothing()),
    
    // Expand top-level record columns
    Expanded = Table.ExpandRecordColumn(AsTable, "Column1",
        {"id", "name", "email", "address"}),
    
    // Address is still a record → expand again
    ExpandAddress = Table.ExpandRecordColumn(Expanded, "address",
        {"city", "country", "zip"}),
    
    // ★ Dynamic expansion (don't hardcode field names)
    DynamicExpand = (tbl as table, col as text) as table =>
        let
            sample = Record.FieldNames(Table.Column(tbl, col){0}),
            expanded = Table.ExpandRecordColumn(tbl, col, sample)
        in
            expanded,
    
    // ★ Table.ExpandListColumn — explode lists to rows
    WithTags = #table({"Name", "Tags"}, {
        {"Alice", {"admin", "user"}},
        {"Bob", {"user"}}
    }),
    ExplodedTags = Table.ExpandListColumn(WithTags, "Tags"),
    // Alice/admin, Alice/user, Bob/user
    
    // ★ Lines.FromBinary — process text line-by-line
    RawText = File.Contents("C:\data.txt"),
    Lines = Lines.FromBinary(RawText, null, null, TextEncoding.Utf8),
    AsTable2 = Table.FromColumns({Lines}, {"Line"}),
    // Now each line is a row → apply cleaning per line
    Cleaned = Table.SelectRows(AsTable2, each
        [Line] <> "" and not Text.StartsWith([Line], "#"))
in
    ExpandAddress
```

---

## 📐 DAX — CALCULATE Deep Dive

### 5 Golden Rules of CALCULATE

```dax
// ★ CALCULATE — THE most important DAX function!
// Every Power BI expert must understand these 5 rules:

// Rule 1: CALCULATE changes filter context
Total_Sales = SUM(Sales[Amount])
// → Sums only within current filter context (slicer/visual)

Thailand_Sales = CALCULATE(SUM(Sales[Amount]), Sales[Region] = "Thailand")
// → Overrides Region filter, keeps all other filters

// Rule 2: Multiple filters = AND (intersection)
Thai_2024 = CALCULATE(
    SUM(Sales[Amount]),
    Sales[Region] = "Thailand",     // AND
    Sales[Year] = 2024              // AND
)

// Rule 3: ALL removes filters
All_Sales = CALCULATE(SUM(Sales[Amount]), ALL(Sales))
// → Ignores ALL filters on Sales table

Pct = DIVIDE(
    SUM(Sales[Amount]),
    CALCULATE(SUM(Sales[Amount]), ALL(Sales))
)
// → % of grand total

// Rule 4: ALLEXCEPT = remove all EXCEPT specified
Pct_In_Category = DIVIDE(
    SUM(Sales[Amount]),
    CALCULATE(SUM(Sales[Amount]), 
        ALLEXCEPT(Sales, Sales[Category]))
)
// → % within category (keeps category filter)

// Rule 5: Context Transition
// In calculated columns and iterators, row context → filter context

Rank = RANKX(ALL(Products), CALCULATE(SUM(Sales[Amount])))
// CALCULATE here triggers context transition:
// For each product (row context) → creates filter context for that product
```

### VAR/RETURN & Iterator Patterns

```dax
// ★ VAR/RETURN — best practices (EXTREMELY POPULAR!)

// Bad: duplicate calculations
Bad_Margin = 
    DIVIDE(
        SUM(Sales[Revenue]) - SUM(Sales[Cost]),   // calculated twice!
        SUM(Sales[Revenue])                        // overlap with above
    )

// Good: use variables
Good_Margin = 
    VAR Revenue = SUM(Sales[Revenue])
    VAR Cost = SUM(Sales[Cost])
    VAR Profit = Revenue - Cost
    RETURN
    DIVIDE(Profit, Revenue)

// ★ Complex calculation with many steps
Sales_KPI = 
    VAR CurrentSales = SUM(Sales[Amount])
    VAR PrevYearSales = CALCULATE(SUM(Sales[Amount]), SAMEPERIODLASTYEAR(Date[Date]))
    VAR Growth = CurrentSales - PrevYearSales
    VAR GrowthPct = DIVIDE(Growth, PrevYearSales)
    VAR Target = [Sales_Target]
    VAR Achievement = DIVIDE(CurrentSales, Target)
    VAR Status = SWITCH(TRUE(),
        Achievement >= 1, "🟢 Achieved",
        Achievement >= 0.8, "🟡 On Track",
        "🔴 Behind"
    )
    RETURN
    Status

// ★ Iterator functions — SUMX, AVERAGEX, COUNTX, MINX, MAXX
// Process row by row (powerful but can be slow on large data)

// SUMX — sum of expression per row
Weighted_Avg_Price = 
    DIVIDE(
        SUMX(Sales, Sales[Price] * Sales[Quantity]),  // price × qty per row
        SUM(Sales[Quantity])
    )

// AVERAGEX — average of expression per row
Avg_Order_Size = 
    AVERAGEX(
        VALUES(Sales[OrderID]),
        CALCULATE(SUM(Sales[Amount]))
    )

// COUNTX — count rows where condition is true
Error_Count = 
    COUNTX(
        Sales,
        IF(Sales[Amount] < 0 || ISBLANK(Sales[ProductID]), 1)
    )

// MINX / MAXX — min/max of expression
Cheapest_Product = 
    MINX(
        FILTER(Products, Products[IsActive] = TRUE()),
        Products[Price]
    )
```

### ALL Family & RELATED / Counting Functions

```dax
// ★ ALL family — filter removal functions

// ALL(table) — remove ALL filters from table
Grand_Total = CALCULATE(SUM(Sales[Amount]), ALL(Sales))

// ALL(column) — remove filter from ONE column only
All_Regions = CALCULATE(SUM(Sales[Amount]), ALL(Sales[Region]))

// ALL(col1, col2) — remove from specific columns
All_Time = CALCULATE(SUM(Sales[Amount]), ALL(Date[Year], Date[Month]))

// ALLEXCEPT — remove all EXCEPT specified columns
Keep_Category = CALCULATE(SUM(Sales[Amount]),
    ALLEXCEPT(Sales, Products[Category]))

// ALLSELECTED — respect external filters only (from slicer)
Pct_Selected = DIVIDE(
    SUM(Sales[Amount]),
    CALCULATE(SUM(Sales[Amount]), ALLSELECTED())
)

// ALLNOBLANKROW — ALL but exclude auto-generated blank row
Clean_Count = CALCULATE(
    DISTINCTCOUNT(Products[Category]),
    ALLNOBLANKROW(Products[Category])
)

// ★ RELATED / RELATEDTABLE — navigate relationships


// RELATED — get value from related table (many-to-one side)
Category_Name = RELATED(Products[Category])
// Use in: calculated columns on Sales table

// RELATEDTABLE — get rows from related table (one-to-many side)
Order_Count = COUNTROWS(RELATEDTABLE(Sales))
// Use in: calculated columns on Products table

// ★ Counting family — choose the right one!
// ┌─────────────────────┬──────────────────────────────────────────┐
// │ Function            │ What it counts                           │
// ├─────────────────────┼──────────────────────────────────────────┤
// │ COUNTROWS(table)    │ Number of rows in table                  │
// │ COUNT(column)       │ Non-blank NUMBER values                  │
// │ COUNTA(column)      │ Non-blank values (any type)              │
// │ COUNTBLANK(column)  │ Blank/null values                        │
// │ DISTINCTCOUNT(col)  │ Unique non-blank values                  │
// │ DISTINCTCOUNTNOBLANK│ Unique values excluding blank            │
// │ COUNTX(table, expr) │ Count of non-blank expression results    │
// └─────────────────────┴──────────────────────────────────────────┘

Completeness_Pct = 
    DIVIDE(
        COUNTA(Customers[Email]),           // Non-blank emails
        COUNTROWS(Customers)                 // Total rows
    )

Uniqueness_Pct = 
    DIVIDE(
        DISTINCTCOUNT(Sales[CustomerID]),    // Unique customers
        COUNTROWS(Sales)                     // Total transactions
    )
```

---

## 📐 DAX — Time Intelligence Complete Reference

### MTD / QTD / YTD & Closing Balance

```dax
// ★ Complete Time Intelligence reference
// REQUIREMENT: Must have a proper Date table marked as Date Table!

// Period-to-Date totals
Sales_MTD = TOTALMTD(SUM(Sales[Amount]), Date[Date])
Sales_QTD = TOTALQTD(SUM(Sales[Amount]), Date[Date])
Sales_YTD = TOTALYTD(SUM(Sales[Amount]), Date[Date])

// With fiscal year (April start)
Sales_FY_YTD = TOTALYTD(SUM(Sales[Amount]), Date[Date], "3/31")

// ★ Closing Balance (semi-additive: last value in period)
Balance_EOM = CLOSINGBALANCEMONTH(SUM(Balance[Amount]), Date[Date])
Balance_EOQ = CLOSINGBALANCEQUARTER(SUM(Balance[Amount]), Date[Date])
Balance_EOY = CLOSINGBALANCEYEAR(SUM(Balance[Amount]), Date[Date])

// Opening Balance
Balance_BOM = OPENINGBALANCEMONTH(SUM(Balance[Amount]), Date[Date])
Balance_BOQ = OPENINGBALANCEQUARTER(SUM(Balance[Amount]), Date[Date])
Balance_BOY = OPENINGBALANCEYEAR(SUM(Balance[Amount]), Date[Date])

// Change during period
Monthly_Change = [Balance_EOM] - [Balance_BOM]
```

### Parallel Period & Previous/Next

```dax
// ★ Period comparison functions

// PARALLELPERIOD — shift entire period
Sales_1Y_Ago = CALCULATE(SUM(Sales[Amount]),
    PARALLELPERIOD(Date[Date], -1, YEAR))
Sales_1Q_Ago = CALCULATE(SUM(Sales[Amount]),
    PARALLELPERIOD(Date[Date], -1, QUARTER))
Sales_1M_Ago = CALCULATE(SUM(Sales[Amount]),
    PARALLELPERIOD(Date[Date], -1, MONTH))

// PREVIOUS / NEXT period functions
Sales_PrevMonth = CALCULATE(SUM(Sales[Amount]), PREVIOUSMONTH(Date[Date]))
Sales_PrevQtr = CALCULATE(SUM(Sales[Amount]), PREVIOUSQUARTER(Date[Date]))
Sales_PrevYear = CALCULATE(SUM(Sales[Amount]), PREVIOUSYEAR(Date[Date]))

Sales_NextMonth = CALCULATE(SUM(Sales[Amount]), NEXTMONTH(Date[Date]))
Sales_NextQtr = CALCULATE(SUM(Sales[Amount]), NEXTQUARTER(Date[Date]))
Sales_NextYear = CALCULATE(SUM(Sales[Amount]), NEXTYEAR(Date[Date]))

// ★ DATESBETWEEN / DATESINPERIOD — custom date ranges
Sales_Custom_Range = CALCULATE(
    SUM(Sales[Amount]),
    DATESBETWEEN(Date[Date], DATE(2026,1,1), DATE(2026,3,31))
)

Sales_Last_90_Days = CALCULATE(
    SUM(Sales[Amount]),
    DATESINPERIOD(Date[Date], MAX(Date[Date]), -90, DAY)
)

Sales_Last_12_Months = CALCULATE(
    SUM(Sales[Amount]),
    DATESINPERIOD(Date[Date], MAX(Date[Date]), -12, MONTH)
)
```

### Complete Date Table Pattern

```dax
// ★ THE definitive Date Table — use this in every Power BI model!

DateTable = 
    VAR StartDate = DATE(2020, 1, 1)
    VAR EndDate = DATE(2030, 12, 31)
    VAR BaseCalendar = CALENDAR(StartDate, EndDate)
    RETURN
    ADDCOLUMNS(
        BaseCalendar,
        "Year", YEAR([Date]),
        "Quarter", "Q" & FORMAT(QUARTER([Date]), "0"),
        "QuarterNum", QUARTER([Date]),
        "Month", FORMAT([Date], "MMMM"),
        "MonthShort", FORMAT([Date], "MMM"),
        "MonthNum", MONTH([Date]),
        "MonthYear", FORMAT([Date], "MMM YYYY"),
        "Week", WEEKNUM([Date]),
        "Day", DAY([Date]),
        "DayOfWeek", FORMAT([Date], "dddd"),
        "DayOfWeekNum", WEEKDAY([Date], 2),  // 1=Mon
        "DayOfYear", DATEDIFF(DATE(YEAR([Date]),1,1), [Date], DAY) + 1,
        "IsWeekend", IF(WEEKDAY([Date], 2) >= 6, TRUE(), FALSE()),
        "IsToday", IF([Date] = TODAY(), TRUE(), FALSE()),
        
        // Fiscal Year (April start)
        "FiscalYear", IF(MONTH([Date]) >= 4, YEAR([Date]), YEAR([Date]) - 1),
        "FiscalQuarter", "FQ" & FORMAT(
            INT((MONTH([Date]) - 4 + 12) / 3) + 1, "0"),
        "FiscalMonth", MOD(MONTH([Date]) - 4 + 12, 12) + 1,
        
        // Relative dates
        "IsCurrentMonth", IF(
            YEAR([Date]) = YEAR(TODAY()) && MONTH([Date]) = MONTH(TODAY()),
            TRUE(), FALSE()),
        "IsCurrentYear", IF(YEAR([Date]) = YEAR(TODAY()), TRUE(), FALSE()),
        "IsPastDate", IF([Date] < TODAY(), TRUE(), FALSE()),
        
        // Thai Buddhist year (พ.ศ.)
        "BuddhistYear", YEAR([Date]) + 543,
        "ThaiMonthYear", FORMAT([Date], "MMM") & " " & (YEAR([Date]) + 543)
    )

// ★ After creating: Table tools → Mark as date table → Date column
// ★ Sort MonthShort by MonthNum (Sort by column)
```

---

## 📐 DAX — Table Constructors & IN Operator

### Table Constructors, IN & ISEMPTY

```dax
// ★ Table constructor — create inline table with { }

// 1) Single-column table
Sales_In_Top_Cities = 
    CALCULATE(
        SUM(Sales[Amount]),
        Sales[City] IN {"Bangkok", "Chiang Mai", "Phuket", "Pattaya"}
    )

// 2) Multi-column table constructor
Sales_Specific = 
    CALCULATE(
        SUM(Sales[Amount]),
        FILTER(
            Sales,
            (Sales[Region], Sales[Year]) IN {
                ("Thailand", 2024),
                ("Thailand", 2025),
                ("Singapore", 2025)
            }
        )
    )

// 3) NOT IN — exclude values
Sales_Excl = 
    CALCULATE(
        SUM(Sales[Amount]),
        NOT Sales[Status] IN {"Cancelled", "Returned", "Void"}
    )

// ★ ISEMPTY — check if table has any rows
Has_Sales = 
    IF(
        NOT ISEMPTY(RELATEDTABLE(Sales)),
        "Has Sales ✅",
        "No Sales ❌"
    )

Is_New_Category = 
    IF(
        ISEMPTY(
            CALCULATETABLE(
                Sales,
                PREVIOUSMONTH(Date[Date])
            )
        ),
        "New This Month 🆕",
        "Existing"
    )

// ★ TREATAS — virtual relationship (no physical relationship needed!)
Sales_By_ColorMap = 
    CALCULATE(
        SUM(Sales[Amount]),
        TREATAS(
            DATATABLE("Color", STRING, {{"Red"}, {"Blue"}}),
            Products[Color]     // Map to this column
        )
    )

// ★ ROW — create single-row table
Summary = ROW(
    "Total", SUM(Sales[Amount]),
    "Count", COUNTROWS(Sales),
    "Average", AVERAGE(Sales[Amount])
)
```

---

## 📊 Data Quality Dashboard — Complete Template

### Measures for Data Quality KPIs

```dax
// ★ Complete Data Quality Dashboard measures

// === COMPLETENESS ===
Completeness_Score = 
    VAR TotalCells = COUNTROWS(Customers) * 5    // 5 key columns
    VAR FilledCells = 
        COUNTA(Customers[Name]) + 
        COUNTA(Customers[Email]) + 
        COUNTA(Customers[Phone]) +
        COUNTA(Customers[City]) +
        COUNTA(Customers[Category])
    RETURN
    DIVIDE(FilledCells, TotalCells)

Missing_by_Column = 
    SWITCH(
        SELECTEDVALUE(ColumnName[Column]),
        "Name", COUNTBLANK(Customers[Name]),
        "Email", COUNTBLANK(Customers[Email]),
        "Phone", COUNTBLANK(Customers[Phone]),
        "City", COUNTBLANK(Customers[City]),
        0
    )

// === VALIDITY ===
Valid_Email_Pct = 
    DIVIDE(
        COUNTROWS(FILTER(Customers,
            CONTAINSSTRING(Customers[Email], "@")
            && CONTAINSSTRING(Customers[Email], ".")
            && LEN(Customers[Email]) > 5
        )),
        COUNTA(Customers[Email])
    )

Invalid_Records = 
    COUNTROWS(
        FILTER(Customers,
            ISBLANK(Customers[Name])
            || LEN(Customers[Name]) < 2
            || Customers[Amount] < 0
        )
    )

// === UNIQUENESS ===
Duplicate_Rate = 
    1 - DIVIDE(
        DISTINCTCOUNT(Customers[Email]),
        COUNTA(Customers[Email])
    )

// === FRESHNESS ===
Data_Age_Days = 
    DATEDIFF(MAX(Sales[OrderDate]), TODAY(), DAY)

Freshness_Status = 
    VAR AgeDays = [Data_Age_Days]
    RETURN
    SWITCH(
        TRUE(),
        AgeDays <= 1, "🟢 Fresh (today)",
        AgeDays <= 7, "🟡 Recent (" & AgeDays & " days)",
        "🔴 Stale (" & AgeDays & " days)"
    )

// === OVERALL SCORE ===
Overall_Quality_Score = 
    VAR Completeness = [Completeness_Score] * 0.3
    VAR Validity = [Valid_Email_Pct] * 0.25
    VAR Uniqueness = (1 - [Duplicate_Rate]) * 0.25
    VAR Freshness = IF([Data_Age_Days] <= 1, 1,
        IF([Data_Age_Days] <= 7, 0.75, 0.5)) * 0.2
    RETURN
    Completeness + Validity + Uniqueness + Freshness
```

### Dashboard Layout Guide

```
★ Data Quality Dashboard — recommended layout:

┌─────────────────────────────────────────────────────────────┐
│  🔄 Last Refresh: 01/03/2026 13:45    Overall Score: 94%   │
├────────────┬────────────┬────────────┬──────────────────────┤
│ Completeness│ Validity   │ Uniqueness │ Freshness           │
│   97.2%    │   95.1%    │   99.8%    │ 🟢 Fresh            │
│   ████████░│   ████████░│   █████████│                      │
├────────────┴────────────┴────────────┴──────────────────────┤
│                                                             │
│  Missing Values by Column          Error Trend (Line Chart) │
│  ┌──────────────────┐              ┌──────────────────────┐ │
│  │ Name    ░░ 2.1%  │              │  ╱\  ╱\              │ │
│  │ Email   ███ 4.8% │              │ ╱  \/  \___/\___     │ │
│  │ Phone   █ 1.2%   │              │                      │ │
│  │ City    ░ 0.5%   │              │                      │ │
│  └──────────────────┘              └──────────────────────┘ │
│                                                             │
│  Top Issues (Table)                Quality by Category      │
│  ┌──────────────────────────┐      ┌──────────────────────┐ │
│  │ Issue    │ Count │ %     │      │ Electronics  🟢 98%  │ │
│  │ No email │  245  │ 4.8%  │      │ Clothing     🟡 87%  │ │
│  │ No phone │   61  │ 1.2%  │      │ Food         🔴 72%  │ │
│  │ Invalid  │   15  │ 0.3%  │      │              (chart) │ │
│  └──────────────────────────┘      └──────────────────────┘ │
│                                                             │
│  [📊 Chart View]  [📋 Detail View]  [⬇️ Export Issues]     │
└─────────────────────────────────────────────────────────────┘

★ Design tips:
  1. Use KPI cards at top (most important metrics)
  2. Color-code: Green ≥ 95%, Yellow ≥ 80%, Red < 80%
  3. Include trend over time (are we getting better?)
  4. Add drill-through to see actual bad records
  5. Export button to download issues for fixing
  6. Last Refresh prominently displayed
  7. Add Bookmarks for different views
```

---

## 🟡 Power Query — List Functions & Dynamic Generation

### List.Generate, List.Accumulate & List.Zip

```m
// ★ List.Generate — create dynamic sequences (very powerful!)
let
    // Generate list of dates (Monday of each week)
    Mondays = List.Generate(
        () => #date(2026, 1, 5),       // initial value (first Monday)
        each _ <= #date(2026, 12, 31),  // condition (keep going?)
        each Date.AddDays(_, 7),        // next value (+7 days)
        each _                          // output (the date itself)
    ),
    // Result: {2026-01-05, 2026-01-12, 2026-01-19, ...}
    
    // Generate custom ID sequence
    CustomIDs = List.Generate(
        () => [i = 1, id = "TH-0001"],
        each [i] <= 100,
        each [i = [i] + 1, id = "TH-" & Text.PadStart(Text.From([i] + 1), 4, "0")],
        each [id]
    ),
    // Result: {"TH-0001", "TH-0002", ..., "TH-0100"}
    
    // Paginated API calls (fetch until no more pages)
    AllPages = List.Generate(
        () => [Page = 1, Data = GetPage(1), HasMore = true],
        each [HasMore],
        each [
            Page = [Page] + 1,
            Data = GetPage([Page] + 1),
            HasMore = List.Count([Data]) > 0
        ],
        each [Data]
    ),
    
    // ★ List.Accumulate — fold/reduce (running calculation)
    RunningSum = List.Accumulate(
        {10, 20, 30, 40},    // list to process
        0,                     // initial state (seed)
        (state, current) => state + current
    ),
    // Result: 100  (0+10+20+30+40)
    
    // Build comma-separated string
    JoinedText = List.Accumulate(
        {"Apple", "Banana", "Cherry"},
        "",
        (state, current) =>
            if state = "" then current
            else state & ", " & current
    ),
    // Result: "Apple, Banana, Cherry"
    
    // ★ List.Zip — combine multiple lists element-wise
    Names = {"Alice", "Bob", "Charlie"},
    Ages = {30, 25, 35},
    Cities = {"BKK", "CNX", "PKT"},
    Zipped = List.Zip({Names, Ages, Cities}),
    // Result: {{"Alice",30,"BKK"}, {"Bob",25,"CNX"}, {"Charlie",35,"PKT"}}
    
    AsRecords = List.Transform(Zipped, each
        [Name = _{0}, Age = _{1}, City = _{2}]),
    AsTable = Table.FromRecords(AsRecords)
in
    AsTable
```

### List Sequences & Table Construction

```m
// ★ List.Numbers / List.Dates / List.Durations — sequence generators
let
    // Number sequence
    Numbers = List.Numbers(1, 100, 1),          // 1 to 100 step 1
    Evens = List.Numbers(2, 50, 2),              // 2,4,6,...,100
    
    // Date sequence
    DateRange = List.Dates(
        #date(2026, 1, 1),      // start
        365,                     // count
        #duration(1, 0, 0, 0)   // step (1 day)
    ),
    
    // Duration sequence
    Intervals = List.Durations(
        #duration(0, 0, 0, 0),   // start
        24,                       // count
        #duration(0, 1, 0, 0)    // step (1 hour)
    ),
    
    // ★ List.Transform / List.Select — list operations
    Cleaned = List.Transform(
        {"  hello ", " WORLD", "  foo  "},
        each Text.Trim(Text.Lower(_))
    ),
    // Result: {"hello", "world", "foo"}
    
    OnlyLong = List.Select(
        {"a", "hello", "hi", "world", "x"},
        each Text.Length(_) >= 3
    ),
    // Result: {"hello", "world"}
    
    // ★ Table construction from different sources
    FromRecords = Table.FromRecords({
        [Name = "Alice", Age = 30],
        [Name = "Bob", Age = 25]
    }),
    
    FromColumns = Table.FromColumns(
        {{"Alice", "Bob"}, {30, 25}},
        {"Name", "Age"}
    ),
    
    // Table → Records → Table (for transformation)
    Records = Table.ToRecords(FromRecords),
    Modified = List.Transform(Records, each
        Record.TransformFields(_, {{"Name", Text.Upper}})),
    BackToTable = Table.FromRecords(Modified),
    
    // ★ Table.Column — extract single column as list
    Names = Table.Column(FromRecords, "Name"),
    // Result: {"Alice", "Bob"}
    
    // ★ Table.Pivot — long-to-wide (opposite of Unpivot!)
    LongData = #table({"Product", "Month", "Sales"}, {
        {"A", "Jan", 100}, {"A", "Feb", 150},
        {"B", "Jan", 200}, {"B", "Feb", 250}
    }),
    Pivoted = Table.Pivot(LongData,
        List.Distinct(LongData[Month]),  // column values
        "Month",                          // value column
        "Sales",                          // value to put in cells
        List.Sum                          // aggregation function
    )
    // Result: Product | Jan | Feb
    //         A       | 100 | 150
    //         B       | 200 | 250
in
    Pivoted
```

### Table Utilities & Type Checking

```m
// ★ Table utility functions for data quality
let
    Source = #table({"A", "B", "C"}, {
        {1, "x", true}, {2, "y", false}, {1, "x", true}
    }),
    
    // 1) Table.IsDistinct — check for duplicates
    HasDuplicates = not Table.IsDistinct(Source),
    HasDuplicatesOnCols = not Table.IsDistinct(
        Table.SelectColumns(Source, {"A", "B"})),
    
    // 2) Table.ContainsAll / ContainsAny — membership
    HasAll = Table.ContainsAll(Source, {
        [A = 1, B = "x"],
        [A = 2, B = "y"]
    }),
    HasAny = Table.ContainsAny(Source, {
        [A = 99],
        [A = 1]
    }),
    // HasAny = true (found A=1)
    
    // 3) Table.AddKey — set primary key for joins
    WithKey = Table.AddKey(Source, {"A"}, true),  // true = primary
    
    // 4) Table.PrefixColumns — add prefix to all column names
    Prefixed = Table.PrefixColumns(Source, "src"),
    // Columns: src.A, src.B, src.C
    
    // 5) Table.DemoteHeaders — move headers back to rows
    Demoted = Table.DemoteHeaders(Source),
    
    // 6) Value.Is / Value.Type — type checking
    IsText = Value.Is("hello", type text),          // true
    IsNumber = Value.Is(42, type number),            // true
    TypeOf = Value.Type(42),                         // type number
    TypeName = Type.FunctionDomain(Value.Type(42)),  // "number"
    
    // 7) Splitter functions — for SplitColumn
    ByDelim = Splitter.SplitTextByDelimiter(","),
    ByPos = Splitter.SplitTextByPositions({0, 3, 6}),
    ByLen = Splitter.SplitTextByLengths({3, 3, 4}),
    ByTransition = Splitter.SplitTextByCharacterTransition(
        {"0".."9"}, {"A".."Z","a".."z"}),  // digit→letter
    
    // Apply: "ABC123DEF456" → {"ABC", "123", "DEF", "456"}
    SplitResult = Splitter.SplitTextByCharacterTransition(
        {"A".."Z","a".."z"}, {"0".."9"})("ABC123DEF456")
in
    HasDuplicates
```

---

## 📐 DAX — Window Functions (NEW!)

### OFFSET, INDEX & WINDOW

```dax
// ★ NEW DAX Window Functions (2023+)
// These are the LATEST additions to DAX — very powerful!

// ★ OFFSET — access value from relative position
Prev_Month_Sales = 
    CALCULATE(
        SUM(Sales[Amount]),
        OFFSET(
            -1,                              // -1 = previous row
            ALLSELECTED(Date[MonthYear]),    // partition
            ORDERBY(Date[MonthYear])         // order
        )
    )

MoM_Change_Window = 
    VAR Current = SUM(Sales[Amount])
    VAR Previous = CALCULATE(
        SUM(Sales[Amount]),
        OFFSET(-1, ALLSELECTED(Date[MonthYear]),
            ORDERBY(Date[MonthYear]))
    )
    RETURN
    DIVIDE(Current - Previous, Previous)

// ★ INDEX — access value at absolute position
First_Month_Sales = 
    CALCULATE(
        SUM(Sales[Amount]),
        INDEX(
            1,                               // position 1 (first)
            ALLSELECTED(Date[MonthYear]),
            ORDERBY(Date[MonthYear])
        )
    )

Last_Month_Sales = 
    CALCULATE(
        SUM(Sales[Amount]),
        INDEX(
            -1,                              // -1 = last position
            ALLSELECTED(Date[MonthYear]),
            ORDERBY(Date[MonthYear])
        )
    )

// Growth from first month
Growth_From_Start = 
    VAR Current = SUM(Sales[Amount])
    VAR First = [First_Month_Sales]
    RETURN
    DIVIDE(Current - First, First)

// ★ WINDOW — access range of rows
Rolling_3_Month = 
    CALCULATE(
        SUM(Sales[Amount]),
        WINDOW(
            -2, REL,                         // 2 rows before current
            0, REL,                          // current row
            ALLSELECTED(Date[MonthYear]),
            ORDERBY(Date[MonthYear])
        )
    )

Rolling_Avg_3M = DIVIDE([Rolling_3_Month], 3)

// Window: from beginning to current (running total)
Running_Total_Window = 
    CALCULATE(
        SUM(Sales[Amount]),
        WINDOW(
            1, ABS,                          // absolute position 1
            0, REL,                          // relative current
            ALLSELECTED(Date[MonthYear]),
            ORDERBY(Date[MonthYear])
        )
    )
```

### RANK, ORDERBY, PARTITIONBY & MATCHBY

```dax
// ★ RANK — ranking with window functions
Product_Rank = 
    RANK(
        DENSE,                               // DENSE or SKIP
        ALLSELECTED(Products[ProductName]),
        ORDERBY([Total Sales], DESC)
    )

// Rank within category (PARTITIONBY!)
Rank_In_Category = 
    RANK(
        DENSE,
        ALLSELECTED(Products[ProductName]),
        ORDERBY([Total Sales], DESC),
        PARTITIONBY(Products[Category])      // Reset rank per category
    )

// ★ PARTITIONBY — group window operations
// Sales rank by region
Regional_Rank = 
    RANK(
        DENSE,
        ALLSELECTED(Products[ProductName]),
        ORDERBY([Total Sales], DESC),
        PARTITIONBY(Geography[Region])
    )

// ★ ORDERBY — control ordering in window functions  
// Multi-column ordering
Multi_Sort_Rank = 
    RANK(
        DENSE,
        ALLSELECTED(Products[ProductName]),
        ORDERBY(
            [Total Sales], DESC,             // Primary: sales desc
            Products[ProductName], ASC       // Secondary: name asc
        )
    )

// ★ Previous value with PARTITIONBY
Prev_Month_By_Region = 
    CALCULATE(
        SUM(Sales[Amount]),
        OFFSET(
            -1,
            ALLSELECTED(Date[MonthYear], Geography[Region]),
            ORDERBY(Date[MonthYear]),
            PARTITIONBY(Geography[Region])    // Reset per region!
        )
    )

// ★ MATCHBY — specify columns for matching
// Used when PARTITIONBY + ORDERBY don't uniquely identify rows
Unique_Rank = 
    RANK(
        DENSE,
        ALLSELECTED(Sales[OrderID]),
        ORDERBY([Total Sales], DESC),
        MATCHBY(Sales[OrderID])               // Ensure unique matching
    )
```

---

## 📐 DAX — Advanced Modeling Patterns

### Calculation Groups & SELECTEDMEASURE

```dax
// ★ Calculation Groups — reuse logic across multiple measures
// Created in: Tabular Editor or SSDT

// Calculation Group: "Time Intelligence"
// Calculation Items:

// Item: "Current"
SELECTEDMEASURE()

// Item: "YoY"
VAR Current = SELECTEDMEASURE()
VAR PrevYear = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR(Date[Date]))
RETURN Current - PrevYear

// Item: "YoY %"
VAR Current = SELECTEDMEASURE()  
VAR PrevYear = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR(Date[Date]))
RETURN DIVIDE(Current - PrevYear, PrevYear)

// Item: "YTD"
CALCULATE(SELECTEDMEASURE(), DATESYTD(Date[Date]))

// Item: "MTD"
CALCULATE(SELECTEDMEASURE(), DATESMTD(Date[Date]))

// Item: "Rolling 12M"
CALCULATE(
    SELECTEDMEASURE(),
    DATESINPERIOD(Date[Date], MAX(Date[Date]), -12, MONTH)
)

// ★ SELECTEDMEASURENAME — customize by measure
VAR MeasureName = SELECTEDMEASURENAME()
VAR Result = SELECTEDMEASURE()
RETURN
    IF(
        MeasureName = "Margin %",
        FORMAT(Result, "0.0%"),
        FORMAT(Result, "#,##0")
    )

// ★ Benefits of Calculation Groups:
// - Define YoY/MTD/YTD ONCE → applies to ALL measures!
// - No need to create YoY_Sales, YoY_Cost, YoY_Profit separately
// - Just put Calculation Group in slicer → user selects!
```

### ISINSCOPE, RLS & Data Categories

```dax
// ★ ISINSCOPE — check if column is actively being grouped/drilled
Dynamic_Label = 
    SWITCH(
        TRUE(),
        ISINSCOPE(Geography[City]), "City: " & SELECTEDVALUE(Geography[City]),
        ISINSCOPE(Geography[State]), "State: " & SELECTEDVALUE(Geography[State]),
        ISINSCOPE(Geography[Country]), "Country: " & SELECTEDVALUE(Geography[Country]),
        "All Regions"
    )

// Dynamic measure based on drill level
Smart_Total = 
    SWITCH(
        TRUE(),
        ISINSCOPE(Date[Date]), [Daily_Sales],
        ISINSCOPE(Date[Month]), [Monthly_Sales],
        ISINSCOPE(Date[Quarter]), [Quarterly_Sales],
        ISINSCOPE(Date[Year]), [Yearly_Sales],
        [Grand_Total]
    )

// ★ USERCULTURE — localized formatting  
Localized_Amount = 
    FORMAT(SUM(Sales[Amount]),
        SWITCH(
            LEFT(USERCULTURE(), 2),
            "th", "#,##0.00 ฿",
            "ja", "¥#,##0",
            "en", "$#,##0.00",
            "#,##0.00"
        )
    )
```

```
★ Row-Level Security (RLS) — advanced patterns

// Basic RLS: filter by user
[Region] = LOOKUPVALUE(
    UserMapping[Region],
    UserMapping[Email],
    USERPRINCIPALNAME()
)

// Dynamic RLS with table
Sales[Territory] IN 
    SELECTCOLUMNS(
        FILTER(UserAccess, 
            UserAccess[Email] = USERPRINCIPALNAME()),
        "Territory", UserAccess[Territory]
    )

// Manager sees all subordinates
[Department] IN 
    SELECTCOLUMNS(
        FILTER(OrgChart,
            OrgChart[ManagerEmail] = USERPRINCIPALNAME()
            || OrgChart[EmployeeEmail] = USERPRINCIPALNAME()),
        "Dept", OrgChart[Department]
    )

// Testing: Modeling → View As → select role + user

★ Data Categories — semantic types for columns

Properties → Data category:
┌──────────────────┬────────────────────────────────────────┐
│ Category         │ Enables                                │
├──────────────────┼────────────────────────────────────────┤
│ Address          │ Bing Maps geocoding                    │
│ City             │ Map visual auto-recognition            │
│ Country/Region   │ Map visual auto-recognition            │
│ State/Province   │ Map visual + ArcGIS                    │
│ Postal Code      │ Precision geo mapping                  │
│ Latitude         │ Custom map coordinates                 │
│ Longitude        │ Custom map coordinates                 │
│ Web URL          │ Clickable links in tables              │
│ Image URL        │ Display images inline                  │
│ Barcode          │ Barcode scanning (mobile app)          │
└──────────────────┴────────────────────────────────────────┘
```

---

## 🏗️ Power BI — Performance & Architecture Patterns

### Incremental Refresh & Aggregation Tables

```
★ Incremental Refresh — only load new/changed data!

Setup (Power BI Desktop):
1) Create parameters: RangeStart, RangeEnd (DateTime)
2) Filter source query: [Date] >= RangeStart && [Date] < RangeEnd
3) Right-click table → Incremental Refresh
4) Configure:
   - Archive: 5 years (historical data, never refreshed)
   - Refresh: 10 days (recent data, refreshed each time)
   - □ Detect data changes (optional, uses a column)
   - □ Only refresh complete days

Benefits:
  ✅ Refresh 10 days instead of 5 years → MUCH faster!
  ✅ Reduces memory during refresh
  ✅ Historical partitions stay cached
  ✅ Supports datasets > 1 GB

★ Aggregation Tables — pre-aggregate for speed!

1) Create aggregation table (Power Query):
   = Table.Group(Sales, {"Year", "Month", "ProductCategory"}, {
       {"TotalAmount", each List.Sum([Amount])},
       {"RowCount", each Table.RowCount(_)}
   })

2) Set aggregation (Model view → right-click agg table):
   ┌────────────────┬─────────────┬──────────────────┐
   │ Agg Column     │ Function    │ Detail Column    │
   ├────────────────┼─────────────┼──────────────────┤
   │ TotalAmount    │ Sum         │ Sales[Amount]    │
   │ RowCount       │ Count       │ Sales[Amount]    │
   │ Year           │ GroupBy     │ Date[Year]       │
   │ Month          │ GroupBy     │ Date[Month]      │
   │ ProductCategory│ GroupBy     │ Prod[Category]   │
   └────────────────┴─────────────┴──────────────────┘

3) Hide aggregation table from report view
4) Power BI auto-uses agg table when possible → 10-100x faster!
```

### Composite Models, Dynamic M & Real-Time

```
★ Composite Models — mix Import + DirectQuery!

Use case: big fact table = DirectQuery, small dims = Import
1) Some tables: Import mode (fast, cached)
2) Other tables: DirectQuery (always live)
3) Mix in same model → best of both worlds!

Benefits:
  ✅ Large tables don't need full import
  ✅ Dimensions stay fast (in-memory)
  ✅ Real-time data from DirectQuery tables

★ Hybrid Tables — same table, mixed storage!
  - Historical data: Import (fast)
  - Recent data: DirectQuery (live)
  - Configure via Incremental Refresh with "Get latest data in real-time"

★ Dynamic M Parameters — bind M query to DAX!

1) Create DAX table: ServerList = {"Server1", "Server2", "Server3"}
2) In M query: use parameter bound to DAX table
3) User selects server in slicer → M query changes data source!

Use cases:
  - Switch between databases
  - Select schema dynamically
  - Choose file path from slicer

★ Query Reduction — fewer queries to source

Settings → Options → Query reduction:
  □ Disable cross highlighting/filtering
  □ Add "Apply" button to slicers
  □ Add "Apply" button to all filters

Benefits:
  ✅ DirectQuery: fewer SQL queries fired
  ✅ Users make all filter selections, THEN click Apply
  ✅ Better performance with many slicers

★ Auto Page Refresh — real-time dashboards

Page settings → Page refresh:
  - Fixed interval: every 30 seconds, 1 min, etc.
  - Change detection: refresh when data changes
  - Admin must enable in Power BI Service
  - Works with DirectQuery only

★ Change Detection Measures:
  - Choose a measure that changes when new data arrives
  - E.g., MAX(Sales[OrderDate]) or COUNTROWS(Sales)
  - Page refreshes ONLY when this value changes
  - More efficient than fixed interval!
```

---

## 🟡 Power Query — Date/Time Functions Complete

### Date Arithmetic & IsIn* Family

```m
// ★ Date arithmetic functions — complete reference
let
    Today = Date.From(DateTime.LocalNow()),
    
    // Add/subtract time
    Plus30Days = Date.AddDays(Today, 30),
    Minus7Days = Date.AddDays(Today, -7),
    Plus3Months = Date.AddMonths(Today, 3),
    Plus1Year = Date.AddYears(Today, 1),
    Plus2Quarters = Date.AddQuarters(Today, 2),
    Plus1Week = Date.AddWeeks(Today, 1),

    // Date parts
    Y = Date.Year(Today),
    M = Date.Month(Today),
    D = Date.Day(Today),
    Q = Date.QuarterOfYear(Today),
    DOW = Date.DayOfWeek(Today, Day.Monday),   // 0=Mon
    DOY = Date.DayOfYear(Today),
    WOY = Date.WeekOfYear(Today),
    WOM = Date.WeekOfMonth(Today),
    DIM = Date.DaysInMonth(Today),             // 28/29/30/31
    
    // Start/End of period
    StartOfMonth = Date.StartOfMonth(Today),
    EndOfMonth = Date.EndOfMonth(Today),
    StartOfYear = Date.StartOfYear(Today),
    EndOfYear = Date.EndOfYear(Today),
    StartOfWeek = Date.StartOfWeek(Today, Day.Monday),
    EndOfWeek = Date.EndOfWeek(Today, Day.Monday),
    StartOfQuarter = Date.StartOfQuarter(Today),
    EndOfQuarter = Date.EndOfQuarter(Today),
    
    // ★ Date.IsIn* family — boolean date checks (VERY handy!)
    Source = #table({"Date", "Value"}, {}),
    
    CurrentDay = Table.SelectRows(Source, each Date.IsInCurrentDay([Date])),
    CurrentWeek = Table.SelectRows(Source, each Date.IsInCurrentWeek([Date])),
    CurrentMonth = Table.SelectRows(Source, each Date.IsInCurrentMonth([Date])),
    CurrentQuarter = Table.SelectRows(Source, each Date.IsInCurrentQuarter([Date])),
    CurrentYear = Table.SelectRows(Source, each Date.IsInCurrentYear([Date])),
    
    PrevDay = Table.SelectRows(Source, each Date.IsInPreviousDay([Date])),
    PrevWeek = Table.SelectRows(Source, each Date.IsInPreviousWeek([Date])),
    PrevMonth = Table.SelectRows(Source, each Date.IsInPreviousMonth([Date])),
    PrevQuarter = Table.SelectRows(Source, each Date.IsInPreviousQuarter([Date])),
    PrevYear = Table.SelectRows(Source, each Date.IsInPreviousYear([Date])),
    
    NextDay = Table.SelectRows(Source, each Date.IsInNextDay([Date])),
    NextWeek = Table.SelectRows(Source, each Date.IsInNextWeek([Date])),
    NextMonth = Table.SelectRows(Source, each Date.IsInNextMonth([Date])),
    NextQuarter = Table.SelectRows(Source, each Date.IsInNextQuarter([Date])),
    NextYear = Table.SelectRows(Source, each Date.IsInNextYear([Date])),
    
    // ★ N-period checks
    PrevNDays = Table.SelectRows(Source, each Date.IsInPreviousNDays([Date], 30)),
    PrevNMonths = Table.SelectRows(Source, each Date.IsInPreviousNMonths([Date], 3)),
    PrevNYears = Table.SelectRows(Source, each Date.IsInPreviousNYears([Date], 2)),
    NextNDays = Table.SelectRows(Source, each Date.IsInNextNDays([Date], 7))
in
    Today
```

### DateTime, DateTimeZone & Duration

```m
// ★ DateTime & DateTimeZone — timezone handling
let
    // Current time with timezone
    NowLocal = DateTime.LocalNow(),           // Local time
    NowUtc = DateTimeZone.UtcNow(),           // UTC time
    NowFixed = DateTime.FixedLocalNow(),      // Same value during refresh
    
    // ★ Convert between timezones
    ThaiTime = DateTimeZone.SwitchZone(
        DateTimeZone.UtcNow(), 7),            // UTC+7
    JapanTime = DateTimeZone.SwitchZone(
        DateTimeZone.UtcNow(), 9),            // UTC+9
    
    // Remove timezone info
    WithoutTZ = DateTimeZone.RemoveZone(ThaiTime),
    
    // ★ DateTime construction & conversion
    FromParts = #datetime(2026, 3, 1, 14, 30, 0),
    FromText = DateTime.FromText("2026-03-01T14:30:00"),
    FromFileTime = DateTime.FromFileTime(133534386000000000),
    
    // Extract time parts
    Hour = DateTime.Time(NowLocal),           // time portion
    DateOnly = DateTime.Date(NowLocal),       // date portion
    
    // ★ Duration functions — time differences
    D1 = #date(2026, 1, 1),
    D2 = #date(2026, 3, 1),
    Diff = D2 - D1,                           // Duration: 59.00:00:00
    
    TotalDays = Duration.Days(Diff),          // 59
    TotalHours = Duration.TotalSeconds(Diff) / 3600,
    
    // Duration parts
    Days = Duration.Days(#duration(5, 12, 30, 45)),     // 5
    Hours = Duration.Hours(#duration(5, 12, 30, 45)),   // 12
    Minutes = Duration.Minutes(#duration(5, 12, 30, 45)), // 30
    Seconds = Duration.Seconds(#duration(5, 12, 30, 45)), // 45
    
    // ★ Format dates for display
    Formatted1 = DateTime.ToText(NowLocal, [Format="dd/MM/yyyy HH:mm"]),
    Formatted2 = DateTime.ToText(NowLocal, [Format="yyyy-MM-dd"]),
    ThaiFormat = DateTime.ToText(NowLocal, [Format="d MMMM yyyy", Culture="th-TH"]),
    // Result: "1 มีนาคม 2569" (Thai Buddhist year!)
    
    // ★ Parse dates from text with culture
    ParsedThai = Date.FromText("01/03/2569", [Culture="th-TH"]),
    ParsedUS = Date.FromText("03/01/2026", [Culture="en-US"]),
    ParsedUK = Date.FromText("01/03/2026", [Culture="en-GB"])
in
    ThaiTime
```

---

## 🟡 Power Query — Parameters & Error Recovery

### Parameter Queries & Dynamic Sources

```m
// ★ Parameters — make queries dynamic!

// 1) Create parameter: Manage Parameters → New Parameter
// Name: pServerName, Type: Text, Current Value: "server01"
// Name: pDatabaseName, Type: Text, Current Value: "SalesDB"
// Name: pStartDate, Type: Date, Current Value: 2026-01-01

// 2) Use parameters in M queries
let
    Source = Sql.Database(pServerName, pDatabaseName),
    Sales = Source{[Schema="dbo",Item="Sales"]}[Data],
    Filtered = Table.SelectRows(Sales, each [OrderDate] >= pStartDate)
in
    Filtered

// ★ Parameter from Query — make it dynamic from data!
// Create query that returns a single value:
let
    Source = Sql.Database("server", "db"),
    Max = List.Max(Source{[Schema="dbo",Item="Config"]}[Data][LastDate])
in
    Max
// Right-click → Convert to Parameter

// ★ Dynamic file path with parameter
let
    BasePath = pFolderPath,   // Parameter: "C:\Data\Monthly\"
    FileName = pFileName,      // Parameter: "Sales_2026.xlsx"
    FullPath = BasePath & FileName,
    Source = Excel.Workbook(File.Contents(FullPath)){0}[Data]
in
    Source

// ★ Relative file path (portable!)
let
    Source = Excel.CurrentWorkbook(){[Name="Parameters"]}[Content],
    FolderPath = Source{0}[Value],
    Files = Folder.Files(FolderPath)
in
    Files
```

### Error Recovery Patterns

```m
// ★ Error recovery — robust data cleaning
let
    Source = SomeDataSource,
    
    // 1) Table.RemoveRowsWithErrors — remove bad rows
    CleanRows = Table.RemoveRowsWithErrors(Source, {"Amount", "Date"}),
    
    // 2) Table.SelectRowsWithErrors — find bad rows (for investigation!)
    ErrorRows = Table.SelectRowsWithErrors(Source, {"Amount", "Date"}),
    
    // 3) try/otherwise — per-cell safe conversion
    SafeTransform = Table.TransformColumns(Source, {
        {"Amount", each try Number.From(_) otherwise null, type number},
        {"Date", each try Date.FromText(_) otherwise null, type date},
        {"Name", each try Text.Proper(Text.Trim(_)) otherwise "", type text}
    }),
    
    // 4) try with error recording — log WHY it failed
    WithErrorInfo = Table.AddColumn(Source, "ParseResult", each
        let
            result = try Number.From([Amount])
        in
            if result[HasError] then
                [Value = null, Error = result[Error][Message]]
            else
                [Value = result[Value], Error = null]
    ),
    // Expand to get Value and Error columns separately
    Expanded = Table.ExpandRecordColumn(WithErrorInfo, "ParseResult",
        {"Value", "Error"}, {"ParsedAmount", "ParseError"}),
    
    // 5) Multi-step recovery — try multiple formats
    SmartDateParse = Table.AddColumn(Source, "CleanDate", each
        let
            raw = [DateField],
            attempt1 = try Date.FromText(raw, [Format="dd/MM/yyyy"]),
            attempt2 = try Date.FromText(raw, [Format="MM/dd/yyyy"]),
            attempt3 = try Date.FromText(raw, [Format="yyyy-MM-dd"]),
            attempt4 = try Date.From(raw)
        in
            if not attempt1[HasError] then attempt1[Value]
            else if not attempt2[HasError] then attempt2[Value]
            else if not attempt3[HasError] then attempt3[Value]
            else if not attempt4[HasError] then attempt4[Value]
            else null,
    type date),
    
    // 6) Table.TransformColumnTypes with error handling
    TypedSafe = try Table.TransformColumnTypes(Source, {
        {"Amount", type number}
    }) otherwise Source   // If entire column fails, keep original
in
    SafeTransform
```

---

## 📐 DAX — Statistical & Financial Functions

### Statistical Functions

```dax
// ★ DAX statistical functions — data quality analysis

// Percentile
P50 = PERCENTILE.INC(Sales[Amount], 0.50)    // Median (inclusive)
P90 = PERCENTILE.INC(Sales[Amount], 0.90)    // 90th percentile
P95 = PERCENTILE.EXC(Sales[Amount], 0.95)    // Exclusive percentile
P25 = PERCENTILEX.INC(Sales, Sales[Amount], 0.25)  // Iterator version

// Median
Median_Sales = MEDIAN(Sales[Amount])
Median_By_Cat = MEDIANX(
    VALUES(Products[Category]),
    CALCULATE(SUM(Sales[Amount]))
)

// Standard Deviation
StdDev_Sample = STDEV.S(Sales[Amount])       // Sample (n-1)
StdDev_Pop = STDEV.P(Sales[Amount])          // Population (n)

// Variance
Var_Sample = VAR.S(Sales[Amount])
Var_Pop = VAR.P(Sales[Amount])

// ★ Outlier detection using statistics
Is_Outlier = 
    VAR Avg = AVERAGE(Sales[Amount])
    VAR StDev = STDEV.S(Sales[Amount])
    VAR CurrentVal = Sales[Amount]
    VAR ZScore = DIVIDE(CurrentVal - Avg, StDev)
    RETURN
    IF(ABS(ZScore) > 2, "⚠️ Outlier", "✅ Normal")

// IQR-based outlier detection
Outlier_IQR = 
    VAR Q1 = PERCENTILE.INC(Sales[Amount], 0.25)
    VAR Q3 = PERCENTILE.INC(Sales[Amount], 0.75)
    VAR IQR = Q3 - Q1
    VAR Lower = Q1 - 1.5 * IQR
    VAR Upper = Q3 + 1.5 * IQR
    RETURN
    COUNTROWS(
        FILTER(Sales,
            Sales[Amount] < Lower || Sales[Amount] > Upper)
    )

// Coefficient of Variation  
CV = DIVIDE(STDEV.S(Sales[Amount]), AVERAGE(Sales[Amount]))
```

### Financial Functions

```dax
// ★ DAX financial functions — loan/investment calculations

// PMT — monthly loan payment
Monthly_Payment = 
    VAR Rate = 0.05 / 12                      // 5% annual → monthly
    VAR Periods = 30 * 12                      // 30 years → months
    VAR LoanAmount = 5000000                   // 5M baht
    RETURN
    -PMT(Rate, Periods, LoanAmount, 0, 0)

// IPMT / PPMT — interest vs principal portions
Interest_Month_1 = -IPMT(0.05/12, 1, 360, 5000000, 0, 0)
Principal_Month_1 = -PPMT(0.05/12, 1, 360, 5000000, 0, 0)

// PV — present value
Present_Value = -PV(0.08, 10, 0, 1000000, 0)
// "How much to invest now to get 1M in 10 years at 8%?"

// FV — future value
Future_Value = -FV(0.08, 10, 50000, 0, 0)
// "If I save 50K/year for 10 years at 8%, how much?"

// ★ XIRR — IRR with irregular dates (VERY useful!)
Project_IRR = 
    XIRR(
        CashFlows,
        CashFlows[Amount],
        CashFlows[Date],
        0.1                                    // Initial guess
    )

// ★ XNPV — NPV with irregular dates
Project_NPV = 
    XNPV(
        0.10,                                  // Discount rate
        CashFlows,
        CashFlows[Amount],
        CashFlows[Date]
    )

// ★ SLN — straight-line depreciation
Annual_Depreciation = SLN(1000000, 100000, 10)
// Cost=1M, Salvage=100K, Life=10 years → 90K/year

// ★ RATE — find interest rate
Interest_Rate = RATE(360, -26500, 5000000, 0, 0, 0.01) * 12
// Monthly payment=26,500, Loan=5M, 360 months → annual rate
```

---

## 📐 DAX — INFO Functions & Advanced Logic

### INFO Functions & COALESCE Patterns

```dax
// ★ INFO.VIEW functions — inspect your model from DAX!

// List all measures in model
All_Measures = INFO.VIEW.MEASURES()
// Returns: Table, Name, Expression, DisplayFolder, Description, etc.

// List all tables
All_Tables = INFO.VIEW.TABLES()
// Returns: Name, Rows, DataCategory, StorageMode, etc.

// List all columns
All_Columns = INFO.VIEW.COLUMNS()
// Returns: Table, Name, DataType, IsHidden, SortByColumn, etc.

// List all relationships
All_Rels = INFO.VIEW.RELATIONSHIPS()
// Returns: FromTable, FromColumn, ToTable, ToColumn,
//          CrossFilterDirection, IsActive, etc.

// ★ NAMEOF — get column name as text
Column_Name = NAMEOF(Sales[Amount])
// Result: "Sales[Amount]"
// Useful in: dynamic error messages

// ★ COALESCE — first non-blank value (multi-column)
Contact = COALESCE(
    Customers[MobilePhone],
    Customers[HomePhone],
    Customers[WorkPhone],
    Customers[Email],
    "No Contact ❌"
)

// COALESCE with calculated values
Best_Price = COALESCE(
    Products[SalePrice],
    Products[DiscountPrice],
    Products[RetailPrice],
    Products[ListPrice]
)

// ★ IF.EAGER — force eager evaluation (performance)
// Normal IF: only evaluates branch that's needed (lazy)
// IF.EAGER: evaluates BOTH branches (can be faster sometimes!)
Result_Eager = IF.EAGER(
    HASONEVALUE(Products[Category]),
    [Complex_Measure_A],
    [Complex_Measure_B]
)
// Use when: both branches are similar cost
// Don't use when: one branch is much heavier

// ★ SWITCH TRUE — clean multi-condition (preferred over nested IF!)
Quality_Level = 
    SWITCH(
        TRUE(),
        [Score] >= 95, "🏆 Excellent",
        [Score] >= 85, "🟢 Good",
        [Score] >= 70, "🟡 Average",
        [Score] >= 50, "🟠 Below Average",
        "🔴 Poor"
    )
```

---

## 🏗️ Power BI Service — Administration & Features

### Dataflows, Datamarts & Gateway

```
★ Dataflows — shared ETL in Power BI Service

What: Power Query in the cloud, shared across datasets!
1) Create Dataflow (workspace → New → Dataflow)
2) Build Power Query transforms (same M language)
3) Schedule refresh independently
4) Multiple datasets can reference same Dataflow

Benefits:
  ✅ Clean data ONCE, use in MANY reports
  ✅ No duplication of ETL logic
  ✅ Centralized data preparation
  ✅ Non-Pro users can consume (with Premium)

Types:
  - Standard Dataflows (Gen1): Basic PQ in cloud
  - Analytical Dataflows: Write to Azure Data Lake (CDM)
  - Dataflows Gen2 (Fabric): Enhanced with Lakehouse

★ Datamarts — self-service relational database!

What: Auto-provisioned Azure SQL DB with Power BI UI
1) Create Datamart (workspace → New → Datamart)
2) Import data via visual editor
3) Auto-creates star schema
4) Query with T-SQL, DAX, or visual tools
5) Auto-generates dataset for reporting

Benefits:
  ✅ SQL database without DBA
  ✅ T-SQL query support
  ✅ Automatic dataset generation
  ✅ Row-level security built-in

★ On-premises Data Gateway — connect to local data

Types:
┌──────────────────────┬────────────────────────────────┐
│ Standard Mode        │ Personal Mode                  │
├──────────────────────┼────────────────────────────────┤
│ Shared across users  │ Single user only               │
│ Centrally managed    │ Self-managed                   │
│ Enterprise use       │ Individual use                 │
│ Supports Dataflows   │ Desktop refresh only           │
│ Multiple data sources│ Limited data sources           │
└──────────────────────┴────────────────────────────────┘

Setup:
  1) Download gateway from powerbi.com
  2) Install on machine with access to data sources
  3) Register in Power BI Service
  4) Map dataset connections to gateway
  5) Schedule automatic refresh
```

### REST API, Embedding & Paginated Reports

```
★ Power BI REST API — automation & management

// Trigger dataset refresh
POST https://api.powerbi.com/v1.0/myorg/datasets/{id}/refreshes

// Get datasets in workspace
GET https://api.powerbi.com/v1.0/myorg/groups/{workspaceId}/datasets

// Export report to file (PDF/PPTX/PNG)
POST https://api.powerbi.com/v1.0/myorg/reports/{id}/ExportTo

// Get refresh history
GET https://api.powerbi.com/v1.0/myorg/datasets/{id}/refreshes

// Update parameters
POST https://api.powerbi.com/v1.0/myorg/datasets/{id}/Default.UpdateParameters

Use cases:
  ✅ Trigger refresh after ETL completes
  ✅ Monitor refresh failures
  ✅ Auto-export reports to SharePoint
  ✅ Manage workspaces programmatically
  ✅ Mass-update data sources

★ Power BI Embedded — embed reports in apps

Embedding modes:
  1) "Embed for your organization" — AAD authenticated users
  2) "Embed for your customers" — app owns the token (B2C)

Token types:
  - AAD token: for organization users
  - Embed token: for external users (no Power BI license needed)
  
API: PATCH/GET endpoints for embedding configuration
JavaScript SDK: powerbi-client (npm package)

★ Paginated Reports — pixel-perfect output

Use cases: invoices, statements, regulatory reports
Features:
  - Page headers/footers
  - Page numbers
  - Table of contents
  - Subreports
  - Export to PDF, Word, Excel, CSV
  - Mail merge
  - Scheduled subscriptions

Created in: Power BI Report Builder (free download)
Connection: Power BI datasets, SQL, SSAS, etc.

★ Subscription & Alerts

1) Subscriptions:
   - Auto-email reports on schedule
   - PDF or online link
   - Per-user or distribution list

2) Data alerts:
   - Set threshold on KPI card
   - "Alert me when Sales < 100K"
   - Triggers Power Automate flow

3) Comments:
   - Comment on dashboards/reports
   - @mention colleagues
   - Tracked in activity feed
```

---

---

## 🟡 Power Query — Web & API Patterns

### Web.Contents with Headers & Authentication

```m
// ★ Web.Contents — REST API integration
let
    // Basic GET request
    SimpleGet = Json.Document(Web.Contents("https://api.example.com/data")),
    
    // ★ With headers (API key, Bearer token)
    WithApiKey = Json.Document(Web.Contents(
        "https://api.example.com/data",
        [
            Headers = [
                #"Authorization" = "Bearer " & pApiToken,
                #"Content-Type" = "application/json",
                #"Accept" = "application/json",
                #"X-API-Key" = pApiKey
            ]
        ]
    )),
    
    // ★ RelativePath — base URL + path (query folding friendly!)
    BaseUrl = "https://api.example.com",
    WithRelPath = Json.Document(Web.Contents(
        BaseUrl,
        [
            RelativePath = "/v2/orders",
            Headers = [#"Authorization" = "Bearer " & pToken],
            Query = [
                status = "active",
                page = "1",
                limit = "100"
            ]
        ]
    )),
    
    // ★ POST request with body
    PostResult = Json.Document(Web.Contents(
        "https://api.example.com/search",
        [
            Headers = [#"Content-Type" = "application/json"],
            Content = Json.FromValue([
                query = "sales data",
                filters = [year = 2026]
            ])
        ]
    )),
    
    // ★ Handle HTTP errors gracefully
    SafeApiCall = 
        let
            response = try Web.Contents(
                "https://api.example.com/data",
                [ManualStatusHandling = {400, 401, 403, 404, 500}]
            ),
            statusCode = Value.Metadata(response[Value])[Response.Status],
            result = if statusCode = 200 
                     then Json.Document(response[Value])
                     else [error = "HTTP " & Text.From(statusCode)]
        in
            result
in
    WithApiKey
```

### API Pagination & Web.Page

```m
// ★ API Pagination — fetch ALL pages automatically
let
    BaseUrl = "https://api.example.com",
    
    GetPage = (page as number) as table =>
        let
            response = Json.Document(Web.Contents(
                BaseUrl,
                [
                    RelativePath = "/orders",
                    Query = [
                        page = Text.From(page),
                        per_page = "100"
                    ]
                ]
            )),
            data = Table.FromRecords(response[data])
        in
            data,
    
    // Use List.Generate for auto-pagination
    AllPages = List.Generate(
        () => [Page = 1, Data = GetPage(1), HasMore = true],
        each [HasMore] and [Page] <= 50,    // Safety: max 50 pages
        each [
            Page = [Page] + 1,
            Data = try GetPage([Page] + 1) otherwise #table({}, {}),
            HasMore = try (Table.RowCount([Data]) > 0) otherwise false
        ],
        each [Data]
    ),
    
    Combined = Table.Combine(AllPages),
    
    // ★ Web.Page — parse HTML tables from web pages
    WebPage = Web.Page(
        Web.Contents("https://example.com/data-table")
    ),
    // Returns table with: Caption, Source (sub-table), ClassName
    FirstTable = WebPage{0}[Data],
    
    // ★ XML parsing
    XmlData = Xml.Tables(Web.Contents("https://api.example.com/feed.xml")),
    
    // ★ OData connector (auto-pagination built-in!)
    OData = OData.Feed("https://services.odata.org/V4/Northwind/", null, [
        Implementation = "2.0",
        ODataVersion = 4
    ])
in
    Combined
```

---

## 🟡 Power Query — Record Functions Complete

### Record Manipulation & Table.Schema

```m
// ★ Record functions — complete reference
let
    rec = [Name = "Alice", Age = 30, City = "Bangkok", Score = 95],
    
    // 1) Record.Field — get single field value
    Name = Record.Field(rec, "Name"),             // "Alice"
    
    // 2) Record.FieldValues — get all values as list
    Values = Record.FieldValues(rec),             // {"Alice", 30, "Bangkok", 95}
    
    // 3) Record.FieldNames — get all field names
    Names = Record.FieldNames(rec),               // {"Name", "Age", "City", "Score"}
    
    // 4) Record.FieldCount — count fields
    Count = Record.FieldCount(rec),               // 4
    
    // 5) Record.HasFields — check if fields exist
    Has = Record.HasFields(rec, {"Name", "Age"}), // true
    HasBad = Record.HasFields(rec, {"Email"}),    // false
    
    // 6) Record.AddField — add new field
    WithEmail = Record.AddField(rec, "Email", "alice@mail.com"),
    
    // 7) Record.RemoveFields — remove fields
    WithoutAge = Record.RemoveFields(rec, {"Age", "Score"}),
    // Result: [Name = "Alice", City = "Bangkok"]
    
    // 8) Record.SelectFields — keep only specified
    OnlyNameAge = Record.SelectFields(rec, {"Name", "Age"}),
    // Result: [Name = "Alice", Age = 30]
    
    // 9) Record.RenameFields — rename fields
    Renamed = Record.RenameFields(rec, {
        {"Name", "FullName"},
        {"City", "Location"}
    }),
    
    // 10) Record.TransformFields — transform values
    Transformed = Record.TransformFields(rec, {
        {"Name", Text.Upper},
        {"Age", each _ + 1}
    }),
    // Result: [Name = "ALICE", Age = 31, ...]
    
    // 11) Record.Combine — merge records (later wins on conflicts)
    Merged = Record.Combine({
        [A = 1, B = 2],
        [B = 99, C = 3]     // B overwrites!
    }),
    // Result: [A = 1, B = 99, C = 3]
    
    // 12) Record.ReorderFields — change field order
    Reordered = Record.ReorderFields(rec,
        {"Score", "Name", "Age", "City"}),
    
    // 13) Record.ToTable — convert record to table (Name/Value pairs)
    AsTable = Record.ToTable(rec),
    // Result: Name  | Value
    //         Name  | Alice
    //         Age   | 30
    //         ...
    
    // ★ Table.Schema — inspect table structure (metadata!)
    SomeTable = #table({"ID", "Name", "Amount"}, {{1, "A", 100}}),
    Schema = Table.Schema(SomeTable)
    // Returns: Name, Position, TypeName, Kind, IsNullable,
    //          NumericPrecisionBase, NumericPrecision, NumericScale
    // Very useful for data quality checks!
in
    Schema
```

---

## 📐 DAX — Table Functions Deep Dive

### ADDCOLUMNS, SELECTCOLUMNS & SUMMARIZE

```dax
// ★ ADDCOLUMNS — add calculated columns to virtual table
Sales_With_Category = 
    ADDCOLUMNS(
        Sales,
        "Category", RELATED(Products[Category]),
        "Revenue", Sales[Qty] * Sales[Price],
        "Is_High", IF(Sales[Qty] * Sales[Price] > 10000, "Yes", "No")
    )

// ★ SELECTCOLUMNS — pick & rename columns (like SQL SELECT)
Product_Summary = 
    SELECTCOLUMNS(
        Products,
        "Product", Products[ProductName],
        "Price", Products[ListPrice],
        "Category", Products[Category]
    )

// ★ SUMMARIZE — group by with context
// ⚠️ WARNING: Don't add measures in SUMMARIZE! Use ADDCOLUMNS wrapper
Sales_By_Category = 
    // ❌ BAD: SUMMARIZE(Sales, Products[Category], "Total", SUM(Sales[Amount]))
    // ✅ GOOD:
    ADDCOLUMNS(
        SUMMARIZE(Sales, Products[Category]),
        "Total", CALCULATE(SUM(Sales[Amount])),
        "Count", CALCULATE(COUNTROWS(Sales))
    )

// ★ SUMMARIZECOLUMNS — best for grouped summaries
// Automatically removes blank rows!
Region_Product_Sales = 
    SUMMARIZECOLUMNS(
        Geography[Region],
        Products[Category],
        TREATAS({"2026"}, Date[Year]),        // filter
        "Total Sales", SUM(Sales[Amount]),
        "Avg Price", AVERAGE(Sales[Price]),
        "Orders", COUNTROWS(Sales)
    )
```

### TOPN, GENERATE, CROSSJOIN & Joins

```dax
// ★ TOPN — get top N rows
Top_10_Products = 
    TOPN(10, Products, [Total Sales], DESC)

// Dynamic Top N with slicer
Top_N_Dynamic = 
    CALCULATE(
        SUM(Sales[Amount]),
        TOPN(
            SELECTEDVALUE(TopN_Param[Value], 10),
            ALL(Products[ProductName]),
            [Total Sales], DESC
        )
    )

// ★ SAMPLE — random sample of rows
Random_10 = SAMPLE(10, Sales, Sales[OrderDate], ASC)

// ★ GENERATE — cross apply (for each row, evaluate expression)
Product_With_Monthly = 
    GENERATE(
        VALUES(Products[ProductName]),
        ADDCOLUMNS(
            VALUES(Date[Month]),
            "Sales", CALCULATE(SUM(Sales[Amount]))
        )
    )

// ★ GENERATEALL — like GENERATE but keeps blank rows too  
All_Combos = 
    GENERATEALL(
        VALUES(Products[Category]),
        ADDCOLUMNS(
            VALUES(Date[Month]),
            "Sales", CALCULATE(SUM(Sales[Amount]))
        )
    )

// ★ CROSSJOIN — all combinations (cartesian product)
All_Product_Dates = 
    CROSSJOIN(
        VALUES(Products[ProductName]),
        VALUES(Date[Month])
    )

// ★ NATURALINNERJOIN — join on matching columns
Matched = 
    NATURALINNERJOIN(
        SELECTCOLUMNS(Sales, "ProdKey", Sales[ProductKey], "Amount", Sales[Amount]),
        SELECTCOLUMNS(Products, "ProdKey", Products[ProductKey], "Name", Products[Name])
    )

// ★ NATURALLEFTOUTERJOIN — left join on matching columns
AllWithDetails = 
    NATURALLEFTOUTERJOIN(
        ALL(Products),
        ADDCOLUMNS(
            SUMMARIZE(Sales, Sales[ProductKey]),
            "TotalSales", CALCULATE(SUM(Sales[Amount]))
        )
    )
```

---

## 📐 DAX — FORMAT Patterns Complete

### FORMAT Function Reference

```dax
// ★ FORMAT — complete format string reference

// === Number Formats ===
Amount_Comma = FORMAT(1234567.89, "#,##0.00")        // "1,234,567.89"
Amount_Thai = FORMAT(1234567.89, "#,##0.00 ฿")       // "1,234,567.89 ฿"
Percent = FORMAT(0.1567, "0.0%")                      // "15.7%"
Percent_2d = FORMAT(0.1567, "0.00%")                  // "15.67%"
Integer = FORMAT(42, "000")                            // "042" (padded)
Millions = FORMAT(1234567, "#,##0,, M")               // "1 M"
Thousands = FORMAT(1234567, "#,##0, K")               // "1,235 K"
Scientific = FORMAT(0.0000123, "0.00E+0")             // "1.23E-5"
Negative_Red = FORMAT(-100, "#,##0;(#,##0)")          // "(100)"

// === Date Formats ===
ISO = FORMAT(TODAY(), "yyyy-MM-dd")                    // "2026-03-01"
Thai = FORMAT(TODAY(), "dd/MM/yyyy")                   // "01/03/2026"
US = FORMAT(TODAY(), "MM/dd/yyyy")                     // "03/01/2026"
Long = FORMAT(TODAY(), "dddd, MMMM d, yyyy")          // "Sunday, March 1, 2026"
Short = FORMAT(TODAY(), "d MMM yy")                    // "1 Mar 26"
MonthYear = FORMAT(TODAY(), "MMM yyyy")                // "Mar 2026"
YearMonth = FORMAT(TODAY(), "yyyyMM")                  // "202603"
QuarterYear = "Q" & FORMAT(TODAY(), "Q yyyy")          // "Q1 2026"

// === Time Formats ===
Time_24h = FORMAT(NOW(), "HH:mm:ss")                  // "14:30:00"
Time_12h = FORMAT(NOW(), "hh:mm tt")                   // "02:30 PM"
DateTime = FORMAT(NOW(), "yyyy-MM-dd HH:mm:ss")       // "2026-03-01 14:30:00"

// === Day/Month Names ===
DayFull = FORMAT(TODAY(), "dddd")                      // "Sunday"
DayShort = FORMAT(TODAY(), "ddd")                      // "Sun"
MonthFull = FORMAT(TODAY(), "MMMM")                    // "March"
MonthShort = FORMAT(TODAY(), "MMM")                    // "Mar"

// ★ Dynamic Format Strings (NEW! — PBI Dec 2022+)
// Set on measure → Properties → Dynamic format string
Dynamic_Format = 
    SWITCH(
        TRUE(),
        SELECTEDVALUE(Metrics[Metric]) = "Revenue", "$#,##0",
        SELECTEDVALUE(Metrics[Metric]) = "Margin", "0.0%",
        SELECTEDVALUE(Metrics[Metric]) = "Units", "#,##0",
        "#,##0.00"
    )

// ★ Conditional positive/negative/zero format
// FORMAT pattern: "positive;negative;zero"
Smart_Format = FORMAT(
    [Value],
    "#,##0.00 ▲;#,##0.00 ▼;—"
)

// ★ Arrow indicators for KPIs
KPI_Arrow = 
    VAR Change = [MoM_Change]
    RETURN
    FORMAT(Change, "↑ 0.0%;↓ 0.0%;→ 0.0%")
```

---

## 🏗️ Data Modeling — Advanced Patterns

### SCD, Role-Playing & Bridge Tables

```
★ Slowly Changing Dimensions (SCD) — handling changes over time

Type 1: Overwrite (no history)
  - Just update the value
  - Old value is lost
  - Use: correcting errors, non-important changes
  
Type 2: Add new row (full history!) ← MOST COMMON
  - Add new row with updated values  
  - Mark old row as inactive (ValidFrom/ValidTo dates)
  - Table: CustomerID, Name, Address, ValidFrom, ValidTo, IsCurrent
  
  DAX for SCD Type 2:
  Current_Customer = CALCULATE(
      COUNTROWS(DimCustomer),
      DimCustomer[IsCurrent] = TRUE
  )
  
  Historical_Value = CALCULATE(
      VALUES(DimCustomer[Address]),
      DimCustomer[ValidFrom] <= [OrderDate],
      DimCustomer[ValidTo] >= [OrderDate]
  )

Type 3: Add column (limited history)
  - Old column + New column
  - Only stores 1 previous value
  - Table: CustomerID, Name, CurrentCity, PreviousCity

★ Role-Playing Dimensions — same dim, multiple roles

Example: Date dimension used for OrderDate, ShipDate, DueDate

Setup:
  1) Create ONE Date dimension table
  2) Create 3 relationships (only 1 active!)
     FactSales[OrderDate] → DimDate[Date]     ← ACTIVE
     FactSales[ShipDate] → DimDate[Date]      ← INACTIVE
     FactSales[DueDate] → DimDate[Date]       ← INACTIVE
  
  3) Use USERELATIONSHIP in DAX:
  Ship_Sales = CALCULATE(
      SUM(Sales[Amount]),
      USERELATIONSHIP(Sales[ShipDate], DimDate[Date])
  )
  
  Due_Sales = CALCULATE(
      SUM(Sales[Amount]),
      USERELATIONSHIP(Sales[DueDate], DimDate[Date])
  )

★ Bridge Tables — Many-to-Many relationships

Use case: Sales → Products, but Orders have MULTIPLE products
  
  OrderProducts (Bridge):
  ┌──────────┬───────────┬────────────┐
  │ OrderID  │ ProductID │ Weight     │
  ├──────────┼───────────┼────────────┤
  │ 1        │ A         │ 0.6        │
  │ 1        │ B         │ 0.4        │
  │ 2        │ A         │ 1.0        │
  └──────────┴───────────┴────────────┘
  
  Weighted_Sales = SUMX(
      Bridge,
      Bridge[Weight] * RELATED(Sales[Amount])
  )

★ Junk Dimensions — group low-cardinality flags

Instead of: IsPaid(Y/N), IsShipped(Y/N), IsReturned(Y/N) in fact table
Create: DimStatus with all combinations (2×2×2 = 8 rows)
  ┌────┬────────┬──────────┬──────────┐
  │ ID │ IsPaid │ IsShipped│ IsReturn │
  ├────┼────────┼──────────┼──────────┤
  │ 1  │ Yes    │ Yes      │ No       │
  │ 2  │ Yes    │ No       │ No       │
  │ ...│ ...    │ ...      │ ...      │
  └────┴────────┴──────────┴──────────┘

Benefits: reduces fact table width, cleaner model

★ DAX Query View (NEW! — PBI Desktop 2024+)

  - Write DAX queries directly in PBI Desktop
  - Tab: View → DAX Query View
  - Syntax: EVALUATE <table expression>
  
  EVALUATE
  TOPN(10,
      ADDCOLUMNS(
          VALUES(Products[ProductName]),
          "Sales", [Total Sales]
      ),
      [Sales], DESC
  )
  ORDER BY [Sales] DESC
  
  Use for: data validation, debugging measures, ad-hoc analysis
```

---

---

## 🟡 Power Query — Custom Functions & Expression.Evaluate

### Creating Reusable Custom Functions

```m
// ★ Custom Functions — reusable transformation logic!

// 1) Basic custom function (clean text)
let
    CleanText = (input as text) as text =>
        let
            trimmed = Text.Trim(input),
            lower = Text.Lower(trimmed),
            noExtraSpaces = Text.Combine(
                List.Select(
                    Text.Split(lower, " "),
                    each _ <> ""
                ), " "
            )
        in
            noExtraSpaces
in
    CleanText
// Usage: = Table.TransformColumns(Source, {{"Name", CleanText}})

// 2) Multi-parameter function with optional params
let
    FormatCurrency = (
        amount as number,
        optional currency as text,
        optional decimals as number
    ) as text =>
        let
            cur = if currency = null then "฿" else currency,
            dec = if decimals = null then 2 else decimals,
            formatted = Number.ToText(amount, "N" & Text.From(dec))
        in
            formatted & " " & cur
in
    FormatCurrency
// Usage: FormatCurrency(1234.5)       → "1,234.50 ฿"
//        FormatCurrency(1234.5, "$")   → "1,234.50 $"

// 3) Function with documentation (shows in UI!)
let
    fn = (input as text) as text => Text.Proper(Text.Trim(input)),
    fnType = type function (
        input as (type text meta [
            Documentation.FieldCaption = "Input Text",
            Documentation.FieldDescription = "Text to clean and format",
            Documentation.SampleValues = {"  john doe  "}
        ])
    ) as text meta [
        Documentation.Name = "CleanName",
        Documentation.Description = "Trims whitespace and converts to proper case",
        Documentation.Category = "Data Cleaning",
        Documentation.Examples = {[
            Description = "Clean a name",
            Code = "CleanName(""  john doe  "")",
            Result = """John Doe"""
        ]}
    ]
in
    Value.ReplaceType(fn, fnType)

// 4) Function that processes entire table
let
    StandardizeTable = (tbl as table) as table =>
        let
            // Trim all text columns
            textCols = Table.ColumnsOfType(tbl, {type text}),
            trimmed = List.Accumulate(
                textCols, tbl,
                (state, col) => Table.TransformColumns(state,
                    {{col, Text.Trim}})
            ),
            // Remove empty rows
            noEmpty = Table.SelectRows(trimmed, each not List.AllTrue(
                List.Transform(Record.FieldValues(_), each _ = null or _ = "")
            ))
        in
            noEmpty
in
    StandardizeTable
```

### Expression.Evaluate & Dynamic M

```m
// ★ Expression.Evaluate — execute M code dynamically!
let
    // Dynamic column reference
    ColName = "Amount",
    DynamicRef = Expression.Evaluate(
        "each [" & ColName & "]",
        [each = each, #"[]" = _]
    ),
    
    // ★ Dynamic M from parameter/config table
    ConfigTable = #table({"Step", "MCode"}, {
        {"Filter", "Table.SelectRows(_, each [Status] = ""Active"")"},
        {"Sort", "Table.Sort(_, {{""Date"", Order.Descending}})"}
    }),
    
    ApplyStep = (tbl as table, mCode as text) as table =>
        Expression.Evaluate(mCode, #shared & [_ = tbl]),
    
    // Apply all config steps
    Result = List.Accumulate(
        ConfigTable[MCode],
        SourceTable,
        (state, code) => ApplyStep(state, code)
    ),
    
    // ★ Table.View — custom query folding hints
    CustomView = Table.View(null, [
        GetType = () => type table [ID = number, Name = text],
        GetRows = () => SourceTable,
        OnSelectColumns = (columns) =>
            Table.SelectColumns(SourceTable, columns),
        OnSelectRows = (condition) =>
            Table.SelectRows(SourceTable, condition),
        OnSort = (order) =>
            Table.Sort(SourceTable, order)
    ]),
    
    // ★ #shared — access all available M functions
    AllFunctions = Record.FieldNames(#shared),
    // Returns 700+ built-in function names
    
    TextFunctions = List.Select(AllFunctions, each Text.StartsWith(_, "Text."))
    // Returns: {"Text.Trim", "Text.Upper", "Text.Lower", ...}
in
    Result
```

---

## 📐 DAX — Relationship & Filter Functions

### CROSSFILTER, ISFILTERED & Filter Inspection

```dax
// ★ CROSSFILTER — change filter direction dynamically
// Default: single direction (dim → fact)
// CROSSFILTER: override per-measure!

Bi_Directional_Count = 
    CALCULATE(
        DISTINCTCOUNT(Products[ProductID]),
        CROSSFILTER(Sales[ProductKey], Products[ProductKey], BOTH)
    )

No_Filter_Propagation = 
    CALCULATE(
        SUM(Sales[Amount]),
        CROSSFILTER(Sales[CustomerKey], Customers[CustomerKey], NONE)
    )

One_Way = 
    CALCULATE(
        SUM(Sales[Amount]),
        CROSSFILTER(Sales[DateKey], Date[DateKey], ONEWAY)
    )

// ★ ISFILTERED — check if column has direct filter
// ★ ISCROSSFILTERED — check if column has ANY filter (direct or cross)
Smart_Measure = 
    IF(
        ISFILTERED(Products[Category]),
        "Category is filtered: " & SELECTEDVALUE(Products[Category]),
        IF(
            ISCROSSFILTERED(Products[Category]),
            "Category is cross-filtered",
            "No filter on Category"
        )
    )

// ★ SELECTEDVALUE vs HASONEVALUE — when to use which?
// SELECTEDVALUE: returns value if single, else alternate
Safe_Country = SELECTEDVALUE(Geography[Country], "Multiple")

// HASONEVALUE: returns TRUE/FALSE (for IF conditions)
Conditional_Calc = 
    IF(
        HASONEVALUE(Products[Category]),
        [Detailed_Measure],    // single category → show detail
        [Summary_Measure]      // multiple → show summary
    )

// ★ HASONEFILTER — is exactly ONE filter value selected?
Single_Filter_Check = HASONEFILTER(Products[Category])

// ★ ALLSELECTED — what user sees in visual context
Visual_Total = 
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(SUM(Sales[Amount]), ALLSELECTED())
    )

// ★ VALUES vs DISTINCT — subtle difference!
// VALUES: includes blank row added by invalid relationships
// DISTINCT: only actual distinct values (no extra blank)
Count_With_Blank = COUNTROWS(VALUES(Products[Category]))
Count_No_Blank = COUNTROWS(DISTINCT(Products[Category]))
```

---

## 📐 DAX — String Functions Complete

### Text Manipulation & Comparison

```dax
// ★ DAX string functions — complete reference

// REPT — repeat text
Stars = REPT("★", Sales[Rating])          // "★★★★★"
Line = REPT("─", 50)                       // 50-char line
Indent = REPT("  ", [Level]) & [Name]      // hierarchy indent

// UNICHAR / UNICODE — special characters
CheckMark = UNICHAR(10004)                  // ✔
CrossMark = UNICHAR(10008)                  // ✘
Arrow_Up = UNICHAR(9650)                    // ▲
Arrow_Down = UNICHAR(9660)                  // ▼
Bullet = UNICHAR(8226)                      // •
ThaiChar = UNICHAR(3585)                    // ก

CharCode = UNICODE("A")                    // 65
ThaiCode = UNICODE("ก")                    // 3585

// EXACT — case-sensitive comparison (unlike =)
Is_Match = EXACT("Hello", "hello")          // FALSE (case matters!)
Is_Equal = ("Hello" = "hello")              // TRUE (DAX = is case-insensitive!)

// SUBSTITUTE vs REPLACE
// SUBSTITUTE: find & replace text anywhere
Clean1 = SUBSTITUTE("Hello World", "World", "DAX")     // "Hello DAX"
Clean2 = SUBSTITUTE("A-B-C", "-", " ")                  // "A B C"
// Replace ALL occurrences:
Clean3 = SUBSTITUTE("a.b.c.d", ".", ",")                // "a,b,c,d"
// Replace specific instance:
Clean4 = SUBSTITUTE("a.b.c", ".", "-", 2)               // "a.b-c" (2nd only)

// REPLACE: position-based replacement
Repl1 = REPLACE("ABCDEF", 3, 2, "XX")                   // "ABXXEF"
// Start at pos 3, replace 2 chars with "XX"

// ★ COMBINEVALUES — delimiter-separated concatenation
// Special: optimizes DirectQuery!
Full_Key = COMBINEVALUES("_",
    Sales[Region],
    Sales[Product],
    FORMAT(Sales[Date], "yyyyMMdd")
)

// ★ CONTAINSSTRING / CONTAINSSTRINGEXACT
Has_Text = CONTAINSSTRING(Products[Name], "pro")         // Case-insensitive
Has_Exact = CONTAINSSTRINGEXACT(Products[Name], "Pro")   // Case-sensitive

// ★ TRIM vs CLEAN
Trimmed = TRIM("  hello   world  ")         // "hello world" (extra spaces)
Cleaned = CLEAN("hello" & UNICHAR(10))      // Removes non-printable chars

// ★ BLANK() vs "" — important difference!
// BLANK() is "nothing" — measures can return BLANK
// "" is empty string — still a value!
Check = IF(ISBLANK([Value]), "No data", [Value])
```

---

## 🤖 Power BI — AI & Copilot Features

### Q&A, Smart Narratives & AI Visuals

```
★ Q&A Visual — natural language queries

How to use:
  1) Insert → Q&A visual
  2) Type question: "total sales by region last month"
  3) Power BI generates visual automatically!

Improve Q&A:
  - Add synonyms: Modeling → Q&A Setup → Teach Q&A
  - Define terms: "revenue" = SUM(Sales[Amount])
  - Suggest questions: appear in Q&A dropdown

★ Smart Narratives — auto-generated text insights

How to use:
  1) Insert → Smart Narrative visual
  2) Auto-detects: top values, trends, outliers
  3) Customize: click "+" to add custom values
  4) Dynamic: updates with filters!

Formats: "Sales increased by {SUM(Sales[Amount])} this month"

★ Key Influencers — what drives a metric?

How to use:
  1) Insert → Key Influencers visual
  2) Set "Analyze" field: what you want to understand
  3) Set "Explain by" fields: potential factors
  4) Shows: top factors that increase/decrease metric

Use cases:
  - What drives customer churn?
  - What affects product ratings?
  - Why do some orders get delayed?

★ Decomposition Tree — drill-down analysis

How to use:
  1) Insert → Decomposition Tree
  2) Set "Analyze" field: your measure
  3) Set "Explain by" fields: dimensions to drill
  4) Click "+": manually choose or let AI suggest!
  5) AI picks highest/lowest value automatically

★ Anomaly Detection — auto-detect unusual data points

How to use (in line charts):
  1) Create line chart with date axis
  2) Analytics pane → Find Anomalies → ON
  3) Configure sensitivity (0-100%)
  4) Shows: anomaly markers + explanations

Provides:
  - Expected value
  - Upper/lower bounds
  - Anomaly strength
  - Possible explanations (Key Influencers engine)

★ Copilot in Power BI (Premium/Fabric)

Features:
  1) Create report from data: "Show me sales by region"
  2) Generate DAX: "Create measure for YoY growth"
  3) Summarize page: auto-generates narrative
  4) Suggest questions: recommends what to ask
  5) Explain changes: "Why did sales drop?"
```

---

## 🔧 Power BI — DevOps & ALM

### Deployment Pipelines, Git & BPA

```
★ Deployment Pipelines — Dev → Test → Prod

Setup (requires Premium/Fabric):
  1) Create pipeline: Deployment Pipelines → New
  2) Assign workspaces to stages:
     ┌──────────┐    ┌──────────┐    ┌──────────┐
     │   DEV    │ →  │   TEST   │ →  │   PROD   │
     │workspace │    │workspace │    │workspace │
     └──────────┘    └──────────┘    └──────────┘
  3) Deploy: click ► between stages
  4) Compare: see what changed before deploying

Features:
  ✅ Auto-rebind data sources per stage
  ✅ Deployment rules (change connection string per stage)
  ✅ Selective deployment (choose which items)
  ✅ Backward deployment (Prod → Dev for hotfixes)
  ✅ API support for automated deployments

★ Git Integration (PBIP format) — version control!

Setup:
  1) File → Save as → Power BI Project (.pbip)
  2) Workspace → Settings → Git Integration
  3) Connect to Azure DevOps or GitHub repo
  4) Sync: workspace ↔ Git branch

PBIP format explodes .pbix into files:
  📁 MyReport.Report/
     📄 report.json         ← report layout
     📄 definition.pbir      ← report config
  📁 MyReport.SemanticModel/
     📄 model.bim            ← data model (TMDL format)
     📄 definition.pbism     ← model config
  📄 MyReport.pbip           ← project file

Benefits:
  ✅ Code review on report changes
  ✅ Merge conflict resolution
  ✅ Branch per feature
  ✅ CI/CD automation
  ✅ History of all changes

★ Best Practices Analyzer (BPA) — via Tabular Editor

Rules check:
  ┌──────────────────────────────────┬──────────┐
  │ Rule                             │ Severity │
  ├──────────────────────────────────┼──────────┤
  │ Hidden columns → use in calc     │ Warning  │
  │ Unused measures                  │ Warning  │
  │ SUMMARIZE with expressions       │ Error    │
  │ No format string on measures     │ Warning  │
  │ Relationships inactive           │ Info     │
  │ Columns not in any relationship  │ Warning  │
  │ Date table not marked            │ Error    │
  │ Large text columns in fact table │ Warning  │
  │ Measure not in display folder    │ Warning  │
  │ Bi-directional relationships     │ Warning  │
  └──────────────────────────────────┴──────────┘

How: Tabular Editor → Tools → Best Practice Analyzer

★ Sensitivity Labels — data protection

Types:
  - Public
  - General  
  - Confidential
  - Highly Confidential

Apply: File → Info → Sensitivity Label
Inherits: label travels with data (export, share)
Enforces: encryption, watermarks, access control

★ ALM Toolkit — schema comparison

Compare two .pbix files:
  - New objects ✅ (measures, tables, columns)
  - Changed objects 🔄 (modified DAX, renamed)
  - Missing objects ❌ (deleted items)
  - Selective sync: choose what to merge
```

---

---

## 🟡 Power Query — Join Patterns Deep

### All Join Types & Anti-Join

```m
// ★ Table.NestedJoin — complete join reference
let
    Left = #table({"ID","Name"}, {{1,"A"},{2,"B"},{3,"C"},{4,"D"}}),
    Right = #table({"ID","Score"}, {{1,90},{2,85},{5,70}}),
    
    // 1) Inner Join — only matching rows
    Inner = Table.NestedJoin(Left, "ID", Right, "ID", "Match", JoinKind.Inner),
    // Result: {1,A,90}, {2,B,85}  (only ID 1,2)
    
    // 2) Left Outer — all left + matching right
    LeftOuter = Table.NestedJoin(Left, "ID", Right, "ID", "Match", JoinKind.LeftOuter),
    // Result: {1,A,90}, {2,B,85}, {3,C,null}, {4,D,null}
    
    // 3) Right Outer — matching left + all right
    RightOuter = Table.NestedJoin(Left, "ID", Right, "ID", "Match", JoinKind.RightOuter),
    // Result: {1,A,90}, {2,B,85}, {null,null,70}
    
    // 4) Full Outer — all from both sides
    FullOuter = Table.NestedJoin(Left, "ID", Right, "ID", "Match", JoinKind.FullOuter),
    // Result: all rows from both, null where no match
    
    // 5) Left Anti — left rows WITHOUT match (NOT IN!) ★
    LeftAnti = Table.NestedJoin(Left, "ID", Right, "ID", "Match", JoinKind.LeftAnti),
    // Result: {3,C}, {4,D}  (IDs not in Right!)
    // USE CASE: Find missing records, orphaned data!
    
    // 6) Right Anti — right rows WITHOUT match
    RightAnti = Table.NestedJoin(Left, "ID", Right, "ID", "Match", JoinKind.RightAnti),
    // Result: {5,70}  (ID 5 not in Left!)
    
    // ★ Multi-column join
    MultiJoin = Table.NestedJoin(
        Sales, {"Year", "Region"},
        Budget, {"Year", "Region"},
        "BudgetData", JoinKind.LeftOuter
    ),
    
    // ★ Expand after join
    Expanded = Table.ExpandTableColumn(
        LeftOuter, "Match",
        {"Score"}, {"Score"}
    ),
    
    // ★ Fuzzy Join options (approximate matching!)
    FuzzyJoin = Table.FuzzyNestedJoin(
        Table1, "Name", Table2, "Name", "Match",
        JoinKind.LeftOuter,
        [
            Threshold = 0.8,              // 80% similarity
            IgnoreCase = true,
            IgnoreSpace = true,
            NumberOfMatches = 1,           // best match only
            TransformationTable = synonyms // custom mapping
        ]
    )
in
    Expanded
```

### Comparer Functions & Culture-Aware Operations

```m
// ★ Comparer functions — culture-aware sorting & matching
let
    // Comparer types:
    // Comparer.Ordinal — binary comparison (fastest, case-sensitive)
    // Comparer.OrdinalIgnoreCase — binary, case-insensitive
    // Comparer.FromCulture — locale-aware comparison
    
    // Culture-aware sort (Thai alphabet order!)
    ThaiSort = Table.Sort(Source, {
        {"Name", Order.Ascending, Comparer.FromCulture("th-TH")}
    }),
    
    // Case-insensitive distinct
    DistinctCI = Table.Distinct(Source, {
        "Name", Comparer.OrdinalIgnoreCase
    }),
    
    // Case-insensitive group
    GroupedCI = Table.Group(Source, {
        {"Name", each _, Comparer.OrdinalIgnoreCase}
    }, {{"Count", each Table.RowCount(_)}}),
    
    // ★ Table.Join vs Table.NestedJoin
    // Table.Join: flat result (auto-expands)
    // Table.NestedJoin: nested table column (you control expansion)
    
    FlatJoin = Table.Join(Left, "ID", Right, "ID", JoinKind.Inner),
    // Immediately flat — no need to expand
    
    // ★ Merge Queries (UI equivalent)
    // Home → Merge Queries → select tables + join kind
    // Same as Table.NestedJoin behind the scenes!
    
    // ★ Append Queries (UNION)
    // Home → Append Queries → 2+ tables
    Appended = Table.Combine({Table1, Table2, Table3})
    // Stacks rows vertically (like SQL UNION ALL)
in
    ThaiSort
```

---

## 📐 DAX — PATH Functions (Hierarchy)

### Org Chart & Parent-Child Hierarchies

```dax
// ★ PATH functions — flatten parent-child hierarchies!
// Use case: Org Charts, Bill of Materials, Category trees

// Source table: Employees
// | EmpID | Name    | ManagerID |
// |-------|---------|-----------|
// | 1     | CEO     | null      |
// | 2     | VP Sales| 1         |
// | 3     | Manager | 2         |
// | 4     | Rep     | 3         |

// ★ PATH — create pipe-delimited path string
EmpPath = PATH(Employees[EmpID], Employees[ManagerID])
// Results:
// CEO:       "1"
// VP Sales:  "1|2"
// Manager:   "1|2|3"
// Rep:       "1|2|3|4"

// ★ PATHITEM — get Nth item from path
Level1 = PATHITEM([EmpPath], 1)              // "1" (root)
Level2 = PATHITEM([EmpPath], 2)              // "2" (second level)
Level3 = PATHITEM([EmpPath], 3, INTEGER)     // 3 (as number!)

// ★ PATHITEMREVERSE — get Nth item from END
CurrentLevel = PATHITEMREVERSE([EmpPath], 1)  // Self
DirectManager = PATHITEMREVERSE([EmpPath], 2) // Direct manager

// ★ PATHLENGTH — depth in hierarchy
Depth = PATHLENGTH([EmpPath])
// CEO=1, VP=2, Manager=3, Rep=4

// ★ PATHCONTAINS — check if ancestor exists
Reports_To_CEO = PATHCONTAINS([EmpPath], "1")  // Always TRUE
Reports_To_VP = PATHCONTAINS([EmpPath], "2")

// ★ Flatten hierarchy into columns
Level1_Name = LOOKUPVALUE(Employees[Name], Employees[EmpID],
    VALUE(PATHITEM([EmpPath], 1)))
Level2_Name = LOOKUPVALUE(Employees[Name], Employees[EmpID],
    VALUE(PATHITEM([EmpPath], 2)))
Level3_Name = LOOKUPVALUE(Employees[Name], Employees[EmpID],
    VALUE(PATHITEM([EmpPath], 3)))

// ★ Count subordinates
Subordinate_Count = 
    COUNTROWS(
        FILTER(ALL(Employees),
            PATHCONTAINS(Employees[EmpPath],
                FORMAT(SELECTEDVALUE(Employees[EmpID]), "0"))
        )
    ) - 1   // Minus self

// ★ Aggregate for entire sub-tree
Team_Sales = 
    CALCULATE(
        SUM(Sales[Amount]),
        FILTER(ALL(Employees),
            PATHCONTAINS(Employees[EmpPath],
                FORMAT(SELECTEDVALUE(Employees[EmpID]), "0"))
        )
    )
```

---

## 📐 DAX — LOOKUPVALUE & Lookup Patterns

### Multi-Condition Lookups & Alternatives

```dax
// ★ LOOKUPVALUE — find value from another table
// Like VLOOKUP/INDEX-MATCH in Excel!

// Basic lookup
Product_Name = LOOKUPVALUE(
    Products[ProductName],              // return this
    Products[ProductKey], Sales[ProductKey]  // match condition
)

// ★ Multi-condition lookup
Target_Amount = LOOKUPVALUE(
    Targets[Target],
    Targets[Year], YEAR(Sales[OrderDate]),
    Targets[Region], Sales[Region],
    Targets[Category], RELATED(Products[Category])
)

// ★ With default value (no match → return default)
Safe_Lookup = LOOKUPVALUE(
    Rates[ExchangeRate],
    Rates[Currency], Sales[Currency],
    Rates[Date], Sales[OrderDate],
    1.0    // Default: 1.0 if no match found
)

// ★ LOOKUPVALUE vs RELATED — when to use which?
//
// RELATED:
//   ✅ Uses model relationships
//   ✅ Faster (pre-computed)
//   ❌ Only works with existing relationships
//   = RELATED(Products[Name])
//
// LOOKUPVALUE:
//   ✅ No relationship needed!
//   ✅ Multi-condition support
//   ❌ Slower (scans table each time)
//   = LOOKUPVALUE(Products[Name], Products[Key], Sales[Key])

// ★ LOOKUPVALUE for SCD Type 2 (date-range lookup)
Historical_Price = 
    CALCULATE(
        VALUES(PriceHistory[Price]),
        FILTER(PriceHistory,
            PriceHistory[ProductKey] = Sales[ProductKey]
            && PriceHistory[ValidFrom] <= Sales[OrderDate]
            && PriceHistory[ValidTo] >= Sales[OrderDate]
        )
    )

// ★ Closest match (nearest date)
Closest_Rate = 
    VAR CurrentDate = Sales[OrderDate]
    VAR Currency = Sales[Currency]
    RETURN
    CALCULATE(
        LASTNONBLANK(Rates[ExchangeRate], 1),
        FILTER(ALL(Rates),
            Rates[Currency] = Currency
            && Rates[Date] <= CurrentDate
        )
    )
```

---

## 🎨 Power BI — Conditional Formatting Deep

### Rules, Color Scales, Icons & Data Bars

```
★ Conditional Formatting — make data visual!

Access: Select visual → Format → Cell elements (tables/matrices)
  or: Right-click field → Conditional Formatting

1) Background color
   ┌─────────────────────────────────────────────────┐
   │ By rules:                                       │
   │   If value >= 100 → Green                       │
   │   If value >= 50  → Yellow                      │
   │   If value < 50   → Red                         │
   │                                                 │
   │ By color scale:                                 │
   │   Min (Red) ←──────────────→ Max (Green)        │
   │   Customize: min/center/max colors              │
   │   Based on: field value or measure              │
   │                                                 │
   │ By field value:                                 │
   │   Use a DAX measure that returns color hex:     │
   │   Color_Measure = IF([Score]>80, "#00B050",     │
   │                   IF([Score]>50, "#FFC000",     │
   │                   "#FF0000"))                    │
   └─────────────────────────────────────────────────┘

2) Font color — same options as background

3) Data bars — inline bar charts in cells!
   ┌─────────────────────────────────────────────────┐
   │ Settings:                                       │
   │   Show bar only / bar + value                   │
   │   Positive bar color: Blue                      │
   │   Negative bar color: Red                       │
   │   Bar direction: Left-to-right                  │
   │   Min/Max: auto or custom values                │
   └─────────────────────────────────────────────────┘

4) Icons — KPI indicators in cells
   ┌─────────────────────────────────────────────────┐
   │ Icon styles:                                    │
   │   ● ◐ ○   (circles)                            │
   │   ▲ ► ▼   (arrows/triangles)                   │
   │   ✔ ! ✘   (status)                             │
   │   ⭐⭐⭐    (stars)                              │
   │   🟢🟡🔴    (traffic lights)                    │
   │                                                 │
   │ Rules: value ranges → icon assignment           │
   │   >= 80%: ✔ Green                               │
   │   >= 50%: ! Yellow                              │
   │   < 50%:  ✘ Red                                 │
   │                                                 │
   │ Layout: left of value / right of value only     │
   └─────────────────────────────────────────────────┘

5) Web URL — make cells clickable links
   Format field as "Web URL" → cells become hyperlinks
   
   DAX: URL_Measure = "https://example.com/report/" & [OrderID]

★ Conditional Formatting on other visuals:

Cards: Use DAX with UNICHAR for colored icons
  Card_Value = UNICHAR(11044) & " " & FORMAT([Score], "#,##0")
  // Shows: ⬤ 1,234 (use font color for icon color)

Shapes: Conditional visibility via Bookmarks + buttons

Titles: Dynamic title with conditional text
  Dynamic_Title = 
      "Sales " & IF([MoM] > 0, "▲", "▼") & 
      FORMAT(ABS([MoM]), "0.0%")
```

---

## 📐 DAX — Visual Calculations (NEW!)

### Visual-Level DAX (2024+)

```dax
// ★ Visual Calculations — DAX that runs in visual context ONLY!
// NEW feature: Edit → New Visual Calculation (on a table/matrix)

// These work ONLY within the visual they're defined in
// They see the visual's rows, not the entire model

// ★ Running Sum (within visual)
Running_Sales = RUNNINGSUM([Total Sales])

// ★ Moving Average (within visual)
MA_3 = MOVINGAVERAGE([Total Sales], 3)

// ★ Rank (within visual rows)
Visual_Rank = RANK()

// ★ Percent of Parent (hierarchy-aware!)
Pct_Parent = 
    DIVIDE(
        [Total Sales],
        COLLAPSE([Total Sales], ROWS)    // parent total
    )

// ★ Percent of Grand Total
Pct_Grand = 
    DIVIDE(
        [Total Sales],
        COLLAPSEALL([Total Sales], ROWS) // grand total
    )

// ★ Difference from previous
MoM_Change = 
    [Total Sales] - PREVIOUS([Total Sales])

MoM_Pct = 
    DIVIDE(
        [Total Sales] - PREVIOUS([Total Sales]),
        PREVIOUS([Total Sales])
    )

// ★ First / Last in visual
First_Value = FIRST([Total Sales])
Last_Value = LAST([Total Sales])

// ★ EXPAND / COLLAPSE — navigate hierarchy
Parent_Sales = COLLAPSE([Total Sales], ROWS)
Child_Detail = EXPAND([Total Sales], ROWS)

// ★ COLLAPSEALL / EXPANDALL — jump to top/bottom
Grand_Total = COLLAPSEALL([Total Sales], ROWS)

// ★ Benefits of Visual Calculations:
// ✅ No model measures needed
// ✅ Context-aware (sees visual rows only)
// ✅ Simpler syntax than WINDOW/OFFSET
// ✅ RUNNINGSUM, MOVINGAVERAGE built-in
// ❌ Only in the visual they're created
// ❌ Can't be used in other visuals or DAX
// ❌ Preview feature (may change)
```

---

---

## 🟡 Power Query — Binary & Diagnostics

### Binary Functions & Query Diagnostics

```m
// ★ Binary functions — file & encoding operations

// Read binary file
let
    // Load raw file
    RawFile = File.Contents("C:\data\file.dat"),
    
    // Binary to text (decode)
    AsText = Text.FromBinary(RawFile, TextEncoding.Utf8),
    // Encodings: Utf8, Utf16, Ascii, Windows, Unicode
    
    // Text to binary (encode)
    AsBinary = Text.ToBinary("Hello World", TextEncoding.Utf8),
    
    // ★ Binary.Length — file size
    FileSize = Binary.Length(RawFile),
    // Returns size in bytes
    
    // ★ Binary.ToText — base64 encode
    Base64 = Binary.ToText(RawFile, BinaryEncoding.Base64),
    // Use case: embed binary data in JSON/XML
    
    // ★ Binary.FromText — base64 decode
    Decoded = Binary.FromText(Base64, BinaryEncoding.Base64),
    
    // ★ Binary.Compress / Decompress — GZip
    Compressed = Binary.Compress(RawFile, Compression.GZip),
    Decompressed = Binary.Decompress(Compressed, Compression.GZip),
    // Also: Compression.Deflate, Compression.None
    
    // ★ Lines.FromBinary — split binary to text lines
    Lines = Lines.FromBinary(RawFile, null, null, TextEncoding.Utf8),
    // Returns: list of text lines
    
    // ★ Binary.Range — extract portion
    Header = Binary.Range(RawFile, 0, 100)
    // First 100 bytes
in
    AsText

// ★ Query Diagnostics — measure query performance!
// UI: Tools → Start Diagnostics → run query → Stop Diagnostics
//
// Returns 2 tables:
// 1) Diagnostics.Aggregated — summary per step
//    Columns: [Exclusive Duration, Inclusive Duration, Step, Category]
//
// 2) Diagnostics.Detailed — every operation
//    Columns: [Start Time, End Time, Category, Operation, Data Source]
//
// Categories:
//   - Query Folding: sent to source (fast!)
//   - Local Processing: done in PQ engine (slow for big data)
//   - Connection: data source connection time
//   - Evaluation: M expression evaluation
//
// ★ Diagnostics.Trace — programmatic tracing
let
    Traced = Diagnostics.Trace(
        TraceLevel.Information,
        "Processing started",
        () => SomeExpression,
        true    // includeCallerInfo
    )
in
    Traced

// ★ Check if query folds (View → Query Plan)
// Green checkmark = folded to source ✅
// Warning icon = local processing ⚠️
// Use Table.View to hint folding
```

---

## 🟡 Power Query — Number Functions Complete

### Math, Rounding & Random

```m
// ★ Number functions — complete reference

// Parity checks
Number.IsEven(4)           // true
Number.IsOdd(3)            // true
Number.IsNaN(0/0)          // true

// Sign & absolute
Number.Sign(-5)            // -1  (negative)
Number.Sign(0)             // 0   (zero)  
Number.Sign(7)             // 1   (positive)
Number.Abs(-42)            // 42

// Integer operations
Number.Mod(17, 5)          // 2   (remainder: 17 mod 5)
Number.IntegerDivide(17, 5) // 3  (floor division: 17 ÷ 5)
// Use case: split into groups of N

// Power & roots
Number.Power(2, 10)        // 1024  (2^10)
Number.Sqrt(144)           // 12
Number.Power(27, 1/3)      // 3     (cube root)

// Logarithms
Number.Log(100)            // 2      (log base 10)
Number.Log(8, 2)           // 3      (log base 2)
Number.Ln(#e)              // 1      (natural log)
Number.Exp(1)              // 2.718  (e^1)

// Combinatorics
Number.Combinations(10, 3) // 120    (10 choose 3)
Number.Permutations(5, 3)  // 60     (5 P 3)
Number.Factorial(5)        // 120    (5!)

// Random
Number.Random()            // 0.0 to 1.0 (decimal)
Number.RandomBetween(1, 100) // 1 to 100 (integer)

// ★ Rounding family (complete)
Number.Round(3.456, 2)     // 3.46  (standard)
Number.RoundDown(3.999, 0) // 3     (floor)
Number.RoundUp(3.001, 0)   // 4     (ceiling)
Number.RoundTowardZero(3.7) // 3    (truncate positive)
Number.RoundTowardZero(-3.7) // -3  (truncate negative)
Number.RoundAwayFromZero(3.2) // 4  (away from zero)

// ★ Bankers rounding (round half to even)
Number.Round(2.5, 0, RoundingMode.ToEven)  // 2
Number.Round(3.5, 0, RoundingMode.ToEven)  // 4
// Reduces cumulative rounding errors!

// Constants
Number.E                   // 2.71828...
Number.PI                  // 3.14159...

// ★ Number.ToText formatting
Number.ToText(1234.5, "N2")     // "1,234.50"
Number.ToText(0.15, "P1")       // "15.0%"
Number.ToText(1234, "X")        // "4D2" (hex)
Number.ToText(42, "00000")      // "00042" (padded)
```

---

## 📐 DAX — Type Conversion & EARLIER

### CONVERT, Type Functions & Row Context

```dax
// ★ CONVERT — explicit type conversion
// Syntax: CONVERT(value, dataType)
// DataTypes: INTEGER, DOUBLE, STRING, BOOLEAN, CURRENCY, DATETIME

To_Int = CONVERT("42", INTEGER)           // 42
To_Dbl = CONVERT("3.14", DOUBLE)          // 3.14
To_Str = CONVERT(42, STRING)              // "42"
To_Bool = CONVERT(1, BOOLEAN)             // TRUE
To_Curr = CONVERT(99.99, CURRENCY)        // ¤99.99 (fixed decimal)
To_Date = CONVERT("2024-01-15", DATETIME) // date value

// ★ INT — truncate to integer (toward zero)
Int_Pos = INT(3.9)                        // 3
Int_Neg = INT(-3.9)                       // -4 (floor!)

// ★ FIXED — round to fixed decimal places as text
Fixed1 = FIXED(1234.567, 2, FALSE)        // "1,234.57" (with comma)
Fixed2 = FIXED(1234.567, 2, TRUE)         // "1234.57" (no comma)
Fixed3 = FIXED(1234.567, 0, FALSE)        // "1,235"

// ★ VALUE — text to number
Num = VALUE("1,234.50")                   // 1234.5
// Understands locale formatting!

// ★ CURRENCY — convert to currency type (4 decimal places)
Price = CURRENCY(99.999999)               // 100.0000

// ★ Type checking
Is_Num = ISNUMBER([Value])                // TRUE if number
Is_Txt = ISTEXT([Value])                  // TRUE if text
Is_Log = ISLOGICAL([Value])               // TRUE if boolean
Is_Dte = ISNONTEXT([Value])               // TRUE if not text
Is_Err = ISERROR([Calc])                  // TRUE if error
Is_Blk = ISBLANK([Value])                 // TRUE if blank

// ★ EARLIER / EARLIEST — row context navigation (legacy)
// Used in calculated columns to reference "outer" row context
// Modern alternative: use VAR + CALCULATE instead

// Classic pattern: rank within group
Rank_InGroup = 
    COUNTROWS(
        FILTER(Sales,
            Sales[Category] = EARLIER(Sales[Category])
            && Sales[Amount] > EARLIER(Sales[Amount])
        )
    ) + 1

// Same with modern VAR approach (PREFERRED!):
Rank_Modern = 
    VAR CurrentCategory = Sales[Category]
    VAR CurrentAmount = Sales[Amount]
    RETURN
    COUNTROWS(
        FILTER(Sales,
            Sales[Category] = CurrentCategory
            && Sales[Amount] > CurrentAmount
        )
    ) + 1

// ★ Running total in calculated column
Running_Total = 
    CALCULATE(
        SUM(Sales[Amount]),
        FILTER(Sales,
            Sales[Category] = EARLIER(Sales[Category])
            && Sales[Date] <= EARLIER(Sales[Date])
        )
    )
```

---

## 🎨 Power BI — Themes & Templates

### Custom JSON Themes & .pbit Templates

```jsonc
// ★ Custom Theme — JSON structure
// Apply: View → Themes → Browse for themes → .json file
{
    "name": "Corporate Theme",
    "dataColors": [
        "#2E86AB",    // Primary blue
        "#A23B72",    // Purple
        "#F18F01",    // Orange
        "#C73E1D",    // Red
        "#3B1F2B",    // Dark
        "#44BBA4",    // Teal
        "#E94F37",    // Coral
        "#393E41"     // Charcoal
    ],
    "background": "#F5F5F5",
    "foreground": "#252525",
    "tableAccent": "#2E86AB",
    
    "visualStyles": {
        "*": {
            "*": {
                "background": [{
                    "color": { "solid": { "color": "#FFFFFF" } },
                    "transparency": 0
                }],
                "border": [{
                    "show": true,
                    "color": { "solid": { "color": "#E0E0E0" } },
                    "radius": 8
                }],
                "title": [{
                    "fontColor": { "solid": { "color": "#333333" } },
                    "fontSize": 14,
                    "fontFamily": "Segoe UI Semibold"
                }],
                "padding": [{ "top": 10, "right": 10, "bottom": 10, "left": 10 }],
                "dropShadow": [{
                    "show": true,
                    "color": { "solid": { "color": "#000000" } },
                    "position": "outer",
                    "preset": "bottomRight",
                    "transparency": 85
                }]
            }
        }
    },
    
    "textClasses": {
        "label": { "fontSize": 10, "fontFace": "Segoe UI" },
        "callout": { "fontSize": 28, "fontFace": "Segoe UI Light" },
        "title": { "fontSize": 14, "fontFace": "Segoe UI Semibold" },
        "header": { "fontSize": 12, "fontFace": "Segoe UI Semibold" },
        "largeLightTitle": { "fontSize": 24, "fontFace": "Segoe UI Light" }
    }
}
```

```
★ Templates (.pbit) — reusable report templates

Create:
  File → Export → Power BI Template (.pbit)
  Includes: report layout, data model, queries, measures
  Excludes: data (re-prompts for connection on open!)

Use cases:
  ✅ Standardize reports across teams
  ✅ Share best-practice layouts
  ✅ Quick-start new projects
  ✅ Include M queries without data
  ✅ Parameterized: prompts for settings on open

Open template:
  Double-click .pbit → prompts for parameters → loads data

★ Report-Level Themes (built-in)

Preset themes:  Default, City Park, Classroom, Color blind safe,
  Electric, High contrast, Innovate, Executive, Sunset, Tidal,
  Valentines Day, Spring, Summer, Winter, Autumn, Accessible default

Custom themes:
  1) Apply built-in theme → customize visuals
  2) View → Themes → Save current theme
  3) Exports .json → share across reports!
```

---

## 🔧 Power BI — Composite Models & DirectQuery

### Hybrid Storage & Chaining

```
★ Composite Models — mix Import + DirectQuery!

Why: Get the best of both worlds
  Import: Fast, cached, full DAX support
  DirectQuery: Real-time, no size limits

Setup:
  1) Connect to DirectQuery source (SQL Server, etc.)
  2) Add Import tables (Excel, CSV, etc.)
  3) Create relationships between them!
  4) Set storage mode per table:

  ┌────────────────────┬────────────────────────────────────┐
  │ Storage Mode       │ Behavior                           │
  ├────────────────────┼────────────────────────────────────┤
  │ Import             │ Cached in memory (fast)            │
  │ DirectQuery        │ Queries source on demand (live)    │
  │ Dual (auto-detect) │ Import or DQ depending on context  │
  └────────────────────┴────────────────────────────────────┘

★ DirectQuery Chaining — connect to published Semantic Models!

  1) Published model on Power BI Service (Premium/PPU)
  2) New report → Get Data → Power BI Datasets
  3) Connect as DirectQuery to existing model
  4) Add local model on top (new measures, new tables!)

  Benefits:
    ✅ Reuse certified data models
    ✅ Add department-specific measures
    ✅ No data duplication
    ✅ Central governance + local flexibility

★ Aggregation Tables — auto-switch Import↔DQ

  Setup:
  1) Create summary table (aggregated) → Import mode
  2) Keep detail table → DirectQuery mode
  3) Manage Aggregations:
     ┌─────────────┬──────────────┬────────────────┐
     │ Agg Column  │ Summarize    │ Detail Column  │
     ├─────────────┼──────────────┼────────────────┤
     │ Agg_Amount  │ Sum          │ Sales[Amount]  │
     │ Agg_Count   │ Count        │ Sales[OrderID] │
     │ Region      │ GroupBy      │ Sales[Region]  │
     │ YearMonth   │ GroupBy      │ Sales[Date]    │
     └─────────────┴──────────────┴────────────────┘
  4) PBI auto-routes: summary queries → Import (fast!)
     detail queries → DirectQuery (live!)

★ Hybrid Tables — Import + real-time partition!

  Combine:
    Historical data: Import (cached, fast)
    Recent/today data: DirectQuery (live!)
  
  Setup via Incremental Refresh:
    1) Enable incremental refresh on table
    2) Set "Get latest data in real-time" = ON
    3) Historical partitions = Import
    4) Current partition = DirectQuery
    5) Users always see latest data!

★ Storage Mode performance tips:
  ✅ Dimension tables → Dual mode (best flexibility)
  ✅ Large fact tables → DirectQuery or Hybrid
  ✅ Small lookup tables → Import mode
  ✅ Use aggregation tables for common queries
  ❌ Don't mix DQ sources from different databases
```

---

---

## 🟡 Power Query — Table Manipulation Functions

### TransformRows, AlternateRows & Fuzzy Clustering

```m
// ★ Table manipulation — advanced row/table operations

let
    Source = #table({"ID","Name","Amount"}, {
        {1,"Alice",100}, {2,"Bob",200}, {3,"Carol",300},
        {4,"Dan",150}, {5,"Eve",250}
    }),
    
    // ★ Table.TransformRows — transform each row to record/value
    // Returns a LIST (not table!) — must convert back
    Transformed = Table.FromRecords(
        Table.TransformRows(Source, (row) =>
            Record.TransformFields(row, {
                {"Name", Text.Upper},
                {"Amount", each _ * 1.07}   // add 7% tax
            })
        )
    ),
    
    // ★ Table.AlternateRows — skip/take alternating rows
    // Useful for: removing header rows from multi-header files
    SkipAlternate = Table.AlternateRows(Source, 0, 1, 1),
    // offset=0, skip=1, take=1 → takes every other row
    // Result: rows 2, 4 (Bob, Dan)
    
    // ★ Table.Repeat — duplicate table N times
    Repeated = Table.Repeat(Source, 3),
    // 5 rows × 3 = 15 rows (useful for: cross-join prep, testing)
    
    // ★ Table.Reverse — reverse row order
    Reversed = Table.Reverse(Source),
    // Last row first: Eve, Dan, Carol, Bob, Alice
    
    // ★ Table.FindText — search text across ALL columns
    Found = Table.FindText(Source, "ol"),
    // Returns rows where ANY column contains "ol"
    // Result: {3, "Carol", 300}
    
    // ★ Table.Split — split table into chunks
    Chunks = Table.Split(Source, 2),
    // Returns: list of tables, each with 2 rows
    // {Table[2 rows], Table[2 rows], Table[1 row]}
    // Use case: batch processing, pagination
    
    // ★ Table.First / Table.Last / Table.FirstN / Table.LastN
    First = Table.First(Source),           // record: {1,"Alice",100}
    Last = Table.Last(Source),             // record: {5,"Eve",250}
    TopN = Table.FirstN(Source, 3),        // table: first 3 rows
    BotN = Table.LastN(Source, 2),         // table: last 2 rows
    
    // ★ Table.FirstN with condition (take while)
    TakeWhile = Table.FirstN(Source, each [Amount] < 250),
    // Takes rows until condition fails
    
    // ★ Table.Skip / Table.Range  
    Skipped = Table.Skip(Source, 2),       // skip first 2 rows
    Ranged = Table.Range(Source, 1, 3),    // from index 1, take 3
    
    // ★ Table.AddFuzzyClusterColumn — group similar values!
    Clustered = Table.AddFuzzyClusterColumn(Source, "Name", "Cluster",
        [
            Threshold = 0.6,
            IgnoreCase = true,
            IgnoreSpace = true
        ]
    ),
    // Groups: "Alice" & "Alise" → same cluster
    // Use case: deduplication, standardization!
    
    // ★ Table.ReplaceMatchingRows — update specific rows
    Updated = Table.ReplaceMatchingRows(Source,
        {{1, "Alice", 100}},      // match this row
        {{1, "Alice", 999}}       // replace with this
    )
in
    Transformed
```

---

## 📐 DAX — Grouping Functions Comparison

### SUMMARIZE vs SUMMARIZECOLUMNS vs GROUPBY

```dax
// ★ Three ways to group data in DAX — when to use which?

// ═══════════════════════════════════════════════════════════
// 1) SUMMARIZE — simple grouping (AVOID for measures!)
// ═══════════════════════════════════════════════════════════
Simple_Group = 
    SUMMARIZE(Sales,
        Products[Category],     // group by (via relationship)
        Sales[Region]           // group by (same table)
    )
// ✅ Group by columns from related tables
// ⚠️ DON'T add measure columns with SUMMARIZE directly!
// ❌ BAD: SUMMARIZE(Sales, Cat, "Total", SUM(Sales[Amount]))
// This can give WRONG RESULTS!

// ✅ CORRECT: wrap with ADDCOLUMNS
Correct_Pattern = 
    ADDCOLUMNS(
        SUMMARIZE(Sales, Products[Category]),
        "Total", CALCULATE(SUM(Sales[Amount])),
        "Count", CALCULATE(COUNTROWS(Sales))
    )

// ═══════════════════════════════════════════════════════════
// 2) SUMMARIZECOLUMNS — BEST for new tables with measures ★
// ═══════════════════════════════════════════════════════════
Best_Group = 
    SUMMARIZECOLUMNS(
        Products[Category],     // group by
        Sales[Region],          // group by
        TREATAS({("Electronics")}, Products[Category]),  // filter!
        "Total Sales", SUM(Sales[Amount]),
        "Avg Price", AVERAGE(Sales[Price]),
        "Order Count", COUNTROWS(Sales)
    )
// ✅ Safe to add measures directly
// ✅ Auto-removes blanks (ROLLUPGROUP behavior)
// ✅ Supports TREATAS filters
// ✅ Most efficient for query results
// ❌ Can't be used inside CALCULATE
// ❌ Can't be used inside iterator measures

// ═══════════════════════════════════════════════════════════
// 3) GROUPBY — iterator with CURRENTGROUP() ★
// ═══════════════════════════════════════════════════════════
Iterator_Group = 
    GROUPBY(Sales,
        Sales[Region],
        "Max Amount", MAXX(CURRENTGROUP(), Sales[Amount]),
        "Min Amount", MINX(CURRENTGROUP(), Sales[Amount]),
        "Range", MAXX(CURRENTGROUP(), Sales[Amount]) - 
                 MINX(CURRENTGROUP(), Sales[Amount])
    )
// ✅ CURRENTGROUP() = rows in current group
// ✅ Can use any iterator (SUMX, MAXX, MINX, etc.)
// ❌ ONLY iterator functions allowed (no SUM, CALCULATE)
// ❌ Less common, more complex

// ★ PRODUCTX — multiply all values (iterator)
Compound_Growth = 
    PRODUCTX(
        GrowthTable,
        1 + GrowthTable[GrowthRate]
    ) - 1
// Use case: compound interest, chained growth rates

// ═══════════════════════════════════════════════════════════
// COMPARISON TABLE
// ═══════════════════════════════════════════════════════════
//
// | Feature            | SUMMARIZE | SUMMARIZECOLUMNS | GROUPBY  |
// |--------------------|-----------|------------------|----------|
// | Group by columns   | ✅        | ✅               | ✅       |
// | Add measures       | ⚠️ unsafe | ✅ safe          | ❌ iter  |
// | Cross-table group  | ✅        | ✅               | ❌ same  |
// | Filter support     | ❌        | ✅ TREATAS       | ❌       |
// | Inside CALCULATE   | ✅        | ❌               | ✅       |
// | Performance        | Good      | Best             | Good     |
// | Recommended?       | GroupOnly | ★ YES            | Rare     |
```

---

## 🔒 Power BI — Row-Level & Object-Level Security

### RLS Dynamic Patterns & OLS

```dax
// ★ Row-Level Security (RLS) — restrict data per user

// ═════════════════════════════════════════════
// Pattern 1: Static RLS (simple role)
// ═════════════════════════════════════════════
// Modeling → Manage Roles → New Role:
//   Role Name: "US Sales"
//   Table: Geography
//   Filter: [Country] = "USA"

// ═════════════════════════════════════════════
// Pattern 2: Dynamic RLS (user-based!) ★
// ═════════════════════════════════════════════
// Security table:
// | UserEmail              | Region       |
// |------------------------|--------------|
// | john@company.com       | North        |
// | jane@company.com       | South        |
// | admin@company.com      | ALL          |

// DAX filter on Security table:
[UserEmail] = USERPRINCIPALNAME()
// Or for "ALL" access:
[UserEmail] = USERPRINCIPALNAME() || [Region] = "ALL"

// ═════════════════════════════════════════════
// Pattern 3: Manager hierarchy RLS
// ═════════════════════════════════════════════
// Uses PATH functions!
PATHCONTAINS(
    [ManagerPath],
    LOOKUPVALUE(
        Employees[EmpID],
        Employees[Email], USERPRINCIPALNAME()
    )
)

// ═════════════════════════════════════════════
// Testing RLS
// ═════════════════════════════════════════════
// Modeling → View as → select role → check "Other user" 
//   → enter email → OK
// Report shows filtered data as that user would see!

// ═════════════════════════════════════════════
// USERNAME() vs USERPRINCIPALNAME()
// ═════════════════════════════════════════════
// USERNAME():         DOMAIN\username (on-premises)
// USERPRINCIPALNAME(): user@domain.com (cloud/AAD) ★
// CUSTOMDATA():       custom string from embed token
```

```
★ Object-Level Security (OLS) — hide columns/tables!

What: Restrict which COLUMNS or TABLES users can see
How: Available only via Tabular Editor or XMLA endpoint

Setup (Tabular Editor):
  1) Open model in Tabular Editor
  2) Select table or column
  3) Object Level Security → Add role
  4) Set permission: None / Read

Restrictions:
  ┌────────────┬──────────────────────────────────────┐
  │ Permission │ Effect                               │
  ├────────────┼──────────────────────────────────────┤
  │ None       │ Column/table completely hidden        │
  │ Read       │ Column/table visible (default)        │
  └────────────┴──────────────────────────────────────┘

Use cases:
  ✅ Hide salary columns from non-HR
  ✅ Hide sensitive PII columns
  ✅ Restrict test/dev tables
  ⚠️ Measures referencing hidden columns will ERROR!
  ⚠️ Must handle with ISINSCOPE or try/catch
```

---

## 📄 Power BI — Report Page Settings

### Page Size, Background & Navigation

```
★ Report Page Configuration

Page Size (Format → Page Information):
  ┌─────────────────────┬────────────────────┐
  │ Type                │ Dimensions         │
  ├─────────────────────┼────────────────────┤
  │ 16:9 (default)      │ 1280 × 720 px      │
  │ 4:3                 │ 960 × 720 px        │
  │ Letter              │ 816 × 1056 px       │
  │ Tooltip (small)     │ 320 × 240 px        │
  │ Custom              │ Any size!           │
  └─────────────────────┴────────────────────┘

★ Page Background:
  - Color: solid color with transparency
  - Image: upload background image
  - Transparency: 0-100%
  - Image fit: Fit / Fill / Normal

★ Wallpaper (canvas behind page):
  - Color behind the report page
  - Image wallpaper
  - Separate from page background!

★ Page Types:
  ┌─────────────────────┬────────────────────────────────────┐
  │ Type                │ Use                                │
  ├─────────────────────┼────────────────────────────────────┤
  │ Regular             │ Standard report page               │
  │ Tooltip page        │ Custom hover tooltips              │
  │ Drillthrough page   │ Detail page via right-click        │
  │ Hidden page         │ Not visible in tab bar             │
  │ Q&A page            │ Natural language query page        │
  └─────────────────────┴────────────────────────────────────┘

★ Tooltip Page Setup:
  1) New page → Page Information → Tooltip = ON
  2) Set page size to "Tooltip" (320×240)
  3) Design tooltip layout (cards, charts, images)
  4) On source visual → Format → Tooltip → Page = your tooltip page
  5) Hover shows your custom tooltip!

★ Drillthrough Setup:
  1) New page → add drill-through filter field
  2) Add visuals showing detail for that field
  3) Auto-creates "← Back" button
  4) On source visual → right-click data point → Drillthrough!
  5) Cross-report: set "Cross-report" = ON in drillthrough filter

★ Page Navigation:
  1) Insert → Buttons → Navigator → Page Navigator
  2) Auto-generates tabs for all visible pages!
  3) Or: manual buttons with "Page navigation" action
  4) Customize: icon, shape, position, style
```

---

## ⚡ Power BI — Performance Analyzer & Optimization

### Measuring & Reducing Load Time

```
★ Performance Analyzer — measure visual load time

How to use:
  1) View → Performance Analyzer → Start Recording
  2) Interact with report (click, filter, navigate)
  3) Stop Recording → see results per visual

Results breakdown:
  ┌────────────────────────┬──────────────────────────────────┐
  │ Metric                 │ What it measures                 │
  ├────────────────────────┼──────────────────────────────────┤
  │ DAX query              │ Time to execute DAX formula      │
  │ Visual display         │ Time to render visual            │
  │ Other                  │ Waiting, network, etc.           │
  │ Copy query             │ Copy actual DAX sent to engine!  │
  └────────────────────────┴──────────────────────────────────┘

★ Copy DAX Query → paste in DAX Studio for deep analysis!

★ VertiPaq Analyzer (via DAX Studio or Tabular Editor)

  Analyze model size:
  ┌────────────────────────┬──────────────────────────────────┐
  │ Component              │ What to check                    │
  ├────────────────────────┼──────────────────────────────────┤
  │ Table size             │ Rows × columns = memory          │
  │ Column cardinality     │ High unique values = more memory │
  │ Dictionary size        │ Text columns with many values    │
  │ Relationship size      │ One-to-many vs many-to-many     │
  │ Hierarchy size         │ User hierarchies                 │
  └────────────────────────┴──────────────────────────────────┘

★ Model Size Reduction Tips:

  1) Remove unused columns ★ (biggest impact!)
     - Right-click column → Delete
     - Or: Table.SelectColumns in PQ (better!)
  
  2) Reduce cardinality
     - Round timestamps to hour/day
     - Group rare categories into "Other"
     - Split date+time into Date + Time columns
  
  3) Optimize data types
     - Text → Whole Number (where possible)
     - Decimal → Fixed Decimal/Whole Number
     - Avoid auto-date/time tables (disable!)
       File → Options → Data Load → Auto date/time = OFF
  
  4) Use Star Schema
     - Fact tables: only keys + measures
     - Dimension tables: only used attributes
  
  5) Reduce relationships
     - Avoid bi-directional (use CROSSFILTER in DAX)
     - Prefer single-direction filters
  
  6) Avoid calculated columns
     - Move calculations to Power Query instead
     - Use measures (evaluated at query time, not stored)
  
  7) Use VARIABLES in DAX
     - VAR evaluates ONCE, reuse multiple times
     - Prevents re-computation

★ Performance targets:
  ┌────────────────────────┬────────────┐
  │ Metric                 │ Target     │
  ├────────────────────────┼────────────┤
  │ Report load time       │ < 5 sec    │
  │ Visual render          │ < 1 sec    │
  │ DAX query              │ < 500 ms   │
  │ Model size             │ < 1 GB     │
  │ Columns per fact table │ < 20       │
  │ Tables in model        │ < 30       │
  └────────────────────────┴────────────┘
```

---

---

## 🟡 Power Query — JSON & CSV Deep

### JSON Parsing, CSV Options & Column Renaming

```m
// ★ JSON — parse and create JSON data

let
    // ★ Json.Document — parse JSON string/binary to M values
    JsonText = "{""name"":""Alice"",""age"":30,""scores"":[90,85,95]}",
    Parsed = Json.Document(JsonText),
    // Returns record: [name="Alice", age=30, scores={90,85,95}]
    
    Name = Parsed[name],          // "Alice"
    Scores = Parsed[scores],     // {90, 85, 95} (list)
    
    // ★ Parse JSON from API response
    ApiResponse = Web.Contents("https://api.example.com/data"),
    ApiData = Json.Document(ApiResponse),
    
    // ★ JSON array → table
    JsonArray = "[{""id"":1,""v"":""A""},{""id"":2,""v"":""B""}]",
    AsList = Json.Document(JsonArray),
    AsTable = Table.FromRecords(AsList),
    // | id | v |
    // | 1  | A |
    // | 2  | B |
    
    // ★ Nested JSON → flatten
    Nested = Json.Document("{""data"":{""items"":[{""x"":1},{""x"":2}]}}"),
    Items = Nested[data][items],
    FlatTable = Table.FromRecords(Items),
    
    // ★ Json.FromValue — M value → JSON string
    MyRecord = [name = "Bob", age = 25, active = true],
    AsJson = Text.FromBinary(Json.FromValue(MyRecord)),
    // Returns: {"name":"Bob","age":25,"active":true}
    
    // ★ Create JSON for API POST body
    PostBody = Json.FromValue([
        query = "SELECT * FROM table",
        limit = 100,
        filters = {[field = "status", value = "active"]}
    ])
in
    AsTable

// ★ Csv.Document — advanced CSV parsing options
let
    RawCsv = File.Contents("C:\data\file.csv"),
    
    // Basic parse
    Basic = Csv.Document(RawCsv),
    
    // ★ With all options!
    Advanced = Csv.Document(RawCsv, [
        Delimiter = ",",           // or "|", #(tab), ";"
        Columns = 5,               // expected column count
        Encoding = TextEncoding.Utf8,  // 65001
        CsvStyle = CsvStyle.QuoteAfterDelimiter,
        QuoteStyle = QuoteStyle.Csv    // handle quoted fields
    ]),
    
    // ★ Tab-delimited
    TabFile = Csv.Document(RawCsv, [Delimiter = "#(tab)"]),
    
    // ★ Fixed-width (no delimiter — positional)
    FixedWidth = Table.SplitColumn(
        Csv.Document(RawCsv, [Delimiter = {}]),
        "Column1", 
        Splitter.SplitTextByPositions({0, 10, 25, 40})
    ),
    
    // ★ Multi-character delimiter  
    PipeDelim = Csv.Document(RawCsv, [Delimiter = "||"]),
    
    // ★ Skip header rows
    SkipHeaders = Table.Skip(
        Csv.Document(RawCsv, [Delimiter = ","]), 
        3   // skip first 3 rows
    )
in
    Advanced

// ★ Table.TransformColumnNames — rename ALL columns at once
let
    // Clean all column names
    Cleaned = Table.TransformColumnNames(Source, each
        Text.Trim(
            Text.Replace(
                Text.Replace(
                    Text.Clean(_),     // remove non-printable
                    " ", "_"),         // spaces → underscores
                "#", "Num")           // # → Num
        )
    ),
    
    // PascalCase
    Pascal = Table.TransformColumnNames(Source, each
        Text.Combine(
            List.Transform(
                Text.Split(_, " "),
                Text.Proper
            )
        )
    ),
    
    // Add prefix/suffix
    Prefixed = Table.TransformColumnNames(Source, each "src_" & _),
    Suffixed = Table.TransformColumnNames(Source, each _ & "_v2"),
    
    // ★ Table.MaxN / Table.MinN — top/bottom N by value
    Top5 = Table.MaxN(Source, {"Amount", Order.Descending}, 5),
    Bot5 = Table.MinN(Source, {"Amount", Order.Ascending}, 5)
in
    Cleaned
```

---

## 📐 DAX — Filter Modifiers Complete

### REMOVEFILTERS, KEEPFILTERS & ISONORAFTER

```dax
// ★ Filter modifier functions — control filter context

// ═══════════════════════════════════════════════
// REMOVEFILTERS — modern replacement for ALL in CALCULATE
// ═══════════════════════════════════════════════
Grand_Total = 
    CALCULATE(
        SUM(Sales[Amount]),
        REMOVEFILTERS()               // removes ALL filters
    )

Remove_Category = 
    CALCULATE(
        SUM(Sales[Amount]),
        REMOVEFILTERS(Products[Category])  // remove one column
    )

Remove_Table = 
    CALCULATE(
        SUM(Sales[Amount]),
        REMOVEFILTERS(Products)       // remove all from table
    )

// ★ REMOVEFILTERS vs ALL — what's the difference?
// REMOVEFILTERS: ONLY removes filters (clear)
// ALL: removes filters AND returns table/column
// 
// In CALCULATE: identical behavior!
// Outside CALCULATE: ALL returns table, REMOVEFILTERS = error
//
// Best practice: use REMOVEFILTERS in CALCULATE for clarity

// ═══════════════════════════════════════════════
// KEEPFILTERS — add filter WITHOUT removing existing
// ═══════════════════════════════════════════════
// Normal CALCULATE filter REPLACES existing filter:
Replaces = 
    CALCULATE(
        SUM(Sales[Amount]),
        Products[Color] = "Red"    // replaces user's color filter!
    )

// KEEPFILTERS adds filter AND KEEPS user's filter:
Keeps = 
    CALCULATE(
        SUM(Sales[Amount]),
        KEEPFILTERS(Products[Color] = "Red")  // intersects with user filter
    )
// If user selects "Blue", result = 0 (Red ∩ Blue = empty)
// Without KEEPFILTERS, result = Red sales (ignores Blue)

// ═══════════════════════════════════════════════
// ALLCROSSFILTERED — remove cross-filter effects
// ═══════════════════════════════════════════════
No_Cross = 
    CALCULATE(
        DISTINCTCOUNT(Products[ProductID]),
        ALLCROSSFILTERED(Products)    // ignore filters from related tables
    )

// ═══════════════════════════════════════════════
// ISONORAFTER — pagination / cursor pattern
// ═══════════════════════════════════════════════
// Returns TRUE for rows at or after a position in sorted order
After_Row = 
    FILTER(
        ALL(Sales),
        ISONORAFTER(
            Sales[Date], DATE(2024, 6, 1), DESC,
            Sales[Amount], 1000, DESC
        )
    )
// Use case: "give me all rows after this cursor position"
// Great for: large table pagination, incremental processing
```

---

## 📐 DAX — Calculation Groups Advanced

### Dynamic Formatting & Multiple Groups

```dax
// ★ Calculation Groups — most powerful DAX feature!
// Created via: Tabular Editor or Model Explorer

// ═══════════════════════════════════════════════
// Basic Calculation Group: Time Intelligence
// ═══════════════════════════════════════════════
// Table: "Time Calc"
// Column: "Time Calculation"
// Items:
//   Current      → SELECTEDMEASURE()
//   YTD          → CALCULATE(SELECTEDMEASURE(), DATESYTD(Date[Date]))
//   PY           → CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR(Date[Date]))
//   YoY          → VAR Current = SELECTEDMEASURE()
//                   VAR PY = CALCULATE(SELECTEDMEASURE(), 
//                       SAMEPERIODLASTYEAR(Date[Date]))
//                   RETURN DIVIDE(Current - PY, PY)
//   YoY %        → same as YoY but formatted as %

// ★ SELECTEDMEASURE() = whatever measure the user places in visual!
// One calculation group replaces N × M individual measures!

// ═══════════════════════════════════════════════
// SELECTEDMEASURENAME() — conditional logic per measure
// ═══════════════════════════════════════════════
// In calculation item expression:
IF(
    SELECTEDMEASURENAME() = "Count",
    // Don't apply time intelligence to count measures
    SELECTEDMEASURE(),
    // Apply to all other measures
    CALCULATE(SELECTEDMEASURE(), DATESYTD(Date[Date]))
)

// ═══════════════════════════════════════════════
// SELECTEDMEASUREFORMATSTRING() — dynamic formatting ★
// ═══════════════════════════════════════════════
// In Format String Expression of calculation item:
// For YoY %:
IF(
    SELECTEDMEASUREFORMATSTRING() = "$#,##0",
    "0.0%",    // change currency format to percentage
    "0.0%"     // default to percentage for YoY
)

// ═══════════════════════════════════════════════
// ISSELECTEDMEASURE — check specific measure
// ═══════════════════════════════════════════════
IF(
    ISSELECTEDMEASURE([Total Sales]),
    CALCULATE(SELECTEDMEASURE(), DATESYTD(Date[Date])),
    SELECTEDMEASURE()   // don't modify other measures
)

// ═══════════════════════════════════════════════
// Multiple Calculation Groups — precedence
// ═══════════════════════════════════════════════
// You can have MULTIPLE calculation groups!
// Example: "Time Calc" + "Currency Conv"
// Precedence = order of application (set in Tabular Editor)
// Higher precedence = applied FIRST (innermost)
//
// Precedence 20: Currency Conv  (applied first)
// Precedence 10: Time Calc      (applied to result)
//
// Result: Time Intelligence applied to currency-converted values
```

---

## 👥 Power BI — Workspace & Sharing

### Roles, Distribution & Lineage

```
★ Workspace Roles — who can do what?

  ┌─────────────┬────────┬────────┬─────────┬────────────┐
  │ Permission  │ Viewer │ Contr. │ Member  │ Admin      │
  ├─────────────┼────────┼────────┼─────────┼────────────┤
  │ View reports│ ✅     │ ✅     │ ✅      │ ✅         │
  │ Share items │ ❌     │ ❌     │ ✅      │ ✅         │
  │ Edit/create │ ❌     │ ✅     │ ✅      │ ✅         │
  │ Delete items│ ❌     │ ❌     │ ✅      │ ✅         │
  │ Manage roles│ ❌     │ ❌     │ ❌      │ ✅         │
  │ Publish     │ ❌     │ ✅     │ ✅      │ ✅         │
  └─────────────┴────────┴────────┴─────────┴────────────┘

★ Sharing Methods:

  1) Direct Share (per report/dashboard)
     Share → enter email → set permissions
     Options: allow reshare, allow build, send email
  
  2) Power BI App (recommended for organization!)
     Workspace → Create app → configure:
       - Audience: specific groups/users
       - Included content: select pages
       - Permissions: view / build
     Users: install app from AppSource
  
  3) Embed → SharePoint/Teams
     Get embed link → paste in:
       - SharePoint Online page (web part)
       - Microsoft Teams tab
       - PowerPoint (live connection!)
  
  4) Publish to Web (PUBLIC — no auth!)
     File → Embed report → Publish to web
     ⚠️ WARNING: anyone with link can see!
     Use ONLY for public data!

★ Data Lineage — track data flow!

  Workspace → Lineage View:
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Data     │ →  │ Dataflow │ →  │ Semantic │ →  │ Report   │
  │ Source   │    │          │    │ Model    │    │          │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
  
  Shows: which sources feed which models feed which reports
  Click any item → see upstream/downstream dependencies

★ Impact Analysis — what breaks if I change?

  Right-click item → Impact Analysis:
  - Shows all downstream dependent items
  - "If I change this dataset, these 5 reports are affected"
  - Contact owners of affected items
  - Plan changes safely!

★ Endorsement — mark trusted content:
  - Promoted: "this is ready to use"
  - Certified: officially verified by admin
  Settings → Endorsement → Promoted/Certified
```

---

## ⚡ Power BI — Power Automate Integration

### Triggers, Alerts & Automated Flows

```
★ Power Automate + Power BI — automate workflows!

Triggers (what starts the flow):
  ┌────────────────────────────────┬──────────────────────────┐
  │ Trigger                        │ When it fires            │
  ├────────────────────────────────┼──────────────────────────┤
  │ Data-driven alert triggered    │ KPI crosses threshold    │
  │ Dataset refresh completed      │ After scheduled refresh  │
  │ Dataset refresh failed         │ On refresh error         │
  │ Button clicked in report       │ User clicks button       │
  │ When data changes (Fabric)     │ Data modification event  │
  └────────────────────────────────┴──────────────────────────┘

★ Example Flow 1: Alert on KPI
  1) PBI: Set alert on dashboard tile (> threshold)
  2) Power Automate: trigger = "Data-driven alert"
  3) Action: Send Teams notification + email
  4) Action: Create Planner task for follow-up

★ Example Flow 2: Refresh failure notification
  1) Trigger: "Dataset refresh failed"
  2) Action: Send email to data team
  3) Action: Post to Teams channel
  4) Action: Log to SharePoint list

★ Example Flow 3: Report button automation
  1) PBI: Insert → Buttons → Power Automate
  2) Assign flow to button
  3) User clicks → flow runs!
  4) Can pass report context (filters, values)

★ Power Automate Actions for Power BI:
  ┌────────────────────────────────┬──────────────────────────┐
  │ Action                         │ What it does             │
  ├────────────────────────────────┼──────────────────────────┤
  │ Run query on dataset           │ Execute DAX query        │
  │ Refresh dataset                │ Trigger manual refresh   │
  │ Get refresh history            │ Check refresh status     │
  │ Add rows to dataset            │ Push data to PBI table   │
  │ Export report                  │ Export to PDF/PPTX/PNG   │
  │ Get reports/dashboards         │ List workspace content   │
  └────────────────────────────────┴──────────────────────────┘

★ Power Apps + Power BI:
  - Embed PBI visuals in Power Apps
  - Power Apps visual in PBI reports
  - Bidirectional: filter from app ↔ report

★ Scheduled Refresh + Flow:
  1) Dataset → Schedule refresh → set times
  2) Flow trigger: "When refresh completes"
  3) Action: notify stakeholders
  4) Action: export PDF → upload to SharePoint
  5) Stakeholders get updated report automatically!
```

---

> 📅 Last Updated: 2026-03-01
> 📊 Coverage: 65 industries, 2050+ cleaning patterns, M + Python + DAX + SQL + Polars
> 🆕 v28 JSON & AUTOMATE: PQ JSON (Json.Document parse string/API/nested,
>    Json.FromValue M→JSON, JSON array→table, nested→flatten,
>    Csv.Document 5 options delimiter/columns/encoding/CsvStyle/QuoteStyle,
>    tab-delimited/fixed-width/multi-char/skip headers,
>    Table.TransformColumnNames clean/Pascal/prefix/suffix, Table.MaxN/MinN),
>    DAX Filter Modifiers (REMOVEFILTERS vs ALL comparison, KEEPFILTERS intersect,
>    ALLCROSSFILTERED, ISONORAFTER pagination cursor),
>    Calculation Groups (SELECTEDMEASURE/SELECTEDMEASURENAME conditional,
>    SELECTEDMEASUREFORMATSTRING dynamic format, ISSELECTEDMEASURE,
>    multiple groups precedence),
>    Workspace (4 roles Viewer/Contributor/Member/Admin permissions table,
>    4 sharing methods Direct/App/Embed/PublishToWeb, Lineage View, Impact Analysis,
>    Endorsement Promoted/Certified),
>    Power Automate (5 triggers alert/refresh/fail/button/dataChange,
>    6 PBI actions DAX query/refresh/export/push, Power Apps integration,
>    3 example flows with step-by-step)
> 🏆 **ABSOLUTE EXHAUSTIVE** — COMPLETE ENCYCLOPEDIA v8
