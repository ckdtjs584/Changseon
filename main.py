from  flask import Flask, redirect, render_template, request, send_file
from extractors.berlinstartup import berlinstartup_scrape_page
from extractors.wwr import wwr_scrape_page
from extractors.web3 import web3_scrape_page
from file import save_to_file


app  = Flask("JobScrapper")

# 가짜 DB 생성
db = {}

@app.route("/") # 데코레이터. 함수"바로위"에 데코레이터를 두면 flask는 user가 이 주소의 page를 방문했을 때 이 함수를 호출해야 하는 것을 알게됨.
def home():
    keyword = request.args.get("keyword")
    return render_template("home.html", keyword=keyword) # 변수를 전달하면 그 변수가 html에 전달됨. html에서는 {{변수이름}}으로 사용할 수 있음

@app.route("/search")
def search():

    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")

    if keyword in db:
        print(f"{keyword}로 검색한 이력이 DB에 존재합니다.")
        keyword_job_list = db[keyword]
    else:
        # 해당 URL에 keyword관련 job list를 반환
        berlinstartup_job_list = berlinstartup_scrape_page(f"https://berlinstartupjobs.com/skill-areas/{keyword}")
        web3_job_list = web3_scrape_page(f"https://web3.career/{keyword}-jobs")
        wwr_job_list  = wwr_scrape_page(f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}")

        keyword_job_list = berlinstartup_job_list + web3_job_list + wwr_job_list
        db[keyword] = keyword_job_list
             
    return render_template("search.html", keyword=keyword, jobs=keyword_job_list)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    
    if keyword not in db:
        print("asdfas")
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)

#잘못된 주소로 접근했을 때 루트로 리다이렉트
@app.errorhandler(404)
def page_not_found(error):
    return redirect('/')

@app.errorhandler(500)
def page_not_found(error):
    return redirect('/')


app.run("0.0.0.0")

