from os import getenv
from app.MPP import app

def main() -> None:
    application = app()
    application.run_webhook(
        listen='0.0.0.0',
        port=getenv('WEBHOOK_URL',8080),
        webhook_url=getenv('WEBHOOK_URL')
    )
    #application.run_polling()
if __name__ == "__main__":
    main()
