import asyncio
import json
from fastapi import FastAPI
from kasa import Discover

app = FastAPI()

@app.get("/devices")
async def root():
    devices = await Discover.discover()
    return devices

@app.get("/devices/{item_alias}")
async def get_item_by_alias(item_alias):
    devices = await Discover.discover()
    for (_, device) in devices.items():
        if device.alias == item_alias:
            return device