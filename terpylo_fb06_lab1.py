import time
import random

hex_alphabet = ['0', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
hex_binary_alphabet = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110',
                       '7': '0111', '8': '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101',
                       'E': '1110', 'F': '1111'}
base = 16


def normalize(num1, num2):
    if len(num1) > len(num2):
        while len(num2) < len(num1):
            num2 += '0'
    elif len(num2) > len(num1):
        while len(num1) < len(num2):
            num1 += '0'
    return num1, num2


def convert_to_binary(num):
    num = int(num, 16)
    bin_str = ''
    while num > 0:
        bin_str = str(num % 2) + bin_str
        num = num >> 1
    return bin_str


def long_add(num1, num2, hex_alphabet, base):
    summary = ''
    num1 = num1[::-1]
    num2 = num2[::-1]
    num1, num2 = normalize(num1, num2)
    carry = 0
    if num1 == 0:
        return num2
    if num2 == 0:
        return num1
    for digit1, digit2 in zip(num1, num2):
        temp = hex_alphabet.index(digit1) + hex_alphabet.index(digit2) + carry
        sum_digit = temp % base
        carry = temp // base
        summary += hex_alphabet[sum_digit]
    if carry != 0:
        summary += hex_alphabet[carry]
    return summary[::-1]


def long_sub(num1, num2, hex_alphabet, base):
    comparison = long_compare(num1, num2, hex_alphabet)
    if comparison == 1:
        difference = ''
        num1 = num1[::-1]
        num2 = num2[::-1]
        num1, num2 = normalize(num1, num2)
        borrow = 0
        for digit1, digit2 in zip(num1, num2):
            temp = hex_alphabet.index(digit1) - hex_alphabet.index(digit2) - borrow
            if temp >= 0:
                difference += hex_alphabet[temp]
                borrow = 0
            else:
                difference += hex_alphabet[temp]
                borrow = 1
        return difference[::-1]
    elif comparison == 0:
        return '0'
    else:
        return 'error'


def long_mul_one_digit(num, digit, hex_alphabet, base):
    product = ''
    carry = 0
    for d in range(len(num)):
        temp = int(hex_alphabet.index(num[d])) * int(digit) + carry
        p = temp % base
        carry = temp // base
        product += hex_alphabet[p]
    if carry != 0:
        product += hex_alphabet[carry]
    return product


def long_mul(num1, num2, hex_alphabet, base):
    product = ''
    num1 = num1[::-1]
    num2 = num2[::-1]
    n = 0
    carry = '0'
    carry, num1 = normalize(carry, num1)
    c = []
    for digit2 in range(len(num2)):
        temp_mul = long_mul_one_digit(num1, hex_alphabet.index(num2[digit2]), hex_alphabet, base)
        temp_mul = temp_mul[::-1]
        if digit2 != 0:
            n = 0
            while n != digit2:
                temp_mul += '0'
                n += 1
        carry = long_add(carry, temp_mul, hex_alphabet, base)
    return carry


def long_pow(num, p, hex_alphabet, base):
    product = '1'
    p = convert_to_binary(p)
    # p = p[::-1]
    if p == '1':
        return num
    if p == '0':
        return 1
    else:
        for digit in range(len(p)):
            if p[digit] == '1':
                product = long_mul(product, num, hex_alphabet, base)
            num = long_mul(num, num, hex_alphabet, base)
    return product


def long_compare(num1, num2, hex_alphabet):
    num1 = num1.lstrip('0')
    num2 = num2.lstrip('0')
    num1 = num1[::-1]
    num2 = num2[::-1]

    if len(num1) > len(num2):
        return 1
    elif len(num1) < len(num2):
        return -1
    for i in range(len(num1) -1, -1, -1):
        if hex_alphabet.index(num1[i]) < hex_alphabet.index(num2[i]):
            return -1
        elif hex_alphabet.index(num1[i]) > hex_alphabet.index(num2[i]):
            return 1
    return 0


def long_div(num1, num2, hex_alphabet, base):
    quotient = ''
    remainder = ''
    dividend = ''  # intermediate dividend

    if long_compare(num1, num2, hex_alphabet) == -1:
        # if divisor is greater than dividend,then remainder will be equal to dividend and quotient will be zero
        remainder = num1

    else:
        # initializing the intermediate remainder, then begin iterating
        if len(num2) >= 2:
            # because most significant digits is in the end
            # remainder = num1[- len(num2) + 1:]
            remainder = num1[: len(num2) - 1]

        for i in range(0, len(num1) - len(num2) + 1):
            # add the next digit of the dividend to the intermediate dividend
            temp_remainder = remainder
            # temp_remainder = remainder
            # print("temp remainder: ", temp_remainder)
            # to intermediate dividend concatenating next digit of the divisor
            # dividend = num1[-i-len(num2)] + temp_remainder
            dividend = temp_remainder + num1[i + len(num2) - 1]
            # print("intermediate dividend: ", dividend)
            # find next digit of the quotient using binary search
            # the next digit of the quotient is  the greatest multiple of the divisor less than
            # intermediate dividend
            q_next = 0
            # create a binary search
            for j in range(base - 1, -1, -1):
                if j != 0:
                    # print("j => ", j)
                    mul_for_compare = long_mul(num2, hex_alphabet[j], hex_alphabet, base)
                    # print("num2 * j => ", num2, " * ", j, " = ", mul_for_compare)
                    sub_for_compare = long_sub(dividend, mul_for_compare, hex_alphabet, base)
                    # print("dividend - mul_for_compare => ", dividend, " - ", mul_for_compare, " = ", sub_for_compare)
                    if sub_for_compare != 'error':
                        comparison = long_compare(sub_for_compare, dividend, hex_alphabet)
                        # print("sub_for_compare ? num2 ", sub_for_compare, " ? ", num2, " = ", comparison)
                        if comparison == -1 or comparison == 0:
                            q_next = j
                            break
            # print("next quotient digit: ", q_next)
            temp = long_mul(num2, hex_alphabet[q_next], hex_alphabet, base)
            remainder = long_sub(dividend, temp, hex_alphabet, base)
            # concat
            quotient = quotient + str(hex_alphabet[q_next])

    return quotient.lstrip('0'), remainder.lstrip('0')


