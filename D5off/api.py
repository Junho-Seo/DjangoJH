import requests
from pprint import pprint

API_KEY = "ttbsjh23951131001"
URL = "http://www.aladin.co.kr/ttb/api/ItemList.aspx"
params = {
    "ttbkey": "ttbsjh23951131001",
    "SearchTarget": "Book",
    "output": "js",
    "QueryType": "Bestseller",
    "MaxResults": "50",
    "Version": 20131101,
    "start": 1,
}

response = requests.get(URL, params=params)
# print(response)  # <Response [200]>
# pprint(response.json())

response = response.json()  # json으로 변환

# - 도서번호(isbn)
# - 제목(title)
# - 내용(description)
# - 출간연도(pubDate)
# - 작가(author)
# - 판매가격(priceSales)

result = []
for item in response['item']:
    info = {
        'isbn': item['isbn'],
        'title': item['title'],
        'description': item['description'],
        'pubDate': item['pubDate'],
        'author': item['author'],
        'priceSales': item['priceSales'],
    }
    result.append(info)
print(result)