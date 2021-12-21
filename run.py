# 该文件用于脚本的执行和停止

import pyautogui
import time
import threading
import json
from loguru import logger
import configparser

#由于录制按键值和操作接口的参数存在差异，所以需要个对照表
keyDict={
'0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9',
'A':'a', 'B':'b', 'C':'c', 'D':'d', 'E':'e', 'F':'f', 'G':'g', 'H':'h', 'I':'i', 'J':'j', 'K':'k', 'L':'l', 'M':'m', 
'N':'n', 'O':'o', 'P':'p', 'Q':'q', 'R':'r', 'S':'s', 'T':'t', 'U':'u', 'V':'v', 'W':'w', 'X':'x', 'Y':'y', 'Z':'z',
'Oem_3':'`', 'Tab':'tab', 'Capital':'capslock', 'Lshift':'shiftleft', 'Lcontrol':'ctrlleft', 'Oem_Minus':'-', 'Oem_Plus':'=', 'Back':'backspace', 
'Oem_4':'[', 'Oem_6':']', 'Oem_5':'\\', 'Oem_1':';', 'Oem_7':"'", 'Return':'enter', 'Oem_Comma':',', 'Oem_Period':'.',
'Oem_2':'/', 'Rshift':'shiftright', 'Up':'up', 'Down':'down', 'Left':'left', 'Right':'right', 'Prior':'pageup', 'Next':'pagedown', 
'Lmenu':'altleft', 'Rmenu':'altright', 'Rcontrol':'ctrlright', 'Escape':'esc', 'F1':'f1', 'F2':'f2', 'F3':'f3', 'F4':'f4', 'F5':'f5',
'F6':'f6', 'F7':'f7', 'F8':'f8', 'F9':'f9', 'F10':'f10', 'F11':'f11', 'F12':'f12', 'Home':'home', 'End':'end', 'Insert':'insert',
'Delete':'delete',
'Lwin':'winleft','Rwin':'winright','Space':'space'
}

class Runner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.flag= False # 标志运行(T)和停止(F)
        self.count = 1  # 执行次数
        self.closeFlag = True # 退出标志位，退出(F)
        self.scriptsPath = "" # 脚本地址
        self.nowCmdLog="" # 当前执行的命令
        self.status = ""
        try:
            #  实例化configParser对象
            config = configparser.ConfigParser()
            # -read读取ini文件
            config.read('config.ini')
            self.pifConfidence = config.getfloat('runCfg', 'Confidence')
        except:
            logger.error("read config error")
            self.pifConfidence = 0.7

    def run(self):
        logger.info('run')
        while 1:
            if(self.flag):
                #如果一开始次数为0则表示无线循环
                if(self.count == 0): 
                    self.runScripts()
                else:
                    nowCount = self.count
                    while(nowCount>0):
                        logger.info("count: "+ str(self.count))
                        self.runScripts()
                        nowCount=nowCount-1
                        if(self.flag == False):#如果在运行中切换为关闭
                            nowCount =0
                    #执行完毕,恢复默认
                    self.flag=False    
                    self.status = "执行完成"
                    logger.info("scripts over")
            else:
                time.sleep(1)
                pass
            if(self.closeFlag == False):
                break
        logger.info('end')

    
    #设置循环次数
    def setCount(self,count):
        if(self.flag == False):
            self.count = count
        else:
            logger.error("running，set fail")

    #设置脚本地址
    def setScritpsPath(self,path):
        self.scriptsPath = path

    def go(self):
        self.flag = True

    def suspend(self):
        self.flag = False

    def close(self):
        self.closeFlag = False

    def getNowCmdLog(self):
        return self.nowCmdLog

    def getFlag(self):
        return self.flag

    def getStatus(self):
        #return self.flag
        return self.status

    #def get

    #开始执行脚本
    def runScripts(self):
        lines=[]
        content = ''
        logger.info(self.scriptsPath)
        try:
            lines = open(self.scriptsPath, 'r', encoding='utf8').readlines()
        except Exception as e:
            logger.error("open fail1"+e)
            self.status = "脚本打开失败，尝试切换编码方式"
            try:
                lines = open(self.scriptsPath, 'r', encoding='gbk').readlines()
            except Exception as e:
                logger.error("open fail2"+e)
                self.status = "脚本打开失败，停止执行"
                return True

        #print(lines)
        self.status = "脚本开始执行"
        for line in lines:
            # 去注释
            if '//' in line:
                index = line.find('//')
                line = line[:index]
                # 去空字符
            line = line.strip()
            content += line
        content = content.replace('],\n]', ']\n]').replace('],]', ']]')
        # logger.info(content)
        s = json.loads(content)
        steps = len(s)
        #执行脚本中的每一行
        for i in range(steps):
            if(self.closeFlag == False or self.flag == False): #如果中途退出，则不在执行脚本了
                logger.info("scripts exit")
                return True

            self.nowCmdLog = s[i]
            logger.info(self.nowCmdLog)
            
            #执行该行命令的延时
            delay = s[i][0]
            #是键盘还是鼠标
            taskType =s[i][1]
            #特别的状态
            sta = s[i][2]
            msg = s[i][3]
            #print("debug : msg = "+msg)
            time.sleep(delay / 1000.0)
            # 休眠前后都添加个退出
            if(self.closeFlag == False or self.flag == False): #如果中途退出，则不在执行脚本了
                logger.info("scripts exit")
                return True
            try:
                if(taskType == "mouse"):
                    x,y = msg
                    if(sta == "left down"):
                        #pyautogui.click(x,y,1,1,'left') #X,Y，点击次数，次数间隔，方式
                        pyautogui.mouseDown(x, y, 'left')
                    elif(sta == "right down"):
                        pyautogui.mouseDown(x, y, 'right')
                    elif(sta == "left up"):
                        pyautogui.mouseUp(x, y, 'left')
                    elif(sta == "right up"):
                        pyautogui.mouseUp(x, y, 'right')
                    elif(sta == "move"):
                        pyautogui.moveTo(x, y)
                    else:
                        logger.error("mouse sta error!")
                        self.status = "当前语句执行错误，状态未知"

                elif(taskType == "keyboard"):
                    if(sta == "down"):
                        #pyautogui.keyDown(msg)
                        pyautogui.keyDown(keyDict[msg])
                    elif(sta == "up"):
                        pyautogui.keyUp(keyDict[msg])
                    elif(sta == "txt"):
                        pyautogui.typewrite(msg)  
                elif(taskType == "pic"):
                    #logger.debug(msg)
                    picPos=pyautogui.locateCenterOnScreen(msg,confidence=self.pifConfidence)
                    if(picPos == None):
                        logger.error("not find pic : " + msg)
                        continue
                    if(sta == "left click"):
                        pyautogui.click(picPos.x,picPos.y,button='left') 
                    elif(sta == "right click"):
                        pyautogui.click(picPos.x,picPos.y,button='night')
                    elif(sta == "left D click"):
                        pyautogui.doubleClick(picPos.x,picPos.y)
                    else:
                        logger.error("script error:sta")
                        self.status = "当前语句执行错误，状态未知"             
                else:
                    logger.error("script error:taskType")
                    self.status = "当前语句执行错误，类型未知"
            except:
                self.suspend()
                self.status = "当前语句执行错误，已停止"
                logger.error("script error")
                

