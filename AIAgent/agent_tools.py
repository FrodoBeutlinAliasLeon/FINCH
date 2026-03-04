from langchain.tools import tool
from tapo import ApiClient
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from TapoTools.lamps import (light_on, 
                             light_off, 
                             change_brightness, 
                             change_color,
                             light_strip_on,
                             light_strip_off,
                             change_color_light_strip)
load_dotenv()
client = ApiClient(tapo_username=os.getenv("TAPO_USER"), tapo_password=os.getenv("TAPO_PW"))

@tool
def light_on_agent():
    "Turn the light on"
    light_on()
    
@tool
def light_off_agent():
    "Turn the light off"
    light_off()

@tool
def change_brightness_agent(brightness):
    "Change the brighthness 1-100"
    change_brightness(brightness)

@tool
def change_color_agent(h,s):
    "Change Color, h is hue and s is saturation"
    change_color(h,s)

@tool
def light_strip_off_agent():
    "Turn the LED strip off (which is located behind the bed)"
    light_strip_off()

@tool
def light_strip_on_agent():
    "Turn the LED strip on (which is located behind the bed)"
    light_strip_on()
    
@tool
def change_color_light_strip_agent():
    "Change the color of the LED strip (which is located behind the bed)"
    change_color_light_strip()

@tool
def start_kodi():
    "Start the Kodi-App on the TV. Kodi is a private Netflix alternativ"
    subprocess.Popen(["kodi"])

@tool
def end_kodi():
    "End the Kodi-App on the TV. Kodi is a private Netflix alternativ"
    subprocess.Popen(["pkill", "-9", "kodi"])
    subprocess.run(
    ["cec-client", "-s", "-d", "1"],
    input=b"standby 0\n",
    timeout=10
)
    
@tool
def change_volume(volume: int):
    "This tool changes the volume."
    subprocess.Popen(["amixer", "set", "PCM", f"{volume}%"])
    
    
    
    
tools = [light_on_agent,
         light_off_agent, 
         change_color_agent, 
         change_brightness_agent, 
         light_strip_on_agent, 
         light_strip_off_agent,
         change_color_light_strip,
         start_kodi,
         end_kodi,]