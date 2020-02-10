from indeed import extract_indeed_pages, extract_indeed_jobs

last_indeed_page = extract_indeed_pages()  # 마지막페이지 가져오고

indeed_jobs = extract_indeed_jobs(last_indeed_page)  # 마지막페이지 받아서 실행

print(indeed_jobs)
