import os
from cryptography.fernet import Fernet

# 📌 Carregar a chave de criptografia
def carregar_chave():
    with open("criptografia/chave_secreta.key", "rb") as chave_file:
        return Fernet(chave_file.read())

# 🔒 Criptografar um dado
def criptografar(dado):
    f = carregar_chave()
    return f.encrypt(dado.encode()).decode()

# 🔓 Descriptografar um dado
def descriptografar(dado_criptografado):
    f = carregar_chave()
    return f.decrypt(dado_criptografado.encode()).decode()
