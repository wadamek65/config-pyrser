import pytest

from config_pyrser import manager, fields


def test_no_config_defined():
    with pytest.raises(manager.NoConfigError) as error:
        manager.Config()

    assert error.value.args[0] == 'No path to config or prepared config specified.'


def test_read_config(test_config):
    class Section1(manager.Section):
        string_option = fields.Field()
        bool_option = fields.BoolField()
        int_option = fields.IntField()
        float_option = fields.FloatField()

    class Section2(manager.Section):
        option = fields.Field()

    class Config(manager.Config):
        section_1 = Section1()
        section_2 = Section2()

    cfg = Config(config_parser=test_config)

    assert cfg.section_1.string_option is test_config.get('section_1', 'string_option')
    assert cfg.section_1.bool_option is test_config.getboolean('section_1', 'bool_option')
    assert cfg.section_1.int_option is test_config.getint('section_1', 'int_option')
    assert cfg.section_1.float_option == test_config.getfloat('section_1', 'float_option')
    assert cfg.section_2.option is test_config.get('section_2', 'option')


def test_read_config_from_path(test_config_path, test_config):
    class Section1(manager.Section):
        string_option = fields.Field()
        bool_option = fields.BoolField()
        int_option = fields.IntField()
        float_option = fields.FloatField()

    class Section2(manager.Section):
        option = fields.Field()

    class Config(manager.Config):
        section_1 = Section1()
        section_2 = Section2()

    cfg = Config(path=test_config_path)

    assert cfg.section_1.string_option == test_config.get('section_1', 'string_option')
    assert cfg.section_1.bool_option is test_config.getboolean('section_1', 'bool_option')
    assert cfg.section_1.int_option == test_config.getint('section_1', 'int_option')
    assert cfg.section_1.float_option == test_config.getfloat('section_1', 'float_option')
    assert cfg.section_2.option == test_config.get('section_2', 'option')


def test_read_config_assign_new_value(test_config):
    class Section1(manager.Section):
        string_option = fields.Field()

    class Config(manager.Config):
        section_1 = Section1()

    cfg = Config(config_parser=test_config)

    assert cfg.section_1.string_option is test_config.get('section_1', 'string_option')

    new_value = 'new_value'
    cfg.section_1.string_option = new_value
    assert cfg.section_1.string_option == new_value


def test_read_config_frozen_option(test_config):
    class Section1(manager.Section):
        string_option = fields.Field(frozen=True)

    class Config(manager.Config):
        section_1 = Section1()

    cfg = Config(config_parser=test_config)

    assert cfg.section_1.string_option is test_config.get('section_1', 'string_option')

    with pytest.raises(fields.FrozenFieldError) as error:
        cfg.section_1.string_option = 'new value'

    assert error.value.args[0] == 'Cannot set frozen field "string_option" in section "section_1"'
