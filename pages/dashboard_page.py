from playwright.sync_api import expect

from .base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.dashboard_header = page.get_by_role("heading", name="Dashboard").describe("Dashboard Header")
        self.lnk_pim = page.get_by_role("link", name="PIM").describe("PIM Link")

    def click_pim(self) -> None:
        self.lnk_pim.click()
        print("Clicked on PIM Link")

    def verify_dashboard_page(self) -> None:
        expect(self.dashboard_header).to_be_visible()
        print("Dashboard Page is displayed")
