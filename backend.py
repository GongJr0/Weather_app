import requests
import json
import geocoder # type: ignore
import io

class Backend:
    
    def __init__(self):
        self.base_url = "http://api.weatherapi.com/v1"
        
        with open("key.json") as f:
            key = json.load(f)
            self.api_key = key["API_KEY"]

        self.location = self.get_location()
        
    def get_location(self) -> dict[str, float]:
        g = geocoder.ip('me')
        return {"lat": g.latlng[0], "lon": g.latlng[1]}

    def get_current_report(self) -> dict:
        url = f"{self.base_url}/current.json?key={self.api_key}&q={self.location['lat']},{self.location['lon']}"
        response = requests.get(url)
        return response.json()
    
    def get_forecast(self) -> dict:
        url = f"{self.base_url}/forecast.json?key={self.api_key}&q={self.location['lat']},{self.location['lon']}"
        response = requests.get(url)
        return response.json()

    def get_temperature(self) -> float:
        return self.get_current_report()["current"]["temp_c"]
    
    def get_wind(self) -> float:
        return self.get_current_report()["current"]["wind_kph"]

    def get_condition(self) -> dict:
        return self.get_current_report()["current"]["condition"]
    
    def get_current_icon(self) -> io.BytesIO:
        url = "https:"+ self.get_condition()["icon"]
        return io.BytesIO(requests.get(url).content)
    
if __name__ == "__main__":
    test = Backend()
    print(test.get_condition())
    