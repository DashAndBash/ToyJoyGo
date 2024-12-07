import keyboard
import time

class Settings:
    def __init__(self):
        #비트연산 기호 사용.
        #근데 개쩌는 오퍼레이터를 사용해서 편하게 딸깍계산 가능함.
        #고정 토글기능[0]
        #상시 고정[1]
        #비활성시 창 25%반투명화[2]
        #비활성시 창 75%반투명화[3]
        #비활성시 창 최소화[4]
        #자동 포커싱[5]
        #상호작용 비활성화[6]
        #alt+" " 키 조합[7]
        #검색 필터 활성화[8]
        self.Bit = 0
        self.ToggleKey = None
        with open('setting.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()  # 파일의 각 줄을 리스트로 반환
            self.Bit = int(lines[0])
            self.ToggleKey = lines[1]
    def __setitem__(self,index,value):
        if value:
            self.Bit |= (1 << index)  # 비트를 1로 설정
        else:
            self.Bit &= ~(1 << index)  # 비트를 0으로 설정
    def __getitem__(self,index):
        return (self.Bit & (1 << index)) > 0  # 비트를 확인
    def SettingMain(self):
        time.sleep(0.3)
        print("사용할 옵션의 넘버를 입력하세요."
        ,"\n<1> 토글 키 설정:",self.ToggleKey
        ,"\n<2> 고정 토글:","on" * self[0]
        ,"\n<3> 언제나 고정:","on" * self[1]
        ,"\n<4> 선택적 반투명 효과:","on" * self[2]
        ,"\n<5> 강화된 반투명 효과:","on" * self[3]
        ,"\n<6> 비활성 시 최소화:","on" * self[4]
        ,"\n<7> 자동 포커싱:","on" * self[5]
        ,"\n<8> 상호작용 비활성화:","on" * self[6]
        ,"\n<9> Alt키 조합:","on" * self[7]
        ,"\n<0> 검색 필터링:","on" * self[8])
        key = keyboard.read_event().name
        OptionFunction = [self.SetKey,self.SetToggle,self.AlwaysFixed
                          ,self.TransparentSmall25,self.TransparentSmall75
                          ,self.JustMinimize,self.WinAutoFocus
                          ,self.WinInteract,self.AltRequire
                          ,self.SerachFileter]
        if key.isdigit():
            key = int(key)
            if key > 0:
                OptionFunction[int(key)-1]()
            else: #0임
                OptionFunction[9]
    def SetToggle(self):#[0],2
        print("고정 토글 기능은 창 최대시 창을 맨 앞에 고정하고, 최소화시 창의 고정을 해제합니다."+
            "전체화면시 백그라운드에 있던 창도 앞으로 보내는 장점도 있지만,\n"+
            "자체 고정기능이 있는 창에 사용하기 부적절합니다.\n"+
            "고정토글 기능을 켜시겠습니까?  (y/n)\n")
        self.WaitAnswerYN(0,"고정 토글",[1])
    def AlwaysFixed(self):#[1],3
        print("항시 고정 기능은 창이 항상 고정되도록 설정됩니다.\n"+
            "항시 고정 기능을 켜시겠습니까?  (y/n)\n")
        self.WaitAnswerYN(1,"언제나 고정",[0])
    def TransparentSmall25(self):#[2],4
        print("창이 작은 상태일때, 25% 반투명해집니다.\n"+
            "25%는 작은 창이 보이고 뒤가 살짝 비치는 정도입니다.\n\n"+
            "반투명효과를 활성화하시겠습니까?  (y/n)\n")
        self.WaitAnswerYN(2,"선택적 반투명 기능",[3,4])
    def TransparentSmall75(self):#[3],5
        print("반투명 효과가 75% 로 강화됩니다.\n"+
            "75%는 창이 겨우 보이고 뒤가 훤히 보이는 정도입니다.\n\n"+
            "반투명 효과를 강화를 활성화하시겠습니까?  (y/n)\n")
        self.WaitAnswerYN(3,"강력한 반투명 기능",[2,4])
    def JustMinimize(self):#[4],6
        print("창? 모르겠고 그냥 최소화됩니다.\n"+
            "그냥 소리만 듣고 싶을때 있잖아요.\n"+
            "반투명 효과를 강화를 활성화하시겠습니까?  (y/n)\n")
        self.WaitAnswerYN(4,"반투명 효과 강화 기능",[0,1,2,3,6])
    def WinAutoFocus(self):#[5],7
        print("창 선택시 자동으로 포커싱됩니다.\n"+
            "디스코드방송의 경우 포커싱하지 않으면 창 크기가 안맞춰집니다.\n"+
            "자동 포커싱을 활성화하시겠습니까?  (y/n)\n")
        self.WaitAnswerYN(5,"자동 포커싱",[6])
    def WinInteract(self):#[6],8
        print("비활성화시 창이 최대화 되었을때 그 창은 커서를 위에 올리거나 클릭해도 상호작용이 안됩니다.\n"+
            "창 위에 커서를 올리면 화면이 변한다는 점이 불편할때 사용하기 좋습니다.\n"+
            "비활성시 최소화가 자동으로 비활성화됩니다.\n"+
            "상호작용을 활성화하시겠습니까?  (y/n)\n")
        self.WaitAnswerYN(6,"최대화 시 상호작용",[4,5])
    def AltRequire(self):#[7],9
        print("키 입력시 Alt+"+self.ToggleKey+"를 입력해야 발동됩니다.\n"+
            "기본 조작보다 조금더 불편해지지만 필요할 때가 있을껍니다.\n"+
            "키조합을 활성화하시겠습니까?  (y/n)\n")
        self.WaitAnswerYN(7,"Alt키 조합")
    def SerachFileter(self):#[8]
        print("제목없는 창들과 DefaultIME, MSCTFIME UI 를 제외하고 섬색합니다.\n"+
            "시각적으로 검색하기 편리해지지만, 원하는 창이 없을 수도 있습니다.\n"+
            "검색필터를 활성화하시겠습니까?  (y/n)\n")
        self.WaitAnswerYN(8,"검색 필터링")
    def WaitAnswerYN(self,index,text,AutoDisable = []):
        while True:
            key = keyboard.read_event().name
            if key =="y":
                print(text+"이 활성화 되었습니다.")
                self[index] = 1
                for i in AutoDisable:
                    self[i] = 0
                break
            elif key =="n":
                print(text+"이 비활성화 되었습니다.")
                self[index] = 0
                break
        self.SaveSettings()
        self.SettingMain()
    def SetKey(self):
        print("지금부터 누르는 키가 토글 키로 설정됩니다.")
        while keyboard.is_pressed("1"):
            time.sleep(0.1)
        key = keyboard.read_event().name
        print(key,"를 눌러서 최대화/최대화 해제를 토글합니다.")
        self.ToggleKey = key
        self.SaveSettings()
        self.SettingMain()
    def SaveSettings(self):
        # 파일 쓰기 (with 사용)
        with open('setting.txt', 'w', encoding='utf-8') as file:
            file.write(f"{self.Bit}\n{self.ToggleKey}")

settings = Settings();
settings.SettingMain()