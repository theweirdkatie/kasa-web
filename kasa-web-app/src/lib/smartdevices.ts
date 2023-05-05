export class SmartDevice {
    host: string;
    deviceType: number;
    deviceId: string;
    name: string;
    alias: string;
    mac: string;
    hasChildren: boolean;
    children: ChildDevice[];

    constructor(device: SmartDeviceJSON) {
        if (device === undefined) {
            this.host = "192.168.1.207";
            this.deviceType = 1;
            this.deviceId = "8006E1AF7F5634FA56B4FD9131F313862053D3BE";
            this.name = "Smart Wi-Fi Plug Mini";
            this.alias = "Table";
            this.mac = "9C:A2:F4:0C:C5:96";
            this.hasChildren = false;
            this.children = [];
        } else {
            this.host = device.host;
            this.deviceType = device.deviceType;
            this.deviceId = device.deviceId;
            this.name = deviceName(device.deviceType);
            this.alias = device.alias;
            this.mac = device.mac;
            this.hasChildren = false;
            this.children = [];
        }
    }

}

class ChildDevice {
    id: string = "";
    alias: string = "";

    constructor() {
        this.id = "";
        this.alias = "";
    }
}

type SmartDeviceJSON =  {
    host: string;
    deviceType: number;
    deviceId: string;
    alias: string;
    mac: string;
}

export async function findDevices() {
    let devices: SmartDeviceJSON[] = await fetchDevices();

    let smart_devices: SmartDevice[] = [];
    for (let i=0; i<devices.length; i++) {
        smart_devices.push(new SmartDevice(devices[i]));
    }
    return smart_devices;
}

async function fetchDevices(): Promise<SmartDeviceJSON[]> {
    let response = await fetch("http://localhost:8000/devices/", {"method": "GET"});

    const data = await response.json();

    if (response.ok) {
        if (data) {
            let devices: SmartDeviceJSON[] = JSON.parse(data);
            return devices;
        } else {
            return Promise.reject(new Error(`No devices found`));
        }
    } else {
        return Promise.reject(new Error(`No response from server`))
    }
}

function deviceName(n: number): string {
    switch (n) {
        case 1: return "Plug";
        case 2: return "Bulb";
        case 3: return "Strip";
        case 4: return "Strip Socket";
        case 5: return "Dimmer";
        case 6: return "Lightstrip";
        default: return "Undefined";
    }
}