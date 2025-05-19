import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests
from statistics import mean

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv('WEATHERBIT_API_KEY')
BASE_URL = 'https://api.weatherbit.io/v2.0'

#  https://www.rmets.org/metmatters/beaufort-wind-scale
BEAUFORT_SCALE = [
    (1, 'Calme'),
    (5, 'Brise légère'),
    (11, 'Petite brise'),
    (19, 'Jolie brise'),
    (28, 'Brise modérée'),
    (38, 'Bonne brise'),
    (49, 'Forte brise'),
    (61, 'Grand vent'),
    (74, 'Coup de vent'),
    (88, 'Fort coup de vent'),
    (102, 'Tempête'),
    (117, 'Violente tempête'),
    (float('inf'), 'Ouragan')
]

def categorize_beaufort(speed_kmh):
    for threshold, name in BEAUFORT_SCALE:
        if speed_kmh <= threshold:
            return name
    return 'Inconnu'


@app.route('/weather/current')
def current_weather():
    city = request.args.get('location')
    if not city:
        return jsonify({'error': 'Paramètre location manquant'}), 400
    if not API_KEY:
        return jsonify({'error': 'Clé API manquante'}), 500

    url = f"{BASE_URL}/current"
    params = {'city': city, 'key': API_KEY, 'units': 'M', 'lang': 'fr'}
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        return jsonify({"error": "Échec de l'appel API externe", "details": resp.text}), resp.status_code

    items = resp.json().get('data', [])
    if not items:
        return jsonify({'error': 'Aucune donnée retournée'}), 404
    data = items[0]

    result = {
        'city_name': data.get('city_name'),
        'state_code': data.get('state_code'),
        'country_code': data.get('country_code'),
        'latitude': data.get('lat'),
        'longitude': data.get('lon'),
        'observation_time': data.get('ob_time'),
        'timezone': data.get('timezone'),
        'description': data.get('weather', {}).get('description'),
        'temperature_C': data.get('temp'),
        'feels_like_C': data.get('app_temp'),
        'min_temp_C': data.get('min_temp'),
        'max_temp_C': data.get('max_temp'),
        'pressure_mb': data.get('pres'),
        'humidity_percent': data.get('rh'),
        'dew_point_C': data.get('dewpt'),
        'clouds_percent': data.get('clouds'),
        'visibility_km': data.get('vis'),
        'wind_speed_m_s': data.get('wind_spd'),
        'wind_speed_kmh': round(data.get('wind_spd', 0) * 3.6, 2),
        'wind_direction_deg': data.get('wind_dir'),
        'wind_cdir': data.get('wind_cdir'),
        'wind_cdir_full': data.get('wind_cdir_full'),
        'uv_index': data.get('uv'),
        'sunrise': data.get('sunrise'),
        'sunset': data.get('sunset'),
        'observation_timestamp': data.get('ts')
    }
    return jsonify(result)


@app.route('/weather/forecast')
def forecast_weather():
    city = request.args.get('location')
    if not city:
        return jsonify({'error': 'Paramètre location manquant'}), 400
    if not API_KEY:
        return jsonify({'error': 'Clé API manquante'}), 500

    url = f"{BASE_URL}/forecast/daily"
    params = {'city': city, 'key': API_KEY, 'units': 'M', 'days': 7, 'lang': 'fr'}
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        return jsonify({"error": "Échec de l'appel API externe", "details": resp.text}), resp.status_code

    data = resp.json().get('data', [])
    if not data:
        return jsonify({'error': 'Aucune donnée retournée'}), 404

    temps = [day['temp'] for day in data]
    pressions = [day['pres'] for day in data]
    vents = [day['wind_spd'] * 3.6 for day in data]

    # Temperature trend
    delta_temp = temps[-1] - temps[0]
    if delta_temp > 1:
        trend_temp = 'en hausse'
    elif delta_temp < -1:
        trend_temp = 'en baisse'
    else:
        trend_temp = 'stable'

    # Pressure trend
    delta_pres = pressions[-1] - pressions[0]
    if delta_pres > 5:
        trend_pres = 'en forte hausse'
    elif delta_pres > 1:
        trend_pres = 'en hausse'
    elif delta_pres < -5:
        trend_pres = 'en forte baisse'
    elif delta_pres < -1:
        trend_pres = 'en baisse'
    else:
        trend_pres = 'stable'

    # General evolution
    if delta_temp > 0 and delta_pres > 0:
        evolution = 'en amélioration'
    elif delta_temp < 0 and delta_pres < 0:
        evolution = 'en dégradation'
    else:
        evolution = 'stable'

    # Average wind Beaufort
    avg_wind = mean(vents)
    beaufort = categorize_beaufort(avg_wind)

    result = {
        'evolution_generale': evolution,
        'tendance_temperature': trend_temp,
        'tendance_pression': trend_pres,
        'vent_moyen_beaufort': beaufort
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)