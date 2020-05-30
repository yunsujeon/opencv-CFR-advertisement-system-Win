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
import screeninfo
import speech_recognition as sr
import pygame
import pyautogui

try:
    import Image
except ImportError:
    from PIL import Image

screen_id = 0

# excel 받아오기
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
print(width)
print(height)
pygame.init()  # 라이브러리 초기화 안해줘도 되긴함


def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("say something!")
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def selectname(randnumb, response2):
    print("랜덤한 숫자 : "), randnumb
    print("실제로 음성 인식한 내용 : "), response2
    correct = 2

    if (randnumb == 0):
        print("걸렸네1")
        if response2 in ('navigation', 'vacation', 'delegation', 'randiation', 'navigate', 'Asian', 'dedication', 'definition', 'litigation', 'baby Asian', 'reggaeton', 'meditation', 'vision', 'Nick Cannon'):
            correct = 1
            print("걸렸네2")
        else:
            correct = 2
            print("걸렸네3")
    elif (randnumb == 1):
        if response2 in ('happy birthday', 'birthday', 'divorcee', 'North Bay', 'Thursday', 'PRCA', 'Weber State'):
            correct = 1
            print("걸렸네4")
        else:
            correct = 2
            print("걸렸네5")
    elif (randnumb == 2):
        if response2 in ('English', 'ego-C', 'ngozi', 'Melissa', 'NBC', 'Embassy', 'Blissey', 'Khaleesi', 'Chrissy', "English C", 'sushi', 'Gracie'):
            correct = 1
            print("걸렸네6")
        else:
            correct = 2
            print("걸렸네7")
    elif (randnumb == 3):
        if response2 in ('Museum', 'medium', 'idiom', 'wake me up at', 'video', 'continuum', 'rhenium', 'resume', 'iridium', 'lithium', 'potassium'):
            correct = 1
            print("걸렸네8")
        else:
            correct = 2
            print("걸렸네9")
    elif (randnumb == 4):
        if response2 in ('Coca-Cola', 'Aquila', 'koala', 'popular', 'Opera', 'kookaburra', 'Pablo', 'Buffalo'):
            correct = 1
            print("걸렸네10")
        else:
            correct = 2
            print("걸렸네11")
    elif (randnumb == 5):
        if response2 in ('Hawaii', 'hi', 'how are you'):
            correct = 1
            print("걸렸네12")
        else:
            correct = 2
            print("걸렸네13")

    else:
        print("please say again")
    return correct


def facerecog(faceposes, agelens, firstages, facegenders):
    cell = None
    start = 0
    end = 0
    iagelens = int(agelens)
    ifirstages = int(firstages)
    if faceposes == '100' or agelens == '100' or firstages == '100' or facegenders == '100':
        print("recognize face error")
        faceposenum = 2
    elif faceposes == "frontal_face" or "left_face" or "right_face" or "rotate_face":
        faceposenum = 1
        if iagelens is 5:
            if ifirstages is 1:
                if facegenders == ("male" or "child"):  # 남자10대
                    selectnum = 22
                    start = 3
                    end = 27
                elif facegenders == ("female" or "child"):  # 여자10대
                    selectnum = 22
                    start = 36
                    end = 62
            elif ifirstages is 2:
                if facegenders == ("male" or "child"):  # 남자 20대
                    selectnum = 23
                    start = 3
                    end = 27
                elif facegenders == "female":  # 여자20대
                    selectnum = 23
                    start = 3
                    end = 62
            elif ifirstages is 3:
                if facegenders == ("male" or "child"):  # 남자30대
                    selectnum = 24
                    start = 3
                    end = 27
                elif facegenders == "female":  # 여자30대
                    selectnum = 24
                    start = 3
                    end = 62
            elif ifirstages is 4:
                if facegenders == "male":  # 남자 40대
                    selectnum = 25
                    start = 3
                    end = 27
                elif facegenders == "female":  # 여자 40대
                    selectnum = 25
                    start = 3
                    end = 62
            elif ifirstages is 5:
                if facegenders == "male":  # 남자 50대
                    selectnum = 26
                    start = 3
                    end = 27
                elif facegenders == "female":  # 여자 50대
                    selectnum = 26
                    start = 3
                    end = 62
            elif ifirstages is 6:
                if facegenders == "male":  # 남자 60대
                    selectnum = 27
                    start = 3
                    end = 27
                elif facegenders == "female":  # 여자 60대
                    selectnum = 27
                    start = 3
                    end = 62
            elif 6 < ifirstages < 10:
                if facegenders == "male":  # 남자 70대이상
                    selectnum = 28
                    start = 3
                    end = 27
                elif facegenders == "female":  # 여자 70대이상
                    selectnum = 28
                    start = 3
                    end = 62
        if iagelens < 5:
            if -1 < ifirstages < 10:
                if facegenders == ("male" or "child"):  # 남자 0대
                    selectnum = 21
                    start = 3
                    end = 27
                elif facegenders == ("female" or "child"):  # 여자 0대
                    selectnum = 21
                    start = 3
                    end = 62
    else:
        faceposenum = 2

    while cell is None:
        if faceposenum == 1:
            print(start)
            print(end)
            if start <= end:
                manrownum = random.randrange(start, end)
            else:
                manrownum = random.randrange(end, start)
            print(manrownum, selectnum)
            cell = sheet.cell(row=manrownum, column=selectnum).value
            err = 0
        else:
            cell = None
            err = 1
            break
    print (cell,err)
    return cell, err


