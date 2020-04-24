from flask import Flask, render_template
from urllib.request import urlopen, Request
import bs4
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
    info_temp[1]=info_temp[1].strip().split(' ')
    t=info_temp[1][0].split('/')
    for i in t:
        temperature.append(int(i[:-1]))
    list={'cast_txt':info_temp[0].strip().split(',')[0], 'temperature': info_temp[1][0],
          'min_t':temperature[0],'max_t': temperature[1], 'sensible':info_temp[1][2]}
    print(list)
    return render_template("index.html", list=list)

if __name__ == '__main__':
    app.run(debug=True)