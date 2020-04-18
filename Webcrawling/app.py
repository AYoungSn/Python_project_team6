from flask import Flask, render_template
from urllib.request import urlopen, Request
import bs4
app = Flask(__name__)

@app.route('/')
def hello():
    url ='https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8'

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html5lib')
    t = soup.find('li', class_='date_info today').find('dd').text.split('/')
    temperature = []
    for i in t:
        temperature.append(int(i.split('°')[0]))
    temperature.append(soup.find('li', class_='date_info today').find('dd').text)

    return render_template("index.html", list=temperature)

if __name__ == '__main__':
    app.run()