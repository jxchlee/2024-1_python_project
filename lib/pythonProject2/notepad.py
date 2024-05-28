import tkinter as tk
from tkinter import messagebox
import mysql.connector

# MySQL 데이터베이스 연결 설정
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="0000",
    database="mydatabase"
)

text_widget = None
user_id = None

# 로그인 함수
def login():
    global user_id
    email = email_entry.get()
    password = password_entry.get()

    # MySQL에서 사용자 정보 조회
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, password))
    row = cursor.fetchone()

    if row:
        user_id = row[0]  # 사용자 ID 설정
        messagebox.showinfo("로그인 성공", "로그인에 성공했습니다!")
        open_notepad()
    else:
        messagebox.showerror("로그인 실패", "이메일 또는 비밀번호가 잘못되었습니다!")

def open_notepad():
    global text_widget
    notepad = tk.Toplevel(root)
    notepad.title("Notepad with MySQL")

    text_widget = tk.Text(notepad)
    text_widget.pack()

    # 저장 버튼
    save_button = tk.Button(notepad, text="저장", command=save_to_db)
    save_button.pack()

# 데이터베이스에 저장 함수
def save_to_db():
    global user_id, text_widget
    text = text_widget.get("1.0", "end-1c")
    cursor = db.cursor()
    cursor.execute("INSERT INTO notes (user_id, content) VALUES (%s, %s)", (user_id, text))
    db.commit()
    messagebox.showinfo("저장 완료", "메모가 성공적으로 저장되었습니다!")

# 프로그램 종료 함수
def close_program():
    db.close()  # 데이터베이스 연결 종료
    root.destroy()  # Tkinter 창 닫기

# 로그인 창 생성
root = tk.Tk()
root.title("로그인")

# 이메일 입력
email_label = tk.Label(root, text="이메일:")
email_label.grid(row=0, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=0, column=1)

# 비밀번호 입력
password_label = tk.Label(root, text="비밀번호:")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1)

# 로그인 버튼
login_button = tk.Button(root, text="로그인", command=login)
login_button.grid(row=2, column=0, columnspan=2)

# 종료 버튼
close_button = tk.Button(root, text="종료", command=close_program)
close_button.grid(row=3, column=0, columnspan=2)

root.mainloop()
