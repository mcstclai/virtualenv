from __future__ import absolute_import, unicode_literals

import pytest

from virtualenv.interpreters.discovery.py_info import CURRENT
from virtualenv.run import run_via_cli
from virtualenv.seed.embed.wheels import BUNDLE_SUPPORT


@pytest.mark.slow
def test_base_bootstrap_via_pip_invoke(tmp_path, coverage_env):
    bundle_ver = BUNDLE_SUPPORT[CURRENT.version_release_str]
    create_cmd = [
        "--seeder",
        "pip",
        str(tmp_path / "env"),
        "--download",
        "--pip",
        bundle_ver["pip"].split("-")[1],
        "--setuptools",
        bundle_ver["setuptools"].split("-")[1],
        "--creator",
        "builtin",
    ]
    result = run_via_cli(create_cmd)
    coverage_env()
    assert result

    # uninstalling pip/setuptools now should leave us with a clean env
    site_package = result.creator.purelib
    pip = site_package / "pip"
    setuptools = site_package / "setuptools"
    wheel = site_package / "wheel"

    files_post_first_create = list(site_package.iterdir())
    assert pip in files_post_first_create
    assert setuptools in files_post_first_create
    assert wheel in files_post_first_create