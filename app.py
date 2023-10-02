from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import redis
import jwt
import uuid  # Importe a biblioteca uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

app = Flask(__name__)


# Acesse a variável de ambiente
secret_key = os.environ.get('MY_SECRET_KEY')

# Verifique se a variável de ambiente foi definida
if secret_key is None:
    raise ValueError('A variável de ambiente MY_SECRET_KEY não está definida.')



# Configurando o Limiter para controle de taxa (rate limiting)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://",
)

db = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
app.config['SECRET_KEY'] = secret_key
app.config['ALGORITHM'] = 'HS512'
OLDTOKEN = None



# Configuração dos cabeçalhos de segurança
@app.after_request
def add_security_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Permite acesso de qualquer origem
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'same-origin'
    return response



# Função para validar a presença dos campos esperados nos dados de entrada
def validate_input(data, *expected_fields):
    for field in expected_fields:
        if field not in data:
            return False
    return True

# Função para obter os dados JSON da requisição
def get_json():
    try:
        return request.get_json()
    except Exception as e:
        print(f"Error parsing JSON: {str(e)}")
        return None

def generate_token(username):
    global OLDTOKEN
    
    expiration_time = datetime.utcnow() + timedelta(seconds=3600)
    payload = {
        'username': username,
        'exp': expiration_time
    }
    
    if OLDTOKEN:
        revoke_token(OLDTOKEN)
    
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm=app.config['ALGORITHM'])
    OLDTOKEN = token
    return token

def verify_token(token):
    try:
        if db.lrange('revoked_tokens', 0, -1):
            if token in db.lrange('revoked_tokens', 0, -1):
                return None
        
        decoded = jwt.decode(
            token, 
            app.config['SECRET_KEY'], 
            algorithms=[app.config['ALGORITHM']],
            options={'verify_options': {'algorithms': ['HS512'], 'require': ['exp']}}
        )
        
        return decoded['username']
    
    except jwt.ExpiredSignatureError:
        return None
    
    except jwt.InvalidTokenError:
        return None

def revoke_token(token):
    db.lpush('revoked_tokens', token)

@app.route('/revoke', methods=['POST'])
def revoke_token_route():
    token = request.headers.get('Authorization')
    
    if token:
        revoke_token(token)
        return jsonify({'message': 'Token revoked successfully'})
    else:
        return jsonify({'message': 'Token não fornecido'}), 401

@app.route('/register', methods=['POST'])
def register_user():
    data = get_json()
    if not data or not validate_input(data, 'username', 'password'):
        return jsonify({'message': 'Dados de entrada inválidos'}), 400

    username = data['username']
    password = data['password']

    db.hmset(f'user:{username}', {'username': username, 'password': password})
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    global OLDTOKEN
    
    data = get_json()
    if not data or not validate_input(data, 'username', 'password'):
        return jsonify({'message': 'Dados de entrada inválidos'}), 400

    username = data['username']
    password = data['password']

    user_data = db.hgetall(f'user:{username}')
    
    if user_data and user_data['password'] == password:
        if OLDTOKEN:
            revoke_token(OLDTOKEN)
        
        token = generate_token(username)
        return jsonify({'message': 'Login successful', 'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'})

@app.route('/record', methods=['POST'])
def create_record():
    token = request.headers.get('Authorization')
    username = verify_token(token)
    if not username:
        return jsonify({'message': 'Unauthorized'}), 401

    data = get_json()
    if not data or not validate_input(data, 'name', 'address', 'cpf'):
        return jsonify({'message': 'Dados de entrada inválidos'}), 400

    # Gere um UID único para o registro
    record_uid = str(uuid.uuid4())

    name = data['name']
    address = data['address']
    cpf = data['cpf']

    # Utilize o UID gerado para a chave do registro
    record_key = f'record:{record_uid}'
    db.hmset(record_key, {'user_id': record_uid, 'name': name, 'address': address, 'cpf': cpf})
    return jsonify({'message': 'Record created successfully'})

@app.route('/users', methods=['GET'])
def list_users():
    token = request.headers.get('Authorization')
    username = verify_token(token)
    if not username:
        return jsonify({'message': 'Unauthorized'}), 401

    record_keys = db.keys('record:*')
    records = []
    for key in record_keys:
        record_data = db.hgetall(key)
        records.append(record_data)
    
    return jsonify({'Data': records})

@app.route('/record/<uuid:record_uid>', methods=['PUT'])
def update_record(record_uid):
    token = request.headers.get('Authorization')
    username = verify_token(token)
    if not username:
        return jsonify({'message': 'Unauthorized'}), 401

    data = get_json()
    if not data or not validate_input(data, 'name', 'address', 'cpf'):
        return jsonify({'message': 'Dados de entrada inválidos'}), 400

    name = data['name']
    address = data['address']
    cpf = data['cpf']

    # Utiliza o UID recebido na URL para identificar o registro a ser atualizado
    record_key = f'record:{record_uid}'
    if db.exists(record_key):
        db.hmset(record_key, {'name': name, 'address': address, 'cpf': cpf})
        return jsonify({'message': 'Record updated successfully'})
    else:
        return jsonify({'message': 'Record not found'}), 404

@app.route('/record/<uuid:record_uid>', methods=['DELETE'])
def delete_record(record_uid):
    token = request.headers.get('Authorization')
    username = verify_token(token)
    if not username:
        return jsonify({'message': 'Unauthorized'}), 401

    # Utiliza o UID recebido na URL para identificar o registro a ser excluído
    record_key = f'record:{record_uid}'
    if db.exists(record_key):
        db.delete(record_key)
        return jsonify({'message': 'Record deleted successfully'})
    else:
        return jsonify({'message': 'Record not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
