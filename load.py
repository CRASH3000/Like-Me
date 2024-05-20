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


def start():
    url = "https://horoscopes.rambler.ru/sovmestimost-znakov-zodiaka/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_frames = soup.find_all("div", class_="j+xoX")
    print(all_frames)



start()
