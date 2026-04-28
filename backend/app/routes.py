from flask import Blueprint, jsonify, request
from analytics.summary_service import get_project_summary
from analytics.data_service import (
    get_available_cities,
    get_available_parameters,
    get_pollution_timeseries,
    get_average_by_city,
    get_latest_by_city,
    get_pollution_trend
)
from models.prediction_service import predict_next_value
from app.utils import get_dataset_path
from models.model_info_service import get_model_info

api_bp = Blueprint("api", __name__)


@api_bp.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "BDT Air Quality Backend is running"
    })


@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })


@api_bp.route("/api/summary", methods=["GET"])
def summary():
    summary_data = get_project_summary()
    return jsonify(summary_data)


@api_bp.route("/api/cities", methods=["GET"])
def cities():
    return jsonify({
        "cities": get_available_cities()
    })


@api_bp.route("/api/parameters", methods=["GET"])
def parameters():
    return jsonify({
        "parameters": get_available_parameters()
    })


@api_bp.route("/api/pollution", methods=["GET"])
def pollution():
    city = request.args.get("city")
    parameter = request.args.get("parameter")

    if not city or not parameter:
        return jsonify({
            "error": "Both 'city' and 'parameter' query parameters are required"
        }), 400

    result = get_pollution_timeseries(city, parameter)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result)


@api_bp.route("/api/pollution/latest", methods=["GET"])
def pollution_latest():
    parameter = request.args.get("parameter")

    if not parameter:
        return jsonify({
            "error": "'parameter' query parameter is required"
        }), 400

    result = get_latest_by_city(parameter)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result)


@api_bp.route("/api/summary/by-city", methods=["GET"])
def summary_by_city():
    parameter = request.args.get("parameter")

    if not parameter:
        return jsonify({
            "error": "'parameter' query parameter is required"
        }), 400

    result = get_average_by_city(parameter)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result)


@api_bp.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    city = data.get("city")
    parameter = data.get("parameter")

    if not city or not parameter:
        return jsonify({
            "error": "Both 'city' and 'parameter' are required"
        }), 400

    result = predict_next_value(city, parameter)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result)


@api_bp.route("/api/dataset/info", methods=["GET"])
def dataset_info():
    return jsonify({
        "dataset_path": get_dataset_path()
    })


@api_bp.route("/api/trend", methods=["GET"])
def trend():
    city = request.args.get("city")
    parameter = request.args.get("parameter")

    if not city or not parameter:
        return jsonify({
            "error": "Both 'city' and 'parameter' query parameters are required"
        }), 400

    result = get_pollution_trend(city, parameter)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result)


@api_bp.route("/api/model/info", methods=["GET"])
def model_info():
    return jsonify(get_model_info())