# tamash-playwright-python-pytest

Example usage of [`tamash-playwright`](https://pypi.org/project/tamash-playwright/) with **pytest** (via `pytest-playwright`) — with and without the Page Object Model.

## Structure

- `tests/test_sampletest.py` — no page objects; locators declared directly in the test body.
- `tests/test_pomtest.py` — Page Object Model; page objects are instantiated directly with the self-healing `page` fixture.
- `pages/` — page object classes.
- `conftest.py` — imports `tamash_playwright.plugin.page` to override pytest-playwright's `page` fixture with the self-healing version, and sets `base_url`/`headless` defaults.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate    # or: source .venv/bin/activate
pip install -e .
cp .env.example .env
# fill in an AI provider key in .env (Ollama/OpenAI/Anthropic/Gemini)
playwright install chromium
```

## Run

```bash
pytest -v
```

## How self-healing shows up

When a selector fails, `tamash-playwright` captures an ARIA snapshot, asks the configured AI provider for a replacement, retries the action once, and prints a line like:

```
[self-healer] Recovered using ollama:gpt-oss:120b (placeholder "Username").
```
