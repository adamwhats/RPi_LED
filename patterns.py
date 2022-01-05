import time

from rpi_ws281x import Color


def color_wipe(strip, lp):
    """Wipe color across display a pixel at a time."""
    # Initialise
    colour = int
    i = 0
    if lp.active:
        colour = Color(*lp.colour)
    else:
        colour = Color(0, 0, 0)
    # Colour
    while i < strip.numPixels():
        strip.setPixelColor(i, colour)
        strip.show()
        time.sleep(10 / 1000.0)
        i += 1
        # Update on lp.active change
        if lp.active and colour != Color(*lp.colour):
            colour = Color(*lp.colour)
            i = 0
        if not lp.active and colour != Color(0, 0, 0):
            colour = Color(0, 0, 0)
            i = 0
        # Transition to rainbow pattern
        if lp.pattern == "rainbow" and lp.active:
            for i in range(strip.numPixels()):
                colour = wheel(int(i * 256 / strip.numPixels() * lp.width) & 255)
                strip.setPixelColor(i, colour)
                strip.show()
                time.sleep(10 / 1000.0)
            lp.fade = 255
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
    # Initialise
    frame_count = 0
    j = 0
    # Colour
    while j < int(256 * iterations):
        if frame_count % lp.speed == 0:
            for i in range(strip.numPixels()):
                colour = wheel((int(i * 256 / strip.numPixels() * lp.width) + j) & 255)
                strip.setPixelColor(i, colour)
            j += 1
        # Fade
        if lp.active:  # Fade on
            for i in range(strip.numPixels()):
                strip.setBrightness(int(lp.fade))
            lp.fade = min(lp.fade + 2, 255)
        elif not lp.active:  # Fade off
            for i in range(strip.numPixels()):
                strip.setBrightness(int(lp.fade))
            lp.fade = lp.fade - 2
            if lp.fade <= 0:  # Set to black
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(0, 0, 0))
                    strip.setBrightness(255)
                strip.show()
                break
        if lp.pattern != "rainbow":
            break
        strip.show()
        frame_count += 1
        time.sleep(0.001)


if __name__ == "__main__":
    pass
