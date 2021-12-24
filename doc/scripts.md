### 脚本编写

```
 [3000,"keyboard","down","a"],
```

* 参数1：3000表示按压前将延迟3秒钟

* 参数2:

|参数2的值|说明|
|---|---|
|keyboard|键盘操作|
|mouse|鼠标操作|
|pic|寻找图片的点击操作|
|ifpic|寻找图片的条件语句|

* 参数3：根据上面命令不同此处也不同

如果参数2是按键keyboard:

|参数3的值|说明|
|---|---|
|down|按下|
|up|抬起|
|txt|输入文本|

如果参数2是鼠标mouse:

|参数3的值|说明|
|---|---|
|left down|左按下|
|left up|左抬起|
|right down|右按下|
|right up|右抬起|
|move|单纯移动|

如果参数2是识别图片pic:

|参数3的值|说明|
|---|---|
|left click|左单击|
|right click|右单击|
|left D click|左双击|

如果参数2是识别图片ifpic:

|参数3的值|说明|
|---|---|
|true|存在|
|false|不存在|


* 参数4：如果是按键则其值就为键值或文本，如果是鼠标则值为横坐标，纵坐标，如果是寻找图片，则是其地址


按键示例：

```
 [5000,"keyboard","down","Lwin"],
 [81,"keyboard","up","Lwin"],
```

鼠标示例：
```
 [708,"mouse","move",[1007,546]],
 [202,"mouse","move",[955,587]],
 [205,"mouse","move",[938,611]],
 [207,"mouse","move",[922,636]],
 [203,"mouse","move",[918,641]],
 [156,"mouse","left down",[918,642]],
 [107,"mouse","left up",[918,642]],
```

图片示例：
```
 [3000,"pic","left click","./scripts/tp1.png"]
```

图片判断示例：
```
 [3000,"ifpic","True","./scripts/youdao.png"],
 [100,"keyboard","txt","find it"],
 [3000,"ifpic","False","./scripts/youdao.png"],
 [100,"keyboard","txt","not find"],
 [100,"keyboard","txt","over"]
```

### 按键值


'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
'A':, 'B', 'C', 'D', 'E':, 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
'Oem_3':'`', 'Tab':'tab', 'Capital':'capslock', 'Lshift':'shiftleft', 'Lcontrol':'ctrlleft', 'Oem_Minus':'-', 'Oem_Plus':'=', 'Back':'backspace', 
'Oem_4':'[', 'Oem_6':']', 'Oem_5':'\\', 'Oem_1':';', 'Oem_7':"'", 'Return':'enter', 'Oem_Comma':',', 'Oem_Period':'.',
'Oem_2':'/', 'Rshift':'shiftright', 'Up':'up', 'Down':'down', 'Left':'left', 'Right':'right', 'Prior':'pageup', 'Next':'pagedown', 
'Lmenu':'altleft', 'Rmenu':'altright', 'Rcontrol':'ctrlright', 'Escape':'esc', 'F1':'f1', 'F2':'f2', 'F3':'f3', 'F4':'f4', 'F5':'f5',
'F6':'f6', 'F7':'f7', 'F8':'f8', 'F9':'f9', 'F10':'f10', 'F11':'f11', 'F12':'f12', 'Home':'home', 'End':'end', 'Insert':'insert',
'Delete':'delete',
'Lwin':'winleft','Rwin':'winright','Space':'space'