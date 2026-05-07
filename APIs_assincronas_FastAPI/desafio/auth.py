from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext


# Configurando a segurança
SECRET_KEY = "uma_chave_secreta_e_longa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Usando a ferramenta para transformar as senhas hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Função para ver se as senhas são compatíveis
def verificar_senha(senha_original, senha_hash):
    return pwd_context.verify(senha_original, senha_hash)


# Função para gerar o token
def criar_token_acesso(dados: dict):
    dados_para_criptografar = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_para_criptografar.update({"exp": expiracao})

    # token seguro com jwt
    token_jwt = jwt.encode(dados_para_criptografar,
                           SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt
