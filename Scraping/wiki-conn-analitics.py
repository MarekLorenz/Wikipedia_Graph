import sqlite3
import requests
import sys
from bs4 import BeautifulSoup

conn = sqlite3.connect('wiki_1000_conn.db')



cursor = conn.cursor()
cursor.execute("SELECT id, html FROM content")

rows = cursor.fetchall()
links = []
i = 0
for row in rows:
    num=0
    if(i > 1000):
        break
    #print(row[0])
    page_to_scrape = row[1]
    soup = BeautifulSoup(page_to_scrape, 'html.parser')
   
    
    
    for link in soup.findAll('a'):
    # if "wiki" in link.getText():
        if str(link.get('href')).__contains__(":"):
            k=0

        elif str(link.get('href')).startswith("/wiki"):
            links.append(link.get('href'))
            num=num+1

    data=''.join(links)
    val = (row[0], num, data)
    sql = "INSERT INTO conn (id, num, conn) VALUES (?, ?, ?)"
    cursor.execute(sql, val)
    print(row[0]," | ",num)
    i += 1
    links.clear()
    
conn.commit()
