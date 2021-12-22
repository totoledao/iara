import pyautogui
import win32api, win32con
import keyboard
import time
import random
import pyaudio,audioop

state = "waiting"
launch_time = 0.2 + random.random()
fishingPos = ()
noiseThreshold = 5500 
 
def setFishingSpot():
  global fishingPos  
  print("press space to set pos")

  keyboard.wait('space')
  fishingPos = pyautogui.position()  

def castHook():
  global launch_time, state
  print("Started fishing")
  time.sleep(1)

  win32api.SetCursorPos(fishingPos)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)  
  time.sleep(launch_time)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

  state = "fishing"

def hookFish():
  global state
  print("FISHIN'")
  p = pyaudio.PyAudio()
  stream = p.open(format=pyaudio.paInt16,channels=2,rate=44100,input=True,frames_per_buffer=1024)
  time.sleep(3)
  startCounter = time.time()  

  while state == "fishing":    
    data = stream.read(1024)
    reading = audioop.max(data, 2)
    endCounter = time.time()
    
    if reading >= noiseThreshold:
      print("Clicked to fish! Treshold: ", reading)
      stream.stop_stream()
      stream.close()
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
      time.sleep(0.1)
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
      state = "catching"
      break

    if endCounter - startCounter >= 35 + random.random():
      print("Is stuck, set to wait")
      stream.stop_stream()
      stream.close()
      state = "waiting"
      time.sleep(1)
      break

def catchFish():
  global state
  print("Started Catching")
  time.sleep(0.2)
  bobber = pyautogui.locateOnScreen('bobber.png', confidence = 0.7, region = (830, 530, 260, 65) )
  
  if bobber == None:
    print("set to wait")
    state = "waiting"
    time.sleep(1) 
  
  while bobber != None:

    print("In minigame")
    (x, y, w, h) = bobber   
    bobberPosX = x + ( 0.5 * w )

    if bobberPosX <= 1010 and bobberPosX > 960:      
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
      time.sleep(random.random())
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

    if bobberPosX <= 960 and bobberPosX > 890:    
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
      time.sleep(random.random() + 1)
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)      
    
    if bobberPosX <= 890:      
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
      time.sleep(random.random() + 2.4)
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

setFishingSpot()
while 1:    
  if state == "waiting":
    castHook()
  if state == "fishing":
    hookFish()
  if state == "catching":
    catchFish()