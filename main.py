from  flask import Flask, render_template, request
import requests
from extractors.scaper import get_page_number, scrape_page

app  = Flask("JobScrapper")

@app.route("/") # 데코레이터. 함수"바로위"에 데코레이터를 두면 flask는 user가 이 주소의 page를 방문했을 때 이 함수를 호출해야 하는 것을 알게됨.
def home():

    return render_template("home.html", name = "nico") # 변수를 전달하면 그 변수가 html에 전달됨. html에서는 {{변수이름}}으로 사용할 수 있음

@app.route("/search")
def search():
    page = get_page_number("https://www.berlinstartupjobs.com/engineering/")
    jobs = scrape_page("https://www.berlinstartupjobs.com/engineering/")
    keyword = request.args.get("keword")
    return render_template("search.html", keyword = keyword, page = page, jobs = jobs)

app.run("127.0.0.1")

