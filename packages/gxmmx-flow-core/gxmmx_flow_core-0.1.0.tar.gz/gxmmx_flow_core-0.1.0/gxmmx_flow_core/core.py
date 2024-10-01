import os
import yaml
import inspect
from typing import Callable, Any

from .errors import FlowError, FlowConfigError, FlowValidationError
from .log import FlowLog

# ------------------------------------------------------------------------------
# Flow Core
# ------------------------------------------------------------------------------


class Flow:
    _started = False
    _root_dir = os.getcwd()
    _validators = dict()
    config = dict()

    # --------------------------------------
    # Internal functions
    # --------------------------------------

    @classmethod
    def _get_config(cls) -> None:
        config_env_var = "FLOW_CONFIG_PATH"
        config_default_paths = [
            "flow.yml",
            ".flow.yml",
            "flow/flow.yml",
            ".gitlab/flow.yml",
            ".gitlab/.flow.yml",
            ".gitlab/ci/flow.yml",
            ".gitlab/flow/flow.yml",
        ]
        config_from_env = os.getenv(config_env_var, None)
        if config_from_env is not None:
            if os.path.exists(config_from_env):
                try:
                    with open(config_from_env, "r") as file:
                        cls.config = yaml.safe_load(file)
                        return None
                except Exception:
                    raise FlowConfigError(
                        f"Could not read yaml from FLOW_CONFIG_PATH: '{config_from_env}'"
                    )
            else:
                FlowLog.wrn(
                    f"Passed config file not found from FLOW_CONFIG_PATH: '{config_from_env}'"
                )
        for path in config_default_paths:
            config_path = f"{cls._root_dir}/{path}"
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r") as file:
                        cls.config = yaml.safe_load(file)
                        return None
                except Exception:
                    raise FlowConfigError(
                        f"Could not read yaml from flow config file: '{config_path}'"
                    )

        FlowLog.wrn("No config file found, using defaults")
        cls.config = dict()
        return None

    @classmethod
    def _validate_config(cls) -> None:
        for key, validator in cls._validators.items():
            value = cls.config.get(key, None)
            try:
                validated_value = validator(value)
                cls.config[key] = validated_value
            except FlowValidationError as e:
                FlowLog.err(e)

    # --------------------------------------
    # Callable functions
    # --------------------------------------

    @classmethod
    def ensure_directory(self, directory: str) -> None:
        """Creates subdirectory under the root directory Flow is called from"""
        root_dir_abs = os.path.abspath(self._root_dir)
        dir_path_rel = directory.lstrip("/")
        full_path = os.path.join(root_dir_abs, dir_path_rel)
        try:
            os.makedirs(full_path, exist_ok=True)
        except Exception:
            raise FlowError(f"Could not create directory: '{full_path}'")

    @classmethod
    def config_param(cls, config_key: str | None = None) -> Callable[[Any], Any]:
        """
        Decorator function used to assign a function
        as a validator and setter for a specific config key.

        If no argument is passed, it uses the function name as the key in configuration.
        The decorator will strip 'validate_' and 'param_' from the function name.

        The value returned will be the set config value.
        If the value is not valid, raise a FlowValidationError.
        """
        # Ensure no validators are declared after start
        if cls._started:
            raise FlowError("Validators must be declared before Flow is started")

        def wrapper(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            # Validate function
            sig = inspect.signature(func)
            params = sig.parameters
            if len(params) != 1:
                raise TypeError(
                    "A Config validator function must take exactly one argument for the value."
                )

            # Set config_key value
            if config_key is None:
                key = func.__name__.lstrip("validate_").lstrip("param_")
            else:
                key = config_key
            # Add validator to spec
            cls._validators[key] = func
            return func

        return wrapper

    @classmethod
    def start(cls) -> None:
        """
        Starts Flow

        Sets and validates configuration.
        """
        cls._get_config()
        cls._validate_config()
        # cls.ensure_directory(flow_dir_arg)
        cls._started = True
