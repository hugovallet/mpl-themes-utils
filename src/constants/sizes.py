from src.utils.plot import cm2inch

large = cm2inch(26.76, 10.01)
medium = cm2inch(21.85, 10.01)
small = cm2inch(17, 9.91)
half = cm2inch(12.85, 9.91)
two_third = cm2inch(17.00, 10.01)
one_third = cm2inch(9.69, 9.91)
one_third_spaced = cm2inch(8.76, 9.91)

size_names = [
    "large",
    "medium",
    "small",
    "half",
    "two_third",
    "one_third",
    "one_third_spaced",
]
SIZES = {name: eval(name) for name in size_names}
