from customtkinter import *
from PIL import Image
import tkinter as tk
from tkinter import messagebox
import subprocess
import requests
import json
import threading
import psutil
import time
import os


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

def monitor_and_kill_notepad(stopEvent, procName):
    while not stopEvent.is_set():
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == procName:
                message = f"Killing process: {proc.info}"
                os.kill(proc.info['pid'], 9)
                print(message)
                #show_message(message)
        time.sleep(1)

'''def close_window():
    print("debug2")
    root.destroy()'''

'''def show_message(message):
    global root
    # tkinter 창을 생성하여 메시지를 생성
    root = tk.Tk()
    messagebox.showinfo("Process Monitor", message)
    root.withdraw()  # 윈도우를 화면에 보이게 함
    root.after(1000, root.destroy)  # 1초 후에 윈도우를 닫음
    print("debug")'''

def login():
    # Retrieve login credentials
    email = email_entry.get()
    password = password_entry.get()
    global resData
    resData = None
    data = {'email': email, 'password': password}
    url = 'https://e37b-182-231-229-141.ngrok-free.app/loginCheck'
    print(email, password)
    res = requests.post(url, data=data)
    if res != None:
        value = json.loads(res.text)
        resData = value['class']    # Receive the class value from the server
        print(resData)
        # You're already registered
        if resData != -1:
            status_label.configure(text="Login successful!", text_color="#00FF00")
            stopEvent.set() # Signal to the thread to exit
            message = f'Process({procName}) is alive!'
            #show_message(message)
            #messageThread = threading.Thread(target=show_message, args=(message))
            #messageThread.start()
            #messageThread.join()
            print(message)
            subprocess.run(["python", "cameraTest.py"])  # Run guitest.py using subprocess
    else:
        # User not found
        status_label.configure(text="User not found!", text_color="#FF0000")


CTkButton(master=frame, text="Login", fg_color="#5766F9", hover_color="#E44982", font=("Arial Bold", 12),
          text_color="#ffffff", width=225, command=login).pack(anchor="w", pady=(40, 0), padx=(25, 0))

# 스레드 초기화
procName = 'Notepad.exe'
stopEvent = threading.Event()
monitorThread = threading.Thread(target=monitor_and_kill_notepad, args=(stopEvent, procName))
monitorThread.start()

# mainloop 호출
app.mainloop()
