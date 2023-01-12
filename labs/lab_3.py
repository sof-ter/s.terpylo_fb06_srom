def set_field_generator(pow, list_of_components):
    generator = [0] * (pow + 1)
    for x in list_of_components:
        generator[x] = 1
    return ''.join(str(x) for x in generator)


generator = set_field_generator(233, [233, 9, 4, 1, 0])
print('field generator: ', generator)


def shift_left(num, k):
    zeros = '0' * k
    num = num + zeros
    return num


def shift_right(num, k):
    zeros = '0' * k
    num = zeros + num
    return num


def remove_trailing_zeros(num):
    return num.rstrip('0')


def equalizes_lengths(first_num, second_num):
    if len(first_num) > len(second_num):
        while len(second_num) < len(first_num):
            second_num += '0'
    elif len(second_num) > len(first_num):
        while len(first_num) < len(second_num):
            first_num += '0'
    return first_num, second_num


def compare_in_field(first_num, second_num):
    if len(first_num) > len(second_num):
        return 1
    elif len(first_num) < len(second_num):
        return -1
    for i in range(len(first_num) - 1, -1, -1):
        if int(first_num[i]) < int(second_num[i]):
            return -1
        elif int(first_num[i]) > int(second_num[i]):
            return 1
    return 0


def subtract_in_field(first_num, second_num):
    if first_num == '0' or second_num == '0':
        return second_num if first_num == 0 else first_num
    first_num, second_num = equalizes_lengths(first_num, second_num)
    difference = ''
    borrow = 0
    for digit1, digit2 in zip(first_num, second_num):
        temp = int(digit1) - int(digit2) - borrow
        if temp >= 0:
            difference += str(abs(temp))
            borrow = 0
        else:
            difference += str(abs(temp))
            borrow = 1
    return remove_trailing_zeros(difference)


def divide_in_field(first_num, second_num):
    comparison = compare_in_field(first_num, second_num)
    if comparison == -1 or comparison == 0:
        return 0 if comparison == 0 else 0, first_num
    remainder = first_num
    length_divisor = len(second_num)
    quotient = ''
    while compare_in_field(remainder, second_num) != -1:
        sub_num = shift_left(second_num, len(remainder) - length_divisor)
        result_of_subtract = subtract_in_field(remainder[::-1], sub_num[::-1])[::-1]
        remainder = result_of_subtract
        quotient += '1'
    if compare_in_field(remainder, second_num) == -1:
        quotient += '0'
    return quotient, remainder


def modulo_in_field(num, generator):
    return divide_in_field(num, generator)[1]


def add_in_field(first_num, second_num):
    summary = ''
    carry = 0
    first_num, second_num = equalizes_lengths(first_num, second_num)
    if first_num == '0' or second_num == '0':
        return second_num if first_num == 0 else first_num
    for digit1, digit2 in zip(first_num, second_num):
        temp = int(digit1) + int(digit2) + carry
        sum_digit = temp % 2
        carry = temp // 2
        summary += str(sum_digit)
    if carry != 0:
        summary += str(carry)
    summary = modulo_in_field(summary[::-1], generator)
    return summary[::-1]


def multiply_in_field(first_num, second_num):
    if first_num == '0' or second_num == '0':
        return '0'
    if first_num == '1' or second_num == '1':
        return first_num if second_num == '1' else second_num
    first_num, second_num = equalizes_lengths(first_num, second_num)
    carry = '0'
    carry, first_num = equalizes_lengths(carry, first_num)
    n = 0
    for digit in range(len(second_num)):
        if second_num[digit] != '0':
            temp_mul = first_num
            temp_mul = shift_right(temp_mul, n)
            carry = add_in_field(carry, temp_mul)
        n += 1
    carry = modulo_in_field(carry[::-1], generator)
    return carry[::-1]


def square_in_field(num):
    return multiply_in_field(num, num)


def power_in_field(num, p):
    product = '1'
    for digit in range(len(p)):
        if p[digit] == '1':
            product = multiply_in_field(product, num)
        if digit != len(p) - 1:
            product = multiply_in_field(product, product)
    return product


def trace_in_field(num, pow):
    trace = num
    for x in range(0, pow-1):
        num = square_in_field(num)
        trace = add_in_field(trace, num)
    return trace


def inverse_in_field(num, pow):
    inverse = num
    for i in range(0, len(pow) - 2):
        num = square_in_field(num)
        inverse = multiply_in_field(inverse, num)
    inverse = square_in_field(inverse)
    return inverse


# first_num = '1101'
# second_num = '101'
second_num = '0001111101100011001100111010000110101010010100111010110011100011101101100000001111000011011101' \
             '1000010011000111100110110000101011000100101011000010010000110101101001000010010011110100100111' \
             '0111011111100011101010001110011011000010100011111110100010100000100111101000010000010010101110' \
             '0100110010001000110111100110100110000101001110100011101110110011011101010000100101111101011101' \
             '1101101110010001100001010100100100000110010010010011110010101011100001010101110011111100000111' \
             '10001101010111011010010001110001000001010110000110110001111111110'
first_num = '011100001111100010101110011010111110101011000000010000101100001101101010100111010011001111110' \
            '110001000000100110111100010101100110111100000011000101000101011111001100100110010101001001110' \
            '101001010101100011001011110100000010110010100110001011001111011111010010010111010001011111011' \
            '101100011110000001011111000110010110100000000101111000001001111001000010011010101111010111110' \
            '111110010010010011111000101110001100010110000110010011001111110011110100111001001000001110100' \
            '111001110110011011000100111101110101001100011000010001111011111011110111011010111111000100111' \
            '101101110100111110000010111000111001011110001001001001111001100100110010110001111000001011111' \
            '101111110000010001000000111011011100010100111101010111010100111010010011100110001110010010010' \
            '010101001110000011110100011001100100011111110011110011111101001000010110110111111010110011000' \
            '000110011100110111011010111101001101111011001001101011111000101000000010000111111100100011011' \
            '101000110111111110110110001110110100001011100100101010101111110101100010110'
# print('shift left: ', first_num, '->', shift_left(first_num, 3))
# print('shift right: ', first_num, '->', shift_right(first_num, 3))

print('addition: ', first_num, '+', second_num, '=', add_in_field(first_num[::-1], second_num[::-1])[::-1])
print('multiplication: ', first_num, '*', second_num, '=', multiply_in_field(first_num[::-1], second_num[::-1])[::-1])
print('square: ', first_num, '** 2 =', square_in_field(first_num[::-1])[::-1])
print('subtract: ', first_num, '-', second_num, '=', subtract_in_field(first_num[::-1], second_num[::-1])[::-1])
print('compare: ', first_num, '?', second_num, '=', compare_in_field(first_num[::-1], second_num[::-1]))
print('divide: ', first_num, '/', second_num, '=', divide_in_field(first_num, second_num))
print('power: ', first_num, '^', second_num, '=', power_in_field(first_num[::-1], second_num[::-1])[::-1])
