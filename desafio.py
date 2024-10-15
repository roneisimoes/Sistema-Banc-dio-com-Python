def menu():
    menu = """

        Bem vindo ao nosso Banco, selecione uma das opções abaixo:

        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Criar Conta
        [5] Listar Contas
        [6] Cadastrar Usuário
        [0] Sair

    => """
    return int(input(menu))

def depositar(valor_deposito, saldo, extrato, /):
        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito -> R$ {valor_deposito:.2f}\n"
            print('Deposito finalizado com sucesso!')
        else:
            print("Valor inválido, tente novamente!")

        return saldo, extrato
        
def sacar(*, saldo, valor_saque, extrato, limite, numero_saques, limite_saques):
    if numero_saques < limite_saques:
        if valor_saque > saldo:
            print("Não é possível efetuar o saque, saldo insuficiente!!")
            
        elif valor_saque > limite:
            print("Valor acima do limite máximo por saque!")
            
        elif valor_saque > 0:
            saldo -= valor_saque
            extrato += f"Saque -> R$ {valor_saque:.2f}\n"
            numero_saques += 1

            print("Saque efetuado com sucesso!")   
        else:
            print("Valor inválido para saque, tente novamente!")
    else:
        print("Você atingiu numero limite de saques diário!")
    
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
        print("----------- Extrato da sua conta -------------")
        print("Não foram realizadas movimentações nessa conta. " if not extrato else extrato)
        print(f"Saldo total da conta -> R$ {saldo:.2f}")
        print('----------------------------------------------')

def criar_usuario(usuarios):
    cpf = input("Digite o cpf (somente números):")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe um cadastro para esse CPF, por favor tente novamente!")
        return
    
    nome = input("Digite o nome completo:")
    data_nasc = input("Digite a data de nascimento (dd/mm/yyyy):")
    endereco = input("Digite o endereço (logradouro, nº - bairro - cidade/uf):")

    usuario = {
        'nome' : nome,
        'data_nasc' : data_nasc,
        'cpf' : cpf,
        'endereco' : endereco 
    }
    usuarios.append(usuario)
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(numero_conta, usuarios, agencia):
    cpf = input("Digite o cpf do usuário (somente números):")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        
        conta = {
            'agencia' : agencia,
            'numero_conta' : numero_conta,
            'usuario' : usuario
        }

        print("Conta criada com sucesso!")
        return conta
    
    print("Falha ao criar a conta, usuário não encontrado, tente novamente!!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
            ---- Informações da Conta ----
            Ag: {conta['agencia']}
            C/C: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print('=' * 100)
        print(linha)

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    lista_usuarios = []
    lista_contas = []
    numero_conta = 1

    while True:

        opcao = menu()

        if opcao == 1:

            valor_deposito = float(input("Digite o valor que deseja depositar: "))
            saldo, extrato = depositar(valor_deposito,saldo,extrato)
            
        elif opcao == 2:
            valor_saque = float(input("Digite o valor que deseja sacar: "))
            saldo, extrato, numero_saques = sacar(saldo=saldo,valor_saque=valor_saque,extrato=extrato,limite=limite,numero_saques=numero_saques,limite_saques=LIMITE_SAQUES)
            
        elif opcao == 3:
            exibir_extrato(saldo,extrato=extrato)
        
        elif opcao == 4:
            conta = criar_conta(numero_conta, lista_usuarios, AGENCIA)

            if conta:
                lista_contas.append(conta)
                numero_conta += 1
        
        elif opcao == 5:
            listar_contas(lista_contas)

        elif opcao == 6:
            criar_usuario(lista_usuarios)

        elif opcao == 0:
            print("Obrigado por utilizar nosso Banco!!")
            break

        else:
            print("Operação Inválida!! Selecione novamente a opção desejada.")

main()