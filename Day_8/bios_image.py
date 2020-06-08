import file_helper

width = 25
length = 6
pixels_per_layer = width * length


def count_and_divide(numbers):
    layer_zeroes = []
    layers_themselves = []
    zeroes_count = 0
    row = 0
    row_count = 0
    current_layer = []
    current_row = []
    for i in numbers:
        current_row.append(i)
        row_count += 1
        if i == 0:
            zeroes_count += 1
        if row_count == width:
            row += 1
            current_layer.append(current_row)
            current_row = []
            row_count = 0
        if row == length:
            row = 0
            layers_themselves.append(current_layer)
            current_layer = []
            layer_zeroes.append(zeroes_count)
            zeroes_count = 0
    return layer_zeroes, layers_themselves


def find_min(layers_zeroes):
    value = float('inf')
    best_index = -1
    for i in range(len(layers_zeroes)):
        zero_count = layers_zeroes[i]
        if zero_count < value:
            value = zero_count
            best_index = i
    return best_index


def one_times_two_count(layer):
    one_count = 0
    two_count = 0
    for row in layer:
        for digit in row:
            if digit == 1:
                one_count += 1
            elif digit == 2:
                two_count += 1
    return one_count * two_count


def decode_layers(layers):
    final_layer = []
    number_of_layers = len(layers)
    for rows in range(length):
        row = []
        for columns in range(width):
            for layer_i in range(number_of_layers):
                pixel = layers[layer_i][rows][columns]
                if pixel in [0, 1]:
                    row.append(pixel)
                    break
        final_layer.append(row)
    return final_layer


if __name__ == '__main__':
    values = file_helper.read_text_into_list("input.txt")
    values = [int(x) for x in values[0].strip()]
    zeroes, layers = count_and_divide(values)
    layer_index = find_min(zeroes)
    one_times_two_counts = one_times_two_count(layers[layer_index])
    decoded_image = decode_layers(layers)