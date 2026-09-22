import os

from gunicorn.app.base import BaseApplication

from sbapi.main import create_app

app = create_app()


class GunicornApplication(BaseApplication):
    def __init__(self, application, options):
        self.application = application
        self.options = options
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if value is not None:
                self.cfg.set(key, value)

    def load(self):
        return self.application


def main() -> None:
    options = {
        "bind": os.getenv("SBAPI_BIND", "0.0.0.0:8000"),
        "workers": int(os.getenv("SBAPI_WORKERS", "4")),
    }
    GunicornApplication(app, options).run()


if __name__ == "__main__":
    main()
