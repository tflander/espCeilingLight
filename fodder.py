
# TODO: we want to eventually check last startup time to test if power was cycled twice as a reset signal.
#  The reset would put the light in normal white light mode
def time_spike():
    print(utime.mktime(utime.localtime()) - utime.mktime((2021, 1, 4, 17, 40, 4, 0, 4)))

