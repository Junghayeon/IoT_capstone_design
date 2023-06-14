import cv2
import json
import numpy as np
import tensorflow as tf
import pygame
import random
import math
import yt_dlp
import requests
import os
import time
import threading
import re
from pyvidplayer import Video

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model=tf.keras.models.load_model("2_try.h5")
score=0
total_score=0
video_score=0
total_video_score=0
name = "박원서"
tags = ["기타", "요리", "바둑", "미술", "운동", "영화", "건강", "교양", "상담"]
res_tags = "사회활동 초기값"

def remove_extensions(filename):
    extensions = ['.mp4', '.part']
    for ext in extensions:
        if filename.endswith(ext):
            filename = filename[:-len(ext)]
    return filename

def remove_files():
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    for file in files:
        if os.path.isfile(file):
            filename = remove_extensions(file)
            if filename != file:
                os.remove(file)

def recommand_social(name):
    def get_inter_tag(tag, cnt):
        video_url = "http://hiroshilin.iptime.org:20000/get_rec_heal/" + tag
        response = requests.get(video_url)
        html_text = response.text
        html_text = html_text.replace('[', '')
        html_text = html_text.replace(']', '')
        html_text = html_text.replace('"', '')
        S = html_text.split(',')
    db_url = "http://hiroshilin.iptime.org:20000/get_interest_user/" + name
    response = requests.get(db_url)
    data = response.json()
    DB_tags = [[data[index], tag] for index, tag in enumerate(tags)]
    # 내림차순으로 태그 정렬
    DB_tags.sort(reverse=True)
    # id가 2인 태그값을 DB에서 받아오기 (Raw Data)
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
    return res_tags

def recommand_movie(name):
    res_tags = ["init", "init", "init"]
    # '영상주소/태그문자열'로 틀어올 영상 리스트 받아오기
    def get_inter_tag(tag, cnt):
        video_url = "http://hiroshilin.iptime.org:20000/get_rec_heal/" + tag
        response = requests.get(video_url)
        html_text = response.text
        html_text = html_text.replace('[', '')
        html_text = html_text.replace(']', '')
        html_text = html_text.replace('"', '')
        S = html_text.split(',')
    db_url = "http://hiroshilin.iptime.org:20000/get_interest_user/" + name
    response = requests.get(db_url)
    data = response.json()
    DB_tags = [[data[index], tag] for index, tag in enumerate(tags)]
    # 내림차순으로 태그 정렬
    DB_tags.sort(reverse=True)
    # id가 2인 태그값을 DB에서 받아오기 (Raw Data)
    # 흥미도가 가장 높은 TOP1과 TOP2로 res_tags의 0번째와 1번째 인덱스에 대입
    for i in range(2):
        res_tags[i] = DB_tags[i][1]
    # 돌림판 섹터와 해당 섹터의 가중치를 정의하기 (DB_tags를 기반으로)
    wheel = [(sector, weight) for weight, sector in DB_tags]
    # 돌림판 섹터에 TOP1과 TOP2는 제외
    wheel = wheel[2:]
    # 가중치를 기반으로 선택할 수 있는 섹터 목록 생성
    choices = [sector for sector, weight in wheel for _ in range(weight)]
    # 돌림판을 돌리기
    spin_result = random.choice(choices)
    # res_tags의 2번째 인덱스에 돌림판 결과값 대입
    res_tags[2] = spin_result
    # 최종 res_tags 결과값
    return res_tags



def get_movie_from_tag(movie):
    movie = movie.split("/")[-1]
    url = "http://hiroshilin.iptime.org:20000/get_rec_heal_tag/" + movie
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return "오류"

def check_viewed(user_id, video_link):
    headers = {
        "Content-Type" : "application/json"
    }
    temp = {
        "user_id" : user_id,
        "video_id" : video_link
    }
    datas = json.dumps(temp)
    url = "http://hiroshilin.iptime.org:20000/add_user_viewed_video"
    response = requests.post(url, headers=headers, data = datas)
    return response

