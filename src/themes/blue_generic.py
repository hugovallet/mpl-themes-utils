# # -*- coding: utf-8 -*-
from src.themes.common.template import Theme
from src.themes.common.colors import Color

default_red = Color("magenta", 231, 28, 87)
default_green = Color("green", 0, 191, 111)
default_blue = Color("blue", 44, 77, 142)
default_yellow = Color("gold", 250, 188, 21)

blue_generic_theme = Theme(
    name="mpl-themes-blue",
    background1=Color("white", 255, 255, 255),
    background2=Color("off_white", 242, 242, 242),
    text1=Color("gray", 134, 134, 134),
    text2=default_blue,
    accent1=Color("turquoise", 0, 172, 236),
    accent2=Color("lime", 206, 220, 0),
    accent3=default_yellow,
    accent4=Color("tan", 197, 183, 134),
    accent5=Color("teal", 0, 163, 173),
    accent6=default_green,
    default_blue=default_blue,
    default_green=default_green,
    default_yellow=default_yellow,
    default_red=default_red,
    font="Trebuchet MS",
    custom_colors=[default_red],
)
