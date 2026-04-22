# Urban Air Quality Analysis and Prediction Using Big Data Techniques

## Team Members
- Biras Raluca
- Campan Dana
- Ivan Teodora
- Longodor Andreea
- Pop Iulian

## Project Overview
This project analyzes large-scale urban air quality data and applies descriptive and predictive analytics to identify pollution patterns and forecast air quality levels.

## Tech Stack
- Python
- PySpark
- pandas
- scikit-learn
- Flask

## Repository Structure

bdt-air-quality-project/
│
├── backend/                 # Backend services (Flask API, data processing, ML)
│   ├── app/                 # Flask app (routes, API endpoints)
│   ├── ingestion/           # Data collection (OpenAQ API, downloads)
│   ├── processing/          # Data cleaning and transformation (PySpark)
│   ├── analytics/           # Descriptive analytics (statistics, aggregations)
│   ├── models/              # Predictive models (scikit-learn)
│   ├── tests/               # Backend tests
│   ├── requirements.txt     # Python dependencies for backend
│   └── run.py               # Entry point for running the backend server
│
├── frontend/                # Frontend application (React / Streamlit / other)
│
├── data/                    # Dataset storage
│   ├── raw/                 # Raw, unprocessed data
│   └── processed/           # Cleaned and transformed data
│
├── notebooks/               # Jupyter notebooks (exploration, experiments)
│
├── docs/                    # Documentation (reports, diagrams, slides)
│
├── README.md                # Project overview and setup instructions
└── .gitignore               # Ignored files (venv, cache, etc.)

## Workflow
- Data ingestion
- Data cleaning
- Descriptive analytics
- Predictive analytics
- Backend integration
- Presentation/reporting

## Setup Instructions

### 1. Create virtual environment

Make sure you have Python 3.11 installed.

py -3.11 -m venv venv

### 2. Activate virtual environment

venv/Scripts/Activate

### 3. Install requirements

pip install -r backend/requirements.txt