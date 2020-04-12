# NAVER clova face recognition CFR
# 결과를 엑셀 또는 서버에 저장하도록 하기
# 영상처리를 먼저 해서 얼굴이 걸리면 CFR을 실행하도록 하기

import requests
import cv2
import json
import time
import numpy as np
from moviepy.editor import VideoFileClip
import pygame
from pygame.locals import *

try:
    import Image
except ImportError:
    from PIL import Image

cap = cv2.VideoCapture(0)

client_id = "Nzp_FC__3rbf3tRsbXHR"
client_secret = "eagFGHv7lI"
url = "https://openapi.naver.com/v1/vision/face"  # 얼굴감지
# url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식

framenum = 0
imgnum = 0
pygame.init() #라이브러리 초기화 안해줘도 되긴함

# 영상은 클라우드에 / 조건과 이에따른 영상제목은 엑셀,office에 / 코드상 조건이 맞으면 엑셀,office 가서 랜덤으로 영상제목을 읽어온다 / 클라우드 접속하여 그 영상을 불러온다.
# 얼굴인식 코드를 지나 CFR을 했을 때 얼굴이 err 이나 frontal img 이외의 이미지일때는 다시 얼굴인식 코드를 하게끔 수정

def facerecog(faceposes, agelens, firstages, facegenders):
    iagelens = int(agelens)
    ifirstages = int(firstages)
    if faceposes == "frontal_face":
        if iagelens is 5:
            if ifirstages is 1:
                if facegenders == "male":
                    fin = 110  # 남자 1 여자2 로 구분 나이대는 뒤에 10~ 으로 붙인다. 110은 남자 10대
                elif facegenders == "female":
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
            elif 5 < ifirstages < 10:
                if facegenders == "male":
                    fin = 160  # 60~90대로 우선
                elif facegenders == "female":
                    fin = 260
        if iagelens < 5:
            if -1 < ifirstages < 10:
                if facegenders == "male":
                    fin = 10  # 남자 0대
                elif facegenders == "female":
                    fin = 20
        return fin

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

 # 6번문제. 여기서 문제점 : harsscade에서 얼굴을 인식했는데 그 crop 이미지를 불러왔을때 CFR이 보기에 분석이 불가능하다면 팅김 > 다시 앞으로 돌아가는 알고리즘 필요

                        res = facerecog(facepose, agelen, firstage, facegender)

                        # return 된 fin 에 따라 영상을 재생하는 코드
                        if res is 10:
                            print("a")
                        elif res is 110:
                            print("b")
                        elif res is 120:
                            print("c")
                        elif res is 130:
                            print("d")

                            #여기서 위로 올려도 될만한 문장들은 위로 올리기 = 코드정리하기
                            #아래 cv 로 작성된 영상재생 코드는 소리가 안나는 버전이다.
                            # cv2.namedWindow('ad', cv2.WINDOW_NORMAL)
                            # cv2.setWindowProperty('ad', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                            # vid = cv2.VideoCapture('C:/Users/dbstn/Desktop/ad/2015oronaminc.mp4')  # 재생할 동영상파일
                            # fps = vid.get(cv2.CAP_PROP_FPS)
                            # delay = round(1000 / fps) / 1000  # frame 계산해서 29.7 frame 일 경우 33ms마다 1장 나타나게 했지만 생각보다 딜레이가 더걸림
                            # while True:
                            #     ret2, frame2 = vid.read()
                            #     if ret2:
                            #         cv2.imshow('ad', frame2)
                            #         if cv2.waitKey(1) & 0xFF == 27:
                            #             break
                            #         time.sleep(delay)
                            #     else:
                            #         break
                            # vid.release()
                            # cv2.destroyAllWindows()  # cv2.destroyWindows(vid) 로 했어서 연속재생이 안됐었음

                            #아래 pygame과 moviepy로 작성된 코드는 소리가 나는 코드이다.
                            # screen =  pygame.display.set_mode((720,480), FULLSCREEN|HWSURFACE|DOUBLEBUF) #하드웨어가속, 더블버퍼
                            pygame.display.set_caption('My video!')
                            screen = pygame.display.set_mode((720,480), FULLSCREEN)
                            clip = VideoFileClip('C:/Users/dbstn/Desktop/ad/2015oronaminc.mp4')
                            clip.preview()
                            pygame.quit()

                    # 영상 재생속도 영상의 소리

                    else:
                        print("Error Code:" + rescode)

            # !!!!!!!!!!!!!!중요!!!!!!!!!!!!!!!
            # else: # face list 가 없을 때 예외처리방법 작성 필요

cap.release()

cv2.destroyAllWindows()


# pygame 과 moviepy 로 비디오 재생
# from moviepy.editor import VideoFileClip
# import pygame
#
# pygame.display.set_caption('My video!')
#
# clip = VideoFileClip('C:/Users/dbstn/Desktop/ad/2015oronaminc.mp4')
# clip.preview()
# pygame.quit()





#
# import cv2
# import time
#
# vid = cv2.VideoCapture('C:/Users/dbstn/Desktop/ad/2015oronaminc.mp4') # 재생할 동영상파일
# fps = vid.get(cv2.CAP_PROP_FPS)
# delay = round(1000/fps)/1000 # frame 계산해서 29.7 frame 일 경우 33ms마다 1장 나타나게 했지만 생각보다 딜레이가 더걸림
# while True:
#     ret2, frame2 = vid.read()
#     if ret2:
#         cv2.imshow('ad',frame2)
#         if cv2.waitKey(1) & 0xFF == 27:
#             break
#         time.sleep(delay)
#     else:
#         break
#
# vid.release()
# cv2.destroyAllWindows()
