from flask import Flask, jsonify
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Initialize Nominatim geocoder
geolocator = Nominatim(user_agent="weather_app")

# Function to get coordinates from city name
def get_coordinates(city_name):
    try:
        location = geolocator.geocode(city_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except GeocoderTimedOut:
        return None

# Function to fetch weather data using coordinates
def get_weather(lat, lon):
    api_key = "c6f17ea48252f1668a1da226296a9ac5"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Route to handle city name input
@app.route('/weather/<city>')
def weather_by_city(city):
    # Get coordinates for the city
    coordinates = get_coordinates(city)
    if not coordinates:
        return jsonify({"error": "Could not find the city. Please check the city name and try again."})

    # Fetch weather data using coordinates
    weather_data = get_weather(coordinates[0], coordinates[1])
    if not weather_data:
        return jsonify({"error": "Could not fetch weather data. Please try again later."})

    # Prepare response
    response = {
        "city": city,
        "temperature": weather_data['main']['temp'],
        "description": weather_data['weather'][0]['description']
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)