import time

from rpi_ws281x import Color


def color_wipe(strip, lp):
    """Wipe color across display a pixel at a time."""
    colour = tuple
    if lp.active:
        colour = Color(*lp.colour)
    else:
        colour = Color(0, 0, 0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, colour)
        strip.show()
        time.sleep(10 / 1000.0)
        if not lp.pattern == "block":
            break


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow_cycle(strip, lp, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(int(256 * iterations)):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels() * lp.width) + j) & 255))
        if not lp.active:
            [strip.setPixelColor(i, Color(0, 0, 0)) for i in range(strip.numPixels())]
            strip.show()
            break
        elif lp.pattern != "rainbow":
            break
        strip.show()
        time.sleep(lp.speed / 1000.0)


if __name__ == "__main__":
    pass
