
import sys
import pyWinhook
import pythoncom

import win32api
import run
import wincore

mainHander = ""

class autogui():
    def __init__(self):
       self.runnerThread=""
       self.nowMousePosition=""
       self.hm = pyWinhook.HookManager()
       self.hm.KeyAll = self.onKeyboardEvent
       self.hm.HookKeyboard()
       # 监听鼠标 
       # hm.MouseAll = self.onMouseEvent   
       # hm.HookMouse()
       # pythoncom.PumpMessages()

    def onKeyboardEvent(self,event):
        print(event.Key)  # 返回按下的键
        if(event.Key == "F9"):
            print("start!")
            mainHander.runnerThread.go()
        elif(event.Key == "F10"):
            print("stop!")
            mainHander.runnerThread.close()
            mainHander.listenStop()
        elif(event.Key == "F8"):
            print(mainHander.nowMousePosition)
        return True

    def runnerInit(self,scriptPath,count):
        self.runnerThread = run.Runner()
        self.runnerThread.start()
        self.runnerThread.setScritpsPath(scriptPath)
        self.runnerThread.setCount(int(count))
    
    def listenStart(self):
        pythoncom.PumpMessages()
    def listenStop(self):
        win32api.PostQuitMessage()

    # 监听到鼠标事件调用
    def onMouseEvent(self,event):
        #if(event.MessageName=="mouse move"):
            #print(event.MessageName)
            # mainHander.nowMousePosition = event.Position
            # print(event.Position)
        return True


           
if __name__=='__main__':
    print(sys.argv)
    #命令方式执行脚本
    if len(sys.argv) == 3:
        scriptPath = sys.argv[1]
        count = sys.argv[2]
        mainHander = autogui()
        mainHander.runnerInit(scriptPath,count)
        mainHander.listenStart()
    #启动窗体    
    elif(len(sys.argv) == 1):
        wincore.windowsOpen(sys)
    else:
        print("input error "+ str(len(sys.argv)))
       


