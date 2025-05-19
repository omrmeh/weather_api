# Flask Weather API

[![CI](https://github.com/omrmeh/weather_api/actions/workflows/ci.yml/badge.svg)](https://github.com/omrmeh/weather_api/actions/workflows/ci.yml)

## Description

Une API Flask exposant deux endpoints :

* `/weather/current?location={city}` : météo actuelle (description, température, vent, humidité)
* `/weather/forecast?location={city}` : tendances météo sur 7 jours (évolution générale, tendances, vent moyen selon Beaufort)

## Prérequis

* Docker installé
* Clé API WeatherBit (quota 50 appels/jour)

## Setup et exécution

1. Cloner le repo :

   ```bash
   git clone https://github.com/omrmeh/weather_api.git
   cd weather_api
   ```
2. Copier `.env.example` en `.env` et renseigner :

   ```ini
   WEATHERBIT_API_KEY=your_api_key_here
   ```
3. Builder l’image Docker :

   ```bash
   docker build -t weather-api .
   ```
4. Lancer le container :

   ```bash
   docker run --env-file .env -p 5000:5000 weather-api
   ```
5. Tester les endpoints :

   ```bash
   curl "http://localhost:5000/weather/current?location=Toulouse"
   curl "http://localhost:5000/weather/forecast?location=Bordeaux"
   ```

## Tests unitaires

Exécution :

```bash
pytest -q
```

## CI/CD

Ce workflow GitHub Actions déclenche à chaque push :

1. Checkout du code
2. Installation des dépendances
3. Lancement des tests (pytest)
4. Build de l’image Docker

Le statut du build est visible via le badge en haut du README.
