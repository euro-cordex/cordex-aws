import os
import sys
from os import path as op
from warnings import warn

import requests

api_url = "https://api.github.com/repos/euro-cordex/cordex-aws"


def concat_pages(pages):
    """concat all pages return by github api"""
    jobs = []
    for p in pages:
        if p.status_code == 200:
            jobs.extend(p.json()["jobs"])
        else:
            warn("reponse: p.json()")
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
    if os.environ.get("PAT"):
        headers = {"Authorization": "token " + os.environ.get("PAT")}
    else:
        headers = {}
    session = requests.Session()

    url = op.join(api_url, "actions", "runs", str(run_id), "jobs?&per_page=20")

    first_page = session.get(
        url, headers=headers
    )  # , params=querystring) #, headers=GITHUB_AUTH_HEADER)
    yield first_page

    next_page = first_page
    while next_page.links.get("next") is not None:
        next_page_url = next_page.links["next"]["url"]
        next_page = session.get(
            next_page_url, headers=headers
        )  # , params=querystring) #, headers=GITHUB_AUTH_HEADER)
        yield next_page


def handle_failures(failed):
    print(f"Jobs failed: {len(failed)}")


if __name__ == "__main__":
    run_id = int(sys.argv[1])
    pages = list(get_matrix_status(run_id))
    jobs = concat_pages(pages)
    uploads = get_upload_jobs(jobs)
    s, f = filter_by_success(uploads)
    # handle_failures(f)
    print(s)
