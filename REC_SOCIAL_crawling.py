import requests
import json

custom_header = {
'referer' : "http://seoulnoin.platfarm.co.kr/board/BD17120706248208/list?menu=8&menuitem=30",
'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
}

# 가장 최근 게시글부터 50개 크롤링
data_url = "http://seoulnoin.platfarm.co.kr/board/BD17120706248208/contents?start=0&count=50&showingSimple=true&keyword=&keywordType=title&categoryIdx=&_=1683123288598"

data_req = requests.get(data_url, headers=custom_header)

# db에 들어가는 헤더
db_headers = {
        "Content-Type" : "application/json"
        }

# 태그 분류하는 함수
# 태그 목록은 tags[] 안에 계속 추가 가능
tags = ["기타", "요리", "바둑", "미술", "운동", "영화", "건강", "교양", "상담"]
def tag_sort(title, desc, tags) :
    for i in range(1, len(tags)) :
        if tags[i] in title:
            return tags[i]
        if "헬스" in title or "체력" in title:
            return tags[4]
        
        if "문화행사" in title or "문화체험" in title or "권익배움터" in title or "스페인어" in title or "미디어 강좌" in title:
            return tags[7]
        
    for i in range(1, len(tags)) :
        if tags[i] in desc:
            return tags[i]
    # "기타"로 분류    
    return tags[0]
    

if data_req.status_code == requests.codes.ok :
    print("접속 성공")
    stock_data = json.loads(data_req.text)
    # print(stock_data)
    for rank in stock_data["body"] :
		# 채용 공지사항은 크롤링에 포함하지 않음
        if "[채용" in rank['title'] :
            continue
        if "[입찰" in rank['title'] :
            continue
        if "강사 모집" in rank['title'] :
            continue
        else :
            print(rank['title'], rank['desc'], rank['pubdate'])
            # db에 들어가는 temp 데이터 형식
            temp = {
            "tag" : tag_sort(rank['title'], rank['desc'], tags),
            "act" : "0",
            "title" : rank['title'],
            "date" : rank['pubdate'],
            "desc" : rank['desc']
            }
        # db에 들어가는 덤프 datas
        datas = json.dumps(temp)
        # db_url 수정해야 함
        db_url = "http://hiroshilin.iptime.org:20000/post_social_data"
        response = requests.post(db_url, headers=db_headers, data = datas)
else:
    print("Error!!")