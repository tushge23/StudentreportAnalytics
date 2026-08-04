# 🎓 StudentReportAnalytics

An end-to-end data analytics project demonstrating **SQL, Statistics, Machine Learning, Excel reporting,
and BI-style dashboarding** — built around an education/assessment dataset (student demographics,
study habits, and test scores).

> Built to demonstrate the core Data Analyst skill set: **SQL · Tableau/Power BI-equivalent dashboarding ·
> Statistics · Excel**, plus applied ML for predictive insight.

**Author:** [tushge23](https://github.com/tushge23)

## 📁 Project Structure

```
StudentReportAnalytics/
├── data/
│   └── generate_data.py       # Generates realistic synthetic dataset (2,000 students)
├── sql/
│   ├── schema.sql              # Table schema
│   ├── load_db.py              # Loads CSV -> SQLite database
│   └── queries.sql             # 7 analytical business-question queries
├── analysis/
│   └── stats_analysis.py       # t-tests, ANOVA, correlation, chi-square, confidence intervals
├── ml/
│   └── predict_grades.py       # Classification (pass/fail) + Regression (grade %) models
├── excel/
│   └── export_report.py        # Generates formatted Excel workbook with pivot tables + chart
├── dashboard/
│   └── app.py                  # Interactive Streamlit + Plotly BI dashboard
└── requirements.txt
```

## 🚀 Quickstart

```bash
pip install -r requirements.txt

# 1. Generate the dataset
python data/generate_data.py

# 2. Load into SQLite and run analytical queries
python sql/load_db.py
sqlite3 db/students.db < sql/queries.sql   # or open db/students.db in any SQL client

# 3. Run statistical analysis
python analysis/stats_analysis.py

# 4. Train ML models
python ml/predict_grades.py

# 5. Generate the Excel report
python excel/export_report.py

# 6. Launch the interactive dashboard
streamlit run dashboard/app.py
```

## 🔍 What each layer demonstrates

| Skill | Where |
|---|---|
| **SQL** | `sql/schema.sql`, `sql/queries.sql` — joins, aggregations, window functions (`NTILE`), CASE-based bucketing |
| **Statistics** | `analysis/stats_analysis.py` — Welch's t-tests, one-way ANOVA, Pearson correlation, chi-square test of independence, 95% confidence intervals |
| **Machine Learning** | `ml/predict_grades.py` — Logistic Regression & Random Forest classifier (pass/fail prediction, AUC ~0.84), Random Forest regressor (grade prediction), feature importance for explainability |
| **Excel** | `excel/export_report.py` — multi-sheet workbook with styled headers, pivot-style summaries, and a native Excel chart |
| **BI Dashboard** | `dashboard/app.py` — interactive filters, KPI cards, and cross-filtered charts (Plotly) |

## 📊 Key Findings (from the generated sample data)

- Students who completed **test preparation** score ~6.8 points higher on average (p < 0.001).
- **Tutoring** is associated with a ~5.9 point increase in final grade (p < 0.001).
- **Attendance rate** and **study hours/week** are the two strongest predictors of pass/fail in the ML model.
- Parental education level shows a statistically significant effect on final grade (ANOVA, p < 0.001).

## 📝 Note on Tableau / Power BI

Tableau (`.twbx`) and Power BI (`.pbix`) are proprietary desktop-tool file formats that can't be generated
from a script/repo. This project ships an equivalent **interactive Plotly/Streamlit dashboard** instead
(same filtering + KPI + chart functionality), which is fully reproducible from code and easy to deploy
(Streamlit Community Cloud, free). If you have Tableau/Power BI Desktop installed, you can also just
connect either tool directly to `data/students.csv` or `db/students.db` and rebuild the same visuals —
the underlying data and queries are identical either way.

## 🛠 Tech Stack

Python · pandas · SQLite · scipy · scikit-learn · openpyxl · Streamlit · Plotly

## 📄 License

MIT
