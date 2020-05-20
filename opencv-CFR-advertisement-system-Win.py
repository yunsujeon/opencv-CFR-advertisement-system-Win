# import time
# import numpy as np
# import moviepy
# from moviepy.editor import *
# from moviepy.video.fx.resize import resize # 이런식으로 가져오면 시간을 줄일 수 있음
# from pygame.locals import *
import requests
import cv2
import json
import random
import openpyxl
from moviepy.editor import VideoFileClip
import subprocess
import speech_recognition as sr
import pygame
import pyautogui
try:
    import Image
except ImportError:
    from PIL import Image

#excel 받아오기
excel_document = openpyxl.load_workbook('C:/Users/dbstn/Desktop/data.xlsx')
excel_document.get_sheet_names()
sheet = excel_document.get_sheet_by_name('Sheet1')

cap = cv2.VideoCapture(0)

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
    cell= None
    start=0
    end=0
    iagelens = int(agelens)
    ifirstages = int(firstages)
    if faceposes == "frontal_face":
        if iagelens is 5:
            if ifirstages is 1:
                if facegenders == ("male"or"child"): #남자10대
                    selectnum = 22
                    start = 3
                    end = 27
                elif facegenders == ("female"or"child"): #여자10대
                    selectnum = 22
                    start = 36
                    end = 62
            elif ifirstages is 2:
                if facegenders == "male": #남자 20대
                    selectnum = 23
                    start = 3
                    end = 27
                elif facegenders == "female": #여자20대
                    selectnum = 23
                    start = 3
                    end = 62
            elif ifirstages is 3:
                if facegenders == "male": #남자30대
                    selectnum = 24
                    start = 3
                    end = 27
                elif facegenders == "female": #여자30대
                    selectnum = 24
                    start = 3
                    end = 62
            elif ifirstages is 4:
                if facegenders == "male": #남자 40대
                    selectnum = 25
                    start = 3
                    end = 27
                elif facegenders == "female": #여자 40대
                    selectnum = 25
                    start = 3
                    end = 62
            elif ifirstages is 5:
                if facegenders == "male": #남자 50대
                    selectnum = 26
                    start = 3
                    end = 27
                elif facegenders == "female": #여자 50대
                    selectnum = 26
                    start = 3
                    end = 62
            elif ifirstages is 6:
                if facegenders == "male": #남자 60대
                    selectnum = 27
                    start = 3
                    end = 27
                elif facegenders == "female": #여자 60대
                    selectnum = 27
                    start = 3
                    end = 62
            elif 6 < ifirstages < 10:
                if facegenders == "male": #남자 70대이상
                    selectnum = 28
                    start = 3
                    end = 27
                elif facegenders == "female": #여자 70대이상
                    selectnum = 28
                    start = 3
                    end = 62
        if iagelens < 5:
            if -1 < ifirstages < 10:
                if facegenders == ("male"or"child"): #남자 0대
                    selectnum = 21
                    start = 3
                    end = 27
                elif facegenders == ("female"or"child"): #여자 0대
                    selectnum = 21
                    start = 3
                    end = 62
    while cell is None:
        print (start)
        print (end)
        manrownum = random.randrange(start, end)
        print(manrownum, selectnum)
        cell = sheet.cell(row=manrownum, column=selectnum).value
    return cell

while True:
    if framenum == 2:
        framenum = 0
    else:
        framenum = framenum + 1

    ret, frame = cap.read()

    if ret:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        else:
            ori = frame.copy()  # 나중에 frame 의 원본을 쓰기 위해 ori 에 복사한 것으로 얼굴을 인식시킨다.
            img_gray = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
            cascade_file = "C:/opencv-4.2.0/haarcascade_frontalface_default.xml "  # https://github.com/opencv/opencv/tree/master/data/haarcascades xml파일 다운경로
            cascade = cv2.CascadeClassifier(cascade_file)
            face_list = cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=3,
                                                 minSize=(150, 150))  # 가까이있는 얼굴 인식하고싶어서 150으로 올려둠 멀리있는 얼굴 인식하려면 낮추기

            if len(face_list) > 0:  # face가 없을때도 코드가 돌아야 되는데... 뒤에 else 문 채워주기
                print(face_list)
                color = [(0, 0, 255), (0, 255, 0)]
                for face in face_list:
                    x, y, w, h = face
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), color[0], thickness=3) #n번째가 아닌 인식되는 즉시 즉시를 보려면 이 코드 사용
                # cv2.imshow('video', frame)

                if framenum == 2:  # 처음 얼굴을 인식했을 때 말고 시간이 약간 지난 후의 x 번째 프레임을 캡쳐한다.
                    cv2.rectangle(ori, (x, y), (x + w, y + h), color[0], thickness=3)
                    cv2.imshow('video', ori)

                    # crop = ori[y + 3:y + h - 3, x + 3:x + w - 3] #크롭이미지로 이미지 판별 빨간 줄은 저장하지않도록 선의 굵기만큼 빼고 더한다.
                    # imgpath = ('C:/Users/dbstn/Desktop/nene/cropimg%d.jpg' % (imgnum))

                    crop = frame  # crop 이지만 크롭하지 않은 전체 이미지를 저장해서 CFR이 인식하도록 함. 추후 수정필요
                    imgpath = ('C:/Users/dbstn/Desktop/nene/img%d.png' % (imgnum))
                    imgnum = imgnum + 1
                    cv2.imwrite(imgpath, crop)
                    files = {'image': open(imgpath, 'rb')}
