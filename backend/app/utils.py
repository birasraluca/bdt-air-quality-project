from flask import current_app


def get_dataset_path():
    return current_app.config["DATASET_PATH"]