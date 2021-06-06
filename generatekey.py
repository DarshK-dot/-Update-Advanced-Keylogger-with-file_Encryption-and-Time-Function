from cryptography.fernet import Fernet

key = Fernet.generate_key()
ex = "\\"
file = open("encryptionkey.txt", "wb")
file.write(key)
file.close()
