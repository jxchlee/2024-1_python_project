import threading
import psutil
import time
import os

def monitor_and_kill_notepad(stopEvent, procName):
    while not stopEvent.is_set():
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == procName:
                message = f"Killing process: {proc.info}"
                os.kill(proc.info['pid'], 9)
                print(message)
                #show_message(message)
        time.sleep(1)


# 스레드 초기화
def monitor_thread_start():
    procName = 'Notepad.exe'
    stopEvent = threading.Event()
    monitorThread = threading.Thread(target=monitor_and_kill_notepad, args=(stopEvent, procName))
    monitorThread.start()
    return stopEvent

