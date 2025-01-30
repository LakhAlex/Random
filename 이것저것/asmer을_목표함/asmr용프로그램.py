from tkinter import *
from PIL import ImageTk, Image
import pygame

def forest():
    global bg
    img = Image.open('imageFiles/BackGround_2.png')
    bg = ImageTk.PhotoImage(img)
    label.config(image=bg)

    # sound = pygame.mixer.stop()
    # sound = pygame.mixer.Sound('soundFiles/숲_새소리.mp3')
    # sound.play(-1)

    pygame.mixer_music.stop()
    pygame.mixer_music.load('soundFiles/숲_새소리.mp3')
    pygame.mixer_music.play(-1)

    # print("배경화면이 숲으로 변했습니다.")


def sea():
    global bg
    img = Image.open('imageFiles/BackGround_1.png')
    bg = ImageTk.PhotoImage(img)
    label.config(image=bg)

    # sound = pygame.mixer.stop()
    # sound = pygame.mixer.Sound('soundFiles/파도소리.mp3')
    # sound.play(-1)

    pygame.mixer_music.stop()
    pygame.mixer_music.load('soundFiles/파도소리.mp3')
    pygame.mixer_music.play(-1)

    # print("배경화면이 바다로 변했습니다.")

def soundSet(value):
    volume = float(value) / 100
    pygame.mixer_music.set_volume(volume)

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
soundValue.pack()

# Tkinter 화면 계속 띄워둘 수 있게 하기
win.mainloop()

# pyintaller -w -F asmr용프로그램.py 로 생성하기