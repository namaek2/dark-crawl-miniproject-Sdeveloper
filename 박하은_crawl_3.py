import requests,re
from bs4 import BeautifulSoup
import mysql.connector



product_list=[]
price_list=[]
current_url=[]

def parse_product_info(soup,url):
    """
    상품 정보를 파싱하는 함수
    """
    try:
        product = soup.find("h2").text
        #print(product+"\n")
        product_list.append(product)


        price = soup.find("bdi").text
        price_match = re.search(r'\d+\.\d+', price)
        if price_match:
            price_num = price_match.group()
            price_list.append(price_num)
        current_url.append(url)
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

        

            except Exception as e:
                print("Error parsing content:", e)
        else:
            print("Failed to fetch URL. Status Code:", response.status_code)
            print("Response Headers:", response.headers)


            

# 선택한 URI
selected_uri =['다크웹 링크들']
#category_item_links,category_cal = category_visit(selected_uri)





# 데이터 삽입 코드 및 테스트 코드

def insert_data(data):
    try:
        connection = mysql.connector.connect(
            host='192.168.0.35',
            user='guest4',
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
    

visit_url()




for p, j,k in zip(product_list, price_list,current_url):
    #print('\n상품이름: ' + p + '\n가격: ' + j)
    insert_data((k,j,p))
    print(k,j,p)

length = len(current_url)
print('\n상품의 총 개수: {}'.format(length))
