from bs4 import BeautifulSoup
import requests

def crawling_basic():
    # 가져올 url 문자열로 입력
    url = 'http://quotes.toscrape.com/tag/love/'  

    # requests의 get함수를 이용해 해당 url로 부터 html이 담긴 자료를 받아옴
    response = requests.get(url)    

    # 우리가 얻고자 하는 html 문서가 여기에 담기게 됨
    # type: 문자열 - 구조화가 안되어있다. (파싱하기 어렵다.)
    html_text = response.text

    # html을 잘 정리된 형태로 변환
    # type: bs4.BeautifulSoup - BeautifulSoup 가 제공하는 객체로 변환
    soup = BeautifulSoup(html_text, 'html.parser')

    # 1. 태그를 이용하여 하나 검색
    # .text를 빼면 해당 a 태그 전체 코드 출력
    main = soup.find('a')
    print(f'제목 : {main.text}')

    # 2. 해당 태그인 모든 요소 검색
    a_tags = soup.find_all('a')  # 리스트 형태로 반환 (반복문 사용 가능)
    print(f'a 태그 : {a_tags}')
    # for tag in a_tags:
    #     print(f'태그: {tag.text}')

    # 3. CSS 선택자로 하나 검색
    # 선택자가 일치하는 첫 번째글
    # (웹 복습)선택자: 태그, 클래스(.), id(#)
    # 선택자에는 우선순위 존재
    word = soup.select_one('.text')  # text 라는 '클래스'가 붙어있는 첫 번째 글
    print(f'첫 번째 글 = {word.text}')

    # 4. CSS 선택자로 여러 개 검색하기
    words = soup.select('.text')
    for w in words:
        print(f'글 : {w.text}')

    # 예쁘게 출력하기
    # print(soup.prettify())


crawling_basic()
