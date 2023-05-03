export class SmartDevice {
    host: string;
    deviceType: number;
    deviceId: string;
    name: string;
    alias: string;
    mac: string;
    hasChildren: boolean;
    children: ChildDevice[];

    constructor() {
        this.host = "192.168.1.207";
        this.deviceType = 1;
        this.deviceId = "8006E1AF7F5634FA56B4FD9131F313862053D3BE";
        this.name = "Smart Wi-Fi Plug Mini";
        this.alias = "Table";
        this.mac = "9C:A2:F4:0C:C5:96";
        this.hasChildren = false;
        this.children = [];
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