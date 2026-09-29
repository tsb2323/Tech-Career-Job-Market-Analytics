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
    # CREATE RECOMMENDATION LIST
    # ==========================================

    recommendations = []


    # ==========================================
    # PROCESS EACH OCCUPATION
    # ==========================================

    for occupation, group in working.groupby(
        "Occupation"
    ):

        # --------------------------------------
        # EDUCATION MATCH
        # --------------------------------------

        education_score = (
            group["EducationMatch"].mean() * 100
        )


        # --------------------------------------
        # EMPLOYMENT MATCH
        # --------------------------------------

        employment_score = (
            group["EmploymentMatch"].mean() * 100
        )


        # --------------------------------------
        # FIND CLOSEST EXPERIENCE
        # --------------------------------------

        closest_index = (
            group["ExperienceGap"].idxmin()
        )

        closest_experience = (
            group.loc[
                closest_index,
                "Experience"
            ]
        )


        # --------------------------------------
        # EXPERIENCE SCORE
        # --------------------------------------

        closest_gap = (
            group.loc[
                closest_index,
                "ExperienceGap"
            ]
        )

        experience_score = (
            100 / (closest_gap + 1)
        )


        # --------------------------------------
        # FINAL MATCH SCORE
        # --------------------------------------

        match_score = (

            experience_score * 0.50

            +

            education_score * 0.30

            +

            employment_score * 0.20

        )


        # --------------------------------------
        # FIELD
        # --------------------------------------

        field_mode = (
            group["Field"].mode()
        )

        if not field_mode.empty:

            field = field_mode.iloc[0]

        else:

            field = group["Field"].iloc[0]


        # --------------------------------------
        # COUNTRY
        # --------------------------------------

        country_mode = (
            group["Country"].mode()
        )

        if not country_mode.empty:

            country = country_mode.iloc[0]

        else:

            country = group["Country"].iloc[0]


        # --------------------------------------
        # AVERAGE SALARY
        # --------------------------------------

        average_salary = (
            group["Annual_salary(usd)"].mean()
        )


        # --------------------------------------
        # NUMBER OF JOBS
        # --------------------------------------

        jobs_available = len(group)


        # --------------------------------------
        # STORE RESULT
        # --------------------------------------

        recommendations.append({

            "Occupation":
                occupation,

            "Field":
                field,

            "Country":
                country,

            "Closest_Experience":
                closest_experience,

            "Average_Salary":
                average_salary,

            "Jobs_Available":
                jobs_available,

            "Match_Score":
                match_score,

            "Education_Score":
                education_score,

            "Employment_Score":
                employment_score,

            "Experience_Score":
                experience_score

        })


    # ==========================================
    # CREATE RECOMMENDATION DATAFRAME
    # ==========================================

    recommendation = pd.DataFrame(
        recommendations
    )


    # ==========================================
    # SALARY FACTOR
    # ==========================================

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

    # 95% comes from user's profile.
    # 5% comes from salary as a secondary factor.

    recommendation["FinalScore"] = (

        recommendation["Match_Score"] * 0.95

        +

        recommendation["SalaryFactor"] * 0.05

    )


    # ==========================================
    # SORT RECOMMENDATIONS
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
    # SUCCESS MESSAGE
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


            # ----------------------------------
            # LEFT COLUMN
            # ----------------------------------

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


            # ----------------------------------
            # RIGHT COLUMN
            # ----------------------------------

            with col2:

                st.write(
                    f"**🧑 Closest Matching Experience:** "
                    f"{row['Closest_Experience']:.1f} Years"
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
    # RECOMMENDATION SUMMARY
    # ==========================================

    st.divider()

    st.subheader(
        "📌 Recommendation Summary"
    )


    best = recommendation.iloc[0]


    st.success(
        f"""
### Best Career Match

**Occupation:** {best['Occupation']}

**Field:** {best['Field']}

**Country:** {best['Country']}

**Closest Matching Experience:** {best['Closest_Experience']:.1f} Years

**Average Salary:** ${best['Average_Salary']:,.0f}

**Match Score:** {best['FinalScore']:.1f}%

This occupation provides the strongest match
based on your selected education level,
employment type and years of experience.
"""
    )


    # ==========================================
    # RECOMMENDATION TABLE
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

            "Closest_Experience":
                "Matched Experience",

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
                "Matched Experience",
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