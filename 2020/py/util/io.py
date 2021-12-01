import requests


def filename(day):
    return "../input/2020/day{}.txt".format(day)


def download_day(day):
    session_cookie = open("../cookies.txt").read().strip().removeprefix("session=")
    url = "https://adventofcode.com/2020/day/{}/input".format(day)
    r = requests.get(url, cookies={"session": session_cookie})
    r.raise_for_status()
    data = r.text
    with open(filename(day), "w") as f:
        f.write(data)


def read(day):
    try:
        with open(filename(day)) as f:
            return f.read()
    except:
        download_day(day)
        with open(filename(day)) as f:
            return f.read()
