import requests
from bs4 import BeautifulSoup

# web3의 특정 url에 몇 페이지까지 있는지 알아내는 function
def web3_get_page(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")

     #page 확인 -> 구한 길이 -3을 해주어야 함. (prev, next, ...버튼 3가지 제외)
    page = len(soup.find("ul", class_ = "pagination"))-3
    return page


# tbody에 박스들이 존재.
def web3_scrape_page(url):

    all_jobs_data = []
    response = requests.get(url)

    soup = BeautifulSoup(response.content,"html.parser")

   
    

    jobs = soup.find("tbody", class_ = "tbody").find_all("tr", class_ = "table_row")
    for each_job in jobs:
        try:
            job_data = {
                "job_name" : each_job.find("h2").text,
                "company" : each_job.find("h3").text,
                "location": each_job.find_all('a', style="font-size: 12px; color: #d5d3d3;"),
                "link" : f"https://web3.career/{each_job.find('a', attrs={"data-turbo-frame": "job"})['href']}"
                

            }
            # 지역이 여러개인 경우가 있어서 이런 경우에는 각각의 지역요소를  text로 변환해주어야 함
            if len(job_data["location"]) > 1:
                length = len(job_data["location"])
                i = 0
                for i in range(0,length):
                    job_data["location"][i] = job_data["location"][i].text
            elif len(job_data["location"]) == 0:
                job_data["location"] = "Remote"
            else :
                job_data["location"][0] = job_data["location"][0].text
            

        except:
            continue
        all_jobs_data.append(job_data)

    return all_jobs_data
    
if __name__ == "__main__":
    print(web3_scrape_page("https://web3.career/python-jobs"))