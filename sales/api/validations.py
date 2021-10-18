import re


def only_numbers(cpf):
    return re.sub('[^0-9]','',cpf)

def first_digit(cpf):
    cpf = only_numbers(cpf)
    sequency = cpf[0] * len(cpf)
    if sequency == cpf:
        return False
    else:
        slice = cpf[:9]
        sum = 0
        for key, mult in enumerate(range(len(slice)+1, 1, -1)):
            sum+= int(slice[key]) * mult
        rest= 11 - sum%11
        rest = rest if rest<=9 else 0
        return slice+str(rest)

def validate_cpf(cpf):
    if len(only_numbers(cpf)) != 11:
        return False
    calculate_second_digit = first_digit(cpf)
    if calculate_second_digit:
        sum= 0
        for key, mult in enumerate(range(len(calculate_second_digit)+1, 1, -1)):
            sum+= int(calculate_second_digit[key]) * mult
        rest= 11- sum%11
        rest = rest if rest<=9 else 0
        cpf_final = calculate_second_digit+str(rest)
        if cpf_final == only_numbers(cpf):
            return cpf_final
        else:
            return False
    else:
        return False


def validate_type(type):
    if len(type)>1:
        return False
    verify = re.match('^[A-C]', type)
    if verify:
        return True
    else:
        return False

if __name__ == '__main__':
    # CPF's utilizados para teste, alguns gerados automaticamente por sites externos.
    # dado = validate_cpf('79529274942')
    # dado = validate_cpf('044.575.780-96')
    dado = validate_cpf('821.253.460-01')
    # dado = validate_cpf('111.111.111-11')

    dado2 = validate_type('A')
    if dado2:
        print(dado2)