from flask import Flask, request
from flask_basicauth import BasicAuth
import subprocess
import os
from dotenv import load_dotenv
import glob
from tapo import ApiClient
from tapo.requests import Color 
import asyncio
import time
import random
from enum import Enum
from TTS.piper_tts import TTS
from State.world_state import save_state, get_state
print(random.randint(0,100))


app = Flask(__name__)
load_dotenv()
app.config["BASIC_AUTH_USERNAME"] = "leon"
app.config["BASIC_AUTH_PASSWORD"] = os.getenv('AUTHPW_FLASK')



basic_auth = BasicAuth(app)


@app.route("/temp-endpoint", methods=["GET"])
@basic_auth.required
def get_temp():
    data = request.get_json()
    print(data)
    temp = data["temperature"]
    humidity= data["humidity"]
    state = get_state()
    state.room.temp = temp
    state.room.humidity = humidity
    save_state(state)    
    return "OK\n", 200

client = ApiClient(tapo_username=os.getenv("TAPO_USER"), tapo_password=os.getenv("TAPO_PW"))
@app.route("/turn-light-on", methods=["GET"])
@basic_auth.required
def turn_light_on():
    async def _do():
        device1 = await client.l530(ip_address="192.168.188.23")
        device2 = await client.l530(ip_address="192.168.188.24")
        await device1.on()
        await device2.on()
    asyncio.run(_do())
    return "OK\n", 200

@app.route("/turn-light-off", methods=["GET"])
@basic_auth.required
def turn_light_off():
    async def _do():
        device1 = await client.l530(ip_address="192.168.188.23")
        device2 = await client.l530(ip_address="192.168.188.24")
        await device1.off()
        await device2.off()
    asyncio.run(_do())
    return "OK\n", 200

@app.route("/disco", methods=["GET"])
@basic_auth.required
def disco():
    
    colors = [getattr(Color, attr) for attr in dir(Color) 
          if isinstance(getattr(Color, attr), Color)]
    async def _do():

        #device_info = await device1.get_device_info()
        #print(f"Device info: {device_info.to_dict()}")
        device1 = await client.l530(ip_address="192.168.188.23")
        device2 = await client.l530(ip_address="192.168.188.24")
        device1_dict = (await device1.get_device_info()).to_dict()
        device2_dict = (await device2.get_device_info()).to_dict()
        print(device1_dict)
        time.sleep(0.2)
        
        print(f"sat: {device2_dict['default_states']['state']['saturation']}")
        print(f"brightness: {device2_dict['default_states']['state']['brightness']}")
        
        
        await device1.off()
        await device2.off()
        
        time.sleep(1)
        for _ in range(1, 80):
            random_color1 = random.choice(colors)
            random_color2 = random.choice(colors)
            await device1.set_color(random_color1)
            time.sleep(0.15)
            await device2.set_color(random_color2)
            time.sleep(0.15)
        
        #fix for edge case when sat is 0
        sat1 = device1_dict['default_states']['state']['saturation'] if device1_dict['default_states']['state']['saturation']!=0 else 1
        sat2 = device2_dict['default_states']['state']['saturation'] if device2_dict['default_states']['state']['saturation']!=0 else 1
        
        #until now we dont change temperaturé, if we do we also need to reset it here
        await device1.set_hue_saturation(
            device1_dict['default_states']['state']['hue'],
            sat1
            )
        await device2.set_hue_saturation(
            device2_dict['default_states']['state']['hue'],
            sat2
            )
        await device1.set_brightness(device1_dict['default_states']['state']['brightness'])
        await device2.set_brightness(device2_dict['default_states']['state']['brightness'])
        if not device1_dict['device_on']:
            await device1.off()
        if not device2_dict['device_on']:
            await device2.off()
        
    asyncio.run(_do())
    return "OK\n", 200
if __name__ == "__main__":
    # private certificate for https
    app.run(host="0.0.0.0", port=5051,ssl_context=('SSL/cert.pem', 'SSL/key.pem'))
