import requests
import json
import geocoder # type: ignore
import io
import datetime as dt # type: ignore

from typing import List

class Backend:
    
    def __init__(self):
        self.base_url = "http://api.weatherapi.com/v1"
        
        with open("key.json") as f:
            key = json.load(f)
            self.api_key = key["API_KEY"]

        self.location = self.get_location()
    
    def get_image(self, url: str) -> io.BytesIO:
        return io.BytesIO(requests.get(url).content)
    
    def get_location(self) -> dict[str, float]:
        g = geocoder.ip('me')
        return {"lat": g.latlng[0], "lon": g.latlng[1]}

    def get_current_report(self) -> dict:
        url = f"{self.base_url}/current.json?key={self.api_key}&q={self.location['lat']},{self.location['lon']}"
        response = requests.get(url)
        return response.json()
    
    def get_forecast(self, days: int = 14) -> dict:
        url = f"{self.base_url}/forecast.json?key={self.api_key}&q={self.location['lat']},{self.location['lon']}&days={days}"
        response = requests.get(url)
        return response.json()

    def get_temperature(self) -> float:
        return self.get_current_report()["current"]["temp_c"]
    
    def get_wind(self) -> float:
        return self.get_current_report()["current"]["wind_kph"]
    
    def get_gusts(self) -> float:
        return self.get_current_report()["current"]["gust_kph"]

    def get_condition(self) -> dict:
        return self.get_current_report()["current"]["condition"]
    
    def get_humidity(self) -> float:
        return self.get_current_report()["current"]["humidity"]
    
    def get_sunrise(self) -> str:
        return self.get_forecast()['forecast']['forecastday'][0]['astro']['sunrise']
    
    def get_sunset(self) -> str:
        return self.get_forecast()['forecast']['forecastday'][0]['astro']['sunset']
    
    def get_current_icon(self) -> io.BytesIO:
        url = "https:"+ self.get_condition()["icon"]
        return io.BytesIO(requests.get(url).content)
    
    def get_14_days_forecast(self) -> dict:
        today = dt.datetime.now()
        next_14 = list(map(lambda x: x.strftime(format='%Y-%m-%d'), [today + dt.timedelta(days=i) for i in range(1, 15)]))
        
        forecast: List = self.get_forecast()['forecast']['forecastday']
        return {day: {'maxtemp_c': forecast[i]['day']['maxtemp_c'], 'mintemp_c': forecast[i]['day']['mintemp_c'], 'icon': forecast[i]['day']['condition']['icon']} for i, day in enumerate(next_14)}
    
if __name__ == "__main__":
    test = Backend()
    day = (dt.datetime.now() + dt.timedelta(days=1)).strftime("%Y-%m-%d")
    print(day)
    print(test.get_forecast()['location']['name'])
    