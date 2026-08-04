"""
generate_data.py
Generates a realistic synthetic dataset of student academic performance
for the StudentReportAnalytics project (SQL + Stats + ML + BI dashboard).

Run:
    python data/generate_data.py

Output:
    data/students.csv
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 2000

genders = np.random.choice(["Female", "Male"], size=N, p=[0.52, 0.48])
ethnicities = np.random.choice(
    ["Group A", "Group B", "Group C", "Group D", "Group E"], size=N,
    p=[0.15, 0.22, 0.28, 0.20, 0.15]
)
parent_education = np.random.choice(
    ["High School", "Some College", "Associate's", "Bachelor's", "Master's"],
    size=N, p=[0.25, 0.25, 0.20, 0.20, 0.10]
)
lunch_type = np.random.choice(["Standard", "Free/Reduced"], size=N, p=[0.65, 0.35])
test_prep = np.random.choice(["Not Completed", "Completed"], size=N, p=[0.64, 0.36])
study_hours_week = np.round(np.random.gamma(shape=3, scale=2.5, size=N), 1)
attendance_rate = np.clip(np.random.normal(0.90, 0.08, size=N), 0.4, 1.0)
tutoring = np.random.choice(["No", "Yes"], size=N, p=[0.7, 0.3])
extracurricular = np.random.choice(["No", "Yes"], size=N, p=[0.45, 0.55])

# Build a "true" score signal, then add noise, so ML models have real
# relationships to learn (this also makes the stats tests meaningful).
base = 55
score = (
    base
    + (test_prep == "Completed") * 6.5  # noqa: E501
    + (tutoring == "Yes") * 5.0
    + (lunch_type == "Standard") * 4.0
    + study_hours_week * 1.3
    + (attendance_rate - 0.9) * 60
    + pd.Series(parent_education).map({
        "High School": -4, "Some College": -1, "Associate's": 1,
        "Bachelor's": 4, "Master's": 7
    }).values
    + np.random.normal(0, 8, size=N)
)

math_score = np.clip(score + np.random.normal(0, 5, N), 0, 100).round(1)
reading_score = np.clip(score + np.random.normal(2, 5, N), 0, 100).round(1)
writing_score = np.clip(score + np.random.normal(-1, 5, N), 0, 100).round(1)

final_grade_pct = ((math_score + reading_score + writing_score) / 3).round(1)
passed = (final_grade_pct >= 60).astype(int)

df = pd.DataFrame({
    "student_id": np.arange(1, N + 1),
    "gender": genders,
    "ethnicity_group": ethnicities,
    "parent_education": parent_education,
    "lunch_type": lunch_type,
    "test_preparation": test_prep,
    "study_hours_week": study_hours_week,
    "attendance_rate": attendance_rate.round(3),
    "tutoring": tutoring,
    "extracurricular": extracurricular,
    "math_score": math_score,
    "reading_score": reading_score,
    "writing_score": writing_score,
    "final_grade_pct": final_grade_pct,
    "passed": passed,
})

out_path = "data/students.csv"
df.to_csv(out_path, index=False)
print(f"Generated {len(df)} rows -> {out_path}")
print(df.head())
