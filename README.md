# Urban Air Quality Analysis and Prediction Using Big Data Techniques

## Project Overview

This project implements an urban air quality data platform focused on the collection, cleaning, analysis, monitoring, and prediction of air pollution data.

The system uses OpenAQ monitoring location metadata for Romanian cities and generates a reproducible daily air-quality time series for selected pollutants. The dataset is processed using PySpark, exposed through a Flask backend API, and visualized in a React dashboard.

The project demonstrates key Big Data concepts, especially the **velocity dimension**, by implementing a repeatable ingestion and processing pipeline that can be rerun as new data becomes available.

---

## Real-Life Problem

Urban air pollution is an important environmental and public health issue. Pollutants such as PM2.5 and PM10 can affect respiratory health, reduce quality of life, and indicate poor environmental conditions in cities.

This project addresses the problem of monitoring and analyzing urban air quality by providing:

- cleaned air-quality data
- descriptive statistics
- city and pollutant comparisons
- pollution trend analysis
- anomaly/pollution alert detection
- next-day pollution prediction
- pipeline monitoring metadata

---

## Big Data Dimension

The project focuses mainly on the **velocity** dimension of Big Data.

Although the local demonstration dataset is not larger than 500 MB, air-quality measurements represent time-series sensor data that can be produced continuously. The implemented pipeline supports repeated ingestion, processing, analytics, and monitoring of air-quality data over time.

The velocity aspect is demonstrated through:

- repeatable data ingestion
- automated PySpark processing
- pipeline execution logging
- latest pipeline run monitoring
- API-based access to updated analytics
- dashboard visualization of processed results

---

## Dataset Description

The project uses the OpenAQ API to retrieve monitoring location metadata for Romania.

For each selected monitoring location and pollutant, the ingestion script generates a reproducible daily air-quality time series. The generated values include realistic characteristics such as:

- city-specific pollution levels
- pollutant-specific baseline values
- seasonal variation
- random daily noise
- weekend effects
- occasional pollution spikes

The final dataset focuses on:

- `pm25`
- `pm10`

The ingestion script also attempts to retrieve NO2 metadata, but no NO2 rows are returned for the selected Romanian bounding box in the current OpenAQ query. Therefore, the final project focuses on PM2.5 and PM10.

---

## Architecture

```text
OpenAQ API
   ↓
Python Ingestion Script
   ↓
data/raw/openaq_measurements.csv
   ↓
PySpark Cleaning and Processing
   ↓
data/processed/sample_air_quality.csv
   ↓
Flask Backend API
   ↓
Analytics + Prediction Endpoints
   ↓
React Dashboard
```

---

## Tech Stack

### Backend and Data Processing

- Python
- PySpark
- pandas
- scikit-learn
- Flask
- Flask-CORS
- OpenAQ API

### Frontend

- React
- Vite
- Axios
- Recharts

### Other Tools

- Git/GitHub
- dotenv
- JSON pipeline logs

---

## Project Structure

```text
backend/
├── analytics/
│   ├── data_service.py
│   ├── data_quality_service.py
│   ├── pipeline_service.py
│   └── summary_service.py
├── app/
│   ├── config.py
│   ├── routes.py
│   └── utils.py
├── ingestion/
│   └── fetch_openaq_data.py
├── models/
│   ├── model_info_service.py
│   └── prediction_service.py
├── pipeline/
│   └── pipeline_logger.py
├── processing/
│   └── clean_air_quality_data_spark.py
├── requirements.txt
├── run.py
└── run_pipeline.py

frontend/
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── api.js
│   └── main.jsx

data/
├── raw/
├── processed/
└── pipeline_logs/
```

---

## Main Features

### 1. Data Ingestion

The ingestion script retrieves Romanian monitoring location metadata from OpenAQ and generates daily air-quality time-series data for each selected city and pollutant.

The generated dataset includes:

- city
- pollutant parameter
- pollution value
- date
- unit
- source
- latitude
- longitude
- location ID
- original OpenAQ location name

---

### 2. Data Cleaning and Processing

Data processing is performed using PySpark.

The cleaning pipeline includes:

- schema validation
- column selection
- text trimming
- pollutant name normalization
- numeric type casting
- date parsing
- missing value removal
- duplicate removal
- invalid pollution value filtering
- city name normalization
- derived date columns:
  - year
  - month
  - day
- pollutant group classification

The final processed dataset is saved to:

```text
data/processed/sample_air_quality.csv
```

---

### 3. Descriptive Analytics

The backend provides descriptive analytics for:

- dataset summary
- available cities
- available pollutants
- pollution time series
- average pollution by city
- latest pollution values by city
- trend analysis
- descriptive statistics
- monthly averages
- city profiles
- pollution alerts/anomaly detection

