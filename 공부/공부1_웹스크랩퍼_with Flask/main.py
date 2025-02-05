
# ---------------------------------------- #

from flask import Flask, render_template, request, redirect, send_file
from CodeChallenge_클래스까지 import webScrap
from file import save_to_file

# app 변수 생성 & 초기화
# app = Flask("JobScrapper")
app = Flask(__name__)

# app 실행
# app.run("0.0.0.0")  # Not Found가 나옴
'''
[Not Found가 발생하는 이유]

user가 우리의 웹사이트에 방문하려 하지만
방문자들을 처리하는 어떤 코드도 작성하지 않았기 때문임
그래서 GET / HTTP/1.1" 404 - 발생!
이제 request하면 우리는 response해줘야 함
'''

@app.route("/")
def home():
    # return "<h1>Hello! Welcome to Job Scrapper!</h1><a href='/hello'>go to hello</a>"
    return render_template('home.html', name="lakh")
'''
@app.route("/") @가 붙은 이 형식을 decorator라고 함
간단해 보이지만 동작은 복잡함.

@app.route("/")를 def 함수 위에 두면
Flask는 user가 이 주소의 page를 방문했을 때 이 함수를 
호출해야 하는 것을 알게 됨.

하지만 @app.route("/")가 def home() 함수를
decorating하고 있을 때만 위에 서술했던 것처럼 동작함
(home이라는 이름은 사용자가 지정한 것, 얼마든지 다른 이름으로 설정해도 OK)

이 말은 무엇이냐 @app.route("/")와 def home()을 붙이지 않고
한줄이라도 떨어 뜨리면 동작하지 않는 다는 것을 의미함
 => user가 홈페이지에 방문했더라도 home 함수가 실행되지 않음

 return render_template('home.html', name="lakh") 
 => home.html에 'lakh'라는 name이라는 변수를 보냄
'''

db = {}

@app.route("/search")
def hello():
    keyword = request.args.get("keyword")
    print("키워드:", keyword, "키워드")
    
    if keyword == "":
        return redirect("/")
    
    if keyword in db:
        job_data = db[keyword]
    else:
        content = webScrap(keyword)
        content.keywordJob()
        job_data = content.beautiSoup()
        db[keyword] = job_data

    return render_template('search.html', keyword=keyword, jobs=job_data)
'''
/hello라는 새로운 경로를 만들었음 + 기존의 서버를 실행 중임 -> 서버를 종료 후 다시시작하기
=> 변경사항이 발생하면 해야하는 사항, 안 그러면 작동 X

HTML의 여러 스타일(header, nav, footer 등)을 적용하고 싶으면
"templates"라는 이름의 폴더 생성하기
=> Flask는 templates라는 이름의 폴더를 찾음
=> 폴더의 위치도 main.py 옆이어야함 (그러니까 같은 위치 level이란느 소리)

'''

@app.route("/export")
def explort():
    keyword = request.args.get("keyword")

    if keyword == None:
        return redirect("/")
    
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")

    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)

app.run("0.0.0.0")