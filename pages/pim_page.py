from playwright.sync_api import expect

from .base_page import BasePage


class PIMPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.pim_header = page.locator("//h6[text()='PIM']").describe("PIM Header")
        self.btn_add = page.locator("//button[normalize-space()='Add']").describe("Add Button")

    def verify_pim_page(self) -> None:
        expect(self.pim_header).to_be_visible(timeout=10000)
        print("PIM Page is displayed")

    def click_add(self) -> None:
        self.btn_add.click()
        print("Clicked on Add Button")
