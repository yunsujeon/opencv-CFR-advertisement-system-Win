# NAVER clova face recognition CFR
# 결과를 엑셀 또는 서버에 저장하도록 하기
# 영상처리를 먼저 해서 얼굴이 걸리면 CFR을 실행하도록 하기

import requests
import cv2
import json

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

# 인식되면 소리도 나게끔
# 영상은 클라우드에 / 조건과 이에따른 영상제목은 엑셀,office에 / 코드상 조건이 맞으면 엑셀,office 가서 랜덤으로 영상제목을 읽어온다 / 클라우드 접속하여 그 영상을 불러온다.
# 얼굴인식 코드를 지나 CFR을 했을 때 얼굴이 err 이나 frontal img 이외의 이미지일때는 다시 얼굴인식 코드를 하게끔 수정

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
                        print("감지된 얼굴의 성별은 {}입니다.".format(facegender))
                        print("감지된 얼굴의 나이는 {}입니다.".format(faceage))
                        print("감지된 얼굴의 감정은 {}입니다.".format(faceemo))
                        print("감지된 얼굴의 방향은 {}입니다.".format(facepose))
                        print("나이 문자열의 총길이는 {}입니다.".format(agelen))
                        print("감지된 얼굴의 첫번째 나이대는 {}0대 입니다.".format(firstage))
                        print("감지된 얼굴의 두번째 나이대는 {}0대 입니다.".format(secondage))

                        # 여기서부터 조건문 들어가서 광고 실행시켜야됨. 무슨 조건 걸건지, 에러시 break 해서 어디로 돌아갈건지 코드짜기
                        # 한 명일때 여러 명 일때 동작이 다르게 하는 것도 여기서부터 갈라져야됨
                        # 예외처리를 다 해주지 않은 상태이다.
                        # 더 세분화 할 필요가 있다. 20~20 대와 20~30대는 다르다. 나이대는 5씩잘린다.
                        if agelen is 5:
                            print("a")

                        if facepose == "frontal_face":
                            if agelen is 5:
                                if firstage is 1:
                                    if facegender == "male":
                                        print("남자 10대입니다.")
                                    elif facegender == "female":
                                        print("여자 10대입니다.")
                                elif firstage is 2:
                                    if facegender == "male":
                                        print("남자 20대입니다.")
                                    elif facegender == "female":
                                        print("여자 20대입니다.")
                                elif firstage is 3:
                                    if facegender == "male":
                                        print("남자 30대입니다.")
                                    elif facegender == "female":
                                        print("여자 30대입니다.")
                                elif firstage is 4:
                                    if facegender == "male":
                                        print("남자 40대입니다.")
                                    elif facegender == "female":
                                        print("여자 40대입니다.")
                                elif firstage is 5:
                                    if facegender == "male":
                                        print("남자 50대입니다.")
                                    elif facegender == "female":
                                        print("여자 50대입니다.")
                                elif (firstage >= 6) and (firstage <= 9):
                                    if facegender == "male":
                                        print("남자 60대~90대입니다.")
                                    elif facegender == "female":
                                        print("여자 60대~90대입니다.")
                            if agelen <= 4:
                                if (firstage >= 0) and (firstage <= 9):
                                    if facegender == "male":
                                        print("남자 0대입니다.")
                                    elif facegender == "female":
                                        print("여자 0대입니다.")

                            # 성별 : 남자
                            # 나이대 : 유아 / 고등학생이하 / 대학생이하 / 사회초년생 / 30대 / 40대(유아) / 50대(청소년) / 60대 / 70대이상
                            # 성별 : 여자
                            # 나이대 : 유아 / 고등학생이하 / 대학생이하 / 사회초년생 / 30대 / 40대(유아) / 50대(청소년) / 60대 / 70대이상
                    else:
                        print("Error Code:" + rescode)

cap.release()

cv2.destroyAllWindows()