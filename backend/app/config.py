import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    DATASET_PATH = os.getenv(
        "DATASET_PATH",
        os.path.join(PROJECT_ROOT, "data", "processed", "sample_air_quality.csv")
    )