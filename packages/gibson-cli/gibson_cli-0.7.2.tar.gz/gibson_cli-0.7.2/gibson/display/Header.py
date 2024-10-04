import gibson.core.Colors as Colors


class Header:
    def render(self, text, color=None):
        output = text if color is None else Colors.colorize(text, color)
        header = "+-----------------------------------------------------------------------------+\n"
        header += "| " + output + " " * (76 - len(text)) + "|\n"
        header += "+-----------------------------------------------------------------------------+"
        return header
