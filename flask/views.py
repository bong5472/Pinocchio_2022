import pattern_match
from dateutil.relativedelta import relativedelta
import json
import requests
import datetime

# Create your views here.
def firstApi(crawl_title,crawl_article,crawl_date):
        # SERVICE SEQUENCE

        # 1. 사용자로부터 제목과 본문을 입력받음
        title = crawl_title.replace('"', '\\"')
        document_text = crawl_article
        datelist = list(map(int, crawl_date.split(".")))
        date = datetime.datetime(datelist[0], datelist[1], datelist[2])

        # 2. 유사한 영역의 기사 5개 탐색(BigKinds API - POST METHOD)
        SERVICE_KEY = "ce44aee0-5d38-483b-9d85-e54db6286df0"
        BASE_URL = "http://tools.kinds.or.kr:8888"
        # 2-1. KEY WORD FINDING
        response = requests.post(BASE_URL + "/keyword", data = json.dumps({"access_key": SERVICE_KEY,
                                                                           "argument": {"title": title}}))
        keywords = response.json()["return_object"]["result"]["title"].split()

        # 2-2. 기사 검색
        queryText = " OR ".join(keywords)
        titles = []
        articles = []
        fields = ["title", "content"]
        fromdate = date + relativedelta(days=-7)
        response = requests.post(BASE_URL + "/search/news", data=json.dumps({"access_key": SERVICE_KEY,
                                                                               "argument": {"query": queryText,
                                                                                            "published_at": {
                                                                                                "from": str(fromdate.date()),
                                                                                                "until": str(date.date())
                                                                                            },
                                                                                            "sort": [
                                                                                                {"date":"desc"}, {"_score":"desc"}
                                                                                            ],
                                                                                            "return_from": 0,
                                                                                            "return_size": 5,
                                                                                            "fields": fields}}))
        for document in response.json()["return_object"]["documents"]:
            titles.append(document["title"])
            articles.append(document["content"])
        articles.append(document_text)
        # 3. 상위 5개 기사 유사도와 함께 Return
        tot_tratio = 0.0
        tot_tratio2 = 0.0
        DTO = {}
        for i in range(0, len(articles)):
            # 마지막
            if i == len(articles) - 1:
                transparency_Ratio, hazard_cnt, predict_sentences, hazard_sentences = pattern_match.master(articles[i])
                DTO["transparency_Ratio"] = round(transparency_Ratio, 2)
                DTO["hazard_Ratio"] = hazard_cnt
                DTO["predcitive_Reporting"] = predict_sentences
                DTO["provocative_Reporting"] = hazard_sentences
                DTO["Other_transparency_Ratio"] = round(tot_tratio / (len(articles) - 1), 2)
                DTO["Other_hazard_Ratio"] = round(tot_tratio2 / (len(articles) - 1), 2)
                DTO["Other_title_list"] = titles
            else:
                transparency_Ratio, hazard_cnt, predict_sentences, hazard_sentences = pattern_match.master(articles[i])
                tot_tratio += transparency_Ratio
                tot_tratio2 += hazard_cnt

        with open("response.json", 'w', encoding='utf-8') as make_file:
            json.dump(DTO, make_file, ensure_ascii=False)
       