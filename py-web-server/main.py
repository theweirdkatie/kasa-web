from typing import Union
import jsonpickle
from fastapi import FastAPI
from kasa import Discover, SmartDevice

app = FastAPI()


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
    return jsonpickle.encode(list(found_devices.values()))