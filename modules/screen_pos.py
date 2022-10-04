import win32gui, win32con

windowList = []
win32gui.EnumWindows(lambda hwnd, windowList: windowList.append((win32gui.GetWindowText(hwnd),hwnd)), windowList)
cmdWindow = [i for i in windowList if "python.exe" in i[0].lower()]
win32gui.SetWindowPos(cmdWindow[0][1],win32con.HWND_TOPMOST,0,0,100,100,0) #100,100 is the size of the window