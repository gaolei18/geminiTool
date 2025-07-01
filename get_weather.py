
import requests
import sys

def get_city_adcode(api_key, city_name):
    """
    Uses Amap Geocoding API to get the adcode for a given city name.
    The adcode is required for the weather API.
    """
    url = f"https://restapi.amap.com/v3/geocode/geo?address={city_name}&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "1" and data["geocodes"]:
            return data["geocodes"][0]["adcode"]
        else:
            print(f"Error getting adcode for '{city_name}': {data.get('info', 'Unknown error')}", file=sys.stderr)
            return None
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}", file=sys.stderr)
        return None

def get_weather(api_key, city_name):
    """
    Gets tomorrow's weather forecast for a specific city using Amap API.
    """
    adcode = get_city_adcode(api_key, city_name)
    if not adcode:
        return

    # extensions=all means get forecast
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={adcode}&key={api_key}&extensions=all"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()

        if data["status"] == "1" and data.get("forecasts"):
            # The API returns forecasts for today and the next 3 days.
            # The second item in the list is tomorrow's forecast.
            tomorrow_forecast = data["forecasts"][0]["casts"][1]
            
            print(f"--- Tomorrow's Weather Forecast for {city_name} ---")
            print(f"Date: {tomorrow_forecast['date']}")
            print(f"Day Weather: {tomorrow_forecast['dayweather']}")
            print(f"Night Weather: {tomorrow_forecast['nightweather']}")
            print(f"Temperature: {tomorrow_forecast['daytemp']}°C (day) / {tomorrow_forecast['nighttemp']}°C (night)")
            print(f"Wind: {tomorrow_forecast['daywind']} wind, direction {tomorrow_forecast['daypower']}")
        else:
            print(f"Error: Could not retrieve weather data. Reason: {data.get('info', 'Unknown error')}", file=sys.stderr)

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}", file=sys.stderr)
    except (KeyError, IndexError) as e:
        print(f"Error parsing weather data: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python get_weather.py <your_api_key> <city_name>", file=sys.stderr)
        sys.exit(1)
    
    api_key = sys.argv[1]
    city_name = sys.argv[2]
    get_weather(api_key, city_name)
