from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
APIkey = "33013f5b41c386ea0705bdf9c2689dfd"

@app.route('/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitorName')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # For testing purposes, use a known public IP address
    if ip.startswith("192.") or ip.startswith("10.") or ip.startswith("172."):
        ip = "8.8.8.8"  # Google's public DNS IP address for testing

    print(f"Visitor IP: {ip}")  # Debug print
    
    try:
        geo_response = requests.get(f"http://ip-api.com/json/{ip}")
        geo_data = geo_response.json()
        print(f"Geocoder result: {geo_data}")  # Debug print

        if geo_data['status'] == 'success':
            city = geo_data['city']
        else:
            return jsonify({"error": "Unable to determine visitor location"}), 400

        link = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={APIkey}&units=metric"

        response = requests.get(link)
        if response.status_code == 200:
            data = response.json()
            current_temp = data.get('main', {}).get('temp')
            if current_temp is not None:
                greeting = f"Hello, {visitor_name}! The current temperature in {city} is {current_temp} degrees Celsius"
                return jsonify({"client_ip": ip, "location": city, "greeting": greeting}), 200
            else:
                return jsonify({"error": "Could not fetch weather data"}), 500
        else:
            return jsonify({"error": f"Error response from weather API: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error fetching weather data: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)