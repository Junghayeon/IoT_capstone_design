import requests
import json
import random

tags = ["기타", "요리", "바둑", "미술", "운동", "영화", "건강", "교양", "상담"]
res_tags = "사회활동 초기값"

# '영상주소/태그문자열'로 틀어올 영상 리스트 받아오기
def get_inter_tag(tag, cnt):
    video_url = "http://hiroshilin.iptime.org:20000/get_rec_heal/" + tag
    print(video_url)
    response = requests.get(video_url)
    html_text = response.text
    html_text = html_text.replace('[', '')
    html_text = html_text.replace(']', '')
    html_text = html_text.replace('"', '')
    S = html_text.split(',')

db_url = "http://hiroshilin.iptime.org:20000/get_inter_t"
response = requests.get(db_url)
data = response.json()

# id가 2인 목록 추출
target_user = None
for user in data:
    if user["id"] == 2:
        target_user = user
        break

DB_tags = [[target_user[tag], tag] for tag in tags]
# 내림차순으로 태그 정렬
DB_tags.sort(reverse=True)

# id가 2인 태그값을 DB에서 받아오기 (Raw Data)
print(DB_tags)

arr = []
# DB_tags 중에서 가중치가 가장 큰 값을 top에 대입
top = DB_tags[0][0]
arr.append(DB_tags[0][1])

# TOP1 값이 여러 개일 경우 랜덤하게 하나의 태그만 선정
for i in range(1,len(DB_tags)):
    if DB_tags[i][0] == top:
        arr.append(DB_tags[i][1])
    else:
        break
    
res_tags = random.choice(arr)
print(res_tags)