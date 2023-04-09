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
#https://api.oag.com/flight-instances/[?DepartureDate][&ArrivalDate][&CarrierCode][&FlightNumber][&DepartureAirport][&ArrivalAirport][&AircraftRegistrationNumber][&Content][&FlightType][&CodeType][&ServiceType][&Limit][&After][&IataCarrierCode][&IcaoCarrierCode]&version=1.0

def getFlight():
    # require: departure date, arrival date, carrier code, flight number, departure airport, arrival airport
    # html = https://api.oag.com/flight-instances/?DepartureDate=2023-04-25&ArrivalDate=2023-04-25&CarrierCode=DL&FlightNumber=317&DepartureAirport=JFK&ArrivalAirport=SEA&version=1.0
    with open('flight.json', 'r') as f:
        data = json.load(f)
        print(data)
        condensed = {}
        condensed['departure'] = { "flight": data['data'][0]['carrierCode']['iata'] + str(data['data'][0]['flightNumber']), "airport": data['data'][0]['departure']['airport']['iata'], "terminal": data['data'][0]['departure']['terminal'], "date": data['data'][0]['departure']['date'], "localTime": data['data'][0]['departure']['passengerLocalTime']}
        condensed['arrival'] = { "flight": data['data'][0]['carrierCode']['iata'] + str(data['data'][0]['flightNumber']), "airport": data['data'][0]['arrival']['airport']['iata'], "terminal": data['data'][0]['arrival']['terminal'], "date": data['data'][0]['arrival']['date'], "localTime": data['data'][0]['arrival']['passengerLocalTime']}
        return condensed

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
        
#getForecast(getLocation(API))
#getIndices(getLocation(API))


print(getFlight())