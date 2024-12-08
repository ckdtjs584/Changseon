import requests
from bs4 import BeautifulSoup
import pprint


# url 에 몇 개의 page가 있는지 반환하는 function
def get_page_number(url):
    response = requests.get(url, headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(response.content, "html.parser")
    page = len(soup.find_all("a", class_ = "page-numbers"))
    return page



# url 내부 job_data를 추출하여 반환하는 function
def berlinstartup_scrape_page(url):
    #웹에서 크롤링을 막는 것으로 추정되어 헤더를 수정.
    response = requests.get(url, headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find("ul", class_ = "jobs-list-items").find_all("li", class_ = "bjs-jlid")
    
    # '해당 페이지'에 있는 모든 일자리들의 데이터 배열
    jobs_data = []
    
    for job in jobs:
        job_data = {
            "job_name" : job.find("h4", class_ = "bjs-jlid__h").find("a").get_text(),
            "link" : job.find("h4", class_ = "bjs-jlid__h").find("a")["href"],
            "company" : job.find("a", class_ = "bjs-jlid__b").get_text(),
            "descryption" : job.find("div", class_ = "bjs-jlid__description").get_text(),
            
        }
        jobs_data.append(job_data)
        
    
    return jobs_data



# url 측면에 있는 skill들의 url을 담은 list를 반환하는 function
def extract_skill(url):
    response = requests.get(url, headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(response.content, "html.parser")
    skill_list = soup.find("ul", class_ = "links links-box").find_all("li", class_ = "link")

    
    # 각 skill들의 url이 있는 요소의 soup객체들을 담는 list
    skill_class_list = soup.find_all("a",class_="bjs-bl bjs-bl--dolphin")

    # 각 skill들의 url 이 담기는 리스트
    skill_url_list  = []

    # 각 skill들의 url을 리스트에 담아 반환.
    for class_ in skill_class_list:
        skill_url_list.append(class_["href"])
    return skill_url_list
    


if __name__ == '__main__':


    # 아래 url은 pagination 필요함.
    url = "https://www.berlinstartupjobs.com/engineering/"

    # "https://www.berlinstartupjobs.com/engineering/"의 모든 페이지에 있는 job data(직무, 회사, 설명) 리스트
    all_jobs_data = []

    # 모든 스킬 URL이 들어가는 리스트
    all_skill_url = []

    # 각 페이지별 job data를 전체 리스트에 추가
    for page in range(get_page_number(url)+1):
        all_jobs_data.append(berlinstartup_scrape_page(f"{url}page/{page}"))


    # "https://www.berlinstartupjobs.com/engineering/" 측면에 존재하는 여러가지 skill들을 담는 리스트 (saas, python, 등등)
    all_skill_url = extract_skill("https://www.berlinstartupjobs.com/engineering/")

    # 각각의 skill 페이지에서 job data를 추출
    for skill_url in all_skill_url:
        all_jobs_data.append(berlinstartup_scrape_page(skill_url))


    pprint.pprint(all_jobs_data) 