---

### 4. Predictive Analytics

The predictive analytics component uses a baseline Linear Regression model.

The model predicts the next daily pollutant value for a selected city and pollutant.

The prediction uses:

- feature: `day_index`
- target: pollution value
- chronological 80/20 train-test split
- Linear Regression
- previous-value baseline comparison

Evaluation metrics include:

- MAE
- RMSE
- R2 score

---

### 5. Data Quality Monitoring

The backend exposes a data quality endpoint that reports:

- total rows
- date range
- available pollutants
- missing expected pollutants
- missing values
- duplicate rows
- invalid values
- records by city
- records by pollutant
- city/pollutant coverage

This supports the data clean-up requirement and makes the cleaning process transparent.

---

### 6. Pipeline Monitoring

Each pipeline execution is logged with metadata including:

- run ID
- start time
- finish time
- duration
- status
- ingestion status
- processing status
- raw row count
- processed row count
- error message, if any

This demonstrates that the pipeline can be repeatedly executed and monitored.

---

### 7. Frontend Dashboard

The React dashboard includes:

- city selector
- pollutant selector
- time-series pollution chart
- trend analysis card
- prediction card
- pollution alert/anomaly card
- monthly average chart
- descriptive statistics table
- data quality panel
- latest pipeline run panel

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

---

### 2. Create a virtual environment

Make sure Python 3.11 is installed.

On Windows:

```bash
py -3.11 -m venv venv
```

---

### 3. Activate the virtual environment

On Windows:

```bash
venv\\Scripts\\activate
```

---

### 4. Install backend requirements

```bash
pip install -r backend/requirements.txt
```

---

### 5. Configure environment variables

Copy the example environment file:

```bash
copy .env.example .env
```

Then add your OpenAQ API key inside `.env`:

```env
OPENAQ_API_KEY=your_api_key_here
```

---

## Running the Project

### 1. Run the data pipeline

From the project root:

```bash
python backend/run_pipeline.py
```

This performs:

```text
OpenAQ ingestion → raw CSV generation → PySpark processing → processed CSV generation → pipeline log creation
```

---

### 2. Run the Flask backend

```bash
python backend/run.py
```

The backend will be available at:

```text
http://localhost:5000
```

---

### 3. Run the React frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The dashboard will be available at:

```text
http://localhost:5173
```

---

## API Endpoints

### Health and General

#### `GET /`

Returns a basic backend status message.

#### `GET /health`

Returns a simple health check response.

---

### Metadata

#### `GET /api/cities`

Returns the list of available cities.

#### `GET /api/parameters`

Returns the list of available pollutant parameters.

#### `GET /api/dataset/info`

Returns the path of the processed dataset used by the backend.

---

### Dataset Summary

#### `GET /api/summary`

Returns an overall dataset summary, including:

- total records
- number of cities
- number of pollutants
- pollutant list
- date range
- value statistics
- records by city
- records by pollutant

---

### Descriptive Analytics

#### `GET /api/pollution?city=<city>&parameter=<parameter>`

Returns time-series pollution data for a selected city and pollutant.

Example:

```text
/api/pollution?city=Brasov&parameter=pm10
```

---

#### `GET /api/summary/by-city?parameter=<parameter>`

Returns average pollutant value by city for a selected pollutant.

Example:

```text
/api/summary/by-city?parameter=pm25
```

---

#### `GET /api/pollution/latest?parameter=<parameter>`

Returns the latest available pollutant value for each city.

Example:

```text
/api/pollution/latest?parameter=pm10
```

---

#### `GET /api/trend?city=<city>&parameter=<parameter>`

Returns trend analysis for a selected city and pollutant.

Example:

```text
/api/trend?city=Brasov&parameter=pm10
```

---

#### `GET /api/descriptive/statistics`

Returns descriptive statistics for all cities and pollutants.

#### `GET /api/descriptive/statistics?parameter=<parameter>`

Returns descriptive statistics for a selected pollutant.

Example:

```text
/api/descriptive/statistics?parameter=pm10
```

---

#### `GET /api/descriptive/city-profile?city=<city>`

Returns a city-level pollution profile.

Example:

```text
/api/descriptive/city-profile?city=Brasov
```

---

#### `GET /api/descriptive/monthly-average?city=<city>&parameter=<parameter>`

Returns monthly average pollution values.

Example:

```text
/api/descriptive/monthly-average?city=Brasov&parameter=pm10
```

---

### Pollution Alerts

#### `GET /api/alerts?city=<city>&parameter=<parameter>`

Returns unusually high pollution days using the following anomaly detection method:

