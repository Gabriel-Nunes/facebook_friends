import win32gui

appname = 'Command Prompt'
xpos = 50
ypos = 100
width = 800
length = 600

def enumHandler(hwnd, lParam):
    if win32gui.IsWindowVisible(hwnd):
        if appname in win32gui.GetWindowText(hwnd):
            win32gui.MoveWindow(hwnd, xpos, ypos, width, length, True)

def run():
    win32gui.EnumWindows(enumHandler, None)