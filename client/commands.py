def is_command(text):

    return text.startswith("/")


def parse(text):

    return text.strip().split()