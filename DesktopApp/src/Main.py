
from datetime import datetime, timedelta
import requests
import json

feed_url = "https://io.adafruit.com/api/v2/EmilyCharles/feeds/desktop-doorbell/data"
last_check = datetime.now()


querystring = {"start_time":"2017-12-10T23:39:24Z","end_time":"2017-12-10T23:45:24Z"}

headers = {
    'X-AIO-KEY': "04f40a9872f740fc8f5b26e1ee4afa8d",
    'Cache-Control': "no-cache",
    'Postman-Token': "b8bd05cf-5468-aec9-482d-495be736f563"
    }


def get_server_data(start_time, end_time):
    global headers
    # request the interval from now to now minus [CHECK_INTERVAL] seconds
    querystring = {"start_time":datetime_to_server_string(start_time), "end_time":datetime_to_server_string(end_time)}
    print(querystring)
    payload_str = "&".join("%s=%s" % (k, v) for k, v in querystring.items())
    response = requests.request("GET",  feed_url, headers=headers, params=payload_str)



    print(response.url)
    print(response.text)


def get_time_range(time_now):
    return [time_now - DATETIME_INTERVAL, time_now]


def datetime_to_server_string(time):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ')

CHECK_INTERVAL =  2.1 # just slightly longer than the 2s interval that we get for free. Let's not get blocked out!
DATETIME_INTERVAL  = timedelta(seconds = CHECK_INTERVAL)


while True:
    if datetime.now() - last_check > DATETIME_INTERVAL:
        last_check = datetime.now()
        time_range = get_time_range(datetime.utcnow())
        get_server_data(time_range[0], time_range[1])

