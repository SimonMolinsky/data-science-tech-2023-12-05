gcloud pubsub topics create get-forecasts-topic

gcloud functions deploy get-forecasts \
--gen2 \
--runtime=python310 \
--region=europe-north1 \
--source=. \
--entry-point=main \
--trigger-topic=get-forecasts-topic \
--timeout=540s

gcloud scheduler jobs create pubsub get-forecasts-scheduler \
--location="" \
--schedule="15 6,12,18 * * *" \
--topic=get-forecasts-topic \
--message-body="Job to GET and UPLOAD forecasts from external API"