import re

# Embora que receba o CPF com pontos/traços, esta função remove e deixa apenas com números.
def only_numbers(cpf):
    return re.sub('[^0-9]','',cpf)

# função que irá calcular o primeiro dígito do CPF, assim também como irá verificar se não é uma sequencia de números repetidos.
def first_digit(cpf):
    cpf = only_numbers(cpf)
    sequency = cpf[0] * len(cpf)
    if sequency == cpf: # Verifica se o CPF é uma sequencia de números repetidos.
        return False
    else:
        slice = cpf[:9] # Como é informado um CPF completo, essa variavel pega somente os 9 primeiros digitos, para assim poder calcular o 10º digito.
        sum = 0
        for key, mult in enumerate(range(len(slice)+1, 1, -1)):
            sum+= int(slice[key]) * mult
        rest= 11 - sum%11
        rest = rest if rest<=9 else 0
        return slice+str(rest)

# Cria o ultimo digito do CPF e compara se realmente é igual ao informado.
def validate_cpf(cpf):
    if len(only_numbers(cpf)) != 11: # verifica se realmente contém os 11 dígitos necessários de um CPF.
        return False
    calculate_second_digit = first_digit(cpf) # armazena os 10 dígitos e começa a calcular o ultimo dígito do CPF
    if calculate_second_digit:
        sum= 0
        for key, mult in enumerate(range(len(calculate_second_digit)+1, 1, -1)):
            sum+= int(calculate_second_digit[key]) * mult
        rest= 11- sum%11
        rest = rest if rest<=9 else 0
        cpf_final = calculate_second_digit+str(rest)
        if cpf_final == only_numbers(cpf): # verificação se o CPF calculado realmente é igual ao passado como parâmetro.
            return cpf_final
        else:
            return False
    else:
        return False

# Verifica se o TIPO do produto foi passado de forma correta: A, B ou C.
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