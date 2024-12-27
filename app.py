from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO
import base64

import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    number = request.form['number']
    result = {}

    try:
        phone_number = phonenumbers.parse(number)

        # Country
        result['country'] = geocoder.description_for_number(phone_number, 'en')

        # Operator
        result['operator'] = carrier.name_for_number(phone_number, "en")

        # Phone timezone
        result['timezone'] = timezone.time_zones_for_number(phone_number)

        # Longitude and Latitude
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(result['country'])
        
        if location:
            lng = location.longitude
            lat = location.latitude
            result['longitude'] = lng
            result['latitude'] = lat

            # Time showing in phone
            obj = TimezoneFinder()
            result['timezone'] = obj.timezone_at(lng=lng, lat=lat)

            home = pytz.timezone(result['timezone'])
            local_time = datetime.now(home)
            result['time'] = local_time.strftime("%I:%M:%p")
        else:
            result['longitude'] = 'N/A'
            result['latitude'] = 'N/A'
            result['time'] = 'N/A'

    except phonenumbers.NumberParseException as e:
        result['error'] = str(e)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)