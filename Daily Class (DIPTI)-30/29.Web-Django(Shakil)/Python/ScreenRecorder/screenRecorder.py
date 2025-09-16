import cv2
import pyautogui
from win32api import GetSystemMetrics
import numpy as np
import time

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

dim = (width,height)
f = cv2.VideoWriter_fourcc(*'avc1')
name = input("File name please: ")
output = cv2.VideoWriter(f"{name}.mp4",f,30.0,dim)
now_start_time = time.time()
dur = 30
end_time = now_start_time + dur
while True:
    image = pyautogui.screenshot()
    frame_1 = np.array(image)
    fram = cv2.cvtColor(frame_1, cv2.COLOR_BGR2RGB)
    output.write(fram)
    c_time = time.time()
    if c_time > end_time:
        break
output.release()
print("_end_")