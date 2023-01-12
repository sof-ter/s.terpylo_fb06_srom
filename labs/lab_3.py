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
        temp = (int(digit1) - int(digit2) - borrow) % 2
        if temp >= 0:
            difference += str(temp)
            borrow = 0
        else:
            difference += str(temp)
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
second_num = '1001101111000101011001101101001000110001010000010111110011001001100101010010011101010010000011001'
first_num = '11100001111100010101110011010111110101011000000010000101100001101101010100111010011001111110110001' \
            '00000010011011110001010110011011110000001100010100010101111100110010011001010100100111010100101'
# print('shift left: ', first_num, '->', shift_left(first_num, 3))
# print('shift right: ', first_num, '->', shift_right(first_num, 3))

print('addition: ', first_num, '+', second_num, '=', add_in_field(first_num[::-1], second_num[::-1])[::-1])
print('multiplication: ', first_num, '*', second_num, '=', multiply_in_field(first_num[::-1], second_num[::-1])[::-1])
print('square: ', first_num, '** 2 =', square_in_field(first_num[::-1])[::-1])
print('subtract: ', first_num, '-', second_num, '=', subtract_in_field(first_num[::-1], second_num[::-1])[::-1])
print('compare: ', first_num, '?', second_num, '=', compare_in_field(first_num[::-1], second_num[::-1]))
print('divide: ', first_num, '/', second_num, '=', divide_in_field(first_num, second_num))
print('power: ', first_num, '^', second_num, '=', power_in_field(first_num[::-1], second_num[::-1])[::-1])
