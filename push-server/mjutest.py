#-*- coding:utf-8 -*-
import requests 
from bs4 import BeautifulSoup
from time import sleep

f = open('lastN.txt', 'r')
s = f.read()
f.close()

lastN = s

def send_to_topic(topc,content,title):
    print(title)
    print(content)


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
            delTAG2 = delTAG.split(']',maxsplit=1)
            send_to_topic("noti",delTAG2[1],delTAG2[0])
if ('-' not in tmp):
    lastN = tmp
print('lastN :' + lastN)

f = open('lastN.txt', 'w')
f.write(lastN)
f.close()
