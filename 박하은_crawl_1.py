import requests,re
from bs4 import BeautifulSoup
import mysql.connector




def category_visit(selected_uri):
    proxies = {
        "http": "socks5h://127.0.0.1:9150",
        "https": "socks5h://127.0.0.1:9150"
    }

    try:
        response = requests.get(selected_uri, proxies=proxies, allow_redirects=True)
        response.close()
    except Exception as e:
        print("Error occurred:", e)
        return []

    links = []
    category=[]
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, "html.parser")

            # 섹션을 찾습니다.
            category_section = soup.find("div", class_="panel-group category-products")
                  
            if category_section:
                # 섹션 안의 링크를 추출합니다.
                for a in category_section.find_all("a"):
                    href = a["href"]
                    if href.endswith(".html"):
                        #print(href)
                        links.append(href)
                        print(a.text.strip())
                        category.append(a.text.strip())

        except Exception as e:
            print("Error parsing content:", e)

    else:
        print("Failed to fetch URL. Status Code:", response.status_code)
        print("Response Headers:", response.headers)

    return links,category



product_list=[]
price_list=[]


def parse_product_info(soup, url):
    """
    상품 정보를 파싱하는 함수
    """
    try:
        # 상품 이름 파싱
        product_name = soup.find('p').text.strip()
        #print("\nProduct Name:", product_name)
        product_list.append(product_name)

        # 상품 가격 파싱
        price = soup.find("h2").text
        price_match = re.search(r'[\d,]+', price.replace(',', ''))
        if price_match:
            price_num = price_match.group()
            #print("\nPrice:", price_num)
            price_list.append(price_num)    

        current_url.append(url)  # 현재 URL 추가
        
    except Exception as e:
        print("Error parsing content:", e)



def visit_url():
    proxies = {
        "http": "socks5h://127.0.0.1:9150",
        "https": "socks5h://127.0.0.1:9150"
    }
    
    urls_to_parse = []  # 파싱할 URL들을 담을 리스트
    current_urls = []  # 현재 페이지의 URL들을 담을 리스트
    
    for link in category_item_links:
        url = selected_uri + '/' + link
        print('\nthis: ' + url)
        current_urls.append(url)  # 현재 페이지의 URL 추가

        response = requests.get(url, proxies=proxies, allow_redirects=True)
        
        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.content, "html.parser")
                section = soup.find_all("div", class_="productinfo text-center")

                for this in section:
                    # 상품 정보 파싱
                    parse_product_info(this, url)  # 현재 페이지의 URL 전달
                    
                page = soup.find("ul", class_="pagination")
                pagelink = []
                if page:
                    for a in page.find_all("a"):
                        href = a["href"]
                        if href.endswith(".html"):
                            pagelink.append(href)
                
                # 마지막 요소 삭제
                if pagelink:
                    del pagelink[-1]  # 마지막 요소 삭제
                    
                # 각 페이지의 자식 링크들을 파싱
                for child_link in pagelink:
                    child_url = '다크웹 링크크' + '/' + child_link
                    print('\nchild link: ' + child_url)
                    urls_to_parse.append(child_url)  # 파싱할 URL 추가
                    response_child = requests.get(child_url, proxies=proxies, allow_redirects=True)
                    
                    if response_child.status_code == 200:
                        try:
                            soup_child = BeautifulSoup(response_child.content, "html.parser")
                            # 자식 링크에서 상품 정보 파싱
                            section_child = soup_child.find_all("div", class_="productinfo text-center")
                            for this_child in section_child:
                                # 상품 정보 파싱
                                parse_product_info(this_child, child_url)  # 자식 페이지의 URL 전달
                            
                        except Exception as e:
                            print("Error parsing child content:", e)
                    else:
                        print("Failed to fetch child URL. Status Code:", response_child.status_code)
                        print("Response Headers:", response.headers)
                        
    return current_urls, urls_to_parse  # 현재 페이지의 URL과 파싱할 URL들 반환



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
    




selected_uri = "다크웹 링크"    
current_url=[]
category_item_links,category_cal = category_visit(selected_uri)
urls_to_parse = visit_url()

for p, j, url in zip(product_list, price_list, current_url):
    print('\n상품이름: ' + p + '\n가격: ' + j)
    # 데이터 삽입 함수 호출
    insert_data((url, j, p))
    print(url,j,p)
length = len(product_list)
print('\n상품의 총 개수: {}'.format(length))
