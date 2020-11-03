# SSH Config JSON

`SSH Config JSON` is dumping JSON for your ssh config include IdentityFiles and restoring those.

## Description

`SSH Config JSON` enables you to pack and restore your SSH Config and Private Key in JSON format,
allowing you to backup, port to CI and share with others in the project.

## Getting Started

`SSH Config JSON` uses `The Python Package Index(Pypi)`, so that you can use `pip` installer.

```
$ pip install ssh-config-json
```

## Usage

You can use global command ``scj`` .

Show help.

```
$ scj -h
SSH Config JSON
Overview:
  Dump JSON for your ssh config include IdentityFiles and restore thos
Usage:
  scj [-h|--help] [-v|--version]
  scj dump <file> [-c|--config=<config>] [-i|--identityFile]
  scj restore <file> [-c|--config=<config>] [-i|--identityFil
Options:
  dump                       : dump SSH Config file to JSON
  restore                    : Restore SSH Config file from JSON
  <file>                     : Dumped json file
  -h, --help                 : Help
  -v, --version              : Show version
  -c, --config=<config>      : Specific SSH Config file path [default: ~/.ssh/config]
  -i, --identityFile         : Include IdentityFiles
```


Ex1) Dump your SSH Config to JSON

```
$ scj dump dump_config.json
```

Ex2) Dump your SSH Config to JSON with IdentityFiles

```
$ scj dump dump_config.json -i
```

Ex3) Restore JSON to SSH Config

```
$ scj restore dump_config.json
```

Ex4) Restore JSON to SSH Config with IdentityFiles

```
$ scj restore dump_config.json -i
```