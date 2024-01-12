from cryptography.fernet import Fernet
import os

# Função para descriptografar um arquivo usando a chave fornecida
def decrypt_file(key, encrypted_filename, output_filename):
    try:
        # Criar um objeto Fernet com a chave
        fernet = Fernet(key)

        # Abrir o arquivo criptografado em modo de leitura binária
        with open(encrypted_filename, "rb") as file:
            # Ler os dados criptografados do arquivo
            encrypted_data = file.read()
        
        # Descriptografar os dados
        decrypted_data = fernet.decrypt(encrypted_data)

        # Abrir o arquivo de saída em modo de gravação binária e escrever os dados descriptografados
        with open(output_filename, "wb") as file:
            file.write(decrypted_data)
        
    except Exception as e:
        print(f"Erro")

# Função para abrir o arquivo contendo a chave de criptografia
def open_FileCrypt(key_file_path):
    with open(key_file_path, "rb") as file:
        key = file.read()
    return key

# Lista de arquivos criptografados a serem descriptografados
lista_arquivos_criptografados = [
]

# Caminho para o arquivo contendo a chave de criptografia
key_file_path = r""

# Obter a chave de criptografia a partir do arquivo
key = open_FileCrypt(key_file_path)

# Iterar sobre a lista de arquivos criptografados e descriptografar cada um
for encrypted_file_path in lista_arquivos_criptografados:
    # Descriptografar o arquivo e salvar o resultado no arquivo descriptografado
    decrypt_file(key, encrypted_file_path, encrypted_file_path)

