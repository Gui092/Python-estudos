# models.py

**O que é Enum?**
É uma "Lista de Escolhas". Imagine que você pergunta a cor de um sinal de trânsito.
A resposta tem que ser "Verde", "Amarelo" ou "Vermelho". O Enum impede que alguém
escreva "Azul". No nosso caso, impede que alguém invente um tipo de transação
que não existe.

**O que é Optional da biblioteca typing?**
É uma forma de dizer ao Python: "Este campo pode ter um valor ou pode ser None
(vazio)". É útil para campos que não são obrigatórios no formulário.

**Como saber o que é um "modelo" para usar BaseModel?**
Pense no BaseModel como a "planta" de uma casa. Se você precisa receber ou enviar
um grupo de dados organizados (como um usuário, um produto ou uma conta),
você cria um modelo. Se for apenas um valor solto (como só o saldo), não precisa.

**O que é Field?**
É uma ferramenta para colocar "regras extras" em um campo. Exemplo: "Este número
tem que ser maior que zero" (gt=0) ou "Este texto deve ter no máximo 20 caracteres".

**Na classe "class Transacao(BaseModel):**
**tipo: TipoTransacao"**
**O que quer dizer esse "tipo: TipoTransacao?"**
Aqui estamos dizendo que a variável tipo não é apenas um texto comum, mas sim
um dos valores que definimos lá no nosso Enum lá em cima.

**Na classe "class ContaCorrente(BaseModel):" O que é transacoes: List[Transacao] = []?**
Isso diz que o campo transacoes será uma lista (como um array) e que cada item
dentro dessa lista deve seguir o modelo Transacao. O [] no final diz que, se a
conta for nova, ela começa com uma lista vazia.

# main.py

**Por que usamos "post" e "get"?**
São verbos de ação na web.
GET: Você quer "pegar" algo (ex: ver o extrato). Não altera nada no servidor.
POST: Você quer "postar/enviar" algo para ser criado ou processado
(ex: fazer um depósito ou login).

**O que é OAuth2PasswordBearer?**
É o "vigia" que diz ao FastAPI: "Olha, para acessar este sistema, o usuário
precisa me mostrar um token neste endereço /token".

**O que é "token_type": "bearer"?**
"Bearer" significa "Portador". É um padrão que diz: "Quem for o portador deste
token tem permissão de acesso". É como um ingresso de cinema: não importa quem
comprou, quem estiver com ele na mão entra.

**O que é "Depends(oauth2_scheme)"?**
É uma trava. Ele diz: "Esta função depende de um token válido". Se o usuário não
enviar o token, o FastAPI nem executa a função e já barra o usuário ali mesmo.

# auth.py

**O que é ALGORITHM = "HS256"?**
É o tipo de "embaralhamento" usado. O HS256 é um dos mais comuns e seguros para
JWT. É como escolher se você vai escrever uma mensagem secreta usando código
Morse ou Cifra de César.

**Por que usar JWTError?**
É um aviso específico. Se alguém tentar falsificar um token, o sistema gera esse
erro. Usamos o try/except para capturar esse erro e dizer "Acesso Negado".

**Detalhando essa parte: CryptContext(schemes=["bcrypt"], deprecated="auto")**
É a configuração do nosso "triturador de senhas".
schemes=["bcrypt"]: Diz que o algoritmo para esconder a senha é o Bcrypt.
deprecated="auto": Diz para o sistema se atualizar automaticamente se surgir
uma versão mais segura do Bcrypt no futuro.

**Função "verify" dentro de verificar senha?**
Vem da biblioteca passlib. Ela pega a senha pura ("123") e o hash que está no
banco e faz o cálculo matemático para ver se eles batem.

**O que é o "update" dentro de tokens_de_acesso?**
**dados_para_criptografar.update({"exp": expiracao})**
No Python, update serve para adicionar ou mudar informações em um dicionário.
Aqui, estamos adicionando a data de expiração ao token.

**O que é o "encode"?**
É o ato de transformar os dados (JSON) naquela string gigante e criptografada
que aparece no Swagger.

**Na biblioteca datetime, o que o timedelta faz?**
É a "calculadora de tempo". Se você quer que o token vença em 30 minutos, o
timedelta(minutes=30) soma esses 30 minutos à hora atual.

**Como é usado o SECRET_KEY?**
Ela é o "tempero secreto". O encode usa essa chave para assinar o token. Se
alguém tentar mudar o saldo dentro do token, a assinatura quebra porque o hacker
não tem a sua SECRET_KEY.

**"dados={"sub": username}"?**
No padrão JWT, sub é o "Assunto" ou "Dono" do token. Geralmente guardamos o ID
ou o Username do usuário ali.

**O que significa payload?**
É a parte "recheada" do token, onde ficam os dados (username, data de expiração, etc.).

**O que é o decode?**
É o contrário do encode. É pegar aquela string gigante e transformar de volta
em dados legíveis.

**O que é "\*\*user"?**
Isso se chama "Unpacking" (Descompactar). Ele pega todos os dados do dicionário
do usuário (nome, saldo, etc.) e os entrega "espalhados". É como se você abrisse
uma caixa de ferramentas e colocasse tudo em cima da mesa.

# models.py

**Esse banco de dados é temporário?**
Sim. Como criamos um dicionário db_contas no Python, ele vive na memória RAM.
Se você fechar o terminal e abrir de novo, os depósitos que você fez somem.
Para ser permanente, precisaríamos de um banco como SQLite ou PostgreSQL.

# dúvidas gerais

**Como saber quando usar async def?**
Use sempre que a função for lidar com entrada e saída de dados (In/Out), como
ler um banco de dados, chamar outra API ou esperar um arquivo carregar.
No FastAPI, é boa prática usar quase sempre.

**Como saber quando iniciar com @app?**
Sempre que você quiser criar uma "rota", ou seja, um endereço que o usuário
pode acessar no navegador ou no sistema (ex: /login, /extrato).

---

## 💡 Resumo das dúvidas (O "Manual do Aluno")

resumo dos pontos chave:

### 1. Sobre a Segurança (JWT)

O **JWT** é como um "crachá assinado". Quando você faz login, o servidor usa
sua `SECRET_KEY` para criar esse crachá. Como só o seu servidor tem essa chave,
ninguém pode alterar o saldo dentro do token sem invalidar a assinatura.

O **Payload** é o conteúdo do crachá, e o **Decode** é o ato de ler esse conteúdo.

### 2. Sobre o Código (Async & Depends)

**Async:** Usamos quando o código precisa "esperar" por algo (como uma resposta
de banco de dados), permitindo que o servidor atenda outras pessoas nesse meio
tempo.

**Depends:** É um sistema de "pedágio". A função só executa se a dependência
(como o login) for satisfeita.

### 3. Sobre os Modelos (Pydantic)

**BaseModel** define a estrutura.
**Field** coloca as regras (tipo "não aceite valor menor que zero").
**Enum** restringe as opções (tipo "só aceite'saque' ou 'deposito'").

### 4. Por que `bcrypt==4.0.1`?

As versões mais novas do Python mudaram como os módulos internos funcionam.
A versão 4.0.1 do `bcrypt` é a que mantém a compatibilidade com a biblioteca
`passlib` que usamos no projeto.

**Observação:**
Em ambiente de produção, a SECRET_KEY e dados sensíveis seriam gerenciados via
variáveis de ambiente para maior segurança.