```text
threshold = mean + 2 * standard deviation
```

Example:

```text
/api/alerts?city=Brasov&parameter=pm10
```

---

### Predictive Analytics

#### `POST /api/predict`

Predicts the next pollutant value for a selected city and parameter.

The prediction endpoint uses a baseline Linear Regression model based on the time index of historical pollutant measurements.

Example request body:

```json
{
  "city": "Brasov",
  "parameter": "pm10"
}
```

Example response:

```json
{
  "city": "Brasov",
  "parameter": "pm10",
  "predicted_value": 31.95,
  "predicted_date": "2024-12-31",
  "based_on_records": 365,
  "train_records": 292,
  "test_records": 73,
  "mae": 3.12,
  "rmse": 4.23,
  "r2_score": 0.65,
  "baseline": {
    "method": "previous value",
    "mae": 3.45,
    "rmse": 4.67
  }
}
```

---

### Model Information

#### `GET /api/model/info`

Returns information about the predictive model, including:

- model name
- model type
- purpose
- features
- target
- evaluation method
- metrics
- baseline

---

### Data Quality

#### `GET /api/data-quality`

Returns a data quality report, including:

- total rows
- date range
- available pollutants
- missing expected pollutants
- missing values
- duplicate rows
- invalid values
- records by city
- records by parameter
- city/pollutant coverage

---

### Pipeline Monitoring

#### `GET /api/pipeline/latest`

Returns metadata for the latest pipeline execution.

#### `GET /api/pipeline/runs`

Returns all saved pipeline execution logs.

---

## Example Workflow

A typical execution flow is:

```bash
python backend/run_pipeline.py
python backend/run.py
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

## Notes for Windows and PySpark

On Windows, PySpark may require `winutils.exe` and `HADOOP_HOME` to be configured.

Example:

```text
C:\\hadoop\\bin\\winutils.exe
```

The processing script currently sets:

```python
HADOOP_HOME = C:\\hadoop
```

If PySpark fails on Windows, check that:

- Java is installed
- `JAVA_HOME` is configured if needed
- `winutils.exe` exists in `C:\\hadoop\\bin`
- `HADOOP_HOME` points to `C:\\hadoop`

---

## Generated Files and Git Ignore

The dataset files are generated by the pipeline and should not be committed to Git.

Ignored generated files include:

```text
data/raw/*.csv
data/processed/*.csv
data/processed/spark_output/
data/pipeline_logs/*.json
```

The folders are kept using `.gitkeep` files.

---

## Limitations

Current limitations include:

- The project uses real OpenAQ monitoring location metadata, but daily measurement values are generated for demonstration.
- The local dataset is smaller than 500 MB, so the project focuses on the velocity dimension rather than the volume dimension.
- The final dataset currently contains PM2.5 and PM10 only.
- NO2 was attempted but no rows were returned for the selected Romanian bounding box.
- The predictive model is a simple baseline Linear Regression model.
- The system is designed for local execution, not production deployment.

---

## Future Work

Possible future improvements include:

- integrating real historical measurement values from OpenAQ sensors
- adding true streaming ingestion
- adding more pollutants if available
- improving the predictive model with additional features
- comparing multiple models such as Random Forest or Gradient Boosting
- adding caching for API responses
- containerizing the application with Docker
- deploying the backend and frontend
- adding authentication for administrative endpoints
- adding automatic scheduled pipeline execution

---

## Conclusion

This project demonstrates a complete air-quality data platform using Big Data techniques. It includes data ingestion, PySpark-based cleaning and processing, descriptive analytics, anomaly detection, predictive analytics, pipeline monitoring, and frontend visualization.

The project focuses on the velocity dimension of Big Data by implementing a repeatable data pipeline that can ingest, process, analyze, and expose updated air-quality data through an API and dashboard.

<img width="1874" height="770" alt="image" src="https://github.com/user-attachments/assets/2434621f-f8fd-40f5-8485-f45295b4f205" />
<img width="1854" height="754" alt="image" src="https://github.com/user-attachments/assets/de5030e2-a477-4610-8059-30453777d031" />
<img width="622" height="598" alt="image" src="https://github.com/user-attachments/assets/0a4ea56f-9fe5-46dd-8db1-74c0b8c093ae" />
<img width="1848" height="850" alt="image" src="https://github.com/user-attachments/assets/819cd1ce-5888-46b2-85ca-bf85631c35b2" />
<img width="1844" height="631" alt="image" src="https://github.com/user-attachments/assets/d532694e-d2fc-4012-b91b-ad858defa58f" />
<img width="1842" height="528" alt="image" src="https://github.com/user-attachments/assets/123e508a-3e27-482c-8b44-f30ca8078a8f" />



