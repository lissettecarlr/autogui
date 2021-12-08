import os
import io
import sys
import pyautogui
import time
import pyWinhook
import pythoncom
import threading
import win32api
import run

       
global runnerThread

def onKeyboardEvent(event):
    #print(event.Key)  # 返回按下的键
    if(event.Key == "F9"):
        print("start!")
        runnerThread.go()
    elif(event.Key == "F10"):
        print("stop!")
        runnerThread.close()
        win32api.PostQuitMessage()
    return True


if __name__=='__main__':
    print(sys.argv)
    if len(sys.argv) != 3:
        print("input error "+ str(len(sys.argv)))
    else:
        scriptPath = sys.argv[1]
        count = sys.argv[2]

        runnerThread = run.Runner()
        runnerThread.start()
        runnerThread.setScritpsPath(scriptPath)
        runnerThread.setCount(int(count))

        hm = pyWinhook.HookManager()
        hm.KeyDown = onKeyboardEvent
        hm.HookKeyboard()
        pythoncom.PumpMessages()
