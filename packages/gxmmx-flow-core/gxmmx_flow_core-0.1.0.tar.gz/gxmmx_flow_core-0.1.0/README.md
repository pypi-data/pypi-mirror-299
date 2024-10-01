# Flow Core

GxMMx Flow Core is a Python package for Flow's core functionality.  

Flow Core is the building block used and extended by Flow images for workflows.  
It consists of basic configuration, validation and management of Flow parameters.

<!-- Badges etc -->

## Information

### Requirements

Python 3.11+

## Installation

Package is available on [PyPI](https://pypi.org/project/gxmmx-flow-core/) and installable via pip:

``` shell
pip install gxmmx-flow-core
```

## Usage

``` python
from gxmmx_flow_core import Flow, FlowLog, FlowCodeQuality, FlowValidationError

# Add config_param decorator to function
# Declares validation for a config parameter.
# This value must be an integer.
# In this case if the value is not present in the config,
# the value gets a default of 15.
# If it is greater than 30 it is invalid, and an exception is raised.
@Flow.config_param()
def param_some_int(value):
    if value is None:
        value = 15
    if not isinstance(value, int):
        raise FlowValidationError("some_int must be an integer")
    if value > 30:
        raise FlowValidationError("some_int must be 30 or less")
    return value

# Creates directory and parent directories
# under the root dir that the program is called from.
Flow.ensure_directory("my_build_dir")

# Creates a code quality report that logs errors
# to stdout as well as creates a report.
cq_report = FlowCodeQuality("my_report")

# Looks for and loads flow.yml config file.
# Can be specified by 'FLOW_CONFIG_PATH' env variable.
Flow.start()

# dummy logic
something_failed_in_file_txt = True
if something_failed_in_file_txt:
    cq_report.critical(name="my-error",
                       desc="description of error",
                       path="file.txt", begin=14)

FlowLog.msg("This is a normal message")
FlowLog.wrn("This is a warning message")

# Finish report and write it out.
# If there are errors, the program will exit with error.
cq_report.write()
```

## Development

Development documentation can be found under the projects
[`docs`](https://gitlab.com/gxmmx/gitops/flow/core/flow-core).

## Changes

Version history with features and bugfixes, as well as upcoming features and roadmap  
depicted in `CHANGELOG.md`

## Contributing

Any contributions are greatly appreciated. See `CONTRIBUTING.md` for more information.

### Contributors

* [gummigudm](https://gitlab.com/gummigudm)  

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Guðmundur Guðmundsson - <gummigudm@gmail.com>

* Gitlab - [gummigudm](https://gitlab.com/gummigudm)  
* Github - [gummigudm](https://github.com/gummigudm)
