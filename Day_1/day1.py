import file_helper
import multiprocessing
import argparse
from numpy import array_split


def calculate_fuel(mass):
    return int(int(mass) / 3) - 2


def calculate_recursive_fuel(mass):
    mass = int(mass)
    if mass <= 0:
        return 0
    fuel = calculate_fuel(mass)
    fuel_extra = calculate_recursive_fuel(fuel)
    fuel += max(0, fuel_extra)
    return fuel


def compute_fuel_of_sublist(sublist):
    total_fuel = 0
    for mass in sublist:
        total_fuel += calculate_recursive_fuel(mass)
    return total_fuel


def compute_total_fuel(args):
    workers = args.workers
    input_name = args.input
    output_name = args.output
    lines = file_helper.read_text_into_list(input_name)
    sublists = array_split(lines, workers)

    pool = multiprocessing.Pool(workers)
    fuel = pool.map(compute_fuel_of_sublist, sublists)
    fuel_total = sum(fuel)
    file_helper.write_to_file("The total fuel needed is: "+str(fuel_total), output_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find the total fuel required")
    parser.add_argument('--workers', '-w',
                        default=4,
                        type=int,
                        help="Number of parallel processes to use")
    parser.add_argument('--output', '-o',
                        default="output.txt",
                        type=str,
                        help="Filename for the output")
    parser.add_argument('--input', '-i',
                        default="input.txt",
                        type=str,
                        help="Filename for the input")
    args = parser.parse_args()
    compute_total_fuel(args)