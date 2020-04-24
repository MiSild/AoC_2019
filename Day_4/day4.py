start_range = 357253
end_range = 892942


def has_adjacent(number):
    for i in range(len(number) - 1):
        if number[i] == number[i+1]:
            return True
    return False


def has_adjacent_only_pair(number):
    first = True
    for i in number:
        if first:
            current_digit = i
            first = False
            count = 0
            continue
        if i == current_digit:
            count += 1
        else:
            if count == 1:
                return True
            current_digit = i
            count = 0
    if count == 1:
        return True
    return False


def never_decreases(number):
    current_digit = int(number[0])
    for i in number:
        if int(i) < current_digit:
            return False
        else:
            current_digit = int(i)
    return True


def possible_password(number):
    return has_adjacent_only_pair(number) and never_decreases(number)


def count_possible_passwords():
    possible = 0
    for i in range(start_range, end_range + 1):
        if possible_password(str(i)):
            possible += 1
    return possible


if __name__ == "__main__":
    print(has_adjacent_only_pair("123444"))
    print(has_adjacent_only_pair("112233"))
    print(has_adjacent_only_pair("111122"))

    print(count_possible_passwords())