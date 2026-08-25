from tamash_playwright import expect
from tamash_playwright.healer import get_healing_reports

# Demonstrates the OTHER half of self-healing beyond a simple broken-placeholder fix (see
# test_sampletest.py / test_pomtest.py for that): the widening search that kicks in when an
# element has no id/name/testid/aria-label/placeholder of its own to key off of — the exact shape
# of a real OrangeHRM "Employee Id" field (a bare <input> with a sibling <label>, no <label for>
# association). Self-contained via page.set_content() rather than the live demo site, so this
# stays deterministic regardless of what that site's current DOM looks like.
EMPLOYEE_ID_FORM_HTML = """
<html><body>
  <div class="oxd-input-group">
    <label class="oxd-label">First Name</label>
    <input class="oxd-input" id="firstName">
  </div>
  <div class="oxd-input-group">
    <label class="oxd-label">Employee Id</label>
    <input class="oxd-input">
  </div>
</body></html>
"""


def test_healing_anchors_on_nearby_text_when_the_field_has_no_identity_of_its_own(page):
    page.set_content(EMPLOYEE_ID_FORM_HTML)

    # Deliberately broken — there's no placeholder on the real element either, so this always
    # fails and always needs a real heal, not a lucky match.
    employee_id_input = page.get_by_placeholder("Employee").describe("Employee Id Textbox")
    employee_id_input.fill("72900")

    # The field that actually matters: did healing land on "Employee Id", not "First Name" right
    # next to it?
    expect(page.locator("#firstName")).to_have_value("")
    employee_id_locator = page.locator(".oxd-input-group", has_text="Employee Id").locator("input")
    expect(employee_id_locator).to_have_value("72900")

    report = get_healing_reports()[-1]
    assert report.healed is True

    # No id/name/testid/aria-label/placeholder means normalize()'s own "self" identity check has
    # nothing to key off of, so the widening search anchoring on "Employee Id" is what has to do
    # the real work here — which is exactly why this heal is flagged needs_review (a
    # nearby-text anchor is real and verified, just inherently less stable than a real identity)
    # rather than trusted outright the way a role/testId/label match would be.
    assert report.needs_review is True
    assert "Employee Id" in (report.suggested_selector or "")
