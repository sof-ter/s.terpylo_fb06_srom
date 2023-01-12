import time

hex_alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
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


def convert_to_hex(dec):
    digits = "0123456789ABCDEF"
    x = (dec % 16)
    rest = dec // 16
    if (rest == 0):
        return digits[x]
    return convert_to_hex(rest) + digits[x]


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
    num1 = num1[::-1]
    num2 = num2[::-1]
    carry = '0'
    carry, num1 = normalize(carry, num1)
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


def long_pow(num, p, hex_alphabet, base):  # error !!!!!!
    p = convert_to_binary(p)
    product = '1'
    for digit in range(len(p)):
        if p[digit] == '1':
            product = long_mul(product, num, hex_alphabet, base)
        if digit != len(p) - 1:
            product = long_mul(product, product, hex_alphabet, base)
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
    for i in range(len(num1) - 1, -1, -1):
        if hex_alphabet.index(num1[i]) < hex_alphabet.index(num2[i]):
            return -1
        elif hex_alphabet.index(num1[i]) > hex_alphabet.index(num2[i]):
            return 1
    return 0


def long_div(num1, num2, hex_alphabet, base):
    quotient = ''
    remainder = ''
    dividend = '' 
    if long_compare(num1, num2, hex_alphabet) == -1:
        remainder = num1
    else:
        if len(num2) >= 2:
            remainder = num1[: len(num2) - 1]

        for i in range(0, len(num1) - len(num2) + 1):
            temp_remainder = remainder
            dividend = temp_remainder + num1[i + len(num2) - 1]
            q_next = 0
            for j in range(base - 1, -1, -1):
                if j != 0:
                    mul_for_compare = long_mul(num2, hex_alphabet[j], hex_alphabet, base)
                    sub_for_compare = long_sub(dividend, mul_for_compare, hex_alphabet, base)
                    if sub_for_compare != 'error':
                        comparison = long_compare(sub_for_compare, dividend, hex_alphabet)
                        if comparison == -1 or comparison == 0:
                            q_next = j
                            break
            temp = long_mul(num2, hex_alphabet[q_next], hex_alphabet, base)
            remainder = long_sub(dividend, temp, hex_alphabet, base)
            # concat
            quotient = quotient + str(hex_alphabet[q_next])
    if remainder == '0':
        return [quotient.lstrip('0'), '0']
    else:
        return [quotient.lstrip('0'), remainder.lstrip('0')]


# LAB 2

def odd_or_not(num1, hex_alphabet, base):
    div_result = long_div(num1, '2', hex_alphabet, base)
    if div_result[1] == '':
        return True
    else:
        return False


def long_gcd(num1, num2, hex_alphabet, base):
    result = '1'
    while odd_or_not(num1, hex_alphabet, base) and odd_or_not(num2, hex_alphabet, base):
        num1 = long_div(num1, '2', hex_alphabet, base)[0]
        num2 = long_div(num2, '2', hex_alphabet, base)[0]
        result = long_mul(result, '2', hex_alphabet, base)
    while odd_or_not(num1, hex_alphabet, base) and not odd_or_not(num2, hex_alphabet, base):
        num1 = long_div(num1, '2', hex_alphabet, base)[0]
    while num2 != '0':
        while odd_or_not(num2, hex_alphabet, base):
            num2 = long_div(num2, '2', hex_alphabet, base)[0]
        if long_compare(num1, num2, hex_alphabet) == 1: # num1 > num2
            num1, num2 = num2, num1
        num2 = long_sub(num2, num1, hex_alphabet, base)
    result = long_mul(result, num1, hex_alphabet, base)
    return result.lstrip('0')


def long_lcm(num1, num2, hex_alphabet, base):
    mul_result = long_mul(num1, num2, hex_alphabet, base)
    gcd = long_gcd(num1, num2, hex_alphabet, base)
    div_result = long_div(mul_result, gcd, hex_alphabet, base)[0]
    return div_result


def barrett_reduction(num, mod, hex_alphabet, base):
    b_2k = long_pow('10', convert_to_hex(len(mod) * 2), hex_alphabet, base)
    mu = long_div(b_2k, mod, hex_alphabet, base)[0]
    k = len(mod)
    n_len = len(num)
    q = num[:n_len - k - 1]
    q = long_mul(q, mu, hex_alphabet, base)
    q = q[:len(q) - k + 1]
    r = long_mul(q, mod, hex_alphabet, base)
    r = long_sub(num, r, hex_alphabet, base)
    r = r.lstrip('0')
    while long_compare(r, mod, hex_alphabet) == 1:
        r = long_sub(r, mod, hex_alphabet, base)
    return r.lstrip('0')


def long_op_mod(num1, num2, mod, operation, hex_alphabet, base):
    op_result = ''
    if operation == 'add':
        op_result = long_add(num1, num2, hex_alphabet, base)
        print('sum: ', op_result)
    elif operation == 'sub':
        op_result = long_sub(num1, num2, hex_alphabet, base)
        print('dif: ', op_result)
    elif operation == 'mul':
        op_result = long_mul(num1, num2, hex_alphabet, base)
        print('mul: ', op_result)
    if op_result != 'error':
        mod_result = barrett_reduction(op_result, mod, hex_alphabet, base)
    else:
        mod_result = 'error'
    return mod_result


