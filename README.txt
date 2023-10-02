# API de Exemplo

Esta é uma API simples construída com Flask que demonstra práticas de segurança.

## Configuração

Antes de executar a aplicação, é necessário configurar a chave secreta que será usada para assinar os tokens JWT. Você pode definir essa chave como uma variável de ambiente.

export MY_SECRET_KEY=chave_secreta_aqui


Certifique-se de substituir `chave_secreta_aqui` pela sua própria chave.

## Instalação

1. Certifique-se de ter Python 3.x e pip instalados.
2. Instale as dependências do projeto:

pip install -r requirements.txt


## Executando a API

Execute o seguinte comando para iniciar o servidor:

python3 app.py


A API estará disponível em http://localhost:5000.

## Endpoints

- `POST /register`: Registrar um usuário.
- `POST /login`: Fazer login e obter um token JWT.
- `POST /record`: Criar um registro.
- `GET /users`: Obter informações dos usuários.
- `PUT /record/<uuid>`: Atualizar um registro.
- `DELETE /record/<uuid>`: Excluir um registro.

Consulte a [documentação da API](./API_DOCUMENTATION.md) para obter mais detalhes sobre os endpoints e seu uso.

## Documentação da API

Para mais detalhes sobre os aspectos de segurança e funcionais da API, consulte a [documentação da API](./API_DOCUMENTATION.md).

## Contribuição

Sinta-se à vontade para contribuir e melhorar esta API. Crie um PR e ficaremos felizes em revisar.

## Licença

Este projeto está licenciado sob a [MIT License](./LICENSE).



