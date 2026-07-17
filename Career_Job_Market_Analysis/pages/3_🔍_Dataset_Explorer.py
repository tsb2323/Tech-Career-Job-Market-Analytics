import streamlit as st
import pandas as pd

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Dataset Explorer",
    page_icon="🔍",
    layout="wide"
)

# ==========================================
# Load Dataset
# ==========================================

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "Cleaned_Project_DataSet.csv"

df = pd.read_csv(DATA_PATH)

# ==========================================
# Title
# ==========================================

st.title("🔍 Dataset Explorer")

st.write(
    "Explore the Global Job Market Dataset using interactive filters."
)

st.divider()

# ==========================================
# Sidebar Filters
# ==========================================

st.sidebar.header("🎛 Filter Dataset")

country = st.sidebar.multiselect(
    "🌍 Country",
    sorted(df["Country"].unique())
)

field = st.sidebar.multiselect(
    "📂 Field",
    sorted(df["Field"].unique())
)

occupation = st.sidebar.multiselect(
    "💼 Occupation",
    sorted(df["Occupation"].unique())
)

employment = st.sidebar.multiselect(
    "🧑 Employment Type",
    sorted(df["Employment_type"].unique())
)

education = st.sidebar.multiselect(
    "🎓 Education Level",
    sorted(df["Education_level"].unique())
)

company = st.sidebar.multiselect(
    "🏢 Company Size",
    sorted(df["Company_size"].unique())
)

gender = st.sidebar.multiselect(
    "👤 Gender",
    sorted(df["Gender"].unique())
)

experience = st.sidebar.slider(
    "📈 Experience (Years)",
    int(df["Experience"].min()),
    int(df["Experience"].max()),
    (
        int(df["Experience"].min()),
        int(df["Experience"].max())
    )
)

salary = st.sidebar.slider(
    "💰 Salary (USD)",
    int(df["Annual_salary(usd)"].min()),
    int(df["Annual_salary(usd)"].max()),
    (
        int(df["Annual_salary(usd)"].min()),
        int(df["Annual_salary(usd)"].max())
    )
)

# ==========================================
# Apply Filters
# ==========================================

filtered = df.copy()

if country:
    filtered = filtered[
        filtered["Country"].isin(country)
    ]

if field:
    filtered = filtered[
        filtered["Field"].isin(field)
    ]

if occupation:
    filtered = filtered[
        filtered["Occupation"].isin(occupation)
    ]

if employment:
    filtered = filtered[
        filtered["Employment_type"].isin(employment)
    ]

if education:
    filtered = filtered[
        filtered["Education_level"].isin(education)
    ]

if company:
    filtered = filtered[
        filtered["Company_size"].isin(company)
    ]

if gender:
    filtered = filtered[
        filtered["Gender"].isin(gender)
    ]

filtered = filtered[
    (filtered["Experience"] >= experience[0]) &
    (filtered["Experience"] <= experience[1])
]

filtered = filtered[
    (filtered["Annual_salary(usd)"] >= salary[0]) &
    (filtered["Annual_salary(usd)"] <= salary[1])
]

# ==========================================
# KPI Cards
# ==========================================

st.subheader("📊 Filter Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Records", len(filtered))

with c2:
    st.metric("Countries", filtered["Country"].nunique())

with c3:
    st.metric("Occupations", filtered["Occupation"].nunique())

with c4:
    st.metric(
        "Average Salary",
        f"${filtered['Annual_salary(usd)'].mean():,.0f}"
        if len(filtered) > 0 else "$0"
    )

st.divider()

# ==========================================
# Search
# ==========================================

search = st.text_input(
    "🔎 Search Occupation"
)

if search:
    filtered = filtered[
        filtered["Occupation"]
        .str.contains(search, case=False)
    ]

# ==========================================
# Dataset
# ==========================================

st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered,
    use_container_width=True,
    height=500
)

st.divider()

# ==========================================
# Download
# ==========================================

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="Filtered_Dataset.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()

# ==========================================
# Quick Statistics
# ==========================================

st.subheader("📈 Quick Statistics")

left, right = st.columns(2)

with left:

    st.write("### Salary Statistics")

    st.write(
        f"**Highest Salary:** ${filtered['Annual_salary(usd)'].max():,.0f}"
        if len(filtered) > 0 else "-"
    )

    st.write(
        f"**Lowest Salary:** ${filtered['Annual_salary(usd)'].min():,.0f}"
        if len(filtered) > 0 else "-"
    )

    st.write(
        f"**Average Salary:** ${filtered['Annual_salary(usd)'].mean():,.0f}"
        if len(filtered) > 0 else "-"
    )

with right:

    st.write("### Experience Statistics")

    st.write(
        f"**Highest Experience:** {filtered['Experience'].max()} Years"
        if len(filtered) > 0 else "-"
    )

    st.write(
        f"**Lowest Experience:** {filtered['Experience'].min()} Years"
        if len(filtered) > 0 else "-"
    )

    st.write(
        f"**Average Experience:** {filtered['Experience'].mean():.1f} Years"
        if len(filtered) > 0 else "-"
    )

st.divider()

st.caption(
    "Tech-Career & Job Market Analytics | Dataset Explorer | Developed by Ravinder Singh and Tanvir Singh Bains"
)
