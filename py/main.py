# 1. get the page
# 2. make the request
# 3. extract the jobs

from indeed import get_jobs
from save import save_to_file

indeed_jobs = get_jobs()

save_to_file(indeed_jobs)
