import os

from ingestion.fetch_openaq_data import main as fetch_openaq_data
from processing.clean_air_quality_data_spark import main as run_spark_processing
from pipeline.pipeline_logger import (
    create_run_metadata,
    start_step,
    finish_step,
    fail_step,
    finish_run,
    count_csv_rows,
    save_run_metadata,
)


def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def main():
    print("Starting OpenAQ air quality data pipeline...\n")

    project_root = get_project_root()

    raw_path = os.path.join(project_root, "data", "raw", "openaq_measurements.csv")
    processed_path = os.path.join(project_root, "data", "processed", "sample_air_quality.csv")

    metadata = create_run_metadata()

    try:
        metadata = start_step(metadata, "ingestion")
        fetch_openaq_data()
        metadata = finish_step(metadata, "ingestion")

        metadata["raw_rows"] = count_csv_rows(raw_path)

        print("\nOpenAQ ingestion completed.\n")

        metadata = start_step(metadata, "processing")
        run_spark_processing()
        metadata = finish_step(metadata, "processing")

        metadata["processed_rows"] = count_csv_rows(processed_path)

        print("\nSpark processing completed.\n")

        metadata = finish_run(metadata, status="success")
        log_path = save_run_metadata(metadata)

        print("Pipeline finished successfully.")
        print(f"Pipeline log saved to: {log_path}")

    except Exception as error:
        current_step = None

        for step_name, step_data in metadata["steps"].items():
            if step_data["status"] == "running":
                current_step = step_name
                break

        if current_step:
            metadata = fail_step(metadata, current_step, error)

        metadata = finish_run(metadata, status="failed", error=error)
        log_path = save_run_metadata(metadata)

        print("Pipeline failed.")
        print(f"Pipeline log saved to: {log_path}")
        print(f"Error: {error}")

        raise


if __name__ == "__main__":
    main()