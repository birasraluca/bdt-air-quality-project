def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "ok"


def test_summary_endpoint(client):
    response = client.get("/api/summary")

    assert response.status_code == 200

    data = response.get_json()
    assert "records" in data
    assert "cities" in data
    assert "pollutants" in data
    assert "date_range" in data


def test_cities_endpoint(client):
    response = client.get("/api/cities")

    assert response.status_code == 200

    data = response.get_json()
    assert "cities" in data
    assert "Timisoara" in data["cities"]


def test_parameters_endpoint(client):
    response = client.get("/api/parameters")

    assert response.status_code == 200

    data = response.get_json()
    assert "parameters" in data
    assert "pm25" in data["parameters"]


def test_pollution_endpoint_success(client):
    response = client.get("/api/pollution?city=Timisoara&parameter=pm25")

    assert response.status_code == 200

    data = response.get_json()
    assert data["city"] == "Timisoara"
    assert data["parameter"] == "pm25"
    assert len(data["data"]) > 0


def test_pollution_endpoint_missing_params(client):
    response = client.get("/api/pollution?city=Timisoara")

    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data


def test_predict_endpoint_success(client):
    response = client.post(
        "/api/predict",
        json={
            "city": "Timisoara",
            "parameter": "pm25"
        }
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["city"] == "Timisoara"
    assert data["parameter"] == "pm25"
    assert "predicted_value" in data
    assert "predicted_date" in data


def test_predict_endpoint_missing_body(client):
    response = client.post("/api/predict", json={})

    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data


def test_predict_endpoint_invalid_city(client):
    response = client.post(
        "/api/predict",
        json={
            "city": "NopeCity",
            "parameter": "pm25"
        }
    )

    assert response.status_code == 404

    data = response.get_json()
    assert "error" in data