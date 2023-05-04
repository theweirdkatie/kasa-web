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
        return dev
    
    try: 
        found_devices = await (Discover.discover())

        devices = []

        for device in found_devices.values():
            obj = SmartDeviceAPI(device)
            devices.append(obj.toJSON())

        return devices
    except:
        return {"error": "No devices found"}