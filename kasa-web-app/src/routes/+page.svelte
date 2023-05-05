<script lang="ts">
    import { Button } from 'flowbite-svelte';
    import { LightBulb, MagnifyingGlass } from 'svelte-heros-v2';
    import DeviceList from '../lib/devicelist.svelte';
    import { findDevices, SmartDevice } from '../lib/smartdevices';

    // let bulb = new SmartDevice();
    let bulb = {
        alias: "Tank Lamp 1",
        state: true,
    };

    let devices: SmartDevice[] = [];
    let looking = false;

    async function find_devices() {
        console.log("looking");
        looking = true;
        devices = await findDevices();
        looking = false;
        console.log("done");
    }
    
</script>

<div class="w-full grid grid-cols-3 gap-3 pt-3.5">
    <div class="col-start-2">
        <Button on:click={find_devices} pill={true} color="light" class="!p-2 h-auto" size="xl"><MagnifyingGlass size="20"/></Button>
        <Button>Filter</Button>
    </div>
    <div class="col-start-2">
        <DeviceList smartdevices={devices} />
    </div>
</div>