import json

def response(raw_len):
    with open('./response.json','rt',encoding='UTF-8') as f:
        json_data = json.load(f)

    #span 넣을 단어 위치
    span_input = []

    #span 넣을 문장 위치
    index_cnt = []

    #태그 넣을 문장 순서 입력
    data_len = len(json_data.get('predcitive_Reporting'))
    for i in range(data_len):
        index_cnt.append(json_data.get('predcitive_Reporting')[i].get('index') - 1)
    #태그 위치 입력
    cnt = 0
    for i in range(raw_len):
        if i in index_cnt:
            span_input.append([json_data.get('predcitive_Reporting')[cnt].get('word_index_start')[0]-1,
                               json_data.get('predcitive_Reporting')[cnt].get('word_index_end')[0]])
            cnt += 1
        else:
            span_input.append([0,0])
    
    #비교 데이터 확인
    transparency_Ratio = json_data.get("transparency_Ratio")
    Other_transparency_Ratio = json_data.get("Other_transparency_Ratio")
    Other_title_list = json_data.get("Other_title_list")
    
    
    #같은 방법으로 자극적 표현 확인
    h_span_input = []
    h_index_cnt= []
    h_data_len = len(json_data.get('provocative_Reporting'))
    for i in range(h_data_len):
        h_index_cnt.append(json_data.get('provocative_Reporting')[i].get('index') - 1)
    
    h_cnt = 0
    for i in range(raw_len):
        if i in h_index_cnt:
            h_span_input.append([json_data.get('provocative_Reporting')[h_cnt].get('word_index_start')[0]-1,
                                json_data.get('provocative_Reporting')[h_cnt].get('word_index_end')[0]])
            h_cnt += 1
        else:
            h_span_input.append([0,0])
    

    hazard_Ratio = json_data.get('hazard_Ratio')
    Other_hazard_Ratio = json_data.get('Other_hazard_Ratio')


    return span_input, index_cnt, transparency_Ratio, Other_transparency_Ratio, Other_title_list,h_span_input,h_index_cnt, hazard_Ratio, Other_hazard_Ratio
