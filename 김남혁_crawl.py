import requests
from bs4 import BeautifulSoup
import openpyxl
import pandas as pd
import mysql.connector

#pip install pysocks requests bs4

links = []
depth = 2

def visit_onion(onion_url, now_depth):
    global depth
    if now_depth > depth:
        return
    
    proxies = {
        "http" : "socks5h://127.0.0.1:9150",
        "https" : "socks5h://127.0.0.1:9150"
    }
    try:
        response = requests.get(onion_url, proxies=proxies, allow_redirects=True)
        response.close()

    except Exception as e:
        print(onion_url, e)
        print("\n")
        return False
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        print(onion_url + "\n")
        print("now_depth:", now_depth, "\n")

        if(now_depth == 0):
            for a in soup.findAll("a"):
                href = a.attrs.get("href")
                if "product-category" in href:
                    if href not in links:
                        links.append(href)
                        visit_onion(href, now_depth + 1)
                else:
                    continue
                
        if now_depth == 1:
            for a in soup.findAll("a"):
                href = a.attrs.get("href")
                if "product" in href:
                    if href not in links:
                        links.append(href)
                        visit_onion(href, now_depth + 1)
                else:
                    continue
            
        if now_depth == 2:
            product_title = soup.find('h1', class_='product_title').text.strip()
            print(product_title)
            price_span = soup.find_all('span', class_='woocommerce-Price-amount')
            for i, span in enumerate(price_span, start=1):
                if i == (2):
                    price_int = span.text.strip().replace("$", "")
                    price_int = int(price_int.split(".")[0])
                    print(price_int)
            data = (onion_url, price_int, product_title)
            insert_data(data)
            
            return


    else:
        print(onion_url, response.status_code, response.headers)
    return True

def insert_data(data):
    try:
        connection = mysql.connector.connect(
            host='192.168.0.35',
            user='guest5',
            password='guest',
            database='dark_web'
        )
        cursor = connection.cursor()

        # 삽입 쿼리
        insert_query = "INSERT INTO web (url, price, product) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, data)
        connection.commit()
        
        # 연결 및 커서 닫기
        cursor.close()
        connection.close()
        
        print("데이터 삽입 완료!")
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL:", error)
        return None   

book = openpyxl.Workbook()
sheet = book.active
onion_url = enter onion url here!!!
visit_onion(onion_url, 0)


