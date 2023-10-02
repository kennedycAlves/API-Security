# Documentação da API

Esta documentação descreve a API de exemplo e seus endpoints.

## Autenticação

A API utiliza JSON Web Tokens (JWT) para autenticação. Para obter um token JWT, faça uma requisição para o endpoint `/login` com as credenciais do usuário.

### Login

**Endpoint:** `POST /login`

**Requisição**

```json
{
  "username": "exemplo",
  "password": "senha_exemplo"
}
Resposta de Sucesso


{
  "message": "Login bem-sucedido",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
Registro de Usuário
Endpoint: POST /register

Requisição


{
  "username": "novo_usuario",
  "password": "nova_senha"
}
Resposta de Sucesso


{
  "message": "Usuário registrado com sucesso"
}
Operações de Registros
Criar Registro
Endpoint: POST /record

Requisição


{
  "name": "Nome do Registro",
  "address": "Endereço do Registro",
  "cpf": "CPF do Registro"
}
Resposta de Sucesso


{
  "message": "Registro criado com sucesso"
}
Obter todos os Registros
Endpoint: GET /users

Resposta de Sucesso


{
  "Data": [
    {
      "user_id": "ID_do_Usuario",
      "name": "Nome do Registro",
      "address": "Endereço do Registro",
      "cpf": "CPF do Registro"
    },
    ...
  ]
}
Atualizar Registro
Endpoint: PUT /record/<uuid>

Requisição


{
  "name": "Novo Nome do Registro",
  "address": "Novo Endereço do Registro",
  "cpf": "Novo CPF do Registro"
}
Resposta de Sucesso


{
  "message": "Registro atualizado com sucesso"
}
Excluir Registro
Endpoint: DELETE /record/<uuid>

Resposta de Sucesso


{
  "message": "Registro excluído com sucesso"
}
Rate Limiting
A API possui limites de taxa para cada endpoint, limitando o número de requisições para prevenir possíveis ataques de DDoS e força bruta.

Os limites são configurados para 100 requisições por minuto por padrão.

Revogação de Token
A API permite revogar tokens anteriormente emitidos, caso seja necessário invalidar o acesso. Para revogar um token, faça uma requisição para o endpoint /revoke com o token no cabeçalho de autorização.

Revogar Token
Endpoint: POST /revoke

Requisição

Header:

makefile
Copy code
Authorization: Bearer <token>
Resposta de Sucesso


{
  "message": "Token revogado com sucesso"
}
Consulte o código fonte para mais detalhes sobre a implementação da API.

Licença
Este projeto está licenciado sob a MIT License.