def update_inter_table(name, tag_dict):
	headers = {
		"Content-Type" : "application/json"
	}
	datas = json.dumps(tag_dict)
	url = "http://hiroshilin.iptime.org:20000/update_inter_t/" + name
	response = requests.post(url, headers=headers, data = datas)
	if response.status_code == 200:
		return True
	else:
		return False

def get_social_act(tag):
    response = requests.get('http://hiroshilin.iptime.org:20000/get_social_tag/' + tag)
    social_acts = response.json()
    return random.choice(social_acts)


def repeat(model):
	global score
	while True:
		temp=modeltest(model)
		score=score+temp
		print("score:",score,"temp:",temp)
		time.sleep(10)
def modeltest(model):
	img=cv2.imread("test2.jpg")
	img=(img[:,:,0]+img[:,:,1]+img[:,:,2])/3
	img=img.reshape(50,50,1)
	img=img.astype(np.float32)
	test_itm=img.reshape(1,50,50,1)/255.0
	y_pred=model.predict(test_itm)
	if y_pred>0.5:
		return 1
	else:
		return 0

def clean_title(title):
	pattern = r'[^\w\s]'
	return re.sub(pattern, '', title)

def download_videos(yt_link, vid_list, index):
	ydl_opts = {'format' : 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]',
            'outtmpl' : index+".mp4",
            'extract_info' : True}
	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		info_dict = ydl.extract_info(yt_link, download=False)
		title = info_dict.get('title', None)
		ydl.download(yt_link)
		vid_list.append(index + ".mp4")
		return index + ".mp4"
def show_popup(text, yes_callback=None, no_callback=None):
	font = pygame.font.Font("NanumSquare.ttf", 30)
	text_surface = font.render(text, True, (255, 255, 255))
	popup_width = text_surface.get_width() + 20
	popup_height = text_surface.get_height() + 80
	popup = pygame.Surface((popup_width, popup_height))
	popup.fill((0, 0, 0))
	popup.blit(text_surface, (10, 20))
	yes_btn = pygame.Rect(20, popup_height-60, 120, 40)
	no_btn = pygame.Rect(popup_width - yes_btn.width - 140 - 20, popup_height - 60, 120, 40)
	pygame.draw.rect(popup, (50, 50, 255), yes_btn)
	pygame.draw.rect(popup, (255, 50, 50), no_btn)
	yes_font = pygame.font.Font("NanumSquare.ttf", 24)
	yes_text = yes_font.render("네", True, (255, 255, 255))
	yes_btn_center = yes_btn.center
	yes_text_center = yes_text.get_rect(center=yes_btn_center)
	popup.blit(yes_text, yes_text_center)
	no_font = pygame.font.Font("NanumSquare.ttf", 24)
	no_text = no_font.render("아니오", True, (255, 255, 255))
	no_btn_center = no_btn.center
	no_text_center = no_text.get_rect(center=no_btn_center)
	popup.blit(no_text, no_text_center)
	popup_x = (800 - popup_width) // 2
	popup_y = (480 - popup_height) // 2
	win.blit(popup, (popup_x, popup_y))
	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif event.type == pygame.MOUSEBUTTONUP:
				x, y = event.pos
				if yes_btn.collidepoint(x - popup_x, y - popup_y):
					return 1
				elif no_btn.collidepoint(x - popup_x, y - popup_y):
					return 0

def video_play(vid_link, movie):
	tag = get_movie_from_tag(movie)[0]
	global total_score
	black_screen = pygame.Surface((800, 480))
	black_screen.fill((0, 0, 0))
	vid = Video(vid_link)
	vid.set_size((800, 480))
	x=0
	y=0
	while True:
		key=None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				vid.close()
				pygame.quit()
				exit()
			elif event.type == pygame.MOUSEBUTTONUP:
				x, y = event.pos
			elif event.type == pygame.KEYDOWN:
				key = pygame.key.name(event.key)
		popup_clicked = False
		clock.tick(60)
		if x < 266 and y > 160 and y < 320:
			vid.seek(-15)
		elif x > 532 and y > 160 and y < 320:
			vid.seek(15)
		elif x > 266 and x < 532:
			popup_clicked = not popup_clicked
		if(popup_clicked == True):
			vid.pause()
			while popup_clicked:
				for event in pygame.event.get():
					if(event.type == pygame.MOUSEBUTTONUP):
						vid.resume()
						popup_clicked = not popup_clicked
						break
					clock.tick(60)
			else:
				popup_clicked = not popup_clicked
				vid.resume()
		else:
			vid.resume()
		x=0
		y=0
		if(int(vid.duration) == int(vid.get_pos())):
			total_score=int(vid.duration)/10
			return

		vid.draw(win, (0, 0), force_draw=False)
		pygame.display.update()

