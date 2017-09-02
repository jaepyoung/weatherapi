docker build -t arcusassign_web .
docker tag arcusassign_web us.gcr.io/arcusassign/weather:old
gcloud docker -- push us.gcr.io/arcusassign/weather:old
kubectl delete -f kubernetes/weather-deployment-prod-old.yml
kubectl create -f kubernetes/weather-deployment-prod-old.yml
