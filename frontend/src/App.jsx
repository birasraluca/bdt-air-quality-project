import { useEffect, useState } from "react";
import {
  getSummary,
  getCities,
  getParameters,
  getPollution,
  getTrend,
  getPrediction,
  getModelInfo,
  getDescriptiveStatistics,
  getMonthlyAverage,
} from "./api";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

function App() {
  const [summary, setSummary] = useState(null);
  const [cities, setCities] = useState([]);
  const [parameters, setParameters] = useState([]);

  const [selectedCity, setSelectedCity] = useState("");
  const [selectedParameter, setSelectedParameter] = useState("");

  const [pollutionData, setPollutionData] = useState([]);
  const [trend, setTrend] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [descriptiveStats, setDescriptiveStats] = useState([]);
  const [monthlyAverage, setMonthlyAverage] = useState([]);

  useEffect(() => {
    async function loadInitialData() {
      try {
        setError("");

        const [summaryData, citiesData, parametersData, modelData] =
          await Promise.all([
            getSummary(),
            getCities(),
            getParameters(),
            getModelInfo(),
          ]);

        const normalizedCities = Array.isArray(citiesData)
          ? citiesData
          : citiesData.cities || citiesData.data || [];

        const normalizedParameters = Array.isArray(parametersData)
          ? parametersData
          : parametersData.parameters || parametersData.data || [];

        setSummary(summaryData);
        setCities(normalizedCities);
        setParameters(normalizedParameters);
        setModelInfo(modelData);

        if (normalizedCities.length > 0) {
          setSelectedCity(normalizedCities[0]);
        }

        if (normalizedParameters.length > 0) {
          setSelectedParameter(normalizedParameters[0]);
        }
      } catch (err) {
        console.error(err);
        setError("Could not load initial dashboard data. Make sure Flask is running.");
      }
    }

    loadInitialData();
  }, []);

  useEffect(() => {
    async function loadAnalytics() {
      if (!selectedCity || !selectedParameter) return;

      try {
        setLoading(true);
        setError("");

        const [pollution, trendData, predictionData, statsData, monthlyData] =
          await Promise.all([
            getPollution(selectedCity, selectedParameter),
            getTrend(selectedCity, selectedParameter),
            getPrediction(selectedCity, selectedParameter),
            getDescriptiveStatistics(selectedParameter),
            getMonthlyAverage(selectedCity, selectedParameter),
          ]);

        const normalizedPollutionData = Array.isArray(pollution)
          ? pollution
          : pollution.data || [];

        setPollutionData(normalizedPollutionData);
        setTrend(trendData);
        setPrediction(predictionData);
        setDescriptiveStats(statsData.statistics || []);
        setMonthlyAverage(monthlyData.data || []);
      } catch (err) {
        console.error(err);
        setError("Could not load analytics for the selected city and pollutant.");
      } finally {
        setLoading(false);
      }
    }

    loadAnalytics();
  }, [selectedCity, selectedParameter]);

  const latestValue =
    pollutionData.length > 0
      ? pollutionData[pollutionData.length - 1].value
      : null;

  return (
    <div className="app">
      <header className="hero">
        <div>
          <p className="eyebrow">Big Data Technologies Project</p>
          <h1>Air Quality Data Platform</h1>
          <p className="subtitle">
            A data pipeline for ingesting, processing, analyzing, and predicting
            air quality measurements using Python, PySpark, Flask, and React.
          </p>
        </div>
      </header>

      {error && <div className="error-box">{error}</div>}

      <section className="controls">
        <div className="control-group">
          <label>City</label>
          <select
            value={selectedCity}
            onChange={(event) => setSelectedCity(event.target.value)}
          >
            {Array.isArray(cities) &&
              cities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
          </select>
        </div>

        <div className="control-group">
          <label>Pollutant</label>
          <select
            value={selectedParameter}
            onChange={(event) => setSelectedParameter(event.target.value)}
          >
            {Array.isArray(parameters) &&
              parameters.map((parameter) => (
                <option key={parameter} value={parameter}>
                  {parameter}
                </option>
              ))}
          </select>
        </div>
      </section>

      <section className="cards">
        <div className="card">
          <p className="card-label">Total Records</p>
          <h2>{summary?.total_records ?? "—"}</h2>
        </div>

        <div className="card">
          <p className="card-label">Cities</p>
          <h2>{cities.length || "—"}</h2>
        </div>

        <div className="card">
          <p className="card-label">Pollutants</p>
          <h2>{parameters.length || "—"}</h2>
        </div>

        <div className="card">
          <p className="card-label">Latest Value</p>
          <h2>
            {latestValue !== null && latestValue !== undefined
              ? Number(latestValue).toFixed(2)
              : "—"}
          </h2>
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="panel chart-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Time Series</p>
              <h2>
                {selectedParameter} levels in {selectedCity}
              </h2>
            </div>
            {loading && <span className="badge">Loading...</span>}
          </div>

          <div className="chart-wrapper">
            {pollutionData.length > 0 ? (
              <ResponsiveContainer width="100%" height={350}>
                <LineChart data={pollutionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="value"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="empty-state">No pollution data available.</p>
            )}
          </div>
        </div>

        <div className="side-panels">
          <div className="panel">
            <p className="eyebrow">Trend Analysis</p>
            <h2>Trend</h2>

            {trend ? (
              <div className="metric-list">
                <p>
                  <strong>Direction:</strong>{" "}
                  {trend.trend_direction || trend.direction || "N/A"}
                </p>
                <p>
                  <strong>Change:</strong>{" "}
                  {trend.change !== undefined
                    ? Number(trend.change).toFixed(2)
                    : trend.absolute_change !== undefined
                    ? Number(trend.absolute_change).toFixed(2)
                    : trend.value_change !== undefined
                    ? Number(trend.value_change).toFixed(2)
                    : "N/A"}
                </p>
                <p>
                  <strong>Percentage Change:</strong>{" "}
                  {trend.percentage_change !== undefined
                    ? `${Number(trend.percentage_change).toFixed(2)}%`
                    : "N/A"}
                </p>
              </div>
            ) : (
              <p className="empty-state">No trend data available.</p>
            )}
          </div>

          <div className="panel">
            <p className="eyebrow">Predictive Analytics</p>
            <h2>Next Day Prediction</h2>

            {prediction ? (
              <div className="metric-list">
                <p>
                  <strong>Predicted Next Day Value:</strong>{" "}
                  {prediction.predicted_value !== undefined
                    ? Number(prediction.predicted_value).toFixed(2)
                    : "N/A"}
                </p>
                <p>
                  <strong>MAE:</strong>{" "}
                  {prediction.mae !== undefined
                    ? Number(prediction.mae).toFixed(3)
                    : prediction.model?.mae !== undefined
                    ? Number(prediction.model.mae).toFixed(3)
                    : "N/A"}
                </p>
                <p>
                  <strong>RMSE:</strong>{" "}
                  {prediction.rmse !== undefined
                    ? Number(prediction.rmse).toFixed(3)
                    : prediction.model?.rmse !== undefined
                    ? Number(prediction.model.rmse).toFixed(3)
                    : "N/A"}
                </p>
                <p>
                  <strong>R² Score:</strong>{" "}
                  {prediction.r2_score !== undefined && prediction.r2_score !== null
                    ? Number(prediction.r2_score).toFixed(3)
                    : prediction.model?.r2_score !== undefined && prediction.model?.r2_score !== null
                    ? Number(prediction.model.r2_score).toFixed(3)
                    : "N/A"}
                </p>
                <p>
                  <strong>Predicted Date:</strong>{" "}
                  {prediction.predicted_date || "N/A"}
                </p>
              </div>
            ) : (
              <p className="empty-state">No prediction available.</p>
            )}
          </div>

          <div className="panel">
            <p className="eyebrow">Model Info</p>
            <h2>Linear Regression</h2>

            {modelInfo ? (
              <div className="metric-list">
                <p>
                  <strong>Model:</strong>{" "}
                  {modelInfo.model_name || modelInfo.model || modelInfo.model_type || "Linear Regression"}
                </p>
                <p>
                  <strong>Target:</strong>{" "}
                  {modelInfo.target || "Air pollution value"}
                </p>
                <p>
                  <strong>Features:</strong>{" "}
                  {Array.isArray(modelInfo.features)
                    ? modelInfo.features.join(", ")
                    : modelInfo.features || "day_index"}
                </p>
              </div>
            ) : (
              <p className="empty-state">No model info available.</p>
            )}
          </div>
        </div>
      </section>
      <section className="analytics-section">
        <div className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Descriptive Analytics</p>
              <h2>
                Monthly Average for {selectedParameter} in {selectedCity}
              </h2>
            </div>
          </div>

          <div className="chart-wrapper">
            {monthlyAverage.length > 0 ? (
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={monthlyAverage}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="avg_value" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="empty-state">No monthly average data available.</p>
            )}
          </div>
        </div>
      </section>

      <section className="analytics-section">
        <div className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Descriptive Statistics</p>
              <h2>City Comparison for {selectedParameter}</h2>
            </div>
          </div>

          {descriptiveStats.length > 0 ? (
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>City</th>
                    <th>Pollutant</th>
                    <th>Records</th>
                    <th>Min</th>
                    <th>Max</th>
                    <th>Mean</th>
                    <th>Median</th>
                    <th>Std</th>
                  </tr>
                </thead>
                <tbody>
                  {descriptiveStats.map((row) => (
                    <tr key={`${row.city}-${row.parameter}`}>
                      <td>{row.city}</td>
                      <td>{row.parameter}</td>
                      <td>{row.records}</td>
                      <td>{Number(row.min).toFixed(2)}</td>
                      <td>{Number(row.max).toFixed(2)}</td>
                      <td>{Number(row.mean).toFixed(2)}</td>
                      <td>{Number(row.median).toFixed(2)}</td>
                      <td>{Number(row.std).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="empty-state">No descriptive statistics available.</p>
          )}
        </div>
      </section>
    </div>
  );
}

export default App;