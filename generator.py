# generator

'''<div class="form-check">
    <input type="checkbox" class="form-check-input" id="check1" name="flight_delays" value="0" checked>
    <label class="form-check-label" for="check1">Flight Delays</label>
</div>
<div class="form-check">
    <input type="checkbox" class="form-check-input" id="check2" name="indoor_activity_forecast" value="1">
    <label class="form-check-label" for="check2">Indoor Activity Forecast</label>
</div>'''

items = ['Flight Delays', 'Indoor Activity Forecast', 'Running Forecast', 'Jogging Forecast', 'Hiking Forecast', 'Bicycling Forecast', 'Golf Weather Forecast', 'Tennis Forecast', 'Skateboarding Forecast', 'Outdoor Concert Forecast', 'Kite Flying Forecast', 'Beach & Pool Forecast', 'Sailing Forecast', 'Stargazing Forecast', 'Fishing Forecast', 'Construction Forecast', 'Ski Weather Forecast', 'Healthy Heart Fitness Forecast', 'Mosquito Activity Forecast', 'Dust & Dander Forecast', 'Snow Days Forecast', 'Hunting Forecast', 'Arthritis Pain Forecast', 'Asthma Forecast', 'Outdoor Barbecue', 'Common Cold Forecast', 'Flu Forecast', 'Migraine Headache Forecast', 'Lawn Mowing Forecast', 'Outdoor Activity Forecast', 'Sinus Headache Forecast', 'Flying Travel Index', 'Field Readiness Forecast', 'Grass Growing Forecast', 'Soil Moisture Forecast', 'Morning School Bus Forecast', 'Home Energy Efficiency Forecast', 'Fuel Economy Forecast', 'Composting Forecast', 'Shopping Forecast', 'Driving Travel Index', 'Thirst Forecast, brought to you by Country Time', 'Hair Frizz Forecast', 'Dog Walking Comfort Forecast', 'COPD Forecast']
def genForm(items):
    template = '<div class="form-check"><input type="checkbox" class="form-check-input" id="check{}" name="{}" value={} checked><label class="form-check-label" for="check{}">{}</label></div>'
    html = ""
    counter = 0
    for name in items:
        snake_name = (name.lower()).replace(' ', '_')
        gen_url = template.format(counter, snake_name, name, counter, name)
        html+= gen_url
        counter+=1

    print(html)

genForm(items)
