"""
predict_grades.py
Trains two ML models on the student performance dataset:
 1. Classification: predict pass/fail (Logistic Regression + Random Forest)
 2. Regression: predict final_grade_pct (Random Forest Regressor)

Also prints feature importance so the analysis is explainable, not a black box.

Run:
    python ml/predict_grades.py

Output:
    ml/model_report.txt
    ml/pass_fail_model.pkl
    ml/grade_regressor.pkl
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score, roc_auc_score, classification_report,
    mean_absolute_error, r2_score
)

df = pd.read_csv("data/students.csv")

categorical_cols = [
    "gender", "ethnicity_group", "parent_education",
    "lunch_type", "test_preparation", "tutoring", "extracurricular"
]
numeric_cols = ["study_hours_week", "attendance_rate"]

X = df[categorical_cols + numeric_cols]
y_class = df["passed"]
y_reg = df["final_grade_pct"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
], remainder="passthrough")

report_lines = []


def log(msg=""):
    print(msg)
    report_lines.append(str(msg))


log("=" * 60)
log("ML MODEL REPORT")
log("=" * 60)

# ---------- Classification: Pass / Fail ----------
Xtr, Xte, ytr, yte = train_test_split(X, y_class, test_size=0.2, random_state=42, stratify=y_class)

log_reg_pipe = Pipeline([("prep", preprocessor), ("clf", LogisticRegression(max_iter=1000))])
log_reg_pipe.fit(Xtr, ytr)
pred_lr = log_reg_pipe.predict(Xte)
proba_lr = log_reg_pipe.predict_proba(Xte)[:, 1]

rf_pipe = Pipeline([("prep", preprocessor), ("clf", RandomForestClassifier(n_estimators=300, random_state=42))])
rf_pipe.fit(Xtr, ytr)
pred_rf = rf_pipe.predict(Xte)
proba_rf = rf_pipe.predict_proba(Xte)[:, 1]

log("\n[Classification] Predicting Pass/Fail")
log(f"  Logistic Regression: accuracy={accuracy_score(yte, pred_lr):.3f}, AUC={roc_auc_score(yte, proba_lr):.3f}")
log(f"  Random Forest:       accuracy={accuracy_score(yte, pred_rf):.3f}, AUC={roc_auc_score(yte, proba_rf):.3f}")
log("\n  Random Forest classification report:")
log(classification_report(yte, pred_rf))

# Feature importance (Random Forest)
feature_names = rf_pipe.named_steps["prep"].get_feature_names_out()
importances = rf_pipe.named_steps["clf"].feature_importances_
top_idx = np.argsort(importances)[::-1][:10]
log("  Top 10 features driving pass/fail prediction:")
for i in top_idx:
    log(f"    {feature_names[i]:35s} {importances[i]:.4f}")

# ---------- Regression: Final grade ----------
Xtr2, Xte2, ytr2, yte2 = train_test_split(X, y_reg, test_size=0.2, random_state=42)
reg_pipe = Pipeline([("prep", preprocessor), ("reg", RandomForestRegressor(n_estimators=300, random_state=42))])
reg_pipe.fit(Xtr2, ytr2)
pred_reg = reg_pipe.predict(Xte2)

log("\n[Regression] Predicting Final Grade %")
log(f"  MAE = {mean_absolute_error(yte2, pred_reg):.2f}")
log(f"  R^2 = {r2_score(yte2, pred_reg):.3f}")

log("\n" + "=" * 60)

joblib.dump(rf_pipe, "ml/pass_fail_model.pkl")
joblib.dump(reg_pipe, "ml/grade_regressor.pkl")

with open("ml/model_report.txt", "w") as f:
    f.write("\n".join(report_lines))

print("\nModels saved to ml/pass_fail_model.pkl and ml/grade_regressor.pkl")
print("Report saved to ml/model_report.txt")
