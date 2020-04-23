import file_helper


def restore_1202_program_alarm(input_list):
    input_list[1] = 12
    input_list[2] = 2


def addition_intcode(input_list, index):
    input_list[input_list[index + 3]] = input_list[input_list[index + 1]] + input_list[input_list[index + 2]]


def multiplication_intcode(input_list, index):
    input_list[input_list[index + 3]] = input_list[input_list[index + 1]] * input_list[input_list[index + 2]]


def run_intcode_instructions(input_list):
    index = 0
    while True:
        command = input_list[index]
        if command == 1:
            addition_intcode(input_list, index)
        elif command == 2:
            multiplication_intcode(input_list, index)
        elif command == 99:
            print(input_list[0])
            break
        else:
            raise ValueError("Incorrect instruction code found!", index, command)
        index += 4


if __name__ == "__main__":
    text = str.rstrip(file_helper.read_text_into_list("input.txt")[0])
    inputs = text.split(",")
    inputs = [int(x) for x in inputs]
    mock_input = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    mock_input_2 = [1,1,1,4,99,5,6,0,99]
    restore_1202_program_alarm(inputs)
    run_intcode_instructions(inputs)
