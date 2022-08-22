import requests
import sys
from bs4 import BeautifulSoup
import mysql.connector
import multiprocessing as mp


def my_func(x):
    x += 1
    print(x)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18021902",
        database="data1"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT id, url FROM links where id =%s",(x,))
    rows = cursor.fetchall()
    for row in rows:
        #num = 0

        
        # print(row[0])


        page_to_scrape = requests.get(row[1])
        soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
        site = soup.prettify()
        text = soup.get_text()
        val = (row[0], site, text)
        sql = "INSERT INTO content (id, html, text) VALUES (%s, %s, %s)"
        cursor.execute(sql, val)
        #print(row[0], " | ", num)

    mydb.commit()


##############################################################################################

#cursor = mydb.cursor()
pool = mp.Pool(mp.cpu_count())
lst=range(100000)
result = pool.map(my_func, lst)
