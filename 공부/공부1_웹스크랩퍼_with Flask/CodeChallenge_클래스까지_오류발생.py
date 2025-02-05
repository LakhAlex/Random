from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import re
import csv


'''
[ 발생한 에러 ]

  File "c:\Users\jgy09\OneDrive\바탕 화면\PythonWorkspace\Nomadcoders\Python_Web\7. Build a Website with Flask_with_Python\main.py", line 61, in hello
    title = job.find("h2", itemprop="title").text.strip()  # 제목
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'text'

=> title이라는 것이 없는지 있는지 확인 하지 않고 바로 text.strip()을 진행해서 발생함
'''

class webScrap:
    def __init__(self, keyWord):
        self.keyword = keyWord
        self.all_jobs = []


    def keywordJob(self):  # 전달받은 keyword를 사용해서 페이지 내부의 내용을 저장하기

        print(f"{self.keyword} page scraping start!")

        # 동적으로 읽어야 읽히는 상황
        p = sync_playwright().start()  # playwright 시작!

        browser = p.chromium.launch(headless=True) # 브라우저 : 크롬

        page = browser.new_page() # 브라우저에 새로운 탭 생성

        page.goto(f"https://remoteok.com/remote-{self.keyword}-jobs") # keywords에 있는 직업을 검색!

        time.sleep(3) # 화면 로딩 대기

        # 스크롤을 더이상 내릴 수 없을 때까지 내리는 코드도 짜봤는데, python이나 golang이 경우 1년 이상 지난 게시물까지 전부 로딩되는걸 확인하고 아래 코드로 최종 결정.
        for i in range(4): # 스크롤 4번만 내리면 내 컴퓨터 기준 120개 정도의 게시물이 로딩됨.
            page.keyboard.down('End')
            time.sleep(5)

        content = page.content()  # 페이지 내용 가져오기
        browser.close()
        p.stop()
        
        self.content = content
        print(f"{self.keyword} page scraping finish!")


    def beautiSoup(self):  # beautifulSoup를 사용해서 원하는 데이터를 뽑아내기

        print(f"{self.keyword} job list making...") # 현재 스크랩 중인 잡을 알려줌

        soup = BeautifulSoup(self.content, "html.parser")

        jobsboard = soup.find('table', id='jobsboard'
                        ).find_all('td', class_='company position company_and_position')[1:]

        for job in jobsboard:
            link = f"https://remoteok.com{job.find('a')['href']}"  # 각각 직업에 걸려져있는 링크완성하기!
            title = job.find("h2", itemprop="title").text.strip()  # 제목
            print(title)
            company = job.find("h3", itemprop="name").text.strip()  # 회사

            location_check = job.find('div', class_='location') # 이렇게만 가져오면 location_tooltip, location_tooltip-set 까지 같이 가져오짐.
            if location_check is None: # 내용이 없어서 None 으로 불러와진 경우 편집
                location='정보 없음'
            elif 'tooltip' in location_check.get('class', []):  # 'tooltip'이 class 속성에 포함되어 있는지 확인 후 편집
                location='정보 없음'
            elif 'tooltip-set' in location_check.get('class', []):  # 'tooltip-set'이 class 속성에 포함되어 있는지 확인 후 편집
                location='정보 없음'
            else:
                location=location_check.text.strip()

            pay = job.find("div", class_="location tooltip", title=re.compile("No salary data published"))

            if pay:
                pay = pay.get_text(strip=True)  # 텍스트만 가져오고 양쪽 공백을 제거
                # print(pay)  # 💰 $60k - $130k*
            else:
                pay = "None"  # 값이 없을 경우!

            job = {
                "title" : title,
                "company" : company,
                "location" : location,
                "pay" : pay,
                "link" : link
            }

            self.all_jobs.append(job)  # 생성된 job 딕셔너리를 all_jobs 리스트에 추가!
    
        # print(self.all_jobs)
        return self.all_jobs

    

# 우리가 이제 검색하고자 하는 직업의 키워드 리스트
keywords = [
    'flutter',
    # 'python',
    # 'golang'
]

# keywords에 저장된 갯수만큼 반복
for i in range(len(keywords)):
    keyword=webScrap(keywords[i])  # 
    keyword.keywordJob()  # page의 content를 읽기
    keyword.beautiSoup()  # 읽은 content에서 원하는 정보 읽기 실행!
