import pytest


def test_forecast_missing_location(client):
    resp = client.get('/weather/forecast')
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data


def test_forecast_success(monkeypatch, client):
    dummy_days = [
        {
            "datetime": f"2025-05-{10+i:02d}",
            "temp": 20 + i,
            "pres": 1000 + i*2,
            "wind_spd": 3 + 0.5*i
        }
        for i in range(7)
    ]
    dummy_api_response = {"data": dummy_days}

    class DummyResp:
        status_code = 200
        def json(self):
            return dummy_api_response

    monkeypatch.setattr(
        'flask_weather_api.app.requests.get',
        lambda url, params: DummyResp(),
        raising=False
    )

    resp = client.get('/weather/forecast?location=Lyon')
    assert resp.status_code == 200

    data = resp.get_json()
    assert 'evolution_generale' in data
    assert 'tendance_temperature' in data
    assert 'tendance_pression' in data
    assert 'vent_moyen_beaufort' in data