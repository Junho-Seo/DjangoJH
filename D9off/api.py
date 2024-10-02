import requests
from pprint import pprint

API_KEY = 'ttbyts02751555001'
URL = 'http://www.aladin.co.kr/ttb/api/ItemList.aspx'
params = {
    'ttbkey': API_KEY,
    'QueryType': 'Bestseller',
    'MaxResults': 50,
    'start': 1,
    'SearchTarget': 'Book',
    'output': 'js',
    'Version': 20131101,
}

response = requests.get(URL, params=params)
print(response) # <Response [200]>
pprint(response.json())

response = response.json()

#   - 도서번호(isbn)
#   - 제목(title)
#   - 내용(description)
#   - 출간연도(pubDate)
#   - 작가(author)
#   - 판매가격(priceSales)

result = []
for item in response['item']:
    info = {
        'isbn': item['isbn'],
        'title': item['title'],
        'description': item['description'],
        'pubDate': item['pubDate'],
        'author': item['author'],
        'priceSales': item['priceSales']
    }
    result.append(info)
# print(result)
