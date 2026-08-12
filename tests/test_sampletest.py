from playwright.sync_api import expect

# Non-POM example: locators are declared directly inside the test body.


def test_login_using_css_selectors(page):
    page.goto("/")

    # Intentionally broken selector ("username1") to demonstrate self-healing recovery.
    txt_username = page.locator('input[name="username1"]').describe("User Name Textbox")
    txt_username.fill("testadmin")

    txt_password = page.locator("input[placeholder='Password']").describe("Password Textbox")
    txt_password.fill("Vibetestq@123#")

    btn_login = page.locator("button[type='submit']").describe("Login Button")
    btn_login.click()

    expect(page.locator("h6")).to_have_text("Dashboard")
