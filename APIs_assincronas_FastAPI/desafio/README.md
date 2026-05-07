# 🏦 API Bancária Assíncrona - LuizaLabs Bootcamp

Este projeto é uma API RESTful desenvolvida com **FastAPI** para gerenciar
operações bancárias simples, como depósitos, saques e consulta de extratos,
utilizando autenticação segura via **JWT**.

## 🚀 Tecnologias Utilizadas

- **Python 3.13.3**
- **FastAPI**
- **Pydantic**: Validação de dados e modelos.
- **JWT (JSON Web Tokens)**: Segurança e autenticação.
- **Passlib & Bcrypt**: Criptografia de senhas.

## 🛠️ Como Instalar e Rodar

1. **Clone o repositório:**
   git clone <link-do-seu-repositorio>
   cd APIs_assincronas_FastAPI/desafio

2. **Crie e ative o ambiente virtual:**
   python -m venv venv

# Windows:

venv\Scripts\activate

# Linux/Mac:

source venv/bin/activate

3. **Instale as dependências:**
   pip install -r requirements.txt

4. **Inicie o servidor:**
   uvicorn main:app --reload

# 📖 Guia de Uso

1. **Acesso à Documentação**
   Com o servidor rodando, acesse http://127.0.0.1:8000/docs para visualizar a
   interface do Swagger.

2. **Autenticação (Login)**
   Clique no botão Authorize (cadeado) ou no endpoint /token.

   Use as credenciais cadastradas (No nosso exemplo: Usuário: gui123 | Senha: 123).

   Após o login, o sistema liberará o acesso aos endpoints restritos.

3. **Operações**
   Depósito: Envie um valor positivo para aumentar seu saldo.

   Saque: O sistema validará se você possui saldo suficiente antes de processar.

   Extrato: Consulte todo o seu histórico de transações e saldo atual.

## 🧠 Documentação de Apoio

Para facilitar o entendimento dos conceitos aplicados (JWT, Pydantic, Async/Await),
criei um guia detalhado explicando a finalidade de cada componente:
[Veja o Guia de Conceitos aqui](./CONCEITOS.md)

# 📲 Melhorias futuras

**Persistência de Dados:**
Implementar um banco de dados real (PostgreSQL/SQLite) para que os dados não
sumam ao reiniciar.

**Hash Dinâmico:**
Criar um endpoint de cadastro de usuários em vez de usar usuários fixos
no database.py.

**Testes Automatizados:**
Implementar testes com pytest para garantir que a lógica de saque/depósito
nunca quebre.
