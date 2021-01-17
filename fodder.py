
def demo_modes():
    modes = LightingModes()
    modes.current_mode().activate()
    previous_mode = modes.current_mode()

    while True:
        mode = modes.next()
        for i in range(len(mode.modes)):
            previous_mode.deactivate()
            mode.activate()
            previous_mode = mode
            mode.next()
        if modes.current_mode_index == 0:
            return


async def first_simple_animation():
    print("starting animation")
    while True:
        led.duty(1023)
        await uasyncio.sleep_ms(100)
        led.duty(0)
        await uasyncio.sleep_ms(100)


def control_animation():
    while True:
        task = uasyncio.create_task(first_simple_animation())
        await uasyncio.sleep(2)
        task.cancel()
        led.duty(0)
        await uasyncio.sleep(2)


def doit():
    uasyncio.run(control_animation())


def two_buttons():
    while True:
        if led_touch_button.is_state_changed():
            if led_touch_button.state == TouchState.SELECTED:
                if led.duty() > 0:
                    led.duty(0)
                else:
                    led.duty(1023)
        if adjust_touch_button.is_state_changed():
            if adjust_touch_button.state == TouchState.SELECTED:
                if led.duty() > 0:
                    if led.duty() > 1000:
                        led.duty(512)
                    else:
                        led.duty(1023)
        utime.sleep_ms(20)


def activate_led_by_touch_latched():
    poll_for_touch_state_change(handle_latched_touch)


def activate_led_by_touch_momentary():
    poll_for_touch_state_change(handle_momentary_touch)


def handle_latched_touch():
    if led_touch_button.state == TouchState.SELECTED:
        if led.duty() > 0:
            led.duty(0)
        else:
            led.duty(1023)


def handle_momentary_touch():
    if led_touch_button.state == TouchState.SELECTED:
        led.duty(1023)
    elif led_touch_button.state == TouchState.RELEASED:
        led.duty(0)


def poll_for_touch_state_change(touch_handler):
    """

    :type touch_handler: function that takes no parameters and returns nothing
    """
    while True:
        if led_touch_button.is_state_changed():
            touch_handler()
        utime.sleep_ms(20)


# async def led_on(event):
#     await event.wait()
#     led.duty(1023)
#
#
# async def led_off(event):
#     await event.wait()
#     led.duty(0)


# async def toggle_led_with_uasyncio():
#
#     while True:
#         touch_selected_event = uasyncio.Event()
#         touch_release_event = uasyncio.Event()
#
#         led_on_task = uasyncio.create_task(led_on(touch_selected_event))
#         led_off_task = uasyncio.create_task(led_off(touch_release_event))
#
#         await uasyncio.sleep(1)
#         touch_selected_event.set()
#         await led_on_task
#
#         await uasyncio.sleep(1)
#         touch_release_event.set()
#         await led_off_task
#
# uasyncio.run(toggle_led_with_uasyncio())

# TODO: we want to eventually check last startup time to test if power was cycled twice as a reset signal.
#  The reset would put the light in normal white light mode
def time_spike():
    print(utime.mktime(utime.localtime()) - utime.mktime((2021, 1, 4, 17, 40, 4, 0, 4)))

# def test_thread():
#     while True:
#         print("Hello from thread")
#         utime.sleep(2)


# _thread.start_new_thread(testThread, ())
