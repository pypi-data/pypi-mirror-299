from pyspark.sql.functions import col, expr, coalesce
from .dlt_transformations import update_cdc_timestamp, apply_partitions, adjust_sequence_operation, compare_cdc_timestamp_and_commit_timestamp

# Define the transformation function dynamically
def create_bronze_table_definition(spark, dlt, table_name: str, files_path: str, file_format: str, partitions: dict, schema_exclude_columns: list, keys: list, time_diff_history_cdc_timestamp: int = 30):
    @dlt.table(
        name=f"bronze_{table_name}",
        comment="This is the bronze table.",
        temporary=False
    )
    def transform_cdc_to_bronze():
        df = spark.read.format(file_format).load(files_path)
        fields = [field for field in df.schema.fields if field.name not in schema_exclude_columns]
        schema_string = ', '.join([f"{field.name} {field.dataType.simpleString()}" for field in fields])
        return spark \
            .readStream \
            .format('cloudFiles') \
            .option("cloudFiles.format", file_format) \
            .option("cloudFiles.schemaHints", schema_string) \
            .load(files_path) \
            .withColumn('cdc_timestamp', col('cdc_timestamp').cast('timestamp')) \
            .transform(lambda df: compare_cdc_timestamp_and_commit_timestamp(df, keys)) \
            .transform(lambda df: update_cdc_timestamp(df, time_diff_history_cdc_timestamp)) \
            .transform(lambda df: apply_partitions(df, partitions))


    return transform_cdc_to_bronze



# Create silver streaming data
def silver_streaming_process(dlt, table_name: str, keys: list, partitions: dict, exclude_columns: list):
    dlt.create_streaming_table(
        name=table_name,
        table_properties={
            "delta.autoOptimize.optimizeWrite": "true",
            "delta.autoOptimize.autoCompact": "true"
        },
        comment = "This is the silver table with source in",
        partition_cols=partitions if partitions else None
    )

    dlt.apply_changes(
        target=table_name,
        source=f"bronze_{table_name}",
        keys=keys,
        sequence_by=col("cdc_timestamp"),
        apply_as_deletes=expr("Op = 'D'"),
        apply_as_truncates=expr("Op = 'T'"),
        except_column_list=["Op", "_rescued_data"] + exclude_columns,
        stored_as_scd_type=1
    )
