from tkinter import *
from PIL import ImageTk, Image
import pygame

def forest():
    global bg
    img = Image.open('imageFiles/BackGround_2.png')
    bg = ImageTk.PhotoImage(img)
    label.config(image=bg)

    pygame.mixer_music.stop()
    pygame.mixer_music.load('soundFiles/숲_새소리.mp3')
    pygame.mixer_music.play(-1)



def sea():
    global bg
    img = Image.open('imageFiles/BackGround_1.png')
    bg = ImageTk.PhotoImage(img)
    label.config(image=bg)

    pygame.mixer_music.stop()
    pygame.mixer_music.load('soundFiles/파도소리.mp3')
    pygame.mixer_music.play(-1)

    # print("배경화면이 바다로 변했습니다.")

saveVolume = 0.5  # 기본 볼륨 (50%)
isMuted = False  # 음소거 상태 여부

def soundSet(value):
    global saveVolume, isMuted, btnImg
    volume = float(value) / 100  # 볼륨 값 계산

    # 🔹 스케일 값이 0이면 자동으로 음소거 처리
    if volume == 0:  # 볼륨이 0이면 
        isMuted = True  # 음소거 상태로 변경
        btnSpiker = Image.open('imageFiles/off.png')
    else:  # 볼륨이 1이상이면
        isMuted = False  # 음소거 해제
        btnSpiker = Image.open('imageFiles/on.png')

    # 음소거 버튼 상태 변화
    btnSpiker = btnSpiker.resize((17, 17))  # 버튼 이미지 크기 설정
    btnImg = ImageTk.PhotoImage(btnSpiker)
    mute.config(image=btnImg)  # 버튼 이미지 변경

    # 음소거 상태가 아니면 볼륨 조절
    if not isMuted:
        pygame.mixer.music.set_volume(volume)
    

# 음소서 on/off 함수
def play_And_mute():
    global saveVolume, isMuted, btnImg
    
    if isMuted:  # 음소거가 되어 있다면?
        pygame.mixer_music.set_volume(saveVolume)
        soundValue.set(saveVolume * 100)  # saveVolume값은 0.5와 같은 소수점! 하지만 보여야 하는 것은 50! -> 100을 곱해준다.
        isMuted = False
        btnSpiker = Image.open('imageFiles/on.png')

    else:  # 음소거 하고 싶다면?
        saveVolume = pygame.mixer_music.get_volume()  # 현재 음략 값을 saveVolume에 저장
        pygame.mixer_music.set_volume(0.0)
        soundValue.set(0)
        isMuted = True

        btnSpiker = Image.open('imageFiles/off.png')
    
    btnSpiker = btnSpiker.resize((17, 17))
    btnImg = ImageTk.PhotoImage(btnSpiker)
    mute.config(image=btnImg)  # 버튼 이미지 변경



pygame.init()
pygame.mixer.init()

# Sound는 mixer_music에 비하면 불안정 함 -> 한번에 하나의 노래만 재생하니 Sound 사용 X
# sound = pygame.mixer.Sound('soundFiles/파도소리.mp3')
# sound.play(-1)

pygame.mixer_music.load('soundFiles/파도소리.mp3')
pygame.mixer_music.play(-1)

win = Tk()
win.title("바다와 숲의 소리")

# 창의 크기 설정
window_width = 300
window_height = 215

# 화면 크기 가져오기
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

# 오른쪽 상단 위치 계산
x_position = screen_width - window_width  # 오른쪽 가장자리
y_position = 0  # 상단

# 배경 사진 설정
img = Image.open('imageFiles/BackGround_1.png')
bg = ImageTk.PhotoImage(img)

# 창의 크기와 나타날 위치 설정 & 크기 변경 불가
win.geometry(f'{window_width}x{window_height}+{x_position-10}+{y_position}')
win.resizable(False, False)

label = Label(win, image=bg)
label.place(x=-2, y=-2)

# 노래를 변경할 버튼 그룹 생성
btn_group = Frame(win, padx=5, pady=3)
btn_group.pack(side="bottom")

# 버튼 생성
btn1 = Button(btn_group, text="숲", command=forest)
btn1.pack(side="right", padx=3)

btn2 = Button(btn_group, text="바다", command=sea)
btn2.pack(side="right", padx=3)

# 사운드 조절 스케일
soundValue = Scale(btn_group, from_ = 0, to = 100, orient=HORIZONTAL, command=soundSet)
soundValue.set(50)
soundValue.pack(side="right", padx=3)

btnSpiker = Image.open('imageFiles/on.png')
btnSpiker = btnSpiker.resize((17, 17))
btnImg = ImageTk.PhotoImage(btnSpiker)
mute = Button(btn_group, image=btnImg, command=play_And_mute)
mute.pack(side="left")

# Tkinter 화면 계속 띄워둘 수 있게 하기
win.mainloop()

# pyinstaller -w -F asmr용프로그램.py 로 생성하기
