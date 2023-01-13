def set_field_generator(pow, list_of_components):
    generator = [0] * (pow + 1)
    for x in list_of_components:
        generator[x] = 1
    return ''.join(str(x) for x in generator)


generator = set_field_generator(233, [233, 9, 4, 1, 0])[::-1]
# print('field generator: ', generator)


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
    elif len(first_num) == len(second_num):
        for i in range(len(first_num) - 1, -1, -1):
            if first_num[i] == second_num[i]:
                pass
            elif int(first_num[i]) < int(second_num[i]):
                return -1
            elif int(first_num[i]) > int(second_num[i]):
                return 1

    return 0


def subtract_in_field(first_num, second_num):
    if first_num == '0' or second_num == '0':
        return second_num if first_num == 0 else first_num
    first_num, second_num = equalizes_lengths(first_num, second_num)
    # print('reversed first number: ', first_num)
    # print('reversed second number: ', second_num)
    difference = ''
    borrow = 0
    for digit1, digit2 in zip(first_num, second_num):
        temp = (int(digit1) - int(digit2) - borrow)
        # print(int(digit1), '-', int(digit2), '-', borrow, ' => temp=', temp)
        if temp >= 0:
            difference += str(temp)
            borrow = 0
        elif temp == -1 or temp == -2:
            difference += str(abs(temp) % 2)
            borrow = 1
    return remove_trailing_zeros(difference)


def divide_in_field(first_num, second_num):
    comparison = compare_in_field(first_num[::-1], second_num[::-1])
    if comparison == -1 or comparison == 0:
        return 0 if comparison == 0 else 0, first_num
    remainder = first_num
    length_divisor = len(second_num)
    quotient = [0] * (len(remainder) - length_divisor + 1)
    while compare_in_field(remainder[::-1], second_num[::-1]) != -1:
        k = len(remainder) - length_divisor
        sub_num = shift_left(second_num, k)
        if compare_in_field(remainder[::-1], sub_num[::-1]) == -1:
            sub_num = sub_num[:-1]
            k -= 1
        result_of_subtract = subtract_in_field(remainder[::-1], sub_num[::-1])[::-1]
        remainder = result_of_subtract
        quotient[k] = 1
    return (''.join(str(x) for x in quotient)), remainder


def modulo_in_field(num, generator):
    return divide_in_field(num, generator)[1][::-1]


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
    return summary


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
    return carry


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
    for x in range(0, pow - 1):
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


# first_num = '10011011101'
# second_num = '11010101'

# first_num = '111000011001101'
# second_num = '1001101111'

# first_num = '11100001111100010101110011010111110101011000'
# second_num = '1001101111000101011001101101001'

# print('shift left: ', first_num, '->', shift_left(first_num, 3))
# print('shift right: ', first_num, '->', shift_right(first_num, 3))
# print('compare: ', first_num, '?', c, '=', compare_in_field(first_num[::-1], c[::-1]))

first_num = '1110000111110001010111001101011111010101100000001000010110000110110101010011101001100111111011000100000010011011110001010110011011110000001100010100010101111100110010011001010100100111010100101'
second_num = '1001101111000101011001101101001000110001010000010111110011001001100101010010011101010010000011001'
power_num = '1001'

# summary = add_in_field(first_num[::-1], second_num[::-1])[::-1]
# print('addition: ', first_num, '+', second_num, '=', modulo_in_field(summary, generator)[::-1])
#
# product = multiply_in_field(first_num[::-1], second_num[::-1])[::-1]
# print('multiplication: ', first_num, '*', second_num, '=', modulo_in_field(product, generator)[::-1])
#
# square_product = square_in_field(first_num[::-1])[::-1]
# print('square: ', first_num, '** 2 =', modulo_in_field(square_product, generator)[::-1])
#
# # print('subtract: ', first_num, '-', second_num, '=', subtract_in_field(first_num[::-1], second_num[::-1])[::-1])
#
# quotient, remainder = divide_in_field(first_num, second_num)
# print('divide: ', first_num, '/', second_num, '= Q:', quotient[::-1], ', R:', remainder)
#
# power_product = power_in_field(first_num[::-1], power_num[::-1])[::-1]
# print('power: ', first_num, '^', power_num, '=', modulo_in_field(power_product, generator)[::-1])

#### TEST: (a + b) * c = a * c + c * b

a = '111000011001101'
b = '111000011001101'
c = '1001101111'
sum1_1 = add_in_field(a[::-1], b[::-1])[::-1]
prod1_1 = multiply_in_field(sum1_1[::-1], c[::-1])[::-1]

prod2_1 = multiply_in_field(a[::-1], c[::-1])[::-1]
prod2_2 = multiply_in_field(c[::-1], b[::-1])[::-1]
sum2_1 = add_in_field(prod2_1[::-1], prod2_2[::-1])[::-1]

print('TEST:', prod1_1, '=', sum2_1)
