
## 安装
```
pip install PyQt5
pip install PyQt5-tools
```

## 使用
使用工具designer.exe，参考地址
```
Python\Python39\Lib\site-packages\qt5_applications\Qt\bin
```
* 建立一个MainWindow，这是一个窗体有菜单状态栏，而Widget只是个页面


## 生成

将软件导出的UI文件转化为py文件
```
pyuic5 -o win.py win.ui
```

## 引入
```
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,QRegExp,QThread,pyqtSignal
from PyQt5.QtGui import QKeyEvent, QKeySequence,QRegExpValidator
from winshell import Ui_MainWindow

class wincore (QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(wincore,self).__init__()
        self.setupUi(self)
        self.init()
    def init(self):
        self.statusBar=QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('>_< >_< >_< >_<',5000)    


def open(sys):
    app=QtWidgets.QApplication(sys.argv)
    win = wincore()
    win.show()
    sys.exit(app.exec_())

```

然后：

```
    #启动窗体    
    elif(len(sys.argv) == 1):
        wincore.open(sys)
```

设置窗体名称
```
self.setWindowTitle('自用的蓝牙工具')
```

## 其他

* 下拉框读取文件地址
```
    for file in os.listdir("./scripts"):
        logger.debug(file)
        self.comboBox.addItem("./scripts/"+file)
```

* 查找文件夹没有就建个
```
    if(os.path.exists('./scripts') ==False):#如果没有这个而文件夹
        os.mkdir("scripts")
        logger.debug("not find scripts,mkdir it")
```

* 定时器
```
        # 定时器
        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.updateComboBox)
        self.timer.start(2 * 1000)
        
    def updateComboBox(self):
        for file in os.listdir("./scripts"):
            logger.debug(file)
            self.comboBox.addItem("./scripts/"+file)   
```

* 限制输入
```
        # 限制输入正整数
        reg = QRegExp("^[0-9]*[1-9][0-9]*$")
        LE1Validator = QRegExpValidator(self)
        LE1Validator.setRegExp(reg)
        self.lineEdit.setValidator(LE1Validator)
```

控制窗体
```
self.showMinimized()# 最小状态
self.showNormal()#正常态
self.activateWindow() #活动态
```