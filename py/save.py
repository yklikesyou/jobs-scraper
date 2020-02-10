import csv


def save_to_file(jobs):
    file = open("jobs.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])

    for job in jobs:  # job을 가지고 row를 작성할건데, job이 가진 list를 row로 가져오게 되는 것
        writer.writerow(list(job.values()))
    return
