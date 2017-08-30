docker build -t arcusassign_web .
docker tag arcusassign_web us.gcr.io/arcusassign/weather:latest
gcloud docker -- push us.gcr.io/arcusassign/weather:latest
kubectl delete -f kubernetes/weather-deployment-prod.yml
kubectl create -f kubernetes/weather-deployment-prod.yml
