import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&l=%EC%84%9C%EC%9A%B8&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)
    # 해당 사이트의 html을 가져옴. 데이터를 탐색하고 추출하기 위해.
    soup = BeautifulSoup(result.text, "html.parser")
    # page 태그(=pagination) 얘들 뭉태기로 데려오기

    pagination = soup.find("div", {"class": "pagination"})
    # find는 첫번째 찾은 결과, find_all은 리스트 전부를 가져옴

    links = pagination.find_all('a')
    # anchor 얘들 리스트 형태로 links변수에 넣어줌. links를 따로 리스트로 선언안해도, find_all 하면 리스트로 들어감

    pages = []
    for link in links[:-1]:     # 마지막 next 빼고 가져오는것 list에서 [-1]은 마지막 요소를 뜻함
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("div", {"class": "title"}).find("a")["title"]
    # result는 일자리목록, 그 안에서 class명이 title인 div를 찾았지,그리고 그 안에서 anchor를 찾아서 그 attribute인 title을 가져왔어.
    # anchor = title.find("a")["title"] 생략하고 title한줄로 했음
    company = html.find('span', {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()  # strip(안에 있는 걸 다 없애서 출력함) 그냥 두면 끝쪽의 빈칸을 없애는 것
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {"title": title, 'company': company, 'location': location, "link": f"https://kr.indeed.com/viewjob?jk={job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):  # range는 0부터 해당 숫자까지
        print(f"Scrapping page {page}")
        # 50개씩 출력되게 했으니까 + 첫페이지 start=0 맞음
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        # jobsearch-SerpJobCard 뒤에 unifiedRow row result clickcard 는 생략
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()  # 마지막페이지 가져오고
    jobs = extract_jobs(last_page)  # 마지막페이지 받아서 실행
    return jobs
