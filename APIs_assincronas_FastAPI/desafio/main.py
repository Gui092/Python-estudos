from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import TipoTransacao, Transacao
from jose import jwt, JWTError

from auth import verificar_senha, criar_token_acesso, SECRET_KEY, ALGORITHM
from database import db_contas

app = FastAPI()

# Configuração do esquema de segurança
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    user_dict = db_contas.get(username)

    # Se o usuário não existe ou a senha não bate
    if not user_dict or not verificar_senha(password, user_dict["senha_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos."
        )

    token = criar_token_acesso(dados={"sub": username})
    return {"access_token": token, "token_type": "bearer"}


# Função de token
async def obter_usuario_atual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        user = db_contas.get(username)
        if user is None:
            raise HTTPException(
                status_code=401, detail="Usuário não encontrado")

        return {"username": username, **user}
    except JWTError:
        raise HTTPException(status_code=401, detail="Erro ao validar token")


# Endpoint de transações
@app.post("/transacoes/")
async def realizar_transacao(
    transacao: Transacao,
    usuario: dict = Depends(obter_usuario_atual)
):
    username = usuario["username"]

    # Lógica de Saque
    if transacao.tipo == TipoTransacao.saque:
        if transacao.valor > db_contas[username]["saldo"]:
            raise HTTPException(
                status_code=400, detail="Saldo insuficiente para este saque.")

        db_contas[username]["saldo"] -= transacao.valor

    # Lógica de Depósito
    elif transacao.tipo == TipoTransacao.deposito:
        db_contas[username]["saldo"] += transacao.valor

    # Registrar no Histórico
    db_contas[username]["transacoes"].append(transacao.dict())

    return {
        "mensagem": f"{transacao.tipo.capitalize()} realizado com sucesso!",
        "novo_saldo": db_contas[username]["saldo"]
    }


# Endpoint de extrato
@app.get("/extrato")
async def ver_extrato(usuario: dict = Depends(obter_usuario_atual)):
    return {
        "titular": usuario["titular"],
        "saldo_atual": db_contas[usuario["username"]]["saldo"],
        "historico": db_contas[usuario["username"]]["transacoes"]
    }
