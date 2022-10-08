from flask import Flask, render_template, request
from urlCrawler import *
from response import *

app = Flask(__name__)

#시작페이지
@app.route('/')
def startPage():
    return render_template('startPage.html')


#url 입력받음
@app.route('/urlCrawler',methods=['GET'])
def crawler():
    #시작페이지에서 url 받아옴
    url1 = request.args.get('urlInput')

    #url로 크롤링
    title, article, date = news_crawling(url1)

#---! 여기에 분석 코드 !---
    a = title,article,date

# 메인페이지 입력값 연결
    
    # 본문 문장별로 분류
    data_str, raw_len = article_split(article)

    #분석 결과
    span_input, index_cnt, transparency_Ratio, Other_transparency_Ratio, Other_title_list = response(raw_len)

    return render_template('resultPage.html',data_str = data_str,
                                        span_input = span_input,
                                        cnt = index_cnt,
                                        lenstr = raw_len,
                                        title = title,
                                        transparency_Ratio = transparency_Ratio,
                                        Other_transparency_Ratio = Other_transparency_Ratio,
                                        Other_title_list = Other_title_list,
                                        url = url1
                                        )
    

if __name__ == '__main__':
    #app.run('127.0.0.1', 5000, debug=True)
    app.run(debug=True)