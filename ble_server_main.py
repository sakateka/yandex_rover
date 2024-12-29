from micropython import const

from machine import Pin, PWM
import asyncio
import aioble
import bluetooth

# Randomly generated UUIDs.
_YDR_SERVICE_UUID = bluetooth.UUID("caa33171-56ee-4169-b2a5-18bcb421740b")
_CONTROL_CHARACTERISTIC_UUID = bluetooth.UUID("9076b123-5d0c-4539-9504-ea623b673e20")

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = const(250_000)
_PWM_FREQ = const(20_000)
_PWM_DUTY = const(230)


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

def setup_pwm(pin: int) -> PWM:
    return PWM(Pin(pin), freq=_PWM_FREQ, duty_u16=0)

led = Pin(15, Pin.OUT)
led.on()

class Control():
    def __init__(self):
        self.leftFwd = setup_pwm(0)
        self.leftBack = setup_pwm(1)
        self.rightFwd = setup_pwm(2)
        self.rightBack = setup_pwm(3)
        self._light = Pin(4, Pin.OUT)
        self._light.value(0)

    def set_pwm(self, left_f=0, left_b=0, right_f=0, right_b=0):
        self.leftFwd.duty_u16(left_f)
        self.leftBack.duty_u16(left_b)
        self.rightFwd.duty_u16(right_f)
        self.rightBack.duty_u16(right_b)

    def turn_left(self):
        self.set_pwm(left_f=0, left_b=_PWM_DUTY, right_f=_PWM_DUTY, right_b=0)

    def turn_right(self):
        self.set_pwm(left_f=_PWM_DUTY, left_b=0, right_f=0, right_b=_PWM_DUTY)

    def go_forward(self):
        self.set_pwm(left_f=_PWM_DUTY, left_b=0, right_f=_PWM_DUTY, right_b=0)

    def go_back(self):
        self.set_pwm(left_f=0, left_b=_PWM_DUTY, right_f=0, right_b=_PWM_DUTY)

    def stop(self):
        self.set_pwm(left_f=0, left_b=0, right_f=0, right_b=0)

    def toggle_light(self):
        self._light.value(not self._light.value())

    def light_off(self):
        self._light.value(0)


async def control_task(control: Control, connection):
    global send_file, recv_file, list_path

    try:
        with connection.timeout(None):
            while True:
                print("Waiting for write")
                await control_characteristic.written()
                msg = control_characteristic.read()
                print("Received data", msg)
                # control_characteristic.write(b"")

                command = msg[0]

                if command == _COMMAND_LEFT:
                    print("Turn left")
                    control.turn_left()
                elif command == _COMMAND_RIGHT:
                    print("Turn right")
                    control.turn_right()
                elif command == _COMMAND_FORWARD:
                    print("Run forward")
                    control.go_forward()
                elif command == _COMMAND_BACK:
                    print("Run back")
                    control.go_back()
                elif command == _COMMAND_LIGHT:
                    print("Toggle light")
                    control.toggle_light()
                    led.value(not led.value())
                elif command == _COMMAND_STOP:
                    print("Stop")
                    control.stop()
                else:
                    print("Unknown command", command)
                    control.stop()
                    control.light_off()

    except aioble.DeviceDisconnectedError:
        print("Error device disconnected")
        return


# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():
    control = Control()
    while True:
        print("Waiting for connection")
        connection = await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="Yandex Delivery Robot 01",
            services=[_YDR_SERVICE_UUID],
        )
        print("Connection from", connection.device)
        await control_task(control, connection)
        await connection.disconnected()

# Run both tasks.
async def main():
    await peripheral_task()


asyncio.run(main())
