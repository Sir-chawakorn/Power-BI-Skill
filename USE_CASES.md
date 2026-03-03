# Power BI Use Cases Reference — 10 Industries

> Real-world dashboard blueprints: KPIs, columns, visuals, DAX, layout

---

## 📑 Table of Contents

1. [Retail / E-Commerce](#1-retail--e-commerce)
2. [Healthcare / Hospital](#2-healthcare--hospital)
3. [Manufacturing / Supply Chain](#3-manufacturing--supply-chain)
4. [Finance / Accounting](#4-finance--accounting)
5. [Banking / Financial Services](#5-banking--financial-services)
6. [Human Resources (HR)](#6-human-resources-hr)
7. [Marketing / Digital Campaigns](#7-marketing--digital-campaigns)
8. [Education](#8-education)
9. [SaaS / Software](#9-saas--software)
10. [Real Estate / Property](#10-real-estate--property)
11. [Logistics / Transportation](#11-logistics--transportation)
12. [Project Management](#12-project-management)
13. [Customer Service / Support](#13-customer-service--support)
14. [Energy / Utilities](#14-energy--utilities)
15. [Agriculture / Farming](#15-agriculture--farming)

---

## 1. Retail / E-Commerce

### 1A. Sales Performance Dashboard

**KPIs (Cards)**:
| KPI | Column | Aggregation | DAX |
|-----|--------|-------------|-----|
| Total Revenue | sales_amount | Sum | `SUM('Orders'[sales_amount])` |
| Total Orders | order_id | DistinctCount | `DISTINCTCOUNT('Orders'[order_id])` |
| Average Order Value | sales_amount | Average | `DIVIDE([Total Revenue], [Total Orders])` |
| Total Items Sold | quantity | Sum | `SUM('Orders'[quantity])` |

**Columns Needed**:
```
order_id, order_date, customer_id, product_name, product_category,
quantity, unit_price, sales_amount, discount, store_id, city, state
```

**Visuals**:
| Visual | visualType | Category | Y | Purpose |
|--------|-----------|----------|---|---------|
| Revenue Trend | `lineChart` | order_date (Month) | Sum(sales_amount) | แนวโน้มรายเดือน |
| Sales by Category | `clusteredBarChart` | product_category | Sum(sales_amount) | เปรียบเทียบหมวด |
| Sales by City | `clusteredBarChart` | city | Sum(sales_amount) | เปรียบเทียบเมือง |
| Top 10 Products | `tableEx` | product_name, Sum(quantity), Sum(sales_amount) | — | รายละเอียด |
| Category Share | `donutChart` | product_category | Sum(sales_amount) | สัดส่วน |
| Sales Slicer | `slicer` | product_category | — | Filter |

**Layout**: Cards (row 1) → Line + Bar (row 2) → Table + Donut (row 3)

---

### 1B. Customer Analytics Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Customers | `DISTINCTCOUNT('Orders'[customer_id])` |
| Repeat Rate | `DIVIDE(COUNTROWS(FILTER(VALUES('Orders'[customer_id]), CALCULATE(COUNT('Orders'[order_id]))>1)), DISTINCTCOUNT('Orders'[customer_id]))` |
| Avg Orders/Customer | `DIVIDE([Total Orders], [Total Customers])` |
| Customer Lifetime Value | `DIVIDE([Total Revenue], [Total Customers])` |

**Columns Needed**:
```
customer_id, customer_name, registration_date, order_date,
sales_amount, city, state, customer_segment, source_channel
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Customer Growth | `areaChart` | ลูกค้าใหม่ตามเวลา |
| Segment Distribution | `donutChart` | แบ่งกลุ่มลูกค้า |
| Revenue by Segment | `clusteredColumnChart` | มูลค่าแต่ละกลุ่ม |
| Top Customers | `tableEx` | Top spenders |
| Customer Map | `map` (if geo) | กระจายตัวทางภูมิศาสตร์ |
| New vs Returning | `stackedColumnChart` | เปรียบเทียบ |

---

### 1C. Inventory Management Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Stock | `SUM('Inventory'[stock_qty])` |
| Low Stock Items | `COUNTROWS(FILTER('Inventory', 'Inventory'[stock_qty] < 'Inventory'[reorder_level]))` |
| Stockout Items | `COUNTROWS(FILTER('Inventory', 'Inventory'[stock_qty] = 0))` |
| Inventory Value | `SUMX('Inventory', 'Inventory'[stock_qty] * 'Inventory'[unit_cost])` |

**Columns Needed**:
```
product_id, product_name, category, stock_qty, reorder_level,
reorder_qty, unit_cost, warehouse_id, supplier_id, last_restock_date
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Stock by Category | `treemap` | ภาพรวม stock |
| Low Stock Alert | `tableEx` (conditional red) | แจ้งเตือน |
| Stock Level Gauge | `gauge` | ระดับ stock ปัจจุบัน |
| Restock Timeline | `lineChart` | แนวโน้ม restock |
| Warehouse Comparison | `clusteredBarChart` | เปรียบเทียบคลัง |

---

### 1D. Profitability Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Gross Profit | `[Total Revenue] - SUM('Orders'[cost])` |
| Gross Margin % | `DIVIDE([Gross Profit], [Total Revenue])` |
| Net Profit | `[Gross Profit] - SUM('Expenses'[amount])` |
| Discount Impact | `SUM('Orders'[discount_amount])` |

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| P&L Waterfall | `waterfallChart` | Revenue → Cost → Expenses → Profit |
| Margin by Product | `clusteredBarChart` | Profit margin per product |
| Margin Trend | `lineChart` | Margin % over time |
| Profit vs Revenue Combo | `lineStackedColumnComboChart` | Revenue (bar) + Margin (line) |

---

## 2. Healthcare / Hospital

### 2A. Hospital Operations Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Patients | `DISTINCTCOUNT('Patients'[patient_id])` |
| Bed Occupancy Rate | `DIVIDE(SUM('Beds'[occupied]), SUM('Beds'[total]))` |
| Avg Length of Stay | `AVERAGE('Admissions'[length_of_stay_days])` |
| Readmission Rate | `DIVIDE(COUNTROWS(FILTER('Admissions', 'Admissions'[is_readmission]="Yes")), COUNTROWS('Admissions'))` |

**Columns Needed**:
```
patient_id, admission_date, discharge_date, department, ward,
bed_id, diagnosis, doctor_id, length_of_stay_days, is_readmission,
is_emergency, insurance_type
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Admissions Trend | `lineChart` | ผู้ป่วยรายเดือน |
| Department Distribution | `donutChart` | สัดส่วนแผนก |
| Bed Occupancy Gauge | `gauge` | อัตราครอบครองเตียง |
| Wait Times by Dept | `clusteredBarChart` | เวลารอคอย |
| Patient Demographics | `stackedColumnChart` | อายุ/เพศ |
| Top Diagnoses | `tableEx` | การวินิจฉัยบ่อย |

---

### 2B. Patient Outcomes Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Recovery Rate | `DIVIDE(COUNTROWS(FILTER('Patients', 'Patients'[outcome]="Recovered")), COUNTROWS('Patients'))` |
| Mortality Rate | `DIVIDE(COUNTROWS(FILTER('Patients', 'Patients'[outcome]="Deceased")), COUNTROWS('Patients'))` |
| Patient Satisfaction | `AVERAGE('Surveys'[satisfaction_score])` |
| Infection Rate | `DIVIDE(COUNTROWS(FILTER('Patients', 'Patients'[hospital_infection]="Yes")), COUNTROWS('Patients'))` |

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Outcomes by Department | `stackedBarChart` | เปรียบเทียบผลลัพธ์ |
| Satisfaction Trend | `lineChart` | แนวโน้มความพอใจ |
| Infection Gauge | `gauge` | อัตราติดเชื้อ |
| Readmission Causes | `funnelChart` | เหตุผล readmission |

---

## 3. Manufacturing / Supply Chain

### 3A. Production Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Output | `SUM('Production'[units_produced])` |
| Defect Rate | `DIVIDE(SUM('Production'[defect_units]), SUM('Production'[units_produced]))` |
| OEE (Overall Equipment Effectiveness) | `[Availability] * [Performance] * [Quality]` |
| Downtime Hours | `SUM('Production'[downtime_hours])` |

**Columns Needed**:
```
production_date, product_id, machine_id, shift, units_produced,
defect_units, downtime_hours, planned_output, cycle_time,
operator_id, raw_material_used
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Output Trend | `lineChart` | ผลผลิตรายวัน |
| OEE Gauge | `gauge` | ประสิทธิภาพรวม |
| Defect by Machine | `clusteredBarChart` | เครื่องจักรปัญหา |
| Downtime Analysis | `waterfallChart` | สาเหตุ downtime |
| Shift Comparison | `stackedColumnChart` | เปรียบเทียบกะ |
| Production Table | `tableEx` | รายละเอียด |

---

### 3B. Supply Chain Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| On-Time Delivery % | `DIVIDE(COUNTROWS(FILTER('Shipments', 'Shipments'[on_time]="Yes")), COUNTROWS('Shipments'))` |
| Avg Lead Time | `AVERAGE('Orders'[lead_time_days])` |
| Inventory Turnover | `DIVIDE(SUM('Sales'[cost_of_goods]), AVERAGE('Inventory'[avg_value]))` |
| Supplier Reliability | `AVERAGE('Suppliers'[reliability_score])` |

**Columns Needed**:
```
order_date, delivery_date, supplier_id, supplier_name, product_id,
quantity_ordered, quantity_received, lead_time_days, on_time,
defect_rate, shipping_cost, warehouse_id
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Delivery Performance | `gauge` | On-time rate |
| Lead Time Trend | `lineChart` | แนวโน้ม lead time |
| Supplier Ranking | `clusteredBarChart` | เปรียบเทียบ suppliers |
| Cost by Route | `treemap` | ต้นทุนขนส่ง |
| Shipment Timeline | `lineChart` | ปริมาณส่งของ |
| Supplier Detail | `tableEx` | ข้อมูล supplier |

---

## 4. Finance / Accounting

### 4A. Financial Overview Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Revenue | `SUM('GL'[credit_amount])` |
| Total Expenses | `SUM('GL'[debit_amount])` |
| Net Income | `[Total Revenue] - [Total Expenses]` |
| Profit Margin % | `DIVIDE([Net Income], [Total Revenue])` |

**Columns Needed**:
```
transaction_date, account_code, account_name, account_type,
debit_amount, credit_amount, department, cost_center, description
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Revenue vs Expense Trend | `lineStackedColumnComboChart` | Revenue (bar) + Expense (line) |
| P&L Waterfall | `waterfallChart` | รายรับ → รายจ่าย → กำไร |
| Expense by Category | `donutChart` | สัดส่วนค่าใช้จ่าย |
| Budget vs Actual | `clusteredColumnChart` | เปรียบเทียบงบ |
| Monthly Detail | `tableEx` | รายเดือนละเอียด |
| Cash Flow | `areaChart` | กระแสเงินสด |

---

### 4B. Accounts Receivable Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Receivable | `SUM('AR'[invoice_amount]) - SUM('AR'[paid_amount])` |
| Overdue Amount | `CALCULATE([Total Receivable], 'AR'[due_date] < TODAY())` |
| Days Sales Outstanding | `DIVIDE([Total Receivable], [Avg Daily Sales])` |
| Collection Rate | `DIVIDE(SUM('AR'[paid_amount]), SUM('AR'[invoice_amount]))` |

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Aging Buckets | `stackedBarChart` | 0-30, 31-60, 61-90, 90+ days |
| Top Debtors | `tableEx` | ลูกหนี้สูงสุด |
| Collection Trend | `lineChart` | แนวโน้มเก็บเงิน |
| Overdue Gauge | `gauge` | สัดส่วน overdue |

---

## 5. Banking / Financial Services

### 5A. Loan Portfolio Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Loans | `SUM('Loans'[loan_amount])` |
| Active Loans | `COUNTROWS(FILTER('Loans', 'Loans'[status]="Active"))` |
| NPL Ratio (Non-Performing) | `DIVIDE(CALCULATE(SUM('Loans'[loan_amount]), 'Loans'[days_overdue]>90), [Total Loans])` |
| Avg Interest Rate | `AVERAGE('Loans'[interest_rate])` |

**Columns Needed**:
```
loan_id, customer_id, loan_type, loan_amount, interest_rate,
disbursement_date, maturity_date, monthly_payment, outstanding_balance,
days_overdue, status, collateral_type, branch_id
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Loan Distribution | `donutChart` | สัดส่วนตามประเภท |
| NPL Trend | `lineChart` | แนวโน้ม NPL |
| Portfolio by Branch | `clusteredBarChart` | เปรียบเทียบสาขา |
| Risk Gauge | `gauge` | ระดับความเสี่ยง |
| Maturity Schedule | `stackedColumnChart` | กำหนดครบสัญญา |
| Loan Detail | `tableEx` | รายละเอียดสินเชื่อ |

---

### 5B. Fraud Detection Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Transactions | `COUNTROWS('Transactions')` |
| Suspicious Transactions | `COUNTROWS(FILTER('Transactions', 'Transactions'[risk_score]>80))` |
| Fraud Rate | `DIVIDE([Suspicious], [Total Transactions])` |
| Blocked Amount | `CALCULATE(SUM('Transactions'[amount]), 'Transactions'[blocked]="Yes")` |

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Fraud Trend | `lineChart` | แนวโน้มรายวัน |
| Risk Distribution | `clusteredColumnChart` | กระจายตัว risk score |
| Fraud by Type | `donutChart` | ประเภทการฉ้อโกง |
| Alert Table | `tableEx` (conditional red) | transactions สงสัย |
| Fraud Gauge | `gauge` | อัตราฉ้อโกงปัจจุบัน |

---

## 6. Human Resources (HR)

### 6A. Workforce Overview Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Employees | `COUNTROWS('Employees')` |
| Turnover Rate | `DIVIDE(COUNTROWS(FILTER('Employees', 'Employees'[status]="Resigned" && YEAR('Employees'[resign_date])=YEAR(TODAY()))), [Total Employees])` |
| Avg Tenure (Years) | `AVERAGE('Employees'[tenure_years])` |
| Avg Salary | `AVERAGE('Employees'[salary])` |

**Columns Needed**:
```
employee_id, employee_name, department, position, hire_date,
resign_date, status, salary, gender, age, education_level,
performance_score, manager_id, location
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Headcount by Dept | `clusteredBarChart` | จำนวนตามแผนก |
| Gender Distribution | `donutChart` | สัดส่วนเพศ |
| Age Distribution | `clusteredColumnChart` | กระจายตัวอายุ |
| Hiring Trend | `lineChart` | แนวโน้มรับพนักงาน |
| Turnover by Dept | `clusteredBarChart` | อัตราลาออกตามแผนก |
| Employee Detail | `tableEx` | รายละเอียด |

---

### 6B. Recruitment Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Open Positions | `COUNTROWS(FILTER('Jobs', 'Jobs'[status]="Open"))` |
| Time to Hire (Days) | `AVERAGE('Jobs'[days_to_fill])` |
| Offer Acceptance Rate | `DIVIDE(COUNTROWS(FILTER('Jobs', 'Jobs'[offer_accepted]="Yes")), COUNTROWS(FILTER('Jobs', 'Jobs'[offer_made]="Yes")))` |
| Cost per Hire | `DIVIDE(SUM('Recruitment'[cost]), [Total Hires])` |

**Columns Needed**:
```
job_id, job_title, department, posted_date, filled_date,
days_to_fill, source_channel, applicants_count, interviews_count,
offers_made, offer_accepted, cost, recruiter_id
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Hiring Funnel | `funnelChart` | Applicants → Interview → Offer → Hire |
| Source Effectiveness | `clusteredBarChart` | ช่องทางสรรหา |
| Time to Hire Trend | `lineChart` | แนวโน้มเวลาสรรหา |
| Open Positions | `tableEx` | ตำแหน่งว่าง |
| Dept Hiring Status | `stackedBarChart` | สถานะตามแผนก |

---

### 6C. Performance & Compensation Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Avg Performance Score | `AVERAGE('Employees'[performance_score])` |
| High Performers | `COUNTROWS(FILTER('Employees', 'Employees'[performance_score]>=4))` |
| Total Payroll | `SUM('Employees'[salary])` |
| Pay Equity Ratio | `DIVIDE(CALCULATE(AVERAGE('Employees'[salary]), 'Employees'[gender]="Female"), CALCULATE(AVERAGE('Employees'[salary]), 'Employees'[gender]="Male"))` |

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Score Distribution | `clusteredColumnChart` | กระจายตัวคะแนน |
| Salary vs Performance | `scatterChart` | ความสัมพันธ์ |
| Performance by Dept | `clusteredBarChart` | เปรียบเทียบแผนก |
| Compensation Trend | `lineChart` | แนวโน้มเงินเดือน |
| Performance Gauge | `gauge` | คะแนนเฉลี่ย vs เป้า |

---

## 7. Marketing / Digital Campaigns

### 7A. Campaign Performance Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Impressions | `SUM('Campaigns'[impressions])` |
| Total Clicks | `SUM('Campaigns'[clicks])` |
| CTR (Click-Through Rate) | `DIVIDE([Total Clicks], [Total Impressions])` |
| ROAS (Return on Ad Spend) | `DIVIDE(SUM('Campaigns'[revenue]), SUM('Campaigns'[spend]))` |
| Cost per Acquisition | `DIVIDE(SUM('Campaigns'[spend]), SUM('Campaigns'[conversions]))` |

**Columns Needed**:
```
campaign_id, campaign_name, channel, start_date, end_date,
impressions, clicks, conversions, spend, revenue, target_audience
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Channel Performance | `clusteredBarChart` | เปรียบเทียบช่องทาง |
| Spend vs Revenue | `lineStackedColumnComboChart` | Spend (bar) + Revenue (line) |
| CTR Trend | `lineChart` | แนวโน้ม CTR |
| Campaign Funnel | `funnelChart` | Impressions → Clicks → Conversions |
| Campaign Detail | `tableEx` | ทุก campaign |
| Channel Share | `donutChart` | สัดส่วนงบ |

---

### 7B. Social Media Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Followers | `SUM('Social'[followers])` |
| Engagement Rate | `DIVIDE(SUM('Social'[engagements]), SUM('Social'[impressions]))` |
| Total Posts | `COUNTROWS('Posts')` |
| Avg Likes per Post | `AVERAGE('Posts'[likes])` |

**Columns Needed**:
```
post_date, platform, content_type, likes, shares, comments,
impressions, engagements, followers, reach, url
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Engagement Trend | `lineChart` | แนวโน้ม engagement |
| Platform Comparison | `clusteredBarChart` | เปรียบเทียบ platform |
| Content Type Performance | `donutChart` | สุดส่วนตาม content type |
| Top Posts | `tableEx` | โพสต์ยอดนิยม |
| Follower Growth | `areaChart` | การเติบโต followers |

---

## 8. Education

### 8A. Student Performance Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Students | `DISTINCTCOUNT('Students'[student_id])` |
| Avg GPA | `AVERAGE('Students'[gpa])` |
| Pass Rate | `DIVIDE(COUNTROWS(FILTER('Grades', 'Grades'[grade]>="C")), COUNTROWS('Grades'))` |
| Attendance Rate | `DIVIDE(SUM('Attendance'[days_present]), SUM('Attendance'[total_days]))` |

**Columns Needed**:
```
student_id, student_name, grade_level, subject, score, grade,
semester, teacher_id, department, attendance_days, total_days,
gpa, scholarship, enrollment_date
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| GPA Distribution | `clusteredColumnChart` | กระจายตัว GPA |
| Score by Subject | `clusteredBarChart` | คะแนนตามวิชา |
| Pass/Fail Trend | `stackedColumnChart` | แนวโน้ม pass/fail |
| Attendance Gauge | `gauge` | อัตราเข้าเรียน |
| At-Risk Students | `tableEx` (conditional red) | นักเรียนเสี่ยง |
| Department Compare | `clusteredBarChart` | เปรียบเทียบแผนก |

---

### 8B. Enrollment & Finance Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Enrollment | `COUNTROWS('Students')` |
| New Students | `CALCULATE(COUNTROWS('Students'), 'Students'[is_new]="Yes")` |
| Revenue (Tuition) | `SUM('Fees'[amount_paid])` |
| Outstanding Fees | `SUM('Fees'[amount_due]) - SUM('Fees'[amount_paid])` |

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Enrollment Trend | `lineChart` | แนวโน้มรับสมัคร |
| Program Distribution | `treemap` | สัดส่วนตามสาขา |
| Fee Collection | `gauge` | อัตราเก็บค่าธรรมเนียม |
| Revenue by Program | `clusteredBarChart` | รายได้ตามหลักสูตร |

---

## 9. SaaS / Software

### 9A. SaaS Metrics Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| MRR (Monthly Recurring Revenue) | `SUM('Subscriptions'[monthly_amount])` |
| ARR (Annual) | `[MRR] * 12` |
| Churn Rate | `DIVIDE(COUNTROWS(FILTER('Subscriptions', 'Subscriptions'[canceled_this_month]="Yes")), COUNTROWS('Subscriptions'))` |
| ARPU (Avg Revenue Per User) | `DIVIDE([MRR], DISTINCTCOUNT('Subscriptions'[customer_id]))` |
| LTV (Lifetime Value) | `DIVIDE([ARPU], [Churn Rate])` |
| CAC (Customer Acquisition Cost) | `DIVIDE(SUM('Marketing'[spend]), [New Customers])` |

**Columns Needed**:
```
customer_id, subscription_start, subscription_end, plan_name,
monthly_amount, status, canceled_this_month, payment_method,
signup_source, usage_hours, feature_used, support_tickets
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| MRR Trend | `lineChart` | แนวโน้ม MRR |
| Churn Gauge | `gauge` | อัตราลูกค้าหาย |
| Plan Distribution | `donutChart` | สัดส่วนตาม plan |
| LTV/CAC Ratio | `card` | Health indicator |
| Revenue by Plan | `stackedAreaChart` | รายได้แต่ละ plan |
| Customer Table | `tableEx` | รายละเอียดลูกค้า |
| Expansion Revenue | `waterfallChart` | New + Upgrade - Churn |

---

### 9B. Product Usage Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Daily Active Users (DAU) | `DISTINCTCOUNT('Events'[user_id])` |
| Feature Adoption | `DIVIDE(COUNTROWS(FILTER('Events', 'Events'[feature]="NewFeature")), DISTINCTCOUNT('Events'[user_id]))` |
| Avg Session Duration | `AVERAGE('Sessions'[duration_minutes])` |
| Support Tickets | `COUNTROWS('Tickets')` |

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| DAU Trend | `areaChart` | แนวโน้ม users |
| Feature Usage | `clusteredBarChart` | features ที่ใช้ |
| Session Duration Distribution | `clusteredColumnChart` | กระจายตัวเวลาใช้ |
| Ticket by Category | `donutChart` | ประเภท support |

---

## 10. Real Estate / Property

### 10A. Property Portfolio Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Properties | `COUNTROWS('Properties')` |
| Total Market Value | `SUM('Properties'[market_value])` |
| Occupancy Rate | `DIVIDE(COUNTROWS(FILTER('Properties', 'Properties'[status]="Occupied")), COUNTROWS('Properties'))` |
| Monthly Rental Income | `SUM('Properties'[monthly_rent])` |
| Yield % | `DIVIDE([Annual Rental] * 12, [Total Market Value])` |

**Columns Needed**:
```
property_id, property_name, property_type, location, area_sqm,
market_value, monthly_rent, purchase_price, purchase_date,
status, tenant_name, lease_start, lease_end, expense_monthly
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Portfolio by Type | `donutChart` | สัดส่วนตามประเภท |
| Value by Location | `treemap` | มูลค่าตามทำเล |
| Rental Income Trend | `lineChart` | แนวโน้มรายได้ |
| Occupancy Gauge | `gauge` | อัตราครอบครอง |
| Property Detail | `tableEx` | รายละเอียด |
| Income vs Expense | `lineStackedColumnComboChart` | รายรับ-จ่าย |

---

### 10B. Sales Performance Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Properties Sold | `COUNTROWS(FILTER('Sales', 'Sales'[status]="Sold"))` |
| Total Sales Value | `SUM('Sales'[sale_price])` |
| Avg Days on Market | `AVERAGE('Sales'[days_on_market])` |
| Price per Sqm | `DIVIDE([Total Sales Value], SUM('Sales'[area_sqm]))` |

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Sales Trend | `lineChart` | แนวโน้มการขาย |
| Price by Location | `clusteredBarChart` | ราคาตามทำเล |
| Sales Funnel | `funnelChart` | Listed → Viewed → Offered → Sold |
| Days on Market Gauge | `gauge` | ระยะเวลาขาย |

---

## 11. Logistics / Transportation

### 11A. Fleet & Delivery Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Deliveries | `COUNTROWS('Deliveries')` |
| On-Time Delivery % | `DIVIDE(COUNTROWS(FILTER('Deliveries', 'Deliveries'[ontime]="Yes")), COUNTROWS('Deliveries'))` |
| Avg Delivery Time (hrs) | `AVERAGE('Deliveries'[delivery_hours])` |
| Total Distance (km) | `SUM('Deliveries'[distance_km])` |
| Cost per Delivery | `DIVIDE(SUM('Deliveries'[cost]), COUNTROWS('Deliveries'))` |

**Columns Needed**:
```
delivery_id, order_id, driver_id, vehicle_id, origin, destination,
distance_km, delivery_hours, planned_date, actual_date,
ontime, cost, fuel_cost, status
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Delivery Performance | `gauge` | On-time rate |
| Volume Trend | `areaChart` | ปริมาณจัดส่ง |
| Route Costs | `clusteredBarChart` | ต้นทุนตามเส้นทาง |
| Driver Performance | `tableEx` | ประสิทธิภาพผู้ขับ |
| Late Delivery Analysis | `waterfallChart` | สาเหตุส่งช้า |

---

## 12. Project Management

### 12A. Project Tracking Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Active Projects | `COUNTROWS(FILTER('Projects', 'Projects'[status]="Active"))` |
| On-Track Projects | `COUNTROWS(FILTER('Projects', 'Projects'[health]="On Track"))` |
| Budget Utilization | `DIVIDE(SUM('Projects'[actual_cost]), SUM('Projects'[budget]))` |
| Avg Completion % | `AVERAGE('Projects'[completion_pct])` |

**Columns Needed**:
```
project_id, project_name, department, manager, start_date,
end_date, budget, actual_cost, status, health, completion_pct,
tasks_total, tasks_completed, risk_level
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Status Distribution | `donutChart` | สัดส่วนสถานะ |
| Budget vs Actual | `clusteredColumnChart` | เปรียบเทียบงบ |
| Timeline | `lineChart` | แนวโน้ม completion |
| Risk Matrix | `scatterChart` (risk vs impact) | ความเสี่ยง |
| Project Detail | `tableEx` | รายละเอียด |
| Completion Gauge | `gauge` | ความคืบหน้ารวม |

---

## 13. Customer Service / Support

### 13A. Support Ticket Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Tickets | `COUNTROWS('Tickets')` |
| Open Tickets | `COUNTROWS(FILTER('Tickets', 'Tickets'[status]="Open"))` |
| Avg Resolution Time (hrs) | `AVERAGE('Tickets'[resolution_hours])` |
| First Response Time | `AVERAGE('Tickets'[first_response_minutes])` |
| CSAT Score | `AVERAGE('Tickets'[satisfaction_score])` |
| Escalation Rate | `DIVIDE(COUNTROWS(FILTER('Tickets', 'Tickets'[escalated]="Yes")), COUNTROWS('Tickets'))` |

**Columns Needed**:
```
ticket_id, created_date, resolved_date, customer_id, agent_id,
category, priority, status, resolution_hours, first_response_minutes,
satisfaction_score, escalated, channel
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Ticket Trend | `lineChart` | ปริมาณ ticket ตามวัน |
| Category Distribution | `donutChart` | ประเภทปัญหา |
| Priority Breakdown | `stackedBarChart` | High/Medium/Low |
| Agent Performance | `tableEx` | ประสิทธิภาพเจ้าหน้าที่ |
| Resolution Time Gauge | `gauge` | เวลาแก้ปัญหา vs SLA |
| CSAT Trend | `lineChart` | แนวโน้มความพอใจ |

---

## 14. Energy / Utilities

### 14A. Energy Consumption Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Consumption (kWh) | `SUM('Meters'[consumption_kwh])` |
| Total Cost | `SUM('Meters'[cost])` |
| Cost per kWh | `DIVIDE([Total Cost], [Total Consumption])` |
| Peak Demand (kW) | `MAX('Meters'[peak_demand_kw])` |
| Carbon Emissions (tons) | `SUM('Meters'[consumption_kwh]) * 0.0004` |

**Columns Needed**:
```
meter_id, reading_date, building, zone, consumption_kwh,
cost, peak_demand_kw, meter_type, tariff_rate
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Consumption Trend | `areaChart` | แนวโน้มการใช้ |
| Cost by Building | `clusteredBarChart` | ต้นทุนตามอาคาร |
| Peak Demand | `lineChart` | ช่วงพีค |
| Consumption Breakdown | `treemap` | สัดส่วนตามโซน |
| Cost Gauge | `gauge` | ค่าใช้จ่าย vs งบ |

---

## 15. Agriculture / Farming

### 15A. Farm Performance Dashboard

**KPIs (Cards)**:
| KPI | DAX |
|-----|-----|
| Total Harvest (kg) | `SUM('Harvest'[quantity_kg])` |
| Revenue | `SUM('Harvest'[revenue])` |
| Yield per Hectare | `DIVIDE(SUM('Harvest'[quantity_kg]), SUM('Plots'[area_hectare]))` |
| Cost per kg | `DIVIDE(SUM('Costs'[amount]), SUM('Harvest'[quantity_kg]))` |

**Columns Needed**:
```
plot_id, crop_type, plant_date, harvest_date, area_hectare,
quantity_kg, revenue, input_cost, labor_cost, weather_condition
```

**Visuals**:
| Visual | visualType | Purpose |
|--------|-----------|---------|
| Yield by Crop | `clusteredBarChart` | ผลผลิตตามพืช |
| Harvest Trend | `lineChart` | แนวโน้มเก็บเกี่ยว |
| Cost Breakdown | `donutChart` | สัดส่วนต้นทุน |
| Revenue vs Cost | `lineStackedColumnComboChart` | รายรับ-จ่าย |
| Plot Detail | `tableEx` | รายละเอียดแปลง |
| Yield Gauge | `gauge` | ผลผลิตต่อไร่ |

---

## 🔧 How to Use These Blueprints

1. **Identify your industry** from the list above
2. **Match your columns** with the "Columns Needed" section
3. **Copy the KPI formulas** — use DAX for calculated measures
4. **Pick visuals** from the Visual table — the `visualType` maps directly to Power BI
5. **Follow the Layout** pattern: Cards → Charts → Tables

> 💡 **Pro Tip**: Combine multiple use cases for cross-functional dashboards!

---

## 📊 Quick Lookup: ข้อมูลลักษณะไหน → ใช้ visual อะไร

| ลักษณะข้อมูลที่มี | Recommended Visual | visualType |
|-------------------|-------------------|-----------|
| 1 ตัวเลข summary | Card | `card` |
| ตัวเลข vs เป้าหมาย | Gauge | `gauge` |
| หมวดหมู่ vs ตัวเลข (≤10 หมวด) | Bar Chart | `clusteredBarChart` |
| หมวดหมู่ vs ตัวเลข (>10 หมวด) | Bar (horizontal) | `clusteredBarChart` |
| เวลา vs ตัวเลข | Line Chart | `lineChart` |
| เวลา vs 2 ตัวเลข | Combo Chart | `lineStackedColumnComboChart` |
| สัดส่วน (≤5 กลุ่ม) | Donut/Pie | `donutChart` |
| สัดส่วน (>5 กลุ่ม) | Treemap | `treemap` |
| Funnel/Pipeline | Funnel | `funnelChart` |
| ความสัมพันธ์ 2 ตัวแปร | Scatter | `scatterChart` |
| P&L / Waterfall | Waterfall | `waterfallChart` |
| อันดับเปลี่ยนตามเวลา | Ribbon | `ribbonChart` |
| สะสม/Cumulative | Area | `areaChart` |
| หมวด + กลุ่มย่อย | Stacked Bar | `stackedBarChart` |
| ข้อมูลหลาย column | Table | `tableEx` |
| ข้อมูล pivot (row×col) | Matrix | `pivotTable` |
| กรอง/Filter | Slicer | `slicer` |

---

## 📐 Universal DAX Templates

> สูตร DAX ใช้ได้ทุก industry — copy & ปรับชื่อ table/column

### Time Intelligence

| Pattern | DAX |
|---------|-----|
| **YoY Growth %** | `DIVIDE([Current Year] - [Previous Year], [Previous Year])` |
| **Previous Year** | `CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Date'[Date]))` |
| **YTD** | `TOTALYTD([Total Revenue], 'Date'[Date])` |
| **QTD** | `TOTALQTD([Total Revenue], 'Date'[Date])` |
| **MTD** | `TOTALMTD([Total Revenue], 'Date'[Date])` |
| **MoM Growth %** | `VAR _curr = [Total Revenue] VAR _prev = CALCULATE([Total Revenue], DATEADD('Date'[Date], -1, MONTH)) RETURN DIVIDE(_curr - _prev, _prev)` |
| **QoQ Growth %** | `VAR _curr = [Total Revenue] VAR _prev = CALCULATE([Total Revenue], DATEADD('Date'[Date], -1, QUARTER)) RETURN DIVIDE(_curr - _prev, _prev)` |
| **Rolling 3-Month Avg** | `AVERAGEX(DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -3, MONTH), [Total Revenue])` |
| **Rolling 12-Month** | `CALCULATE([Total Revenue], DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -12, MONTH))` |
| **Same Period Last Year** | `CALCULATE([Total Revenue], PARALLELPERIOD('Date'[Date], -12, MONTH))` |
| **Days Since Last Order** | `DATEDIFF(MAX('Orders'[order_date]), TODAY(), DAY)` |
| **Running Total** | `CALCULATE([Total Revenue], FILTER(ALLSELECTED('Date'[Date]), 'Date'[Date] <= MAX('Date'[Date])))` |

### Statistical

| Pattern | DAX |
|---------|-----|
| **Moving Average (7-day)** | `AVERAGEX(DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -7, DAY), [Total Revenue])` |
| **Percentile (P90)** | `PERCENTILEX.INC(ALL('Table'), 'Table'[Value], 0.9)` |
| **Standard Deviation** | `VAR _avg = AVERAGE('Table'[Value]) RETURN SQRT(AVERAGEX('Table', ('Table'[Value] - _avg)^2))` |
| **Median** | `MEDIANX('Table', 'Table'[Value])` |
| **Coefficient of Variation** | `DIVIDE(STDEV.P('Table'[Value]), AVERAGE('Table'[Value]))` |

### Ranking & Top N

| Pattern | DAX |
|---------|-----|
| **Rank** | `RANKX(ALL('Products'), [Total Revenue],, DESC, Dense)` |
| **Top N Flag** | `IF(RANKX(ALL('Products'), [Total Revenue],, DESC) <= 10, "Top 10", "Other")` |
| **Dynamic Top N** | `VAR _n = SELECTEDVALUE('Parameter'[Value], 10) RETURN IF(RANKX(ALL('Products'), [Total Revenue],, DESC) <= _n, [Total Revenue])` |
| **Cumulative %** | `VAR _total = CALCULATE([Total Revenue], ALL('Products')) VAR _running = CALCULATE([Total Revenue], FILTER(ALL('Products'), RANKX(ALL('Products'), [Total Revenue],, DESC) <= RANKX(ALL('Products'), [Total Revenue],, DESC))) RETURN DIVIDE(_running, _total)` |

### Text & Dynamic Formatting

| Pattern | DAX |
|---------|-----|
| **Dynamic Title** | `"Revenue: " & FORMAT([Total Revenue], "#,##0") & " (" & FORMAT([YoY Growth %], "+0.0%;-0.0%") & ")"` |
| **Conditional Icon** | `IF([YoY Growth %] > 0, "▲ ", IF([YoY Growth %] < 0, "▼ ", "● ")) & FORMAT([YoY Growth %], "0.0%")` |
| **Star Rating** | `REPT("★", ROUND([Score] * 5, 0)) & REPT("☆", 5 - ROUND([Score] * 5, 0))` |
| **Traffic Light** | `SWITCH(TRUE(), [Value] >= [Target], "🟢", [Value] >= [Target]*0.8, "🟡", "🔴")` |
| **Smart Format** | `IF([Value] >= 1E9, FORMAT([Value]/1E9, "0.0") & "B", IF([Value] >= 1E6, FORMAT([Value]/1E6, "0.0") & "M", IF([Value] >= 1E3, FORMAT([Value]/1E3, "0.0") & "K", FORMAT([Value], "#,##0"))))` |

### Financial

| Pattern | DAX |
|---------|-----|
| **CAGR** | `VAR _years = DATEDIFF(MIN('Date'[Date]), MAX('Date'[Date]), YEAR) VAR _start = CALCULATE([Revenue], FIRSTDATE('Date'[Date])) VAR _end = CALCULATE([Revenue], LASTDATE('Date'[Date])) RETURN POWER(DIVIDE(_end, _start), DIVIDE(1, _years)) - 1` |
| **Gross Margin %** | `DIVIDE([Revenue] - [COGS], [Revenue])` |
| **Break-Even Units** | `DIVIDE([Fixed Costs], [Unit Price] - [Variable Cost per Unit])` |
| **ROI %** | `DIVIDE([Net Profit], [Total Investment])` |
| **Payback Period (months)** | `DIVIDE([Total Investment], [Monthly Net Cash Flow])` |

---

> 💡 **วิธีใช้**: Copy DAX → ปรับชื่อ `'Table'[Column]` ให้ตรงกับ model ของคุณ → ใส่เป็น Measure ใน model.bim
