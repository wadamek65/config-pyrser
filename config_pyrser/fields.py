import configparser


class MissingFieldError(Exception):
    pass


class FrozenFieldError(Exception):
    pass


class Field:
    _UNSET = object()

    def __init__(self, default=_UNSET, required=True, frozen=False):
        self._default = default
        self._required = required
        self._frozen = frozen

        self._value = None
        self._initiated = False
        self._cfg = None
        self._section = None
        self._option = None

    def __call__(self, cfg, section, option):
        self._cfg = cfg
        self._section = section
        self._option = option
        self._initiated = True
        try:
            self._value = self.parse(self._cfg.get(self._section, self._option))
        except (configparser.NoSectionError, configparser.NoOptionError) as error:
            if self._default is not self._UNSET:
                self._value = self._default
            elif self._required:
                raise MissingFieldError(f'Option "{option}" in section "{section}" is required.', error)

    def __get__(self, instance, owner):
        if self._initiated:
            return self._value
        return self

    def __set__(self, instance, value):
        if self._frozen and self._initiated:
            raise FrozenFieldError(f'Cannot set frozen field "{self._option}" in section "{self._section}"')

        self._value = self.parse(value)

    def parse(self, value):
        return value


class BoolField(Field):
    def parse(self, _value):
        return self._cfg.getboolean(self._section, self._option)


class IntField(Field):
    def parse(self, _value):
        return self._cfg.getint(self._section, self._option)


class FloatField(Field):
    def parse(self, _value):
        return self._cfg.getfloat(self._section, self._option)
