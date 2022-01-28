import unittest
import json
from weather import WeatherReporter
from weather import ctof, ftoc


class DummyResponse:
    """Dummy requests response used for json data check
    Only used to simulate the json() method
    """
    def __init__(self):
        self.values = {"dataseries": [{"1a":"first"}, {"1b":"another"}]}
    def json(self):
        return self.values


class TestWeather(unittest.TestCase):
    def test_get(self):
        # Not actually a test of the application but of connectivity
        reporter = WeatherReporter()
        response = reporter.get_weather()
        self.assertEqual(response.status_code, 200, "Response not 200. Got: {}".format(response.status_code))

    def test_extract_dummy_data(self):
        reporter = WeatherReporter()
        test_data = DummyResponse()
        extracted = reporter.extract_data(test_data)
        self.assertEqual(extracted, {'1a': 'first'}, "Not expected data extract")
        
    def test_extract_real_data(self):
        reporter = WeatherReporter()
        response = reporter.get_weather()
        extracted = reporter.extract_data(response)
        for key in ["cloudcover", "seeing", "temp2m"]:
            self.assertTrue(key in extracted.keys(), "Key '{}' not found".format(key))
            
    def test_ctof(self):
        f = ctof(10)
        self.assertEqual(f, 50, "10C should be 50F, not {}".format(f))
        
    def test_ftoc(self):
        c = ftoc(86)
        self.assertEqual(c, 30, "86F should be 30C, not {}".format(c))
    
    # Convert C to F then back to C. Do we get original value back?
    def test_mutual_ctof_ftoc(self):
        # Avoid disrepancies with rightmost floating point digits 
        rounding = 8
        for c1 in range(-100, 101):
            c1 = round(float(c1), rounding)
            f = ctof(c1)
            c2 = round(ftoc(f), rounding)
            self.assertEqual(c1, c2, "{}C converted to F then back to C gives {}C".format(c1, c2) )
            
            
        

if __name__ == '__main__':
    unittest.main()
    