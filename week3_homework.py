import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

genie_chart = soup.select('#body-content > div.newest-list > div > table > tbody > tr')




for music_list in genie_chart:
    a = music_list.select_one('td.info > a')
    if a is not None:
        number = music_list.select_one('td.number').text[0:2].strip()
        title = a.text.strip()
        artist = music_list.select_one('a.artist.ellipsis').text.strip()

        print(number, title, artist)

        doc = {
            'number': number,
            'title': title,
            'artist': artist
        }
        db.genie_chart.insert_one(doc)