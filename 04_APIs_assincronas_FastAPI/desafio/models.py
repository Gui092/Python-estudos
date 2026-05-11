from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


# Tipos de transação
class TipoTransacao(str, Enum):
    deposito = "deposito"
    saque = "saque"


# Formulário da transação
class Transacao(BaseModel):
    tipo: TipoTransacao
    valor: float = Field(gt=0, description="O valor deve ser maior que zero.")


# Formulário da conta corrente
class ContaCorrente(BaseModel):
    id: int
    titular: str
    saldo: float = 0.0
    transacoes: List[Transacao] = []


# Modelo de Login
class UsuarioLogin(BaseModel):
    username: str
    password: str
