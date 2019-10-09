'''
Config File Handler for qpapers
'''

import os
import yaml


class Config():
    '''
    YAML Config File Handler Class
    '''
    config_paths = [
        '~/.config/qpapers/',
        '~/.qpapers/',
        '/etc/qpapers/',
    ]

    config_filename = 'config.yml'

    config_file = None
    # default config
    default_config = {
        'services': {
            'arxiv': {
                'enabled': True,
                'results': 2
            }
        }
    }

    config = None

    def __init__(self):
        self._load_config_file()
        self.services = []
        if self.config_file:
            config_f = open(self.config_file)
            self.config = yaml.load(config_f)

    def _load_config_file(self):
        if not self.config_file:
            for config_path in self.config_paths:
                config_file = os.path.expanduser(
                    os.path.join(config_path, self.config_filename))
                if os.path.isfile(config_file):
                    self.config_file = config_file
                    break

    def get_config(self):
        return self.config or self.default_config

    @property
    def all_services(self):
        '''Return all Services in Config'''
        config = self.get_config()
        if config:
            return config.get('services')
        return {}

    @property
    def enabled_services(self):
        '''Return all Enabled Services'''
        services = self.all_services
        return {service: value for service, value in services.items() if value.get('enabled')}
