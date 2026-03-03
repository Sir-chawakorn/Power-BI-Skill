<p align="center">
  <img src="https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/PBIP-Format-purple?style=for-the-badge" alt="PBIP"/>
  <img src="https://img.shields.io/badge/AI%20Powered-🤖-blue?style=for-the-badge" alt="AI Powered"/>
</p>

<h1 align="center">⚡ Power BI PBIP Automation Skill</h1>

<p align="center">
  <b>สร้าง Power BI Dashboard อัตโนมัติด้วย Python + PBIP Format</b><br/>
  <i>Generate complete Power BI dashboards from CSV data — no GUI required</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Visuals-14%20Types-brightgreen?style=flat-square" alt="14 Visual Types"/>
  <img src="https://img.shields.io/badge/Data%20Cleaning-57%2B%20Techniques-blue?style=flat-square" alt="57+ Cleaning"/>
  <img src="https://img.shields.io/badge/Error%20Reference-1620%2B%20Errors-red?style=flat-square" alt="1620+ Errors"/>
  <img src="https://img.shields.io/badge/Tests-90%2F98%20Passing-success?style=flat-square" alt="Tests"/>
  <img src="https://img.shields.io/badge/Industries-65%2B-orange?style=flat-square" alt="65+ Industries"/>
</p>

---

## 🚀 What is this?

A **comprehensive AI-powered skill** that automates the entire Power BI dashboard creation pipeline:

```
📄 CSV Data → 🧹 Auto Clean → 🏗️ Data Model → 📊 Dashboard → ✅ Validate → 📁 PBIP Project
```

Simply provide your CSV files and let the system:
1. **Analyze** your data structure automatically
2. **Clean** messy data with 57+ techniques
3. **Generate** a complete PBIP project (report.json + model.bim)
4. **Validate** and auto-fix common issues
5. **Output** a ready-to-open Power BI project

> 💡 **No Power BI Desktop needed** for generation — only for viewing the final result!

---

## 📦 What's Inside

| File | Size | Description |
|------|------|-------------|
| 📘 [`SKILL.md`](SKILL.md) | 371 KB | Complete technical reference — PBIP format, JSON structures, visual types, Interactive Wizard guide |
| 🐍 [`generate.py`](generate.py) | 526 KB | Main engine — 14 visual generators, 57+ data cleaning, auto-validation, M expression builder |
| 🧪 [`test_generate.py`](test_generate.py) | 44 KB | 98 automated tests covering visuals, utilities, cleaning, and validation |
| 🧹 [`DATA_CLEANING.md`](DATA_CLEANING.md) | 723 KB | **Encyclopedia** — 65 industries, 2050+ cleaning patterns, M + Python + DAX + SQL + Polars |
| 🔴 [`ERROR_REFERENCE.md`](ERROR_REFERENCE.md) | 312 KB | **Error Bible** — 1,620+ errors across 230 categories with solutions |
| 📋 [`USE_CASES.md`](USE_CASES.md) | 38 KB | 15 industries, 25+ dashboard blueprints, 100+ KPIs with DAX formulas |

---

## ✨ Key Features

### 📊 14 Visual Generators

<table>
<tr>
<td>

**Charts**
- 📈 Line Chart
- 📊 Bar / Column (Clustered & Stacked)
- 🥧 Pie & Donut
- 🌊 Area Chart
- 🔀 Combo Chart
- 🌳 Treemap
- 💧 Waterfall
- 📉 Scatter Plot

</td>
<td>

**Cards & Tables**
- 🔢 KPI Card
- 📋 Table
- 📐 Matrix (Pivot)
- 🎯 Gauge
- 🎚️ Slicer
- 📝 Text Box

</td>
</tr>
</table>

### 🧹 57+ Data Cleaning Techniques (3 Phases)

<details>
<summary><b>Phase 1: Base Cleaning (15 techniques)</b></summary>

