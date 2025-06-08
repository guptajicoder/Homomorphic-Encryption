import secrets
secure_key = secrets.token_hex(32)  # Generates a 64-character hex string
print(secure_key)