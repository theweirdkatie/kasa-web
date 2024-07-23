<script lang="ts">
    import { Button } from 'flowbite-svelte';
    import { LightBulb, MagnifyingGlass } from 'svelte-heros-v2';
    import DeviceList from '$lib/components/devicelist.svelte';
    import { onMount } from 'svelte'
	import { findDevices, SmartDevice } from '$lib/utils';

    let devices: SmartDevice[] = [];
    let db_devices: SmartDevice[] = [];
    let looking = false;

    onMount( async() => {
        await get_devices_db();
        devices = combine_devices(devices, db_devices);
    })

    $: if (devices.length >= 1) {
        console.log("devices changed, add to db");
        fetch('/api', {
            method: 'POST',
            body: JSON.stringify({ devices }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(resp => console.log(resp));
    }

    async function find_devices() {
        console.log("looking");
        looking = true;
        let new_devices = await findDevices();
        devices = combine_devices(devices, new_devices);
        console.log("devices:", devices);
        looking = false;
        console.log("done");
    }

    function combine_devices(current: SmartDevice[], found: SmartDevice[]): SmartDevice[] {
        for (const new_device of found) {
            // Check if the newItem already exists in currentArray
            const exists = current.some((item) => item.host === new_device.host); // Use isEqual function to compare objects
        
            if (!exists) {
                current.push(new_device);
            }
        }

        return current;
    }

    async function get_devices_db() {
        const response = await fetch('/api');

        if (response.ok) {
            let data = await response.json();
            if (data) {
                console.log(data);
                db_devices = data;
            } else {
                return new Error(`No devices found`);
            }
        } else {
            return new Error(`No response from server`)
        }
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
    <!-- <div class="col-start-2">
        <DeviceList smartdevices={db_devices} />
    </div> -->
</div>