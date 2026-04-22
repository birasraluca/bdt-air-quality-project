import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from the project root .env file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

load_dotenv(ENV_PATH)

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])