from src.api import run_server
from src.client import run_client


if __name__ == "__main__":
    type_input = raw_input("what do you want to do")

    if int(type_input) == 1:
        """
        runs the api server
        """
        run_server()

    if int(type_input) == 2:
        """
        runs the client
        """
        run_client()
