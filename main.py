from dataclasses import dataclass, asdict

import paho.mqtt.client as mqtt

from patterns import color_wipe, rainbow_cycle
from rpi_ws281x import PixelStrip
from utils import hex2rgb, rgb2hex, width_map, speed_map

# LED strip configuration:
LED_COUNT = 106  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

topics = {"active": "mqtt/LED/active",
          "pattern": "mqtt/LED/pattern",
          "colour": "mqtt/LED/colour",
          "speed": "mqtt/LED/speed",
          "width": "mqtt/LED/width"}


@dataclass(init=True)
class LEDparams:
    active: bool
    pattern: str
    colour: tuple
    speed: int
    width: int


def on_message(client, userdata, message):
    if message.topic == topics["active"]:
        lp.active = bool(int(message.payload.decode("utf-8")))
    elif message.topic == topics["pattern"]:
        lp.pattern = str(message.payload.decode("utf-8"))
    elif message.topic == topics["colour"]:
        lp.colour = hex2rgb(str(message.payload.decode("utf-8")))
    elif message.topic == topics["speed"]:
        lp.speed = speed_map(float((message.payload.decode("utf-8"))))
    elif message.topic == topics["width"]:
        lp.width = width_map(float((message.payload.decode("utf-8"))))
    print(asdict(lp))


if __name__ == '__main__':
    # Initialise LED strip
    lp = LEDparams(active=False, pattern="block", colour=(222, 142, 31), speed=60, width=50)
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    # Initialise MQTT client
    client = mqtt.Client(client_id="aw-pi-led")
    client.connect("aw-pi-broker")
    client.subscribe([(v, 0) for v in topics.values()])
    # TODO: add reset defaults function
    client.publish(topics["active"], int(lp.active))
    client.publish(topics["pattern"], lp.pattern)
    client.publish(topics["colour"], rgb2hex(lp.colour))
    client.publish(topics["speed"], lp.speed)
    client.publish(topics["width"], lp.width)
    client.on_message = on_message
    client.loop_start()

    # Write colours to LED strip
    while True:
        if lp.pattern == "rainbow" and lp.active:
            rainbow_cycle(strip, lp)
        elif lp.pattern == "block":
            color_wipe(strip, lp)
