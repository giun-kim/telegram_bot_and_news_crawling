# Telegram chatbot + Crawling

## 개요
텔레그램 봇을 통해 유저로부터 키워드를 입력받아 NAVER(웹 사이트)에서 해당 키워드의 뉴스를 검색 및 크롤링하여 뉴스의 타이틀과 URL을 유저에게 전송한다. 
그 후 1시간 간격으로 키워드에 대한 뉴스를 크롤링 한다. 유저에게 전송하지 않은 뉴스 정보가 크롤링 되면 해당 뉴스를 유저에게 전송한다.


## 프로그램 흐름
<img src="https://user-images.githubusercontent.com/57981257/119594809-70261000-be17-11eb-80b0-9c64213a9a24.PNG" width="350px" height="400px" title="흐름도" alt="flow diagram"></img>


## 사용 기술
Language - Python
- Telepot API
- BeautifulSoup
- requests
- Apscheduler


## 참고자료
[Telepot API](https://telepot.readthedocs.io/en/latest/)  
[Apscheduler](https://apscheduler.readthedocs.io/en/stable/userguide.html)
