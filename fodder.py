

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
