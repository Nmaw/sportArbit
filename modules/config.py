from configparser import ConfigParser, NoSectionError
import sys


class Config:

    def __init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def config_load(config_file):

        # Load Config File
        config = ConfigParser()
        try:
            config.read(config_file)
            path_log_file = config['logs']['path']
            log_file = config['logs']['file']

            return config, '{}/{}'.format(path_log_file, log_file)

        except NoSectionError:
            print('No Config File Found! Exit.')
            sys.exit()

    @staticmethod
    def get_config(config, section):

        # Check all sections
        if section == 'all':
            return config.sections()

        # Check active bets
        elif section == 'bets':
            bets = []
            for bet in config[section]:
                if config[section][bet] == 'true':
                    bet = {'db': bet, 'url': config[bet]['url']}
                    bets.append(bet)
            return bets

        # Check current margin
        elif section == 'margin':
            return config[section]['percentage']
