from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,QRegExp,QThread,pyqtSignal
from PyQt5.QtGui import QKeyEvent, QKeySequence,QRegExpValidator
from winshell import Ui_MainWindow
import run
from loguru import logger
import os
import sys
import pyWinhook
import pythoncom
import time
import json

class wincore (QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(wincore,self).__init__()
        self.setupUi(self)
        self.init()
    def init(self):
        self.nowMousePos = ""
        self.Captureflag = False #实时抓取鼠标位置标志位
        self.eventTagTime = 0    #保存上一次鼠标或者键盘事件时间
        self.creatScripts = False #是否开始录制标志位
        self.record = []  #缓存录制脚本

        self.setWindowTitle('自动化工具')
        self.statusBar=QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('>_< >_< >_< >_<',5000)   

        if(os.path.exists('./scripts') ==False):#如果没有这个而文件夹
            os.mkdir("scripts")
            logger.debug("not find scripts,mkdir it")

        for file in os.listdir("./scripts"):
            logger.debug(file)
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
        hm.KeyDown = self.onKeyboardEvent
        hm.HookKeyboard()
        # 监听鼠标 
        hm.MouseAll = self.onMouseEvent   
        hm.HookMouse()

    def setCycleCount(self,count):
        self.lineEdit.setText(count)
    def getCycleCount(self):
        return self.lineEdit.text()
    def setMousePos(self,pos):
        self.lineEdit_2.setText(pos)
    def getScriptsPath(self):
        return self.comboBox.currentText()

    def buttonStart(self):
        self.showMinimized()# 最小状态
        self.statusBar.showMessage('scripts start',3000)   
        self.runnerThread.setScritpsPath(self.getScriptsPath())
        self.runnerThread.setCount(int(self.getCycleCount()))
        self.runnerThread.go()
        self.timer.start(100)

    def buttonStop(self):
        self.activateWindow() #恢复状态
        self.runnerThread.suspend()
        self.statusBar.showMessage('scripts stop',3000)   
    def buttonCapture(self):
        self.Captureflag = True
        self.statusBar.showMessage('Capture start',3000)   
    def buttonCaptureStop(self):
        self.Captureflag = False
        self.statusBar.showMessage('Capture stop',3000)   

    def buttonRecord(self):
        self.creatScripts = True
        self.pushButton_5.setEnabled(False)
        #最小化
        self.showMinimized()
        self.statusBar.showMessage('record start',3000)   


    def buttonRecordStop(self):
        self.statusBar.showMessage('record stop',3000)  
        # 根据输入文字建立新的脚本
        name = self.lineEdit_3.text()
        if(name == ""):
            self.statusBar.showMessage('new scripts name error',3000) 
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
            self.comboBox.addItem("./scripts/"+file)

    def closeEvent(self,event):
        self.runnerThread.close()
    
    def statusUpdate(self):
        self.label_3.setText( str(self.runnerThread.getNowCmdLog()))

    def getNowTime(self):
        return int(time.time() * 1000)
    # 监听键盘事件
    def onKeyboardEvent(self,event):
        if(event.Key == "F9"):#启动脚本
            print("start!")
            self.showMinimized()
            self.buttonStart()
        elif(event.Key == "F10"):#停止脚本
            self.showNormal()
            self.activateWindow()
            self.buttonStop()
            print("stop!")
        elif(event.Key == "F8"):#抓取鼠标位置
            self.setMousePos(self.nowMousePos)
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
        if(event.MessageName=="mouse move"):
            self.nowMousePos = str(event.Position)
            if(self.Captureflag):
                self.setMousePos(self.nowMousePos)
        return True



def windowsOpen(sys):
    app=QtWidgets.QApplication(sys.argv)
    win=wincore()
    win.show()
    sys.exit(app.exec_())

# def onKeyboardEvent(event):
#     #print(event.Key)  # 返回按下的键
#     if(event.Key == "F9"):
#         print("start!")
#         mainHander.runnerThread.go()
#     elif(event.Key == "F10"):
#         print("stop!")
#         mainHander.runnerThread.close()
#         mainHander.listenStop()
#     elif(event.Key == "F8"):
#         print(mainHander.nowMousePosition)
#     return True

# # 监听到鼠标事件调用
# def onMouseEvent(event):
#     if(event.MessageName=="mouse move"):
#         #print(event.MessageName)
#         mainHander.nowMousePosition = event.Position
#         # print(event.Position)
#     return True
