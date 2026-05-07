import yaml
import os


class Config:

    def __init__(self):
        config_path = os.path.join(
            os.path.dirname(__file__),
            "config.yaml"
        )

        with open(config_path, "r") as file:
            self.data = yaml.safe_load(file)

    def get(self, key):
        return self.data.get(key)


config = Config()