from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
# start_date = os.environ['START_DATE']
city = os.environ['CITY']
# birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


# def get_weather():
#   url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#   res = requests.get(url).json()
#   weather = res['data']['list'][0]
#   return weather['weather'], math.floor(weather['temp'])

# 返回当前温度，今天的天气，今天的最低温~最高温，明天的天气，明天的最低温~最高温，
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  weather2 = res['data']['list'][1]
  return weather['temp'], weather['weather'], math.floor(weather['low']), math.floor(weather['high']), weather2['weather'], math.floor(weather2['low']), math.floor(weather2['high'])

# def get_count():
#   delta = today - datetime.strptime(start_date, "%Y-%m-%d")
#   return delta.days

# def get_birthday():
#   next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#   if next < datetime.now():
#     next = next.replace(year=next.year + 1)
#   return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
# wea, temperature = get_weather()
nowTemp, todayWeather, todayLow, todayHigh, tomorrowWeather, tomorrowLow, tomorrowHigh = get_weather()
# data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
# data = {"words":{"value":get_words(), "color":get_random_color()}}
data = {
  "now_temp":{"value":nowTemp},
  "today_weather":{"value":todayWeather},
  "today_low":{"value":todayLow,"color":"#33cc99"},
  "today_high":{"value":todayHigh,"color":"#ff3333"},
  "tomorrow_weather":{"value":tomorrowWeather},
  "tomorrow_low":{"value":tomorrowLow,"color":"#33cc99"},
  "tomorrow_high":{"value":tomorrowHigh,"color":"#ff3333"},
  "words":{"value":get_words(), "color":"ff3366"}
  }
res = wm.send_template(user_id, template_id, data)
print(res)
