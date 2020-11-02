from os.path import expanduser, join
import re
import logging
import json
from unittest.mock import call
from unittest.mock import patch
from unittest.mock import MagicMock

import pytest

from ssh_config_json.config import SSHConfig, InvalidConfigParseError

_logger = logging.getLogger(name=__name__)


class TestSSHConfig:
    def setup_method(self, method):
        _logger.info("method{}".format(method.__name__))

    def test_constructor_default_config(self):
        target = SSHConfig()
        assert target.ssh_config == join(expanduser("~"), ".ssh/config")

    def test_constructor_specify_config(self):
        target = SSHConfig("tests/assets/test_config")
        assert target.ssh_config == "tests/assets/test_config"

    def test_parse_ok(self):
        expected = [
            {},
            {
                "Host": "test1Server",
                "HostName": "test1.example.com",
                "IdentityFile": "tests/assets/test1.pem",
                "Port": "22",
                "User": "testuser",
                "ServerAliveInterval": "60",
                "StrictHostKeyChecking": "no",
                "UserKnownHostsFile": "/dev/null"
            },
            {
                "Host": "test2Server",
                "HostName": "test2.example.com",
                "Port": "22222",
                "ServerAliveInterval": "60",
                "StrictHostKeyChecking": "no",
                "User": "root",
                "UserKnownHostsFile": "/dev/null"
            },
            {
                "Match": 'exec "networksetup -getairportnetwork en0 | grep -q \'<SSID>\'"',
                "ProxyCommand": "connect -s -S <proxy server> -5 %h %p"
            }
        ]
        target = SSHConfig("tests/assets/test_config")
        actual = target.parse()
        assert actual == expected

    def test_parse_ok_with_comment(self):
        expected = [
            {},
            {
                "Host": "test1Server",
                "HostName": "test1.example.com",
                "IdentityFile": "tests/assets/test1.pem",
                "Port": "22",
                "User": "testuser",
                "ServerAliveInterval": "60",
                "StrictHostKeyChecking": "no",
                "UserKnownHostsFile": "/dev/null"
            },
            {
                "Host": "test2Server",
                "HostName": "test2.example.com",
                "Port": "22222",
                "ServerAliveInterval": "60",
                "StrictHostKeyChecking": "no",
                "User": "root",
                "UserKnownHostsFile": "/dev/null"
            },
            {
                "Match": 'exec "networksetup -getairportnetwork en0 | grep -q \'<SSID>\'"',
                "ProxyCommand": "connect -s -S <proxy server> -5 %h %p"
            }
        ]
        target = SSHConfig("tests/assets/test_config_with_comment")
        actual = target.parse()
        assert actual == expected

    def test_parse_ok_common_setting(self):
        expected = [
            {
                "ServerAliveInterval": "60"
            },
            {
                "Host": "test1Server",
                "HostName": "test1.example.com",
                "IdentityFile": "tests/assets/test1.pem",
                "Port": "22",
                "User": "testuser",
                "StrictHostKeyChecking": "no",
                "UserKnownHostsFile": "/dev/null"
            },
            {
                "Host": "test2Server",
                "HostName": "test2.example.com",
                "Port": "22222",
                "StrictHostKeyChecking": "no",
                "User": "root",
                "UserKnownHostsFile": "/dev/null"
            }
        ]
        target = SSHConfig("tests/assets/test_config_with_common_setting")
        actual = target.parse()
        assert actual == expected

    def test_parse_ok_with_identity_file(self):
        expected = [
            {},
            {
                "Host": "test1Server",
                "HostName": "test1.example.com",
                "IdentityFile": "tests/assets/test1.pem",
                "Port": "22",
                "User": "testuser",
                "ServerAliveInterval": "60",
                "StrictHostKeyChecking": "no",
                "IdentityFileContent": "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpuWEZuVkN1QXNZS1FKS3hLZ1R0MjRnZDdL"
                                       "ejhSYlpiY3pBWUM4Q2hiNk5RYjZiRC1adGYzNll4QkdHRzRFaE1TCjJGeVdIaEJ3aVl4Yk5ha2tMamV"
                                       "LS2thMkY1NTg2cGVpaVZjX0s3ckdnTGthTFpLdzRtN014WEdFQ0FjTnBUOUoKZTZUNWpYbU1paHRENU"
                                       "R4Rnd3a0dHM0hZNUNmeEQyLTJFZFlyUUVWdHhQSkNIUFRyeTc4dUZZTU40WF9Ec18tVgpjS1hwUjRCT"
                                       "ENNd00tUlRfTUtEUkNDenhCazJfYXppWm5EVUJlUG1TUEVwYlZjNjM3c04tMnNHVXpGRldaRXNtCmNY"
                                       "NWZTN3Q3WURlRzU5OEhOX2Rqc1JuNUw4WjlZV0RXZG5BTVp6Z1hMTTVUSERhUjNEaUFnNnRXQnpfX1N"
                                       "HWVUKZ1E3TlN0LWRaZnhaa1VDZ3VMNXVLejVZX1VQYkRLU1ZEZkRCUDhUal85azh3M2lVQWZ3eXlEN"
                                       "GZzOWVHem04SwpGQ2dFbWZncl9ZNGdIUHJmcEtrUmZKVzNmVW1OLWtGODhUZFBfMnc5WTl5ZjdhQVp"
                                       "ENTIyZjdzZ216U01KUGZyCk5jcFhDdzVLQzJyTHdQQ0tXYUNEWkxKOThGTV9LbUZITW1LaHRrNzlpT"
                                       "Vh3UVpTOG5wVEY4LTQ4YjVHMk1tRFcKaDJYYmZELWpINXJZMlFMOURTR3M2WGstbXJiUmVaTi1YbUp"
                                       "qd0EycjZkTkZpWC1teHdtSHJHLUdVa1BOU3c1UQp5VkxLRS1lajlHaTlwZlItM24tOW5oZV9TUmppR0"
                                       "5VRWlhMzM4NFYzbnVuQ2hkVlVtd1NVdExVNUVzRmFaeWozCjVIUmlWQUhyZGRLanNkZFR1RDJVOHR"
                                       "MVFhNVllVVkZMOC1pVmFjZlJFZXJFR0FMN0Y0OVB4SmZYM0Q5VnRXUXcKQXV0WUdKaTZ1VkFqNngz"
                                       "ZHRhc1B6NVJjdXhrZFBkR3J5cE1jUTNDMkJoQWlXTWtjLVpUa3h5cnpwUDRNQUVYdQo1RnJaVVlFV2"
                                       "Y4Y2ZyZXd5U24tbm03NGtVY1o4elpQX0NQWk1QbXdoTFFoc0ZiRi1NcnVFR3htQVJaSDh3UG1GCjZR"
                                       "RXBUX2VpVzM0Uzh5N3BMcnJ4WFJIU3VyX1A5cE54LTU5R2hYc1Q3YTZnekhlallXMlZHX0dzUjZYS"
                                       "HNEYVIKdDlZekRybmYycC1QQnhnMmdEN0RaUHIzNi1XRDhaX01aX3NYUGtlaVVTQjhtSi1hY1ptU01"
                                       "jRTZIU2NMOUNrSgphVGJUbm4ycFJRZms1dTNlVzZiN3JWTkZOUUtnSEFpUXQ5MnNnbnJNWUpzVXB6e"
                                       "m1OUDVha2JBclhpWmZrVHk0CnBmejN6RkhBZU02ZmZyX0VTemFURTdmWmNRdWM4MlN6ZFV0Y05ENndZ"
                                       "bVprMjdjU1dmQ2tOVnBIMmFwQjVXWlMKWnc1Y0Z0ZS1HcHpQVFBtNUVGZ3NGNHRMRjlUajJUZzhfd"
                                       "3NSWGNRRDkzaWV0eUpLNGNRRWduQUJjQWlia3dSLQpXNXRUS0dnYW1yVGVUbjhTYThhVzJfQUpQOFF"
                                       "aaERMS0d1VGQ3MmE2NmZSTS1CZXhoVlluaTRZUjdkZVA1SkRCCm5kaG1VVzNoV1hicmlEMm1Xa056b"
                                       "lY3aHlSbTZpSmlDY0NHemdOWlA4c0NtUVBzSnhNYkIyWW4zRkJYRGNCWUwKTjNhZDk5QWM4ODJHazVm"
                                       "dWV6eGM2ZEx4M2lFeVlnYWFYUU11MjJfa3U0a0tlOUZCOG5yQVhGNkJmcDIzY3p6ZQo2NGtwcjdmY"
                                       "1RwelNrM0d4Ynl4eDNuTTgzZl80ZlVreFFpZURBa1J5OWt5NDlQZzdyTWdfYVJ6ZEFBS2FOeXN6CnV"
                                       "ZQVM1eWc3Q0xBUnhHd3Jra3BORlRkM3pXa1Zoenk0TTlNaWk5eHB5QkdzNXV4ZG1Qa1R6RkhpRDNwa"
                                       "XVYeEEKaDU3dS1nRGVGbWc0eGVRLThILUNRTVY0SGdyaDYyY3hmRmZ5R2VHeVVYWVYyd2R4XzVHdD"
                                       "daOU54N0RYcGdiVQo2VTUtekQtNGJoemt4bjhjMlg1a0xiOExGcGVGV2gzYzJHWjZHOHNzeTg5N1VB"
                                       "Y01qR3hLVDlGOVczWG00RXQ5ClZ4NDJWXzRtOFN0aG41M0p1X2tkejdZRi1fUXI0Q2prVkF4LUJhSn"
                                       "N5WnREc0R4LWNMcndaRWlMZEtRQ3BHN2kKOUZQYVZBdENueFdpY250cFB3SGpVY1FHVzJEVmJfYVRz"
                                       "QmtZWWNudUZGZkdlU2FoaEpuMlB6ZnRCUlBqRFAtWQphbXV4V1luR0M0S3RZMlI3YlQ2NktuNEtKZ0"
                                       "F5VkVqaTJMelBMeVJ0d0RwRWM3XzhiN3Bmd0ZkZ3hXVGtuQ0cyCkVOUE1UZlNqS0hOZEFrRmZtSlVS"
                                       "RDVRSmV3WGhFRkc3TUJHYk15TUtVYV9iNHJ0YkJ6YzRRYjJBeTliMjV0TTkKTGFKU2JUY1Y4M3dMNkV"
                                       "qNDhjdVkzWnlIQTNKbWtCUFFFc1ltckVhUHhhZnVjN0Q4QzloSjdKbWFfTVgzR3RNbgpWZjl3ZUZVNk"
                                       "11QzY5RGNjZ0NCTldpX2ZKWTUta0FUY3VQUjNIZURmUzVwRjR1bkFuRmFKcmYtODl5dUh5Q0o2CkFQN"
                                       "TdTX2VaWUg0VE1XVExZTmo4TE5VZ3VuLWdoUVBTRjl3ZGQ3UGJtVUdEMnpBV1JCVFVtR3NmUEhQNEtk"
                                       "YUgKcGpYSl8ySkZVR2ZpaXhHalZlaVJ5Z2RLeURjaXVheHlLQVdKVVRkdFI1czRrc2hZS1hFcnhnckE"
                                       "zQmNzLURfawpHZy1DRkFjelB0RzlKbkNtZTkyWGRBOVpOWVFkbVNGRHltOWdwWWtBM0t6QTVncFYzQ"
                                       "jVSQ05YLVVyYXVBWWtuCk5lUUNBNk1zZVpqMldCZjJuQ2p4cmZwN1dBbnB1em1OaF9yQ2tETkFBNUF"
                                       "tTWs4SmpIYWJOa01ZX2l1WGJ1RzYKZXlaOWpCbnh6NFlmR3NlQWJ5RmZhYkFCaUFaVWdGeFpoRWo3a"
                                       "l9NbWVfblVoa1p6V3c5Szc0UHp6QUpfYVVaTgpKNVBfQUJqTEdNLUh1MkNndWdOX2FQRWs0empKRVN"
                                       "XQ3RDal9wRDVjY05fTl84NEJCZlBDYm1OYUMtVUJGNDJrCnBjYkozRml5Y2FOSFJMSjVEVHNmLVp3T"
                                       "mU3YkZlVTczdTJiTFJCU2lNVmdlcmllM1pEVFV1azVaeXlpQVNRSEEKTW5CaFZuaXRFWFZDSEZoRHh"
                                       "pUzJwNGFiUE1NY3VCWl9XdWpZM2Q3WmRKUnRWTGFmaVY4VmVwREV1RVF1eWtDMwpkbjdTQ0FwQVR6e"
                                       "nJkbUw1UGhFdFZYTUE1ZEJGcGNiQlZYejdGQ1lLNk4tcm13V0U0NUxLaFl5LTVkLVlGbkpmCnBmRlB"
                                       "pSlN5NUQzQVFERWRlWlhhYVVibldGd0Y4VWpDSEVZTmhoTFRqR0NQaUhnVlR3cjJCV3NQVWhBeWlYaz"
                                       "MKd3BTc2ZFRHN5dGs3YjhCVnU5TlVTNXlVa2taUGJBelBMYWFBVV9IYmdzUmtHZ193aHM0VWlGdUFN"
                                       "V1RtU2Z4UwpRUXVzWHlWeWRZNjQ1aWVKUnVNUGl1cnBMR0RERFJ3RjI1TEFUc3VXaU5aaTMtZ0RWbj"
                                       "N3YjZkREtodXJrM2VZCk1HTFFLNi1rNkU5NEdSRUNHdFRZdHpROVdiNE5Nc2pDaGpVbmg4eDU5LWti"
                                       "VHI5V2pOV2VXNGI5RVhSRmVCdGUKUy1DV0pSNC1RWTdiMlFKeEdURFdaZ1ZXLTVIdENHZC1kQW11aG"
                                       "1XRzViZEtqYzQ4ZzgtTVlZZ2RNajhHZlNYSApfbmRSTDkzbjgyTGZNSDllRV9zRkNkZ0N3R3AtcGRT"
                                       "aVpWTXVOeXBVUEEyZVhnTDRTOFFUek5Ld1R5N3hENndTClYyVllRUVdLR2NGWDVfZ0FrSm5GVnJ4aX"
                                       "JDTnJyX2lzTUZTMnA3Q0hoUXMzTWlZNDdkZ1ZaMjZoa2ttSG0zeVAKa202VHpBUTZXd2ZBWnBIRk51U"
                                       "3I0SExiSEhZaFpqZTVhUmhBTDJ6YlZCcjhLLWtnS3JtYTg1eU1NeUt4X3BMNwpURkVqN2dhVEtGNlhL"
                                       "Q3VKeVZSNlg2SmdodUxCSk4tOTJlRlNQZ3dfSy1IbWhwR0pwN2hRNTVHR3drTUo2RTktCi0tLS0tRU"
                                       "5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg==",
                "UserKnownHostsFile": "/dev/null"
            },
            {
                "Host": "test2Server",
                "HostName": "test2.example.com",
                "Port": "22222",
                "ServerAliveInterval": "60",
                "StrictHostKeyChecking": "no",
                "User": "root",
                "UserKnownHostsFile": "/dev/null"
            },
            {
                "Match": 'exec "networksetup -getairportnetwork en0 | grep -q \'<SSID>\'"',
                "ProxyCommand": "connect -s -S <proxy server> -5 %h %p"
            }
        ]
        target = SSHConfig("tests/assets/test_config")
        actual = target.parse(save_key=True)
        assert actual == expected

    def test_parse_exception_invalid_config(self):
        target = SSHConfig("tests/assets/test_config_invalid")
        with pytest.raises(InvalidConfigParseError):
             target.parse()

    def test_dump_file_ok(self):
        with patch("builtins.open") as mock_open, patch("json.dumps") as mock_json_dumps:
            target = SSHConfig("tests/assets/test_config")
            expected = [
                {},
                {
                    "Host": "test1Server",
                    "HostName": "test1.example.com",
                    "IdentityFile": "tests/assets/test1.pem",
                    "Port": "22",
                    "User": "testuser",
                    "ServerAliveInterval": "60",
                    "StrictHostKeyChecking": "no",
                    "UserKnownHostsFile": "/dev/null"
                },
                {
                    "Host": "test2Server",
                    "HostName": "test2.example.com",
                    "Port": "22222",
                    "ServerAliveInterval": "60",
                    "StrictHostKeyChecking": "no",
                    "User": "root",
                    "UserKnownHostsFile": "/dev/null"
                },
                {
                    "Match": 'exec "networksetup -getairportnetwork en0 | grep -q \'<SSID>\'"',
                    "ProxyCommand": "connect -s -S <proxy server> -5 %h %p"
                }
            ]
            target._config = expected
            target.dump_file("test.json")
            mock_open.assert_any_call("test.json", "w")
            mock_json_dumps.assert_called_once_with(expected, indent=4)

    def test_load_file_ok(self):
        target = SSHConfig("tests/assets/test_config")
        target.load_file("tests/assets/test.json")
        expected = [
            {},
            {
                "Host": "test1Server",
                "HostName": "test1.example.com",
                "IdentityFile": "tests/assets/test1.pem",
                "Port": "22",
                "User": "testuser",
                "ServerAliveInterval": "60",
                "StrictHostKeyChecking": "no",
                "UserKnownHostsFile": "/dev/null"
            },
            {
                "Host": "test2Server",
                "HostName": "test2.example.com",
                "Port": "22222",
                "ServerAliveInterval": "60",
                "StrictHostKeyChecking": "no",
                "User": "root",
                "UserKnownHostsFile": "/dev/null"
            },
            {
                "Match": 'exec "networksetup -getairportnetwork en0 | grep -q \'<SSID>\'"',
                "ProxyCommand": "connect -s -S <proxy server> -5 %h %p"
            }
        ]
        assert target._config == expected

    def test_restore(self):
        target = SSHConfig("tests/assets/test_config")
        with patch("builtins.open") as mock_open, patch.object(target, "create_ssh_config_str") as mock_create_ssh_config_str:
            target._config = [
                {},
                {
                    "Host": "test1Server",
                    "HostName": "test1.example.com",
                    "IdentityFile": "tests/assets/test1.pem",
                    "Port": "22",
                    "User": "testuser",
                    "ServerAliveInterval": "60",
                    "StrictHostKeyChecking": "no",
                    "UserKnownHostsFile": "/dev/null"
                },
                {
                    "Host": "test2Server",
                    "HostName": "test2.example.com",
                    "Port": "22222",
                    "ServerAliveInterval": "60",
                    "StrictHostKeyChecking": "no",
                    "User": "root",
                    "UserKnownHostsFile": "/dev/null"
                },
                {
                    "Match": 'exec "networksetup -getairportnetwork en0 | grep -q \'<SSID>\'"',
                    "ProxyCommand": "connect -s -S <proxy server> -5 %h %p"
                }
            ]
            target.restore()
            mock_open.assert_any_call("tests/assets/test_config", "w")
            mock_create_ssh_config_str.assert_called_once_with(False)
