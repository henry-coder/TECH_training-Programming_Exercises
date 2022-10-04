import MySQLdb as db
from requests import get

def save_breeds(quantity: int):
    response = get(f'https://api.thedogapi.com/v1/breeds?limit={quantity}').json()
    sql = 'INSERT INTO Breeds (Breed) VALUES '
    for dog in response:
        sql += f"('{dog['name']}'),"
    cur.execute(sql[:-1])
    con.commit()

def save_facts(quantity: int):
    response = get(f'http://dog-api.kinduff.com/api/facts?number={quantity}').json()
    facts = response['facts']
    cur.execute('SELECT * FROM Breeds')
    breeds = cur.fetchall()
    sql = 'INSERT INTO Facts(Fact, Breed) VALUES '
    for fact in facts:
        fact = fact.replace('"', "'")
        for breed in breeds:
            if breed[1] in fact:
                cur.execute('SELECT Fact, Breed FROM Facts')
                table_facts = cur.fetchall()
                fact = (fact, breed[0])
                if fact not in table_facts:
                    sql += f'("{fact[0]}", {fact[1]}),'
    cur.execute(sql[:-1])
    con.commit()

def get_facts():
    sql = 'SELECT Breeds.Breed, Facts.Fact FROM Facts JOIN Breeds ON Facts.Breed = Breeds.CodBreed ORDER BY Breeds.Breed'
    cur.execute(sql)
    return cur.fetchall()

def get_breeds():
    sql = 'SELECT Breed, COUNT(Breed) FROM (SELECT Breeds.Breed, Facts.Fact FROM Facts JOIN Breeds ON Facts.Breed = Breeds.CodBreed ORDER BY Breeds.Breed) BF GROUP BY Breed'
    cur.execute(sql)
    return cur.fetchall()

def search_breed(breed: str):
    sql = f"SELECT Facts.Fact FROM Facts JOIN Breeds ON Facts.Breed = Breeds.CodBreed AND Breeds.Breed = '{breed}' ORDER BY Breeds.Breed;"
    cur.execute(sql)
    return cur.fetchall()


con = db.connect('127.0.0.1', 'root', '')
cur = con.cursor()
sql = '''
CREATE DATABASE IF NOT EXISTS Tech;
USE Tech;
CREATE TABLE IF NOT EXISTS Breeds (
    CodBreed INT PRIMARY KEY AUTO_INCREMENT,
    Breed VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS Facts(
    CodFact INT PRIMARY KEY AUTO_INCREMENT,
    Fact VARCHAR(250) NOT NULL,
    Breed INT,
    FOREIGN KEY (Breed) REFERENCES Breeds(CodBreed)
);'''
cur.execute(sql)

save_breeds(172)

qtd = 0
while qtd < 40:
    save_facts(100)
    cur.execute('SELECT MAX(CodFact) FROM Facts')
    qtd = cur.fetchone()[0]

while True:
    print('\n\nMENU DE OPÇÕES')
    print('0. Apagar o Banco de Dados e Sair')
    print('1. Mostrar quantas fatos cada raça possui')
    print('2. Mostrar todas os fatos de todas as raças')
    print('3. Mostrar fatos de uma raça em específico')
    opc = int(input('Digite o número da opção desejada: '))
    print()
    if opc == 0:
        cur.execute('DROP DATABASE tech')
        break
    elif opc == 1:
        breeds = get_breeds()
        for breed in breeds:
            print(f'\033[35m{breed[0]}:\033[0m {breed[1]}')
    elif opc == 2:
            for date in get_facts():
                print(f'\033[35m{date[0]}:\033[0m {date[1]}')
    elif opc == 3:
            breed = input('Digite a raça que deseja conhecer alguns fatos sobre: ')
            facts = search_breed(breed)
            if facts == 0:
                print('Não foram encontrados fatos sobre a raça digitada!')
            else:
                n = 0
                for fact in facts:
                    n += 1
                    print(f'\033[35m{n}.\033[0m {fact[0]}')
    else:
        print('\033[31mOPÇÃO INVÁLIDA!\033[0m')