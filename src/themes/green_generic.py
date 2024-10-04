# # -*- coding: utf-8 -*-
from src.themes.common.template import Theme
from src.themes.common.colors import Color

default_red = Color("magenta", 231, 28, 87)
default_green = Color("bright_green", 41, 186, 116)
default_blue = Color("true_blue", 41, 94, 126)
default_yellow = Color("yellow", 212, 223, 51)

green_generic_theme = Theme(
    name="mpl-themes-green",
    background1=Color("white", 255, 255, 255),
    background2=Color("off_white", 242, 242, 242),
    text1=Color("dark_gray", 87, 87, 87),
    text2=default_green,
    accent1=Color("forest_green", 3, 82, 45),
    accent2=Color("jade_green", 25, 122, 86),
    accent3=default_yellow,
    accent4=Color("mint_green", 62, 173, 146),
    accent5=Color("medium_gray", 110, 111, 115),
    accent6=default_blue,
    default_blue=default_blue,
    default_green=default_green,
    default_yellow=default_yellow,
    default_red=default_red,
    font="Trebuchet MS",
    custom_colors=[
        Color("cranberry", 103, 15, 49),
        Color("dark_yellow", 168, 178, 28),
        Color("bright_blue", 48, 193, 215),
    ],
)
