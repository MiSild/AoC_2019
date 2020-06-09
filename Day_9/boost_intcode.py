import file_helper


class IntcodeComputer:
    def __init__(self):
        self.index = 0
        self.relative_base = 0

    def prepend_zeroes(self, text: str, total_length):
        while len(text) < total_length:
            text = "0" + text
        return text

    def get_a_b(self, input_list, parameter_modes):
        if int(parameter_modes[-2]) == 1:  # Mode 1, immediate mode
            b = input_list[self.index + 2]
        elif int(parameter_modes[-2]) == 0:  # Mode 0, relative mode
            b = input_list[int(input_list[self.index + 2])]
        elif int(parameter_modes[-2]) == 2:  # Mode 2, relative base mode
            b = input_list[self.relative_base + int(input_list[self.index + 2])]
        if int(parameter_modes[-1]) == 1:
            a = input_list[self.index + 1]
        elif int(parameter_modes[-1]) == 0:
            a = input_list[int(input_list[self.index + 1])]
        elif int(parameter_modes[-1]) == 2:
            a = input_list[self.relative_base + int(input_list[self.index + 1])]
        return int(a), int(b)

    def addition_intcode(self, input_list, parameter_modes):
        parameter_modes = self.prepend_zeroes(parameter_modes, 3)
        a, b = self.get_a_b(input_list, parameter_modes)
        if int(parameter_modes[-3]) == 2:
            input_list[int(input_list[self.index + 3]) + self.relative_base] = a + b
        else:
            input_list[int(input_list[self.index + 3])] = a + b

    def multiplication_intcode(self, input_list, parameter_modes):
        parameter_modes = self.prepend_zeroes(parameter_modes, 3)
        a, b = self.get_a_b(input_list, parameter_modes)
        if int(parameter_modes[-3]) == 2:
            input_list[int(input_list[self.index + 3]) + self.relative_base] = a * b
        else:
            input_list[int(input_list[self.index + 3])] = a * b

    def input_intcode(self, input_list, parameter_modes):
        parameter_modes = self.prepend_zeroes(parameter_modes, 1)
        if int(parameter_modes[0]) == 2:
            addition = self.relative_base
        else:
            addition = 0
        to_input = int(input("Your integer input please: "))
        input_list[int(input_list[self.index + 1]) + addition] = to_input

    def output_intcode(self, input_list, parameter_modes):
        parameter_modes = self.prepend_zeroes(parameter_modes, 1)
        if int(parameter_modes) == 1:
            return input_list[self.index + 1]
        elif int(parameter_modes) == 0:
            return input_list[int(input_list[self.index + 1])]
        elif int(parameter_modes) == 2:
            return input_list[self.relative_base + int(input_list[self.index + 1])]

    def get_command_opcode(self, full_command):
        full_command = str(full_command)
        if len(full_command) == 1:
            return "", int(full_command)
        else:
            command = int(full_command[-2:])
            parameters = full_command[:-2]
            return parameters, command

    def jump_if_true_intcode(self, input_list, parameter_modes):
        parameter_modes = self.prepend_zeroes(parameter_modes, 2)
        a, b = self.get_a_b(input_list, parameter_modes)
        if a != 0:
            return -self.index + b
        else:
            return 3

    def jump_if_false_intcode(self, input_list, parameter_modes):
        parameter_modes = self.prepend_zeroes(parameter_modes, 2)
        a, b = self.get_a_b(input_list, parameter_modes)
        if a == 0:
            return -self.index + b
        else:
            return 3

    def less_than_intcode(self, input_list, parameter_modes):
        parameter_modes = self.prepend_zeroes(parameter_modes, 3)
        a, b = self.get_a_b(input_list, parameter_modes)
        if int(parameter_modes[-3]) == 2:
            addition = self.relative_base
        else:
            addition = 0
        if a < b:
            input_list[int(input_list[self.index + 3]) + addition] = 1
        else:
            input_list[int(input_list[self.index + 3]) + addition] = 0

    def equals_intcode(self, input_list, parameter_modes):
        parameter_modes = self.prepend_zeroes(parameter_modes, 3)
        a, b = self.get_a_b(input_list, parameter_modes)
        if int(parameter_modes[-3]) == 2:
            addition = self.relative_base
        else:
            addition = 0
        if a == b:
            input_list[int(input_list[self.index + 3]) + addition] = 1
        else:
            input_list[int(input_list[self.index + 3]) + addition] = 0

    def adjust_relative_intcode(self, input_list, parameter_modes):
        parameter_modes = self.prepend_zeroes(parameter_modes, 1)
        if int(parameter_modes[0]) == 0:
            self.relative_base += int(input_list[int(input_list[self.index + 1])])
        elif int(parameter_modes[0]) == 1:
            self.relative_base += int(input_list[self.index + 1])
        elif int(parameter_modes[0]) == 2:
            self.relative_base += int(input_list[int(input_list[self.index + 1]) + self.relative_base])

    def increase_memory_size(self, input_list):
        [input_list.append(str(0)) for i in range(1000000)]

    def run_intcode_instructions(self, input_list):
        self.increase_memory_size(input_list)
        while True:
            parameter_modes, opcode = self.get_command_opcode(input_list[self.index])
            if opcode == 1:
                self.addition_intcode(input_list, parameter_modes)
                self.index += 4
            elif opcode == 2:
                self.multiplication_intcode(input_list, parameter_modes)
                self.index += 4
            elif opcode == 3:
                self.input_intcode(input_list, parameter_modes)
                self.index += 2
            elif opcode == 4:
                print(self.output_intcode(input_list, parameter_modes))
                self.index += 2
            elif opcode == 5:
                index_delta = self.jump_if_true_intcode(input_list, parameter_modes)
                self.index += index_delta
            elif opcode == 6:
                index_delta = self.jump_if_false_intcode(input_list, parameter_modes)
                self.index += index_delta
            elif opcode == 7:
                self.less_than_intcode(input_list, parameter_modes)
                self.index += 4
            elif opcode == 8:
                self.equals_intcode(input_list, parameter_modes)
                self.index += 4
            elif opcode == 9:
                self.adjust_relative_intcode(input_list, parameter_modes)
                self.index += 2
            elif opcode == 99:
                return "Opcode 99: exiting!"
            else:
                raise ValueError("Incorrect instruction code found!", self.index, opcode)


if __name__ == "__main__":
    text = str.rstrip(file_helper.read_text_into_list("input.txt")[0])
    inputs = text.split(",")
    inputs = [x for x in inputs]
    dummy_inputs = [109, 1, 203, 2, 204, 2, 99]
    computer = IntcodeComputer()
    print(computer.run_intcode_instructions(inputs))