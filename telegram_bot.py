# import urllib.request
import requests
import urllib.parse
import datetime as dt
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import telepot

# 백그라운드에서 실행 될 스케줄러 변수
sched = BackgroundScheduler()

# 텔레그렘 챗 봇 토큰
token = 'your token'

bot = telepot.Bot(token)
old_links=[]
user_id = 0
keyword = ''

# 크롤링하기
def extract_links(old_links=[]):
    # naver 뉴스 url
    baseUrl = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query='
    # 입력받은 키워드 
    plusUrl = keyword
    url = baseUrl + urllib.parse.quote_plus(plusUrl)
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    news_list = soup.select('a.news_tit')

    links = []
    titles = []
    # 크롤링한 뉴스를 5개까지만 가져와 리스트 저장
    for news in news_list[:5] :
        link = news['href']
        title = news['title']
        links.append(link)
        titles.append(title)

    new_links=[]
    new_titles=[]
    # 새로운 리스트를 만들어 이전에 전송한 뉴스(링크)인지 채크
    for link in links:
        # 전송하지 않은 뉴스만 새로운 리스트에 담기
        if link not in old_links:
            new_links.append(link)
    
    # 새로운 리스트(링크를 담는 리스트)에 데이터가 있다면 타이틀도 새로운 리스트에 담기
    if len(new_links)>0:
        for title in titles:
            new_titles.append(title)

    return new_links, new_titles

# 크롤링한 뉴스 데이터 전송
def send_links():
    global old_links
    [new_links, new_titles] = extract_links(old_links)
    print(new_links, new_titles)
    now = dt.datetime.now()
    date = now.strftime('%Y년%m월%d일 %H:%M:%S'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
    
    # 유저에게 메시지 전송
    bot.sendMessage(chat_id=user_id, text=date+' 뉴스 업데이트')
    # 새로운 뉴스가 있으면 해당 뉴스의 타이틀과 링크 전송
    if new_links:
        for i in range(len(new_links)):
            bot.sendMessage(chat_id=user_id, text='Title : '+ new_titles[i]+'\n'+new_links[i])
    # 없으면 새로운 뉴스가 없다는 메시지 전송
    else:
        bot.sendMessage(chat_id=user_id, text='새로운 뉴스가 없습니다.')
    
    # 전송하지 않은 새로운 뉴스인지 확인을 위해 전송한 뉴스의 링크를 복사해 저장
    old_links += new_links.copy()
    # 중복된 뉴스 링크 제거
    old_links = list(set(old_links))

# 스케줄 반복(코드 일정 주기마다 실행)
def start_scedule():
    # 시작 알림 메시지 전송
    bot.sendMessage(chat_id=user_id, text='1시간 마다 새로운 뉴스가 업데이트 됩니다.')

    # 뉴스 전송 메소드 호출
    send_links()
    sched.start()
    # 스케줄 실행 주기 설정(메시지 전송 주기 설정)
    sched.add_job(send_links, 'interval', seconds=30, id="send_links")
    





# 사용자 입력 헨들러
def handle(msg) :
    global user_id
    global keyword
    # 유저 입력 정보(입력 타입, 접근타입, 유저아이디)
    content, chat, user_id = telepot.glance(msg)
    # 유저 입력 메시지의 /keyword 이후 부분만 저장
    keyword = msg['text'][9:]
    print(msg['text'])
    if content  =="text":
        # 종료 입력
        if msg['text'] == '/0':
            bot.sendMessage(user_id, text='뉴스 업데이트 서비스를 종료 합니다.')
            os._exit(1)
        # 도움말 입력
        elif msg['text'] == '/help':
            bot.sendMessage(user_id, InfoMsg)
        # 키워드 입력, 키워드 입력 시 뉴스 전송 크롤링 시작
        elif  '/keyword' in  msg['text'] :
            bot.sendMessage(user_id, text='['+keyword+']'+' 키워드로 뉴스 알림 서비스를 시작 합니다.')
            start_scedule()
        # 그 외에 입력 시 도움말 출력
        else : 
            bot.sendMessage(user_id, InfoMsg)

# 메인 함수
def main():
    bot.message_loop(handle)


# 기본 설명 메시지
InfoMsg = "뉴스 알리미.\n" \
          "[/keyword 키워드]를 입력 시 해당 키워드의 뉴스를 탐색합니다.\n" \
          "**주의** 반드시 /keyword(공백) 키워드를 입력 해야 합니다.\n"\
          "(키워드 재 입력도 동일)\n" \
          "[/0]을 입력 시 서비스가 종료 됩니다.\n" \
          "[/help]를 입력해 설명을 다시 볼 수 있습니다.\n"



status = True
while status == True:
    time.sleep(10)

if __name__ == '__main__':
    main()