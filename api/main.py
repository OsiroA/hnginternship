from flask import Flask, request, jsonify
import requests
import geocoder

app = Flask(__name__)

APIkey = "dfc2e23f70eeb4c96afc57af9764a9ec"

@app.route('/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitorName')

    # Fetch IP Address
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # For local development, use a default IP address or handle accordingly
    if client_ip == '127.0.0.1':
        client_ip = '8.8.8.8'  # Google's public DNS IP; replace with an actual IP for testing

    # Fetch location
    geo = geocoder.ip(client_ip)
    if not geo.ok:
        return jsonify({"error": "Unable to determine visitor location"}), 400

    city = geo.city  # Assuming geocoder provides city information

    # Fetch weather data
    weather = get_weather(geo.lat, geo.lng)
    if weather is not None:
        greeting = f"Hello, {visitor_name}!, the temperature is {weather} degrees Celsius in {city}"
        return jsonify({
            "client_ip": client_ip,
            "location": city,
            "greeting": greeting
        }), 200
    else:
        return jsonify({"error": "Could not fetch weather data"}), 500

def get_weather(latitude, longitude):
    link = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={APIkey}&units=metric"

    try:
        response = requests.get(link)
        if response.status_code == 200:
            data = response.json()
            current_temp = data.get('current', {}).get('temp')
            return current_temp
        else:
            print(f"Error response from weather API: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)