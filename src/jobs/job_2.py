from typing import Optional
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame

def query_2(input_table_name: str, base_table: str, date: str) -> str:
    query = f"""
        WITH yesterday AS (
                SELECT * FROM {input_table_name} WHERE date = DATE_SUB(CAST('{date}' AS DATE), 1)
        ),
        today AS (
            SELECT host,CAST(DATE_TRUNC('day', event_time) AS DATE) AS date,COUNT(1) FROM {base_table} WHERE DATE_TRUNC('day', event_time) = DATE('{date}') GROUP BY host,DATE_TRUNC('day', event_time)
        )
        SELECT
        COALESCE(y.host, t.host) AS host,
        CASE
            WHEN y.host_activity_datelist IS NOT NULL THEN ARRAY(t.date) || y.host_activity_datelist
            ELSE ARRAY(t.date) END AS host_activity_datelist,
            DATE('{date}') AS date
        FROM yesterday AS y FULL OUTER JOIN today AS t ON y.host = t.host
    """
    return query

def job_2(spark_session: SparkSession, input_table_name: str,base_table: str,date: str) -> Optional[DataFrame]:
  return spark_session.sql(query_2(input_table_name, base_table, date))
