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

    assert cfg.section_1.string_option == test_config.get('section_1', 'string_option')
    assert cfg.section_1.bool_option == test_config.getboolean('section_1', 'bool_option')
    assert cfg.section_1.int_option == test_config.getint('section_1', 'int_option')
    assert cfg.section_1.float_option == test_config.getfloat('section_1', 'float_option')
    assert cfg.section_2.option == test_config.get('section_2', 'option')


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
    assert cfg.section_1.bool_option == test_config.getboolean('section_1', 'bool_option')
    assert cfg.section_1.int_option == test_config.getint('section_1', 'int_option')
    assert cfg.section_1.float_option == test_config.getfloat('section_1', 'float_option')
    assert cfg.section_2.option == test_config.get('section_2', 'option')


def test_read_config_assign_new_value(test_config):
    class Section1(manager.Section):
        string_option = fields.Field(frozen=False)

    class Config(manager.Config):
        section_1 = Section1()

    cfg = Config(config_parser=test_config)

    assert cfg.section_1.string_option == test_config.get('section_1', 'string_option')

    new_value = 'new_value'
    cfg.section_1.string_option = new_value
    assert cfg.section_1.string_option == new_value


def test_read_config_frozen_option(test_config):
    class Section1(manager.Section):
        string_option = fields.Field(frozen=True)

    class Config(manager.Config):
        section_1 = Section1()

    cfg = Config(config_parser=test_config)

    assert cfg.section_1.string_option == test_config.get('section_1', 'string_option')

    with pytest.raises(fields.FrozenFieldError) as error:
        cfg.section_1.string_option = 'new value'

    assert error.value.args[0] == 'Cannot set frozen field "string_option" in section "section_1"'


def test_read_config_unspecified_option_with_default(test_config):
    default_value = 'default_value'

    class Section1(manager.Section):
        unspecified_option = fields.Field(default=default_value)
        unspecified_option_2 = fields.IntField(default=10)

    class Config(manager.Config):
        section_1 = Section1()

    cfg = Config(config_parser=test_config)

    assert cfg.section_1.unspecified_option == default_value
    assert cfg.section_1.unspecified_option_2 == 10


def test_read_config_unspecified_option(test_config):
    class Section1(manager.Section):
        unspecified_option = fields.Field()
        unspecified_option_2 = fields.IntField()

    class Config(manager.Config):
        section_1 = Section1()

    with pytest.raises(fields.MissingFieldError) as error:
        Config(config_parser=test_config)

    assert error.value.args[0] == 'Option "unspecified_option" in section "section_1" is required.'


def test_allow_multiple_instances(test_config):
    class Section1(manager.Section):
        string_option = fields.Field(frozen=False)

    class Config(manager.Config):
        section_1 = Section1()

    instance_1 = Config(config_parser=test_config)
    instance_2 = Config(config_parser=test_config)

    assert instance_1.section_1.string_option == instance_2.section_1.string_option


def test_reuse_sections(test_config):
    class CustomSection(manager.Section):
        string_option = fields.Field()

    class Config(manager.Config):
        section_1 = CustomSection()
        section_3 = CustomSection()

    cfg = Config(config_parser=test_config)

    assert cfg.section_1.string_option == test_config.get('section_1', 'string_option')
    assert cfg.section_3.string_option == test_config.get('section_3', 'string_option')
