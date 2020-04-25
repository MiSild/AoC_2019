import file_helper


def prepend_zeroes(text: str, total_length):
    while len(text) < total_length:
        text = "0" + text
    return text


def get_a_b(input_list, index, parameter_modes):
    if int(parameter_modes[-2]):
        b = input_list[index + 2]
    else:
        b = input_list[int(input_list[index + 2])]
    if int(parameter_modes[-1]):
        a = input_list[index + 1]
    else:
        a = input_list[int(input_list[index + 1])]
    return int(a), int(b)


def addition_intcode(input_list, index, parameter_modes):
    parameter_modes = prepend_zeroes(parameter_modes, 2)
    a, b = get_a_b(input_list, index, parameter_modes)
    input_list[int(input_list[index + 3])] = a + b


def multiplication_intcode(input_list, index, parameter_modes):
    parameter_modes = prepend_zeroes(parameter_modes, 2)
    a, b = get_a_b(input_list, index, parameter_modes)
    input_list[int(input_list[index + 3])] = a * b


def input_intcode(input_list, index):
    to_input = int(input("Your integer input please: "))
    input_list[int(input_list[index + 1])] = to_input


def output_intcode(input_list, index, parameter_modes):
    parameter_modes = prepend_zeroes(parameter_modes, 1)
    if int(parameter_modes):
        return input_list[index + 1]
    else:
        return input_list[int(input_list[index + 1])]


def get_command_opcode(full_command):
    full_command = str(full_command)
    if len(full_command) == 1:
        return "", int(full_command)
    else:
        command = int(full_command[-2:])
        parameters = full_command[:-2]
        return parameters, command


def jump_if_true_intcode(input_list, index, parameter_modes):
    parameter_modes = prepend_zeroes(parameter_modes, 2)
    a, b = get_a_b(input_list, index, parameter_modes)
    if a != 0:
        return -index + b
    else:
        return 3


def jump_if_false_intcode(input_list, index, parameter_modes):
    parameter_modes = prepend_zeroes(parameter_modes, 2)
    a, b = get_a_b(input_list, index, parameter_modes)
    if a == 0:
        return -index + b
    else:
        return 3


def less_than_intcode(input_list, index, parameter_modes):
    parameter_modes = prepend_zeroes(parameter_modes, 2)
    a, b = get_a_b(input_list, index, parameter_modes)
    if a < b:
        input_list[int(input_list[index + 3])] = 1
    else:
        input_list[int(input_list[index + 3])] = 0


def equals_intcode(input_list, index, parameter_modes):
    parameter_modes = prepend_zeroes(parameter_modes, 2)
    a, b = get_a_b(input_list, index, parameter_modes)
    if a == b:
        input_list[int(input_list[index + 3])] = 1
    else:
        input_list[int(input_list[index + 3])] = 0


def run_intcode_instructions(input_list):
    index = 0
    while True:
        parameter_modes, opcode = get_command_opcode(input_list[index])
        if opcode == 1:
            addition_intcode(input_list, index, parameter_modes)
            index += 4
        elif opcode == 2:
            multiplication_intcode(input_list, index, parameter_modes)
            index += 4
        elif opcode == 3:
            input_intcode(input_list, index)
            index += 2
        elif opcode == 4:
            print(output_intcode(input_list, index, parameter_modes))
            index += 2
        elif opcode == 5:
            index_delta = jump_if_true_intcode(input_list, index, parameter_modes)
            index += index_delta
        elif opcode == 6:
            index_delta = jump_if_false_intcode(input_list, index, parameter_modes)
            index += index_delta
        elif opcode == 7:
            less_than_intcode(input_list, index, parameter_modes)
            index += 4
        elif opcode == 8:
            equals_intcode(input_list, index, parameter_modes)
            index += 4

        elif opcode == 99:
            return "Opcode 99: exiting!"
        else:
            raise ValueError("Incorrect instruction code found!", index, opcode)


if __name__ == "__main__":
    text = str.rstrip(file_helper.read_text_into_list("input.txt")[0])
    inputs = text.split(",")
    inputs = [x for x in inputs]
    dummy_input = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    print(run_intcode_instructions(inputs))