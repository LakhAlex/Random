from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import re
import csv


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

    def beautiSoup(self):  
        """BeautifulSoup을 사용해 데이터를 스크랩하여 반환하는 함수"""

        print(f"{self.keyword} job list making...")  # 현재 스크랩 중인 작업을 출력

        soup = BeautifulSoup(self.content, "html.parser")
        jobsboard = soup.find('table', id='jobsboard') \
                        .find_all('td', class_='company position company_and_position')[1:]

        for job in jobsboard:
            # 링크 가져오기
            link_tag = job.find('a')
            link = f"https://remoteok.com{link_tag['href']}" if link_tag else "링크 없음"

            # 제목 가져오기
            title_tag = job.find("h2", itemprop="title")
            title = title_tag.text.strip() if title_tag else "제목 없음"

            # 회사 이름 가져오기
            company_tag = job.find("h3", itemprop="name")
            company = company_tag.text.strip() if company_tag else "회사 정보 없음"

            # 위치 가져오기
            location_check = job.find('div', class_='location')
            if location_check is None:
                location = '정보 없음'
            elif 'tooltip' in location_check.get('class', []):
                location = '정보 없음'
            elif 'tooltip-set' in location_check.get('class', []):
                location = '정보 없음'
            else:
                location = location_check.text.strip()

            # 급여 정보 가져오기
            pay_tag = job.find("div", class_="location tooltip", title=re.compile("No salary data published"))
            pay = pay_tag.get_text(strip=True) if pay_tag else "급여 정보 없음"

            # 결과를 딕셔너리로 저장
            job_data = {
                "title": title,
                "company": company,
                "location": location,
                "pay": pay,
                "link": link
            }

            self.all_jobs.append(job_data)  # 생성된 job 딕셔너리를 all_jobs 리스트에 추가

        print(self.all_jobs)
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









'''
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import re
import csv

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

        jobsboard = soup.find('table', id='jobsboard')

        if jobsboard:  # 'jobsboard' 테이블이 있는지 확인
            jobsboard = jobsboard.find_all('td', class_='company position company_and_position')[1:]

            for job in jobsboard:
                # 링크 처리
                link_tag = job.find('a')
                if link_tag and 'href' in link_tag.attrs:
                    link = f"https://remoteok.com{link_tag['href']}"
                else:
                    link = "링크를 찾을 수 없음"

                # 제목 처리
                title_tag = job.find("h2", itemprop="title")
                if title_tag and title_tag.text.strip():
                    title = title_tag.text.strip()
                else:
                    title = "제목을 찾을 수 없음"

                print(f"Title: {title}, Link: {link}")
        else:
            print("jobsboard 테이블을 찾을 수 없습니다.")

    

# 우리가 이제 검색하고자 하는 직업의 키워드 리스트
keywords = [
    'flutter',
]

# keywords에 저장된 갯수만큼 반복
for i in range(len(keywords)):
    keyword=webScrap(keywords[i])  # 
    keyword.keywordJob()  # page의 content를 읽기
    keyword.beautiSoup()  # 읽은 content에서 원하는 정보 읽기 실행!
'''
