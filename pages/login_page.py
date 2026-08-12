from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Intentionally broken placeholder ("Username1") to demonstrate self-healing recovery.
        self.txt_username = page.get_by_placeholder("Username1").describe("Username Textbox")
        self.txt_password = page.get_by_placeholder("Password").describe("Password Textbox")
        self.btn_login = page.get_by_role("button", name="Login").describe("Login Button")

    def enter_username(self, username: str) -> None:
        self.txt_username.fill(username)
        print(f"Entered username {username}")

    def enter_password(self, password: str) -> None:
        self.txt_password.fill(password)
        print(f"Entered password {password}")

    def click_login(self) -> None:
        self.btn_login.click()
        print("Clicked on Login Button")
