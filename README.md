# Tech-Career-Job-Market-Analytics
An interactive Data Science project that explores global technology job market trends, visualizes salary insights, and provides personalized career recommendations through a Streamlit web application.

# About the Project
Choosing the right career in the technology industry can be challenging because job roles, salaries, and required skills continue to evolve. This project was developed to simplify that process by analyzing a global technology job market dataset and presenting the information through an interactive dashboard.
The application allows users to explore salary trends, compare different occupations, analyze employment patterns, and understand how factors such as education, experience, company size, and location influence career opportunities. In addition to data analysis, the project also includes a Career Recommendation System that suggests suitable technology careers based on user inputs.
This project was developed as part of our Six Weeks Industrial Training and demonstrates the practical application of Data Science, Exploratory Data Analysis (EDA), and web application development using Python.

# Key Features
- Interactive dashboard with real-time job market insights.
- Exploratory Data Analysis (EDA) using multiple interactive visualizations.
- Salary analysis based on occupation, field, country, city, and years of experience.
- Education level and company size impact analysis on annual salary.
- Employment type distribution and workforce trend analysis.
- Correlation analysis between key job market attributes.
- Interactive world map displaying country-wise average annual salaries.
- Top-paying occupations and highest-paying cities visualization.
- Career Recommendation System based on education level, experience, and employment preference.
- Dataset Explorer for viewing and filtering job market records.
- User-friendly web interface developed using Streamlit.
- Interactive charts created with Plotly Express, Matplotlib, and Seaborn.
- Data cleaning and preprocessing using Pandas and NumPy.
- Live deployment on Streamlit Community Cloud for easy accessibility.
- Well-structured and responsive interface for an enhanced user experience.

# Project Structure
Tech-Career-Job-Market-Analytics
│
├── Career_Job_Market_Analysis/
│   ├── Home.py
│   ├── Cleaned_Project_DataSet.csv
│   ├── pages/
│   │   ├── Dashboard.py
│   │   ├── Data Insights.py
│   │   ├── Career Recommendation.py
│   │   ├── Dataset Explorer.py
│   │   └── Project Summary.py
│
├── Projectmaking.ipynb
├── README.md
└── requirements.txt

# Dashboard Modules
# Home
Introduces the project, explains its objectives, and provides a brief overview of the application.

# Dashboard
Displays important dataset statistics including total records, countries, cities, occupations, average salary, experience, and quick insights.

# Data Insights
Contains interactive visualizations such as:
Salary vs Experience
Salary by Occupation
Salary by Field
Salary by Company Size
Country Records
Education Impact on Salary
Employment Type Distribution
Correlation Heatmap
Job Distribution by Field
World Salary Map
Top 5 Occupation Salary Trends
Salary Distribution
Top 10 Highest Paying Cities

## Career Recommendation
Recommends suitable technology careers based on:
Education Level
Years of Experience
Employment Type

# Dataset Explorer
Allows users to explore and filter the dataset interactively.

#Project Summary
Provides information about the project, technologies used, conclusion, future scope, and developer credits.

# Live Demo
# Streamlit Application
https://tech-career-job-market-analytics-by-tanvir-and-ravinder.streamlit.app/

# Installation
Clone the repository
git clone https://github.com/your-username/Tech-Career-Job-Market-Analytics.git
Navigate to the project folder
cd Tech-Career-Job-Market-Analytics
Install the required libraries
pip install -r requirements.txt
Run the application
streamlit run Home.py

# Dataset
The project uses a Global Technology Job Market Dataset containing information related to:
Country
City
Occupation
Field
Annual Salary
Education Level
Experience
Company Size
Employment Type
Gender
Year
The dataset was cleaned and preprocessed using Pandas before performing Exploratory Data Analysis and developing the dashboard.

# Future Improvements
Add Machine Learning based salary prediction
Improve the Career Recommendation System
Integrate real-time job market data
Add advanced filtering and search options
Deploy with a cloud database
Develop a mobile-friendly interface

# Developers
Tanvir Bains
B.Tech CSE (Data Science)
Rayat Bahra Institute of Engineering & Nanotechnology, Hoshiarpur
Ravinder Kumar
B.Tech CSE (Data Science)
Rayat Bahra Institute of Engineering & Nanotechnology, Hoshiarpur


# License
This project has been developed for educational and learning purposes as part of our Industrial Training and B.Tech curriculum.
