# autogui

根据脚本实现对应的鼠标键盘操作工具


## 环境

* pyautogui
用来控制鼠标键盘输出，直接pip安装即可
```
pip install pyautogui
```

* pyWinhook
用于监听鼠标键盘的输入，直接按照会报错，需要手动去下载。
下列命令是查看设备支持的版本
```
pip debug --verbose
```
在[pywinhook下载页](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pywinhook)找到自己对应的版本进行下载，然后安装
```
 pip install .\pyWinhook-1.6.2-cp39-cp39-win_amd64.whl
```

## 使用

### 当前版本V2
更新了鼠标移动和点击

#### 写脚本
增加了三种鼠标操作，移动左击，移动右击和单纯移动
```
 [3000,"mouse","left",[1235,43]],  
 [1000,"mouse","move",[387,370]], 
 [1000,"mouse","right",[387,370]], 
```
其中的X,Y坐标可以在打开程序的后，使用F8来获取当前鼠标坐标

#### 启动程序

```
python .\autogui.py .\scripts\test.txt 1
```

#### 快捷键

|键位|功能|
|---|---|
|F8|获取当前鼠标坐标点|
|F9|启动脚本|
|F10|关闭程序|

### 当前版本V1

#### 写脚本
首先编写单次执行脚本，说明可见doc/scripts.md，目前该版本只支持键盘输入
该示例就是按压a和b，然后输入test
```
[
 [3000,"keyboard","down","a"],
 [121,"keyboard","up","a"],
 [263,"keyboard","down","b"],
 [112,"keyboard","up","b"],
 [112,"keyboard","txt","test"],
]
```

#### 启动程序
然后命令启动，需要输入两个参数，第一个是脚本地址，第二个是运行次数，如果为0则无限执行
```
python .\autogui.py .\scripts\test.txt 1
```

#### 启动脚本
键盘按压F9则会按照输入的次数执行脚本，完毕后可以依旧点击F9来再次执行，按压F10则停止并且退出程序