def long_pow_barret(num, p, mod, hex_alphabet, base):
    p = convert_to_binary(p)
    product = '1'
    for digit in range(len(p)):
        if p[digit] == '1':
            product = long_mul(product, num, hex_alphabet, base)
        if digit != len(p) - 1:
            product = long_mul(product, product, hex_alphabet, base)
        print('product = ', product)
        product = barrett_reduction(product, mod, hex_alphabet, base)
    return product

# x = 'A23B'
# y = '412'
# n = '1F'

# 512
x = 'DAF1ABDA4AD4D9FE3E36A529210C2AE99B905922FC0519798A26E351FE23AF375AD6BA288EE030B70DF0CE1CDF1E8B75BA56494DC6ED36B181814CD5783E6C81'
y = '4D3C91C579C2C6216567A5241614B561ADDF76C4BB659E6FE7F65FF76A918C843F0458B3EF457BCD9022D78798A29462EC99C74E6674690267D3E9844251B39D'
n = '170076B15F9575D21DE39D5C429799BBCDDB867016DE2248E3CFDE73A4D70C8636A9E41ABE671E7B9FB4739A5FF64DF9D0D3A64E0C9B20BFE58F1C62B28477EE9FD202010BAC440ADF3CA016A32DB844F23DEC2AB93AE869A6262FC23C5CE419807CDBA930A5433884E3B34B22477289BD3A7712CDD4B4110BD9887E7428FDF78703A1E982F278420C2D60CA7A0ED76C91855E3147B50357074A04EAF6515F07C1D8967674C7577D4112652E8135D145329F0DAE738F75C35004A154F1C43449DB87B6BE0F3EBF5B3BA1016F0A04A10C7EA76C3D30EEDB34B1E6E1009B3FF5C987FA313097485E6F8C78744E2F49DF62D13AD204E00F731BAE0E085C353D8D75'
# 1024
# x = ''
# y = '3A7EF2554E8940FA9B93B2A5E822CC7BB262F4A14159E4318CAE3ABF5AEB1022EC6D01DEFAB48B528868679D649B445A753684C13F6C3ADBAB059D635A2882090FC166EA9F0AAACD16A062149E4A0952F7FAAB14A0E9D3CB0BE9200DBD3B0342496421826919148E617AF1DB66978B1FCD28F8408506B79979CCBCC7F7E5FDE7'

# 2048
# x = '170076B15F9575D21DE39D5C429799BBCDDB867016DE2248E3CFDE73A4D70C8636A9E41ABE671E7B9FB4739A5FF64DF9D0D3A64E0C9B20BFE58F1C62B28477EE9FD202010BAC440ADF3CA016A32DB844F23DEC2AB93AE869A6262FC23C5CE419807CDBA930A5433884E3B34B22477289BD3A7712CDD4B4110BD9887E7428FDF78703A1E982F278420C2D60CA7A0ED76C91855E3147B50357074A04EAF6515F07C1D8967674C7577D4112652E8135D145329F0DAE738F75C35004A154F1C43449DB87B6BE0F3EBF5B3BA1016F0A04A10C7EA76C3D30EEDB34B1E6E1009B3FF5C987FA313097485E6F8C78744E2F49DF62D13AD204E00F731BAE0E085C353D8D75'
# y = '9D1C2D6E1591932F73C2F499C4E0A2E252DE828CDA7842CE0972C4101FE772B56C45C475EDDEDAEC2DBD13E375E02D2C149B69AB51FF3F94533CA34A815484EC86DACE936BDC62B5F3F9EB6F5BE6BD253E256181D35D7D63EE24459824D462C53676E3DFF98700415ADA65FDA7CBD3B3F359C817F52BEDA70C9DD85F68473C6B3CEBC5B7F698FF87B7BED132D299F68010583247B9C9792E809ED86C07B4D65C9E83AEE30897B0DAB7E5883EABE17B40B8F39267AC62377A6AFE0976AA0B81707282EB5FE59B66ED5EB1D3118CA3555F3AFCC28990AB016FE5B89D9159E6BB26151C923501F69629A0D75A6C06B8D0AA0364694DDCEDE35441E011347F85E621'
#
print('X = ', x, '\t', 'length of X-string = ', len(x))
print('Y = ', y, '\t', 'length of Y-string = ', len(y))
print('N = ', n, '\t', 'length of N-string = ', len(n), '\n')

# print("result of power func (there was error last time): ", long_pow(x, y, hex_alphabet, base))

# 1) обчислення НСД та НСК двох чисел;
# print('result of gcd: ', long_gcd(x, y, hex_alphabet, base))
# print('result of lcm: ', long_lcm(x, y, hex_alphabet, base))
# 2) додавання чисел за модулем;
# print('result of addition with mod: ', long_op_mod(x, y, n, 'add', hex_alphabet, base))
# # 3) віднімання чисел за модулем;
# print('result of substitution with mod: ', long_op_mod(x, y, n, 'sub', hex_alphabet, base))
# 4) множення чисел та піднесення чисел до квадрату за модулем;
# print('result of multiplication with mod: ', long_op_mod(x, y, n, 'mul', hex_alphabet, base))
# 5) піднесення числа до багаторозрядного степеня d по модулю n.
print('result of pow mod: ', long_pow_barret(x, y, n, hex_alphabet, base))

