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

mainHander = ""

class autogui():
    def __init__(self):
       self.runnerThread=""
       self.nowMousePosition=""
       self.init()
    
    def init(self):
        hm = pyWinhook.HookManager()
        #键盘
        hm.KeyDown = onKeyboardEvent
        hm.HookKeyboard()
        # 监听鼠标 
        hm.MouseAll = onMouseEvent   
        hm.HookMouse()
    
    def runnerInit(self,scriptPath,count):
        self.runnerThread = run.Runner()
        self.runnerThread.start()
        self.runnerThread.setScritpsPath(scriptPath)
        self.runnerThread.setCount(int(count))

def onKeyboardEvent(event):
    #print(event.Key)  # 返回按下的键
    if(event.Key == "F9"):
        print("start!")
        mainHander.runnerThread.go()
    elif(event.Key == "F10"):
        print("stop!")
        mainHander.runnerThread.close()
        win32api.PostQuitMessage()
    elif(event.Key == "F8"):
        print(mainHander.nowMousePosition)
    return True

# 监听到鼠标事件调用
def onMouseEvent(event):
    if(event.MessageName=="mouse move"):
        #print(event.MessageName)
        mainHander.nowMousePosition = event.Position
        # print(event.Position)
    return True

def ListenInit():
    hm = pyWinhook.HookManager()
    #键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    # 监听鼠标 
    hm.MouseAll = onMouseEvent   
    hm.HookMouse()


if __name__=='__main__':
    print(sys.argv)
    if len(sys.argv) != 3:
        print("input error "+ str(len(sys.argv)))
    else:
        scriptPath = sys.argv[1]
        count = sys.argv[2]

        # runnerThread = run.Runner()
        # runnerThread.start()
        # runnerThread.setScritpsPath(scriptPath)
        # runnerThread.setCount(int(count))

        mainHander = autogui()
        mainHander.runnerInit(scriptPath,count)

        # ListenInit()
        pythoncom.PumpMessages()

