# import os
# import pystray
# from pystray import MenuItem as item
# from PIL import Image
# import threading
# import time

# # 이미지 파일 경로를 리스트로 가져오는 함수
# def get_image_paths(folder):
#     return [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(('png', 'jpg', 'jpeg', 'gif'))]

# # 아이콘을 변경하는 함수
# def change_icon(icon, images):
#     while True:
#         for image_path in images:
#             icon.icon = Image.open(image_path)
#             time.sleep(0.6)  # 0.1: 매우 빠름 / 0.3 : 보통 / 0.6 : 느림

# # 아이콘을 실행하는 함수
# def on_quit(icon, item):
#     icon.stop()

# # 이미지가 있는 폴더 경로
# folder_path = 'imageFiles/hearts/'  # 여기에 폴더 경로를 입력하세요
# image_paths = get_image_paths(folder_path)

# # 메뉴 설정
# icon = pystray.Icon("test_icon", Image.open(image_paths[0]), menu=pystray.Menu(item('Quit', on_quit)))

# # 스레드로 이미지 변경 시작
# thread = threading.Thread(target=change_icon, args=(icon, image_paths))
# thread.daemon = True
# thread.start()

# # 아이콘 실행
# icon.run()


import os
import psutil
import time
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
from threading import Thread
import queue

# # 이미지 파일 경로를 리스트로 가져오는 함수
# def get_image_paths(folder):
#     return [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(('png', 'jpg', 'jpeg', 'gif'))]

# # 아이콘을 변경하는 함수
# def change_icon(icon, images, speed_queue):
#     while True:
#         for image_path in images:
#             icon.icon = Image.open(image_path)
#             # speed_queue에서 속도 정보를 받아옴
#             speed = speed_queue.get()  
#             time.sleep(speed)  # CPU 사용량에 따른 동적 속도 변경

# 이미지를 생성하는 함수
def create_image(color):
    width, height = 64, 64
    image = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), f'Color: {color}', fill='white')
    return image

# 아이콘을 변경하는 함수
def change_icon(icon, speed_queue):
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    while True:
        for color in colors:
            icon.icon = create_image(color)
            # speed_queue에서 속도 정보를 받아옴
            speed = speed_queue.get()  
            time.sleep(speed)  # CPU 사용량에 따른 동적 속도 변경


# 프로그램 종료를 위한 함수
def on_exit(icon, item):
    icon.stop()  # 트레이 아이콘 종료

# CPU 사용량에 따른 속도 조정 함수
def monitor_cpu_usage(speed_queue):
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)  # 1초마다 CPU 사용량 측정
        print(f"CPU 사용량 : {cpu_usage}%")
        
        # CPU 사용량에 따라 이미지 변경 속도 조정
        if cpu_usage < 5:
            speed_queue.put(0.5)  # 낮은 CPU 사용량 -> 느리게
        elif cpu_usage < 15:
            speed_queue.put(0.3)  # 보통 CPU 사용량 -> 보통 속도
        else:
            speed_queue.put(0.1)  # 높은 CPU 사용량 -> 빠르게
        
        time.sleep(1)

# 트레이 아이콘 실행 함수
def main():
    # # 이미지가 있는 폴더 경로
    # folder_path = 'imageFiles/hearts/'  # 여기에 폴더 경로를 입력하세요
    # image_paths = get_image_paths(folder_path)

    # 속도 정보를 저장할 큐 생성
    speed_queue = queue.Queue()

    # 메뉴 설정
    # icon = Icon("test_icon", Image.open(image_paths[0]), menu=Menu(MenuItem('Exit', on_exit)))
    icon = Icon("test_icon", create_image('red'), menu=Menu(MenuItem('Quit', on_exit)))

    # 스레드로 이미지 변경 시작
    # thread = Thread(target=change_icon, args=(icon, image_paths, speed_queue))
    thread = Thread(target=change_icon, args=(icon, speed_queue))
    thread.daemon = True
    thread.start()

    # CPU 사용량을 모니터링하는 스레드 시작
    thread2 = Thread(target=monitor_cpu_usage, args=(speed_queue,))
    thread2.daemon = True
    thread2.start()

    # 아이콘 실행
    icon.run()

if __name__ == "__main__":
    main()
