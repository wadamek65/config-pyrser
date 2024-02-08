# config-pyrser
## About
`config-pyrser` is a simple library on top of `configparser` that makes it easier to manage settings in 
Python apps by providing a way to declaratively define configuration. 
This enables type safety, validation, and IDE autocompletion, reducing room for error in 
comparison to using dynamic strings.

## Installation
To use this project, you need Python version 3.9 or higher. 
Install the package via pip with the following command:

```bash
pip install config-pyrser
```

## Usage
### Basic example
```python
from config_pyrser import Config, Field, BoolField, IntField, FloatField, Section

class DatabaseSection(Section):
    url = Field(default="sqlite:///example.db")
    max_connections = IntField(default=10)

class FeaturesSection(Section):
    debug_mode = BoolField(default=False)
    timeout = FloatField(default=5.5)

class AppConfig(Config):
    Database = DatabaseSection()
    Features = FeaturesSection()

# Initialize AppConfig with the path to your config file
app_config = AppConfig(path='path/to/config.ini')

# Access configuration values within sections
print(f"Database URL: {app_config.Database.url}")
print(f"Database Max Connections: {app_config.Database.max_connections}")
print(f"Debug Mode: {app_config.Features.debug_mode}")
print(f"Timeout: {app_config.Features.timeout}")

```

### Manually parsing configuration files
For cases where you need to manually parse a configuration file before initializing config-pyrser, 
you can use configparser and pass the resulting object to Config via the config_parser argument.

```python
import configparser
from config_pyrser import Config, Field, Section

class SettingsSection(Section):
    debug_mode = Field(default=False)

class AppConfig(Config):
    Settings = SettingsSection()

# Manually parse the configuration file
config_parser = configparser.ConfigParser()
config_parser.read('path/to/config.ini')

# Initialize AppConfig with the configparser object
app_config = AppConfig(config_parser=config_parser)

# Access the configuration value within the section
print(f"Debug Mode: {app_config.Settings.debug_mode}")
```

### Custom fields
To customize usage of `config-pyrser`, you can define and use your own custom fields by inheriting 
the `Field` class and overriding the `parse` method.

#### Additional validation
```python
from config_pyrser import Field, Config, Section

class ValidationError(Exception):
    """Exception raised for errors in the validation of a field."""

class EmailField(Field):
    def parse(self, value):
        if "@" not in value or "." not in value:
            raise ValidationError(f"{value} is not a valid email address.")
        return value

class UserSection(Section):
    admin_email = EmailField(required=True)

class AppConfig(Config):
    User = UserSection()
```

#### Complex data structures
```python
import json
from config_pyrser import Field, Config, Section

class JsonField(Field):
    def parse(self, value):
        return json.loads(value)

class AppConfig(Config):
    class Settings(Section):
        complex_config = JsonField()
```

## API
### `Config`
The `Config` class serves as the base for defining application configurations. 
It supports loading configurations from files or objects and can be extended to include custom behavior.

#### Options
* `path` (optional): The file path to the configuration file. 
If specified, config-pyrser will automatically load the configuration from this file using `configparser`.
* `config_parser` (optional): An instance of configparser.ConfigParser. 
If specified, config-pyrser will use this pre-parsed configuration instead of reading from a file. 
This is useful for advanced scenarios where the configuration is loaded or modified programmatically 
before being passed to Config.
* `**kwargs` (optional): Additional arguments that will be passed to the `configparser.Configparser` 
when using the `path` argument.

### `Section`
The `Section` class is used to define sections within the configuration, 
aligning with sections defined in INI configuration files. 
It acts as a container for multiple configuration options, represented as fields.

### `Field`
The Field class is the foundational element for defining configuration options within a section.

#### Options
* `default` (optional): Sets the default value for the field if it is not explicitly provided in the 
configuration source. This is particularly useful for optional configuration options or providing 
sensible defaults.

* `required` (optional, default `True`): Indicates whether the field must be present in the configuration 
source. If set to False, the configuration can omit this field, and the specified default value will 
be used if provided.

* `frozen` (optional, default `True`): Determines whether the value of the configuration option can be 
modified after initial loading. If set to `True`, any attempts to change the field's value at runtime will 
raise an error, ensuring the immutability of the configuration.

## Errors
### `FrozenFieldError`
Raised when there is an attempt to modify the value of a configuration option marked as frozen. 
This ensures the immutability of certain configuration settings after initial loading.

### `MissingFieldError`
Triggered when a required field is not provided in the configuration source. Helpful in detecting misconfiguration
issues as soon as possible.

### `NoConfigError`
Occurs when a Config object is initialized without specifying a configuration source via either the 
path or config_parser arguments, and no configuration is found or provided.

## License
This project is licensed under the MIT License.
