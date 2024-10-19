from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._agencia = "0001"
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("Não é possível efetuar o saque, saldo insuficiente!!")

        elif valor > 0:
            self._saldo -= valor
            print("Saque efetuado com sucesso!")
            return True
        
        else:
            print("Valor inválido para saque, tente novamente!")
        
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Deposito finalizado com sucesso!')
        else:
            print("Valor inválido, tente novamente!")

            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Valor acima do limite máximo por saque!")
        
        elif excedeu_saques:
            print("Você atingiu numero limite de saques diário!")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""
            Agencia: {self.agencia}
            C/C: {self.numero}
            Titular: {self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_ok = conta.sacar(self.valor)

        if transacao_ok:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_ok = conta.depositar(self.valor)

        if transacao_ok:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """

        Bem vindo ao nosso Banco, selecione uma das opções abaixo:

        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Criar Conta
        [5] Listar Contas
        [6] Cadastrar Cliente
        [0] Sair

    => """
    return int(input(menu))

def depositar(clientes):
        cpf = input("Digite o cpf (somente números):")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("Cliente não encontrado!")
            return
        
        valor = float(input("Digite o valor do deposito:"))
        transacao = Deposito(valor)

        conta = recuperar_conta(cliente)
        if not conta:
            return
        
        cliente.realizar_transacao(conta, transacao)
        
def sacar(clientes):
    cpf = input("Digite o cpf (somente números):")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Digite o valor do saque:"))
    transacao = Saque(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Digite o cpf (somente números):")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    conta = recuperar_conta(cliente)
    if not conta:
        return
    
    print("-------- Extrato --------")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"{transacao['tipo']}: R$ {transacao['valor']:.2f}\n"
    
    print(extrato)
    print(f"Saldo: R$ {conta.saldo:.2f}")
    print('-----------------------------------')

def criar_cliente(clientes):
    cpf = input("Digite o cpf (somente números):")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe um cadastro para esse CPF, por favor tente novamente!")
        return
    
    nome = input("Digite o nome completo:")
    data_nasc = input("Digite a data de nascimento (dd/mm/yyyy):")
    endereco = input("Digite o endereço (logradouro, nº - bairro - cidade/uf):")

    cliente = PessoaFisica(nome=nome,data_nascimento=data_nasc,cpf=cpf,endereco=endereco)
    clientes.append(cliente)
    print("Cliente criado com sucesso!")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Digite o cpf do cliente (somente números):")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")

def recuperar_conta(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    
    return cliente.contas[0]

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))

def main():
    lista_clientes = []
    lista_contas = []
    numero_conta = 1
    
    while True:

        opcao = menu()

        if opcao == 1:
            depositar(lista_clientes)
            
        elif opcao == 2:
            sacar(lista_clientes)
            
        elif opcao == 3:
            exibir_extrato(lista_clientes)
        
        elif opcao == 4:
            criar_conta(numero_conta, lista_clientes, lista_contas)
            numero_conta += 1

        elif opcao == 5:
            listar_contas(lista_contas)

        elif opcao == 6:
            criar_cliente(lista_clientes)

        elif opcao == 0:
            print("Obrigado por utilizar nosso Banco!!")
            break

        else:
            print("Operação Inválida!! Selecione novamente a opção desejada.")

main()