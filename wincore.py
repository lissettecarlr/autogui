from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,QRegExp
from PyQt5.QtGui import QRegExpValidator
from winshell import Ui_MainWindow
import run
from loguru import logger
import os
# import sys
import pyWinhook
# import pythoncom
import time
import json
import configparser
import threading

class wincore (QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(wincore,self).__init__()
        self.setupUi(self)
        self.init()
        
    def readConfig(self):
        try:
            logger.info("read config.....")
            config = configparser.ConfigParser()
            config.read('config.ini')
            self.mouseCmdInterval = config.getint('winCfg', 'mouseCmdInterval')
            self.shortcutKeys={'start':config.get('winCfg', 'startKey'),'stop':config.get('winCfg', 'stopKey'),'capture':config.get('winCfg', 'captureKey'),"stopRecord":config.get('winCfg', 'stopRecordKey')}
            # 需要修改UI
        except:
            logger.error("read config error")
            self.mouseCmdInterval = 200
            self.shortcutKeys={'start':'F9','stop':'F10','capture':'F8',"stopRecord":'F7'}

        logger.info(self.shortcutKeys['start']+" "+self.shortcutKeys['stop'])
        logger.info(self.shortcutKeys['capture']+" "+self.shortcutKeys['stopRecord'])
        

    def init(self):
        self.nowMousePos = ""
        self.Captureflag = False #实时抓取鼠标位置标志位
        self.eventTagTime = 0    #保存上一次鼠标或者键盘事件时间
        self.creatScripts = False #是否开始录制标志位
        self.record = []  #缓存录制脚本
        self.shortcutKeys={} #保存快捷键
        self.lastStatusBarMsg = ""
        self.readConfig()

        self.setWindowTitle('自动化工具')
        self.statusBar=QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('这是一个鼠标键盘自动化执行工具',5000)   
        #根据快捷键显示UI
        self.pushButton.setText("开始("+self.shortcutKeys['start'].replace("\"","")+")")
        self.pushButton_2.setText("停止("+self.shortcutKeys['stop'].replace("\"","")+")")
        self.pushButton_6.setText("停止("+self.shortcutKeys['stopRecord'].replace("\"","")+")")
        self.label_6.setText(self.shortcutKeys['capture'].replace("\"","")+"单次抓取")

        if(os.path.exists('./scripts') ==False):#如果没有这个而文件夹
            os.mkdir("scripts")
            logger.debug("not find scripts,mkdir it")

        for file in os.listdir("./scripts"):
            logger.debug(file)
            if(file.endswith(".txt")):#只加载txt文件
                self.comboBox.addItem("./scripts/"+file)
    
        # 限制输入正整数
        reg = QRegExp("^[0-9]*[1-9][0-9]*$")
        LE1Validator = QRegExpValidator(self)
        LE1Validator.setRegExp(reg)
        self.lineEdit.setValidator(LE1Validator)

        # 绑定按键
        self.pushButton.clicked.connect(self.buttonStart)
        self.pushButton_2.clicked.connect(self.buttonStop)
        self.pushButton_3.clicked.connect(self.buttonCapture)
        self.pushButton_4.clicked.connect(self.buttonCaptureStop)
        self.pushButton_5.clicked.connect(self.buttonRecord)
        self.pushButton_6.clicked.connect(self.buttonRecordStop)
        #菜单事件
        self.creatExample.triggered.connect(self.creatExampleScripts)
        self.openCfg.triggered.connect(self.openConfig)
        self.setCfg.triggered.connect(self.reloadConfig)

        # 实例脚本执行器
        self.runnerThread = run.Runner()
        self.runnerThread.start()

        #默认值
        self.setCycleCount("1")

        #状态更新定时器
        # 定时器
        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.statusUpdate)
    
        #开启监听
        hm = pyWinhook.HookManager()
        #键盘
        hm.KeyAll = self.onKeyboardEvent
        hm.HookKeyboard()
        # 监听鼠标 
        hm.MouseAll = self.onMouseEvent   
        hm.HookMouse()

    def reloadScriptsList(self):
        for file in os.listdir("./scripts"):
            if(file.endswith(".txt")):#只加载txt文件
                self.comboBox.addItem("./scripts/"+file)

    def setCycleCount(self,count):
        self.lineEdit.setText(count)
    def getCycleCount(self):
        return self.lineEdit.text()
    def setMousePos(self,pos):
        self.lineEdit_2.setText(pos)
    def getScriptsPath(self):
        return self.comboBox.currentText()

    def buttonStart(self):
        if(self.runnerThread.getFlag() == True):
            self.statusBar.showMessage('已经在运行，勿重复点击',3000)
            return True       
        self.showMinimized()# 最小状态
        #self.statusBar.showMessage('scripts start',3000)   
        self.runnerThread.setScritpsPath(self.getScriptsPath())
        self.runnerThread.setCount(int(self.getCycleCount()))
        self.runnerThread.go()
        self.timer.start(100)

    def buttonStop(self):
        self.activateWindow() #恢复状态
        self.runnerThread.suspend()
        self.timer.stop()
        self.statusBar.showMessage('已手动停止脚本',3000)  

    def buttonCapture(self):
        self.Captureflag = True
        self.statusBar.showMessage('开始抓取',3000)   

    def buttonCaptureStop(self):
        self.Captureflag = False
        self.statusBar.showMessage('停止抓取',3000)   

    def buttonRecord(self):
        self.creatScripts = True
        self.pushButton_5.setEnabled(False)
        #最小化
        self.showMinimized()
        self.statusBar.showMessage('开始录制脚本',3000)   

    def buttonRecordStop(self):
        self.statusBar.showMessage('停止录制',3000)  
        if(not self.record):#如果啥也没录到则直接退出
            return True
        # 根据输入文字建立新的脚本
        name = self.lineEdit_3.text()
        if(name == ""):
            self.statusBar.showMessage('脚本未命名，使用默认名称',3000) 
            name = "newScripts"
        path = "./scripts/"+name+".txt"

        output = json.dumps(self.record, indent=1)
        output = output.replace('\r\n', '\n').replace('\r', '\n')
        output = output.replace('\n   ', '').replace('\n  ', '')
        output = output.replace('\n ]', ']')
        open(path,"w").write(output)
        self.record = []
        self.creatScripts = False
        self.pushButton_5.setEnabled(True)
        #录制完刷新一下下拉菜单
        self.comboBox.clear()

        for file in os.listdir("./scripts"):
            if(file.endswith(".txt")):#只加载txt文件
                self.comboBox.addItem("./scripts/"+file)

    def closeEvent(self,event):
        self.runnerThread.close()
    
    def statusUpdate(self):
        self.label_3.setText( str(self.runnerThread.getNowCmdLog()))
        # 更新消息提示栏
        if(self.runnerThread.getStatus()!="" and self.runnerThread.getStatus()!=self.lastStatusBarMsg):
            self.lastStatusBarMsg = self.runnerThread.getStatus()
            self.statusBar.showMessage(self.lastStatusBarMsg,3000)

    def getNowTime(self):
        return int(time.time() * 1000)
    # 监听键盘事件
    def onKeyboardEvent(self,event):
        #print('MessageName:',event.MessageName)
        if(event.Key == self.shortcutKeys['start'].replace("\"","")):#启动脚本
            logger.info("start!")
            self.showMinimized()
            self.buttonStart()
        elif(event.Key == self.shortcutKeys['stop'].replace("\"","")):#停止脚本
            self.showNormal()
            self.activateWindow()
            self.buttonStop()
            logger.info("stop!")
        elif(event.Key == self.shortcutKeys['capture'].replace("\"","")):#抓取鼠标位置
            self.setMousePos(self.nowMousePos)
        elif(event.Key ==self.shortcutKeys['stopRecord'].replace("\"","")):#停止录制
            self.showNormal()
            self.activateWindow()
            self.buttonRecordStop()
        else: # 排除快捷键                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            if(self.creatScripts):
                if(not self.record): #如果是新脚本则默认第一个指令前延时5秒
                    delay = 5000
                else:
                    delay = self.getNowTime() - self.eventTagTime
                    # [1000,"keyboard","down","a"],
                self.eventTagTime = self.getNowTime()

                #获取类型
                if(event.MessageName == "key down"):
                    keyType = "down"
                elif(event.MessageName == "key up"): # 妈蛋监听键盘压根儿就没有up
                    keyType = "up"
                else:
                    return #其他类型不处理
                log = "record add: " + str(delay) + " " + keyType + " " + event.Key
                logger.debug(log)
                self.record.append([delay, 'keyboard', keyType, event.Key])               
        return True

    # 监听到鼠标事件调用
    def onMouseEvent(self,event):
        #log = "mouse record add:" + "00" + " " + event.MessageName + " " + str(event.Position)
        #logger.debug(log)
        self.nowMousePos = str(event.Position)
        if(self.Captureflag == True):
            self.setMousePos(str(event.Position))
        if(self.creatScripts):
            if(not self.record): #如果是新脚本则默认第一个指令前延时5秒
                delay = 5000
            else:
                delay = self.getNowTime() - self.eventTagTime
            #这里需要现在鼠标移动的采集率
            if(event.MessageName=="mouse move" and delay<=self.mouseCmdInterval):
                    return True
                
            self.eventTagTime = self.getNowTime()
            log = "mouse record add:" + str(delay) + " " + event.MessageName + " " + str(event.Position)
            logger.debug(log)
            # 修改类型
            if(event.MessageName == "mouse left down"):
                mouseType = "left down"
            elif(event.MessageName == "mouse left up"):
                mouseType = "left up"
            elif(event.MessageName == "mouse move"):
                mouseType = "move"
            elif(event.MessageName == "mouse right down"):
                mouseType = "right down"
            elif(event.MessageName == "mouse right up"):
                mouseType = "right up"
            else:
                return True#其他类型不处理
            #存储
            self.record.append([delay, 'mouse', mouseType, event.Position])
        return True

    def creatExampleScripts(self):
        ex = "[\n [5000,\"keyboard\",\"down\",\"1\"],\n [142,\"keyboard\",\"up\",\"1\"]\n]"
        open("./scripts/example.txt","w").write(ex)
        self.reloadScriptsList()

    def openConfig(self):
        if(os.path.exists('config.ini')):
            thread = threading.Thread(target=openTxt)
            thread.start()
        else:
            logger.info("open config fail,creat")
            cfg = "[runCfg]\nConfidence = 0.7\n\n[winCfg]\nmouseCmdInterval = 200\nstartKey = \"F9\"\nstopKey = \"F10\"\ncaptureKey = \"F8\"\nstopRecordKey = \"F7\""
            open("config.ini","w").write(cfg)
            thread = threading.Thread(target=openTxt)
            thread.start()

    def reloadConfig(self):
        self.readConfig()

def openTxt():
    os.system('config.ini')

def windowsOpen(sys):
    app=QtWidgets.QApplication(sys.argv)
    win=wincore()
    win.show()
    sys.exit(app.exec_())

