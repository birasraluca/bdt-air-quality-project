import json
import os


def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def get_logs_dir():
    return os.path.join(get_project_root(), "data", "pipeline_logs")


def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_pipeline_runs():
    logs_dir = get_logs_dir()

    if not os.path.exists(logs_dir):
        return {
            "runs": [],
            "message": "No pipeline logs found yet. Run the pipeline first."
        }

    runs = []

    for filename in os.listdir(logs_dir):
        if not filename.endswith(".json"):
            continue

        if filename == "latest.json":
            continue

        file_path = os.path.join(logs_dir, filename)

        try:
            runs.append(read_json_file(file_path))
        except json.JSONDecodeError:
            continue

    runs = sorted(
        runs,
        key=lambda item: item.get("started_at", ""),
        reverse=True
    )

    return {
        "count": len(runs),
        "runs": runs
    }


def get_latest_pipeline_run():
    latest_path = os.path.join(get_logs_dir(), "latest.json")

    if not os.path.exists(latest_path):
        return {
            "message": "No pipeline logs found yet. Run the pipeline first."
        }

    return read_json_file(latest_path)