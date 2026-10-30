# Phase 1: Foundational Framework & Project Governance
**Programme:** AnalystLab Africa Experience Lab Internship  
**Project:** Week 3 — Hospital Operations, Cost & Patient Flow Intelligence  
**Role:** Junior Healthcare Analytics Intern | Supervised by Senior Healthcare Analytics Mentor  

---

## Task 1: Business Problem Statement

### 1. Healthcare Organisation's Operational Challenge (Ground Truth from Assignment)
Healthcare provider systems constantly face operational bottlenecks, unpredictable patient inflow volumes, varying duration of hospital encounters, and shifting financial dynamics between medical expenses (claim costs) and payer reimbursements. Without unified intelligence across clinical encounters, procedures, and billing, hospital leadership cannot effectively optimize staff scheduling, allocate inpatient beds, control out-of-pocket patient burdens, or forecast departmental budgets.

### 2. Specific Investigation Scope & Core Operational Questions
The project investigates operational efficiency, patient encounter dynamics, cost drivers, and payer coverage using historical administrative and billing records. Specifically, the inquiry focuses on:
- **Encounter Volume & Temporal Patterns:** How encounter loads distribute over time and across care classes (ambulatory, emergency, inpatient, wellness, urgent care).
- **Encounter Duration & Patient Flow Bottlenecks:** Identification of high-duration encounters (e.g., >24 hours) that consume critical bed capacity.
- **Cost & Coverage Distribution:** Discrepancies between total claim costs and payer coverage, specifically identifying uninsured/zero-coverage encounters and patient-borne liabilities.
- **Procedure Utilisation:** The operational frequency of clinical procedures and their baseline cost impact on hospital resource utilisation.

### 3. Operational Importance
- **Bed & Capacity Management:** Inaccurate duration tracking leads to bed shortages, emergency room boarding, and delayed elective admissions.
- **Financial Sustainability:** Uncompensated care and zero-payer coverage encounters pose direct financial exposure to hospital solvency.
- **Resource Allocation:** High-frequency and high-cost procedures require dedicated staffing, surgical suites, and inventory controls.

### 4. Intended Users & Decision Support
| Intended User Role | Operational Decisions Supported |
| :--- | :--- |
| **Hospital Operations Directors** | Bed turnover management, nurse-to-patient staffing ratios, bottleneck reduction. |
| **Chief Financial Officers (CFOs) / Billing Managers** | Payer contract negotiations, charity care budgeting, debt risk mitigation. |
| **Department / Clinical Service Heads** | Equipment scheduling, procedure inventory planning, outpatient clinic hours. |
| **Quality & Health Informatics Officers** | Care-continuity tracking, readmission pattern monitoring, administrative data quality. |

### 5. Evidence Available & Inherent Limitations
- **Data Modality:** Historical tabular administrative/billing records (`encounters`, `patients`, `procedures`, `payers`, `organizations`).
- **Absence of Clinical Granularity:** Administrative records lack real-time vital signs, laboratory values, severity scores, and physician notes.
- **Distinction Between Correlation and Causality:** Differences in cost or duration across classes or payers reflect operational/demographic associations, not clinical effectiveness.
- **Synthetic/Synthea Nature:** Data generated for healthcare training represents realistic simulated workflows but must not be treated as actual patient clinical histories.
- **No Direct Medical Advice:** Outputs support hospital workflow and financial intelligence, never medical diagnostics or clinical patient treatment.

### 6. Distinction: Assignment Ground Truth vs. Working Assumptions
- **Official Assignment Ground Truth:** Scope covers encounter classes, durations, claim costs, payer coverage, and procedure frequency across the 6 provided CSV files and 2 SQL references.
- **Working Assumptions:** Encounters with valid start and stop timestamps accurately reflect administrative encounter length; missing payer coverage implies zero payer reimbursement unless an unresolved claim flag is indicated; readmissions are strictly operational return visits unless clinically coded otherwise.

---

## Task 2: Data Asset Inventory & Workspace Inspection

### 1. Workspace Inventory Status (As of Initial Inspection)
| Resource Name | Role / Purpose | File Status in `week 3/` |
| :--- | :--- | :--- |
| `AnalystLab_Africa_Week3_Batch_F_Assignment.pdf` | Authoritative specification document | **Present** (in `docs/`) |
| `encounters.csv` | Encounter volumes, classes, duration, costs, coverage | *Awaiting placement in `data/raw/`* |
| `patients.csv` | Patient demographics and longitudinal linkage | *Awaiting placement in `data/raw/`* |
| `procedures.csv` | Clinical procedures, codes, frequency, base costs | *Awaiting placement in `data/raw/`* |
| `payers.csv` | Payer names, categories, and financial coverage rules | *Awaiting placement in `data/raw/`* |
| `organizations.csv` | Facility/provider metadata | *Awaiting placement in `data/raw/`* |
| `data_dictionary.csv` | Schema specifications, data definitions, key constraints | *Awaiting placement in `data/raw/`* |
| `hospital_analytics_questions.sql` | Benchmark analytical queries | *Awaiting placement in `src/` or `data/`* |
| `create_hospital_db.sql` | Practice relational database schema | *Awaiting placement (isolated execution only)* |

> **Safety Warning (Database Execution):** `create_hospital_db.sql` drops and recreates `hospital_db`. It must strictly be run in an isolated sandbox or local test instance, never against an existing or production database.

---

## Task 3: Measurable Success Criteria

To ensure technical rigor, the project will be evaluated against five measurable, verifiable criteria:
1. **Financial & Reconciliation Integrity (Metric Check):** 100% of calculated total claim costs, payer reimbursements, and patient out-of-pocket liabilities reconcile with an independent double-check calculation (e.g., Python verification matching SQL/Power BI measures down to the cent, $\Delta = 0.00$).
2. **Data Consistency & Temporal Logic:** 0% negative encounter durations allowed; encounters with missing end timestamps must be systematically flagged and handled without silently distorting duration averages.
3. **Filter Robustness & Granularity Preservation:** In dashboards or analytical models, multivariable filtering (by year, encounter class, and payer) preserves entity grain without Cartesian duplication or inflated encounter counts.
4. **Reproducibility Benchmark:** 100% of analytical tables, charts, or models can be recomputed from raw data via a single clean script/notebook execution without manual intervention.
5. **Non-Clinical Boundary Adherence:** Zero diagnostic or clinical claims made; all recommendations strictly confined to operational, logistical, and financial workflows.

---

## Task 4: Professional Standards & Governance Checklist

- [x] **Project Structure:** Established clean directory hierarchy (`data/raw`, `data/processed`, `docs`, `notebooks`, `reports`, `src`).
- [ ] **Data Hygiene & Privacy:** Strict de-identification in all artifacts; synthetic patient names, addresses, and identifiers excluded from visual outputs.
- [ ] **Methodological Transparency:** All transformations (handling missing durations, zero-payer rows, currency conversions) documented with business justifications.
- [ ] **Validation Evidence:** Retain execution logs and verification scripts showing independent cross-validation.
- [ ] **Code Attribution & Quality:** Python / SQL scripts PEP-8 formatted, modular, and attributing external packages.
- [ ] **Git & Deliverable Hygiene:** No raw large CSVs, private keys, or credentials committed to version control.
