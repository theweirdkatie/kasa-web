<script lang="ts">
    import { DeskLamp, Power, PowerSocketUs as Plug, LedStrip as Strip, LedStripVariant as LedStrip } from 'svelte-materialdesign-icons';
    import { Button, Card, List, Li, DescriptionList, Layout } from 'flowbite-svelte';
    import { ChildDevice, childFlipState, getChildDeviceState }from '$lib/utils';
    import { slide } from 'svelte/transition';
    import { onMount } from 'svelte';
    
    export let child_device: ChildDevice;
    let error = false;

    onMount( async() => {
        child_device.state = await getChildDeviceState(child_device);
    })

    async function flip_state() {
        // console.log("fn");
        child_device.state = await childFlipState(child_device);
    }

    let showData = false;

</script>

<Card size="lg">
    <!-- <div class="flex flex-row w-full" horizontal={true}> -->
    <div class="flex flex-row w-full">
        <div id="device1icon"><Button class="!p-0 bg-transparent hover:bg-transparent !text-gray-500 hover:text-gray-500 !focus:border-transparent !focus:ring-0" on:click="{e => {showData = !showData}}"><DeskLamp size="40"/></Button></div>
        <div class="px-5 w-full"><h1 class="text-2xl py-1">{child_device.alias}</h1></div>
        <div class="w-fit place-content-center"><Button on:click={flip_state} pill={true} outline={!child_device.state} class="!p-2 h-auto" size="xl"><Power /></Button></div>
    </div>
    {#if showData}
    <div transition:slide="{{duration: 600}}" class="grid grid-cols-2 mt-2 pt-2 gap-3 ml-3 border-t-2">
        <blockquote>
            <h3>IP Address</h3>
            <p class="text-sm">{child_device.host}</p>
        </blockquote>
        <blockquote>
            <h3>Device Type</h3>
            <div class="flex gap-2">
                <Plug />
                <p class="text-sm">{child_device.alias}</p>
            </div>
        </blockquote>
        <blockquote class="col-span-2">
            <h3>Device ID</h3>
            <p class="text-sm">{child_device.deviceId}</p>
        </blockquote>
    </div>
    {/if}
</Card>