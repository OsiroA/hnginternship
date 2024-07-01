from flask import Flask, request, jsonify
import requests
import geocoder

app = Flask(__name__)
APIkey = "dfc2e23f70eeb4c96afc57af9764a9ec"

@app.route('/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitorName')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    geo = geocoder.ip(ip)
    if not geo.ok:
        return jsonify({"error": "Unable to determine visitor location"}), 400
    
    if geo.latlng:
        latitude, longitude = geo.latlng
    else:
        # Handle the case where latlng is empty
        return jsonify({"error": "Unable to determine latitude and longitude"}), 400

    city = geo.city
    link = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={APIkey}"

    try:
        response = requests.get(link)
        if response.status_code == 200:
            data = response.json()
            current_temp = data.get('current', {}).get('temp')
            if current_temp is not None:
                greeting = f"Hello, {visitor_name}! The current temperature in {city} is {current_temp} degrees Celsius"
                return jsonify({"client_ip": ip, "location": city, "greeting": greeting}), 200
            else:
                return jsonify({"error": "Could not fetch weather data"}), 500
        else:
            print(f"Error response from weather API: {response.status_code}")
            return jsonify({"error": "Could not fetch weather data"}), 500
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return jsonify({"error": "Could not fetch weather data"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

