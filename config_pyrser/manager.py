import configparser
import inspect

from config_pyrser import fields


class NoConfigError(Exception):
    pass


class Section:
    def __call__(self, cfg, section):
        for option in cfg.options(section):
            try:
                self.__getattribute__(option)(cfg, section, option)
            except AttributeError:
                # Option was not defined in section class
                continue

        for name, field in inspect.getmembers(self, lambda x: isinstance(x, fields.Field)):
            # Initialize all fields that have a default value but were not found in config file
            field(cfg, section, name)
        return self


class Config:
    def __init__(self, path=None, config_parser=None, **kwargs):
        if isinstance(path, str):
            cfg = configparser.ConfigParser(**kwargs)
            cfg.read(path)
        elif config_parser:
            cfg = config_parser
        else:
            raise NoConfigError('No path to config or prepared config specified.')

        for name, section in inspect.getmembers(self, predicate=lambda field: isinstance(field, Section)):
            section(cfg, name)
