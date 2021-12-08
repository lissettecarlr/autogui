用于自动化控制键盘和鼠标
[官方文档](https://pyautogui.readthedocs.io/en/latest/)
[github](https://github.com/asweigart/pyautogui)

# 安装
```
pip install pyautogui
```
list查看当前版本是PyAutoGUI        0.9.50

# API
* 获取鼠标位置，鼠标位置由左上角为0点，向右下增加
```
pyautogui.position()
```
* 获取屏幕尺寸
```
pyautogui.size()
```
* 如果所给XY在屏幕内则返回Tuer
```
pyautogui.onScreen(x, y)
```

* 为了防止代码错误导致无法操作，有两个安全防护措施，其一是增加操作的间隔时间，其二是将鼠标移动到左上角将退出
```
pyautogui.PAUSE = 2.5
pyautogui.FAILSAFE = True
```

* 鼠标在num_seconds秒内移动到X,Y点上
```
 pyautogui.moveTo(x, y, duration=num_seconds)
```
* 相对于当前位置移动鼠标
```
pyautogui.moveRel(xOffset, yOffset, duration=num_seconds)
```

* 鼠标点击操作
其中button可以等于'left', 'middle', 'right'
```
pyautogui.click(x=moveToX, y=moveToY, clicks=num_of_clicks, interval=secs_between_clicks, button='left')
//其他相关
pyautogui.rightClick(x=moveToX, y=moveToY)
pyautogui.middleClick(x=moveToX, y=moveToY)
pyautogui.doubleClick(x=moveToX, y=moveToY)
pyautogui.tripleClick(x=moveToX, y=moveToY)
```

* 鼠标滚轮
Positive向上滚动，negative向下滚动
```
pyautogui.scroll(amount_to_scroll, x=moveToX, y=moveToY)
```

* 鼠标按压或者弹起
```
pyautogui.mouseDown(x=moveToX, y=moveToY, button='left')
pyautogui.mouseUp(x=moveToX, y=moveToY, button='left')
```

* 键盘输入文本
```
pyautogui.typewrite('Hello world!\n', interval=secs_between_keys) 
```

* 键盘组合键
```
pyautogui.hotkey('ctrl', 'c')
pyautogui.hotkey('ctrl', 'v')
```

* 键盘单独按压和弹起
```
pyautogui.keyDown(key_name)
pyautogui.keyUp(key_name)
```
以下是按键值可填写的参数
```
['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']
```

* 弹出消息框
```
pyautogui.alert('This displays some text with an OK button.')
pyautogui.confirm('This displays text and has an OK and Cancel button.')
pyautogui.prompt('This lets the user type in a string and press OK.')
```

* 获取图片位置，得到中心坐标
```
pos=pyautogui.locateOnScreen('help.png')
xy=pyautogui.center(pos)
```
* 直接获取图片坐标
```
pyautogui.locateCenterOnScreen('help.png')
```

* 获取屏幕上所以符合的位置
```
list(pyautogui.locateAllOnScreen('help.png'))
```