## 线程示例

```
# 该文件用于脚本的执行和停止

import pyautogui
import time
import threading

class Runner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('run')
        while 1:
            if(self.flag):
   
            else:
                time.sleep(1)
                pass
            if(self.closeFlag == False):
                break
        print('end')

 
    def go(self):
        self.flag = True

    def suspend(self):
        self.flag = False

    def close(self):
        self.closeFlag = False

```

使用
```
    th1 = run.Runner()
    th1.start()
    th1.go()
```