from os.path import expanduser, join
import logging
import sys
from unittest.mock import call
from unittest.mock import patch
from unittest.mock import MagicMock
import pytest

from docopt import DocoptExit
from ssh_config_json.main import main

_logger = logging.getLogger(name=__name__)


class TestMain:
    def setup_method(self, method):
        _logger.info("method{}".format(method.__name__))

    def test_main_nothing_args_show_usage(self):
        with pytest.raises(DocoptExit):
            main()

    def test_main_dump(self):
        del sys.argv[1:]
        sys.argv.append("dump")
        sys.argv.append("tests/assets/test_config_xxx")
        sys.argv.append("-c")
        sys.argv.append("tests/assets/test_config")
        with patch("builtins.open") as mock_open:
            main()
            mock_open.assert_any_call("tests/assets/test_config_xxx", "w")
            mock_open.assert_any_call("tests/assets/test_config")
        del sys.argv[1:]