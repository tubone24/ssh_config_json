import re
from os.path import expanduser, join
import base64
import json
import logging
from typing import List, Dict, AnyStr

_logger = logging.getLogger(name=__name__)
DEFAULT_SSH_CONFIG = join(expanduser("~"), ".ssh/config")


class BaseError(Exception):
    """Base error
    """

    pass


class InvalidConfigParseError(BaseError):
    """config::InvalidConfigParseError
    """

    def __init__(self, error_class, message):
        self.error_class = error_class
        self.message = message

    def __str__(self):
        return "{error_class}: {message}".format(
            error_class=self.error_class, message=self.message
        )


class SSHConfig:
    """Dumping and restoring SSH Config"""

    SSH_CONFIG_GROUPS = re.compile(r"(\w+)(?:\s*=\s*|\s+)(.+)")

    def __init__(self, ssh_config: AnyStr = DEFAULT_SSH_CONFIG):
        """Constructor

        Args:
            ssh_config (str): SSH Config path [Default: ~/.ssh/config]
        """
        self._config = []
        if ssh_config == "~/.ssh/config":
            self.ssh_config = DEFAULT_SSH_CONFIG
        else:
            self.ssh_config = ssh_config

    def parse(self, save_key: bool = False) -> List[Dict[str, str]]:
        """Parse SSH Config

        Args:
            save_key(bool): Include IdentityFiles to JSON IdentityFileContent

        Returns:
            List[Dict[str, str]]: ConfigList
        """
        with open(self.ssh_config) as f:
            config_list = []
            config_block = {}
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                match = re.match(self.SSH_CONFIG_GROUPS, line)
                if not match:
                    raise InvalidConfigParseError(
                        "InvalidConfigParseError", "Unparsable line {}".format(line)
                    )
                key = match.group(1)
                value = match.group(2)
                if key == "Host":
                    config_list.append(config_block)
                    config_block = {}
                    config_block.update({key: value})
                elif key == "Match":
                    config_list.append(config_block)
                    config_block = {}
                    config_block.update({key: value})
                else:
                    config_block.update({key: value})
                    if key == "IdentityFile" and save_key:
                        path = self._get_identity_file_path(value)
                        config_block.update(
                            {
                                "IdentityFileContent": self._encode_identity_file_base64(
                                    path
                                )
                            }
                        )
            config_list.append(config_block)
        self._config = config_list
        return config_list

    def _dump(self):
        return json.dumps(self._config, indent=4)

    def dump_file(self, filepath: AnyStr):
        """Dump SSH Config Object to JSON

        Args:
            filepath(str): Output filepath
        """
        with open(filepath, "w") as f:
            f.write(self._dump())
        _logger.info(f"Dump JSON: {filepath}")

    def load_file(self, filepath: AnyStr):
        """Load JSON to SSH Config Object

        Args:
            filepath: Input filepath
        """
        with open(filepath, "r") as f:
            self._config = json.loads(f.read())

    def restore(self, restore_key: bool = False):
        """Restore SSH Config Object to SSH Config

        Args:
            restore_key: Restore IdentityFile
        """
        with open(self.ssh_config, "w") as f:
            f.write(self.create_ssh_config_str(restore_key))
        _logger.info(f"Dump Config: {self.ssh_config}")

    def create_ssh_config_str(self, restore_key: bool):
        """Create SSH Config File string

        Args:
            restore_key: Restore IdentityFile
        """
        write_line = []
        for config in self._config:
            if "Host" not in config and "Match" not in config:
                write_line.extend([f"{key} {value}" for key, value in config.items()])
            if "Host" in config:
                write_line.append(f"Host {config['Host']}")
                write_line.extend(
                    [
                        f"    {key} {value}"
                        for key, value in config.items()
                        if key != "IdentityFileContent" and key != "Host"
                    ]
                )
                if (
                    "IdentityFileContent" in config
                    and "IdentityFile" in config
                    and restore_key
                ):
                    self._save_identity_file(
                        config["IdentityFile"], config["IdentityFileContent"]
                    )
            if "Match" in config:
                write_line.append(f"Match {config['Match']}")
                write_line.extend(
                    [
                        f"    {key} {value}"
                        for key, value in config.items()
                        if key != "IdentityFileContent" and key != "Match"
                    ]
                )
        return "\n".join(write_line)

    @staticmethod
    def _get_identity_file_path(path: AnyStr):
        if "~/" in path:
            path = path.replace("~/", "")
            return join(expanduser("~"), path)
        else:
            return path

    def _save_identity_file(self, path: AnyStr, base64_content: str):
        self._decode_identity_file(self._get_identity_file_path(path), base64_content)

    @staticmethod
    def _encode_identity_file_base64(path: AnyStr) -> str:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")

    @staticmethod
    def _decode_identity_file(path: AnyStr, base64_text: str):
        with open(path, "wb") as f:
            f.write(base64.b64decode(base64_text.encode("ascii")))
