from os.path import expanduser, join
import logging
from unittest.mock import call
from unittest.mock import patch
from unittest.mock import MagicMock
import pytest

from ssh_config_json.encrypt import AESCipher

_logger = logging.getLogger(name=__name__)


class TestAESCipher:
    def setup_method(self, method):
        _logger.info("method{}".format(method.__name__))

    def test_init_ok_with_key(self):
        target = AESCipher(key="test")
        assert target.key == b"d3b0aa9cd8b7255622cebc631e867d40"

    def test_init_ok_with_key_key_num(self):
        target = AESCipher(key="test", key_num=64)
        assert target.key == b"d3b0aa9cd8b7255622cebc631e867d40"

    def test_init_ok_without_key(self):
        target = AESCipher()
        assert len(target.key) == 32
        assert target.key.decode("utf-8").isalnum()

    def test_init_ok_without_key_key_num(self):
        target = AESCipher(key_num=64)
        assert len(target.raw_key) == 64
        assert target.raw_key.isalnum()
        assert len(target.key) == 32
        assert target.key.decode("utf-8").isalnum()

    def test_encrypt_decrypt(self):
        target = AESCipher(key="test")
        actual_encrypt = target.encrypt("test")
        assert type(actual_encrypt) is bytes
        actual_decrypt = target.decrypt(actual_encrypt)
        assert actual_decrypt == "test"

