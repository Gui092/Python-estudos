from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco, contas):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco, [])
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
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
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("### Operação falhou! Você não tem saldo suficiente. \n")

        elif valor > 0:
            self._saldo -= valor
            print("### Saque realizado com sucesso! \n")
            return True

        else:
            print("### Operação falhou! O valor informado é inválido. \n")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("### Depósito relaizado com sucesso! \n")
            return True

        else:
            print("### Operação falhou! O valor informado é inválido. \n")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=1000, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.
             transacoes if transacao["tipo"] == "Saque"])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("### Operação falhou! O valor do saque excede o limite. \n")

        elif excedeu_saques:
            print("### Operação falhou! O número máximo de saques excede o limite. \n")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
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
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# Criar cliente
cliente = PessoaFisica(
    cpf="12345678900",
    nome="Guilherme",
    data_nascimento="08-03-1992",
    endereco="Rua Brasil, 123"
)

# Criar conta
conta = ContaCorrente.nova_conta(cliente, numero=1)

# Vincular conta ao cliente
cliente.adicionar_conta(conta)

# Fazer depósito
deposito = Deposito(200)
cliente.realizar_transacao(conta, deposito)

# Fazer saque
saque = Saque(50)
cliente.realizar_transacao(conta, saque)

# Ver saldo
print(f"Saldo: R$ {conta.saldo:.2f}")

# Ver histórico
print("\n=== Histórico de transações ===")
for historico in conta.historico.transacoes:
    print(f"{historico}: R$ {historico['valor']} em {historico['data']}")
