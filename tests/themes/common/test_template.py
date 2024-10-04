import pytest

import matplotlib.pyplot as plt
from src.themes import Theme, Color, set_theme


@pytest.fixture
def template() -> Theme:
    default_red = Color("magenta", 231, 28, 87)
    default_green = Color("bright_green", 41, 186, 116)
    default_blue = Color("true_blue", 41, 94, 126)
    default_yellow = Color("yellow", 212, 223, 51)

    return Theme(
        name="test",
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
    )


class TestTheme:
    def test_continuous_cmap(self, template):
        assert isinstance(template.continuous_cmaps, dict)
        assert len(template.continuous_cmaps) > 0

    def test_continuous_reversed_cmap(self, template):
        assert isinstance(template.continuous_cmaps_reversed, dict)
        assert len(template.continuous_cmaps_reversed) == len(template.continuous_cmaps)

    def test_discrete_cmap(self, template):
        assert isinstance(template.discrete_cmaps, dict)
        assert len(template.discrete_cmaps) > 0

    def test_show(self, template):
        template.show()
        plt.close("all")


def test_set_theme_from_name():
    set_theme(theme="mpl-themes-green")


def test_set_theme_from_theme(template):
    set_theme(theme=template)


def test_wrong_theme():
    with pytest.raises(NotImplementedError):
        set_theme(theme="blabla")