# x = '4676A'
# y = 'A3453'

# 512
# x = '4D3C91C579C2C6216567A5241614B561ADDF76C4BB659E6FE7F65FF76A918C843F0458B3EF457BCD9022D78798A29462EC99C74E6674690267D3E9844251B39D'
# y = 'DAF1ABDA4AD4D9FE3E36A529210C2AE99B905922FC0519798A26E351FE23AF375AD6BA288EE030B70DF0CE1CDF1E8B75BA56494DC6ED36B181814CD5783E6C81'

# 1024
# x = 'D4D2110984907B5625309D956521BAB4157B8B1ECE04043249A3D379AC112E5B9AF44E721E148D88A942744CF56A06B92D28A0DB950FE4CED2B41A0BD38BCE7D0BE1055CF5DE38F2A588C2C9A79A75011058C320A7B661C6CE1C36C7D870758307E5D2CF07D9B6E8D529779B6B2910DD17B6766A7EFEE215A98CAC300F2827DB'
# y = '3A7EF2554E8940FA9B93B2A5E822CC7BB262F4A14159E4318CAE3ABF5AEB1022EC6D01DEFAB48B528868679D649B445A753684C13F6C3ADBAB059D635A2882090FC166EA9F0AAACD16A062149E4A0952F7FAAB14A0E9D3CB0BE9200DBD3B0342496421826919148E617AF1DB66978B1FCD28F8408506B79979CCBCC7F7E5FDE7'

# 2048
x = '170076B15F9575D21DE39D5C429799BBCDDB867016DE2248E3CFDE73A4D70C8636A9E41ABE671E7B9FB4739A5FF64DF9D0D3A64E0C9B20BFE58F1C62B28477EE9FD202010BAC440ADF3CA016A32DB844F23DEC2AB93AE869A6262FC23C5CE419807CDBA930A5433884E3B34B22477289BD3A7712CDD4B4110BD9887E7428FDF78703A1E982F278420C2D60CA7A0ED76C91855E3147B50357074A04EAF6515F07C1D8967674C7577D4112652E8135D145329F0DAE738F75C35004A154F1C43449DB87B6BE0F3EBF5B3BA1016F0A04A10C7EA76C3D30EEDB34B1E6E1009B3FF5C987FA313097485E6F8C78744E2F49DF62D13AD204E00F731BAE0E085C353D8D75'
y = '9D1C2D6E1591932F73C2F499C4E0A2E252DE828CDA7842CE0972C4101FE772B56C45C475EDDEDAEC2DBD13E375E02D2C149B69AB51FF3F94533CA34A815484EC86DACE936BDC62B5F3F9EB6F5BE6BD253E256181D35D7D63EE24459824D462C53676E3DFF98700415ADA65FDA7CBD3B3F359C817F52BEDA70C9DD85F68473C6B3CEBC5B7F698FF87B7BED132D299F68010583247B9C9792E809ED86C07B4D65C9E83AEE30897B0DAB7E5883EABE17B40B8F39267AC62377A6AFE0976AA0B81707282EB5FE59B66ED5EB1D3118CA3555F3AFCC28990AB016FE5B89D9159E6BB26151C923501F69629A0D75A6C06B8D0AA0364694DDCEDE35441E011347F85E621'

print('X = ', x, '\n', 'length of X-string = ', len(x))
print('Y = ', y, '\n', 'length of Y-string = ', len(y), '\n')

t_add_start = time.process_time()
print('result of add: ', long_add(x, y, hex_alphabet, base))
t_add_finish = time.process_time()
t_add_all = t_add_finish - t_add_start
print('time for add func => ', t_add_all, '\n')

t_sub_start = time.process_time()
print('result of sub: ', long_sub(x, y, hex_alphabet, base))
t_sub_finish = time.process_time()
t_sub_all = t_sub_finish - t_sub_start
print('time for sub func => ', t_sub_all, '\n')

t_mul_start = time.process_time()
mul_res = long_mul(x, y, hex_alphabet, base)
print('result of mul: ', mul_res)
t_mul_finish = time.process_time()
t_mul_all = t_mul_finish - t_mul_start
print('time for mul func => ', t_mul_all, '\n')

t_div_start = time.process_time()
print('result of div: ', long_div(x, y, hex_alphabet, base))
t_div_finish = time.process_time()
t_div_all = t_div_finish - t_div_start
print('time for div func => ', t_div_all, '\n')

t_mul_div_start = time.process_time()
print('result of mul-div: ', long_div(mul_res, y, hex_alphabet, base))
t_mul_div_finish = time.process_time()
t_mul_div_all = t_mul_div_finish - t_mul_div_start
print('time for mul-div func => ', t_div_all, '\n')

# t_pow_start = time.process_time()
# print("result of pow: ", long_pow(x, y, hex_alphabet, base))
# t_pow_finish = time.process_time()
# t_pow_all = t_pow_finish - t_pow_start
# print("time for pow func => ", t_pow_all, "\n")




