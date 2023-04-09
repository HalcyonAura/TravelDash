from dotenv import find_dotenv, load_dotenv
import urllib.request
import json
from os import environ as env
import requests

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

API = env.get("WEATHERKEY")
countrycode='US'
city="Sacramento"

#http://dataservice.accuweather.com/forecasts/v1/daily/10day/{locationKey}

def getLocation(API):
    addr="http://dataservice.accuweather.com/locations/v1/cities/"+countrycode+"/search?apikey="+API+"&q="+city+"&details=true"
    with urllib.request.urlopen(addr) as addr:
        data=json.loads(addr.read().decode())
        loc=data[0]['Key']
        return(loc)
    

def getForecast(loc):
    tenday="http://dataservice.accuweather.com/forecasts/v1/daily/1day/"+loc+"?apikey=" + API
    with urllib.request.urlopen(tenday) as tenday:
        data=json.loads(tenday.read().decode())
    print(data)
    for key1 in data["DailyForecasts"]:
        print("Weather Forecast for "+key1['Date']+" is:")
        print("Temperature in F (minimum) is: "+str(key1['Temperature']['Minimum']['Value']))
        print("Temperature in F (maximum) is: " + str(key1['Temperature']['Maximum']['Value']))
        print("Day Forecast "+str(key1['Day']['IconPhrase']))

def getIndices(loc):
    call = "http://dataservice.accuweather.com/indices/v1/daily/1day/"+loc+"?apikey="+API
    output = requests.get(call).text
    dict = json.loads(output)
    for obj in dict:
        print(obj['Name'])
        
getForecast(getLocation(API))
#getIndices(getLocation(API))