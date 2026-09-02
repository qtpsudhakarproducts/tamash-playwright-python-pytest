# tamash-playwright-python-pytest

This repository is a public example of how to use [`tamash-playwright`](https://pypi.org/project/tamash-playwright/) with `pytest` and `pytest-playwright`.

It demonstrates both styles:

- a simple test without page objects
- a Page Object Model (POM) flow using reusable page classes

The goal is to show how the self-healing Playwright experience works in a real project and how to run it end-to-end.

## Repository structure

- `tests/test_sampletest.py` — simple test using direct locators
- `tests/test_pomtest.py` — test using page objects in the `pages/` folder
- `pages/` — reusable page classes for login, dashboard, employee creation, etc.
- `conftest.py` — overrides the default `page` fixture with the self-healing version from `tamash_playwright`
- `.env.example` — environment variables for the AI provider and app URL
- `report.html` — generated test report after running pytest

---

## Step 1: Install prerequisites

Make sure Python 3.9+ is installed.

```bash
python --version
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install this example repo and its dependencies:

```bash
pip install -U pip
pip install -e .
```

This installs:

- `pytest`
- `pytest-playwright`
- `pytest-html`
- `tamash-playwright`
- `python-dotenv`

---

## Step 2: Configure environment variables

Copy the example environment file:

```bash
copy .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

Open `.env` and configure the values:

```env
HEALER_ENABLED=true
HEALER_PROVIDER=ollama
OLLAMA_MODEL=gpt-oss:120b
OLLAMA_API_KEY=
APP_BASE_URL=https://qtpsudhakar-vibetestq-hrm.up.railway.app/
```

You can use one of the supported providers:

- `ollama` / `ollama-local` (your own self-hosted Ollama server)
- `openai` / `anthropic` / `gemini`
- `tamash` — rule-based healing, no AI, no key at all
- `claude-subscription` / `copilot-subscription` — uses an existing subscription login, no API key
- `cursor-subscription` / `kiro-subscription` / `codex-subscription` — subscription-based, **local development only**

Full setup for every one of these (auth, env vars, CI support) is in the
[provider docs](https://qtpsudhakarproducts.github.io/tamash-playwright-support/providers.html).

Example for OpenAI:

```env
HEALER_PROVIDER=openai
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4.1-mini
```

The `APP_BASE_URL` is the base URL of the application you want to test.

> If you are using Ollama locally, make sure the model is pulled and accessible before running the tests.

Confirm everything's wired up correctly before running any tests:

```bash
tamash-playwright doctor
```

It calls your configured provider for real, flags locators missing a `.describe()` label, and tells you exactly what's wrong (and the fix) if anything's off.

---

## Step 3: Install Playwright browser binaries

```bash
playwright install chromium
```

This is required for browser automation.

---

## Step 4: Create your first test

This repo already contains example tests that show how to use the package.

### Example 1: Simple test without POM

See `tests/test_sampletest.py`:

```python
from playwright.sync_api import expect


def test_login_using_css_selectors(page):
    page.goto("/")

    txt_username = page.locator('input[name="username1"]').describe("User Name Textbox")
    txt_username.fill("testadmin")

    txt_password = page.locator("input[placeholder='Password']").describe("Password Textbox")
    txt_password.fill("Vibetestq@123#")

    btn_login = page.locator("button[type='submit']").describe("Login Button")
    btn_login.click()

    expect(page.locator("h6")).to_have_text("Dashboard")
```

This is intentionally using a slightly broken selector (`username1`) to demonstrate the self-healing behavior of `tamash-playwright`.

### Example 2: Page Object Model flow

See `tests/test_pomtest.py` and the files in `pages/`.

The test does this:

```python
base_page = BasePage(page)
login_page = LoginPage(page)
dashboard_page = DashboardPage(page)
pim_page = PIMPage(page)
add_emp_page = AddEmployeePage(page)
personal_details_page = PersonalDetailsPage(page)
```

Then it performs the login and employee creation flow using page object methods instead of inline locators.

This is the recommended structure for maintainable test automation projects.

---

## Step 5: Run the tests

Run all tests:

```bash
pytest -v
```

Run a single file:

```bash
pytest tests/test_sampletest.py -v
pytest tests/test_pomtest.py -v
```

Run a single test by name:

```bash
pytest tests/test_sampletest.py -k login -v
```

The project is configured in `pyproject.toml` to generate two HTML reports automatically:

```toml
[tool.pytest.ini_options]
addopts = "--html=report.html --self-contained-html --tamash-report=tamash-report.html"
```

---

## Step 6: Check the results

Two reports come out of every run, and they show different things:

- **`report.html`** (`pytest-html`) — the standard pass/fail summary, durations, and captured output.
- **`tamash-report.html`** (`tamash-playwright`'s own) — a step-by-step trace of every action, assertion, network call, and fixture, in order. This is the one that shows self-healing in detail: which provider recovered a broken locator, what it recovered *to*, token usage, and the full `attempts:` history (cache/ref/text/vision/action-recovery) when more than one attempt was made.

Open either directly in a browser to inspect the results.

---

## What tamash-playwright does automatically

When a selector fails, the package captures an accessibility snapshot, asks the configured LLM provider to suggest the correct element, retries once, and logs the recovery.

Example log output:

```text
[self-healer] Recovered using ollama:gpt-oss:120b (placeholder "Username").
```

This is the core value of `tamash-playwright`: it reduces broken selector maintenance caused by UI changes.

Runtime healing never edits your source, though — the broken locator stays broken and gets re-healed on every run until you fix it. To make a heal permanent:

```bash
tamash-playwright apply-heals --dry-run   # preview the source rewrite
tamash-playwright apply-heals             # write it, and generate a verification script
python .tamash-playwright/verify_heals.py # re-run just the affected tests with healing off
```

See the [Making heals permanent](https://qtpsudhakarproducts.github.io/tamash-playwright-support/apply-heals.html) guide for the full mechanics. If you'd rather hand this whole loop (setup → run → review → apply → verify) to an AI coding agent, `tamash-playwright init-skill` installs a packaged skill that teaches it — see [The AI agent skill](https://qtpsudhakarproducts.github.io/tamash-playwright-support/agent-skill.html).

---

## Typical workflow for a new project

1. Install the dependency:

```bash
pip install tamash-playwright pytest-playwright pytest-html python-dotenv
```

2. Add a `conftest.py` file that imports the self-healing `page` fixture:

```python
from tamash_playwright.plugin import page  # noqa: F401
```

3. Set your environment variables in `.env`.
4. Create tests using Playwright with the self-healing `page` fixture.
5. Run `pytest`.
6. Open the generated `report.html` file for test results.

---

## Summary

This repository is a ready-to-run public example of how to integrate `tamash-playwright` into a `pytest` project.

It shows:

- installation
- environment configuration
- creating tests
- executing them
- reading results from HTML reports

## Support and feedback

For questions, doubts, issues, or feature requests, please use:

https://github.com/qtpsudhakarproducts/tamash-playwright-support/issues

This is the place to raise support questions and discuss improvements with the project maintainers.
- self-healing locator recovery in action

If you want to build your own project, copy the pattern in this repo and replace the app URL and test logic with your own application flow.
