from unicodedata import normalize

def clear_string(string: str) -> str:
    string = normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')  # Removendo acentuação
    string = ''.join(filter(isvalid, string))  # Removendo números e caracteres especiais
    return string

def isvalid(caracter: str):
    return True if caracter.isspace() else caracter.isalpha() and not caracter.isdigit()

def cypher(phrase: str, key: int):
    phrase = clear_string(phrase)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cipher = alphabet[key:len(alphabet)] + alphabet[0:key]
    cipher += cipher.lower()
    alphabet += alphabet.lower()
    result = ''
    for letter in phrase:
        result += cipher[alphabet.index(letter)] if letter != ' ' else ' '
    return result

def decypher(phrase: str, key: int):
    phrase = clear_string(phrase)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cipher = alphabet[key:len(alphabet)] + alphabet[0:key]
    cipher += cipher.lower()
    alphabet += alphabet.lower()
    result = ''
    for letter in phrase:
        result += alphabet[cipher.index(letter)] if letter != ' ' else ' '
    return result

if __name__ == "__main__":
    print('\033[1;36m', '-' * 26, 'Cifra de César'.center(26), '-' * 26, sep='\n')
    phrase = clear_string(input('\033[1;34mDigite a frase: \033[m'))
    key = int(input('\033[1;34mDigite o número da chave: \033[m'))
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cipher = alphabet[key:len(alphabet)] + alphabet[0:key]
    print('\033[1;35m', 'Alfabeto Cifrado'.center(26), '\033[0;35m'+cipher, cipher.lower()+'\033[m', sep='\n')
    cipher += cipher.lower()
    alphabet += alphabet.lower()
    result = ''
    loop = True
    switch = int(input('\033[1;34m\nEscolha:\n1.\033[0;34m Criptografar\n\033[1;34m2.\033[0;34m Descriptografar\n\033[m'))

    while loop:
        match switch:
            case 1:
                for letter in phrase:
                    result += cipher[alphabet.index(letter)] if letter != ' ' else ' '
                loop = False
                break
            case 2:
                for letter in phrase:
                    result += alphabet[cipher.index(letter)] if letter != ' ' else ' '
                loop = False
                break
            case _:
                print('\033[1;31mOpção Inválida!')
                print('\033[0;31mDigite um valor entre 0 e 3!\033[m')
                switch = int(input())
    print(f'\n\033[1;34mResultado: \033[0;32m{result}')
    binary = ''.join(b + ' ' for b in map(bin, bytearray(phrase, 'utf-8'))).replace('b', '')
    print(f'\n\033[1;34mResultado em binário: \033[0;32m{binary}\033[m')
