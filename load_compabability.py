import requests
from bs4 import BeautifulSoup

HTML_PARSER = "html.parser"

URL = "https://horoscopes.rambler.ru/sovmestimost-znakov-zodiaka/"

ALL_SEX = ["МУЖЧИНА", "ЖЕНЩИНА"]
ALL_ZODIAC = [
    "ОВЕН",
    "ТЕЛЕЦ",
    "БЛИЗНЕЦЫ",
    "РАК",
    "ЛЕВ",
    "ДЕВА",
    "ВЕСЫ",
    "СКОРПИОН",
    "СТРЕЛЕЦ",
    "КОЗЕРОГ",
    "ВОДОЛЕЙ",
    "РЫБЫ",
]

FRAME_CLASS = "j+xoX"
CHART_CLASS = "PM-qP"
PERSENT_CLASS = "THo-S"


def start():
    response = requests.get(URL, timeout=30000)
    page_soup = BeautifulSoup(response.text, HTML_PARSER)
    all_frames = page_soup.find_all("div", class_=FRAME_CLASS)
    counter = 0
    result_json = "{"
    for sex in ALL_SEX:
        sex_str = f'"{sex}"' + ":{"
        result_json += sex_str
        for zodiac in ALL_ZODIAC:
            zodiac_str = f'"{zodiac}"' + ":{"
            result_json += zodiac_str
            current_frame = str(all_frames[counter])
            current_frame_soup = BeautifulSoup(current_frame, HTML_PARSER)
            all_zodiac_chart = current_frame_soup.find_all("a", class_=CHART_CLASS)
            zodiac_counter = 0
            for chart in all_zodiac_chart:
                chart_soup = BeautifulSoup(str(chart), HTML_PARSER)
                persent_span = chart_soup.find("span", class_=PERSENT_CLASS)
                persent_str = persent_span.get_text()
                current_zodiac = ALL_ZODIAC[zodiac_counter]
                print(persent_str)
                current_zodiac_string = f'"{current_zodiac}":"{persent_str}",'
                result_json += current_zodiac_string
                zodiac_counter += 1
            result_json = result_json[0 : len(result_json) - 1]
            counter += 1
            result_json += "},"
        result_json = result_json[0 : len(result_json) - 1]
        result_json += "},"
    result_json = result_json[0 : len(result_json) - 1]
    result_json += "}"
    print(result_json)
    print(counter)


start()
