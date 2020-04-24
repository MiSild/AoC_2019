def read_text_into_list(filename="input.txt"):
    with open(filename, 'r') as file:
        return file.readlines()


def write_to_file(text, filename="output.txt"):
    with open(filename, 'a') as file:
        file.write(text+"\n")