import requests
from bs4 import BeautifulSoup


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

HTML_PARSER_STR = "html.parser"


def start():
    url = "https://horoscopes.rambler.ru/sovmestimost-znakov-zodiaka/"
    response = requests.get(url)
    page_soup = BeautifulSoup(response.text, HTML_PARSER_STR)
    all_frames = page_soup.find_all("div", class_=FRAME_CLASS)
    counter = 0
    for sex in ALL_SEX:
        for zodiac in ALL_ZODIAC:
            current_frame = str(all_frames[counter])
            current_frame_poup = BeautifulSoup(current_frame, HTML_PARSER_STR)
            all_zodiac_chart = current_frame_poup.find_all("a", class_=CHART_CLASS)
            print(len(all_zodiac_chart))
            print(len(ALL_ZODIAC))
            print("-------------------")
            counter += 1


start()
