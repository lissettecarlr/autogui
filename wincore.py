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

class wincore (QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(wincore,self).__init__()
        self.setupUi(self)
        self.init()
    def init(self):
        self.nowMousePos = ""
        self.Captureflag = False #实时抓取鼠标位置标志位

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
        
        # 实例脚本执行器
        self.runnerThread = run.Runner()
        self.runnerThread.start()

        #默认值
        self.setCycleCount("1")

        #状态更新定时器
        # 定时器
        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.statusUpdate)
        self.timer.start(100)
        
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
        self.statusBar.showMessage('scripts start',3000)   
        self.runnerThread.setScritpsPath(self.getScriptsPath())
        self.runnerThread.setCount(int(self.getCycleCount()))
        self.runnerThread.go()

    def buttonStop(self):
        self.runnerThread.suspend()
        self.statusBar.showMessage('scripts stop',3000)   
    def buttonCapture(self):
        self.Captureflag = True
        self.statusBar.showMessage('Capture start',3000)   
    def buttonCaptureStop(self):
        self.Captureflag = False
        self.statusBar.showMessage('Capture stop',3000)   

    def closeEvent(self,event):
        self.runnerThread.close()
    
    def statusUpdate(self):
        self.label_3.setText( str(self.runnerThread.getNowCmdLog()))

    # 监听键盘事件
    def onKeyboardEvent(self,event):
        if(event.Key == "F9"):#启动脚本
            print("start!")
            self.buttonStart()
        elif(event.Key == "F10"):#停止脚本
            self.buttonStop()
            print("stop!")
        elif(event.Key == "F8"):#抓取鼠标位置
            self.setMousePos(self.nowMousePos)
            pass
        return True

    # 监听到鼠标事件调用
    def onMouseEvent(self,event):
        if(event.MessageName=="mouse move"):
            self.nowMousePos = str(event.Position)
            if(self.Captureflag):
                self.setMousePos(self.nowMousePos)
        return True


def open(sys):
    app=QtWidgets.QApplication(sys.argv)
    win = wincore()
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
