# SSH Config JSON

`SSH Config JSON` is dumping JSON for your ssh config include IdentityFiles and restoring those.

## Description

`SSH Config JSON` enables you to pack and restore your SSH Config and Private Key in JSON format,
allowing you to backup, put to CI and share with others in the project.

## Features

- Dumping your SSH Config to JSON and restore it
- Packing up IdentityFiles with the JSON
- AES encrypting with the JSON to enable pushing and saving public GitHub Repository

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
  Dump JSON for your ssh config include IdentityFiles and restore those.

Usage:
  scj [-h|--help] [-v|--version]
  scj dump <file> [-c|--config=<config>] [-i|--identityFile]　[-e|--encrypt] [--key=<key>]
  scj restore <file> [-c|--config=<config>] [-i|--identityFile]　[-d|--decrypt=<key>]

Options:
  dump                       : dump SSH Config file to JSON
  restore                    : Restore SSH Config file from JSON
  <file>                     : Dumped json file
  -h, --help                 : Help
  -v, --version              : Show version
  -c, --config=<config>      : Specific SSH Config file path [default: ~/.ssh/config]
  -i, --identityFile         : Include IdentityFiles
  -e, --encrypt              : Encrypt JSON dump with AES
  --key=<key>                : Set specify key string
  -d, --decrypt=<key>        : Decrypt JSON dump with AES
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

Ex5) Dump your SSH Config to JSON with AES Encrypt

```
$ scj dump dump_config.json -i -e
Encrypt key: 1mado1wmf9amsie0jvo0kfmai9cjasfv # <= This is the "Key"!!
```

Ex6) Decrypt it

```
$ scj restore dump_config.json -i -d 1mado1wmf9amsie0jvo0kfmai9cjasfv
```

## Documents

The Document is <https://ssh-config-json.readthedocs.io/en/latest/> written by mkdocs. (This Site!)

The PyPI page is <https://pypi.org/project/ssh-config-json/> .

The GitHub page is <https://github.com/tubone24/ssh_config_json> .