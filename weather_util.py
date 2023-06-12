from pyowm import OWM
from pyowm.utils import timestamps
from dotenv import load_dotenv
from messages import wrong_place
import os

# getting API key from .env file 
load_dotenv()
OWM_KEY = os.getenv('OWM_KEY')

# initialise OWM manager 
w = OWM(OWM_KEY)
w_manager = w.weather_manager()

# this function formats the results we fetch and preformatted from OWM
def answer(answ: str, *args):
    for _ in args:
        answ = answ + _
    return answ

# function to get weather from OWM server
def get_weather(place: str, mode=None):
    try:
        # initialising the weather object
        observation = w_manager.weather_at_place(place)
        wt = observation.weather
        # getting specific data
        ans = f"Here`s weather in {place.title()}: \n" 
        t = f"Temperature: {wt.temperature('celsius')['temp']} C \n" 
        h = f"Humidity: {wt.humidity}% \n"
        cl = f"Clouds: {wt.clouds} \n"
        r = f"Rain: {'there is no rain today' if wt.rain == {} else wt.rain['all']}\n"
        wn = f"Wind: {wt.wind()['speed']} m/s \n"
    except Exception:
        return wrong_place
    else: 
        if mode:
            match mode:
                case 't':
                    return answer(ans, t)
                case 'h':
                    return answer(ans, h)
                case 'c':
                    return answer(ans, cl)
                case 'r':
                    return answer(ans, r)
                case 'w':
                    return answer(ans, wn)
        return answer(ans, t, h, cl, r, wn)

# function to get forecast from OWM server (only for tomorrow, although options could be added)
# note that we haven`t access to forecast object directly since it was deprecated
# so we need to use one_call API method instead
def get_forecast(place: str, mode=None):
    try:
        # initialising geocod manager to get longitude and latitude of the place
        geocoder = w.geocoding_manager()
        locations = geocoder.geocode(place, limit=1)
        city = locations[0]
        # passing our coords, getting OneCall object and extracting daily forecast from it
        data = w_manager.one_call(city.lat, city.lon)
        tomorrow_w = data.forecast_daily[1]
        # getting specific data
        ans = f"Here`s weather for tomorrow in {place.title()}: \n" 
        t = f"Temperature: {tomorrow_w.temperature('celsius').get('day')} C \n"
        h = f"Humidity: {tomorrow_w.humidity}% \n"
        cl = f"Clouds: {tomorrow_w.clouds} \n"
        r = f"Rain: {'there will be no rain tomorrow' if tomorrow_w.rain == {} else tomorrow_w.rain}\n"
        wn = f"Wind: {tomorrow_w.wind()['speed']} m/s \n"
    except Exception as e:
        return 'We`re unable to forecast the weather for this place, try again'
    else:
        if mode:
            match mode:
                case 't':
                    return answer(ans, t)
                case 'h':
                    return answer(ans, h)
                case 'c':
                    return answer(ans, cl)
                case 'r':
                    return answer(ans, r)
                case 'w':
                    return answer(ans, wn)
        return answer(ans, t, h, cl, r, wn)
    

    

