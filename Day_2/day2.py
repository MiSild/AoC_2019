import file_helper
import multiprocessing


def restore_1202_program_alarm(input_list, noun, verb):
    input_list[1] = noun
    input_list[2] = verb


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
            return input_list[0]
        else:
            raise ValueError("Incorrect instruction code found!", index, command)
        index += 4


def find_noun_and_verb(desired_solution, starting_memory):
    for i in range(99):
        for j in range(99):
            copy_memory = starting_memory.copy()
            restore_1202_program_alarm(copy_memory, i, j)
            result = run_intcode_instructions(copy_memory)
            if result == desired_solution:
                return [i, j]


def final_result(desired_solution, starting_memory):
    noun_and_verb = find_noun_and_verb(desired_solution, starting_memory)
    return 100 * noun_and_verb[0] + noun_and_verb[1]

if __name__ == "__main__":
    text = str.rstrip(file_helper.read_text_into_list("input.txt")[0])
    inputs = text.split(",")
    inputs = [int(x) for x in inputs]
    mock_input = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    mock_input_2 = [1,1,1,4,99,5,6,0,99]
    restore_1202_program_alarm(inputs, 12, 2)
    #print(run_intcode_instructions(inputs))
    print(final_result(19690720, inputs))
