from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests,re
from bs4 import BeautifulSoup
import mysql.connector

def extract_numbers(text):
    numbers = ''.join(c for c in text if c.isdigit() or c == '.') 
    return numbers

def category_visit():
    lst = []
    proxies = {
        "http": "socks5h://127.0.0.1:9150",
        "https": "socks5h://127.0.0.1:9150"
    }
    page =1
    for _ in range(2):
        try:
            response = requests.get(f"link", proxies=proxies, allow_redirects=True)
            response.close()
            print(f"{page} 페이지")
        except Exception as e:
            print("Error occurred:", e)
            return []

        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.content, "html.parser")
                d_list = soup.find("ul", class_="products columns-4")
                list_items = d_list.find_all('li')
                for i in range(len(list_items)):
                    name = list_items[i].find("h2", class_="woocommerce-loop-product__title").text
                    price = extract_numbers(list_items[i].find("bdi").text)    
                    lst.append({"url": f"link","product": f"{name}", "price": f"{price}"})
            except Exception as e:
                print("Error parsing content:", e)

        else:
            print("Failed to fetch URL. Status Code:", response.status_code)
            print("Response Headers:", response.headers)
        page += 1
    return lst

def insert_data(data):
    print("데이터 입력")
    try:
        connection = mysql.connector.connect(
            host='ip',
            user='guest3',
            password='pw',
            database='db'
        )
        cursor = connection.cursor()
        insert_query = f"INSERT INTO web (url, price, product) VALUES (%s, %s, %s)"
        cursor.execute(insert_query,data)
        connection.commit()
        
        # 연결 및 커서 닫기
        cursor.close()
        connection.close()
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL:", error)
        return None
    

data = category_visit()

for i in range(len(data)):
    data_to_query = (data[i]["url"],data[i]["price"],data[i]["product"])
    insert_data(data_to_query)

print("완료!")
