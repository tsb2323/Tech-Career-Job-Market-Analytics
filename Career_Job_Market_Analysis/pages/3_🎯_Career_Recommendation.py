import streamlit as st
import pandas as pd
from pathlib import Path

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

    BASE_DIR = Path(__file__).resolve().parent
    DATA_PATH = BASE_DIR.parent / "Cleaned_Project_DataSet.csv"

    df = pd.read_csv(DATA_PATH)

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
        sorted(
            df["Education_level"]
            .dropna()
            .unique()
        )
    )

    employment = st.selectbox(
        "💼 Employment Type",
        sorted(
            df["Employment_type"]
            .dropna()
            .unique()
        )
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

if st.button(
    "🔍 Recommend Careers",
    use_container_width=True
):

    working = df.copy()


    # ==========================================
    # EXPERIENCE DIFFERENCE
    # ==========================================

    working["ExperienceGap"] = abs(
        working["Experience"] - experience
    )


    # ==========================================
    # EXPERIENCE SCORE
    # ==========================================

    # Exact experience = 100
    # 1 year difference = 50
    # 2 years difference = 33.3
    # etc.

    working["ExperienceScore"] = (
        100 /
        (working["ExperienceGap"] + 1)
    )


    # ==========================================
    # EDUCATION MATCH
    # ==========================================

    working["EducationMatch"] = (
        working["Education_level"] == education
    ).astype(int)


    # ==========================================
    # EMPLOYMENT MATCH
    # ==========================================

    working["EmploymentMatch"] = (
        working["Employment_type"] == employment
    ).astype(int)


    # ==========================================
    # GROUP BY OCCUPATION
    # ==========================================

    recommendations = []


    for occupation, group in working.groupby(
        "Occupation"
    ):

        # --------------------------------------
        # EDUCATION MATCH %
        # --------------------------------------

        education_score = (
            group["EducationMatch"].mean() * 100
        )


        # --------------------------------------
        # EMPLOYMENT MATCH %
        # --------------------------------------

        employment_score = (
            group["EmploymentMatch"].mean() * 100
        )


        # --------------------------------------
        # EXPERIENCE SCORE
        # --------------------------------------

        # Sort by closest experience
        closest = group.sort_values(
            by="ExperienceGap"
        )


        # Use the closest 20% of records
        # instead of averaging all records

        top_count = max(
            1,
            int(len(closest) * 0.20)
        )

        closest_records = closest.head(
            top_count
        )


        experience_score = (
            closest_records["ExperienceScore"]
            .mean()
        )


        # --------------------------------------
        # FINAL MATCH SCORE
        # --------------------------------------

        final_score = (

            experience_score * 0.50 +

            education_score * 0.30 +

            employment_score * 0.20

        )


        # --------------------------------------
        # OTHER INFORMATION
        # --------------------------------------

        field = group["Field"].mode()

        if not field.empty:
            field = field.iloc[0]
        else:
            field = group["Field"].iloc[0]


        country = group["Country"].mode()

        if not country.empty:
            country = country.iloc[0]
        else:
            country = group["Country"].iloc[0]


        average_experience = (
            group["Experience"].mean()
        )


        average_salary = (
            group["Annual_salary(usd)"].mean()
        )


        jobs_available = len(group)


        recommendations.append({

            "Occupation": occupation,

            "Field": field,

            "Country": country,

            "Average_Experience":
                average_experience,

            "Average_Salary":
                average_salary,

            "Jobs_Available":
                jobs_available,

            "Match_Score":
                final_score,

            "Education_Score":
                education_score,

            "Employment_Score":
                employment_score,

            "Experience_Score":
                experience_score

        })


    # ==========================================
    # CREATE DATAFRAME
    # ==========================================

    recommendation = pd.DataFrame(
        recommendations
    )


    # ==========================================
    # SECONDARY NORMALIZATION
    # ==========================================

    # Salary is used only as a very small
    # secondary factor when scores are close.

    salary_min = (
        recommendation["Average_Salary"].min()
    )

    salary_max = (
        recommendation["Average_Salary"].max()
    )


    if salary_max > salary_min:

        recommendation["SalaryFactor"] = (

            (
                recommendation["Average_Salary"]
                - salary_min
            )
            /
            (
                salary_max
                - salary_min
            )

        ) * 100

    else:

        recommendation["SalaryFactor"] = 50


    # ==========================================
    # FINAL SCORE
    # ==========================================

    # Salary has only a 5% influence.
    # Main recommendation still comes from
    # the user's three inputs.

    recommendation["FinalScore"] = (

        recommendation["Match_Score"] * 0.95

        +

        recommendation["SalaryFactor"] * 0.05

    )


    # ==========================================
    # SORT
    # ==========================================

    recommendation = recommendation.sort_values(

        by=[
            "FinalScore",
            "Jobs_Available"
        ],

        ascending=[
            False,
            False
        ]

    )


    # ==========================================
    # TOP 10
    # ==========================================

    recommendation = (

        recommendation
        .head(10)
        .reset_index(drop=True)

    )


    # ==========================================
    # DISPLAY SUCCESS MESSAGE
    # ==========================================

    st.success(
        f"Top {len(recommendation)} Career Recommendations"
    )

    st.divider()


    # ==========================================
    # DISPLAY RECOMMENDATIONS
    # ==========================================

    for i, row in recommendation.iterrows():

        with st.container(border=True):

            st.subheader(
                f"🏆 Recommendation {i + 1}: "
                f"{row['Occupation']}"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    f"**📂 Field:** "
                    f"{row['Field']}"
                )

                st.write(
                    f"**🌍 Country:** "
                    f"{row['Country']}"
                )

                st.write(
                    f"**💼 Jobs Available:** "
                    f"{int(row['Jobs_Available'])}"
                )


            with col2:

                st.write(
                    f"**🧑 Average Experience:** "
                    f"{row['Average_Experience']:.1f} Years"
                )

                st.write(
                    f"**⭐ Match Score:** "
                    f"{row['FinalScore']:.1f}%"
                )

                st.write(
                    f"**💰 Average Salary:** "
                    f"${row['Average_Salary']:,.0f}"
                )


    # ==========================================
    # SUMMARY
    # ==========================================

    st.divider()

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

**Match Score:** {best['FinalScore']:.1f}%

This recommendation is based on your selected
education level, employment type and years of
experience.
"""
    )


    # ==========================================
    # DATA TABLE
    # ==========================================

    st.divider()

    display_df = recommendation.rename(

        columns={

            "Occupation":
                "Occupation",

            "Field":
                "Field",

            "Country":
                "Country",

            "Average_Experience":
                "Avg Experience",

            "Average_Salary":
                "Avg Salary (USD)",

            "Jobs_Available":
                "Jobs",

            "FinalScore":
                "Match Score (%)"

        }

    )


    st.dataframe(
        display_df[
            [
                "Occupation",
                "Field",
                "Country",
                "Avg Experience",
                "Avg Salary (USD)",
                "Jobs",
                "Match Score (%)"
            ]
        ],

        use_container_width=True,

        hide_index=True
    )


# ==========================================
# FOOTER
# ==========================================

st.caption(
    "Tech-Career & Job Market Analytics | "
    "Career Recommendation System | "
    "Developed by Ravinder Singh and Tanvir Singh Bains"
)