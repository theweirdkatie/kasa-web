<script lang="ts">
    import { DeskLamp, Power } from 'svelte-materialdesign-icons';
    import { Button } from 'flowbite-svelte';

    class SmartDevice {
        host: string;
        deviceType: number;
        deviceId: string;
        name: string;
        alias: string;
        mac: string;
        hasChildren: bool;
        children: ChildDevice[];

        constructor() {
            this.host = "192.168.1.207";
            this.deviceType = 1;
            this.deviceId = "8006E1AF7F5634FA56B4FD9131F313862053D3BE";
            this.name = "Smart Wi-Fi Plug Mini";
            this.alias = "Tank Lamp 1";
            this.mac = "9C:A2:F4:0C:C5:96";
            this.hasChildren = false;
            this.children = [];
        }

    }

    class ChildDevice {
        id: string;
        alias: string;
    }

    let bulb = new SmartDevice();

    function flip_state() {
        // console.log("fn");
        bulb.state = !bulb.state;
    }

</script>

<div class="flex px-2 gap-2 pt-3.5 place-content-center" id="device1">
    <div class="flex-none w-20" id="device1icon"><DeskLamp size="50"/></div>
    <div class="flex-initial w-64 items-center"><span>{bulb.alias}</span></div>
    <div class="flex-initial w-32"><Button on:click={flip_state} pill={true} outline={!bulb.state} class="!p-2" size="xl"><Power /></Button></div>
</div>