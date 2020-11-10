import logging
import os
import shutil

import pytest
from ssh_config_json.main import dump, restore, encrypt, decrypt

_logger = logging.getLogger(name=__name__)


class TestItMain:

    @staticmethod
    def copy_file(directory):
        test_config = os.path.join(os.path.dirname(__file__), "../assets", "test_config")
        test_pem = os.path.join(os.path.dirname(__file__), "../assets", "test1.pem")
        test_json = os.path.join(os.path.dirname(__file__), "../assets", "test.json")
        test_config_restore = os.path.join(os.path.dirname(__file__), "../assets", "test_config_restore")
        shutil.copy2(test_config, directory)
        shutil.copy2(test_pem, directory)
        shutil.copy2(test_json, directory)
        shutil.copy2(test_config_restore, directory)
        return True

    @pytest.mark.it
    def test_it_dump(self, tmpdir):
        _logger.debug("Temp directory: {tmp_dir}".format(tmp_dir=tmpdir))
        self.copy_file(tmpdir)
        json_path = os.path.join(tmpdir, "test_config.json")
        config_path = os.path.join(tmpdir, "test_config")
        expected_json_path = os.path.join(tmpdir, "test.json")
        dump(json_path, config_path, identity_file=False)
        with open(json_path, "r") as f1, open(expected_json_path, "r") as f2:
            actual = f1.read()
            expected = f2.read()
            assert actual == expected

    @pytest.mark.it
    def test_it_dump_with_encrypt(self, tmpdir):
        _logger.debug("Temp directory: {tmp_dir}".format(tmp_dir=tmpdir))
        self.copy_file(tmpdir)
        json_path = os.path.join(tmpdir, "test_config.json")
        config_path = os.path.join(tmpdir, "test_config")
        expected_json_path = os.path.join(tmpdir, "test.json")
        dump(json_path, config_path, identity_file=False)
        encrypt(json_path, key="test")
        decrypt(json_path + ".enc", key="test")
        with open(json_path, "r") as f1, open(expected_json_path, "r") as f2:
            actual = f1.read()
            expected = f2.read()
            assert actual == expected

    @pytest.mark.it
    def test_it_restore(self, tmpdir):
        _logger.debug("Temp directory: {tmp_dir}".format(tmp_dir=tmpdir))
        self.copy_file(tmpdir)
        expected_config_path = os.path.join(tmpdir, "test_config_restore")
        config_path = os.path.join(tmpdir, "test_config")
        json_path = os.path.join(tmpdir, "test.json")
        restore(json_path, config_path, identity_file=False)
        with open(config_path, "r") as f1, open(expected_config_path, "r") as f2:
            actual = f1.read()
            expected_line = f2.readline()
            for expected in expected_line:
                _logger.info("Check string: {check_string}".format(check_string=expected))
                assert expected in actual
