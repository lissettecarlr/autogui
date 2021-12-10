# 脚本说明

```
 [3000,"keyboard","down","a"],
```
* 参数1：3000表示按压前将延迟3秒钟
* 参数2：keyboard/mouse 按键或者鼠标命令
* 参数3：根据上面命令不同此处也不同
    如果是按键：down/up/txt 按下/抬起/输入文本
    如果是鼠标：left/right/move 移动后左单击/移动后右单击/单纯移动
* 参数4：如果是按键则其值就为键值或文本，如果是鼠标则值为横坐标，纵坐标。


示例：
```
 [3000,"mouse","left",[1235,43]],  
 [1000,"mouse","move",[387,370]], 
 [1000,"keyboard","down","a"],
 [121,"keyboard","up","a"],
 [263,"keyboard","down","b"],
 [112,"keyboard","up","b"],
 [112,"keyboard","txt","test"],
 [1000,"mouse","right",[387,370]], 
```
