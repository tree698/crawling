import csv, os
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# MySQL 데이터베이스 연결 설정
def connect_to_db():
    return mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE')
    )


# 날짜 형식 변환 함수 (2022/08/23 형식 처리)
def convert_date_format(date_str):
    try:
        # '2022/08/23' 형식을 '2022-08-23'로 변환
        return datetime.strptime(date_str, '%Y/%m/%d').strftime('%Y-%m-%d')
    except ValueError:
        return None  # 변환 실패 시 None 반환


# CSV 파일 데이터를 DB에 저장하는 함수
def save_csv_to_db(file_path, language):
    # 데이터베이스 연결
    conn = connect_to_db()
    cursor = conn.cursor()

    # CSV 파일 열기
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            # 날짜를 처리
            date_str = row.get('date')  # date 컬럼
            date = convert_date_format(date_str)
            if not date:
                print(f"날짜 형식 오류: {date_str} -> 무시됨")
                continue  # 날짜 형식이 맞지 않으면 건너뜀

            # 각 신문사별 기사 제목 처리
            for name, titles in row.items():
                if name in ['date', 'week'] or not titles:  # date와 week는 건너뜀
                    continue

                # 기사 제목을 &&& 기준으로 나눔
                title_list = titles.split('&&&')

                for title in title_list:
                    title = title.strip()  # 제목 앞뒤 공백 제거

                    # 데이터베이스에 삽입
                    cursor.execute('''
                        INSERT INTO news (name, title, date, language)
                        VALUES (%s, %s, %s, %s)
                    ''', (name, title, date, language))

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    # CSV 파일 경로 설정
    ko_file_path = './data/KO_news.csv'  # 한국어 기사 파일 경로
    en_file_path = './data/EN_news.csv'
    jp_file_path = './data/JP_news.csv'

    # 한국어 기사 (language='ko')
    # save_csv_to_db(ko_file_path, 'ko')
    # save_csv_to_db(en_file_path, 'en')
    # save_csv_to_db(jp_file_path, 'jp')

    print("CSV 데이터를 DB에 성공적으로 저장했습니다.")