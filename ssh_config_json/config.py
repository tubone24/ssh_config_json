import fnmatch
import getpass
import os
import re
import shlex
from os.path import expanduser, join
import base64
import json

DEFAULT_SSH_CONFIG = join(expanduser("~"), ".ssh/config")


class SSHConfig:
    """Dumping and restoring SSH Config"""

    SSH_CONFIG_GROUPS = re.compile(r"(\w+)(?:\s*=\s*|\s+)(.+)")

    def __init__(self, ssh_config=DEFAULT_SSH_CONFIG):
        """Constructor

        Args:
            ssh_config (str): SSH Config path [Default: ~/.ssh/config]
        """
        self._config = []
        if ssh_config == "~/.ssh/config":
            self.ssh_config = DEFAULT_SSH_CONFIG
        else:
            self.ssh_config = ssh_config

    def parse(self, save_key=False):
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
                    raise Exception("Unparsable line {}".format(line))
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
                        path = self.get_identity_file_path(value)
                        config_block.update({"IdentityFileContent": self.encode_identity_file_base64(path)})
            config_list.append(config_block)
        self._config = config_list
        return config_list

    def dump(self):
        return json.dumps(self._config, indent=4)

    def dump_file(self, filepath):
        with open(filepath, "w") as f:
            f.write(self.dump())

    def load_file(self, filepath):
        with open(filepath, "r") as f:
            self._config = json.loads(f.read())

    def restore(self, restore_key=False):
        with open(self.ssh_config, "w") as f:
            f.write(self.create_ssh_config_str(restore_key))

    def create_ssh_config_str(self, restore_key):
        write_line = []
        for config in self._config:
            if "Host" not in config and "Match" not in config:
                write_line.extend([f"{key} {value}" for key, value in config.items()])
            if "Host" in config:
                write_line.append(f"Host {config['Host']}")
                write_line.extend([f"    {key} {value}" for key, value in config.items() if key != "IdentityFileContent" and key != "Host"])
                if "IdentityFileContent" in config and "IdentityFile" in config and restore_key:
                    self.save_identity_file(config["IdentityFile"], config["IdentityFileContent"])
            if "Match" in config:
                write_line.append(f"Match {config['Match']}")
                write_line.extend([f"    {key} {value}" for key, value in config.items() if key != "IdentityFileContent" and key != "Match"])
        return "\n".join(write_line)

    @staticmethod
    def get_identity_file_path(path):
        if "~/" in path:
            path = path.replace("~/", "")
            return join(expanduser("~"), path)
        else:
            return path

    def save_identity_file(self, path, base64_content):
        self.decode_identity_file(self.get_identity_file_path(path), base64_content)

    @staticmethod
    def encode_identity_file_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")

    @staticmethod
    def decode_identity_file(path, base64_text):
        with open(path, "wb") as f:
            f.write(base64.b64decode(base64_text.encode("ascii")))
