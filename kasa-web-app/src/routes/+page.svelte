<script lang="ts">
    import { Button } from 'flowbite-svelte';
    import { LightBulb } from 'svelte-heros-v2';
    import { DeskLamp } from 'svelte-materialdesign-icons';
    let deviceId = '8006D1848751AA826A0462EAF15DF43F2053448C'
    let requestData = "{\"system\":{\"set_relay_state\":{\"state\":1}}}"
    let params = {
        deviceId,
        requestData
    }

    let result = ""
    let _body = ""
    let device = ""
    let device_list = []

    async function httpRequest () {
        let method = 'passthrough'
        _body = JSON.stringify({
                        method,
                        params,
                    })
        const res = await fetch('https://use1-wap.tplinkcloud.com/?token=2519c0fa-ATYf4oe7VO8F05tljyAAK67', {
            method: 'POST',
            body: JSON.stringify({
                method,
                params,
            })
        })
            
        const json = await res.json()
        result = JSON.stringify(json)
    }

    async function getDevices () {
        let method = 'getDeviceList'
        _body = JSON.stringify({
                        method,
                    })
        const res = await fetch('https://wap.tplinkcloud.com?token=2519c0fa-ATYf4oe7VO8F05tljyAAK67', {
            method: 'POST',
            body: JSON.stringify({
                method,
            })
        })
            
        const json = await res.json()
        result = JSON.stringify(json)
        device_list = JSON.parse(result).result.deviceList
        device = device_list[4].alias
    }

</script>

<div class="flex place-content-center gap-4 mt-6">
    <Button>Find Devices</Button>
    <Button>Filter</Button>
</div>

<div class="flex px-2 gap-2 pt-3.5 place-content-center" id="device1">
    <div class="flex-none w-20" id="device1icon"><DeskLamp /></div>
    <div class="flex-initial w-64 bg-blue-600">02</div>
    <div class="flex-initial w-32 bg-green-700">03</div>
</div>