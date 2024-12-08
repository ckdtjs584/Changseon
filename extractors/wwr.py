import requests
from bs4 import BeautifulSoup

def wwr_scrape_page(url):
    all_jobs = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")

    job_classfications  = soup.find_all("section", class_ = "jobs")
    print(len(job_classfications))

    for each_classfication in job_classfications:
        jobs = each_classfication.find_all("li")
        print(f"해당 분류의 job 개수 : {len(jobs)}")
        for job in jobs:
            try:
                job_data = {
            
                    "job_name" : job.find("span", class_ = "title").text,
                    "company" : job.find_all("span", class_ = "company")[0].text,
                    "work_time" : job.find_all("span", class_ = "company")[1].text,
                    "location" : job.find("span", class_ = "region").text, 
                    "link" : f"https://weworkremotely.com/{job.find('a', href=lambda x: x and x.startswith('/remote'))['href']}"
            
            
                }
                
            except:
                # 위의 4가지 요소가 없거나, 다르면 job 리스트에 넣지 않음.
                continue
            all_jobs.append(job_data)
        
        
    return all_jobs


if __name__ == "__main__":
    url = "https://weworkremotely.com/"
    all_jobs = wwr_scrape_page(url)

    for each in all_jobs:
        print(each.values())

