from bs4 import BeautifulSoup
import requests
import math
import psycopg2
import random
import time
import datetime
import os


currentDateTime = datetime.datetime.now()
POSTGRES_DATABASE_HOST_ADDRESS = 'ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com'
POSTGRES_DATABASE_NAME = 'd2bib13eka3ngm'
POSTGRES_USERNAME = 'uf4c8m5ko9g43g'
POSTGRES_PASSWORD = 'p864da304922dcf7c9b57f57b3e58283892e585f147e8bfe622e89a5ab1ab1d87'
POSTGRES_CONNECTION_PORT = "5432"

db_info = "host='%s' dbname='%s' user='%s' password='%s' sslmode='require'  port='%s'" % (
    POSTGRES_DATABASE_HOST_ADDRESS, POSTGRES_DATABASE_NAME, POSTGRES_USERNAME, POSTGRES_PASSWORD,
    POSTGRES_CONNECTION_PORT)
con = psycopg2.connect(db_info)
cur = con.cursor()
# cur.execute("CREATE TABLE krakow(id INTEGER PRIMARY KEY, date TIMESTAMP, price, district, rooms, area, sqr_price, floor)")
# cur.execute("CREATE TABLE krakow_rent(id INTEGER PRIMARY KEY, date TIMESTAMP, price, district, rooms, area, floor)")
# cur.execute("CREATE TABLE warszawa(id INTEGER PRIMARY KEY, date TIMESTAMP, price, district, rooms, area, sqr_price, floor)")
# cur.execute("CREATE TABLE warszawa_rent(id INTEGER PRIMARY KEY, date TIMESTAMP, price, district, rooms, area, floor)")
#cur.execute("CREATE TABLE krakow_house(id INTEGER PRIMARY KEY, date TIMESTAMP, price INT, district VARCHAR(255), rooms INT"
#           ", area INT, sqr_price INT, floor INT);")
#con.commit()
#cur.close()

headers = {'User-Agent': '...'}


cities = {
    'krakow_sell': [f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/malopolskie/krakow/krakow/"
                    f"krakow?viewType=listing&page=", 'krakow', 'Kraków'],
    'krakow_rent': [f"https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/malopolskie/krakow/krakow/"
                    f"krakow?ownerTypeSingleSelect=ALL&distanceRadius=0&viewType=listing&page=", "krakow_rent",
                    'Kraków'],
    'krakow_house': ["https://www.otodom.pl/pl/wyniki/sprzedaz/dom/malopolskie/krakow/krakow/krakow?"
                     "ownerTypeSingleSelect=ALL&distanceRadius=5&viewType=listing&page=", "krakow_house"],
    'warszawa_sell': [f'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/'
                      f'warszawa?viewType=listing&page=', "warszawa", 'Warszawa'],
    'warszawa_rent': [f'https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa/warszawa/'
                      f'warszawa?ownerTypeSingleSelect=ALL&distanceRadius=0&viewType=listing&page=', 'warszawa_rent',
                      'Warszawa']
}


number_in_string = [str(x) for x in range(10)]

