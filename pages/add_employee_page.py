from .base_page import BasePage


class AddEmployeePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.txt_first_name = page.get_by_placeholder("First Name").describe("First Name Textbox")
        # Intentionally broken placeholder ("Last Name1") to demonstrate self-healing recovery.
        self.txt_last_name = page.get_by_placeholder("Last Name1").describe("Last Name Textbox")
        self.btn_save = page.get_by_role("button", name="Save").describe("Save Button")

    def enter_first_name(self, first_name: str) -> None:
        self.txt_first_name.fill(first_name)
        print(f"Entered First Name {first_name}")

    def enter_last_name(self, last_name: str) -> None:
        self.txt_last_name.fill(last_name)
        print(f"Entered Last Name {last_name}")

    def click_save(self) -> None:
        self.btn_save.click()
        print("Clicked on Save Button")
