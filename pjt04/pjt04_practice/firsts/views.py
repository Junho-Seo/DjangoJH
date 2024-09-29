from django.shortcuts import render
from .models import Weather

import matplotlib.pyplot as plt

# io: 입출력 연산을 위한 Python 표준 라이브러리
# BytesIO: 메모리 내에서 이진 데이터를 파일처럼 다룰 수 있는 버퍼를 제공
from io import BytesIO

# 텍스트 <--> 이진 데이터 변환할 수 있는 모듈
import base64

# [참고. 터미널 에러] 데이터 분석 혹은 matplotlib 관심있다면 찾아보기
# UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
# matplotlib은 그래프 생성과 출력을 같은 곳에서 하게 되어있는데
# plt 생성과 실제 화면을 그리는 곳이 서로 다른 곳에서 동작하여 오류가 날 수 있다는 뜻
# 백엔드를 Agg로 설정하여 해결할 수 있다.
#  - Agg 설정: GUI 없이 서버 환경에서 그래프를 생성하겠다.

def index(request):
    x = [1, 2, 3, 4, 5]
    y = [1, 2, 3, 4, 5]

    plt.clf()  # 그래프 초기화
    # 요청이 많고 빠르면 broken pipe error가 발생할 수 있기 때문에 사용

    plt.plot(x, y)  # 그래프 그리기
    plt.title('Test Graph')
    plt.ylabel('y label')
    plt.xlabel('x label')

    # plt.show()  # 예전 출력 방식

    # 1. 비어있는 버퍼 생성
    buffer = BytesIO()

    # 2. 버퍼에 그래프를 저장
    plt.savefig(buffer, format='png')

    # 3. 버퍼의 내용을 base64를 활용하여 인코딩
    #   - 이미지 데이터(경로를 포함하고 있다.)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()

    # 1. 그려진 객체를 반환받아서 넘기는 방법 -> plt에서 지원하지 않음
    # 2. 이미지로저장 -> 간단하지만 용량 감당 불가
    # 3. 버퍼(임시 저장 공간)를 활용
    context = {
        # 저장된 이미지의 경로를 전달
        'chart_image': f'data:image/png;base64,{image_base64}'
    }
    return render(request, "firsts/index.html", context)


import pandas as pd


def example(request):
    # 1. csv 파일을 읽기(pandas)
    csv_path = 'firsts/data/test_data.csv'
    df = pd.read_csv(csv_path)

    # 2. DB에 저장(복습용, 데이터가 csv 파일로 있기 때문에 기능상 안 해도 됨)
    #   - 필드를 데이터를 보고 생성하는 연습
    #   - DB 관련 로직을 구현하는 연습
    #   - 중복된 데이터는 저장하지 않도록 구성
    for index, row in df.iterrows():
        # 중복 확인(이미 해당 날짜에 데이터가 저장되어 있는가?)
        # 왜 하필 날짜 데이터인가? 날짜 데이터가 unique한 필드이기 때문(유일하게 구분가능한 필드)
        # date 필드에 row의 'Date' filter 후 존재한다면 이란 의미
        if Weather.objects.filter(date=row['Date']).exists():
            continue
            
        weather = Weather(
            date = row['Date'],
            temp_avg_f = row['TempAvgF'],
            # Events 필드는 결측치를 포함
            #  - 결측치 포함 필드는 아래처럼 여러 조건을 활용
            #  삼항 연산자를 이용하여 결측치일 경우 빈 문자열 저장
            events = row['Events'] if pd.notna(row['Events']) else ""
        )
        weather.save()

    weathers = Weather.objects.all()
    context = {
        'weathers': weathers,
    }
    return render(request, 'firsts/example.html', context)