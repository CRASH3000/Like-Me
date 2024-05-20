import requests
from bs4 import BeautifulSoup


all_sex = [
    'МУЖЧИНА',
    "ЖЕНЩИНА"
]

all_zodiac = [
    "ОВЕН", 
    "ТЕЛЕЦ",
    "БЛИЗНЕЦЫ",
    "РАК", 
    "ЛЕВ",
    "ДЕВА",
    'ВЕСЫ',
    'СКОРПИОН',
    'СТРЕЛЕЦ',  
    "КОЗЕРОГ",
    'ВОДОЛЕЙ', 
    'РЫБЫ'
]

frame_class = "j+xoX"
chart_class = 'PM-qP'

html_parser_str = "html.parser"


def start():
    url = "https://horoscopes.rambler.ru/sovmestimost-znakov-zodiaka/"
    response = requests.get(url)
    pageSoup = BeautifulSoup(response.text, html_parser_str)
    all_frames = pageSoup.find_all("div", class_=frame_class)
    counter = 0
    for sex in all_sex:
        for  zodiac in all_zodiac:
            currentFrame = str(all_frames[counter])
            currentFrameSoup = BeautifulSoup(currentFrame, html_parser_str)
            all_zodiac_chart =  currentFrameSoup.find_all("a", class_=chart_class)
            print(len(all_zodiac_chart))
            print(len(all_zodiac))
            print('-------------------')
            counter += 1;



start()
