<script lang="ts">
    import { Button } from 'flowbite-svelte';
    import { LightBulb } from 'svelte-heros-v2';
    import DeviceList from '../lib/devicelist.svelte';
    import { findDevices } from '../lib/smartdevices';

    // let bulb = new SmartDevice();
    let bulb = {
        alias: "Tank Lamp 1",
        state: true,
    };

    let resp = "";
    let looking = false;

    async function find_devices() {
        console.log("looking");
        looking = true;
        resp = await findDevices();
        looking = false;
        console.log("done");
    }
    
</script>

<div class="w-full grid grid-cols-3 gap-3 pt-3.5">
    <div class="col-start-2 place-content-center">
        <Button on:click{find_devices}>Find Devices</Button>
        <Button>Filter</Button>
    </div>
    <div class="col-start-2">
        <p>{resp}</p>
    </div>
    <div class="col-start-2">
        <DeviceList />
    </div>
</div>