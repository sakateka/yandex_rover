from micropython import const

import machine
import asyncio
import aioble
import bluetooth

# Randomly generated UUIDs.
_YDR_SERVICE_UUID = bluetooth.UUID("caa33171-56ee-4169-b2a5-18bcb421740b")
_CONTROL_CHARACTERISTIC_UUID = bluetooth.UUID("9076b123-5d0c-4539-9504-ea623b673e20")

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000


_COMMAND_STOP = const(0)
_COMMAND_LEFT = const(1)
_COMMAND_RIGHT = const(2)
_COMMAND_FORWARD = const(3)
_COMMAND_BACK = const(4)
_COMMAND_LIGHT = const(5)

# Register GATT server.
service = aioble.Service(_YDR_SERVICE_UUID)
control_characteristic = aioble.Characteristic(
    service,
    _CONTROL_CHARACTERISTIC_UUID,
    write=True
)
aioble.register_services(service)

def setup_pwm(pin: int) -> machine.PWM:
    pass

led = machine.Pin(15, machine.Pin.OUT)
led.on()

async def control_task(connection):
    global send_file, recv_file, list_path

    try:
        with connection.timeout(None):
            while True:
                print("Waiting for write")
                await control_characteristic.written()
                msg = control_characteristic.read()
                print(msg)
                # control_characteristic.write(b"")

                command = msg[0]

                if command == _COMMAND_LEFT:
                    print("Turn left")
                elif command == _COMMAND_RIGHT:
                    print("Turn right")
                elif command == _COMMAND_FORWARD:
                    print("Run forward")
                elif command == _COMMAND_BACK:
                    print("Run back")
                elif command == _COMMAND_LIGHT:
                    print("Toggle light")
                    led.value(not led.value())
                elif command == _COMMAND_STOP:
                    print("Stop")
                else:
                    print("Unknown command: %s", command)
                    # TODO: stop && light off

    except aioble.DeviceDisconnectedError:
        print("Error device disconnected")
        return


# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():
    while True:
        print("Waiting for connection")
        connection = await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="Yandex Delivery Robot 01",
            services=[_YDR_SERVICE_UUID],
        )
        print("Connection from", connection.device)
        await control_task(connection)
        await connection.disconnected()

# Run both tasks.
async def main():
    await peripheral_task()


asyncio.run(main())