def download_process(movie_links, vid_list):
	for movie_link in movie_links:
		vid_file = download_videos(movie_link)
		vid_list.append(vid_file)
def score_calc(x,max_score):
	interest_ratio=x/max_score
	x=(interest_ratio*9)+1
	temp=1/(1+math.exp(-(x-5)))
	return (temp*9)+1

pygame.init()
pygame.font.init()
pygame.font.Font()
win=pygame.display.set_mode((800,480),pygame.FULLSCREEN)
#win=pygame.display.set_mode((800,480))
clock=pygame.time.Clock()
remove_files()
initial_playlist=[]
movies=[]
initial_score=[]
for initial_tag in tags:
    response=requests.get('http://hiroshilin.iptime.org:20000/get_rec_heal/'+initial_tag)
    movies_origin=response.json()
    for movie in movies_origin:
        if check_viewed(name, movie).status_code == 200:
            movies.append(movie)
            break
    #initial_playlist.append(movie[0])

t2=threading.Thread(target=repeat, args=(model,))
t2.daemon=True
t2.start()
print(movies)
for index, movie in enumerate(movies):
    score=0
    total_score=0
    print("index: ",index)
    if(index==0):
        vid=download_videos(movie, initial_playlist,str(index))
    elif(index==len(movies)-1):
        video_play(initial_playlist[index],movie)
        os.remove(initial_playlist[index])
        tag = recommand_social(name)
        black_screen = pygame.Surface((800, 480))
        black_screen.fill((0, 0, 0))
        res = show_popup(get_social_act(tag))
        if(res == 1):
            win.blit(black_screen, (0, 0))
            pygame.display.update()
            black_screen_bool = True
            while black_screen_bool:
                 for event in pygame.event.get():
                     if(event.type == pygame.MOUSEBUTTONUP):
                         black_screen_bool = not black_screen_bool
                         break
                     clock.tick(60)
        break
    t = threading.Thread(target=download_videos, args=(movies[index + 1], initial_playlist, str(index+1)))
    t.start()
    print("----------inital_list------------------")
    print(initial_playlist)
    video_play(initial_playlist[index], movie)
    t.join()
    print("final score:",score)
    video_score+=score
    total_video_score+=total_score
    score_result=int(score_calc(video_score, total_video_score))
    tag_dict={get_movie_from_tag(movie)[0] : score_result}
    update_inter_table(name,tag_dict)
    os.remove(initial_playlist[index])
video_score=0
total_video_score=0

while(1):
    remove_files()
    prefer_tags=recommand_movie(name)
    play_list=[]
    movies=[]
    for i in prefer_tags:
        response=requests.get('http://hiroshilin.iptime.org:20000/get_rec_heal/'+i)
        movies_origin=response.json()
        for movie in movies_origin:
            if check_viewed(name,movie).status_code==200:
                movies.append(movie)
        #play_list.append(movies_origin[0],movies_origin[1])
        #태그당 동영상 2개씩 -> 총 6개 재생
        try:
            for index, movie in enumerate(movies):
                score=0
                total_score=0
                if(index==0):
                    vid=download_videos(movie,play_list,str(index))
                elif(index==len(movies)-1):
                    video_play(play_list[index], movie)
                    os.remove(play_list[index])
                    break
                t = threading.Thread(target=download_videos, args=(movies[index + 1], play_list, str(index+1)))
                t.start()
                video_play(play_list[index], movie)
                score_result=int(score_calc(score,total_score))
                tag_dict={get_movie_from_tag(movie)[0] : score_result}
                update_inter_table(name,tag_dict)
                os.remove(play_list[index])
        except IndexError as e:
            continue
t2.join()
