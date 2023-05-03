<script>
    import Device from '../lib/smartdevice.svelte';
    import { Accordion, AccordionItem } from 'flowbite-svelte';
    import { SmartDevice } from './smartdevices.ts';
    import { Plus } from 'svelte-heros-v2';
    
    let bulb = new SmartDevice();

</script>

<Accordion multiple>
    <AccordionItem>
        <div slot="header" horizontal={true} class="flex flex-row px-2 gap-2 self-center w-full">
            <Plus size="50" class="px-2"/>
            <Device device={bulb}/>
        </div>
        <div slot="arrowup"></div>
        <div slot="arrowdown"></div>
    </AccordionItem>
</Accordion>