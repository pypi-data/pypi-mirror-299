from toml_cfg_tool.src.color_codes import END

def print_two_colors(color1, color2, text1, text2):
    print(f"{color1}{text1}{END}\n{color2}{text2}{END}")
