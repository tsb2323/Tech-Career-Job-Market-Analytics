import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Data Insights",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv("Cleaned_Project_DataSet.csv")

# ==========================================
# PAGE TITLE
# ==========================================

st.title("📈 Data Insights Dashboard")

st.markdown("""
Explore the **Global Job Market Dataset** through interactive visualizations.

This dashboard provides insights into:

- 🌍 Country-wise Analysis
- 💰 Salary Analysis
- 🎓 Education Impact
- 💼 Employment Trends
- 🏢 Company Size Analysis
- 📈 Experience & Time Trends
""")

st.divider()

# ===========================================================
# 🌍 COUNTRY ANALYSIS
# ===========================================================

st.header("🌍 Country Analysis")

st.caption(
    "Explore the geographical distribution of records and average salaries across different countries."
)

# -------------------------------
# COUNTRY RECORDS
# -------------------------------

country_count = (
    df["Country"]
    .value_counts()
    .reset_index()
)

country_count.columns = ["Country", "Count"]

fig_country = px.treemap(
    country_count,
    path=["Country"],
    values="Count",
    color="Count",
    color_continuous_scale="Viridis",
    title="Country Records Distribution"
)

fig_country.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=550,
    margin=dict(t=60, l=20, r=20, b=20)
)

st.plotly_chart(fig_country, use_container_width=True)

st.info(
    "The treemap shows the number of records available for each country in the dataset."
)

st.divider()
top_country = country_count.loc[country_count["Count"].idxmax()]

st.success(
    f"""
### 🔍 Key Insight

• **{top_country['Country']}** has the highest number of records with **{top_country['Count']}** entries.

• Countries with larger rectangles contain more job records in the dataset.

• The dataset is not evenly distributed across all countries.
"""
)

# -------------------------------
# COUNTRY VS SALARY
# -------------------------------

country_salary = (
    df.groupby("Country", as_index=False)["Annual_salary(usd)"]
    .mean()
)

fig_salary = px.choropleth(
    country_salary,
    locations="Country",
    locationmode="country names",
    color="Annual_salary(usd)",
    hover_name="Country",
    color_continuous_scale="Viridis_r",
    title="Average Annual Salary by Country"
)

fig_salary.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=600
)

st.plotly_chart(fig_salary, use_container_width=True)

st.info(
    "This world map compares the average annual salary across different countries."
)

st.divider()
highest_country = country_salary.loc[
    country_salary["Annual_salary(usd)"].idxmax()
]

lowest_country = country_salary.loc[
    country_salary["Annual_salary(usd)"].idxmin()
]

st.success(
    f"""
### 🔍 Key Insight

• **{highest_country['Country']}** has the highest average salary.

• **{lowest_country['Country']}** has the lowest average salary.

• Average salary:
**${highest_country['Annual_salary(usd)']:,.0f}**

• Salary levels differ across countries, reflecting regional job markets.
"""
)

# ===========================================================
# 💰 SALARY ANALYSIS
# ===========================================================

st.header("💰 Salary Analysis")

st.caption(
    "Understand how annual salaries are distributed throughout the dataset."
)

# -------------------------------
# SALARY DISTRIBUTION
# -------------------------------

fig, ax = plt.subplots(figsize=(10,5))

sns.set_style("darkgrid")

sns.histplot(
    data=df,
    x="Annual_salary(usd)",
    bins=30,
    color="royalblue",
    edgecolor="black",
    linewidth=0.8,
    alpha=0.8,
    kde=True,
    ax=ax
)

