# Data_Game: Enterprise Analytics & Risk Optimization Platform

An end-to-end Enterprise Analytics Solution designed for E-Commerce Intelligence, Operations Optimization, Churn Prediction, Fraud Risk Scoring, Sales Forecasting, and Executive Reporting.

---

## 🛠️ Step-by-Step Prerequisites & Downloads Guide

To set up this project on your system and run it smoothly, follow this explicit guide on **what to download** and **what NOT to download**.

### 1. What You MUST Download & Install
1. **Python 3.11 or higher**
   - **Download Link**: [python.org/downloads](https://www.python.org/downloads/)
   - **CRITICAL**: During installation on Windows, check the box **"Add python.exe to PATH"**.
2. **Visual Studio Code (VS Code)**
   - **Download Link**: [code.visualstudio.com](https://code.visualstudio.com/)
   - Standard code editor for viewing code, SQL files, reports, and running terminal commands.
3. **Git**
   - **Download Link**: [git-scm.com](https://git-scm.com/)
   - Required to version control your project and push to GitHub.
4. **Power BI Desktop** *(Optional but Recommended for BI Showcase)*
   - **Download Link**: Microsoft Store or [Power BI Desktop Download](https://powerbi.microsoft.com/desktop/)
   - Free tool for Windows to build executive dashboards.

---

### 2. VS Code Extensions to Install
Open VS Code (`Ctrl + Shift + X` on Windows) and search for:
- **Python** (`ms-python.python`)
- **Pylance** (`ms-python.vscode-pylance`)
- **Jupyter** (`ms-toolsai.jupyter`)
- **SQLTools** or **PostgreSQL** (optional for database querying)

---

### 3. What You DO NOT Need to Download
- ❌ **No heavy paid IDEs** (Visual Studio Professional, PyCharm Ultimate are unnecessary).
- ❌ **No Docker required** (We provide an out-of-the-box zero-config SQLite backend alongside PostgreSQL DDL scripts).
- ❌ **No paid cloud services** (All models and interactive web apps run 100% locally for free).

---

## 🚀 Environment Installation & Command Execution

Open your terminal or PowerShell in VS Code within the `Data_Game` folder:

```bash
# 1. Create a Python Virtual Environment
python -m venv venv

# 2. Activate Virtual Environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
# (Or Command Prompt: venv\Scripts\activate.bat)

# 3. Install all required packages
pip install -r requirements.txt
```

---

## 📁 Repository Structure

```
Data_Game/
│── data/                     # Raw & processed CSV datasets
│   ├── raw/                  # All 10 generated enterprise datasets
│   └── processed/            # Cleaned, aggregated, and modeled datasets
│── database/                 # SQL DDL schemas, CTE queries, analytical views
│   ├── schema.sql            # Table definitions & relational constraints
│   ├── indexes.sql           # Query optimization & B-tree indexes
│   └── advanced_queries.sql  # Complex SQL CTEs, Window Functions & KPIs
│── src/                      # Python source code for Data Gen, ML & Analytics
│   ├── data_generator.py     # High-fidelity synthetic enterprise data generator
│   ├── db_loader.py          # Auto-ingestion script for SQLite & PostgreSQL
│   ├── rfm_segmentation.py   # RFM + K-Means clustering engine
│   ├── churn_model.py        # Customer Churn prediction pipeline (XGBoost/RF)
│   ├── fraud_detection.py    # Fraud Risk Scoring engine (Isolation Forest)
│   ├── sales_forecasting.py  # 6-Month Sales Forecasting engine (ARIMA/SARIMAX)
│   └── operations_opt.py     # Warehouse & Delivery SLA optimization engine
│── dashboards/               # BI Dashboard artifacts & Interactive Web App
│   ├── app.py                # Streamlit Live Interactive Executive Dashboard
│   └── powerbi_guide.md      # Power BI Data Modeling & DAX measure guide
│── reports/                  # Data Dictionary, Business Report & Documentation
│   ├── data_dictionary.md    # Full schema documentation & key relationships
│   ├── methodology.md        # Technical methodology & statistical approach
│   └── executive_report.md   # Final C-suite executive report & insights
└── presentation/             # Executive Presentation Deck
    └── slide_deck.md         # 20-Slide C-level presentation deck
```

---

## ⚡ How to Run the Project (Step-by-Step)

### Step 1: Generate All 10 Enterprise Datasets
```bash
python src/data_generator.py
```
*Outputs 10 CSV files into `data/raw/` representing 5,000+ customers, 20,000+ orders, transactions, products, warehouses, deliveries, reviews, tickets, etc.*

### Step 2: Build Database Schema & Load Data
```bash
python src/db_loader.py
```
*Creates `data_game.db` SQLite database, builds relational tables, applies SQL indexes, and loads all CSV files into SQL tables.*

### Step 3: Run Machine Learning Models & Analytical Engines
```bash
# RFM Customer Segmentation & K-Means
python src/rfm_segmentation.py

# Customer Churn Machine Learning Pipeline
python src/churn_model.py

# Transaction Fraud Detection & Risk Scoring
python src/fraud_detection.py

# 6-Month Revenue & Order Volume Forecasting
python src/sales_forecasting.py

# Operational & Courier Delivery Optimization
python src/operations_opt.py
```

### Step 4: Launch the Live Interactive Executive Dashboard
```bash
streamlit run dashboards/app.py
```
*Launches an interactive web dashboard in your browser (`http://localhost:8501`) featuring executive KPIs, RFM segments, ML churn predictions, fraud scoring, and operational bottleneck visualizations!*

---

## 🎯 Candidate Evaluation Criteria Alignment

| Skill Area | Weight | Data_Game Solution |
| :--- | :---: | :--- |
| **SQL & Data Modeling** | 20% | Relational DDL schema, foreign key constraints, composite B-tree indexes, complex window functions, CTEs, and views in `database/`. |
| **Data Analysis & Processing**| 25% | Robust Pandas ETL pipelines, statistical feature engineering, data quality checks. |
| **Business Understanding** | 20% | Quantified ROI impact, retention strategies, cost-reduction recommendations for warehouse and courier SLAs. |
| **Dashboard & Visualization** | 15% | Live multi-page Streamlit web app + complete Power BI modeling & DAX guide. |
| **Risk / Predictive Analytics**| 10% | XGBoost Churn Prediction, Isolation Forest Anomaly Detection, ARIMA/Prophet Sales Forecasting. |
| **Executive Communication** | 10% | Comprehensive Executive Business Report, Data Dictionary, and 20-slide C-level presentation deck. |
