from duties import Duties


class RgbDutiesConverter:

    @staticmethod
    def to_duties(rgb_string):
        if not RgbDutiesConverter.is_valid_color(rgb_string):
            raise ValueError
        duties = Duties()
        duties.red = int(rgb_string[1:3], 16) << 2
        duties.green = int(rgb_string[3:5], 16) << 2
        duties.blue = int(rgb_string[5:7], 16) << 2
        duties.white = min(duties.red, duties.green, duties.blue)
        duties.red -= duties.white
        duties.green -= duties.white
        duties.blue -= duties.white
        return duties

    @staticmethod
    def is_valid_color(color: str):
        if not color.startswith('#'):
            return False
        if len(color) != 7:
            return False

        hex_digits = set("0123456789abcdefABCDEF")
        hex_portion = color[1:]
        for char in hex_portion:
            if not (char in hex_digits):
                return False
        return True
