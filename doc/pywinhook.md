
## 监听鼠标和键盘事件

```
import pyHook
import pythoncom
 
# 监听到鼠标事件调用
def onMouseEvent(event):
    if (event.MessageName != "mouse move"):  # 因为鼠标一动就会有很多mouse move，所以把这个过滤下
        print(event.MessageName)
    return True  # 为True才会正常调用，如果为False的话，此次事件被拦截
 
# 监听到键盘事件调用
def onKeyboardEvent(event):
    print(event.Key)  # 返回按下的键
    return True
 
def main():
    # 创建管理器
    hm = pyHook.HookManager()
    # 监听键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    # 监听鼠标
    # hm.MouseAll = onMouseEvent
    # hm.HookMouse()
    # 循环监听
    pythoncom.PumpMessages()
 
if __name__ == "__main__":
    main()

```

## 关闭pythoncom.PumpMessages()
```
    import win32api
    win32api.PostQuitMessage()
```
## 鼠标事件

|变量|说明|
|---|---|
|event.MessageName|事件名称|
|event.Message|windows消息常量|
|event.Time|事件发生的时间戳|
|event.Window|窗口句柄|
|event.WindowName|窗口标题|
|event.Position|事件发生时相对于整个屏幕的坐标|
|event.Wheel|鼠标滚轮|
|event.Injected|判断这个事件是否由程序方式生成，而不是正常的人为触发。|

## 键盘事件

|变量|说明|
|---|---|
|event.MessageName|消息名称|
|event.Time|事件发生的时间戳|
|event.Window|窗口句柄|
|event.WindowName|窗口标题|
|event.Ascii, chr(event.Ascii)|按键的ASCII码|
|event.Key|按键的名称|
|event.KeyID|按键的虚拟键值|
|event.ScanCode|按键扫描码|
|event.Extended|判断是否为增强键盘的扩展键|
|event.Injected|判断这个事件是否由程序方式生成，而不是正常的人为触发。|
|event.Alt|是某同时按下Alt
|event.Transition|判断转换状态|
