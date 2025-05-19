# Flask Weather API

[![CI](https://github.com/omrmeh/weather_api/actions/workflows/ci.yml/badge.svg)](https://github.com/omrmeh/weather_api/actions/workflows/ci.yml)

## Description
Une API Flask exposant deux endpoints :

- `/weather/current?location={city}` : météo actuelle (description, température, vent, humidité)
- `/weather/forecast?location={city}` : tendances météo sur 7 jours (température, pression, vent)

## Setup

1. Cloner le repo
2. Copier `.env.example` en `.env` et renseigner la clé `WEATHERBIT_API_KEY`
3. Lancer en local :

```bash
docker build -t weather-api .

docker run --env-file .env -p 5000:5000 weather-api
```

4. Tester les endpoints

## À venir

* Tests unitaires
* CI/CD
* Gestion avancée du quota

