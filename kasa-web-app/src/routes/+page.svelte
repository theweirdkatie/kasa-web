<script lang="ts">
    import { Button } from 'flowbite-svelte';
    import { LightBulb } from 'svelte-heros-v2';
    import SmartDevice from '../lib/smartdevice.svelte';

    // let bulb = new SmartDevice();
    let bulb = {
        alias: "Tank Lamp 1",
        state: true,
    };
    
</script>

<div class="flex place-content-center gap-4 mt-6">
    <Button>Find Devices</Button>
    <Button>Filter</Button>
</div>

<SmartDevice />