while True:
    if framenum == 3:
        framenum = 0
    else:
        framenum = framenum + 1

    randnumb = random.randrange(0,6)
    if randnumb == 0:
        randname = 'navigation'
    elif randnumb ==1:
        randname = 'happybirthday'
    elif randnumb ==2:
        randname = 'english'
    elif randnumb ==3:
        randname = 'museum'
    elif randnumb ==4:
        randname = 'cocacola'
    elif randnumb ==5:
        randname = 'hawaii'

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
                                                 minSize=(50, 50))  # 가까이있는 얼굴 인식하고싶어서 150으로 올려둠 멀리있는 얼굴 인식하려면 낮추기

            if len(face_list) > 0:  # face가 없을때도 코드가 돌아야 되는데... 뒤에 else 문 채워주기
                print(face_list)
                color = [(0, 0, 255), (0, 255, 0)]
                for face in face_list:
                    x, y, w, h = face
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), color[0], thickness=3) #n번째가 아닌 인식되는 즉시 즉시를 보려면 이 코드 사용
                # cv2.imshow('video', frame)

                if framenum == 3:  # 처음 얼굴을 인식했을 때 말고 시간이 약간 지난 후의 x 번째 프레임을 캡쳐한다.
                    cv2.rectangle(ori, (x, y), (x + w, y + h), color[0], thickness=3)
                    cv2.imshow('video', ori)

                    #crop = ori[y + 5:y + h - 5, x + 5:x + w - 5]  # 크롭이미지로 이미지 판별 빨간 줄은 저장하지않도록 선의 굵기만큼 빼고 더한다.
                    #imgpath = ('C:/Users/dbstn/Desktop/nene/cropimg%d.jpg' % (imgnum))

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
                        facepose = '100'
                        firstage = '100'
                        facegender = '100'
                        agelen = '100'
                        print(response.text)
                        data = json.loads(
                            response.text)  # https://developers.naver.com/docs/clova/api/CFR/API_Guide.md#%EC%9D%91%EB%8B%B5-2

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
                        print (facepose, agelen, firstage, facegender)

                        cel, err = facerecog(facepose, agelen, firstage, facegender)
                        if err == 0:
                            print(cel)
                            cel = cel[:-4]
                            clip1 = VideoFileClip('C:/Users/dbstn/Desktop/ad_new/' + cel + '1' + '.mp4')
                            clip2 = VideoFileClip('C:/Users/dbstn/Desktop/ad_new/' + cel + '2' + '.mp4')
                            clip1_resized = clip1.resize(height=height, width=width)
                            clip2_resized = clip1.resize(height=height, width=width)
                            # pygame.display.set_caption('first video!')
                            clip1_resized.preview()  # 작은화면 디버깅시 이용
                            # clip1.preview(fullscreen=True) # 모든화면에서 풀스크린으로 되면 하기 but 팅기더라
                            pygame.quit()
                            print('A')

                            #p = subprocess.Popen('python imviewer.py')
                            width, height = pyautogui.size()
                            image = cv2.imread(
                                'C:/Users/dbstn/Desktop/' + randname + '.jpg')
                            # cv2.imshow('image',image)
                            # cv2.waitKey(1)
                            print("발음해야 할 단어 : " + randname)
                            window_name = 'projector'
                            cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
                            cv2.moveWindow(window_name, width, height)
                            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                            cv2.imshow(window_name, image)
                            cv2.waitKey(100)

                            while True:
                                recognizer = sr.Recognizer()
                                microphone = sr.Microphone(device_index=1)

                                response = recognize_speech_from_mic(recognizer, microphone)
                                response2 = response['transcription']
                                correct = selectname(randnumb, response2)
                                print(response)
                                print(response2)
                                print(correct)
                                print("발음해야 할 단어 : " + randname)
                                if correct == 1:
                                    print (response2, " >> 변환인식완료 >> ", randname)
                                    # p.kill()
                                    break
                                else:
                                    print (response2, " >> 다시 시도해주세요" )
                            print("빠져나옴")
                            cv2.destroyAllWindows()

                            # pygame.display.set_caption('second video!')
                            clip2_resized.preview()  # 작은화면 디버깅시 이용
                            # clip2.preview(fullscreen=True)
                            pygame.quit()
                            # clip2.close() # clip1.close 등 moviepy 명령어인 close 쓰니깐 느림. 팅기는 현상
                        else:
                            print("facepose error")
                    else:
                        print("Error Code:" + rescode)
            else:
                print("no face list")
cap.release()
cv2.destroyAllWindows()

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
