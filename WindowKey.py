import keyboard
import win32gui, win32com.client
import win32con,win32api
import time

def IsTogglePressed():
    return keyboard.is_pressed(toggler.ToggleKey)
def IsToggleAndAltPressed():
    return keyboard.is_pressed(toggler.ToggleKey) and keyboard.is_pressed("alt")
def RunCommand(ToggleCondition):
    DetectKeyDown = 0
    while True:
        if ToggleCondition():
            toggler.WinCtrl()
            while IsTogglePressed():
                time.sleep(0.1)  # 키가 눌린 상태에서 반복 실행 방지
                DetectKeyDown += 0.1
            if DetectKeyDown > 0.8:
                toggler.WinCtrl()
            DetectKeyDown = 0
        if keyboard.is_pressed('f3'):
            toggler.SetAlpha(255)
            toggler.add_interact()
            break
        time.sleep(0.03)
class Toogler:
    def __init__(self,hwnd):
        self.IsMaximized =False
        self.Bit = 0
        self.hwnd = hwnd
        self.ToggleKey = None
        with open('setting.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()  # 파일의 각 줄을 리스트로 반환
            self.Bit = int(lines[0])
            self.ToggleKey = lines[1]
    def __getitem__(self,index):
        return (self.Bit & (1 << index)) > 0  # 비트를 확인
    def WinCtrl(self):
        if self.IsMaximized:
            self.WinMinimize()
            self.IsMaximized = False
        else:
            self.WinMaximize()
            self.IsMaximized = True
    def WinMinimize(self):
        if self[4]:
            win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)
            return
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
        if self[0]:
            win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)#고정 풀기
        elif self[2] or self[3]:
            alpha = 191 - 70 * self[3]
            self.SetAlpha(alpha)
        if self[6]:
            self.add_interact()
    def WinMaximize(self):
        if self[6]:
            self.disable_interact()
        else:
            win32gui.SetForegroundWindow(self.hwnd)
        win32gui.ShowWindow(self.hwnd, 9)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)
        if self[0] or self[1]:
            win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)#창 고정
        if self[2] or self[3]:
            self.SetAlpha(255)

    def SetAlpha(self,Alpha):
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, 
                win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(0, 0, 0), Alpha, win32con.LWA_ALPHA)
        
    def disable_interact(self):
        self.style= win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
        new_style = self.style | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, new_style)
        

    def add_interact(self):
        self.style= win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
        new_style = self.style & (~win32con.WS_EX_TRANSPARENT)
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, new_style)


        

def window_enumeration_handler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

top_windows = []
def getWindowHandle():
    win32gui.EnumWindows(window_enumeration_handler, top_windows)



getWindowHandle()
number = 0
AvailableWindows=[]
toggler = Toogler(None)
if(toggler[8]):
    for i in top_windows:
        if(i[1] != "" and win32gui.GetWindowLong(i[0], win32con.GWL_STYLE) & win32con.WS_VISIBLE):
            number +=1
            print("<"+str(number)+">", "name:",i[1])
            AvailableWindows.append(i)
else:
    AvailableWindows= top_windows
    for i in AvailableWindows:
        number += 1
        print("<"+str(number)+">", "name:",i[1])
del top_windows
print("\n컨트롤 할 창의 번호를 설정하세요.\n현재 사용가능한 창의 갯수:",number)
ControlNunmber = ""
while True:
    ControlNunmber = input()
    if (not ControlNunmber.isdigit()):
        print("입력 오류: 숫자를 입력해 주세요.")
    elif(int(ControlNunmber) > len(AvailableWindows)):
        print("입력 오류: 최대",str(number),"까지 입력 가능합니다.")
    else:
        break
ControlNunmber = int(ControlNunmber) - 1
print("현재",AvailableWindows[ControlNunmber][1],"를 조작하고 있습니다.\n핸들 넘버:",AvailableWindows[ControlNunmber][0])
ControlHWND = AvailableWindows[ControlNunmber][0]
toggler.hwnd = ControlHWND
del number
del ControlNunmber
del AvailableWindows
del ControlHWND
print(toggler[7]*"alt+",toggler.ToggleKey,"를 눌러서 최대화/최대화 해제를 토글합니다.")

if toggler[7]:
    RunCommand(IsToggleAndAltPressed)
else:
    RunCommand(IsTogglePressed)
