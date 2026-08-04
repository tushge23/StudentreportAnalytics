"""
stats_analysis.py
Statistical analysis on the student performance dataset:
 - Independent t-tests (test prep, tutoring, lunch type)
 - One-way ANOVA (parent education level)
 - Pearson correlation (study hours / attendance vs grade)
 - Confidence interval for mean final grade

Run:
    python analysis/stats_analysis.py

Output:
    Printed report + analysis/stats_report.txt
"""

import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("data/students.csv")
report_lines = []


def log(msg=""):
    print(msg)
    report_lines.append(str(msg))


log("=" * 60)
log("STATISTICAL ANALYSIS REPORT")
log("=" * 60)

# --- 1. t-test: test preparation ---
grp_completed = df[df.test_preparation == "Completed"].final_grade_pct
grp_not = df[df.test_preparation == "Not Completed"].final_grade_pct
t, p = stats.ttest_ind(grp_completed, grp_not, equal_var=False)
log("\n[1] Test Prep Completed vs Not Completed (Welch's t-test)")
log(f"    Mean (Completed)     = {grp_completed.mean():.2f}")
log(f"    Mean (Not Completed) = {grp_not.mean():.2f}")
log(f"    t = {t:.3f}, p = {p:.6f}")
log("    -> Statistically significant" if p < 0.05 else "    -> Not significant")

# --- 2. t-test: tutoring ---
grp_tutor = df[df.tutoring == "Yes"].final_grade_pct
grp_no_tutor = df[df.tutoring == "No"].final_grade_pct
t2, p2 = stats.ttest_ind(grp_tutor, grp_no_tutor, equal_var=False)
log("\n[2] Tutoring Yes vs No (Welch's t-test)")
log(f"    Mean (Tutoring)    = {grp_tutor.mean():.2f}")
log(f"    Mean (No Tutoring) = {grp_no_tutor.mean():.2f}")
log(f"    t = {t2:.3f}, p = {p2:.6f}")
log("    -> Statistically significant" if p2 < 0.05 else "    -> Not significant")

# --- 3. One-way ANOVA: parent education ---
groups = [g["final_grade_pct"].values for _, g in df.groupby("parent_education")]
f_stat, p3 = stats.f_oneway(*groups)
log("\n[3] One-way ANOVA: Final grade ~ Parent education level")
log(f"    F = {f_stat:.3f}, p = {p3:.6f}")
log("    -> Significant differences across groups" if p3 < 0.05 else "    -> No significant differences")

# --- 4. Pearson correlation: study hours vs grade ---
r, p4 = stats.pearsonr(df.study_hours_week, df.final_grade_pct)
log("\n[4] Pearson correlation: Study hours/week vs Final grade")
log(f"    r = {r:.3f}, p = {p4:.6f}")

# --- 5. Pearson correlation: attendance vs grade ---
r2, p5 = stats.pearsonr(df.attendance_rate, df.final_grade_pct)
log("\n[5] Pearson correlation: Attendance rate vs Final grade")
log(f"    r = {r2:.3f}, p = {p5:.6f}")

# --- 6. 95% Confidence interval for mean final grade ---
mean = df.final_grade_pct.mean()
sem = stats.sem(df.final_grade_pct)
ci = stats.t.interval(0.95, len(df) - 1, loc=mean, scale=sem)
log("\n[6] 95% Confidence Interval for mean final grade")
log(f"    Mean = {mean:.2f}, 95% CI = ({ci[0]:.2f}, {ci[1]:.2f})")

# --- 7. Chi-square test: lunch type vs pass/fail ---
contingency = pd.crosstab(df.lunch_type, df.passed)
chi2, p6, dof, expected = stats.chi2_contingency(contingency)
log("\n[7] Chi-square test: Lunch type vs Pass/Fail")
log(f"    chi2 = {chi2:.3f}, p = {p6:.6f}, dof = {dof}")
log("    -> Statistically significant association" if p6 < 0.05 else "    -> No significant association")

log("\n" + "=" * 60)

with open("analysis/stats_report.txt", "w") as f:
    f.write("\n".join(report_lines))

print("\nReport saved to analysis/stats_report.txt")
