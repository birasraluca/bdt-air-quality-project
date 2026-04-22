from flask import Blueprint, jsonify
from analytics.summary_service import get_project_summary

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