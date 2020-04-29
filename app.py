from flask import Flask, render_template
from urllib.request import urlopen, Request
import bs4
from bs4 import BeautifulSoup

#import selenium
from selenium import webdriver
app = Flask(__name__)

@app.route('/')
def hello():
    # Webpage html 읽어오는 코드
    url ='https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8'

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html5lib')
    temperature = []

    # 웹 크롤링 부분
    info_temp=soup.find('ul',class_='info_list').text.split('   ')
    info_temp[0]=info_temp[0].strip().split(',')[0]
    info_temp[1]=info_temp[1].strip().split(' ')
    t=info_temp[1][0].split('/')
    for i in t:
        temperature.append(int(i[:-1]))

    list = {'cast_txt':info_temp[0], 'temperature': info_temp[1][0],
          'min_t' : temperature[0],'max_t': temperature[1], 'sensible':info_temp[1][2],
          'image_file' :''}
    img=''
    if list['cast_txt']=='맑음':
        img='sunny'
    elif list['cast_txt']=='구름많음':
        img='suncloud'
    elif list['cast_txt'] == '흐림':
        img='cloud'
    elif list['cast_txt'] == '비':
        img='rain'
    elif list['cast_txt'] == '번개':
        img='lightning'
    list['image_file'] = img+'.png'
    print(list)

    #코디 이미지 읽어오기
    search_list = []
    driver = webdriver.Chrome('./chromedriver.exe')

    driver.implicitly_wait(3)

    if float(list['sensible'][:-1]) < 5:
        driver.get('http://bitly.kr/zES72ShsC')
    elif 5 < float(list['sensible'][:-1]) < 10:
        driver.get('http://bitly.kr/l4Bjw90Tf')
    elif 10 < float(list['sensible'][:-1]) < 15:
        driver.get('http://bitly.kr/3La7rHmtW')
    elif 15 < float(list['sensible'][:-1]) < 20:
        driver.get('http://bitly.kr/d0M88P3XJ')
    elif 20 < float(list['sensible'][:-1]) < 25:
        driver.get('http://bitly.kr/Ji3vd6tCZ')
    else:
        driver.get('http://bitly.kr/tQlnJsKme')

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for i in soup.select("#islrg > div.islrc"):
        print(i.find("img", class_="rg_i Q4LuWd tx8vtf")["src"])
        search_list.append(i.find("img", class_="rg_i Q4LuWd tx8vtf")["src"])

    return render_template("index.html", list=list, search_list=search_list, len=len(search_list))


if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)
