import configparser, os

def readConfigData(section, key):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), "../ConfigurationFiles/Config.cfg")
    config.read(config_path)
    return config.get(section, key)

def fetchElementLocators(section, key):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), "../ConfigurationFiles/Elements.cfg")
    config.read(config_path)
    return config.get(section, key)