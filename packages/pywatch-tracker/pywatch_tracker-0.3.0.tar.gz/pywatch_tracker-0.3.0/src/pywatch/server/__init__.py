import pywatch.server.main as main
from pywatch.parse_setup import parse_module


def start_webapp(path: str) -> None:
    main.path = path

    main.app.run()
