from playwright.sync_api import expect

from .base_page import BasePage


class PersonalDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.personal_details_header = page.locator("//h6[text()='Personal Details']").describe("Personal Details Header")

    def verify_personal_details_page(self) -> None:
        expect(self.personal_details_header).to_be_visible(timeout=10000)
        print("Personal Details Page is displayed")
