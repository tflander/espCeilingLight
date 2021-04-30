import re


class TimeParser:

    time_pattern = re.compile(r"([0-9]+)([a-z]+)")

    @staticmethod
    def parse(time_param):

        result = TimeParser.time_pattern.match(time_param)

        if result is None:
            return None

        time_val = float(result.group(1))
        time_units = result.group(2)

        return [time_val, time_units]
