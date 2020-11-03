"""SSH Config JSON
Overview:
  Dump JSON for your ssh config include IdentityFiles and restore those.

Usage:
  scj [-h|--help] [-v|--version]
  scj dump <file> [-c|--config=<config>] [-i|--identityFile]
  scj restore <file> [-c|--config=<config>] [-i|--identityFile]

Options:
  dump                       : dump SSH Config file to JSON
  restore                    : Restore SSH Config file from JSON
  <file>                     : Dumped json file
  -h, --help                 : Help
  -v, --version              : Show version
  -c, --config=<config>      : Specific SSH Config file path [default: ~/.ssh/config]
  -i, --identityFile         : Include IdentityFiles
"""

from docopt import docopt

try:
    from __init__ import __version__
except ModuleNotFoundError:
    from ssh_config_json.__init__ import __version__
try:
    from config import SSHConfig
except ModuleNotFoundError:
    from ssh_config_json.config import SSHConfig


def main():
    args = docopt(__doc__, version=f"SSH Config JSON: {__version__}")
    if args["dump"]:
        dump(
            args["<file>"],
            config=args["--config"][0],
            identity_file=args["--identityFile"],
        )
    elif args["restore"]:
        restore(
            args["<file>"],
            config=args["--config"][0],
            identity_file=args["--identityFile"],
        )
    else:
        print(__doc__)


def dump(filepath, config, identity_file=False):
    ssh_config = SSHConfig(config)
    ssh_config.parse(save_key=identity_file)
    ssh_config.dump_file(filepath)


def restore(filepath, config, identity_file=False):
    ssh_config = SSHConfig(config)
    ssh_config.load_file(filepath=filepath)
    ssh_config.restore(restore_key=identity_file)


if __name__ == "__main__":
    main()
