from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return {"message": "BDT Air Quality Backend running"}

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app