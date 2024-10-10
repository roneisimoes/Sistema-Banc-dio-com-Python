menu = """

    Bem vindo ao nosso Banco, selecione uma das opções abaixo:

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [0] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = int(input(menu))

    if opcao == 1:

        valor_deposito = float(input("Digite o valor que deseja depositar: "))
        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito -> R$ {valor_deposito:.2f}\n"
            print('Deposito finalizado com sucesso!')

        else:
            print("Valor inválido, tente novamente!")

    elif opcao == 2:

        if numero_saques < 3:
            valor_saque = float(input("Digite o valor que deseja sacar: "))
            if valor_saque > saldo:
                print("Não é possível efetuar o saque, saldo insuficiente!!")
                continue
            if valor_saque > limite:
                print("Valor acima do limite máximo por saque!")
                continue
               
            if valor_saque > 0:
                saldo -= valor_saque
                extrato += f"Saque -> R$ {valor_saque:.2f}\n"
                numero_saques += 1
                print("Saque efetuado com sucesso!")
            else:
                print("Valor inválido para saque, tente novamente!")
        else:
            print("Você atingiu numero limite de saques diário!")
        
    elif opcao == 3:
        print("----------- Extrato da sua conta -------------")
        print("Não foram realizadas movimentações nessa conta. " if not extrato else extrato)
        print(f"Saldo total da conta -> R$ {saldo:.2f}")
        print('----------------------------------------------')

    elif opcao == 0:
        print("Obrigado por utilizar nosso Banco!!")
        break

    else:
        print("Operação Inválida!! Selecione novamente a opção desejada.")


            