# 파일을 저장하지 않고 바로 쓸수는 없는지 생각해보기 files = frame 으로 하면 안되더라.

                    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
                    response = requests.post(url, files=files, headers=headers)
                    rescode = response.status_code

                    if (rescode == 200):
                        print(response.text)
                        data = json.loads(response.text)  # https://developers.naver.com/docs/clova/api/CFR/API_Guide.md#%EC%9D%91%EB%8B%B5-2
                        for i in data['faces']:
                            facegender = i['gender']['value']  # json data의 객체배열을 python으로 출력하고싶음
                            faceage = i['age']['value']
                            faceemo = i['emotion']['value']
                            facepose = i['pose']['value']
                            agelen = len(faceage)  # faceage의 총 길이가 5면 최소 10대 이고 3이면 0~5 4이면 6~10 일 수 있다.
                            firstage = faceage[0]  # faceage의 총 길이에 따라 나이대를 구분한다.
                            secondage = faceage[3]  # 나이대를 정확히 하기 위한 두번 째 변수이다.
                        # print("감지된 얼굴의 성별은 {}입니다.".format(facegender))
                        # print("감지된 얼굴의 나이는 {}입니다.".format(faceage))
                        # print("감지된 얼굴의 감정은 {}입니다.".format(faceemo))
                        # print("감지된 얼굴의 방향은 {}입니다.".format(facepose))
                        # print("나이 문자열의 총길이는 {}입니다.".format(agelen))
                        # print("감지된 얼굴의 첫번째 나이대는 {}0대 입니다.".format(firstage))
                        # print("감지된 얼굴의 두번째 나이대는 {}0대 입니다.".format(secondage))

 # 6번문제. 여기서 문제점 : harsscade에서 얼굴을 인식했는데 그 crop 이미지를 불러왔을때 CFR이 보기에 분석이 불가능하다면 팅김 > 다시 앞으로 돌아가는 알고리즘 필요

                        cel = facerecog(facepose, agelen, firstage, facegender)
                        print (cel)
                        clip1 = VideoFileClip('C:/Users/dbstn/Desktop/ad/'+cel)
                        clip2 = VideoFileClip('C:/Users/dbstn/Desktop/ad/'+cel)
                        clip1_resized = clip1.resize(height=height, width=width)
                        clip2_resized = clip1.resize(height=height, width=width)
                        #pygame.display.set_caption('first video!')
                        clip1_resized.preview()  # 작은화면 디버깅시 이용
                        # clip1.preview(fullscreen=True) # 모든화면에서 풀스크린으로 되면 하기 but 팅기더라
                        pygame.quit()
                        print ('A')
                        p = subprocess.Popen('python imviewer.py')
                        while True:
                            recognizer = sr.Recognizer()
                            mic = sr.Microphone(device_index=1)
                            response = recognize_speech_from_mic(recognizer, mic)
                            response2 = response['transcription']
                            if response2 == "snow":  # snow 또는 now 또는 none 등등 예외를 많이 만들어놓기!!! 음성인식 정확도 %의 기준이 될것
                                print(response2)
                                p.kill()
                                break
                            else:
                                print(response2)

                        #pygame.display.set_caption('second video!')
                        clip2_resized.preview()  # 작은화면 디버깅시 이용
                        # clip2.preview(fullscreen=True)
                        pygame.quit()
                        # clip2.close() # clip1.close 등 moviepy 명령어인 close 쓰니깐 느림. 팅기는 현상

                    else:
                        print("Error Code:" + rescode)
            # !!!!!!!!!!!!!!중요!!!!!!!!!!!!!!!
            # else: # face list 가 없을 때 예외처리방법 작성 필요
cap.release()
cv2.destroyAllWindows()




