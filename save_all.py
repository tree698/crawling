import os
import json
import mysql.connector
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


# JSON 파일을 읽고 데이터베이스에 저장하는 함수
def save_json_to_db(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)  # JSON 파일 읽기

    # 데이터베이스 연결
    conn = connect_to_db()
    cursor = conn.cursor()

    for article in articles:
        # 각 기사 데이터를 삽입
        cursor.execute('''
                INSERT INTO news (name, title, content, date, language, url, image, summary, memo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
            article.get("name"),
            article.get("title"),
            article.get("content", ""),  # content 필드 추가
            article.get("date"),
            article.get("language"),
            article.get("url", None),  # 한국 신문일 경우 URL
            article.get("image", None),  # 한국 신문일 경우 이미지
            article.get("summary", ""),  # 요약 (필요시)
            article.get("memo", ""),  # 메모 (필요시)
        ))

    conn.commit()
    cursor.close()
    conn.close()


# 데이터 폴더 내 JSON 파일을 순차적으로 읽고 처리
def process_all_json_files(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory, file_name)
            print(f"Processing {file_path}")
            save_json_to_db(file_path)


if __name__ == "__main__":
    # JSON 파일들이 저장된 경로
    # json_data_directory = './data'

    # 모든 JSON 파일을 읽고 데이터베이스에 저장
    # process_all_json_files(json_data_directory)
    print("모든 파일이 데이터베이스에 성공적으로 저장되었습니다.")
