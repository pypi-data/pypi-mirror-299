import jwt
import datetime
import base64
from cryptography.fernet import Fernet
import logging

SECRET_KEY = 'your_secret_key_here'

# Générer une clé pour le chiffrement
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# Configuration du journaliseur
LOG_FILE = 'audit_trail.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.DEBUG

def setup_logger():
    """Configurer le journaliseur."""
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    handler = logging.FileHandler(LOG_FILE)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)

def log_audit_trail(event, message, level=logging.INFO):
    """Enregistrer les événements de journalisation avec différents niveaux."""
    logger = logging.getLogger()
    log_message = f'Event: {event}, Message: {message}'

    if level == logging.DEBUG:
        logger.debug(log_message)
    elif level == logging.INFO:
        logger.info(log_message)
    elif level == logging.WARNING:
        logger.warning(log_message)
    elif level == logging.ERROR:
        logger.error(log_message)
    elif level == logging.CRITICAL:
        logger.critical(log_message)
    else:
        logger.info(log_message)  # Niveau par défaut

# Configurer le journaliseur au démarrage du script
setup_logger()

# Chiffrement des données
def encrypt_data(data):
    if isinstance(data, str):
        data = data.encode()  # Convertir les données en bytes si elles sont en string
    encrypted_data = cipher_suite.encrypt(data)
    return base64.urlsafe_b64encode(encrypted_data).decode()  # Encoder en base64 pour la transmission

# Déchiffrement des données
def decrypt_data(encrypted_data):
    encrypted_data = base64.urlsafe_b64decode(encrypted_data)  # Décoder du base64
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode()  # Retourner les données originales en texte

# Générer un token avec données chiffrées et une expiration personnalisée
def generate_token(data, expiration_hours=1):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours)
    
    # Chiffrer les données avant de les inclure dans le token
    encrypted_data = encrypt_data(data)
    
    token = jwt.encode({
        'data': encrypted_data,  # Ajouter les données chiffrées au token
        'exp': expiration
    }, SECRET_KEY, algorithm='HS256')
    
    log_audit_trail('Token Generated', f'Data Encrypted: {bool(data)}, Expiration: {expiration}')
    
    return token

# Valider et détokéniser
def validate_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        encrypted_data = decoded.get('data')
        exp = datetime.datetime.fromtimestamp(decoded['exp'])
        
        # Déchiffrer les données
        decrypted_data = decrypt_data(encrypted_data)
        
        log_audit_trail('Token Validated', f'Data: {decrypted_data}, Expiration: {exp}')
        
        return {
            'valid': True,
            'data': decrypted_data,  # Retourner les données déchiffrées
            'expiration': exp.isoformat()
        }
    except jwt.ExpiredSignatureError:
        log_audit_trail('Token Validation Failed', 'Token expired', level=logging.WARNING)
        return {'valid': False, 'message': 'Token expired'}
    except jwt.InvalidTokenError:
        log_audit_trail('Token Validation Failed', 'Invalid token', level=logging.ERROR)
        return {'valid': False, 'message': 'Invalid token'}

# Détokénisation explicite (si besoin)
def detokenize_data(token):
    decoded = validate_token(token)
    if decoded['valid']:
        log_audit_trail('Data Detokenized', f'Data: {decoded["data"]}')
        return decoded['data']  # Retourner les données déchiffrées
    else:
        log_audit_trail('Data Detokenization Failed', 'Invalid or expired token', level=logging.ERROR)
        return None

# Gestion des tokens expirés
def remove_expired_tokens(tokens):
    """Supprimer les tokens expirés de la liste des tokens."""
    valid_tokens = []
    for token in tokens:
        result = validate_token(token)
        if result['valid']:
            valid_tokens.append(token)
    return valid_tokens
