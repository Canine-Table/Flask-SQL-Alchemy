from dotenv import load_dotenv
from alchemy import create_app


app = create_app()


if __name__ == '__main__':
    load_dotenv()
    app.run()
