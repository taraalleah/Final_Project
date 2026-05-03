import time
import config

oled = None
font_size = 1
theme = "dark"


def init(oled_object):
    global oled
    oled = oled_object


# Internal helpers

def clear():
    if theme == "bright":
        oled.fill(1)
    else:
        oled.fill(0)


def line(y):
    color = o if theme == "bright" else 1
    oled.hline(0, y, config.OLED_W, 1)


def text(words, x, y, color=None):
    if color is None:
        color = 0 if theme == "bright" else 1

    words = str(words)

    if font_size == 1:
        oled.text(words, x, y, color)

    else:
        import framebuf
        for i, char in enumerate(words):
            char_buf = bytearray(8)
            fb = framebuf.FrameBuffer(char_buf, 8, 8, framebuf.MONO_VLSB)
            fb.fill(0)
            fb.text(char, 0, 0, 1)

            for row in range(8):
                for col in range(8):
                    if fb.pixel(col, row):
                        px = x + i * 16 + col * 2
                        py = y + row * 2
                        oled.fill_rect(px, py, 2, 2, color)


def apply_theme():
    if theme == "bright":
        oled.invert(1)
    else:
        oled.invert(0)


def draw_heart(cx, cy, size=1, color=1):
    s = size

    # Left(top-left of heart)
    oled.fill_rect(cx - 3 * s, cy - 2 * s, 3 * s, 3 * s, color)
    oled.fill_rect(cx - 4 * s, cy - 1 * s, 4 * s, 2 * s, color)

    # Right(top-right of heart)
    oled.fill_rect(cx, cy - 2 * s, 3 * s, 3 * s, color)
    oled.fill_rect(cx, cy - 1 * s, 4 * s, 2 * s, color)

    # Wide middle
    oled.fill_rect(cx - 4 * s, cy, 8 * s, 2 * s, color)

    # Narrowing bottom rows → makes the pointed tip
    oled.fill_rect(cx - 3 * s, cy + 2 * s, 6 * s, 1 * s, color)
    oled.fill_rect(cx - 2 * s, cy + 3 * s, 4 * s, 1 * s, color)
    oled.fill_rect(cx - 1 * s, cy + 4 * s, 2 * s, 1 * s, color)


# When start

def show_start():
    clear()
    draw_heart(30, 22, size=2)  # big heart on the left

    text("Korva-", 68, 14)  # korvapuusti on the right side
    text("puusti", 68, 26)

    oled.show()
    time.sleep(5)


# When mesuring, there is a heart that will blink

heart_visible = True


def show_measuring(bpm, seconds):
    global heart_visible

    clear()
    text("Measuring...", 8, 0)
    line(10)

    if heart_visible:
        draw_heart(112, 3, size=1)  # bkinking heart
    heart_visible = not heart_visible

    # BPM number, big in the middle
    if bpm is None:
        text("---", 52, 24)
        text("Place finger", 8, 38)

    oled.show()


SETTINGS_OPTIONS = [
    "Font: Normal",
    "Font: Large",
    "Theme: Dark",
    "Theme: Bright",
]


def show_settings(selected):
    oled.fill(0)
    oled.text("SETTINGS", 24, 0, 1)
    oled.hline(0, 10, config.OLED_W, 1)

    for i, option in enumerate(SETTINGS_OPTIONS):
        y = 14 + i * 12
        is_active = (
                (i == 0 and font_size == 1) or
                (i == 1 and font_size == 2) or
                (i == 2 and theme == "dark") or
                (i == 3 and theme == "bright")
        )

        label = ("*" if is_active else " ") + option

        if i == selected:
            oled.fill_rect(0, y - 1, config.OLED_W, 11, 1)
            oled.text(label, 2, y, 0)
        else:
            oled.text(label, 2, y, 1)

    oled.show()


