#영상 넣는 코드
import requests
import json
headers = {
        "Content-Type" : "application/json"
        }
temp = {
        "tag" : "운동",
        "movie" : "https://www.youtube.com/watch?v=V3vr9TcOsMM",
        "title" : "제목",
        "date" : "날짜",
        "desc" : "부가적인 내용"
        }

datas = json.dumps(temp)
url = "http://hiroshilin.iptime.org:20000/post_healing_data"
response = requests.post(url, headers=headers, data = datas)
