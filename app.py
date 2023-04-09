import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from os import environ as env
from dotenv import find_dotenv, load_dotenv
import requests
import json

#pending func: when first rendering get starred from db, if db updated with star repop list (sort by departured date)
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

API = env.get("WEATHERKEY")
countrycode='US'
city="Sacramento"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_trip(trip_id):
    conn = get_db_connection()
    trip = conn.execute('SELECT * FROM trips WHERE id = ?',
                        (trip_id,)).fetchone()
    conn.close()
    if trip is None:
        abort(404)
    return trip

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


def getLoc():
    addr="http://dataservice.accuweather.com/locations/v1/cities/"+countrycode+"/search?apikey="+API+"&q="+city+"&details=true"
    loc = requests.get(addr).text
    return json.loads(loc)[0]['Key']

def get5Indices(loc):
    output = requests.get("http://dataservice.accuweather.com/indices/v1/daily/5day/"+loc+"?apikey="+API).text
    indices = json.loads(output)
    return indices

def get1Indices(loc):
    output = requests.get("http://dataservice.accuweather.com/indices/v1/daily/1day/"+loc+"?apikey="+API).text
    indices = json.loads(output)
    return indices

def get5Forecast(loc):
    loc = getLoc()
    output = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/5day/"+loc+"?apikey=" + API).text
    forecast = json.loads(output)
    simpleForecast = []
    for day in forecast['DailyForecasts']:
        # for now condensed, later pass whole object as is, convert to C based on settings later
        simpleDay = {}
        simpleDay['date'] = day['date']
        simpleDay['minTemp'] = str(day['Temperature']['Minimum']['Value']) + "F"
        simpleDay['maxTemp'] = str(day['Temperature']['Maximum']['Value']) + "F"
        simpleDay['dayForecast'] = day['Day']['IconPhrase']
        simpleDay['dayRainForecast'] = day['Day']['HasPrecipitation']
        simpleDay['nightForecast'] = day['Night']['IconPhrase']
        simpleDay['nightRainForecast'] = day['Day']['HasPrecipitation']
        simpleForecast.append(simpleDay)
    return simpleForecast

def get1Forecast(loc):
    output = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/1day/"+loc+"?apikey=" + API).text
    forecast = json.loads(output)
    # reformat
    for key1 in forecast["DailyForecasts"]:
        print("Weather Forecast for "+key1['Date']+" is:")
        print("Temperature in F (minimum) is: "+str(key1['Temperature']['Minimum']['Value']))
        print("Temperature in F (maximum) is: " + str(key1['Temperature']['Maximum']['Value']))
        print("Day Forecast "+str(key1['Day']['IconPhrase']))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    conn = get_db_connection()
    starred_trips = conn.execute('SELECT * FROM trips WHERE starred = 1').fetchall()
    conn.close()
    #if starred_trips is None:
        #abort(404)
    # make this empty page or sign in?
    print(starred_trips)

    #daysForecast = get5Forecast(getLoc())
    return render_template('index.html', starred=starred_trips)

@app.route('/trips')
def trips():
    conn = get_db_connection()
    trips = conn.execute('SELECT * FROM trips').fetchall()
    conn.close()
    return render_template('index.html', trips=trips)


@app.route('/<int:trip_id>')
def trip(trip_id):
    flight_info = getFlight()
    trip = get_trip(trip_id)
    return render_template('trip.html', trip=trip, flight_info=flight_info)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        record = request.form['record']
        deptdate = request.form['deptdate']
        arrivdate = request.form['arrivdate']
        carrier = request.form['carrier']
        flight = request.form['flight']
        deptair = request.form['deptair']
        arrivair = request.form['arrivair']
        #content = request.form['content']

        if not record:
            flash('record is required!')
        else:
            conn = get_db_connection()
            #conn.execute('INSERT INTO trips (record, content) VALUES (?, ?)',
            #             (record, content))
            conn.execute('INSERT INTO trips (record, deptdate, arrivdate, carrier, flight, deptair, arrivair) VALUES (?,?,?,?,?,?,?,)',
                         (record, deptdate, arrivdate, carrier, flight, deptair, arrivair))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    trip = get_trip(id)

    if request.method == 'POST':
        record = request.form['record']
        #content = request.form['content']

        if not record:
            flash('record is required!')
        else:
            conn = get_db_connection()
            #conn.execute('UPDATE trips SET record = ?, content = ?'
            #             ' WHERE id = ?',
            #             (record, content, id))
            conn.execute('UPDATE trips SET record = ? WHERE id = ?',
                         (record, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', trip=trip)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    trip = get_trip(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM trips WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(trip['record']))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()