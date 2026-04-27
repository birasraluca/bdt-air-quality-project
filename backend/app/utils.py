import os
from flask import current_app


def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def get_dataset_path():
    dataset_path = current_app.config["DATASET_PATH"]

    if os.path.isabs(dataset_path):
        return dataset_path

    return os.path.abspath(os.path.join(get_project_root(), dataset_path))