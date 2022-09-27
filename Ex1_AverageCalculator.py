quantity = int(input('Digite a quantidade de números que deseja calcular a média: '))
total = 0
for q in range(1, quantity + 1):
    total += float(input(f'Digite o {q}º número: '))
avg = total / quantity
print(f'Sua média é: {avg:.2f}')
print('aprovado' if avg>=6 else 'reprovado')