def rent(city):
    global number_in_string
    start = True
    page = 1
    last_page = float('inf')
    statement = f'''SELECT max(id)  FROM {city[1]}'''
    cur.execute(statement)
    id_add = int(cur.fetchone()[0]) + 1
    print(id_add)
    url = city[0]
    table = city[1]
    localization = city[2]
    while start:

        print(page)
        url_link = url + str(page)
        result = requests.get(url_link, headers=headers).text
        doc = BeautifulSoup(result, "html.parser")

        if last_page == float('inf'):
            last_page = int(doc.find_all(class_='css-1tospdx')[-1].text)
            print(last_page)

        res = doc.find_all(class_="css-13gthep")

        for i in res:
            price, rooms, area, floor = 0, 0, 0, -1
            district = 'N/A'
            if i.find(class_='css-1uwck7i').text != "Zapytaj o cenę":
                print(i.find(class_='css-1uwck7i').text, 'A moje to', i.find(class_='css-1uwck7i').text[0:4])
                try:
                    price = ''
                    for j in i.find(class_='css-1uwck7i').text:
                        if j in number_in_string:
                            price += j
                        elif j == ' ':
                            pass
                        else:
                            break
                    price = int(price)
                    print(price)
                    city = i.find(class_='css-1dvtw4c').text.split()[-2:-1][0][0:-1]
                    if city == localization:
                        district = i.find(class_='css-1dvtw4c').text.split()[-3:-2][0][0:-1]
                    print(i.find(class_='css-uki0wd').text.split())
                    for text in i.find(class_='css-uki0wd').text.split():
                        if 'pokoi' in text:
                            rooms = int(text[-1])
                        if 'pokojePowierzchnia' in text or 'pokójPowierzchnia' in text or 'pokoiPowierzchnia' in text:
                            area = int(math.floor(float(text.split('a')[-1])))
                        if 'm²Piętro'.lower() in text.lower():
                            floor = text.split('o')[-1]
                            print(floor)
                            if floor == 'parter':
                                floor = 0
                            else:
                                floor = int(text.split('o')[-1])
                except ValueError:
                    price, rooms, area, floor = 0, 0, 0, -1
            if rooms == 1 and area > 100:
                price, rooms, area, floor = 0, 0, 0, -1
            if price != 0 and rooms != 0 and area != 0 and floor != -1:
                insertQuery = f"""INSERT INTO {table} VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cur.execute(insertQuery, (id_add, currentDateTime, price, district, rooms, area, floor))

            id_add += 1
        con.commit()
        page += 1
        time.sleep(random.random() * 10)
        if page == last_page + 1:
            start = False


def sell(city):
    start = True
    page = 1
    last_page = float('inf')

    try:
        statement = f'''SELECT max(id)  FROM {city[1]}'''
        cur.execute(statement)
        id_add = int(cur.fetchone()[0]) + 1
    except:
        id_add = 1

    url = city[0]
    table = city[1]
    while start:
        print(page, "page number", last_page, 'last_page')
        url_link = url + str(page)
        result = requests.get(url_link, headers=headers).text
        doc = BeautifulSoup(result, "html.parser")

        if last_page == float('inf'):
            last_page = int(doc.find_all(class_='css-1tospdx')[-1].text)
            print(last_page)

        res = doc.find_all(class_="css-13gthep")

        for i in res:
            price, rooms, area, sqr_price, floor, a = 0, 0, 0, 0, 0, -1
            district = 'N/A'
            if i.find(class_='css-1uwck7i').text != "Zapytaj o cenę":
                print(i.find(class_='css-1uwck7i').text)
                try:
                    price = int(''.join(i.find(class_='css-1uwck7i').text.split()[0:-1]))
                    district = i.find(class_='css-1dvtw4c').text.split()[-3:-2][0][0:-1]
                    print(i.find(class_='css-uki0wd').text.split())
                    for text in i.find(class_='css-uki0wd').text.split():
                        if 'pokoi' in text:
                            rooms = int(text[-1])
                        if 'pokojePowierzchnia' in text or 'pokójPowierzchnia' in text or 'pokoiPowierzchnia' in text:
                            area = int(math.floor(float(text.split('a')[-1])))
                        if 'kwadratowy' in text:
                            sqr_price = int(text.split('y')[-1])
                            if sqr_price < 100:
                                sqr_price *= 1000
                        if 'zł/m²Piętro'.lower() in text.lower():
                            floor = text.split('o')[-1]
                            print(floor)
                            if floor == 'parter':
                                floor = 0
                                print("first condition")
                            else:
                                floor = int(text.split('o')[-1])
                except ValueError:
                    price, rooms, area, sqr_price, floor, a = 0, 0, 0, 0, 0, -1
            if rooms == 1 and area > 100:
                price, rooms, area, sqr_price, floor, a = 0, 0, 0, 0, 0, -1
            if price != 0 and rooms != 0 and area != 0 and sqr_price != 0 and floor != -1:
                print(id_add, price, district, rooms, area, sqr_price, floor)
                insertQuery = f"""INSERT INTO {table} VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                cur.execute(insertQuery, (id_add, currentDateTime, price, district, rooms, area, sqr_price, floor))

            id_add += 1
        con.commit()
        page += 1
        time.sleep(random.random() * 5)
        if page == last_page + 1:
            start = False


def deleting_duplicates(city, rents):
    delete_statement = f"delete from {city} WHERE id IN " \
                           f" (SELECT id FROM "\
                                " (SELECT id, ROW_NUMBER() OVER" \
                                f"( PARTITION BY district, area, rooms,{rents} date, price" \
                                " ORDER BY  id ) AS row_num" \
                                f" FROM {city}) t"\
                                " WHERE t.row_num > 1 );"
    cur.execute(delete_statement)
    con.commit()


deleting_duplicates("warszawa_rent", "")
