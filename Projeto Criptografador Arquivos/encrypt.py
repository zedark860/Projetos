from cryptography.fernet import Fernet

# Lista de arquivos que serão criptografados
lista_arquivos_criptografar = [
]

# Função para gerar uma chave de criptografia usando o Fernet
def generate_key():
    return Fernet.generate_key()

# Função para carregar a chave de criptografia a partir de um arquivo
def load_key(key_file):
    return open(key_file, "rb").read()

# Função para criptografar um arquivo usando a chave fornecida
def encrypt_file(key, filename):
    fernet = Fernet(key)

    # Abrir o arquivo em modo de leitura binária
    with open(filename, "rb") as file:

        # Ler o conteúdo do arquivo
        file_data = file.read()

    # Criptografar os dados do arquivo
    encrypted_data = fernet.encrypt(file_data)

    # Abrir o arquivo em modo de gravação binária e escrever os dados criptografados
    with open(filename, "wb") as file:
        file.write(encrypted_data)

# Exemplo de uso

# Gerar uma nova chave
key = generate_key()

# Caminho para o arquivo que armazenará a chave
key_filename = r""

# Salvar a chave no arquivo
with open(key_filename, "wb") as key_file:
      key_file.write(key)

# Iterar sobre a lista de arquivos a serem criptografados
for arquivo_criptografar in lista_arquivos_criptografar:
    # Criptografar cada arquivo com a chave gerada
    encrypt_file(key, arquivo_criptografar)

# Mensagem indicando que a criptografia foi concluída
print("Criptografia concluída.")
