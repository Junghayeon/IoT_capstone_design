
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model=tf.keras.models.load_model("2_try.h5")
score=0
total_score=0
video_score=0
total_video_score=0

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

def score_calc(x,max_score):
	interest_ratio=x/max_score #인식된 표정개수 대비 좋아요한 표정 개수의 비율
	x=(interest_ratio*9)+1 #해당 값을 1~10점 범위의 값으로 나타냄
	temp=1/(1+math.exp(-(x-5)))#sigmoid 통과
	return (temp*9)+1

t2=threading.Thread(target=repeat, args=(model,))
t2.daemon=True
t2.start()

#main code
score_result=score_calc(video_score, total_video_score)
#video_score = 영상에서 나타난 사용자의 긍정표정 횟수(태그 내에서 재생되는 모든 동영상 합산)
#total_video_score = 영상에서 인식된 얼굴데이터 개수(태그 내에서 재생되는 모든 동영상 합산)

t2.join()
