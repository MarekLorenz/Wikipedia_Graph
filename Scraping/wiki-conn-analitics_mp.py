import multiprocessing as mp
import sqlite3
import requests
import sys
from bs4 import BeautifulSoup

def my_func(x):
    x += 1
    conn = sqlite3.connect('wiki_1000_conn.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, html FROM content where id =?",(x,))
    rows = cursor.fetchall()
    for row in rows:
        num = 0

        links = []
        # print(row[0])
        page_to_scrape = row[1]
        soup = BeautifulSoup(page_to_scrape, 'html.parser')

        for link in soup.findAll('a'):
            # if "wiki" in link.getText():
            if str(link.get('href')).__contains__(":"):
                k = 0

            elif str(link.get('href')).startswith("/wiki"):
                links.append(link.get('href'))
                num = num + 1

        data = ''.join(links)
        val = (row[0], num, data)
        sql = "INSERT INTO conn (id, num, conn) VALUES (?, ?, ?)"
        cursor.execute(sql, val)
        print(row[0], " | ", num)
        links.clear()
    conn.commit()


##############################################################################################
conn = sqlite3.connect('wiki_1000_conn.db')
cursor = conn.cursor()
pool = mp.Pool(mp.cpu_count())
lst=range(1000)
result = pool.map(my_func, lst)
conn.commit()

