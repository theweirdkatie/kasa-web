from typing import Union, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kasa import Discover, SmartDevice, SmartStrip
from enum import Enum, auto

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DeviceType(Enum):
  Plug = 1
  Bulb = auto()
  Strip = auto()
  StripSocket = auto()
  Dimmer = auto()
  LightStrip = auto()
  Unknown = -1,

class SmartDeviceAPI:
    host: str
    deviceType: DeviceType
    deviceId: str
    alias: str
    mac: str
    state: bool

    def __init__(self, device: SmartDevice):
        self.host = device.host
        self.deviceType = device.device_type
        self.deviceId = device.device_id
        self.alias = device.alias
        self.mac = device.mac
        try:
            self.state = device.is_on
        except:
            self.state = device.sys_info.get("relay_state")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/devices/")
async def list_devices():
    try: 
        found_devices = await (Discover.discover())

        devices = []

        for device in found_devices.values():
            obj = SmartDeviceAPI(device)
            devices.append(obj)

        return devices
    except:
        return "error"
    
    # For testing
    # return TEST_DATA

@app.get("/{deviceId}/")
async def get_device(deviceId: str):
    try:
        dev = await (Discover.discover_single(deviceId))
        return SmartDeviceAPI(dev)
    except:
        return "error"
    
@app.post("/{deviceId}/")
async def set_device_property(deviceId: str, alias: Union[str, None] = None, state: Union[bool, None] = None):
    try:
        dev = await (Discover.discover_single(deviceId))
        
        if dev.device_type.value == DeviceType.Strip.value:
            strip = SmartStrip(deviceId)

            await strip.update()

            if alias:
                await strip.set_alias(alias)
            if isinstance(state, bool):
                if state:
                    for child in strip.children:
                        await child.turn_on()
                else:
                    for child in strip.children:
                        await child.turn_off()
            await strip.update()

            return SmartDeviceAPI(strip)
            
        else:
            if alias:
                await dev.set_alias(alias)
            if isinstance(state, bool):
                if state:
                    await dev.turn_on()
                else:
                    await dev.turn_off()
            await dev.update()
            
            return SmartDeviceAPI(dev)
    except:
        return "error"

@app.get("/{deviceId}/children")
async def get_children(deviceId: str):
    dev = SmartStrip(deviceId)
    try:
        await dev.update()
        
        children = []

        for child in dev.children:
            obj = SmartDeviceAPI(child)
            obj.deviceId = obj.deviceId[-3:]
            children.append(obj)

        return children
    except:
        return None
    
@app.get("/{host}/children/{childId}")
async def get_child(host: str, childId: str):
    parent = SmartStrip(host)
    try:
        await parent.update()
        
        idx = int(childId)

        if idx < len(parent.children):
            return SmartDeviceAPI(parent.children[idx])
        else:
            return "child doesn't exist"
    except:
        return None
    
@app.post("/{parentIp}/children/{deviceId}")
async def set_child_device_property(parentIp: str, deviceId: str, alias: Union[str, None] = None, state: Union[bool, None] = None):
    parent = SmartStrip(parentIp)
        
    try:
        await parent.update()

        idx = int(deviceId)

        if idx < len(parent.children):
            if alias:
                await parent.children[idx].set_alias(alias)
            if isinstance(state, bool):
                if state:
                    await parent.children[idx].turn_on()
                else:
                    await parent.children[idx].turn_off()
            await parent.update()
            
            return SmartDeviceAPI(parent.children[idx])
        else:
            return "child doesn't exist"
    except:
        return "error"

TEST_DATA = [
    {
        "host": "192.168.1.12",
        "deviceType": 3,
        "deviceId": "6C:5A:B0:15:F2:EF",
        "alias": "TP-LINK_Power Strip_F2EF",
        "mac": "6C:5A:B0:15:F2:EF"
    },
    {
        "host": "192.168.1.207",
        "deviceType": 1,
        "deviceId": "9C:A2:F4:0C:C5:96",
        "alias": "Tank Lamp 1",
        "mac": "9C:A2:F4:0C:C5:96"
    },
    {
        "host": "192.168.1.32",
        "deviceType": 1,
        "deviceId": "9C:A2:F4:0C:C4:2F",
        "alias": "Plant Lamp",
        "mac": "9C:A2:F4:0C:C4:2F"
    },
    {
        "host": "192.168.1.194",
        "deviceType": 1,
        "deviceId": "9C:A2:F4:0C:D7:6A",
        "alias": "Tank Lamp 2",
        "mac": "9C:A2:F4:0C:D7:6A"
    },
    {
        "host": "192.168.1.31",
        "deviceType": 6,
        "deviceId": "9C:A2:F4:F2:A5:3B",
        "alias": "TV Lights",
        "mac": "9C:A2:F4:F2:A5:3B"
    },
]