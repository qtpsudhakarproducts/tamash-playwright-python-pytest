class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate_to_url(self, url: str) -> None:
        self.page.goto(url)
        print(f"Navigated to URL {url}")
