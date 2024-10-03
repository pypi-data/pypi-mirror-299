from copy import deepcopy
import re


class BackwardCompatibilityAdapter:
    DATA_TYPES = {
        'int': 'integer',
        'str': 'string',
        'float': 'double',
        'bool': 'boolean',
    }

    def __init__(self, config, logger):
        self._config = deepcopy(config)
        self._log = logger

    def convert(self):
        disable_subscriptions = self._config['server'].pop('disableSubscriptions', None)
        if disable_subscriptions is not None:
            self._config['server']['enableSubscriptions'] = not disable_subscriptions

        mapping_configuration = deepcopy(self._config.get('server', {}).get('mapping', []))
        if not mapping_configuration:
            return self._config

        for node_config in mapping_configuration:
            try:
                node_config['deviceNodeSource'] = self.get_value_source(node_config['deviceNodePattern'], False)

                device_type_pattern = node_config.pop('deviceTypePattern', 'default')
                device_name_pattern = node_config.pop('deviceNamePattern', None)
                node_config['deviceInfo'] = {
                    'deviceNameExpressionSource': self.get_value_source(device_name_pattern),
                    'deviceNameExpression': device_name_pattern,
                    'deviceProfileExpressionSource': self.get_value_source(device_type_pattern),
                    'deviceProfileExpression': device_type_pattern
                }

                # converting attributes and timeseries sections
                for config_section_name in ('attributes', 'timeseries'):
                    for section_config in node_config.get(config_section_name, []):
                        path = section_config.pop('path', None)

                        section_config['type'] = self.get_value_source(path)
                        section_config['value'] = path

                # converting attributes_updates section
                for config in node_config.get('attributes_updates', []):
                    attribute_on_tb = config.pop('attributeOnThingsBoard', None)
                    attribute_on_device = config.pop('attributeOnDevice', None)

                    config['key'] = attribute_on_tb
                    config['type'] = self.get_value_source(attribute_on_device)
                    config['value'] = attribute_on_device

                # converting rpc section
                for config in node_config.get('rpc_methods', []):
                    arguments = config.pop('arguments', [])
                    config['arguments'] = []

                    for arg in arguments:
                        converted_argument = {
                            'type': self.DATA_TYPES.get(type(arg).__name__, 'string'),
                            'value': arg
                        }
                        config['arguments'].append(converted_argument)
            except Exception as e:
                self._log.error('Error during conversion: ', e)
                self._log.info('Config: ', node_config)

        # Removing old mapping section
        self._config['server'].pop('mapping')
        # Adding new mapping section
        self._config['mapping'] = mapping_configuration

        return self._config

    @staticmethod
    def get_value_source(value, possible_constant=True):
        if re.search(r"(ns=\d+;[isgb]=[^}]+)", value):
            return 'identifier'
        elif re.search(r"\${([A-Za-z.:\\\d]+)}", value) or not possible_constant:
            return 'path'
        else:
            return 'constant'
