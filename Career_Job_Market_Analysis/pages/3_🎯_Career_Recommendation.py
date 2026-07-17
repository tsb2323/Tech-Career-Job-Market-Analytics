import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Career Recommendation",
    page_icon="🎯",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_Project_DataSet.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ==========================================
# TITLE
# ==========================================

st.title("🎯 Career Recommendation System")

st.write("""
Find the most suitable careers based on your:

- 🎓 Education Level
- 💼 Employment Type
- 🧑 Years of Experience

The recommendations are generated using the Global Job Market Dataset.
""")

st.divider()

# ==========================================
# USER INPUTS
# ==========================================

left, right = st.columns(2)

with left:

    education = st.selectbox(
        "🎓 Education Level",
        sorted(df["Education_level"].dropna().unique())
    )

    employment = st.selectbox(
        "💼 Employment Type",
        sorted(df["Employment_type"].dropna().unique())
    )

with right:

    experience = st.slider(
        "🧑 Years of Experience",
        int(df["Experience"].min()),
        int(df["Experience"].max()),
        2
    )

st.divider()

# ==========================================
# RECOMMEND BUTTON
# ==========================================

if st.button("🔍 Recommend Careers", use_container_width=True):

    working = df.copy()

    # ---------------------------------------
    # Match Scores
    # ---------------------------------------

    working["EducationScore"] = (
        working["Education_level"] == education
    ).astype(int)

    working["EmploymentScore"] = (
        working["Employment_type"] == employment
    ).astype(int)

    working["ExperienceGap"] = abs(
        working["Experience"] - experience
    )

    working["ExperienceScore"] = (
        1 / (working["ExperienceGap"] + 1)
    )

    # Total Score
    working["Score"] = (
        working["ExperienceScore"] * 0.60 +
        working["EducationScore"] * 0.20 +
        working["EmploymentScore"] * 0.20
    )
        # ==========================================
    # Group by Occupation
    # ==========================================

    recommendation = (
        working.groupby("Occupation")
        .agg(
            Field=("Field", "first"),
            Country=("Country", lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]),
            Average_Experience=("Experience", "mean"),
            Average_Salary=("Annual_salary(usd)", "mean"),
            Jobs_Available=("Occupation", "count"),
            Match_Score=("Score", "mean")
        )
        .reset_index()
    )

    # Convert score to percentage
    recommendation["Match_Score"] = (
        recommendation["Match_Score"] /
        recommendation["Match_Score"].max()
    ) * 100

    # Sort recommendations
    recommendation = recommendation.sort_values(
        by=[
            "Match_Score",
            "Jobs_Available",
            "Average_Salary"
        ],
        ascending=[False, False, False]
    )

    # Top 10
    recommendation = recommendation.head(10)

    st.success(f"Top {len(recommendation)} Career Recommendations")

    st.divider()

    # ==========================================
    # Display Recommendations
    # ==========================================

    for i, row in recommendation.iterrows():

        with st.container(border=True):

            st.subheader(
                f"🏆 Recommendation {i+1}: {row['Occupation']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**📂 Field:** {row['Field']}"
                )

                st.write(
                    f"**🌍 Country:** {row['Country']}"
                )

                st.write(
                    f"**💼 Jobs Available:** {int(row['Jobs_Available'])}"
                )

            with col2:

                st.write(
                    f"**🧑 Average Experience:** {row['Average_Experience']:.1f} Years"
                )

                st.write(
                    f"**⭐ Match Score:** {row['Match_Score']:.1f}%"
                )

                st.write(
                    f"**💰 Average Salary:** ${row['Average_Salary']:,.0f}"
                )

    st.divider()

    # ==========================================
    # Summary
    # ==========================================

    st.subheader("📌 Recommendation Summary")

    best = recommendation.iloc[0]

    st.success(
        f"""
### Best Career Match

**Occupation:** {best['Occupation']}

**Field:** {best['Field']}

**Country:** {best['Country']}

**Average Experience:** {best['Average_Experience']:.1f} Years

**Average Salary:** ${best['Average_Salary']:,.0f}

**Match Score:** {best['Match_Score']:.1f}%

This occupation best matches your selected education level,
employment type and years of experience.
"""
    )

    st.divider()

    st.dataframe(
        recommendation.rename(
            columns={
                "Occupation": "Occupation",
                "Field": "Field",
                "Country": "Country",
                "Average_Experience": "Avg Experience",
                "Average_Salary": "Avg Salary (USD)",
                "Jobs_Available": "Jobs",
                "Match_Score": "Match Score (%)"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "Tech-Career & Job Market Analytics  | Career Recommendation System | Developed by Ravinder Singh and Tanvir Singh Bains"
)