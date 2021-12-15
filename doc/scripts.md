# 脚本说明

```
 [3000,"keyboard","down","a"],
```
* 参数1：3000表示按压前将延迟3秒钟
* 参数2：keyboard/mouse/pic 键盘操作，鼠标操作，寻找图片操作
* 参数3：根据上面命令不同此处也不同
    如果是按键：down/up/txt 按下/抬起/输入文本
    如果是鼠标：left down/left up/right down/right up/move
    如果是图片：left click/right click/left D click 
* 参数4：如果是按键则其值就为键值或文本，如果是鼠标则值为横坐标，纵坐标，如果是图片，则是其地址


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
