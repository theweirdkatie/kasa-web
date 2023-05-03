<script lang="ts">
    import { Button } from 'flowbite-svelte';
    import { LightBulb } from 'svelte-heros-v2';
    import DeviceList from '../lib/devicelist.svelte';
    // let bulb = new SmartDevice();
    let bulb = {
        alias: "Tank Lamp 1",
        state: true,
    };
    
</script>

<div class="w-full grid grid-cols-3 gap-3 pt-3.5">
    <div class="col-start-2 place-content-center">
        <Button>Find Devices</Button>
        <Button>Filter</Button>
    </div>
    <div class="col-start-2">
        <DeviceList />
    </div>
</div>