| Technique | What it does |
|-----------|-------------|
| Remove Duplicates | Deduplicate rows |
| Trim Whitespace | Strip leading/trailing spaces |
| Standardize Nulls | Convert "N/A", "null", "-" → empty |
| Fix Currency | Remove $, ¥, €, ฿ symbols from numbers |
| Fix Dates | Parse 50+ date formats → ISO 8601 |
| Boolean Standardization | yes/no/true/false → TRUE/FALSE |
| Remove BOM | Strip byte-order marks |
| Normalize Unicode | NFC/NFKC normalization |
| *...and 7 more* | |

</details>

<details>
<summary><b>Phase 2: Advanced Cleaning (20 techniques)</b></summary>

| Technique | What it does |
|-----------|-------------|
| Remove Emoji | Strip all emoji characters |
| Fix Mojibake | Repair encoding corruption (Ã©→é) |
| Mask PII | Replace SSN/credit cards with ████ |
| Fuzzy Dedup | Merge near-duplicate rows (Levenshtein) |
| Normalize Phone | +66-81-234-5678 format |
| Fix GPS Coordinates | Validate lat/lng ranges |
| *...and 14 more* | |

</details>

<details>
<summary><b>Phase 3: Messy Data Handling (22 techniques)</b></summary>

| Technique | What it does |
|-----------|-------------|
| Fix Column Count | Pad/trim rows to match headers |
| Split Multi-value | "red;blue;green" → 3 rows |
| Extract Numbers | "weighs 2.5 kg" → 2.5 |
| Strip Honorifics | "Dr. Jane Smith" → "Jane Smith" |
| Standardize Gender | Female/F/female/♀ → F |
| Convert Units | kg→lbs, km→miles |
| Parse Durations | "2h30m" → 150 (minutes) |
| Smart Dedup | Merge partial duplicates |
| *...and 14 more* | |

</details>

### ✅ Auto-Validation & Fix

The engine validates **230+ rule categories** across:

| Category | Checks | Auto-Fix |
|----------|--------|----------|
| 📁 Structure | Missing files, encoding, names | ✅ Most |
| 📊 Model | Tables, columns, M expressions, relationships | ✅ Many |
| 🎨 Visuals | Projections, configs, queries | ✅ Partial |
| 🔗 References | Column mismatches, missing tables | ✅ Some |

---

## 🛠️ Quick Start

### Prerequisites

- **Python 3.8+**
- **Power BI Desktop** (for viewing results)
  - Enable: `Options > Preview Features > Power BI Project (.pbip)`

### Basic Usage

```python
import sys
sys.path.insert(0, r'path/to/Power-BI-Skill')
from generate import generate_pbip, validate_and_fix

# 1. Define your tables from CSV
tables = [
    {
        'name': 'Sales',
        'csv_path': r'C:\data\sales.csv',
        'columns': ['Date', 'Product', 'Revenue', 'Quantity'],
    }
]

# 2. Generate PBIP project
generate_pbip(
    project_name='SalesDashboard',
    output_dir=r'C:\output',
    tables=tables,
    pages=[{
        'name': 'Overview',
        'visuals': [
            {'type': 'card', 'table': 'Sales', 'measure': 'Revenue'},
            {'type': 'lineChart', 'table': 'Sales', 'category': 'Date', 'value': 'Revenue'},
        ]
    }]
)

# 3. Validate & auto-fix
result = validate_and_fix(r'C:\output\SalesDashboard')
print(f"Errors: {result['errors']}, Fixed: {result['fixed']}")
```

### Data Cleaning

```python
from generate import clean_csv

# Clean a messy CSV with all techniques
output_path, report = clean_csv(
    r'C:\data\messy_data.csv',
    config={
        'remove_duplicates': True,
        'fix_dates': True,
        'fix_currency': True,
        'remove_emoji': True,
        'strip_honorifics': True,
        'standardize_gender': True,
    }
)

print(f"Cleaned: {report['rows_before']}→{report['rows_after']} rows")
```

---

## 🧙‍♂️ Interactive Wizard

When used as an **AI Skill** (e.g., with Antigravity IDE), the system guides users through a step-by-step wizard:

