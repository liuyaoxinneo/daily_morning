from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
city = os.environ['CITY']
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

read_law = open("./laws.txt", 'r', encoding='utf-8')
lines = read_law.readlines()
total_lines = 3645 # 实际的行数
total_list = []

# 返回当前温度，今天的天气，今天的最低温~最高温，明天的天气，明天的最低温~最高温，
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  weather2 = res['data']['list'][1]
  return weather['temp'], weather['weather'], math.floor(weather['low']), math.floor(weather['high']), weather2['weather'], math.floor(weather2['low']), math.floor(weather2['high'])


def get_color(now_temp):
  if now_temp>40:
    return "#CC0000"
  if now_temp>30:
    return "#FF3333"
  if now_temp>20:
    return "#33CC99"
  return "#3399FF"

# 8.16 每日法条
def is_another_law(line):
    if line == "\n":
        return -1
    if len(line) <= 2:
        return 0
    if line[0] != "第":
        return 0
    if line.find("节") == len(line) - 5:
        return 3
    if line.find("章") == len(line) - 5:
        return 2
    if line.find("条") != -1 and line.find(" ") != -1:
        return 1
    return 0

def get_one_law():
    today_law = ""
    start = random.randint(0, len(total_list)-1)
    # print("start line: ", total_list[start] + 1)
    if start == len(total_list) - 1:
        end = total_lines - 1
    else:
        end = total_list[start+1]
    # print("end line: ", end + 1)

    num = 0
    cnt = -1
    for line in lines:
        cnt += 1
        if total_list[start] <= cnt <= end:
            if is_another_law(line) == 1 and num == 0:
                today_law += line
                num = 1
            elif is_another_law(line) == 0 and num == 1:
                today_law += line
            elif (is_another_law(line) == 2 or is_another_law(line) == 3) and num == 1:
                break

    # print(" today law is : ", today_law)
    return today_law

def get_law():
    num = -1
    for line in lines:
        num += 1
        if is_another_law(line) == 1:
            total_list.append(num)
    return get_one_law()

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
  "today_low":{"value":todayLow,"color":get_color(todayLow)},
  "today_high":{"value":todayHigh,"color":get_color(todayHigh)},
  "tomorrow_weather":{"value":tomorrowWeather},
  "tomorrow_low":{"value":tomorrowLow,"color":get_color(tomorrowLow)},
  "tomorrow_high":{"value":tomorrowHigh,"color":get_color(tomorrowHigh)},
  "words":{"value":get_words(), "color":get_random_color()},
  "today_law":{"value":get_law(), "color":get_random_color()}
  }
res = wm.send_template(user_id, template_id, data)
print(res)
