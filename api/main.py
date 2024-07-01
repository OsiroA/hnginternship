import requests
from flask import Flask, request, jsonify

timezone = "Africa/Lagos"
latitude = 7.3776
longitude = 3.9470

app = Flask(__name__)
weather_codes = {
    0: "Cloud development not observed or not observable",
    1: "Clouds generally dissolving or becoming less developed",
    2: "State of sky on the whole unchanged",
    3: "Clouds generally forming or developing",
    4:
    "Visibility reduced by smoke, e.g. veldt or forest fires, industrial smoke or volcanic ashes",
    5: "Haze",
    6:
    "Widespread dust in suspension in the air, not raised by wind at or near the station at the time of observation",
    7:
    "Dust or sand raised by wind at or near the station at the time of observation, but no well developed dust whirl(s) or sand whirl(s), and no duststorm or sandstorm seen",
    8:
    "Well developed dust whirl(s) or sand whirl(s) seen at or near the station during the preceding hour or at the time ot observation, but no duststorm or sandstorm",
    9:
    "Duststorm or sandstorm within sight at the time of observation, or at the station during the preceding hour",
    10: "Mist",
    11:
    "Patches shallow fog or ice fog at the station, whether on land or sea, not deeper than about 2 metres on land or 10 metres at sea",
    12: "More or less continuous",
    13: "Lightning visible, no thunder heard",
    14:
    "Precipitation within sight, not reaching the ground or the surface of the sea",
    15:
    "Precipitation within sight, reaching the ground or the surface of the sea, but distant, i.e. estimated to be more than 5 km from the station",
    16:
    "Precipitation within sight, reaching the ground or the surface of the sea, near to, but not at the station",
    17: "Thunderstorm, but no precipitation at the time of observation",
    18:
    "Squalls at or within sight of the station during the preceding hour or at the time of observation",
    19: "Funnel cloud(s) - Tornado cloud or water-spout",
    20: "Drizzle (not freezing) or snow grains - not falling as shower(s)",
    21: "Rain (not freezing)",
    22: "Snow",
    23: "Rain and snow or ice pellets",
    24: "Freezing drizzle or freezing rain",
    25: "Shower(s) of rain",
    26: "Shower(s) of snow, or of rain and snow",
    27: "Shower(s) of hail, or of rain and hail",
    28: "Fog or ice fog",
    29: "Thunderstorm (with or without precipitation)",
    30:
    "Slight or moderate duststorm or sandstorm - has decreased during the preceding hour",
    31: "- no appreciable change during the preceding hour",
    32: "- has begun or has increased during the preceding hour",
    33:
    "Severe duststorm or sandstorm - has decreased during the preceding hour",
    34: "- no appreciable change during the preceding hour",
    35: "- has begun or has increased during the preceding hour",
    36: "Slight or moderate blowing snow generally low (below eye level)",
    37: "Heavy drifting snow",
    38: "Slight or moderate blowing snow generally high (above eye level)",
    39: "Heavy drifting snow",
    40: "Fog or ice fog at the time of observation",
    41:
    "Fog or ice fog at a distance at the time of observation, but not at the station during the preceding hour, the fog or ice fog extending to a level above that of the observer",
    42: "Fog or ice fog in patches",
    43:
    "Fog or ice fog, sky visible has become thinner during the preceding hour",
    44: "Fog or ice fog, sky invisible",
    45:
    "Fog or ice fog, sky visible no appreciable change during the preceding hour",
    46: "Fog or ice fog, sky invisible",
    47:
    "Fog or ice fog, sky visible has begun or has become thicker during the preceding hour",
    48: "Fog or ice fog, sky invisible",
    49: "Fog, depositing rime, sky visible",
    50: "Fog, depositing rime, sky invisible",
    51: "Drizzle, not freezing, intermittent slight at time of observation",
    52: "Drizzle, not freezing, continuous",
    53: "Drizzle, not freezing, intermittent moderate at time of observation",
    54: "Drizzle, not freezing, continuous",
    55:
    "Drizzle, not freezing, intermittent heavy (dense) at time of observation",
    56: "Drizzle, not freezing, continuous",
    57: "Drizzle, freezing, slight",
    58: "Drizzle, freezing, moderate or heavy (dense)",
    59: "Drizzle and rain, slight",
    60: "Drizzle and rain, moderate or heavy",
    61: "Rain, not freezing, intermittent slight at time of observation",
    62: "Rain, not freezing, continuous",
    63: "Rain, not freezing, intermittent moderate at time of observation",
    64: "Rain, not freezing, continuous",
    65: "Rain, not freezing, intermittent heavy at time of observation",
    66: "Rain, not freezing, continuous",
    67: "Rain, freezing, slight",
    68: "Rain, freezing, moderate or heavy (dense)",
    69: "Rain or drizzle and snow, slight",
    70: "Rain or drizzle and snow, moderate or heavy",
    71: "Intermittent fall of snowflakes slight at time of observation",
    72: "Continuous fall of snowflakes",
    73: "Intermittent fall of snowflakes moderate at time of observation",
    74: "Continuous fall of snowflakes",
    75: "Intermittent fall of snowflakes heavy at time of observation",
    76: "Continuous fall of snowflakes",
    77: "Diamond dust (with or without fog)",
    78: "Snow grains (with or without fog)",
    79: "Isolated star-like snow crystals (with or without fog)",
    80: "Rain shower(s), slight",
    81: "Rain shower(s), moderate or heavy",
    82: "Rain shower(s), violent",
    83: "Shower(s) of rain and snow mixed, slight",
    84: "Shower(s) of rain and snow mixed, moderate or heavy",
    85: "Snow shower(s), slight",
    86: "Snow shower(s), moderate or heavy",
    87:
    "Shower(s) of snow pellets or small hail, with or without rain or rain and snow mixed - slight",
    88:
    "Shower(s) of snow pellets or small hail, with or without rain or rain and snow mixed - moderate or heavy",
    89:
    "Shower(s) of hail, with or without rain or rain and snow mixed, not associated with thunder - slight",
    90:
    "Shower(s) of hail, with or without rain or rain and snow mixed, not associated with thunder - moderate or heavy",
    91:
    "Slight rain at time of observation - Thunderstorm during the preceding hour but not at time of observation",
    92: "Moderate or heavy rain at time of observation",
    93: "Slight snow, or rain and snow mixed or hail at time of observation",
    94:
    "Moderate or heavy snow, or rain and snow mixed or hail at time of observation",
    95:
    "Thunderstorm, slight or moderate, without hail but with rain and/or snow at time of observation - Thunderstorm at time of observation",
    96: "Thunderstorm, slight or moderate, with hail at time of observation",
    97:
    "Thunderstorm, heavy, without hail but with rain and/or snow at time of observation",
    98:
    "Thunderstorm combined with duststorm or sandstorm at time of observation",
    99: "Thunderstorm, heavy, with hail at time of observation"
}


# print(weather_codes)
def getWeather():
  result = requests.get(
      f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone={timezone}"
      )

  user = result.json()
  code = user["daily"]["weathercode"][0]
  min = user["daily"]["temperature_2m_min"][0]
  max = user["daily"]["temperature_2m_max"][0]
  location = user["timezone"]
  codeMeaning = weather_codes[code]
  return location, codeMeaning, min, max


@app.route('/api/hello', methods=['GET'])
def hello():
  visitor = request.args.get('visitor', 'Visitor')
  ip = request.remote_addr

  #to fetch the weather data:
  location, codeMeaning, min, max = getWeather()
  greeting = f"Hello, {visitor}!, the temperature ranges from {min} to {max} and about the weather, {codeMeaning} in {location}"

  return jsonify({"ip": ip, "location": location, "greeting": greeting})


if __name__ == '__main__':
  app.run()
