from flask import Flask, render_template
from urllib.request import urlopen, Request
import bs4

# import selenium
from selenium import webdriver

app = Flask(__name__)

# sensible 변수를 search 함수에도 불러오기 위해 전역변수로 설정
sense = 1


@app.route('/')
def hello():
    # Webpage html 읽어오는 코드
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8'

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html5lib')
    temperature = []

    # 웹 크롤링 부분
    info_temp = soup.find('ul', class_='info_list').text.split('   ')
    info_temp[0] = info_temp[0].strip().split(',')[0]
    info_temp[1] = info_temp[1].strip().split(' ')
    t = info_temp[1][0].split('/')
    for i in t:
        temperature.append(int(i[:-1]))

    list = {'cast_txt': info_temp[0], 'temperature': info_temp[1][0],
            'min_t': temperature[0], 'max_t': temperature[1], 'sensible': info_temp[1][2],
            'image_file': ''}

    # sense 변수 설정
    global sense
    sense = int(info_temp[1][2].split('.')[0])

    # 날씨에 맞는 이미지 로딩
    img = ''
    if list['cast_txt'] == '맑음':
        img = 'sunny'
    elif list['cast_txt'] == '구름많음':
        img = 'suncloud'
    elif list['cast_txt'] == '흐림':
        img = 'cloud'
    elif list['cast_txt'] == '비':
        img = 'rain'
    elif list['cast_txt'] == '번개':
        img = 'lightning'
    list['image_file'] = img + '.png'

    return render_template("index.html", list=list)


@app.route('/result', methods=['POST'])
def searching():
    # selenium을 이용한 크롤링을 위해 chromewebdriver 불러오기
    driver = webdriver.Chrome('./chromedriver.exe')

    # hello() 함수에서 정의한 sense를 이용해 온도에 따라 크롤링할 웹사이트의 주소를 바꾼다
    global sense

    if sense < 5:
        driver.get('http://bitly.kr/zES72ShsC')
    elif 5 < sense < 10:
        driver.get('http://bitly.kr/l4Bjw90Tf')
    elif 10 < sense < 15:
        driver.get('http://bitly.kr/3La7rHmtW')
    elif 15 < sense < 20:
        driver.get('http://bitly.kr/d0M88P3XJ')
    elif 20 < sense < 25:
        driver.get('http://bitly.kr/UXCC726nfO')
    else:
        driver.get('http://bitly.kr/tQlnJsKme')

    return render_template("result.html")


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)
