from cryptography.fernet import Fernet

# Remplace par ta clé générée précédemment
key = b'_J31q6mAtUEyZCrM8bUQF4mImrLL0McmOYZ7jr3FKWI='

fernet = Fernet(key)

# URL du webhook à chiffrer
webhook_url = "https://discord.com/api/webhooks/1271645951026659339/wWCSAlPG3TuhycH7ex6h9O48nKdFn4G55WUk4-lgay4RQTpCbbt-DYuo9jLIHYEReQKj"

# Chiffrement de l'URL du webhook
encrypted_webhook = fernet.encrypt(webhook_url.encode())

print(f"Webhook chiffré : {encrypted_webhook.decode()}")
