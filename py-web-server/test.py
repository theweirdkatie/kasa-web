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

@app.get("/devices/")
async def list_devices():
    return TEST_DATA

@app.get("/{deviceId}/")
async def get_device(deviceId: str):
    for device in TEST_DATA:
        if device["host"] == deviceId:
            return device
    return "error"
    
@app.post("/{deviceId}/")
async def set_device_property(deviceId: str, alias: Union[str, None] = None, state: Union[bool, None] = None):
    for device in TEST_DATA:
        if device["host"] == deviceId:
            if device.deviceType == DeviceType.Strip.value:
                if alias:
                    device.alias = alias
                if isinstance(state, bool):
                    for child in TEST_CHILD_DATA:
                        child.state = state

                return device
            
            else:
                if alias:
                    device.alias = alias
                if isinstance(state, bool):
                    device.state = state
                
                return device
            
    return "error"

@app.get("/{deviceId}/children")
async def get_children(deviceId: str):
    return TEST_CHILD_DATA
    
@app.get("/{host}/children/{childId}")
async def get_child(host: str, childId: str):
    idx = int(childId)
    if idx < len(TEST_CHILD_DATA):
            return TEST_CHILD_DATA[idx]
    else:
        return "child doesn't exist"
    
@app.post("/{parentIp}/children/{deviceId}")
async def set_child_device_property(parentIp: str, deviceId: str, alias: Union[str, None] = None, state: Union[bool, None] = None):
    idx = int(deviceId)
    if idx < len(TEST_CHILD_DATA):
        if alias:
            TEST_CHILD_DATA[idx].alias = alias
        if isinstance(state, bool):
            TEST_CHILD_DATA[idx].state = state
            
        return TEST_CHILD_DATA[idx]
    else:
        return "child doesn't exist"

TEST_DATA = [
    {
        "host": "192.168.1.12",
        "deviceType": 3,
        "deviceId": "6C:5A:B0:15:F2:EF",
        "alias": "Aquarium Strip",
        "mac": "6C:5A:B0:15:F2:EF",
        "state": "true"
    },
    {
        "host": "192.168.1.207",
        "deviceType": 1,
        "deviceId": "9C:A2:F4:0C:C5:96",
        "alias": "Tank Lamp 1",
        "mac": "9C:A2:F4:0C:C5:96",
        "state": "true"
    },
    {
        "host": "192.168.1.32",
        "deviceType": 1,
        "deviceId": "9C:A2:F4:0C:C4:2F",
        "alias": "Plant Lamp",
        "mac": "9C:A2:F4:0C:C4:2F",
        "state": "true"
    },
    {
        "host": "192.168.1.194",
        "deviceType": 1,
        "deviceId": "9C:A2:F4:0C:D7:6A",
        "alias": "Tank Lamp 2",
        "mac": "9C:A2:F4:0C:D7:6A",
        "state": "true"
    },
    {
        "host": "192.168.1.31",
        "deviceType": 6,
        "deviceId": "9C:A2:F4:F2:A5:3B",
        "alias": "TV Lights",
        "mac": "9C:A2:F4:F2:A5:3B",
        "state": "false"
    },
]

TEST_CHILD_DATA = [
    {
        "host": "192.168.1.12",
        "deviceType": 4,
        "deviceId": "000",
        "alias": "Filter",
        "mac": "6C:5A:B0:15:F2:EF",
        "state": "true"
    },
    {
        "host": "192.168.1.12",
        "deviceType": 4,
        "deviceId": "001",
        "alias": "Light",
        "mac": "6C:5A:B0:15:F2:EF",
        "state": "true"
    },
    {
        "host": "192.168.1.12",
        "deviceType": 4,
        "deviceId": "002",
        "alias": "Heater",
        "mac": "6C:5A:B0:15:F2:EF",
        "state": "true"
    },
]