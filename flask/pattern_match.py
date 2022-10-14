from konlpy.tag import Okt
import pandas as pd
import re
import os


# 인식양태 기반 테스트
def pattern_matching(sent, hazard_word_list):
    okt = Okt()
    hazard_word_list = list(hazard_word_list)
    word_list = ["보인다", "보였다", "본다", "생각", "예상", "추정", "가능성", "전망", "추측","의견","의혹","주장"]
    flag = False
    flag2 = False
    predict_sen = {"text": sent, "word_index_start": [], "word_index_end": []}
    hazard_sen = {"text": sent, "word_index_start": [], "word_index_end": []}
    # 띄어쓰기 제거
    sentence = re.sub(r"^\s+", "", sent)
    sen_len = len(sent) - len(sentence)

    # 주어진 문장의 단어 단위(띄어쓰기)로 검사
    for word in sentence.split():
        morphs = okt.morphs(word)
        for i in range(0,len(morphs)):
            # 추측성 발언 확인
            # 단어 기반 검사(단일 형태소)
            if morphs[i] in word_list:
                flag = True
                predict_sen["word_index_start"].append(sen_len)
                predict_sen["word_index_end"].append(sen_len + len(word) - 1)
            elif morphs[i] == "것":
                if i == len(morphs) -1:
                    continue
                if morphs[i+1] == "같다":
                    flag = True
                    predict_sen["word_index_start"].append(sen_len)
                    predict_sen["word_index_end"].append(sen_len + len(word) - 1)
            # 자극적 발언 확인
            if morphs[i] in hazard_word_list:
                flag2 = True
                hazard_sen["word_index_start"].append(sen_len)
                hazard_sen["word_index_end"].append(sen_len + len(word) - 1)
        sen_len += len(word) + 1

    return predict_sen, hazard_sen, flag, flag2


def master(article):
    # 추측성 문장
    predict_sentences = []
    # 자극적 표현 문장
    hazard_sentences = []
    target_sentence = 0
    target_sentence2 = 0
    idx = 1
    file_path = os.path.join(os.path.dirname(__file__), '해커톤 어휘 조사.xlsx')
    data_hazard = pd.read_excel(file_path, sheet_name="자극적 표현").loc[:, "자극적 표현"]
    split_document = article.split(".")
    line_index = 0
    for sentence in split_document:
        line_index += 1
        predict_sen, hazard_sen, result, result2 = pattern_matching(sentence, data_hazard)
        if result == True:
            predict_sen["index"] = line_index
            predict_sentences.append(predict_sen)
            target_sentence += result
        if result2 == True:
            hazard_sen["index"] = line_index
            hazard_sentences.append(hazard_sen)
            target_sentence2 += result2
        idx += 1
    hazard_cnt = target_sentence2
    transparency_ratio = target_sentence / len(split_document) * 100
    return transparency_ratio, hazard_cnt, predict_sentences, hazard_sentences
