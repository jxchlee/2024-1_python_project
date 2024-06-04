# 5.16 로그인 창 구현
# 로그인 정보를 입력하는 인터페이스. 일단 생각 중인 계획은 로그인을 하게 되면 해당 정보를 DB에서 대조한 이후, 각 정보에 해당하는 class를 불러오는 식으로 구현하는 게 좋을 것 같음.
# 그리고 이미지 비교를 했을 때 클래스가 무엇인지를 확인 후 해당되는 class일 경우 잠금해제하는 식으로 진행할 예정
# 5.27 request 구현. 수요일에 test 예정
# 5.29 서버 요청 후 데이터 정상적으로 받는 것 확인. resData에 해당 값 받음.
# 6.4 pythonProject2 폴더 밑에 kill_notepad 파일 만듬
# 해당 파일을 Login_modify에 작성된 메모장을 닫는 기능만을 뽑아내 함수 형식으로 구현해놓은 파일이다.
# 이 login 파일에서 kill_notepad을 import해서 app.mainloop() 실행 직전에 해당 함수를 실행시켰다.

from customtkinter import *
from PIL import Image
import subprocess
import requests
import json
from lib.pythonProject2.kill_notepad import monitor_thread_start

app = CTk()
app.title('잠금해제')
app.geometry("600x480")
app.resizable(0, 0)

side_img_data = Image.open("../../src/side-.png")
email_icon_data = Image.open("../../src/email-icon.png")
password_icon_data = Image.open("../../src/password-icon.png")

side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="Welcome!", text_color="#5766F9", anchor="w", justify="left",
         font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(master=frame, text="Login with your information", text_color="#7E7E7E", anchor="w", justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Email:", text_color="#5766F9", anchor="w", justify="left",
         font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
email_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#5766F9", border_width=1,
                       text_color="#000000")
email_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Password:", text_color="#5766F9", anchor="w", justify="left",
         font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#5766F9", border_width=1,
                          text_color="#000000", show="*")
password_entry.pack(anchor="w", padx=(25, 0))

status_label = CTkLabel(master=frame, text="", text_color="#FF0000", anchor="w", justify="left",
                        font=("Arial Bold", 12))
status_label.pack(anchor="w", padx=(25, 0))

resData=None
def login():
    # Retrieve login credentials
    email = email_entry.get()
    password = password_entry.get()
    global resData
    resData = None
    data = {'email': email, 'password': password}
    url = 'https://e37b-182-231-229-141.ngrok-free.app/loginCheck'
    res = requests.post(url, data=data)
    if res != None:
        value = json.loads(res.text)
        resData = value['class']    #서버에서 받은 class 값

    if resData != None:
        if resData != -1:
            # Login successful
            status_label.configure(text="Login successful!", text_color="#00FF00")
            app.destroy()
            subprocess.run(["python", "cameraTest.py"])  # Run guitest.py using subprocess
        else:
## User not found
            status_label.configure(text="User not found!", text_color="#FF0000")
    else:
# User not found
        status_label.configure(text="internet error!", text_color="#FF0000")


CTkButton(master=frame, text="Login", fg_color="#5766F9", hover_color="#E44982", font=("Arial Bold", 12),
          text_color="#ffffff", width=225, command=login).pack(anchor="w", pady=(40, 0), padx=(25, 0))

monitor_thread_start()
app.mainloop()
