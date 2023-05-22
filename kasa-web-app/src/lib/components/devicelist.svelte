<script>
    import Device from '$lib/components/smartdevice.svelte';
    import { List, Li, Accordion, AccordionItem, Span } from 'flowbite-svelte';
    import { SmartDevice } from '$lib/utils.ts';
    
    let bulb = new SmartDevice();
    let bulb2 = new SmartDevice();
    bulb2.deviceType = 2;

    export let smartdevices = [bulb, bulb2];

</script>

{#each smartdevices as device}
    <Device device={device} />
    {#if device.hasChildren}
        {#each device.children as child}
            <Device device={child} />
        {/each}
    {/if}
{/each}