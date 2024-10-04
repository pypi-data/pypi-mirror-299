from toml_cfg_tool.src.color_codes import END

def print_two_colors(color1, color2, text1, text2):
    text_one_length = len(text1)
    text_two_length = len(text2)
    dashes = "-" * text_one_length
    dashes_two = "-" * text_two_length
    # dash_text = dashes + "\n" + text1 + "\n" + dashes + "\n"
    dash_text = text1 + "\n"
    dash_text_two = dashes_two + "\n" + text2 + "\n" + dashes_two + "\n"
    colored_text = f"{color1}{dash_text}{END}"
    colored_text_two = f"{color2}{dash_text_two}{END}"
    print_message = colored_text + colored_text_two
    print(print_message)
