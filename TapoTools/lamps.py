from tapo import ApiClient
import asyncio
import os
from dotenv import load_dotenv
import time
import math
from State.world_state import save_state, get_state
from typing import Optional
load_dotenv()
client = ApiClient(tapo_username=os.getenv("TAPO_USER"), tapo_password=os.getenv("TAPO_PW"))

def light_on():
    "Turn the standard light on"
    async def _do():
        device1 = await client.l530(ip_address="192.168.188.23")
        device2 = await client.l530(ip_address="192.168.188.24")
        await device1.on()
        
        await device2.on()
    asyncio.run(_do())
    #change the world state
    state = get_state()
    state.devices.light_mirror.on = True
    state.devices.light_wall.on = True
    save_state(state)

def light_off():
    "Turn the standard light off"
    async def _do():
        device1 = await client.l530(ip_address="192.168.188.23")
        device2 = await client.l530(ip_address="192.168.188.24")
        await device1.off()
        await device2.off()
    asyncio.run(_do())
    #change the world state
    state = get_state()
    state.devices.light_mirror.on = False
    state.devices.light_wall.on = False
    save_state(state)
    

    
    
    

    
    
def change_color(h: int,s: int):
    "Change Color, h is hue and s is saturation"
    async def _do():
        device1 = await client.l530(ip_address="192.168.188.23")
        device2 = await client.l530(ip_address="192.168.188.24")
        await device1.set_hue_saturation(int(h),int(s))
        await device2.set_hue_saturation(int(h),int(s))
    asyncio.run(_do())
    #change the world state
  
    state = get_state()
    state.devices.light_mirror.hue = h
    state.devices.light_wall.hue = h
    state.devices.light_mirror.saturation = s
    state.devices.light_wall.saturation = s
    save_state(state)

# Light Strip
def light_strip_on():
    "Turn the LED strip on"
    change_color_light_strip()
    
def change_color_light_strip(h: Optional[int] = None,s: Optional[int] = None):
    "Change Color of the light strip (and turn it on), h is hue and s is saturation"  
    state = get_state()  
    async def _do():
        device = await client.l900(ip_address="192.168.188.31")
        await device.set_hue_saturation(h,s)
    print(h)
    print(s)
    if h is None and s is None:
        h = state.devices.light_strip.hue
        s = state.devices.light_strip.saturation
    else:
        #change the world state
        state.devices.light_strip.hue = h
        state.devices.light_strip.saturation = s
        
    
    state.devices.light_strip.on = True
    save_state(state)
    asyncio.run(_do())
    
def light_strip_off():
    "Turn the LED strip off"
    async def _do():
        device = await client.l900(ip_address="192.168.188.31")
        await device.off()
    asyncio.run(_do())
    #change the world state
    state = get_state()
    state.devices.light_strip.on = False
    save_state(state)
        
   

def change_brightness(brightness):
    async def _do():
        "Change the brighthness 0-100 of main lamps"
        device1 = await client.l530(ip_address="192.168.188.23")
        device2 = await client.l530(ip_address="192.168.188.24")
        # set_brightness is provided by tapo L530; no-op if value unchanged
        await device1.set_brightness(brightness)
        await device2.set_brightness(brightness)
    asyncio.run(_do())
    #change the world state
    state = get_state()
    state.devices.light_mirror.brightness = brightness
    state.devices.light_wall.brightness = brightness
    save_state(state)
       
def react():
    async def _do():
        device1 = await client.l900(ip_address="192.168.188.31")
        tasks = []
        steps=1
        for i in range(1, steps+1):
                formula = lambda x : (math.sin(x*2*math.pi - math.pi/2)+1)/2
                print(math.ceil(100* formula(i/(steps+1))))
                tasks.append(asyncio.create_task(device1.set_brightness(math.ceil(100* formula(i/(steps+1))))))
                await asyncio.sleep(0.05)
        asyncio.create_task(device1.set_hue_saturation(240,60))
        await asyncio.gather(*tasks)
        #await device1.off()
    asyncio.run(_do())
    state = get_state()
    if state.devices.light_strip.on == False:
        light_strip_off()
    else:
        change_color_light_strip(state.devices.light_strip.hue,state.devices.light_strip.saturation)
        
             
        
      
        
        
    
    
    