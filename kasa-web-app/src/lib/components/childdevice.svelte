<script lang="ts">
    import { DeskLamp, Power, PowerSocketUs as Plug, LedStrip as Strip, LedStripVariant as LedStrip } from 'svelte-materialdesign-icons';
    import { Button, Card, List, Li, DescriptionList, Layout } from 'flowbite-svelte';
    import { ChildDevice, childFlipState }from '$lib/utils.ts';
    import { Plus } from 'svelte-heros-v2';
    import { slide } from 'svelte/transition';
    
    export let child_device: ChildDevice;
    let current_state = false;

    async function flip_state() {
        // console.log("fn");
        await childFlipState(child_device, current_state);
        current_state = !current_state;
    }

    let showData = false;

</script>

<Card size="lg">
    <div class="flex flex-row w-full" horizontal={true}>
        <div id="device1icon"><Button class="!p-0 bg-transparent hover:bg-transparent !text-gray-500 hover:text-gray-500 !focus:border-transparent !focus:ring-0" on:click="{e => {showData = !showData}}"><DeskLamp size="40"/></Button></div>
        <div class="px-5 w-full"><h1 class="text-2xl py-1">{child_device.alias}</h1></div>
        <div class="w-fit place-content-center"><Button on:click={flip_state} pill={true} outline={!current_state} class="!p-2 h-auto" size="xl"><Power /></Button></div>
    </div>
    {#if showData}
    <div transition:slide="{{duration: 600}}" class="grid grid-cols-2 mt-2 pt-2 gap-3 ml-3 border-t-2">
        <blockquote>
            <h3>MAC Address</h3>
            <p class="text-sm">{child_device.mac}</p>
        </blockquote>
        <blockquote>
            <h3>IP Address</h3>
            <p class="text-sm">{child_device.host}</p>
        </blockquote>
        <blockquote>
            <h3>Device Type</h3>
            <div class="flex gap-2">
            {#if child_device.deviceType === 1}
                <Plug />
            {:else if child_device.deviceType === 2}
                <Strip />
            {/if}
            <p class="text-sm">{child_device.name}</p></div>
        </blockquote>
        <blockquote class="col-span-2">
            <h3>Device ID</h3>
            <p class="text-sm">{child_device.deviceId}</p>
        </blockquote>
    </div>
    {/if}
</Card>