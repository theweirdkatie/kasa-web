export class SmartDevice {
    host: string;
    deviceType: number;
    deviceId: string;
    alias: string;
    mac: string;
    state: boolean;
    hasChildren: boolean;
    children: ChildDevice[];

    constructor(device: SmartDeviceJSON) {
        if (device === undefined) {
            this.host = "192.168.1.207";
            this.deviceType = 1;
            this.deviceId = "8006E1AF7F5634FA56B4FD9131F313862053D3BE";
            this.alias = "Table";
            this.mac = "9C:A2:F4:0C:C5:96";
            this.state = false;
            this.hasChildren = false;
            this.children = [];
        } else {
            this.host = device.host;
            this.deviceType = device.deviceType;
            this.deviceId = device.deviceId;
            this.alias = device.alias;
            this.mac = device.mac;
            this.state = device.state;
            if (device.deviceType === DeviceType.Strip) {
                this.hasChildren = true;
            } else {
                this.hasChildren = false;
            }
            this.children = [];
        }
    }

}

export class ChildDevice {
    host: string;
    deviceType: number;
    deviceId: string;
    alias: string;
    mac: string;
    state: boolean;

    constructor(device: SmartDeviceJSON) {
        if (device === undefined) {
            this.host = "192.168.1.207";
            this.deviceType = 1;
            this.deviceId = "8006E1AF7F5634FA56B4FD9131F313862053D3BE";
            this.alias = "Table";
            this.mac = "9C:A2:F4:0C:C5:96";
            this.state = false;
        } else {
            this.host = device.host;
            this.deviceType = device.deviceType;
            this.deviceId = device.deviceId;
            this.alias = device.alias;
            this.mac = device.mac;
            this.state = device.state;
        }
    }
}

enum DeviceType {
  Plug = 1,
  Bulb,
  Strip,
  StripSocket,
  Dimmer,
  LightStrip,
  Unknown = -1,
}

export type SmartDeviceJSON =  {
    host: string;
    deviceType: DeviceType;
    deviceId: string;
    alias: string;
    mac: string;
    state: boolean;
}

export async function findDevices() {
    let devices: SmartDeviceJSON[] = await fetchDevices();

    let smart_devices: SmartDevice[] = [];
    for (let i=0; i<devices.length; i++) {
        let dev = new SmartDevice(devices[i]);
        console.log(dev);
        if (dev.hasChildren) {
            dev.children = await getChildren(devices[i]);
        }
        smart_devices.push(dev);
    }
    return smart_devices;
}

async function fetchDevices() {
    let response = await fetch("http://localhost:8000/devices/", {"method": "GET"});

    const data = await response.json();

    if (response.ok) {
        if (data) {
            console.log(data);
            let devices: SmartDeviceJSON[] = data;
            return devices;
        } else {
            return Promise.reject(new Error(`No devices found`));
        }
    } else {
        return Promise.reject(new Error(`No response from server`))
    }
}

async function getChildren(parent: SmartDeviceJSON) {
    let devices = await fetchChildren(parent.host);
    console.log(devices);
    let children: ChildDevice[] = [];
    for (let i=0; i<devices.length; i++) {
        children.push(new ChildDevice(devices[i]));
    }
    return children;
}

async function fetchChildren(host: string) {
    let response = await fetch("http://localhost:8000/"+ host + "/children", {"method": "GET"});

    const data = await response.json();

    if (response.ok) {
        if (data) {
            console.log(data);
            let devices: SmartDeviceJSON[] = data;
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

export async function flipState(device: SmartDevice) {
    let response = await fetch(
        "http://localhost:8000/"+ device.host + "/?" + new URLSearchParams({"state": (!device.state).toString(),}), {"method": "POST"});

    const data = await response.json();

    return data;
}

export async function childFlipState(device: ChildDevice) {
    let response = await fetch(
        "http://localhost:8000/"+ device.host + "/children/" + device.deviceId +"/?" + new URLSearchParams({"state": (!device.state).toString(),}), {"method": "POST"});

    const data = await response.json();

    if (response.ok) {
        if (data) {
            console.log(data);
            let state: boolean = data;
            return state;
        } else {
            return Promise.reject(new Error(`Error changing device state: `, data));
        }
    } else {
        return Promise.reject(new Error(`No response from server`))
    }
}

export async function getDeviceState(device: SmartDevice) {
    let response = await fetch(
        "http://localhost:8000/"+ device.host, {"method": "GET"});

    const data = await response.json();

    if (response.ok) {
        if (data) {
            console.log(data);
            let dev: SmartDevice = data;
            return dev.state;
        } else {
            return Promise.reject(new Error(`Error: `, data));
        }
    } else {
        return Promise.reject(new Error(`No response from server`))
    }
}

export async function getChildDeviceState(device: ChildDevice) {
    let response = await fetch(
        "http://localhost:8000/"+ device.host + "/children/" + device.deviceId, {"method": "GET"});

    const data = await response.json();

    if (response.ok) {
        if (data) {
            console.log(data);
            let dev: ChildDevice = data;
            return dev.state;
        } else {
            return Promise.reject(new Error(`Error: `, data));
        }
    } else {
        return Promise.reject(new Error(`No response from server`))
    }
}