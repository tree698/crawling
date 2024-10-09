from datetime import datetime
import random

TODAY = datetime.now()
TODAY_FORMATTED = TODAY.strftime("%Y%m%d")
FAKE_USER_AGENTS = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]
KOREAN_NEWSPAPER_CODES = {
    '조선': '023',
    '중앙': '025',
    '동아': '020',
    '한국': '469',
    '경향': '032',
    '국민': '005',
    '한경': '015',
    '매경': '009',
    '서울': '081',
}


class Address:
    def __init__(self):
        self.headers = {
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "User-Agent": f'{FAKE_USER_AGENTS[random.randint(0,4)]}'
        }

        self.sites = {
            "ko": [
                {
                    "name": key,
                    "url": f"https://media.naver.com/press/{value}/newspaper",
                    "title_article-url_selectors": "._persist_wrap > div:nth-child(1) > div:nth-child(1) .newspaper_brick_item._start_page li > a",  # 기사 제목, URL CSS 셀렉터
                    "content_selectors": "#newsct_article #dic_area", # 기사 내용, 이미지 CSS 셀렉터
                    "headers": self.headers
                } for key, value in KOREAN_NEWSPAPER_CODES.items()
            ],
            "jp": [
                {
                    "name": "asahimorning",
                    "url":  f'https://www.asahi.com/shimen/{TODAY_FORMATTED}/?iref=pc_gnavi',
                    "title_article-url_selectors": "#shimen-digest > ul > li > a",
                    # "title_article-url_selectors": "#shimen-page1 > .List li:not(:nth-last-child(-n+3)) a",
                    "headers": self.headers
                },
                {
                    "name": "asahinight",
                    "url": f'https://www.asahi.com/shimen/{TODAY_FORMATTED}ev/?iref=pc_gnavi',
                    "title_article-url_selectors": ".List.ListSideImage.ListHeadline li:not(:last-child)",  # 기사 제목 CSS 셀렉터
                    "headers": self.headers
                }
            ],
            "en": [
                {
                    "name": "nyt",
                    "url": "https://www.nytimes.com/section/todayspaper?redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Finternational%2F",
                    "title_article-url_selectors": ['.css-1u3p7j1', '.css-12y5jls .css-i435f0'],  # 기사 제목, URL CSS 셀렉터
                    "headers": self.headers
                },
                # {
                #     "name": "wp",
                #     "url": "https://www.washingtonpost.com/todays_paper/updates/",
                #     "title_article-url_selectors": "#Front-Page .wpds-c-eGurKC",  # 기사 제목, URL CSS 셀렉터
                #     "headers": self.headers
                # },
                {
                    "name": "wsj",
                    "url": f'https://www.wsj.com/print-edition/{TODAY_FORMATTED}/frontpage',
                    "title_article-url_selectors": ".WSJTheme--list-item--v87pvXUl a",  # 기사 제목, URL CSS 셀렉터
                    "headers": self.headers
                },
                {
                    "name": "ft",
                    "url": "https://www.ft.com/",
                    "title_article-url_selectors": "#top-stories + .layout-desktop__grid-container .text.text--color-black.text-display--scale-3.text--weight-500",
                    # 기사 제목, URL CSS 셀렉터
                    "headers": self.headers
                },
                {
                    "name": "guardian",
                    "url": f'https://www.theguardian.com/uk?INTCMP=CE_UK',
                    "title_article-url_selectors": "section[data-link-name='most-viewed'] ol > li:nth-child(-n+3)",  # 기사 제목, URL CSS 셀렉터
                    "headers": self.headers
                },
                {
                    "name": "times",
                    "url": f'https://www.thetimes.com/uk',
                    "title_article-url_selectors": "div[class*='gre9re'] div[data-testid='lead-article-content'] a[class*='1ezjfb7'] span[class*='d9g6wh']",  # 기사 제목, URL CSS 셀렉터
                    "headers": self.headers
                },
                {
                    "name": "times",
                    "url": f'https://www.thetimes.com/uk',
                    "title_article-url_selectors": "div[class*='196m710'] div[data-testid='lead-article-content'] a[class*='1ezjfb7'] span[class*='135o9vn']",
                    "headers": self.headers
                },
            ],
            "fr": [
                {
                    "name": "monde",
                    "url": f'https://www.lemonde.fr/',
                    "title_article-url_selectors": "#habillagepub .article__list-grid li:nth-child(-n+5)",
                    "headers": self.headers
                },
            ],
            "du": [
                {
                    "name": "sz",
                    "url": f'https://www.sueddeutsche.de/',
                    "title_article-url_selectors": ".css-fhzu3t > article",
                    "headers": self.headers
                },
            ],

        }
