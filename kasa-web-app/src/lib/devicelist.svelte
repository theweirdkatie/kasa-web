<script>
    import Device from '../lib/smartdevice.svelte';
    import { List, Li, Accordion, AccordionItem, Span } from 'flowbite-svelte';
    import { SmartDevice } from './smartdevices.ts';
    import { Plus } from 'svelte-heros-v2';
    
    let bulb = new SmartDevice();
    let bulb2 = new SmartDevice();
    bulb2.deviceType = 2;

    let devices = [bulb, bulb2]

</script>

{#each devices as device}
    <Device device={device} />
{/each}