
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