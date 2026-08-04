"""
app.py
Interactive BI-style dashboard for the Student Performance Analytics project.

Run:
    streamlit run dashboard/app.py
"""

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Student Performance Analytics", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/students.csv")

df = load_data()

st.title("🎓 StudentReportAnalytics")
st.caption("Built by tushge23 — SQL + Statistics + ML + BI dashboard")

# --- Sidebar filters ---
st.sidebar.header("Filters")
genders = st.sidebar.multiselect("Gender", df.gender.unique(), default=list(df.gender.unique()))
parent_ed = st.sidebar.multiselect("Parent Education", df.parent_education.unique(), default=list(df.parent_education.unique()))
lunch = st.sidebar.multiselect("Lunch Type", df.lunch_type.unique(), default=list(df.lunch_type.unique()))

filtered = df[
    df.gender.isin(genders) &
    df.parent_education.isin(parent_ed) &
    df.lunch_type.isin(lunch)
]

# --- KPI row ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Students", f"{len(filtered):,}")
col2.metric("Avg Final Grade", f"{filtered.final_grade_pct.mean():.1f}%")
col3.metric("Pass Rate", f"{filtered.passed.mean() * 100:.1f}%")
col4.metric("Avg Attendance", f"{filtered.attendance_rate.mean() * 100:.1f}%")

st.divider()

# --- Charts ---
c1, c2 = st.columns(2)

with c1:
    grp = filtered.groupby("parent_education", as_index=False).final_grade_pct.mean().sort_values("final_grade_pct")
    fig = px.bar(grp, x="final_grade_pct", y="parent_education", orientation="h",
                 title="Average Grade by Parent Education", labels={"final_grade_pct": "Avg Grade (%)", "parent_education": ""})
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig2 = px.scatter(filtered, x="study_hours_week", y="final_grade_pct", color="passed",
                       title="Study Hours vs Final Grade", opacity=0.6,
                       labels={"study_hours_week": "Study Hours/Week", "final_grade_pct": "Final Grade (%)"})
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    grp2 = filtered.groupby("ethnicity_group", as_index=False)[["math_score", "reading_score", "writing_score"]].mean()
    grp2_melt = grp2.melt(id_vars="ethnicity_group", var_name="Subject", value_name="Avg Score")
    fig3 = px.bar(grp2_melt, x="ethnicity_group", y="Avg Score", color="Subject", barmode="group",
                  title="Subject Scores by Ethnicity Group")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = px.histogram(filtered, x="final_grade_pct", nbins=30, title="Final Grade Distribution",
                         color="passed", labels={"final_grade_pct": "Final Grade (%)"})
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("Raw Data")
st.dataframe(filtered, use_container_width=True, height=300)
