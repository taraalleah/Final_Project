import time
import config
import display
import encoder

#(Tara n JOs)
# import sampling
# import processing
# import storage
# import network


def run():
    display.show_message("HR Monitor is ready pals!")
    time.sleep(10)

    while True:
        choice = menu_screen()

        if choice == "measure":
            samples = measure_screen()
            hrv, ppi = analyze_screen(samples)
            next_step = result_screen(hrv)
            if next_step == "kubios":
                kubios_screen(ppi)

        elif choice == "history":
            history_screen()

        elif choice == "settings":
            settings_screen()


def menu_screen():
    selected = 0
    display.show_menu(config.MENU_ITEMS, selected)

    while True:
        rotation = encoder.get_rotation()
        if rotation != 0:
            selected = (selected + rotation) % len(config.MENU_ITEMS)
            display.show_menu(config.MENU_ITEMS, selected)

        if encoder.was_pressed():
            return config.MENU_ITEMS[selected].lower()

        time.sleep_ms(20)


def measure_screen():
    sampling.start_recording()
    start = time.time()
    last_update = 0

    display.show_measuring(None, 0)

    while True:
        elapsed = int(time.time() - start)

        if elapsed - last_update >= 5:
            bpm = processing.quick_bpm(sampling.samples)
            display.show_measuring(bpm, elapsed)
            if bpm:
                sampling.toggle_led()
            last_update = elapsed

        if encoder.was_pressed():
            sampling.stop_recording()
            return sampling.samples

        time.sleep_ms(20)


def analyze_screen(samples):
    display.show_analyzing()

    peaks = processing.find_peaks(samples)
    ppi = processing.peaks_to_ppi(peaks)
    hrv = processing.compute_hrv(ppi)

    if hrv:
        storage.save_session({
            "date": get_date(),
            "mean_hr": hrv["mean_hr"],
            "mean_ppi": hrv["mean_ppi"],
            "rmssd": hrv["rmssd"],
            "sdnn": hrv["sdnn"],
        })

    return hrv, ppi


def result_screen(hrv):
    display.show_result(hrv)

    while True:
        if encoder.get_rotation() != 0:
            return "menu"
        if encoder.was_pressed():
            return "kubios"
        time.sleep_ms(20)

#do we need to mention connecting to kubios, if yes:
# def kubios_screen(ppi):
# display.show_kubios_waiting()
# connected = network.connect_wifi()

# if not connected:
# display.show_message("Failed!")
# time.sleep(2)
# return

# result = network.send_to_kubios(ppi)
# display.show_kubios_result(result)

# while not encoder.was_pressed():
# time.sleep_ms(20)

# Scrollable history list. Press to see detail, press again to go back
def history_screen():
    sessions = storage.load_history()
    selected = 0
    display.show_history_list(sessions, selected)

    if not sessions:
        while not encoder.was_pressed():
            time.sleep_ms(20)
        return

    while True:
        rotation = encoder.get_rotation()
        if rotation != 0:
            selected = max(0, min(len(sessions) - 1, selected + rotation))
            display.show_history_list(sessions, selected)

        if encoder.was_pressed():
            display.show_history_detail(sessions[selected])
            while not encoder.was_pressed():
                time.sleep_ms(20)
            display.show_history_list(sessions, selected)

        # Scroll past last item to exit
        if selected >= len(sessions) - 1 and rotation > 0:
            return

        time.sleep_ms(20)


def settings_screen():
    # Settings screen with 4 options.
    # Scroll to highlight, press to select.
    # 0 = Font: Normal
    # 1 = Font: Large
    # 2 = Theme: Dark
    # 3 = Theme: Bright
    # Press on an already-selected option → goes back to menu.

    selected = 0
    display.show_settings(selected)

    while True:
        rotation = encoder.get_rotation()
        if rotation != 0:
            selected = (selected + rotation) % len(display.SETTINGS_OPTIONS)
            display.show_settings(selected)

        if encoder.was_pressed():
            apply_setting(selected)

            already_active = (
                    (selected == 0 and display.font_size == 1) or
                    (selected == 1 and display.font_size == 2) or
                    (selected == 2 and display.theme == "dark") or
                    (selected == 3 and display.theme == "bright")
            )
            if already_active:
                return

            display.show_settings(selected)

        time.sleep_ms(20)


def apply_setting(selected):
    if selected == 0:
        display.font_size = 1
        display.show_message("Font: Normal", "Applied!")

    elif selected == 1:
        display.font_size = 2
        display.show_message("Font: Large", "Applied!")

    elif selected == 2:
        display.theme = "dark"
        display.apply_theme()
        display.show_message("Theme: Dark", "Applied!")

    elif selected == 3:
        display.theme = "bright"
        display.apply_theme()
        display.show_message("Theme: Bright", "Applied!")

    time.sleep(1)


def get_date():
    try:
        from machine import RTC
        t = RTC().datetime()
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}".format(
            t[0], t[1], t[2], t[4], t[5])
    except:
        return "0000-00-00 00:00"
