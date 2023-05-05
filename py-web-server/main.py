from typing import Union, List
import json
from fastapi import FastAPI
from kasa import Discover, SmartDevice
from enum import Enum, auto
import asyncio

app = FastAPI()

class DeviceType(Enum):
  Plug = 1
  Bulb = auto()
  Strip = auto()
  StripSocket = auto()
  Dimmer = auto()
  LightStrip = auto()
  Unknown = -1,

class ChildDevice:
    id: str
    alias: str

class SmartDeviceAPI:
    host: str
    deviceType: DeviceType
    deviceId: str
    alias: str
    mac: str

    def __init__(self, device: SmartDevice):
        self.host = device.host
        self.deviceType = device.device_type
        self.deviceId = device.device_id
        self.alias = device.alias
        self.mac = device.mac

    def toJSON(self):
        _json = {
            "host": self.host,
            # "deviceType": self.deviceType,
            "deviceId": self.deviceId,
            "alias": self.alias,
            "mac": self.mac
        }

        return json.dumps(_json)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/devices/")
async def list_devices(host: Union[str, None] = None):
    if host:
        dev = SmartDevice(host)
        await dev.update()
        return SmartDeviceAPI(dev).toJSON()
    
    try: 
        found_devices = await (Discover.discover())

        devices = []

        for device in found_devices.values():
            obj = SmartDeviceAPI(device)
            devices.append(obj.toJSON())

        return devices
    except:
        return TEST_DATA

TEST_DATA = '''[
  "{\"host\": \"192.168.1.12\", \"deviceId\": \"6C:5A:B0:15:F2:EF\", \"alias\": \"TP-LINK_Power Strip_F2EF\", \"mac\": \"6C:5A:B0:15:F2:EF\"}",
  "{\"host\": \"192.168.1.207\", \"deviceId\": \"9C:A2:F4:0C:C5:96\", \"alias\": \"Tank Lamp 1\", \"mac\": \"9C:A2:F4:0C:C5:96\"}",
  "{\"host\": \"192.168.1.32\", \"deviceId\": \"9C:A2:F4:0C:C4:2F\", \"alias\": \"Plant Lamp\", \"mac\": \"9C:A2:F4:0C:C4:2F\"}",
  "{\"host\": \"192.168.1.194\", \"deviceId\": \"9C:A2:F4:0C:D7:6A\", \"alias\": \"Tank Lamp 2\", \"mac\": \"9C:A2:F4:0C:D7:6A\"}",
  "{\"host\": \"192.168.1.31\", \"deviceId\": \"9C:A2:F4:F2:A5:3B\", \"alias\": \"TV Lights\", \"mac\": \"9C:A2:F4:F2:A5:3B\"}"
]'''