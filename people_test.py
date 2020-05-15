# import time
# import numpy as np
# import moviepy
# from moviepy.editor import *
# from moviepy.video.fx.resize import resize # 이런식으로 가져오면 시간을 줄일 수 있음
# from pygame.locals import *
import requests
import cv2
import json
import moviepy.editor as mp
from moviepy.editor import VideoFileClip
import subprocess
import speech_recognition as sr
import pygame
import pyautogui
try:
    import Image
except ImportError:
    from PIL import Image

#cap = cv2.VideoCapture(0)

client_id = "Nzp_FC__3rbf3tRsbXHR"
client_secret = "eagFGHv7lI"
url = "https://openapi.naver.com/v1/vision/face"  # 얼굴감지
# url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식

framenum = 0
imgnum = 0
width, height = pyautogui.size()
print (width)
print (height)
pygame.init() #라이브러리 초기화 안해줘도 되긴함

# 영상은 클라우드에서 다운받는다 / 경로는 플레이되는 경로와 일치 / 엑셀에서 랜덤으로 골라서 영상 재생할 수 있게끔.
# 얼굴인식 코드를 지나 CFR을 했을 때 얼굴이 err 이나 frontal img 이외의 이미지일때는 다시 얼굴인식 코드를 하게끔 수정

def recognize_speech_from_mic(recognizer, microphone): #stt함수
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source) # #  analyze the audio source for 1 second
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable/unresponsive"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    return response

def facerecog(faceposes, agelens, firstages, facegenders):
    iagelens = int(agelens)
    ifirstages = int(firstages)
    if faceposes == "frontal_face":
        if iagelens is 5:
            if ifirstages is 1:
                if facegenders == ("male" or "child"):
                    fin = 110  # 남자 1 여자2 로 구분 나이대는 뒤에 10~ 으로 붙인다. 110은 남자 10대
                elif facegenders == ("female" or "child"):
                    fin = 210
            elif ifirstages is 2:
                if facegenders == "male":
                    fin = 120
                elif facegenders == "female":
                    fin = 220
            elif ifirstages is 3:
                if facegenders == "male":
                    fin = 130
                elif facegenders == "female":
                    fin = 230
            elif ifirstages is 4:
                if facegenders == "male":
                    fin = 140
                elif facegenders == "female":
                    fin = 240
            elif ifirstages is 5:
                if facegenders == "male":
                    fin = 150
                elif facegenders == "female":
                    fin = 250
            elif ifirstages is 6:
                if facegenders == "male":
                    fin = 160
                elif facegenders == "female":
                    fin = 260
            elif 6 < ifirstages < 10:
                if facegenders == "male":
                    fin = 170  # 70~90대로 우선
                elif facegenders == "female":
                    fin = 270
        if iagelens < 5:
            if -1 < ifirstages < 10:
                if facegenders == ("male" or "child"):
                    fin = 10  # 남자 0대
                elif facegenders == ("female" or "child"):
                    fin = 20 # 여자 0대
        return fin

while True:
    ori = cv2.imread('C:/Users/dbstn/Desktop/friend2.png')
    ori2 = ori.copy()
    img_gray = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
    cascade_file = "C:/opencv-4.2.0/haarcascade_frontalface_default.xml "  # https://github.com/opencv/opencv/tree/master/data/haarcascades xml파일 다운경로
    cascade = cv2.CascadeClassifier(cascade_file)
    face_list = cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=3,
                                         minSize=(50, 50))  # 가까이있는 얼굴 인식하고싶어서 150으로 올려둠 멀리있는 얼굴 인식하려면 낮추기 #시간이 좀 걸림
    if len(face_list) > 0:  # face가 없을때도 코드가 돌아야 되는데... 뒤에 else 문 채워주기
        print (len(face_list))
        print(face_list)
        color = [(0, 0, 255), (0, 255, 0)]
        for face in face_list:
            x, y, w, h = face
            cv2.rectangle(ori, (x, y), (x + w, y + h), color[0], thickness=3)

        cv2.imshow('video', ori)

        crop = ori2  # crop 이지만 크롭하지 않은 전체 이미지를 저장해서 CFR이 인식하도록 함. 추후 수정필요
        imgpath = ('C:/Users/dbstn/Desktop/nene/multimg%d.png' % (imgnum))
        imgnum = imgnum + 1
        cv2.imwrite(imgpath, crop)
        files = {'image': open(imgpath, 'rb')}

        headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
        response = requests.post(url, files=files, headers=headers) #시간이 좀 걸림
        rescode = response.status_code

        if (rescode == 200):
            print(response.text)
            data = json.loads(response.text)  # https://developers.naver.com/docs/clova/api/CFR/API_Guide.md#%EC%9D%91%EB%8B%B5-2
            countdata = 0
            genderlist = []
            agelist = []
            for i in data['faces']:
                countdata += 1
                facegender = i['gender']['value']  # json data의 객체배열을 python으로 출력하고싶음
                faceage = i['age']['value'] #emotion과 pose 제외
                facepose = i['pose']['value']
                agelen = len(faceage)  # faceage의 총 길이가 5면 최소 10대 이고 3이면 0~9 4이면 6~10 일 수 있다.
                firstage = faceage[0]  # faceage의 총 길이에 따라 나이대를 구분한다.
                #secondage = faceage[3]  # 나이대를 정확히 하기 위한 두번 째 변수이다. #현재는 적용X
                #나이대를 계산해준다.
            res = facerecog(facepose, agelen, firstage, facegender)
                #리스트에 저장해준다???

                #res 마다 값을 비교해줘서 최종적인 값을 갖게한다? -> 문제있음 /  알고리즘 필요하다


cap.release()
cv2.destroyAllWindows()



