curl -X POST http://127.0.0.1:8000/predict \
  --header "${ACCESS_TOKEN_HEADER_NAME}: ${ACCESS_TOKEN}" \
  --header 'Content-Type: application/json' \
  --data '{"ds": [101, -66.4, 3, 1]}'