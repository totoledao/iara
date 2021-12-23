import pyautogui
import win32api, win32con
import keyboard
import time
import random
import pyaudio,audioop
import dearpygui.dearpygui as dpg

state = "waiting"
launch_time = 0.05 + random.random()
fishingPos = []
noiseThreshold = 5500
noiseReading = 0
botStarted = False

### Bot functions

def setFishingSpot():
  global fishingPos  
  print("press space to set pos")

  keyboard.wait('space')
  fishingPos.append(pyautogui.position())

  # Sets UI Fishing Spots value
  dpg.set_value("spots" ,'Total Spots: ' + str(len(fishingPos)) )
  # Sets UI Fishing Spots Helper text
  dpg.set_value("fishingSpotText", '')

def getRandomFishingSpot():
  x = random.randrange(len(fishingPos))  
  return fishingPos[x]

def castHook():
  global launch_time, state
  print("Started fishing")
  time.sleep(1)
  
  win32api.SetCursorPos(getRandomFishingSpot())
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)  
  time.sleep(launch_time)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

  state = "fishing"

def hookFish():
  global state, noiseReading
  print("FISHIN'")
  p = pyaudio.PyAudio()
  stream = p.open(format=pyaudio.paInt16,channels=2,rate=44100,input=True,frames_per_buffer=1024)
  time.sleep(3)
  startCounter = time.time()  

  while state == "fishing":    
    data = stream.read(1024)
    noiseReading = audioop.max(data, 2)
    endCounter = time.time()
    # Sets UI noise value
    dpg.set_value('noise', noiseReading)
    
    if noiseReading >= noiseThreshold:
      print("Clicked to fish! Treshold: ", noiseReading)
      stream.stop_stream()
      stream.close()
      # Sets UI noise value
      dpg.set_value('noise', 0)
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
      time.sleep(0.1)
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
      state = "catching"
      break

    if endCounter - startCounter >= 35 + random.random():
      print("Is stuck, set to wait")
      stream.stop_stream()
      stream.close()
      # Sets UI noise value
      dpg.set_value('noise', 0)
      state = "waiting"
      time.sleep(1)
      break

def catchFish():
  global state
  print("Started Catching")
  time.sleep(0.2)
  
  if pyautogui.locateOnScreen('bobber.png', confidence = 0.7, region = (830, 530, 260, 65) ) == None:
    print("set to wait")
    state = "waiting"
    time.sleep(1) 
  
  while pyautogui.locateOnScreen('bobber.png', confidence = 0.7, region = (830, 530, 260, 65) ) != None:

    print("In minigame")
    (x, y, w, h) = pyautogui.locateOnScreen('bobber.png', confidence = 0.7, region = (830, 530, 260, 65) )   
    bobberPosX = x + ( 0.5 * w )

    if bobberPosX <= 1030 and bobberPosX > 1000:      
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
      time.sleep(random.random())
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

    if bobberPosX <= 1000 and bobberPosX > 970:    
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
      time.sleep(random.random() + 0.4)
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)      
    
    if bobberPosX <= 970 and bobberPosX > 930:    
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
      time.sleep(random.random() + 1)
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)      
    
    if bobberPosX <= 930:     
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
      time.sleep(random.random() + 2)
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

#### Callbacks for the UI

def start():
  global fishingPos

  if len(fishingPos) > 0:
    print("started")
    botStarted = True  
    while botStarted:    
      if state == "waiting":
        castHook()
      if state == "fishing":
        hookFish()
      if state == "catching":
        catchFish()

def stop():
  print("stopped")
  botStarted = False
  fishingPos = [()]
  # Sets UI Fishing Spots value
  dpg.set_value("spots", 'Total Spots: 0')
  # Sets UI Fishing Spots Helper text
  dpg.set_value("fishingSpotText", '(Add at least one fishing spot)')

def setNoiseThreshold():
  global noiseThreshold

  noiseThreshold = dpg.get_value("threshold")
  print(noiseThreshold)

def blockSetNoise():
  dpg.set_value('noise', noiseReading)

### UI

#Creates the DearPyGui Window
dpg.create_context()
dpg.create_viewport(title='iara', width=480, height=260)
dpg.setup_dearpygui()

# Boilerplate to process image to be displayed
width, height, channels, data = dpg.load_image("iaraLogo.png")
with dpg.texture_registry():
    logo = dpg.add_static_texture(width, height, data)

with dpg.window(tag="iara"):

  dpg.add_image(logo, height=77, width=230)
  dpg.add_spacer(height=5)

  with dpg.group(horizontal=True):
    # Add Fishign Spot
    dpg.add_button(label="Add Spots", callback=setFishingSpot)
    # Amount of Fishing Spots    
    dpg.add_text(label="Total Spots: ", tag="spots", default_value='Total Spots: 0')
    dpg.add_text(default_value="(Add at least one fishing spot)", tag="fishingSpotText")    
  dpg.add_spacer(height=5)

  # Noise threshold to detect when to hook the fish
  dpg.add_slider_int(label="Threshold", tag="threshold", clamped=True, max_value=10000, min_value=0, default_value=noiseThreshold, callback=setNoiseThreshold)
  # Displays current noise
  dpg.add_slider_int(label="Noise", tag="noise", clamped=True, max_value=10000, min_value=0, default_value=noiseReading, no_input=True, callback=blockSetNoise)    
  dpg.add_spacer(height=5)

  with dpg.group(horizontal=True):
    dpg.add_button(label="Start", callback=start)
    # dpg.add_button(label="Stop", callback=stop)
  
  # Displays DearPyGui Window
  dpg.show_viewport()
  dpg.set_primary_window("iara", True)
  dpg.start_dearpygui()
  dpg.destroy_context()