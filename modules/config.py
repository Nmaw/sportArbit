from configparser import ConfigParser, NoSectionError
import sys


class Config:

    def __init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def load_config(config_file):
        # Load Config File
        config = ConfigParser()
        try:
            config.read(config_file)
            log_file = config['logs']['file']
            return config, '{}/{}'.format('logs', log_file)
        except NoSectionError:
            print('No Config File Found! Exit.')
            sys.exit()

    @staticmethod
    def get_config(config, section):

        # Check all sections
        if section == 'all':
            return config.sections()

        # Check config
        elif section == 'default':
            params = [{'db': config[section]['db'], 'margin': config[section]['margin']}]
            return params
