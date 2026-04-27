import os

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ["PATH"]
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim, to_date


def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    input_path = os.path.join(project_root, "data", "raw", "ingested_air_quality.csv")
    output_dir = os.path.join(project_root, "data", "processed", "spark_output")
    final_output_path = os.path.join(project_root, "data", "processed", "sample_air_quality.csv")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    spark = (
        SparkSession.builder
        .appName("AirQualityDataCleaning")
        .master("local[*]")
        .getOrCreate()
    )

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(input_path)
    )

    clean_df = (
        df.select("city", "parameter", "value", "date")
        .dropna()
        .withColumn("city", trim(col("city")))
        .withColumn("parameter", lower(trim(col("parameter"))))
        .withColumn("value", col("value").cast("double"))
        .withColumn("date", to_date(col("date")))
        .dropna()
        .orderBy("city", "parameter", "date")
    )

    clean_df.coalesce(1).write.mode("overwrite").option("header", True).csv(output_dir)

    # Spark writes into a folder, so we copy the single CSV part file to our expected API path
    part_file = None
    for filename in os.listdir(output_dir):
        if filename.startswith("part-") and filename.endswith(".csv"):
            part_file = os.path.join(output_dir, filename)
            break

    if part_file is None:
        raise FileNotFoundError("Spark output CSV part file was not created.")

    with open(part_file, "r", encoding="utf-8") as src:
        with open(final_output_path, "w", encoding="utf-8") as dest:
            dest.write(src.read())

    print("PySpark processed dataset created successfully.")
    print(f"Input: {input_path}")
    print(f"Output: {final_output_path}")
    print(f"Rows: {clean_df.count()}")

    spark.stop()


if __name__ == "__main__":
    main()