# Menu:
def show_menu(items, selected):
    clear()
    text("HR MONITOR", 16, 0)  # HR MONITOR biggest on top of the menu
    line(10)
    for i, name in enumerate(items):
        y = 14 + i * 13
        if i == selected:
            oled.fill_rect(0, y - 1, config.OLED_W, 12, 1)
            text("> " + name, 4, y, 0)
        else:
            text("  " + name, 4, y, 1)
    oled.show()


def show_analyzing():
    clear()
    text("broom broom", 16, 20)
    text("one momento :)", 20, 36)
    oled.show()


def show_result(hrv):
    clear()
    text("RESULT", 40, 0)
    line(10)
    if hrv is None:
        text("No valid data.", 4, 26)
        text("Try again.", 4, 40)
    else:
        text("HR:   " + str(int(hrv["mean_hr"])) + " bpm", 4, 14)
        text("PPI:  " + str(int(hrv["mean_ppi"])) + " ms", 4, 26)
        text("RMSS: " + str(int(hrv["rmssd"])) + " ms", 4, 38)
        text("SDNN: " + str(int(hrv["sdnn"])) + " ms", 4, 50)

    oled.show()


# optional to show while waiting for kubios?
# def show_kubios_waiting():
# clear()
# text("KUBIOS", 40, 0)
# line(10)
# text("Connecting...", 12, 26)
# oled.show()


# def show_kubios_result(data):
# clear()
# text("KUBIOS", 40, 0)
# line(10)
# if data is None:
# text("Failed to get", 8, 20)
# text("data from cloud.", 4, 34)
# else:
# text("HR:  " + str(round(data.get("mean_hr_bpm", 0), 1)), 4, 14)
# text("RMSS:" + str(round(data.get("rmssd", 0), 1)),        4, 26)
# text("SDNN:" + str(round(data.get("sdnn",  0), 1)),        4, 38)
# text("PNS: " + str(round(data.get("pns_index", 0), 2)),   4, 50)
# oled.show()

# history list
def show_history_list(sessions, selected):
    clear()
    text("HISTORY", 36, 0)
    line(10)
    if not sessions:
        text("No saves yet.", 12, 28)
        oled.show()
        return
    start = max(0, selected - 3)
    visible = sessions[start: start + 4]
    for i, s in enumerate(visible):
        real_index = start + i
        y = 14 + i * 12
        label = s.get("date", "??") + " " + str(int(s.get("mean_hr", 0))) + "b"
        if real_index == selected:
            oled.fill_rect(0, y - 1, config.OLED_W, 11, 1)
            text(label, 2, y, 0)
        else:
            text(label, 2, y, 1)
    oled.show()


def show_history_list(sessions, selected):
    clear()
    text("HISTORY", 36, 0)
    line(10)
    if not sessions:
        text("No saves yet.", 12, 28)
        oled.show()
        return
    start = max(0, selected - 3)
    visible = sessions[start: start + 4]
    for i, s in enumerate(visible):
        real_index = start + i
        y = 14 + i * 12
        label = s.get("date", "??") + " " + str(int(s.get("mean_hr", 0))) + "b"
        if real_index == selected:
            hi_color = 0 if theme == "bright" else 1
            oled.fill_rect(0, y - 1, config.OLED_W, 11, hi_color)
            text(label, 2, y, 1 - hi_color)
        else:
            text(label, 2, y)
    oled.show()


def show_history_detail(session):
    clear()
    text("SESSION", 36, 0)
    line(10)
    if session is None:
        text("Empty.", 4, 28)
        oled.show()
        return
    text(session.get("date", ""), 4, 14)
    text("HR:  " + str(int(session.get("mean_hr", 0))) + " bpm", 4, 28)
    text("RMSS:" + str(int(session.get("rmssd", 0))) + " ms", 4, 40)
    text("SDNN:" + str(int(session.get("sdnn", 0))) + " ms", 4, 52)
    oled.show()


def show_message(line1, line2=""):
    clear()
    text(line1, 4, 20)
    if line2:
        text(line2, 4, 36)
    oled.show()

