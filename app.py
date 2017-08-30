from flask import Flask
from flask.ext.cache import Cache
from weatherbit.api import Api
from flask.json import jsonify
import requests
import datetime
import re
from werkzeug.contrib.cache import RedisCache
from redis import from_url as redis_from_url

api_key="c011cdc396c741a28526652b501ad9a5"

app = Flask(__name__)
class Config(object):
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_KEY_PREFIX = 'arcus'
    # ... other option

app.config.from_object(Config)
cache = Cache(app)

#cache = Cache(app,config={'CACHE_TYPE': 'simple'})

base_url="https://api.weatherbit.io/v2.0/history/daily/postal?postal_code="
@app.route("/zipcode/<postal_code>")
@cache.cached(timeout=50)
def hello(postal_code):
    response="Please provide valid Zip code. US Zip code is 5 digit"
#    re-results = re.search(r'^[0-9]{5}(?:-[0-9]{4})?$', postal_code)
    if re.search(r'^[0-9]{5}(?:-[0-9]{4})?$', postal_code):
#    if re-results:
        full_url=base_url+postal_code+"&country=US&start_date=2017-08-02&end_date=2017-08-03&key=c011cdc396c741a28526652b501ad9a5"
        today = datetime.date.today()
        response=""
        for x in range(0,14):
            first_delta = datetime.timedelta(days = x+1)
            second_delta = datetime.timedelta(days = x)
            start_date = today - first_delta
            end_date = today - second_delta
            full_url=base_url+postal_code+"&country=US&start_date="+str(start_date)+"&end_date="+str(end_date)+"&key=c011cdc396c741a28526652b501ad9a5"
            response=response+requests.get(full_url).content
        #response = requests.get('https://api.weatherbit.io/v2.0/history/daily/postal?postal_code=92612&country=US&start_date=2017-08-02&end_date=2017-08-03&key=c011cdc396c741a28526652b501ad9a5').content
    return response

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
