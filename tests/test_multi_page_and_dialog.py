from tamash_playwright import expect
from tamash_playwright.healer import get_healing_reports

# Two capabilities in one test, both "no extra setup needed" per the README's "What gets
# reported": a second page a test opens itself (context.new_page() here, same as a popup or a
# target="_blank" link) is automatically healing/reporting-aware the moment it's created, via the
# browser context's own "page" event — not just the one page the `page` fixture handed you. And a
# page.on("dialog", ...) handler is tracked and reported the same way any other step is.
# Self-contained via page.set_content(), same reasoning as the other synthetic-content tests here.


def test_a_second_page_opened_by_the_test_heals_and_reports_the_same_as_the_first(page, context):
    page.set_content("<h1>First page</h1>")

    second_page = context.new_page()
    second_page.set_content("<input placeholder='Search'>")

    # Deliberately broken, on the SECOND page specifically — an ACTION (fill), not an assertion,
    # since expect(...) is never healed (see test_02/POM tests elsewhere in this repo) and would
    # just fail here instead of proving anything about page-2 healing.
    search_box = second_page.get_by_placeholder("SearchWrong").describe("Search Box")
    search_box.fill("self-healing")

    expect(second_page.get_by_placeholder("Search")).to_have_value("self-healing")

    report = get_healing_reports()[-1]
    assert report.healed is True
    assert report.description == "Search Box"

    second_page.close()


def test_a_confirm_dialog_is_handled_and_recorded(page):
    page.set_content("<button id='delete-btn' onclick=\"window.__result = confirm('Delete this item?')\">Delete</button>")

    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("#delete-btn").click()

    # The dialog's own return value (window.confirm() resolves to True once accepted) is the real
    # proof the handler actually ran, not just that the click didn't hang waiting for it.
    result = page.evaluate("window.__result")
    assert result is True
