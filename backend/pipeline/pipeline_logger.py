import json
import os
from datetime import datetime


def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def get_logs_dir():
    project_root = get_project_root()
    logs_dir = os.path.join(project_root, "data", "pipeline_logs")
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


def create_run_metadata():
    started_at = datetime.now()

    return {
        "run_id": started_at.strftime("%Y%m%d_%H%M%S"),
        "started_at": started_at.isoformat(timespec="seconds"),
        "finished_at": None,
        "duration_seconds": None,
        "status": "running",
        "steps": {
            "ingestion": {
                "status": "pending",
                "started_at": None,
                "finished_at": None,
            },
            "processing": {
                "status": "pending",
                "started_at": None,
                "finished_at": None,
            }
        },
        "raw_rows": None,
        "processed_rows": None,
        "error": None
    }


def start_step(metadata, step_name):
    metadata["steps"][step_name]["status"] = "running"
    metadata["steps"][step_name]["started_at"] = datetime.now().isoformat(timespec="seconds")
    return metadata


def finish_step(metadata, step_name):
    metadata["steps"][step_name]["status"] = "success"
    metadata["steps"][step_name]["finished_at"] = datetime.now().isoformat(timespec="seconds")
    return metadata


def fail_step(metadata, step_name, error):
    metadata["steps"][step_name]["status"] = "failed"
    metadata["steps"][step_name]["finished_at"] = datetime.now().isoformat(timespec="seconds")
    metadata["status"] = "failed"
    metadata["error"] = str(error)
    return metadata


def finish_run(metadata, status="success", error=None):
    finished_at = datetime.now()

    metadata["finished_at"] = finished_at.isoformat(timespec="seconds")
    metadata["status"] = status
    metadata["error"] = str(error) if error else None

    started_at = datetime.fromisoformat(metadata["started_at"])
    metadata["duration_seconds"] = round((finished_at - started_at).total_seconds(), 2)

    return metadata


def count_csv_rows(file_path):
    if not os.path.exists(file_path):
        return 0

    with open(file_path, "r", encoding="utf-8") as file:
        # subtract header row
        return max(sum(1 for _ in file) - 1, 0)


def save_run_metadata(metadata):
    logs_dir = get_logs_dir()
    output_path = os.path.join(logs_dir, f"{metadata['run_id']}.json")

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    latest_path = os.path.join(logs_dir, "latest.json")

    with open(latest_path, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    return output_path