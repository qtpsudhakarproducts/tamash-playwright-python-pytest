import os

import pytest
from dotenv import load_dotenv

load_dotenv()

# The reliable way to guarantee tamash-playwright's self-healing `page` fixture wins over
# pytest-playwright's own — pytest always prefers a conftest.py fixture over a same-named
# plugin fixture.
from tamash_playwright.plugin import page  # noqa: F401,E402


@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("APP_BASE_URL", "https://qtpsudhakar-vibetestq-hrm.up.railway.app/")


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    # Headed for local interactive runs (watching the browser is the whole point when developing
    # locally), headless in CI — GitHub Actions runners have no display server, and CI=true is
    # set automatically on every one of them (also true for most other CI providers), so this
    # needs no separate config to pick up.
    headless = bool(os.environ.get("CI"))
    return {**browser_type_launch_args, "headless": headless}
