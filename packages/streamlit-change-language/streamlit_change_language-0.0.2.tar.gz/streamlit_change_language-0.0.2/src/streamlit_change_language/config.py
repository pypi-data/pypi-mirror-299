import configparser

class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

    def read(self):
        self.config.read(self.config_path)
        return self.config

    def save(self, config: configparser):
        with open(self.config_path, 'w') as config_file:
            config.write(config_file)