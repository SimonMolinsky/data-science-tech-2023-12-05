import logging
import os
from dotenv import load_dotenv


load_dotenv()

# Load variables

# Weather API Key
EXTERNAL_API_KEY = os.getenv('API_KEY')

# BigQuery Input Table
INPUT_TABLE = os.getenv('INPUT_TABLE')
INPUT_DATA_QUERY = f'SELECT * FROM {INPUT_TABLE}'

# BigQuery output table
OUTPUT_TABLE = os.getenv('OUTPUT_TABLE')

# Google Cloud Storage
BUCKET_NAME = os.getenv('BUCKET_NAME')
