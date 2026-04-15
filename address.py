from datetime import datetime
import random

TODAY = datetime.now()
TODAY_FORMATTED = TODAY.strftime("%Y%m%d")
FAKE_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.91 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.91 Mobile Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1'
]
KOREAN_NEWSPAPER_CODES = {
    '조선': '023',
    '중앙': '025',
    '동아': '020',
    '한국': '469',
    # '경향': '032',
    '국민': '005',
    '한경': '015',
    '매경': '009',
    '서울': '081',
}


class Address:
    def __init__(self):
        # self.headers = {
        #     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        #     "User-Agent": f'{FAKE_USER_AGENTS[random.randint(0,3)]}'
        # }
        self.headers = {
            "User-Agent": random.choice(FAKE_USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9,ko-KR,ko;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
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
                    # "title_article-url_selectors": "#shimen-digest > ul > li > a",
                    "title_article-url_selectors": "#shimen-page1 > .List li:not(:nth-last-child(-n+3)) a",
                    "headers": self.headers
                },
                {
                    "name": "asahinight",
                    "url": f'https://www.asahi.com/shimen/{TODAY_FORMATTED}ev/?iref=pc_gnavi',
                    "title_article-url_selectors": ".List.ListSideImage.ListHeadline li:not(:last-child)",  # 기사 제목 CSS 셀렉터
                    "headers": self.headers
                }
            ],
            "fr": [
                {
                    "name": "Le monde",
                    "url": f'https://www.lemonde.fr/',
                    "title_article-url_selectors": "#habillagepub .zone.zone--sectionroll.zone--sectionroll-first .article__list-grid li:nth-child(-n+5)",
                    "headers": self.headers
                },
            ],
            "du": [
                {
                    "name": "sz",
                    "url": f'https://www.sueddeutsche.de/',
                    "title_article-url_selectors": ".css-1v2ot18 > article [data-manual='teaser-title']",
                    "headers": self.headers
                },
            ],
            "en": [
                # {
                #     "name": "nyt",
                #     "url": "https://www.nytimes.com/section/todayspaper?redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Finternational%2F",
                #      "title_article-url_selectors": ['a.css-1u3p7j1', 'div.css-141drxa'],  # 기사 제목, URL CSS 셀렉터
                #     "headers": self.headers
                # },
                # {
                #     "name": "wsj",
                #     "url": f'https://www.wsj.com/print-edition/{TODAY_FORMATTED}/frontpage',
                #     "title_article-url_selectors": ".WSJTheme--list-item--v87pvXUl a",  # 기사 제목, URL CSS 셀렉터
                #     "headers": self.headers
                # },
                # {
                #     "name": "ft",
                #     "url": "https://www.ft.com/",
                #     "title_article-url_selectors": "#top-stories + .layout-desktop__grid-container .text.text--color-black.text-display--scale-3",
                #     "headers": self.headers
                # },
                {
                    "name": "times",
                    "url": f'https://www.thetimes.com/uk',
                    "title_article-url_selectors": "a.article-headline.css-njcf6b ",
                    "headers": self.headers
                },
                {
                    "name": "guardian",
                    "url": f'https://www.theguardian.com/uk?INTCMP=CE_UK',
                    "title_article-url_selectors": "section[data-link-name='most-viewed'] ol.dcr-15dwazu > li:nth-child(-n+3) h4.dcr-1vm0odd > span",
                    "headers": self.headers
                },
                # {
                #     "name": "wp",
                #     "url": "https://www.washingtonpost.com/todays_paper/updates/",
                #     "title_article-url_selectors": "#Front-Page .wpds-c-jrTvZU",  # 기사 제목, URL CSS 셀렉터
                #     "headers": self.headers
                # }
            ],
        }
