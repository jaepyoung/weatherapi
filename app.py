from flask import Flask
from flask.ext.cache import Cache
from weatherbit.api import Api
from flask.json import jsonify
from connexion.resolver import RestyResolver
import requests
import connexion
import datetime
import logging
import json
import re
import redis
from werkzeug.contrib.cache import RedisCache
from redis import from_url as redis_from_url
import ast

requests.adapters.DEFAULT_RETRIES = 5

r = redis.StrictRedis(host='localhost',port=6379,db=0)
api_key="c011cdc396c741a28526652b501ad9a5"

app = Flask(__name__)


base_url="https://api.weatherbit.io/v2.0/history/daily/postal?postal_code="
def get_weather(zip_code):
    WEATHERS=[]
    if re.search(r'^[0-9]{5}(?:-[0-9]{4})?$', zip_code):
        today = datetime.date.today()
        for x in range(0,1):
            weather={}
            first_delta = datetime.timedelta(days = x+1)
            second_delta = datetime.timedelta(days = x)
            start_date = today - first_delta
            end_date = today - second_delta
            full_url=base_url+zip_code+"&country=US&start_date="+str(start_date)+"&end_date="+str(end_date)+"&key=c011cdc396c741a28526652b501ad9a5"

            logging.warning(full_url)
            try:
                if r.get(full_url) is None:
                    logging.warning("API Calling")
                    response=requests.get(full_url)
                    logging.warning("Test"+str(response.status_code))
                    jsonresponse=json.loads(response.content)
                    r.set(full_url,jsonresponse)
                    weather['country_code']=jsonresponse['country_code']
                    weather['state_code']=jsonresponse['state_code']
                    weather['city_name']=jsonresponse['city_name']
                    weather['date']=jsonresponse['data'][0]['datetime']
                    weather['max_temp']=jsonresponse['data'][0]['max_temp']
                    weather['temp']=jsonresponse['data'][0]['temp']
                    weather['min_temp']=jsonresponse['data'][0]['min_temp']
                else:
                    logging.warning("Caching Calling")
                    jsonresponse=ast.literal_eval(r.get(full_url))
                    weather['country_code']=jsonresponse['country_code']
                    weather['state_code']=jsonresponse['state_code']
                    weather['city_name']=jsonresponse['city_name']
                    weather['date']=jsonresponse['data'][0]['datetime']
                    weather['max_temp']=jsonresponse['data'][0]['max_temp']
                    weather['temp']=jsonresponse['data'][0]['temp']
                    weather['min_temp']=jsonresponse['data'][0]['min_temp']
                    logging.warning("Type"+str(type(weather)))

                WEATHERS.append(weather)
            except requests.exceptions.HTTPError as e:
                logging.warning("Execpetion Handling")
                weather['country_code']="n/a"
                weather['state_code']="n/a"
                weather['city_name']="n/a"
                weather['date']="n/a"
                weather['max_temp']="n/a"
                weather['min_temp']="n/a"
                weather['temp']="n/a"
                WEATHERS.append(weather)

        return WEATHERS
logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger/arcus.yaml')

application = app.app
if __name__ == '__main__':
    app.run(debug=True,port=5000)