```
Step 1: 🎯 What do you want?       → Create / Edit / Clean / Validate
Step 2: 📊 Data source?            → CSV / Excel / Database / Generate sample
Step 3: 📈 Dashboard type?         → Executive / Analytical / KPI / Geographic
Step 4: 📄 How many pages?         → 1 (Simple) to 6+ (Enterprise)
Step 5: 🧹 Clean data?             → Auto-clean all / Pick specific / Skip
Step 6: 🎨 Theme?                  → Dark / Light / Corporate / Colorful
Step 7: ✅ Confirm & Build!
```

> Each option includes **detailed explanations** so users understand exactly what they're choosing.

---

## 📚 Documentation

| Guide | Best For |
|-------|----------|
| 📘 [**SKILL.md**](SKILL.md) | Building dashboards — PBIP format reference, JSON schemas, visual configs |
| 🧹 [**DATA_CLEANING.md**](DATA_CLEANING.md) | Cleaning data — 65 industry-specific patterns, M/Python/DAX/SQL recipes |
| 🔴 [**ERROR_REFERENCE.md**](ERROR_REFERENCE.md) | Troubleshooting — 1,620+ error solutions organized by category |
| 📋 [**USE_CASES.md**](USE_CASES.md) | Finding inspiration — 15 industries, 25+ dashboard blueprints |

---

## 🧪 Testing

```bash
# Run all tests
python test_generate.py

# Results: 90/98 passed (8 = pre-existing visual type mismatches)
```

| Test Category | Count | Status |
|---------------|-------|--------|
| Visual Generation | 56 | ✅ 48 pass |
| Utilities | 8 | ✅ All pass |
| JSON Serialization | 4 | ✅ All pass |
| Data Cleaning (Phase 1) | 15 | ✅ All pass |
| Data Cleaning (Phase 2) | 12 | ✅ All pass |
| Data Cleaning (Phase 3) | 15 | ✅ All pass |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    generate.py                       │
├──────────┬──────────┬──────────┬────────────────────┤
│ 📊 Visual │ 🧹 Data   │ ✅ Valid- │ 🏗️ PBIP           │
│ Generators│ Cleaning  │ ation    │ Builder           │
│          │          │          │                    │
│ 14 types │ 57+ tech │ 230+     │ report.json       │
│ make_*() │ clean_csv│ rules    │ model.bim         │
│          │          │          │ M expressions     │
└──────────┴──────────┴──────────┴────────────────────┘
```

---

## 📊 Supported Industries

<details>
<summary><b>Click to see all 15 industries with dashboard blueprints</b></summary>

| # | Industry | Dashboards | KPIs |
|---|----------|-----------|------|
| 1 | 🛒 Retail & E-commerce | Sales, Inventory, Customer | Revenue, AOV, CAC |
| 2 | 🏥 Healthcare | Patient, Clinical, Financial | Wait time, Readmission |
| 3 | 🏦 Banking & Finance | Risk, Portfolio, Fraud | NPL, ROE, CAR |
| 4 | 🏭 Manufacturing | Production, Quality, Supply | OEE, Defect rate |
| 5 | 🎓 Education | Enrollment, Performance | GPA, Dropout rate |
| 6 | 🏨 Hospitality | Occupancy, Revenue, Guest | RevPAR, ADR |
| 7 | 🚛 Logistics | Fleet, Delivery, Warehouse | On-time %, Cost/mile |
| 8 | 📱 Telecom | Network, Subscriber, Churn | ARPU, Churn rate |
| 9 | ⚡ Energy & Utilities | Consumption, Grid, Billing | Peak demand, Outages |
| 10 | 🏗️ Real Estate | Property, Lease, Maintenance | Occupancy, NOI |
| 11 | 🎯 Marketing | Campaign, Digital, Brand | CTR, ROAS, NPS |
| 12 | 👥 Human Resources | Workforce, Recruitment | Turnover, Time-to-hire |
| 13 | 🌾 Agriculture | Crop, Weather, Supply Chain | Yield/hectare |
| 14 | 🎮 Gaming | Player, Revenue, Engagement | DAU, ARPDAU |
| 15 | 🏛️ Government | Budget, Service, Compliance | Response time |

</details>

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  <b>Built with ❤️ by <a href="https://github.com/Sir-chawakorn">Sir-chawakorn</a></b><br/>
  <i>Powered by AI 🤖 • Made for Power BI 📊</i>
</p>
