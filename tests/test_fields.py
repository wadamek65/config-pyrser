import configparser

import pytest

from config_pyrser import fields


def test_field_create():
    field = fields.Field()

    assert field._initiated is False
    assert field._required is True
    assert field._default is field._UNSET


def test_field_initiate(test_config):
    field = fields.Field()
    section = 'section_1'
    option = 'string_option'
    field(test_config, section, option)

    assert field._initiated is True
    assert field._value is test_config.get(section, option)


def test_not_required(test_config):
    field = fields.Field(required=False)
    section = 'is not required'
    option = 'is not required'
    field(test_config, section, option)

    assert field._initiated is True
    assert field._required is False
    assert field._value is None


def test_default(test_config):
    default_value = 'DEFAULT'
    field = fields.Field(default=default_value)
    section = 'is default'
    option = 'is default'
    field(test_config, section, option)

    assert field._initiated is True
    assert field._required is True
    assert field._default is default_value
    assert field._value is default_value


def test_required_no_section(test_config):
    field = fields.Field()
    section = 'does not exist'
    option = 'does not exist too'
    with pytest.raises(fields.MissingFieldError) as error:
        field(test_config, section, option)
    assert error.value.args[0] == f'Option "{option}" in section "{section}" is required.'
    assert isinstance(error.value.args[1], configparser.NoSectionError)


def test_required_no_option(test_config):
    field = fields.Field()
    section = 'section_1'
    option = 'does not exist too'
    with pytest.raises(fields.MissingFieldError) as error:
        field(test_config, section, option)
    assert error.value.args[0] == f'Option "{option}" in section "{section}" is required.'
    assert isinstance(error.value.args[1], configparser.NoOptionError)


def test_bool_field(test_config):
    field = fields.BoolField()
    section = 'section_1'
    option = 'bool_option'
    field(test_config, section, option)

    assert field._initiated is True
    assert isinstance(field._value, bool)
    assert field._value is test_config.getboolean(section, option)


def test_int_field(test_config):
    field = fields.IntField()
    section = 'section_1'
    option = 'int_option'
    field(test_config, section, option)

    assert field._initiated is True
    assert isinstance(field._value, int)
    assert field._value is test_config.getint(section, option)


def test_float_field(test_config):
    field = fields.FloatField()
    section = 'section_1'
    option = 'float_option'
    field(test_config, section, option)

    assert field._initiated is True
    assert isinstance(field._value, float)
    assert field._value == test_config.getfloat(section, option)
