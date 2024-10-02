# -*- coding=utf-8 -*-
r"""

"""
import enum
import typing as t


__all__ = ['StandardColors']


class StandardColors(enum.IntEnum):
    r"""
    collection of standard colors for the terminal
    """

    def __new__(cls, ansi_code: int, rgb: t.Tuple[int, int, int], hexadecimal: str) -> t.NoReturn:
        obj = int.__new__(cls, ansi_code)
        obj._value_ = ansi_code
        obj.ansi_code = ansi_code
        obj.rgb = rgb
        obj.hexadecimal = hexadecimal
        # normal color: 30fg/40bg | bright colors 90fg/100bg
        obj.escape_code_fg = f"\033[{(30 + ansi_code) if ansi_code < 0x8 else (82 + ansi_code)}m"
        obj.escape_code_bg = f"\033[{(40 + ansi_code) if ansi_code < 0x8 else (92 + ansi_code)}m"
        return obj

    BLACK           = 0x0, (0,   0,   0),   "#000000"
    RED             = 0x1, (204, 0,   0),   "#CC0000"
    GREEN           = 0x2, (78,  154, 6),   "#4E9A06"
    YELLOW          = 0x3, (196, 160, 0),   "#C4A000"
    BLUE            = 0x4, (114, 159, 207), "#729FCF"
    MAGENTA         = 0x5, (117, 80,  123), "#75507B"
    CYAN            = 0x6, (6,   152, 154), "#06989A"
    WHITE           = 0x7, (211, 215, 207), "#D3D7CF"
    BRIGHT_BLACK    = 0x8, (85,  87,  83),  "#555753"
    BRIGHT_RED      = 0x9, (239, 41,  41),  "#EF2929"
    BRIGHT_GREEN    = 0xA, (138, 226, 52),  "#8AE234"
    BRIGHT_YELLOW   = 0xB, (252, 233, 79),  "#FCE94F"
    BRIGHT_BLUE     = 0xC, (50,  175, 255), "#32AFFf"
    BRIGHT_MAGENTA  = 0xD, (173, 127, 168), "#AD7FA8"
    BRIGHT_CYAN     = 0xE, (52,  226, 226), "#34E2E2"
    BRIGHT_WHITE    = 0xF, (255, 255, 255), "#FFFFFF"
