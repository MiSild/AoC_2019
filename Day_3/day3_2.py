import file_helper


class Coordinates:
    def __init__(self, x, y, a=0, b=0):
        self.x = x
        self.y = y
        self.distance = [a, b]

    def add_x(self, amount):
        self.x += amount

    def add_y(self, amount):
        self.y += amount

    def increment_distance(self, one):
        if one:
            self.distance[0] += 1
        else:
            self.distance[1] += 1

    def __hash__(self):
        return (str(self.x) + "," + str(self.y)).__hash__()

    def __copy__(self):
        return Coordinates(self.x, self.y, self.distance[0], self.distance[1])


def handle_move_results(current_point, visit_dictionary, first_wire, intersections):
    current_point.increment_distance(first_wire)
    if first_wire:
        if current_point.__hash__() not in visit_dictionary:
            visit_dictionary[current_point.__hash__()] = current_point.__copy__()
    else:
        try:
            if current_point.__hash__() in visit_dictionary:
                current_point.distance[0] = visit_dictionary[current_point.__hash__()].distance[0]
                intersections[current_point.__hash__()] = current_point.__copy__()
        except KeyError:
            pass


def move_up(length, visit_dictionary, current_point, first_wire):
    intersections = {}
    for i in range(length):
        current_point.add_y(1)
        handle_move_results(current_point, visit_dictionary, first_wire, intersections)
    return intersections


def move_down(length, visit_dictionary, current_point, first_wire):
    intersections = {}
    for i in range(length):
        current_point.add_y(-1)
        handle_move_results(current_point, visit_dictionary, first_wire, intersections)
    return intersections


def move_left(length, visit_dictionary, current_point, first_wire):
    intersections = {}
    for i in range(length):
        current_point.add_x(-1)
        handle_move_results(current_point, visit_dictionary, first_wire, intersections)
    return intersections


def move_right(length, visit_dictionary, current_point: Coordinates, first_wire):
    intersections = {}
    for i in range(length):
        current_point.add_x(1)
        handle_move_results(current_point, visit_dictionary, first_wire, intersections)
    return intersections


command_dict = {"U": move_up, "D": move_down, "L": move_left, "R": move_right}


def follow_instructions(instructions, visit_dictionary, first_wire):
    current_point = Coordinates(0, 0)
    intersections = {}
    for instruction in instructions:
        command = instruction[0]
        length = int(instruction[1:])
        if not first_wire:
            new_intersections = command_dict[command](length, visit_dictionary, current_point, first_wire)
            new_intersections.update(intersections)
            intersections.update(new_intersections)
        else:
            command_dict[command](length, visit_dictionary, current_point, first_wire)
    if not first_wire:
        return intersections


def smallest_distance_intersection(intersection_dict):
    smallest_distance = float('inf')
    for coordinate in intersection_dict.values():
        distance = coordinate.distance[0] + coordinate.distance[1]
        if distance < smallest_distance:
            smallest_distance = distance
    return smallest_distance


def smallest_manhattan_distance_coordinates(wire_1_instructions, wire_2_instructions):
    wire_1_visited = {}
    follow_instructions(wire_1_instructions, wire_1_visited, True)
    intersections = follow_instructions(wire_2_instructions, wire_1_visited, False)
    smallest_distance = smallest_distance_intersection(intersections)
    return smallest_distance


if __name__ == "__main__":
    lines = file_helper.read_text_into_list()
    wire_1 = lines[0].split(",")
    wire_2 = lines[1].split(",")
    print(smallest_manhattan_distance_coordinates(wire_1, wire_2))