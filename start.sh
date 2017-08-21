docker stop weather
docker rm weather
docker run -d -p 5000:5000 --name=weather flask-sample-one
