import requests,re
from bs4 import BeautifulSoup
import mysql.connector


product_list = []
price_list = []
current_url = []  # 각 페이지의 URL을 추적하기 위한 리스트


def parse_product_info(soup,c_url):
    """
    상품 정보를 파싱하는 함수
    """
    try:
        product = soup.find("h2").text
        # print(product+"\n")
        product_list.append(product)


        price = soup.find("bdi").text
        price_match = re.search(r'\d+\.\d+', price)
        if price_match:
            price_num = price_match.group()
            price_list.append(price_num)
        
        current_url.append(c_url)
   
        # 데이터 삽입 함수 호출
        # insert_data(data_to_insert)

    except Exception as e:
        print("Error parsing content:", e)


def visit_url():
    proxies = {
        "http": "socks5h://127.0.0.1:9150",
        "https": "socks5h://127.0.0.1:9150"
    }

    for uri in selected_uri:
        next_page = True  # 다음 페이지가 있는지 여부를 확인하기 위한 변수
        while next_page:
            response = requests.get(uri, proxies=proxies, allow_redirects=True)
            if response.status_code == 200:
                print('\ncurrent url: ' + uri)
                #current_url.append(uri)  # 현재 페이지의 URL을 추가

                try:
                    soup = BeautifulSoup(response.content, "html.parser")
                    section = soup.find("ul", class_="products columns-3")
                    if section:
                        products = section.find_all("li")
                        for product in products:
                            parse_product_info(product,uri)

                    # 다음 페이지가 있는지 확인
                    next_button = soup.find("a", class_="next page-numbers")
                    if next_button:
                        uri = next_button["href"]  # 다음 페이지로 이동
                    else:
                        next_page = False  # 다음 페이지가 없으면 반복 종료

                except Exception as e:
                    print("Error parsing content:", e)
            else:
                print("Failed to fetch URL. Status Code:", response.status_code)
                print("Response Headers:", response.headers)






# 선택한 URI
selected_uri = ['다크웹 링크들']


# 데이터 삽입 코드 및 테스트 코드

def insert_data(data):
    try:
        connection = mysql.connector.connect(
            host='****',
            user='guest4',
            password='***',
            database='***'
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
    
    
visit_url()

for p, j, url in zip(product_list, price_list, current_url):

    # 데이터 삽입 함수 호출
    insert_data((url, j, p))
    print(url, j, p)

length = len(current_url)
print('\n상품의 총 개수: {}'.format(length))


