<script lang="ts">
    import { DeskLamp, Power } from 'svelte-materialdesign-icons';
    import { Button, AccordionItem } from 'flowbite-svelte';
    import { SmartDevice }from './smartdevices.ts';
    
    export let device: SmartDevice;

    function flip_state() {
        // console.log("fn");
        device.state = !device.state;
    }

</script>

<div id="device1icon"><DeskLamp size="50"/></div>
<div class="px-5 w-full"><h1 class="text-2xl py-2">{device.alias}</h1></div>
<div class="w-20"><Button on:click={flip_state} pill={true} outline={!device.state} class="!p-2" size="xl"><Power /></Button></div>