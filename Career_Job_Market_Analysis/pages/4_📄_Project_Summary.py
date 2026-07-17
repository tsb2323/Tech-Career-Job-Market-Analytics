import streamlit as st

st.set_page_config(
    page_title="Project Summary",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Project Summary")
st.markdown("---")

# =====================================================
# Project Title
# =====================================================

st.header("📊 Project Title")

st.info("""
**Tech-Career & Job Market Analytics**
""")

st.markdown("---")

# =====================================================
# Objective
# =====================================================

st.header("🎯 Project Objective")

st.write("""
The objective of this project is to analyze the Global Job Market Dataset
using Python and Streamlit. The dashboard helps users understand salary
trends, employment patterns, education impact, company size influence,
experience levels, and occupation-wise insights through interactive
visualizations.
""")

st.markdown("---")

# =====================================================
# Dataset Information
# =====================================================

st.header("📁 Dataset Information")

col1, col2 = st.columns(2)

with col1:

    st.success("""
**Dataset Name**

Global Job Market Dataset
""")

    st.success("""
**Source**

Kaggle
""")

with col2:

    st.success("""
**Records**

500,000+
""")

    st.success("""
**Columns**

11
""")

st.markdown("---")

# =====================================================
# Technologies Used
# =====================================================

st.header("🛠 Technologies Used")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("""
🐍 Python

📊 Pandas

📈 Plotly
""")

with c2:
    st.info("""
💻 Streamlit

📉 Matplotlib

🎨 Seaborn
""")

with c3:
    st.info("""
🧮 NumPy

📝 VS Code

🌐 GitHub
""")

st.markdown("---")

# =====================================================
# Dashboard Features
# =====================================================

st.header("✨ Dashboard Features")

st.write("""
✅ Interactive Dashboard

✅ Salary Analysis

✅ Country-wise Analysis

✅ Occupation Analysis

✅ Experience Analysis

✅ Education Analysis

✅ Employment Type Analysis

✅ Company Size Analysis

✅ Dataset Explorer

✅ Project Summary
""")

st.markdown("---")

# =====================================================
# Key Findings
# =====================================================

st.header("🔍 Key Findings")

findings = [
    "Salary generally increases with experience.",
    "Higher education levels are associated with higher salaries.",
    "Large companies tend to offer higher average salaries.",
    "Salary distribution varies across countries and occupations.",
    "Employment type influences salary trends.",
    "Different career fields have different salary ranges.",
    "Interactive visualizations make data exploration easier."
]

for item in findings:
    st.success(item)

st.markdown("---")

# =====================================================
# Conclusion
# =====================================================

st.header("✅ Conclusion")

st.write("""
This project successfully analyzes the global career market using interactive
visualizations. The dashboard helps users understand relationships between
salary, education, experience, company size, employment type, and occupation.
The use of Streamlit provides an easy-to-use interface for exploring the
dataset and extracting meaningful insights.
""")

st.markdown("---")

# =====================================================
# Future Scope
# =====================================================

st.header("🚀 Future Scope")

future = [
    "Add an AI-based Career Recommendation System.",
    "Integrate Machine Learning for salary prediction.",
    "Connect the dashboard with a live SQL database.",
    "Deploy the application online using Streamlit Community Cloud.",
    "Include real-time job market datasets.",
    "Add user authentication and personalized dashboards."
]

for item in future:
    st.info(item)

st.markdown("---")

# =====================================================
# Developed By
# =====================================================

st.header("👨‍💻 Developed By")

left, right = st.columns(2)

with left:

    st.success("""
**Name**

Ravinder Singh and Tanvir Singh Bains
""")

    st.success("""
**Course**

B.Tech CSE (Data Science)
""")

with right:

    st.success("""
**Project**

Semester Training Project
""")

    st.success("""
**Platform**

Python • Streamlit • Plotly
""")

st.markdown("---")

# =====================================================
# Acknowledgement
# =====================================================

st.header("Acknowledgement")

st.write("""
I sincerely thank my training mentor, faculty members, and institution for
their guidance and support throughout this project. I also acknowledge Kaggle
for providing the Global Job Market Dataset used for analysis.
""")

st.markdown("---")

# =====================================================
# Footer
# =====================================================

st.caption(
    "© 2026 Tech-Career & Job Market Analytics | Semester Training Project | Developed by Ravinder Singh and Tanvir Singh Bains"
)