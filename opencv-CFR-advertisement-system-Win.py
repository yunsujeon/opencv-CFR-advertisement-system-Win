# NAVER clova face recognition CFR
# 결과를 엑셀 또는 서버에 저장하도록 하기
# 영상처리를 먼저 해서 얼굴이 걸리면 CFR을 실행하도록 하기

import requests
import cv2
import json
import numpy as np

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


# 영상은 클라우드에 / 조건과 이에따른 영상제목은 엑셀,office에 / 코드상 조건이 맞으면 엑셀,office 가서 랜덤으로 영상제목을 읽어온다 / 클라우드 접속하여 그 영상을 불러온다.
# 얼굴인식 코드를 지나 CFR을 했을 때 얼굴이 err 이나 frontal img 이외의 이미지일때는 다시 얼굴인식 코드를 하게끔 수정

def facerecog(faceposes, agelens, firstages, facegenders):
    iagelens = int(agelens)
    ifirstages = int(firstages)
    if faceposes == "frontal_face":
        if iagelens is 5:
            if ifirstages is 1:
                if facegenders == "male":
                    fin = "남자 10대입니다."
                elif facegenders == "female":
                    fin = "여자 10대입니다."
            elif ifirstages is 2:
                if facegenders == "male":
                    fin = "남자 20대입니다."
                elif facegenders == "female":
                    fin = "여자 20대입니다."
            elif ifirstages is 3:
                if facegenders == "male":
                    fin = "남자 30대입니다."
                elif facegenders == "female":
                    fin = "여자 30대입니다."
            elif ifirstages is 4:
                if facegenders == "male":
                    fin = "남자 40대입니다."
                elif facegenders == "female":
                    fin = "여자 40대입니다."
            elif ifirstages is 5:
                if facegenders == "male":
                    fin = "남자 50대입니다."
                elif facegenders == "female":
                    fin = "여자 50대입니다."
            elif 5 < ifirstages < 10:
                if facegenders == "male":
                    fin = "남자 60대~90대입니다."
                elif facegenders == "female":
                    fin = "여자 60대~90대입니다."
        if iagelens < 5:
            if -1 < ifirstages < 10:
                if facegenders == "male":
                    fin = "남자 0대입니다."
                elif facegenders == "female":
                    fin = "여자 0대입니다."
        return print(fin)


while True:
    if framenum == 3:
        framenum = 0
    else:
        framenum = framenum + 1
    ret, frame = cap.read()

    if ret:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        else:
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cascade_file = "C:/opencv-4.2.0/haarcascade_frontalface_default.xml "  # https://github.com/opencv/opencv/tree/master/data/haarcascades xml파일 다운경로
            cascade = cv2.CascadeClassifier(cascade_file)
            face_list = cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=3,
                                                 minSize=(150, 150))  # 가까이있는 얼굴 인식하고싶어서 150으로 올려둠

            # vid = cv2.VideoCapture('C:/Users/dbstn/Desktop/ad/2015oronaminc.mp4')  # 재생할 동영상파일
            # while (vid.isOpened()):
            #     ret2, frame2 = vid.read()
            #     cv2.imshow('frame2', frame2)
            #     if cv2.waitKey(1) & 0xFF == 27:
            #         break

            if len(face_list) > 0:  # face가 없을때도 코드가 돌아야 되는데...
                print(face_list)
                color = [(0, 0, 255), (0, 255, 0)]
                for face in face_list:
                    x, y, w, h = face
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), color[0], thickness=3) #n번째가 아닌 인식되는 즉시 즉시를 보려면 이 코드 사용
                # cv2.imshow('video', frame)

                if framenum == 3:  # 처음 얼굴을 인식했을 때 말고 시간이 약간 지난 후의 x 번째 프레임을 캡쳐한다.
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color[0], thickness=3)
                    cv2.imshow('video', frame)
                    crop = frame[y + 3:y + h - 3, x + 3:x + w - 3]
                    imgpath = ('C:/Users/dbstn/Desktop/nene/cropimg%d.jpg' % (imgnum))
                    imgnum = imgnum + 1
                    cv2.imwrite(imgpath, crop)
                    files = {'image': open(imgpath, 'rb')}
                    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
                    response = requests.post(url, files=files, headers=headers)
                    rescode = response.status_code

                    cv2.namedWindow('ad', cv2.WINDOW_NORMAL)  # cv2.WINDOW_AUTOSIZE도 사용가능
                    vid = cv2.VideoCapture('C:/Users/dbstn/Desktop/ad/2015oronaminc.mp4') # 재생할 동영상파일
                    while True:
                        rev = vid.read()
                        if rev == False: #동영상을 끝까지 재생하면 무하루프에서 빠져나온다.
                            break
                    vid.release # 자원 메모리 해제
                    cv2.destroyWindow('ad')

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

# 얼굴인식시 square 를 crop 하게 되는데 CFR 에서는 크롭이미지 말고 그외의 것도 판단하나 봄 나이 측정 등의 성능이 떨어짐
# 6번문제. 여기서 문제점 : harsscade에서 얼굴을 인식했는데 그 crop 이미지를 불러왔을때 CFR이 보기에 분석이 불가능하다면 팅김 > 다시 앞으로 돌아가는 알고리즘 필요

                        facerecog(facepose, agelen, firstage, facegender)

                    else:
                        print("Error Code:" + rescode)

cap.release()

cv2.destroyAllWindows()

# import cv2
#
# vid = cv2.VideoCapture('C:/Users/dbstn/Desktop/ad/2015oronaminc.mp4') # 재생할 동영상파일
#
# while(vid.isOpened()):
#     ret2,frame2 = vid.read()
#     cv2.imshow('frame2',frame2)
#     if cv2.waitKey(1) & 0xFF ==27:
#         break
# vid.release()
# cv2.destroyAllWindows()