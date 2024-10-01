import csv
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import hashlib
import boto3
import json

# Función para obtener la clave de encriptación de Secrets Manager
def get_encryption_key_from_secrets_manager(secret_name):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = response['SecretString']
        secret_data = json.loads(secret)
        return secret_data.get("data-key", None)
    except Exception as e:
        print("Error al obtener el secreto:", e)
        return None

# Convertir la clave de encriptación a 32 bytes para AES-256
def get_aes_key(key_str):
    return hashlib.sha256(key_str.encode('utf-8')).digest()

# Desencriptar un valor encriptado
def decrypt_value(encrypted_value, key):
    if not encrypted_value:
        return ''
    try:
        encrypted_data = base64.b64decode(encrypted_value)
        iv = encrypted_data[:16]
        ct = encrypted_data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        data = unpad(cipher.decrypt(ct), AES.block_size)
        return data.decode('utf-8')
    except Exception as e:
        print(f"Error al desencriptar el valor: {e}")
        return ''

# Verificar si un valor parece estar encriptado (codificado en Base64)
def is_encrypted(value):
    try:
        base64.b64decode(value)
        return True
    except Exception:
        return False

# Función para desencriptar un archivo CSV
def decrypt_csv_file(input_crp_filepath, output_directory, aes_key):
    decrypted_csv_filepath = os.path.join(output_directory, os.path.basename(input_crp_filepath).replace('.crp', '_decrypted.csv'))

    with open(input_crp_filepath, 'r', encoding='utf-8') as encrypted_csv_file:
        reader = csv.reader(encrypted_csv_file, delimiter='~')
        headers = next(reader)
        first_row = next(reader)
        encrypted_columns = [i for i, value in enumerate(first_row) if is_encrypted(value)]

        encrypted_csv_file.seek(0)
        reader = csv.reader(encrypted_csv_file, delimiter='~')
        headers = next(reader)

        with open(decrypted_csv_filepath, 'w', newline='', encoding='utf-8') as decrypted_csv_file:
            writer = csv.writer(decrypted_csv_file, delimiter='~')
            writer.writerow(headers)

            for row in reader:
                decrypted_row = row.copy()
                for idx in encrypted_columns:
                    decrypted_row[idx] = decrypt_value(row[idx], aes_key)
                writer.writerow(decrypted_row)

    print(f"Archivo CSV desencriptado guardado: {decrypted_csv_filepath}")
