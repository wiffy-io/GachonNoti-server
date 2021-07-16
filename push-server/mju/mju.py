#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from time import sleep
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('../gachonnoti-firebase-adminsdk-nl9l7-da5f4a619c.json')
default_app = firebase_admin.initialize_app(cred)

f = open('lastN.txt', 'r')
s = f.read()
f.close()

lastN = s

def send_to_topic(topc, content, title):
    topic = topc
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=content
        ),
        topic=topic,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)


rq = requests.get("https://www.mju.ac.kr/mjukr/255/subview.do")
result = rq.content


soup = BeautifulSoup(result, "html.parser")
div = soup.find("table", {'class': 'artclTable artclHorNum10'})

tmp = '-'
for content in div.find_all("tr"):

    boardN = content.find("td", {'class': '_artclTdNum'})
    if boardN:
        #공지제거
        if('headline' not in content["class"]):
            #print(content["class"])
            boardN = boardN.text.strip()

            if(boardN.isnumeric()):

                if (int(lastN) < int(boardN)):
                    if ('-' in tmp):
                        tmp = boardN
                    #print(boardN)

                    title = content.find("td", {'class': '_artclTdTitle'})
                    href = title.find("a",{'class' : 'artclLinkView'})

                    title = href.find("strong").text.replace("  ", "").strip()
                    #link = 'https://www.mju.ac.kr/' + href['href'].strip()
                    #print(title)
                    #print(link)

                    send_to_topic("mju_noti", "일반공지", title)

if ('-' not in tmp):
    lastN = tmp
print('lastN :' + lastN)

f = open('lastN.txt', 'w')
f.write(lastN)
f.close()
