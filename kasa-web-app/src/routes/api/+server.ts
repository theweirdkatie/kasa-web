import * as Db from '$lib/server/db';
import type { SmartDeviceJSON } from '$lib/utils';
import { SmartDevice } from '$lib/utils';

export async function GET({ request }: { request: Request }): Promise<Response> {
    console.log("get devices from db");
    try {
        const devices = await Db.getInitialDevices();
        return new Response(JSON.stringify(devices), { status: 200, statusText: 'Successfully retrieved devices' });
    } catch (error) {
        console.error('Error fetching devices:', error);
        return new Response(new Blob(), { status: 500, statusText: 'Failed to fetch devices'});
    }
}

export async function POST({ request }: { request: Request }): Promise<Response> {
    console.log("post devices to db");
    const data = await request.json();

    if (data) {
        let smart_devices: SmartDevice[] = [];
        for (let i=0; i<data.devices.length; i++) {
            let dev = new SmartDevice(data.devices[i]);
            smart_devices.push(dev);
        }
        try {
            await Db.insertNewDevices(smart_devices);
            return new Response(new Blob(), { status: 200, statusText: 'Devices inserted successfully' });
        } catch (error) {
            console.log(error);
            return new Response(JSON.stringify(error), { status: 500, statusText: 'Unable to insert devices into db' })
        }
    } else {
        return new Response(data, { status: 500, statusText: 'No devices supplied'});
    }
}