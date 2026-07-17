import streamlit as st
import pandas as pd


# -------------------------------
# Page Configuration
# -------------------------------Career Market Analysis Dashboard
st.set_page_config(
    page_title="",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# Load Dataset
# -------------------------------

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Cleaned_Project_DataSet.csv"

df = pd.read_csv(DATA_PATH)
# -------------------------------
# Header
# -------------------------------
st.title("📊 Tech-Career & Job Market Analytics")
st.markdown(
    """
Welcome to the **Tech-Career & Job Market Analytics**.

This interactive dashboard analyzes the **Global Job Market Dataset** to understand
career trends, salary distribution, education impact, company size, and employment patterns.
"""
)

st.divider()

# -------------------------------
# KPI Cards
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🌍 Countries", df["Country"].nunique())

with col2:
    st.metric("🏙 Cities", df["City"].nunique())

with col3:
    st.metric("💼 Occupations", df["Occupation"].nunique())

with col4:
    st.metric("📄 Total Records", f"{len(df):,}")

st.divider()

# -------------------------------
# Project Information
# -------------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("🎯 Project Objective")

    st.write("""
The objective of this project is to analyze the global job market using
interactive data visualization techniques.

This dashboard helps understand:

- Salary trends
- Experience impact
- Education impact
- Company size analysis
- Employment type distribution
- Country-wise job market analysis
- Occupation insights
""")

with col2:

    st.subheader("🛠 Technologies Used")

    st.write("""
- Python
- Pandas
- Plotly
- Streamlit
- NumPy
- Matplotlib
- Seaborn
- VS Code
""")

st.divider()

# -------------------------------
# Dataset Information
# -------------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("📁 Dataset Information")

    st.info("""
**Dataset Name**

Global Job Market Dataset

**Source**

Kaggle

**Total Columns**

11

**Records**

500,000+
""")

with col2:

    st.subheader("📋 Dataset Columns")

    st.code("""
Country
City
Occupation
Field
Experience
Annual_salary(usd)
Employment_type
Education_level
Gender
Company_size
Year
""")

st.divider()

# -------------------------------
# Features
# -------------------------------
st.subheader("✨ Dashboard Features")

feature1, feature2, feature3 = st.columns(3)

with feature1:

    st.success("""
📊 Dashboard

• KPI Cards

• Dataset Overview

• Quick Statistics
""")

with feature2:

    st.success("""
📈 Data Insights

• Interactive Graphs

• Salary Analysis

• Country Analysis

• Education Analysis
""")

with feature3:

    st.success("""
🔍 Dataset Explorer

• Filter Dataset

• Search Records

• Download CSV
""")

st.divider()

# -------------------------------
# Navigation
# -------------------------------
st.subheader("🧭 Navigation")

st.info("""
Use the **sidebar** to explore different sections of the dashboard.

📊 Dashboard

📈 Data Insights

🔍 Dataset Explorer

📄 Project Summary

🎯 Career Recommendation (Coming Soon)
""")

st.divider()

# -------------------------------
# About
# -------------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("👨‍💻 Developed By")

    st.write("""
**Ravinder Singh  and  Tanvir Singh Bains**
             
**Roll No. - 2449465 and 2449475**
             
B.Tech CSE (Data Science)

Semester Training Project
""")
