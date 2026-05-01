import os
import shutil

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ["PATH"]

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    lower,
    trim,
    to_date,
    year,
    month,
    dayofmonth,
    when,
    lit,
    count,
)


REQUIRED_COLUMNS = {"city", "parameter", "value", "date"}


def validate_schema(df):
    available_columns = set(df.columns)
    missing_columns = REQUIRED_COLUMNS - available_columns

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    input_path = os.path.join(project_root, "data", "raw", "openaq_measurements.csv")
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

    validate_schema(df)

    initial_rows = df.count()

    available_columns = df.columns

    selected_columns = [
        "city",
        "parameter",
        "value",
        "date",
    ]

    optional_columns = [
        "unit",
        "source",
        "latitude",
        "longitude",
        "location_id",
        "original_location_name",
    ]

    for column_name in optional_columns:
        if column_name in available_columns:
            selected_columns.append(column_name)

    clean_df = df.select(*selected_columns)

    clean_df = (
        clean_df
        .withColumn("city", trim(col("city")))
        .withColumn("parameter", lower(trim(col("parameter"))))
        .withColumn("value", col("value").cast("double"))
        .withColumn("date", to_date(col("date")))
    )

    if "unit" in clean_df.columns:
        clean_df = clean_df.withColumn("unit", trim(col("unit")))
    else:
        clean_df = clean_df.withColumn("unit", lit("µg/m³"))

    if "source" in clean_df.columns:
        clean_df = clean_df.withColumn("source", trim(col("source")))
    else:
        clean_df = clean_df.withColumn("source", lit("OpenAQ"))

    # Remove invalid / incomplete rows
    clean_df = clean_df.dropna(subset=["city", "parameter", "value", "date"])

    # Keep only supported pollutants for this project
    clean_df = clean_df.filter(col("parameter").isin("pm25", "pm10", "no2"))

    # Remove physically invalid pollution values
    clean_df = clean_df.filter((col("value") >= 0) & (col("value") <= 1000))

    # Normalize city names
    clean_df = clean_df.withColumn(
        "city",
        when(lower(col("city")).isin("bucharest", "bucuresti"), "Bucharest")
        .when(lower(col("city")).isin("timisoara", "timișoara"), "Timisoara")
        .when(lower(col("city")).contains("cluj"), "Cluj-Napoca")
        .when(lower(col("city")).contains("brasov"), "Brasov")
        .when(lower(col("city")).contains("craiova"), "Craiova")
        .when(lower(col("city")).contains("iasi"), "Iasi")
        .when(lower(col("city")).contains("targu"), "Targu Mures")
        .otherwise(col("city"))
    )

    # Remove duplicate measurements
    duplicate_subset = ["city", "parameter", "date"]

    if "location_id" in clean_df.columns:
        duplicate_subset.append("location_id")

    clean_df = clean_df.dropDuplicates(duplicate_subset)

    # Add derived date columns useful for analytics and ML
    clean_df = (
        clean_df
        .withColumn("year", year(col("date")))
        .withColumn("month", month(col("date")))
        .withColumn("day", dayofmonth(col("date")))
        .withColumn(
            "pollutant_group",
            when(col("parameter").isin("pm25", "pm10"), "particulate_matter")
            .when(col("parameter") == "no2", "gas")
            .otherwise("other")
        )
        .orderBy("city", "parameter", "date")
    )

    final_rows = clean_df.count()
    removed_rows = initial_rows - final_rows

    quality_summary = clean_df.groupBy("parameter").agg(
        count("*").alias("records")
    )

    print("Data quality summary by pollutant:")
    quality_summary.show()

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    clean_df.coalesce(1).write.mode("overwrite").option("header", True).csv(output_dir)

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
    print(f"Initial rows: {initial_rows}")
    print(f"Final rows: {final_rows}")
    print(f"Removed rows during cleaning: {removed_rows}")

    spark.stop()


if __name__ == "__main__":
    main()