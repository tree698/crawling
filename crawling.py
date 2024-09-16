import requests, re
from requests.exceptions import HTTPError, RequestException, Timeout
from bs4 import BeautifulSoup
from address import Address
from datetime import datetime

DATETIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Crawling:

    def __init__(self, language):
        self.language = language
        self.address = Address().sites[language]


    def fetch_html(self, url, headers):
        try:
            response = requests.get(url, headers=headers, timeout=10)  # 10초 타임아웃 설정
            response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
            if response.status_code == 200:
                return response.content  # 원시 바이너리 데이터를 반환 (일본어 등 대응)
            else:
                print(f"Failed to retrieve data from {url} with status code {response.status_code}")
                return None
        except Timeout:
            print(f"Request timed out for {url}")
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - URL: {url}")
        except RequestException as req_err:
            print(f"Error occurred: {req_err} - URL: {url}")
        except Exception as err:
            print(f"Unexpected error: {err} - URL: {url}")
        return None


    def parse_titles(self, site):
        html_content = self.fetch_html(site["url"], site["headers"])
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')

        if self.language == 'jp':
            article_elements = soup.select(site["title_article-url_selectors"])
            articles = []
            seen_titles = set()  # 중복된 제목을 추적하기 위한 set

            for article_element in article_elements:
                title = article_element.getText().strip().replace(u"\u3000", " ")

                # 제목이 중복되지 않으면 articles에 추가
                if title not in seen_titles:
                    articles.append({
                        "name": site["name"],
                        "title": title,
                        "date": DATETIME,
                        "language": self.language
                    })
                    seen_titles.add(title)  # 제목을 중복 추적 집합에 추가

        elif self.language == 'en':
            if site.get('name') == 'nyt':
                # 첫 번째 기사 선택
                article_elements = soup.select(site["title_article-url_selectors"][0])
                articles = []
                for article_element in article_elements:
                    title = article_element.getText().strip()
                    articles.append({
                        "name": site["name"],
                        "title": title,
                        "date": DATETIME,
                        "language": self.language
                    })

                # 두 번째 기사 선택 (A1)
                title_additional = soup.select(site["title_article-url_selectors"][1])
                for article_element in title_additional:
                    is_A1 = article_element.getText().split(' ')[-1]
                    if is_A1 == 'A1':
                        title_text = article_element.select_one('h2').getText()
                        articles.append({
                            "name": site["name"],
                            "title": title_text,
                            "date": DATETIME,
                            "language": self.language
                        })
            else:
                article_elements = soup.select(site["title_article-url_selectors"])
                articles = []
                for article_element in article_elements:
                    title = article_element.getText().strip()
                    articles.append({
                        "name": site["name"],
                        "title": title,
                        "date": DATETIME,
                        "language": self.language
                    })

        else:
            article_elements = soup.select(site["title_article-url_selectors"])

            articles = []
            for article_element in article_elements:
                title = article_element.get_text().strip()
                # 제목 전처리
                cleaned_title = clean_content(title)
                url = article_element.get('href')
                if url and not url.startswith('http'):
                    url = site["url"] + url  # 상대 경로 처리
                article = {
                    "name": site["name"],  # name 필드 추가
                    "title": cleaned_title,
                    "date": DATETIME,  # date 필드 추가
                    "language": self.language,  # language 필드 추가
                    "url": url  # URL 추가 (한국어 신문만)
                }
                articles.append(article)

        return articles

    def parse_content(self, article_url, site, title):
        if self.language in ['jp', 'en']:
            return None

        html_content = self.fetch_html(article_url, site["headers"])
        soup = BeautifulSoup(html_content, "html.parser")
        article_element = soup.select_one(site["content_selectors"])

        if article_element is None:
            print(f"잘못된 selector for URL {article_url} (Title: {title})")
            return {"content": None, "image": None}

        content_element = article_element.get_text().strip() if article_element else None
        cleaned_content = clean_content(content_element)  # 기사 내용 전처리

        image_element = article_element.select_one('img')
        image = image_element.get('data-src') if image_element else None

        return {"content": cleaned_content, "image": image}


    def get_articles(self):
        all_articles = []
        for site in self.address:
            # 각 신문사의 기사를 크롤링
            articles = self.parse_titles(site)

            # 크롤링한 기사가 없으면 프롬프트에 메시지 출력
            if not articles:
                print(f"{site['name']} is empty")
            else:
                # 크롤링된 기사를 all_articles에 추가
                all_articles.extend(articles)

            # 만약 일본이나 미국 신문이 아니고, 내용 크롤링이 필요한 경우
            if self.language not in ['jp', 'en']:
                for article in articles:
                    content_data = self.parse_content(article.get("url"), site, article["title"])
                    if content_data:
                        article.update(content_data)

        return all_articles



# 한글 기사 내용 전처리
def clean_content(content):
    # 1. 줄바꿈(\n)과 탭(\t) 제거
    content = content.replace("\n", " ").replace("\t", " ")

    # 2. 특정 불필요한 문자와 기호 제거
    content = re.sub(r'[\☞\=/#◆◇-]', '', content)

    # 3. URL 제거 (https:// 또는 http://)
    content = re.sub(r'http[s]?://\S+', '', content)

    # 4. 여러 개의 쉼표 및 기타 구두점 제거
    content = re.sub(r',+', ',', content)  # 여러 쉼표를 하나의 쉼표로 대체
    content = re.sub(r'\s+', ' ', content)  # 여러 개의 공백을 하나의 공백으로 대체

    # 5. 이스케이프된 큰따옴표(\") 제거
    content = content.replace('\"', ' ')  # \" 자체를 제거

    # 6. 그 외 불필요한 문자 제거
    content = content.replace("+", "").replace("NBSP", "").strip()

    return content