from __future__ import annotations
import file_helper


class Body:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None

    def set_parent(self, parent: Body):
        self.parent = parent

    def add_child(self, child: Body):
        self.children.append(child)

    def __hash__(self):
        return hash(self.name)


def get_or_create_orbit(dictionary: dict, body_name):
    if body_name in dictionary.keys():
        return dictionary[body_name]
    else:
        new_body = Body(body_name)
        dictionary[body_name] = new_body
        return new_body


def create_hash_orbits(all_orbits):
    orbit_dict = {}
    for orbit in all_orbits:
        parent_name = orbit[0]
        child_name = orbit[1]
        parent_body = get_or_create_orbit(orbit_dict, parent_name)
        child_body = get_or_create_orbit(orbit_dict, child_name)
        child_body.set_parent(parent_body)
        parent_body.add_child(child_body)
    return orbit_dict


def count_indirect_orbits(body):
    indirect_count = -1
    while body.parent is not None:
        indirect_count += 1
        body = body.parent
    return indirect_count


def count_orbits(all_bodies: dict):
    direct_orbit = 0
    indirect_orbit = 0
    for body in all_bodies.values():
        if body.parent is not None:
            direct_orbit += 1
            indirects = count_indirect_orbits(body)
            indirect_orbit += indirects
    return direct_orbit + indirect_orbit


def list_possible_transfers(body: Body, all_bodies: dict):
    transfers = []
    if body.parent is not None:
        transfers.append(body.parent.name)
    children = body.children
    for child in children:
        transfers.append(child.name)
    return transfers


def find_best_transfer(path_dict: dict, all_bodies: dict, current_body, destination_name):
    possibilities = list_possible_transfers(current_body, all_bodies)
    current_cost = path_dict[current_body.name]
    viable_possibilities = []  # Too lazy to use a heap
    for possibility in possibilities:
        if possibility in path_dict.keys():
            if path_dict[possibility] > current_cost + 1:
                path_dict[possibility] = current_cost + 1
                if possibility != destination_name:
                    viable_possibilities.append(possibility)
        else:
            path_dict[possibility] = current_cost + 1
            if possibility != destination_name:
                viable_possibilities.append(possibility)
    for viable in viable_possibilities:
        find_best_transfer(path_dict, all_bodies, all_bodies[viable], destination_name)


def find_min_orbits(all_bodies: dict):
    destination = all_bodies["SAN"].parent
    starting_point = all_bodies["YOU"].parent
    paths_dictionary = {starting_point.name: 0}
    find_best_transfer(paths_dictionary, all_bodies, starting_point, destination.name)
    return paths_dictionary[destination.name]


if __name__ == '__main__':
    lines = file_helper.read_text_into_list()
    orbits = [line.strip().split(")") for line in lines]
    orbit_dictionary = create_hash_orbits(orbits)
    # total_orbits = count_orbits(orbit_dictionary) Part 1
    minimum_transfers = find_min_orbits(orbit_dictionary)