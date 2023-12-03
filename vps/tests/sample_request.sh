curl -X POST http://127.0.0.1:8000/predict \
  --header 'CustomAccessToken: datasciencetech_conf_2023' \
  --header 'Content-Type: application/json' \
  --data '{"ds": [101, -66.4, 3, 1]}'