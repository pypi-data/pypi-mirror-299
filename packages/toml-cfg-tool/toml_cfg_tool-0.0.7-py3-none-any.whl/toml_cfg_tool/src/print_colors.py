from toml_cfg_tool.src.color_codes import END

def print_two_colors(color1, color2, text1, text2):
    text_one_length = len(text1)
    text_two_length = len(text2)
    dashes = "-" * text_one_length
    dashes_two = "-" * text_two_length
    print(f"{color1}{dashes}\n{text1}\n{dashes}\n{END}\n{color2}{dashes_two}\n{text2}\n{dashes_two}\n{END}\n")
