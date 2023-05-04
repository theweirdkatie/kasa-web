from typing import Union
import jsonpickle
from fastapi import FastAPI
from kasa import Discover, SmartDevice
from enum import Enum, auto

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
    name: str
    alias: str
    mac: str
    hasChildren: bool
    children: list(ChildDevice)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/devices/")
async def list_devices(host: Union[str, None] = None):
    if host:
        dev = SmartDevice(host)
        await dev.update()
        return jsonpickle.encode(dev)
    found_devices = await Discover.discover()

    devices = []

    for device in found_devices.values():
        devices.append(convert_device(device))

    return jsonpickle.encode(devices)
    
async def convert_device(device: SmartDevice):
    d = SmartDeviceAPI
    d.alias = device.alias
    d.host = device.host
    d.deviceId = device.device_id
    d.deviceType = device.device_type
    d.hasChildren = len(device.children) > 0
    if d.hasChildren:
        for child in device.children:
            c = convert_device(child)
            d.children.append(c)

    return d