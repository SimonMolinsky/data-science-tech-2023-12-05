from settings import *
from buckets.upload import bucket_upload
from tables.input import get_input_table_data
from tables.output import insert_forecasts


def main(data, context):
    """Event-driven function that downloads forecasts and parses these into
       BigQuery table and (optionally) Storage Bucket.

    :param data:
    :param context:
    """
    # Valid code from here
    try:
        # Get input_data list
        input_data = get_input_table_data(INPUT_TABLE)
    except Exception as ex:
        logging.error('ERROR:APP:Cannot retrieve input_data from bigquery')
        raise ex

    for some_input_data in input_data:
        # Get forecasts
        forecasts = build_forecasts_using_external_api(
            EXTERNAL_API_KEY, input_data
        )

        # Store forecasts
        try:
            bucket_upload(
                ds=forecasts,
                filename='samplefile.json',
                bucket_name=BUCKET_NAME
            )
        except Exception as ex:
            logging.error('ERROR:APP:Bucket error')
            logging.error(ex)

        # Parse forecasts into DB input
        parsed = parse_forecasts(
            forecasts=forecasts
        )

        # Push parsed data into a BigQuery table
        insert_forecasts(
            parsed_forecasts=parsed, bqtable=OUTPUT_TABLE
        )

    logging.info('INFO:APP:Process completed')


if __name__ == '__main__':
    main('data', 'context')
