import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Load dataset

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "Cleaned_Project_DataSet.csv"

df = pd.read_csv(DATA_PATH)
st.title("📊 Dashboard")
st.write("Quick overview of the Global Job Market Dataset")

st.divider()

# ==============================
# KPI Cards
# ==============================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("📄 Total Records", f"{len(df):,}")

with c2:
    st.metric("🌍 Countries", df["Country"].nunique())

with c3:
    st.metric("🏙 Cities", df["City"].nunique())

with c4:
    st.metric("💼 Occupations", df["Occupation"].nunique())

c5, c6, c7, c8 = st.columns(4)

with c5:
    st.metric("📂 Fields", df["Field"].nunique())

with c6:
    st.metric("🏢 Company Sizes", df["Company_size"].nunique())

with c7:
    st.metric(
        "💰 Avg Salary",
        f"${df['Annual_salary(usd)'].mean():,.0f}"
    )

with c8:
    st.metric(
        "🧑 Avg Experience",
        f"{df['Experience'].mean():.1f} Years"
    )

st.divider()

# ==============================
# Salary Statistics
# ==============================

st.subheader("💰 Salary Statistics")

a1, a2, a3 = st.columns(3)

with a1:
    st.metric(
        "Highest Salary",
        f"${df['Annual_salary(usd)'].max():,.0f}"
    )

with a2:
    st.metric(
        "Lowest Salary",
        f"${df['Annual_salary(usd)'].min():,.0f}"
    )

with a3:
    st.metric(
        "Median Salary",
        f"${df['Annual_salary(usd)'].median():,.0f}"
    )

st.divider()

# ==============================
# Dataset Information
# ==============================

left, right = st.columns(2)

with left:

    st.subheader("📋 Dataset Information")

    info = pd.DataFrame({
        "Property": [
            "Rows",
            "Columns",
            "Missing Values",
            "Duplicate Rows"
        ],
        "Value": [
            df.shape[0],
            df.shape[1],
            df.isnull().sum().sum(),
            df.duplicated().sum()
        ]
    })

    st.dataframe(info, use_container_width=True)

with right:

    st.subheader("📑 Column Names")

    st.dataframe(
        pd.DataFrame(df.columns, columns=["Columns"]),
        use_container_width=True
    )

st.divider()

# ==============================
# Dataset Preview
# ==============================

st.subheader("👀 Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)

st.divider()

# ==============================
# Quick Insights
# ==============================

st.subheader("📈 Quick Insights")

col1, col2 = st.columns(2)

with col1:

    highest_country = (
        df.groupby("Country")["Annual_salary(usd)"]
        .mean()
        .idxmax()
    )

    highest_occ = (
        df.groupby("Occupation")["Annual_salary(usd)"]
        .mean()
        .idxmax()
    )
    highest_city = (
        df.groupby("City")["Annual_salary(usd)"]
        .mean()
        .idxmax()
    )
    st.success(f"🌍 Highest Paying Country: **{highest_country}**")

    st.success(f"💼 Highest Paying Occupation: **{highest_occ}**")

    st.success(f"🏙 Highest Paying City: **{highest_city}**")

with col2:

    emp = df["Employment_type"].mode()[0]

    edu = df["Education_level"].mode()[0]

    company = df["Company_size"].mode()[0]

    st.info(f"💼 Most Common Employment Type: **{emp}**")

    st.info(f"🎓 Most Common Education Level: **{edu}**")

    st.info(f"🏢 Most Common Company Size: **{company}**")

st.divider()

# ==============================
# Footer
# ==============================

st.caption(
    " Tech-Career & Job Market Analytics | Semester Training Project | Developed by Ravinder Singh and Tanvir Singh Bains"
)
