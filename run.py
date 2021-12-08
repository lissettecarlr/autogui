# 该文件用于脚本的执行和停止

import pyautogui
import time
import threading
import json
import pyautogui

class Runner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.flag= False # 标志运行和停止
        self.count = 1  # 执行次数
        self.closeFlag = True # 退出标志位
        self.scriptsPath = ""

    def run(self):
        print('run')
        while 1:
            if(self.flag):
                #如果一开始次数为0则表示无线循环
                if(self.count == 0): 
                    self.runScripts()
                else:
                    nowCount = self.count
                    while(nowCount>0):
                        print("count: "+ str(self.count))
                        self.runScripts()
                        nowCount=nowCount-1
                        #执行完毕,恢复默认
                        self.flag=False    
            else:
                time.sleep(1)
                pass
            if(self.closeFlag == False):
                break
        print('end')

    
    #设置循环次数
    def setCount(self,count):
        if(self.flag == False):
            self.count = count
        else:
            print("running，set fail")

    #设置脚本地址
    def setScritpsPath(self,path):
        self.scriptsPath = path

    def go(self):
        self.flag = True

    def suspend(self):
        self.flag = False

    def close(self):
        self.closeFlag = False

    #开始执行脚本
    def runScripts(self):
        lines=[]
        content = ''
        print(self.scriptsPath)
        try:
            lines = open(self.scriptsPath, 'r', encoding='utf8').readlines()
        except Exception as e:
            print("open fail1"+e)
            try:
                lines = open(self.scriptsPath, 'r', encoding='gbk').readlines()
            except Exception as e:
                print("open fail2"+e)

        print(lines)

        for line in lines:
            # 去注释
            if '//' in line:
                index = line.find('//')
                line = line[:index]
                # 去空字符
            line = line.strip()
            content += line
        content = content.replace('],\n]', ']\n]').replace('],]', ']]')
        print(content)
        s = json.loads(content)
        steps = len(s)
        #执行脚本中的每一行
        for i in range(steps):
            if(self.closeFlag == False): #如果中途退出，则不在执行脚本了
                return
            print(s[i])
            #执行该行命令的延时
            delay = s[i][0]
            #是键盘还是鼠标
            taskType =s[i][1]
            #特别的状态
            sta = s[i][2]
            msg = s[i][3]
            #print("debug : msg = "+msg)
            time.sleep(delay / 1000.0)

            if(taskType == "mouse"):
                x,y = msg
                if(sta == "left"):
                    pyautogui.click(x,y,1,1,'left') #X,Y，点击次数，次数间隔，方式
                elif(sta == "right"):
                    pyautogui.rightClick(x, y)
                    pass
                elif(sta == "move"):
                     pyautogui.moveTo(x, y)
                else:
                    print("mouse sta error!")

            elif(taskType == "keyboard"):
                if(sta == "down"):
                    pyautogui.keyDown(msg)
                elif(sta == "up"):
                    pyautogui.keyUp(msg)
                elif(sta == "txt"):
                    pyautogui.typewrite(msg)     
            else:
                print("script error:taskType")
                pass

