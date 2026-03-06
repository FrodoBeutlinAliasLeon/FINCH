from pydantic import BaseModel #here i can create lists to choose from, for attributes, device etc so no mistakes will happen
from pathlib import Path

STATE_FILE = str(Path(__file__).parent /'state.json')
class Room(BaseModel):
        temp: float
        humidity: float
class Light(BaseModel):
    hue: int
    saturation: int
    brightness: int
    on: bool
class Devices(BaseModel):
    light_strip: Light
    light_mirror: Light
    light_wall: Light
    
class SmartHome(BaseModel):
    devices: Devices
    room: Room
    
def get_state() -> SmartHome:
    with open(STATE_FILE, "r") as f:
        data = f.read()
    return SmartHome.model_validate_json(data)

def save_state(state: SmartHome):
    with open(STATE_FILE, "w") as f:
        f.write(state.model_dump_json(indent=4))



    
    

        
    