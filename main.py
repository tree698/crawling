import os, json
from crawling import Crawling
from datetime import datetime

date = datetime.now().strftime("%Y%m%d")

def save_to_json(data, language):
    # 'data' 폴더가 없으면 생성
    folder_name = 'data'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 파일 경로 설정 (폴더 내에 저장)
    file_path = os.path.join(folder_name, f'{language}_{date}.json')

    # 파일 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    languages = ['ko', 'jp', 'en', 'fr', 'du']

    for language in languages:
        crawler = Crawling(language)
        articles = crawler.get_articles()
        if articles:
            save_to_json(articles, language)
            print(f"{language.upper()} articles saved to {language}_{date}.json")
        else:
            print(f"No articles found for {language.upper()}")

if __name__ == "__main__":
    main()
