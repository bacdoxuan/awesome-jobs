"""
Create jobs.db for website
"""
import sqlite3
from urllib.parse import urlencode
import requests


def init_jobs_db():
    """get jobs information from https://github.com/awesome-jobs/vietnam/issues
    and store them in a sqlite3 database named jobs.db
    """
    url_base = 'https://api.github.com/repos/awesome-jobs/vietnam/issues?'
    param = ({'page': 1})
    url = '{}{}'.format(url_base, urlencode(param))
    req = requests.get(url)
    link = req.headers['link']
    no_pages = int(link[link.rfind('e=') + 2: link.rfind('>')])

    conn = sqlite3.connect('jobs.db')
    cur = conn.cursor()
    cur.execute('drop table if exists jobs')
    cur.execute('''create table jobs (
                job_title text,
                job_html_url text
                )
                ''')

    jobs_list = []

    for i in range(1, no_pages + 1):
        param = ({'page': i})
        url = '{}{}'.format(url_base, urlencode(param))
        req = requests.get(url)
        for job in req.json():
            jobs_list.append((job['title'], job['html_url']))

    try:
        cur.executemany('INSERT INTO jobs VALUES (?,?)', jobs_list)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()


def main():
    """
    initiate the database
    """
    init_jobs_db()


if __name__ == "__main__":
    main()
