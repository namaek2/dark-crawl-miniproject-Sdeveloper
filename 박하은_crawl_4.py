import requests,re
from bs4 import BeautifulSoup
import mysql.connector



product_list=[]
price_list=[]
current_url=[]

def parse_product_info(soup, uri):
    """
    상품 정보를 파싱하는 함수
    """
    try:
        product_name = soup.find("h2").text.strip()
        price_element = soup.find("bdi")
        if price_element:
            price = price_element.text.strip()
            #print(price)
            price_match = re.search(r'(\d+)', price)

            if price_match:
                price_num = price_match.group(1)
                price_list.append(price_num)
                #print(price_num)
            product_list.append(product_name)
            current_url.append(uri)

        else:
            print("상품 가격이 없습니다:", product_name)
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
                print('\ncurrent url: '+uri)
                try:
                    soup = BeautifulSoup(response.content, "html.parser")
                    section = soup.find("ul", class_="products columns-4")
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
    
    

# 선택한 URI
selected_uri =['다크웹 링크']
#category_item_links,category_cal = category_visit(selected_uri)
visit_url()




for p, j,k in zip(product_list, price_list,current_url):
    #print('\n상품이름: ' + p + '\n가격: ' + j)
    insert_data((k,j,p))
    print(k,j,p)
    #print('왜안됨')

length = len(price_list)
print('\n상품의 총 개수: {}'.format(length))





