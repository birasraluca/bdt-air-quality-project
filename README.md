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

### 4. .env setup

copy .env.example .env

## API Endpoints

### Health and general
- `GET /`
  - Returns a basic backend status message.

- `GET /health`
  - Returns a simple health check response.

### Metadata
- `GET /api/cities`
  - Returns the list of available cities.

- `GET /api/parameters`
  - Returns the list of available pollutant parameters.

### Descriptive analytics
- `GET /api/summary`
  - Returns overall dataset summary:
    - total records
    - number of cities
    - pollutants
    - date range

- `GET /api/pollution?city=<city>&parameter=<parameter>`
  - Returns time-series pollution data for a selected city and pollutant.

- `GET /api/summary/by-city?parameter=<parameter>`
  - Returns average pollutant value by city for a selected parameter.

- `GET /api/pollution/latest?parameter=<parameter>`
  - Returns the latest available pollutant value for each city.

- `GET /api/model/info`
  - Returns information about the predictive model used by the backend.

### Predictive analytics
- `POST /api/predict`
  - Predicts the next pollutant value for a selected city and parameter.
  - The prediction endpoint uses a baseline Linear Regression model based on the time index of historical pollutant measurements. The response includes MAE and RMSE evaluation metrics.

#### Example request body
{
  "city": "Timisoara",
  "parameter": "pm25"
}

#### Example response
{
  "based_on_records": 5,
  "city": "Timisoara",
  "parameter": "pm25",
  "predicted_date": "2024-01-06",
  "predicted_value": 14.8
}

## Data Pipeline

The project contains two processing options:

### Pandas processing

python backend/ingestion/load_sample_data.py
python backend/processing/clean_air_quality_data.py

On Windows, PySpark may require winutils.exe and HADOOP_HOME to be configured.

## Running the Data Pipeline

The full local data pipeline can be executed with:

python backend/run_pipeline.py

## Running the Frontend

cd frontend
npm install
npm run dev

The dashboard will be available at:
http://localhost:5173