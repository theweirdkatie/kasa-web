<script lang="ts">
    import { Button } from 'flowbite-svelte';
    import { LightBulb, MagnifyingGlass } from 'svelte-heros-v2';
    import DeviceList from '$lib/components/devicelist.svelte';
    import * as SD from '$lib/utils';

    let devices: SmartDevice[] = [];
    let db_devices: SmartDevice[] = [];
    let looking = false;

    $: (devices) {
        await fetch({
            method: 'POST',
            body: JSON.stringify({ devices }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

    async function find_devices() {
        console.log("looking");
        looking = true;
        new_devices = await findDevices();
        devices = combineDevices(devices, new_devices);
        looking = false;
        console.log("done");
    }

    function combine_devices(current: SmartDevice[], found: SmartDevice[]) {
        for (const new_device of found) {
            // Check if the newItem already exists in currentArray
            const exists = current.some((item) => item.host === new_device.host); // Use isEqual function to compare objects
        
            if (!exists) {
                current.push(new_device);
            }
        }
    }

    function get_devices_db() {
        const response = await fetch('/devices');
		db_devices = await response.json();
    }
    
</script>

<div class="w-full grid grid-cols-3 gap-3 pt-3.5">
    <div class="col-start-2">
        <Button on:click={find_devices} pill={true} color="light" class="!p-2 h-auto" size="xl"><MagnifyingGlass size="20"/></Button>
        <Button on:click={get_devices_db}>Filter</Button>
    </div>
    <div class="col-start-2">
        <DeviceList smartdevices={devices} />
    </div>
    <div class="col-start-2">
        <DeviceList smartdevices={db_devices} />
    </div>
</div>