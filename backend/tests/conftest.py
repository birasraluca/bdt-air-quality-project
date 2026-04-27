import os
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()

    test_dataset_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../data/processed/sample_air_quality.csv"
        )
    )

    app.config.update({
        "TESTING": True,
        "DATASET_PATH": test_dataset_path
    })

    with app.test_client() as client:
        yield client