#
# # 음성인식 주기를 줄였다.
# def recognize_speech_from_mic(recognizer, microphone):
#     if not isinstance(recognizer, sr.Recognizer):
#         raise TypeError("`recognizer` must be `Recognizer` instance")
#     if not isinstance(microphone, sr.Microphone):
#         raise TypeError("`microphone` must be `Microphone` instance")
#     with microphone as source:
#         recognizer.adjust_for_ambient_noise(source) # #  analyze the audio source for 1 second
#         audio = recognizer.listen(source)
#
#     response = {
#         "success": True,
#         "error": None,
#         "transcription": None
#     }
#     try:
#         response["transcription"] = recognizer.recognize_google(audio)
#     except sr.RequestError:
#         # API was unreachable or unresponsive
#         response["success"] = False
#         response["error"] = "API unavailable/unresponsive"
#     except sr.UnknownValueError:
#         # speech was unintelligible
#         response["error"] = "Unable to recognize speech"
#     return response
#
# # def recognize(audio):
# #     try:
# #         return r.recognize_google(audio,language='en=US')
# #     except sr.UnknownValueError:
# #     # except LookupError:
# #         print("음성이 안들어왔는데요?")
# #         return ''
#
# # pygame 과 moviepy 로 비디오 재생
# from moviepy.editor import VideoFileClip
# import subprocess
# import speech_recognition as sr
# # import moviepy
# import pygame
#
# clip1 = VideoFileClip('C:/Users/dbstn/Desktop/ad/oronaminc.mp4')
# clip2 = VideoFileClip('C:/Users/dbstn/Desktop/ad/adidas.mp4')
# pygame.display.set_caption('first video!')
# # clip1.preview()
# clip1.preview(fullscreen=True)
# pygame.quit()
# p = subprocess.Popen('python imviewer.py')
#
# # r = sr.Recognizer()
# # mic = sr.Microphone()
# # with mic as source:
# #     while True:
# #         print("말하세여")
# #         audio = r.listen(source)
# #         print("들었어요")
# #         sttfinal = recognize(audio)
# #         print("함수에서 반환함")
# #         if sttfinal == "snow":# 조건이 만족되면
# #             p.kill()
# #             break
# #         else:
# #             print (sttfinal)
#
# # while True:
# #     r = sr.Recognizer()
# #     with sr.Microphone() as source:
# #         print("말하세여")
# #         audio=r.listen(source)
# #         print("들었어요")
# #         aed = recognize(audio)
# #         print("함수에서 반환함")
# #         if aed == "snow":
# #             p.kill()
# #             break
# #         else:
# #             print(aed)
#
# while True:
#     recognizer = sr.Recognizer()
#     mic = sr.Microphone(device_index=1)
#     response = recognize_speech_from_mic(recognizer, mic)
#     response2 = response['transcription']
#     if response2 =="snow":
#         print (response2)
#         p.kill()
#         break
#     else:
#         print (response2)
#
# pygame.display.set_caption('second video!')
# # clip2.preview()
# clip2.preview(fullscreen=True)
# pygame.quit()
# # clip2.close() # clip1.close 등 moviepy 명령어인 close 쓰니깐 느림. 팅기는 현상
# # pygame.quit()


# # opencv 로 비디오 재생
# import cv2
# import time
# vid = cv2.VideoCapture('C:/Users/dbstn/Desktop/ad/2015oronaminc.mp4') # 재생할 동영상파일
# fps = vid.get(cv2.CAP_PROP_FPS)
# # 원래 /1000이 맞지만 사양따라 딜레이가 달라서 /1300으로 해줌 가변적임.
# delay = round(1000/fps)/1300 # frame 계산해서 29.7 frame 일 경우 33ms마다 1장 나타나게 했지만 생각보다 딜레이가 더걸림
# while True:
#     ret2, frame2 = vid.read()
#     if ret2:
#         cv2.imshow('ad',frame2)
#         if cv2.waitKey(1) & 0xFF == 27:
#             break
#         time.sleep(delay)
#     else:
#         break
# vid.release()
# cv2.destroyAllWindows()


# #음성인식 google speech_recognition 이용
# import speech_recognition as sr
# r = sr.Recognizer()
# mic = sr.Microphone()
# with mic as source:
#     audio = r.listen(source)
# print(r.recognize_google(audio,language='ko=KR'))


# #pocketsphinx 설치실패.. pip install pocketsphinx 리눅스에서 도전
# import speech_recognition as sr
# from pocketsphinx import pocketsphinx
# from sphinxbase import sphinxbase
# r = sr.Recognizer()
# with sr.Microphone() as source:
#     print("Say something!")
#     audio = r.listen(source)
# try:
#     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
# except sr.UnknownValueError:
#     print("Sphinx could not understand audio")
# except sr.RequestError as e:
#     print("Sphinx error; {0}".format(e))
