import re


class TimeParser:

    time_pattern = re.compile(r"([0-9]+)([a-z]+)")

    @staticmethod
    def parse(time_param):

        result = TimeParser.time_pattern.match(time_param)

        if result is None:
            return None

        time_and_units = result.groups()
        time_val = float(time_and_units[0])
        time_units = time_and_units[1]

        return [time_val, time_units]
