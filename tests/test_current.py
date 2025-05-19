import pytest

def test_current_missing_location(client):
    resp = client.get('/weather/current')
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data


def test_current_success(monkeypatch, client):
    # Dummy payload renvoyé par WeatherBit
    dummy_api_response = {
        "data": [{
            "weather": {"description": "Ensoleillé"},
            "temp": 22.3,
            "app_temp": 21.0,
            "min_temp": 18.0,
            "max_temp": 25.0,
            "pres": 1012,
            "rh": 55,
            "dewpt": 13.0,
            "clouds": 10,
            "vis": 10.0,
            "wind_spd": 4.5,
            "wind_dir": 90,
            "wind_cdir": "E",
            "wind_cdir_full": "Est",
            "uv": 5.0,
            "sunrise": "05:30",
            "sunset": "21:15",
            "ts": 1622476800
        }]
    }

    class DummyResp:
        status_code = 200
        def json(self):
            return dummy_api_response

    # Patch de la méthode requests.get importée dans app.py
    monkeypatch.setattr(
        'flask_weather_api.app.requests.get',
        lambda url, params: DummyResp(),
        raising=False
    )

    resp = client.get('/weather/current?location=Paris')
    assert resp.status_code == 200

    data = resp.get_json()
    assert data['description'] == "Ensoleillé"
    assert data['temperature_C'] == 22.3
    assert data['feels_like_C'] == 21.0
    assert data['wind_speed_kmh'] == round(4.5 * 3.6, 2)
    assert data['humidity_percent'] == 55