from datetime import datetime, timedelta
import requests
import json
import credentials
from win10toast import ToastNotifier


toaster = ToastNotifier()
feed_url = "https://io.adafruit.com/api/v2/EmilyCharles/feeds/desktop-doorbell/data"
last_check = datetime.now()
notify = False


# set up standard headers
headers = {
    'X-AIO-KEY': credentials.AIOkey,
    'Cache-Control': "no-cache",
    'Postman-Token': "b8bd05cf-5468-aec9-482d-495be736f563"
    }


def parse_server_response(response_text):
    global notify
    for item in json.loads(response_text):
        if item["value"] == "1":
            notify = True;


def get_server_data(start_time, end_time):
    global headers
    # request the interval from now to now minus [CHECK_INTERVAL] seconds
    querystring = {"start_time":datetime_to_server_string(start_time), "end_time":datetime_to_server_string(end_time)}
    print(querystring)
    payload_str = "&".join("%s=%s" % (k, v) for k, v in querystring.items())
    response = requests.request("GET",  feed_url, headers=headers, params=payload_str)

    if response.text  != "[]":
        parse_server_response(response.text)


def get_time_range(time_now):
    return [time_now - DATETIME_INTERVAL, time_now]


def datetime_to_server_string(time):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ')

CHECK_INTERVAL = 2
DATETIME_INTERVAL  = timedelta(seconds = CHECK_INTERVAL)


while True:
    if datetime.now() - last_check > DATETIME_INTERVAL:
        last_check = datetime.now()
        time_range = get_time_range(datetime.utcnow())
        get_server_data(time_range[0], time_range[1])

    if notify:
        notify = False
        print("Got a message!")
        toaster.show_toast("Look up!", "Someone wants to talk to you.",
                           icon_path="custom.ico",
                           duration=5
                           )
