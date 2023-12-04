from google.cloud import bigquery


def get_input_table_data(query: str) -> list:
    """
    Function gets input data from BigQuery table.

    :param query: (str) Must contain dataset name.

    :return: List
    """
    client = bigquery.Client()
    query_job = client.query(query)
    rows = query_job.result()
    dict_rows = [dict(row.items()) for row in rows]
    return dict_rows
