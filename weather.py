"""
Gets weather data from http://www.7timer.info
"""

import requests
    
class WeatherReporter:
    """Get weather forecast from www.7timer.info"""
    def __init__(self, url="http://www.7timer.info/bin/api.pl", output="json", unit="metric"):
        self.url = url
        self.output = output
        self.unit = unit
        
    def get_weather(self, lon=0.00, lat=51.50, product="astro"):
        """Get plain forecast response from API"""
        params = dict(lon=lon, lat=lat, product=product, output=self.output, unit=self.unit)
        response = requests.get(self.url, params=params)
        return response
 
    def extract_data(self, response):
        """Extract some weather data from forecast API response"""
        all_data = response.json()
        weather_data = all_data.get("dataseries", [])
        # Above is multiple sets of data - each for different time/date
        # Just return the first for now
        return weather_data[0]
 
    def get_weather_info(self, lon=0.00, lat=51.50, product="astro"):
        """Get response, extract and return some values if successful""" 
        response = self.get_weather(lon, lat, product)
        if response.status_code == 200:
            values = self.extract_data(response)
        else:
            values = []
        return values

                
# Some temperature unit convertors
def ctof(centigrade):
    return centigrade * 9/5 + 32

def ftoc(faren):
    return (faren - 32) * 5/9

def ctok(centigrade):
    return centigrade + 273.15

def ftok(faren):
    return ctok(ftoc(faren))

def ktoc(kelvin):
    return kelvin - 273.15

def ktof(kelvin):
    return ctof(ktoc(kelvin))


if __name__ == "__main__":
    rep = WeatherReporter()
    w = rep.get_weather_info()
    print(w["cloudcover"], w["seeing"], w["temp2m"])
    print(ctof(w["temp2m"]))
    print(ctok(w["temp2m"]))

