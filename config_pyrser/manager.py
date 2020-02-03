import configparser
import copy

from config_pyrser import fields


class NoConfigError(Exception):
    pass


class SectionMeta(type):
    def __new__(mcs, name, bases, attrs):
        options = {}
        for key, value in attrs.items():
            if isinstance(value, fields.Field):
                options[key] = copy.copy(value)

        for option in options:
            del attrs[option]

        attrs['_options'] = options
        return type.__new__(mcs, name, bases, attrs)


class Section(metaclass=SectionMeta):
    def init(self, cfg, section):
        for option in self._options:
            self._options[option].init(cfg, section, option)

        return self

    def __getattribute__(self, item):
        try:
            print(self, super().__getattribute__('_options')[item])
            return super().__getattribute__('_options')[item].value
        except (KeyError, AttributeError):
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        try:
            super().__getattribute__('_options')[key].set(value)
        except (KeyError, AttributeError):
            super().__setattr__(key, value)


class ConfigMeta(type):
    def __new__(mcs, name, bases, attrs):
        sections = {}
        for key, value in attrs.items():
            if isinstance(value, Section):
                sections[key] = copy.copy(value)

        for section in sections:
            del attrs[section]

        attrs['_sections'] = sections
        return type.__new__(mcs, name, bases, attrs)


class Config(metaclass=ConfigMeta):
    def __init__(self, path=None, config_parser=None, **kwargs):
        if isinstance(path, str):
            cfg = configparser.ConfigParser(**kwargs)
            cfg.read(path)
        elif config_parser:
            cfg = config_parser
        else:
            raise NoConfigError('No path to config or prepared config specified.')

        for section in self._sections:
            self._sections[section].init(cfg, section)

    def __getattribute__(self, item):
        try:
            return super().__getattribute__('_sections')[item]
        except (KeyError, AttributeError):
            return super().__getattribute__(item)