ax.set_title(
    "Distribution of Annual Salaries",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("Annual Salary (USD)")

ax.set_ylabel("Number of Employees")

ax.grid(axis="y", linestyle="--", alpha=0.4)

st.pyplot(fig)

st.info(
    "This histogram shows how annual salaries are distributed among employees."
)

st.divider()
st.success(
    f"""
### 🔍 Key Insight

• Average Salary: **${df['Annual_salary(usd)'].mean():,.0f}**

• Median Salary: **${df['Annual_salary(usd)'].median():,.0f}**

• Salaries range from **${df['Annual_salary(usd)'].min():,.0f}** 
  to **${df['Annual_salary(usd)'].max():,.0f}**.

• Most salaries are concentrated around the middle of the distribution.
"""
)


# ===========================================================
# 🏙 TOP 10 CITIES BY SALARY
# ===========================================================

st.header("🏙 Top 10 Highest Paying Cities")

st.caption(
    "Compare the cities offering the highest average annual salaries."
)

city_salary = (
    df.groupby(["City", "Country"])["Annual_salary(usd)"]
    .mean()
    .sort_values()
    .tail(10)
)

labels = [
    f"{city}, {country}"
    for city, country in city_salary.index
]

fig, ax = plt.subplots(figsize=(11,6))

ax.hlines(
    y=labels,
    xmin=0,
    xmax=city_salary.values,
    color="gray",
    linewidth=4
)

ax.scatter(
    city_salary.values,
    labels,
    color="darkorange",
    s=220
)

for i, value in enumerate(city_salary.values):

    ax.text(
        value + 6000,
        i,
        f"${value:,.0f}",
        va="center",
        fontsize=10,
        fontweight="bold"
    )

ax.set_title(
    "Top 10 Cities by Average Annual Salary",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("Average Salary (USD)")
ax.set_ylabel("City")

ax.grid(axis="x", linestyle="--", alpha=0.4)

st.pyplot(fig)

best_city = city_salary.idxmax()

st.success(f"""
### 🔍 Key Insight

• **{best_city[0]} ({best_city[1]})** has the highest average salary.

• The chart highlights the highest-paying cities in the dataset.

• Salary levels vary considerably across cities.
""")

st.divider()

# ===========================================================
# 🎓 EDUCATION VS SALARY
# ===========================================================

st.header("🎓 Education Impact on Salary")

st.caption(
    "Analyze how education level influences annual salary."
)

fig = px.box(
    df,
    x="Education_level",
    y="Annual_salary(usd)",
    color="Education_level",
    title="Education Level vs Annual Salary"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=550
)

st.plotly_chart(fig, use_container_width=True)

edu = (
    df.groupby("Education_level")["Annual_salary(usd)"]
    .mean()
)

highest = edu.idxmax()

st.success(f"""
### 🔍 Key Insight

• **{highest}** has the highest average salary.

• Higher education generally leads to higher salaries.

• Salary varies within every education level.
""")

st.divider()

# ===========================================================
# 💼 EMPLOYMENT TYPE
# ===========================================================

st.header("💼 Employment Type Distribution")

employment_counts = df["Employment_type"].value_counts()

fig, ax = plt.subplots(figsize=(5,5))

ax.pie(
    employment_counts.values,
    labels=employment_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

ax.set_title("Employment Type Distribution")

st.pyplot(fig)

most_common = employment_counts.idxmax()

st.success(f"""
### 🔍 Key Insight

• **{most_common}** is the most common employment type.

• The chart shows the percentage of each employment category.

• Full-time jobs dominate if they occupy the largest slice.
""")

st.divider()

# ===========================================================
# 🏢 COMPANY SIZE
# ===========================================================

st.header("🏢 Company Size Analysis")

company_salary = (
    df.groupby("Company_size", as_index=False)["Annual_salary(usd)"]
    .mean()
)

fig = px.bar(
    company_salary,
    x="Company_size",
    y="Annual_salary(usd)",
    color="Annual_salary(usd)",
    color_continuous_scale="Viridis",
    text="Annual_salary(usd)",
    title="Average Salary by Company Size"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=550
)

st.plotly_chart(fig, use_container_width=True)

highest_company = (
    company_salary.loc[
        company_salary["Annual_salary(usd)"].idxmax(),
        "Company_size"
    ]
)

st.success(f"""
### 🔍 Key Insight

• **{highest_company}** companies offer the highest average salary.

• Company size has a noticeable impact on employee compensation.

• Larger organizations generally provide higher salaries.
""")

st.divider()

# ===========================================================
# 📂 JOB DISTRIBUTION BY FIELD
# ===========================================================

st.header("📂 Job Distribution by Field")

field_count = df["Field"].value_counts()

fig, ax = plt.subplots(figsize=(7,7))

ax.pie(
    field_count,
    labels=field_count.index,
    autopct="%1.1f%%",
    startangle=90,
    explode=[0.05]*len(field_count),
    wedgeprops={
        "edgecolor":"white",
        "linewidth":1
    }
)

ax.set_title("Job Distribution by Field")

st.pyplot(fig)

top_field = field_count.idxmax()

st.success(f"""
### 🔍 Key Insight

• **{top_field}** contains the highest number of jobs.

• Some fields contribute significantly more records than others.

• The dataset covers multiple career domains.
""")

st.divider()

# ===========================================================
# 💼 SALARY BY OCCUPATION
# ===========================================================

st.header("💼 Average Salary by Occupation")

occupation_salary = (
    df.groupby("Occupation", as_index=False)["Annual_salary(usd)"]
    .mean()
    .sort_values(by="Annual_salary(usd)")
)

fig = px.bar(
    occupation_salary,
    x="Annual_salary(usd)",
    y="Occupation",
    orientation="h",
    color_discrete_sequence=["teal"],
    text="Annual_salary(usd)",
    title="Average Annual Salary by Occupation"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside",
    cliponaxis=False
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=650,
    margin=dict(l=180, r=100)
)

st.plotly_chart(fig, use_container_width=True)

highest_occ = occupation_salary.iloc[-1]

st.success(f"""
### 🔍 Key Insight

• **{highest_occ['Occupation']}** has the highest average salary.

• Average Salary: **${highest_occ['Annual_salary(usd)']:,.0f}**

• Salary varies significantly among occupations.
""")

st.divider()





# ===========================================================
# 📅 TIME ANALYSIS
# ===========================================================

st.header("📅 Time Analysis")

st.caption(
    "Analyze how salaries have changed over the years for the most common occupations."
)

top_occ = df["Occupation"].value_counts().head(5).index

df_top = df[df["Occupation"].isin(top_occ)]

salary_trend = df_top.pivot_table(
    values="Annual_salary(usd)",
    index="Year",
    columns="Occupation",
    aggfunc="mean"
)

fig, ax = plt.subplots(figsize=(10,6))

for occupation in salary_trend.columns:

    ax.plot(
        salary_trend.index,
        salary_trend[occupation],
        marker="o",
        linewidth=2,
        label=occupation
    )

ax.set_title(
    "Average Annual Salary by Year for Top Occupations",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("Year")
ax.set_ylabel("Average Salary (USD)")

ax.grid(True)

ax.legend(
    title="Occupation",
    bbox_to_anchor=(1.02,1),
    loc="upper left"
)

st.pyplot(fig)

highest_year = (
    df.groupby("Year")["Annual_salary(usd)"]
    .mean()
    .idxmax()
)

st.success(f"""
### 🔍 Key Insight

• **{highest_year}** has the highest average salary.

• Salary trends vary across occupations.

• The graph helps compare salary growth over time.
""")

st.divider()

# ===========================================================
# 📈 EXPERIENCE ANALYSIS
# ===========================================================

st.header("📈 Experience Analysis")

st.caption(
    "Understand how salary changes with years of experience."
)

salary_exp = (
    df.groupby("Experience")["Annual_salary(usd)"]
    .mean()
)

fig, ax = plt.subplots(figsize=(9,5))

ax.plot(
    salary_exp.index,
    salary_exp.values,
    marker="o",
    linewidth=3,
    color="darkviolet"
)

ax.set_title(
    "Average Annual Salary by Years of Experience",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("Years of Experience")
ax.set_ylabel("Average Salary (USD)")

ax.grid(True)

st.pyplot(fig)

st.success(f"""
### 🔍 Key Insight

• Average salary generally increases with experience.

• Employees with more years of experience tend to earn higher salaries.

• Average Experience in the dataset:
**{df['Experience'].mean():.1f} Years**
""")

st.divider()

# ===========================================================
# 🔥 CORRELATION HEATMAP
# ===========================================================

st.header("🔥 Correlation Analysis")

st.caption(
    "Explore the relationship between Experience, Year and Annual Salary."
)

corr = df[
    [
        "Experience",
        "Year",
        "Annual_salary(usd)"
    ]
].corr()

fig, ax = plt.subplots(figsize=(6,5))

sns.heatmap(
    corr,
    annot=True,
    cmap="icefire",
    fmt=".2f",
    square=True,
    linewidths=2,
    annot_kws={
        "size":12,
        "weight":"bold"
    },
    cbar_kws={
        "shrink":0.8
    },
    ax=ax
)

ax.set_title(
    "Correlation Heatmap",
    fontsize=16,
    fontweight="bold"
)

st.pyplot(fig)

corr_value = corr.loc["Experience", "Annual_salary(usd)"]

st.success(f"""
### 🔍 Key Insight

• Correlation between Experience and Salary:

**{corr_value:.2f}**

• Positive values indicate that salary tends to increase as experience increases.

• The heatmap summarizes relationships among the selected variables.
""")

st.divider()

# ===========================================================
# 📌 DASHBOARD SUMMARY
# ===========================================================

st.header("📌 Overall Dashboard Summary")

st.info("""
### Main Findings

✅ Salary generally increases with experience.

✅ Higher education levels are associated with higher salaries.

✅ Large companies tend to offer better salaries.

✅ Salaries vary significantly across occupations.

✅ Countries show different salary distributions.

✅ Employment type influences salary patterns.

✅ Different career fields have different earning potential.
""")

st.divider()

# ===========================================================
# 👨‍💻 FOOTER
# ===========================================================

st.markdown("---")

st.caption(
    "Tech-Career & Job Market Analytics | Semester Training Project | Developed by Ravinder Singh and Tanvir Singh Bains"
)
