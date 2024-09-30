from zlibsanitizer import sanitize


def replace_special_spaces(text, threshold=1.0):
    other = text.count('-') + text.count('_')
    spaces = text.count(' ')

    if not other:
        return text

    if spaces / other > threshold:
        return text

    return text.replace("-", " ").replace("_", " ")


def filename_tuning(text: str):
    print('🔵 filename_tuning: ')
    print(text)

    text = sanitize(text)
    print(text)

    text = replace_special_spaces(text)
    print(text)

    return text

