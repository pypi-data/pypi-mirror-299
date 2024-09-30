from pyspark.sql import DataFrame
from pyspark.sql.types import TimestampType, DateType
from pyspark.sql.functions import col, expr, greatest, when, datediff


def apply_partitions(df: DataFrame, partitions: dict):
    # apply partitioning to the dataframe
    if partitions:
        for col_name, expression in partitions.items():
            if expression.replace(" ", "") != '':
                df = df.withColumn(col_name, expr(expression))
    return df
    
def update_cdc_timestamp(df: DataFrame, time_diff_threshold: int) -> DataFrame:
    # if cdc_timestamp is null or time difference is greater than threshold, set it to the max timestamp in the row
    timestamp_cols = [col.name for col in df.schema.fields if isinstance(col.dataType, (TimestampType, DateType)) and col.name != 'cdc_timestamp']

    if timestamp_cols:
        max_timestamp_per_row = None

        if len(timestamp_cols) > 1:
            max_timestamp_per_row = greatest(*[col(col_name) for col_name in timestamp_cols])
            # temp fix for market table if possible need take last_update_date becouse of market table contnin close time
            if 'last_update_date' in timestamp_cols:
                max_timestamp_per_row = when(
                                                col('last_update_date').isNotNull(), 
                                                col('last_update_date')
                                            ).otherwise(max_timestamp_per_row)
            # temp fix for artemis table if possible need take last_update_date becouse of market table contnin close time
            if 'version' in timestamp_cols:
                max_timestamp_per_row = when(
                                                col('version').isNotNull(), 
                                                col('version')
                                            ).otherwise(max_timestamp_per_row)        
        else:
            max_timestamp_per_row = col(timestamp_cols[0])
            
        df = df.withColumn(
            'cdc_timestamp',
                when(
                    (col('cdc_timestamp').isNull()) | 
                    (datediff(col('cdc_timestamp'), max_timestamp_per_row) > time_diff_threshold), 
                    max_timestamp_per_row
                ).otherwise(col('cdc_timestamp'))
            )
    return df


def adjust_sequence_operation(df: DataFrame, uniq_columns: list) -> DataFrame:
    window_spec = Window.partitionBy(uniq_columns).orderBy("cdc_timestamp")

    df_with_lag = df.withColumn("prev_op", lag("Op").over(window_spec)) \
                    .withColumn("prev_cdc_timestamp", lag("cdc_timestamp").over(window_spec))

    window_spec_all = Window.partitionBy(uniq_columns)
    df_with_max_u_timestamp = df_with_lag.withColumn(
        "min_u_cdc_timestamp", spark_min(when(col("Op") == "U", col("cdc_timestamp"))).over(window_spec_all)
    )

    df_adjusted = df_with_max_u_timestamp.withColumn(
        "cdc_timestamp",
        when((col("Op") == "I") & (col("min_u_cdc_timestamp").isNotNull()), col("min_u_cdc_timestamp") -F.expr("interval 1 milliseconds")).otherwise(col("cdc_timestamp"))
    )
    df_final = df_adjusted.drop("prev_op", "prev_cdc_timestamp", "min_u_cdc_timestamp")
    return df_final
