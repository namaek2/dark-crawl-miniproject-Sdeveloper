import requests,re
from bs4 import BeautifulSoup
import mysql.connector


uri_list=[]
price_list=[]
product_list=[]


def parse_product_info(soup):
    """
    상품 정보를 파싱하는 함수
    """
    try:
        # uri 파싱
        ins_uri = soup["href"]
        modified_uri = ins_uri.replace("../", "")
        uri_list.append("enter onion url" + modified_uri)

        # 상품 가격 파싱
        ins_price = soup.find("ins")
        if ins_price:
            price = ins_price.text.strip()
        else:
            price = soup.find("bdi").text.strip()
        match = re.search(r'\d+\.\d+', price)
        if match:
            price_num = match.group()
        #print("\nPrice:", price_num)
        price_list.append(price_num)

        # 상품 이름 파싱
        product_name = soup.find("h2").text
        #print("\nProduct Name:", product_name)
        product_list.append(product_name)
        
    except Exception as e:
        print("Error parsing content:", e)


def visit_url(selected_uri):
    proxies = {
        "http": "socks5h://127.0.0.1:9150",
        "https": "socks5h://127.0.0.1:9150"
    }
    

    url = selected_uri
    print('\nthis: ' + url)
    response = requests.get(url, proxies=proxies, allow_redirects=True)
    
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            section = soup.find_all("a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")
            for this in section:
                # 상품 정보 파싱
                parse_product_info(this)
                
            page = soup.find("ul", class_="page-numbers")
            pagelink = []
            if page:
                for a in page.find_all("a"):
                    href = a["href"]
                    if href.endswith(".html"):
                        #print(href)  
                        pagelink.append(href)
            
            # 마지막 요소 삭제
            if pagelink:
                del pagelink[-1]  # 마지막 요소 삭제
                
            # 각 페이지의 자식 링크들을 파싱
            for child_link in pagelink:
                child_url = "enter onion url" + child_link
                print('\nchild link: ' + child_url)
                response_child = requests.get(child_url, proxies=proxies, allow_redirects=True)
                
                if response_child.status_code == 200:
                    try:
                        soup_child = BeautifulSoup(response_child.content, "html.parser")
                        # 자식 링크에서 상품 정보 파싱
                        section_child = soup_child.find_all("a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")
                        for this_child in section_child:
                            parse_product_info(this_child)
                        
                    except Exception as e:
                        print("Error parsing child content:", e)
                else:
                    print("Failed to fetch child URL. Status Code:", response_child.status_code)
                    print("Response Headers:", response_child.headers)
                
        except Exception as e:
            print("Error parsing content:", e)
    else:
        print("Failed to fetch URL. Status Code:", response.status_code)
        print("Response Headers:", response.headers)


# 데이터 삽입 코드
def insert_data(data):
    try:
        connection = mysql.connector.connect(
            host='192.168.0.35',
            user='guest1',
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
    
# 선택한 URI
selected_uri = "enter onion url"
visit_url(selected_uri)

for u, p, n in zip(uri_list, price_list, product_list):
    print('\nuri: ' + u + '\n가격: ' + p + '\n상품이름: ' + n)
    data_to_insert = (u, p, n)
    insert_data(data_to_insert)

length = len(product_list)
print('\n상품의 총 개수: {}'.format(length))
