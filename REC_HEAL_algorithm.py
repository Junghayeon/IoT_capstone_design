import requests
import json
import random

tags = ["기타", "요리", "바둑", "미술", "운동", "영화", "건강", "교양", "상담"]
res_tags = ["초기값", "초기값", "초기값"]

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

# 흥미도가 가장 높은 TOP1과 TOP2로 res_tags의 0번째와 1번째 인덱스에 대입
for i in range(2):
    res_tags[i] = DB_tags[i][1]
print(res_tags)

# 돌림판 섹터와 해당 섹터의 가중치를 정의하기 (DB_tags를 기반으로)
wheel = [(sector, weight) for weight, sector in DB_tags]
# 돌림판 섹터에 TOP1과 TOP2는 제외
wheel = wheel[2:]

# 가중치를 기반으로 선택할 수 있는 섹터 목록 생성
choices = [sector for sector, weight in wheel for _ in range(weight)]

# 돌림판을 돌리기
spin_result = random.choice(choices)
print(f"돌림판이 멈춘 섹터: {spin_result}")

# res_tags의 2번째 인덱스에 돌림판 결과값 대입
res_tags[2] = spin_result

# 최종 res_tags 결과값
print(res_tags)