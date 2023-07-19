from dotenv import load_dotenv
from alchemy import create_app


if __name__ == '__main__':
    load_dotenv()
    create_app = create_app()
    create_app.run()
else:
    gunicorn_app = create_app()
