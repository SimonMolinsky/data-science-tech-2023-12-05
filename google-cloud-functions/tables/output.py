import logging
from typing import List
from google.cloud import bigquery
from google.cloud.bigquery import SchemaField


REQ = "REQUIRED"

SAMPLE_OUTPUT_SCHEMA = [
    SchemaField("id", "STRING", mode=REQ),
    SchemaField("request_datetime", "DATETIME", mode=REQ),
    SchemaField("date", "DATE", mode=REQ),
    SchemaField("proba", "FLOAT", mode=REQ),
    SchemaField("days_ahead", "INTEGER", mode=REQ)
]

def insert_forecasts(parsed_forecasts: List, bqtable: str):
    """
    Function inserts given list of dictionaries into BigQuery table.

    :param parsed_forecasts: List
    :param bqtable: str
    :return:
    """

    client = bigquery.Client()
    client.insert_rows_json(
        bqtable, parsed_forecasts
    )
    logging.info('INFO:APP:Forecasts updated')
