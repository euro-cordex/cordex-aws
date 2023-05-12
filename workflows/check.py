import sys
from os import path as op

import requests

api_url = "https://api.github.com/repos/euro-cordex/cordex-aws"


def concat_pages(pages):
    """concat all pages return by github api"""
    jobs = []
    for p in pages:
        jobs.extend(p.json()["jobs"])
    return jobs


def get_upload_jobs(jobs, filt="upload"):
    """filter jobs to get only jobs that upload"""
    return [j for j in jobs if filt in j["name"]]


def filter_by_success(jobs):
    """split jobs and retun a list of successful and failed datasets iids"""
    success = []
    failed = []
    for j in jobs:
        iid = j["name"].split()[-1]
        if j["conclusion"] == "success":
            success.append(iid)
        else:
            failed.append(iid)
    return (success, failed)


def get_matrix_status(run_id):
    # header = {}
    # headers = {'Authorization': 'token ' + os.environ["PAT"]}
    session = requests.Session()

    url = op.join(api_url, "actions", "runs", run_id, "jobs?&per_page=20")

    first_page = session.get(
        url
    )  # , params=querystring) #, headers=GITHUB_AUTH_HEADER)
    yield first_page

    next_page = first_page
    while next_page.links.get("next") is not None:
        next_page_url = next_page.links["next"]["url"]
        next_page = session.get(
            next_page_url
        )  # , params=querystring) #, headers=GITHUB_AUTH_HEADER)
        yield next_page


def update_catalog():
    pass


if __name__ == "__main__":
    run_id = int(sys.argv[1])
