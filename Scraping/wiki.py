import sqlite3
import requests
import sys
from bs4 import BeautifulSoup

conn = sqlite3.connect('wiki.db')



cursor = conn.cursor()
cursor.execute("SELECT id, url FROM links")

rows = cursor.fetchall()

for row in rows:
    print(row[0])
    page_to_scrape = requests.get(row[1])
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
    site=soup.prettify()
    text=soup.get_text()
    val = (row[0], site, text)
    sql = "INSERT INTO content (id, html, text) VALUES (?, ?, ?)"
    cursor.execute(sql, val)

conn.commit()
