import os
import cv2
from datetime import datetime
from machineModel import identify

now = datetime.now().microsecond
print(now)
print(cv2.__version__)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

faceSearch = os.path.abspath('../../model/faceSearch/haarcascade_frontalface_default.xml')
faceDirectory = os.path.abspath('../faceImage/')
print(faceSearch)
face_cascade = cv2.CascadeClassifier(faceSearch)
#eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')

#while cv2.waitKey(33) < 0:
while True:
    ret, frame = capture.read()  # 카메라로부터 현재 영상을 받아 frame에 저장, 잘 받았다면 ret가 참

# scaleFactor를 1에 가깝게 해주면 정확도가 상승하나 시간이 오래걸림
# minNeighbors를 높여주면 검출률이 상승하나 오탐지율도 상승
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=4, minSize=(20, 20))

# 찾은 얼굴이 있으면 얼굴 영역을 영상에 사각형으로 표시
    if len(faces):
        for x, y, w, h in faces:
            print(str(faces))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255,255,255), 2, cv2.LINE_4)
            fileName = str(now)+'.jpg'
            identify(frame)             #class 구분 함수. 해당 함수로 실시간으로 얼굴의 class 값을 구분시켜줌
#            newFile = os.path.join(faceDirectory, fileName)
            #cv2.imwrite(newFile, frame)
        #break

    if cv2.waitKey(1) == ord('q'):  # 키보드의 q 를 누르면 무한루프가 멈춤
            break
    cv2.imshow("face", frame)  # frame(카메라 영상)을 face 이라는 창에 띄워줌

capture.release()
cv2.destroyAllWindows()