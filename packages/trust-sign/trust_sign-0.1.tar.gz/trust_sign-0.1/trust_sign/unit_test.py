import unittest
from token_sign import generate_token, validate_token, detokenize_data, encrypt_data, decrypt_data
import audit_trail
import time
import jwt

class TestTokenSign(unittest.TestCase):
    def setUp(self):
        # Réinitialiser la base de données pour chaque test
        audit_trail.init_db()
        self.test_data = "Sensitive Data"
        self.token = generate_token(self.test_data)

    def test_encrypt_data(self):
        encrypted_data = encrypt_data(self.test_data)
        self.assertIsNotNone(encrypted_data)
        self.assertNotEqual(encrypted_data, self.test_data)

    def test_decrypt_data(self):
        encrypted_data = encrypt_data(self.test_data)
        decrypted_data = decrypt_data(encrypted_data)
        self.assertEqual(decrypted_data, self.test_data)

    def test_generate_token(self):
        self.assertIsNotNone(self.token)
        decoded = jwt.decode(self.token, 'your_secret_key_here', algorithms=['HS256'])
        self.assertIn('data', decoded)

    def test_validate_token_expired(self):
        # Générer un token avec une date d'expiration passée
        expired_token = jwt.encode({
            'data': encrypt_data(self.test_data),
            'exp': time.time() - 3600  # Date passée (1 heure dans le passé)
        }, 'your_secret_key_here', algorithm='HS256')
        result = validate_token(expired_token)
        self.assertFalse(result['valid'])
        self.assertEqual(result['message'], 'Token expired')

    def test_detokenize_data(self):
        result = detokenize_data(self.token)
        self.assertEqual(result, self.test_data)

    def test_detokenize_data_invalid(self):
        invalid_token = self.token + 'extra'  # Ajouter du texte pour rendre le token invalide
        result = detokenize_data(invalid_token)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
