from flask import Flask, request, render_template
import requests

app = Flask(__name__)

API_KEY = "661e8f0ee2674e0ab3b33427240812"

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    forecast_data = None
    error_message = None
    selected_unit = "Fahrenheit"  # Default

    if request.method == "POST":
        city = request.form.get("city")
        selected_unit = request.form.get("unit")

        if city:
            unit_symbol = "F" if selected_unit == "Fahrenheit" else "C"

            weather_url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
            forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=4&aqi=no&alerts=no"

            weather_response = requests.get(weather_url)
            forecast_response = requests.get(forecast_url)

            if weather_response.status_code == 200 and forecast_response.status_code == 200:
                weather_json = weather_response.json()
                forecast_json = forecast_response.json()
                
                try:
                    location = f"{weather_json['location']['name']}, {weather_json['location']['country']}"
                    temperature = weather_json["current"]["temp_f"] if selected_unit == "Fahrenheit" else weather_json["current"]["temp_c"]
                    feels_like = weather_json["current"]["feelslike_f"] if selected_unit == "Fahrenheit" else weather_json["current"]["feelslike_c"]
                    description = weather_json["current"]["condition"]["text"]
                    wind_speed = weather_json["current"]["wind_mph"] if selected_unit == "Fahrenheit" else weather_json["current"]["wind_kph"]
                    humidity = weather_json["current"]["humidity"]
                    pressure = weather_json["current"]["pressure_in"] if selected_unit == "Fahrenheit" else weather_json["current"]["pressure_mb"]
                    icon_url = f"https:{weather_json['current']['condition']['icon']}"

                    weather_data = {
                        "location": location,
                        "temperature": round(temperature, 2),
                        "feels_like": round(feels_like, 2),
                        "unit": unit_symbol,
                        "description": description,
                        "wind_speed": wind_speed,
                        "humidity": humidity,
                        "pressure": pressure,
                        "icon_url": icon_url,
                    }

                    forecast_data = {
                        "daily": [
                            {
                                "date": day["date"],
                                "max_temp": round(day["day"]["maxtemp_f"] if selected_unit == "Fahrenheit" else day["day"]["maxtemp_c"], 2),
                                "min_temp": round(day["day"]["mintemp_f"] if selected_unit == "Fahrenheit" else day["day"]["mintemp_c"], 2),
                                "condition": day["day"]["condition"]["text"],
                                "icon_url": f"https:{day['day']['condition']['icon']}"
                            }
                            for day in forecast_json["forecast"]["forecastday"][1:]  # Skip today
                        ]
                    }

                except KeyError as e:
                    error_message = "Error parsing weather or forecast data."

            else:
                error_message = "Error fetching weather or forecast data. Please check the city name."

    return render_template("index.html", weather_data=weather_data, forecast_data=forecast_data, error_message=error_message, selected_unit=selected_unit)

if __name__ == "__main__":
    app.run(debug=True)
