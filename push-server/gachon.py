#-*- coding:utf-8 -*-
import requests 
from bs4 import BeautifulSoup
from time import sleep
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('gachonnoti-firebase-adminsdk-nl9l7-da5f4a619c.json')
default_app = firebase_admin.initialize_app(cred)

f = open('lastN.txt', 'r')
s = f.read()
f.close()

lastN = s

def send_to_topic(topc,content):
    topic = topc
    message = messaging.Message(
        notification = messaging.Notification(
           title='[Notice]',
           body=content
            ),
        topic=topic,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)


rq = requests.get("http://m.gachon.ac.kr/gachon/notice.jsp?boardType_seq=358")
result = rq.content

soup = BeautifulSoup(result,"html.parser")
div = soup.find("div",{'class' : 'list'})

tmp = '-'
for content in div.find_all("li"):
    #print(content)
    if ('/icons/icon_notice.gif' not in str(content)):
        delTAG = BeautifulSoup(str(content)).text
        #delTAG = BeautifulSoup(str(content), "lxml").text
        delTAG = delTAG.replace("\n", "").replace("  ", "")
        href = 'http://m.gachon.ac.kr/gachon/' + content.find('a')['href']
        boardN = href.split('board_no=')[1].split('&')[0]
        if (int(lastN) < int(boardN)):
            if ('-' in tmp):
                tmp = boardN
            #print(delTAG)
            print(href)
            print(boardN)
            send_to_topic("noti",delTAG)
if ('-' not in tmp):
    lastN = tmp
print('lastN :' + lastN)

f = open('lastN.txt', 'w')
f.write(lastN)
f.close()
