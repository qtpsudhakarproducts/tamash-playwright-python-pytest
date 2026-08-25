from tamash_playwright.healer import get_healing_reports

# A genuinely non-unique element: two identical buttons, same accessible name, no id/label/
# landmark anywhere to tell them apart. Proves self-healing degrades safely on the hardest case
# it can face — it still recovers (clicks exactly one of them, never neither, never both), but it
# never silently claims full confidence about which one it picked. Self-contained, same reasoning
# as test_needs_review_healing.py.
REPEATED_BUTTON_HTML = """
<html><body>
  <div><button id="btn1" onclick="this.setAttribute('data-clicked', '1')">Yes</button></div>
  <div><button id="btn2" onclick="this.setAttribute('data-clicked', '1')">Yes</button></div>
</body></html>
"""


def test_a_non_unique_element_is_still_healed_but_never_silently_trusted(page):
    page.set_content(REPEATED_BUTTON_HTML)

    yes_button = page.locator("#doesNotExist").describe("Yes confirmation button")
    yes_button.click()

    # Exactly one of the two identical buttons received the click — not neither (heal failed),
    # not both (something replayed twice).
    clicked = page.locator('[data-clicked="1"]').count()
    assert clicked == 1

    report = get_healing_reports()[-1]
    assert report.healed is True

    # The invariant that must hold no matter which of the two buttons ended up picked: an element
    # with no stable identity of its own is always flagged for review, never trusted outright.
    assert report.needs_review is True
    assert "Yes" in (report.suggested_selector or "")
