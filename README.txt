# API Segura - Documentação

Esta documentação oferece uma visão geral dos aspectos funcionais e de segurança. Esta é uma API simples construída com Flask que demonstra práticas de segurança.

## Configuração

Antes de executar a aplicação, é necessário configurar a chave secreta que será usada para assinar os tokens JWT. Você pode definir essa chave como uma variável de ambiente.


export MY_SECRET_KEY=sua_chave_secreta_aqui
Certifique-se de substituir sua_chave_secreta_aqui pela sua própria chave.


Instalação
Certifique-se de ter Python 3.x e pip instalados.
Instale as dependências do projeto:

pip install -r requirements.txt


Executando a API
Execute o seguinte comando para iniciar o servidor:

python3 app.py
A API estará disponível em http://localhost:5000.

Endpoints
POST /register: Registrar um usuário.
POST /login: Fazer login e obter um token JWT.
POST /record: Criar um registro.
GET /users: Obter informações dos usuários.
PUT /record/<uuid>: Atualizar um registro.
DELETE /record/<uuid>: Excluir um registro.


Funcionalidades

Controle de Taxa: A API implementa limites de requisições por minuto utilizando o Flask Limiter para controlar e mitigar possíveis ataques de negação de serviço (DDoS) e tentativas de força bruta.

Registro de Usuário: A API permite que os usuários se registrem fornecendo um nome de usuário e senha por meio do endpoint /register.

Login do Usuário: Os usuários podem fazer login fornecendo seu nome de usuário e senha pelo endpoint /login, que retorna um token JWT para autenticação.

Gerenciamento de Registros: A API possibilita a criação, recuperação, atualização e exclusão de registros de usuário por meio dos endpoints apropriados (/record, /users, /record/<uuid>, e /record/<uuid> respectivamente).

Revogação de Token: Um mecanismo de revogação de token é implementado por meio do endpoint /revoke, permitindo a invalidação de tokens previamente emitidos.



Aspectos de Segurança

Uso de JWT (JSON Web Tokens): O JWT com HS512 é utilizado para autenticação, garantindo comunicação segura e validação das identidades dos usuários. O token contém informações do usuário e é assinado digitalmente com uma chave secreta para evitar adulteração. Também possui funcionalidades de renovação e controle de tempo de uso.

Rate Limiting: É aplicado o controle de taxa para prevenir abusos e limitar o número de requisições por minuto, mitigando ataques de negação de serviço (DDoS) e tentativas de força bruta.

Cabeçalhos de Segurança: A API define cabeçalhos de segurança para controlar o acesso e mitigar várias vulnerabilidades, incluindo clickjacking e scripts maliciosos. Alguns cabeçalhos de segurança importantes incluem:

Access-Control-Allow-Origin
X-Content-Type-Options
X-Frame-Options
X-XSS-Protection
Content-Security-Policy
Strict-Transport-Security
Referrer-Policy

Identificadores Únicos (UUID): São gerados UUIDs para fornecer identificadores únicos para os registros, evitando enumeração de usuários e registros.

Variável de Ambiente para a Chave Secreta: A chave secreta para JWT é obtida de uma variável de ambiente (MY_SECRET_KEY), aumentando a segurança ao manter informações sensíveis fora do código.

Revogação de Token: A API permite a revogação de tokens previamente emitidos.

Tratamento de Exceções: É implementado um tratamento adequado de exceções em todo o código, aumentando a segurança e prevenindo possíveis vazamentos de informações.

Validação de Entrada: A entrada de dados é validada para garantir que os campos obrigatórios estejam presentes e mitigar possíveis ataques de injeção de código.
