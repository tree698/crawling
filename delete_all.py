import os
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


# DB에서 모든 데이터를 삭제하는 함수
def delete_all_data():
    # 데이터베이스 연결
    conn = connect_to_db()
    cursor = conn.cursor()

    # news 테이블의 모든 데이터 삭제
    cursor.execute("DELETE FROM news")

    # 변경 사항 커밋
    conn.commit()

    cursor.close()
    conn.close()
    print("DB에서 모든 데이터가 삭제되었습니다.")

if __name__ == "__main__":
    # delete_all_data()
    print('test')
