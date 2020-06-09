import file_helper


def find_asteroids(field):
    asteroids = []
    columns = len(field[0])
    for row in range(len(field)):
        for column in range(columns):
            if field[row][column] == "#":
                asteroids.append([row, column])
    return asteroids


def in_line_of_sight(asteroid_one, asteroid_two, field):
    x_delta = asteroid_two[1] - asteroid_one[1]
    y_delta = asteroid_two[0] - asteroid_one[0]
    if x_delta == 0:
        lowest_common = abs(y_delta)
    elif y_delta == 0:
        lowest_common = abs(x_delta)
    else:
        lowest_common = min(abs(x_delta), abs(y_delta))
    denominator = 1
    for i in range(lowest_common, 1, -1):
        if abs(x_delta) % i == 0 and abs(y_delta) % i == 0:
            denominator = i
            break
    for i in range(1, denominator):
        x_step = x_delta / denominator * i
        y_step = y_delta / denominator * i
        if field[int(asteroid_one[0] + y_step)][int(asteroid_one[1] + x_step)] == "#":
            return False
    return True


def detectable_from_asteroid(asteroid, asteroid_coordinates, field):
    detectable = 0
    for other_asteroid in asteroid_coordinates:
        if other_asteroid == asteroid:
            continue
        if in_line_of_sight(asteroid, other_asteroid, field):
            detectable += 1
    return detectable


def return_all_in_line_of_sight(asteroid, asteroid_coordinates, field):
    detectable = []
    for other_asteroid in asteroid_coordinates:
        if other_asteroid == asteroid:
            continue
        if in_line_of_sight(asteroid, other_asteroid, field):
            detectable.append(other_asteroid)
    return detectable


def find_most_detectable(field):
    asteroid_coordinates = find_asteroids(field)
    most_detectable = 0
    best_asteroid = []
    for asteroid in asteroid_coordinates:
        detectable = detectable_from_asteroid(asteroid, asteroid_coordinates, field)
        if detectable > most_detectable:
            most_detectable = detectable
            best_asteroid = asteroid
    return most_detectable, best_asteroid


def ascending_sort(relative_coordinates):
    x_rel = relative_coordinates[1]
    y_rel = relative_coordinates[0]
    if x_rel == 0:
        return float('inf')
    return abs(y_rel / x_rel)


def descending_sort(relative_coordinates):
    x_rel = relative_coordinates[1]
    y_rel = relative_coordinates[0]
    if x_rel == 0:
        return float('-inf')
    return -abs(y_rel / x_rel)


def set_in_order(detectable_asteroids, reference_point):
    quadrant_1 = []
    quadrant_2 = []
    quadrant_3 = []
    quadrant_4 = []
    for asteroid in detectable_asteroids:
        x_delta = asteroid[1] - reference_point[1]
        y_delta = reference_point[0] - asteroid[0]
        relative_cords = [y_delta, x_delta]
        if y_delta >= 0:
            if x_delta >= 0:
                quadrant_1.append(relative_cords)
            elif x_delta < 0:
                quadrant_4.append(relative_cords)
        elif y_delta < 0:
            if x_delta >= 0:
                quadrant_2.append(relative_cords)
            elif x_delta < 0:
                quadrant_3.append(relative_cords)
    quadrant_2.sort(key=ascending_sort)
    quadrant_4.sort(key=ascending_sort)
    quadrant_1.sort(key=descending_sort)
    quadrant_3.sort(key=descending_sort)
    return quadrant_1 + quadrant_2 + quadrant_3 + quadrant_4


def find_asteroid_two_hundreth(best_asteroid, field_matrix):
    asteroid_coordinates = find_asteroids(field_matrix)
    destroyed = 0
    last_destroyed = []
    destroyed_enough = False
    while not destroyed_enough:
        detectable = return_all_in_line_of_sight(best_asteroid, asteroid_coordinates, field_matrix)
        in_order_asteroids = set_in_order(detectable, best_asteroid)
        for destroyed_asteroid in in_order_asteroids:
            if destroyed == 200:
                destroyed_enough = True
                break
            destroyed_asteroid[0] = best_asteroid[0] - destroyed_asteroid[0]
            destroyed_asteroid[1] = destroyed_asteroid[1] + best_asteroid[1]
            field_matrix[destroyed_asteroid[0]] = \
                field_matrix[destroyed_asteroid[0]][:destroyed_asteroid[1]] + '.' + field_matrix[destroyed_asteroid[0]][destroyed_asteroid[1] + 1:]
            destroyed += 1
            last_destroyed = destroyed_asteroid

    return last_destroyed


if __name__ == '__main__':
    field_matrix = file_helper.read_text_into_list("input.txt")
    field_matrix = [str.rstrip(line) for line in field_matrix]
    dummy_map = [".#..#",
                 ".....",
                 "#####",
                 "....#",
                 "...##"]
    dummy_map_2 = ["......#.#.",
                   "#..#.#....",
                   "..#######.",
                   ".#.#.###..",
                   ".#..#.....",
                   "..#....#.#",
                   "#..#....#.",
                   ".##.#..###",
                   "##...#..#.",
                   ".#....####"]
    dummy_map_3 = [".#..##.###...#######",
                   "##.############..##.",
                   ".#.######.########.#",
                   ".###.#######.####.#.",
                   "#####.##.#.##.###.##",
                   "..#####..#.#########",
                   "####################",
                   "#.####....###.#.#.##",
                   "##.#################",
                   "#####.##.###..####..",
                   "..######..##.#######",
                   "####.##.####...##..#",
                   ".#####..#.######.###",
                   "##...#.##########...",
                   "#.##########.#######",
                   ".####.#.###.###.#.##",
                   "....##.##.###..#####",
                   ".#.#.###########.###",
                   "#.#.#.#####.####.###",
                   "###.##.####.##.#..##"]
    dummy_map_4 = [".#....#####...#..",
                   "##...##.#####..##",
                   "##...#...#.#####.",
                   "..#.....X...###..",
                   "..#.#.....#....##"]
    most_detected, best_asteroid = find_most_detectable(field_matrix)
    two_hundreth = find_asteroid_two_hundreth(best_asteroid, field_matrix)
