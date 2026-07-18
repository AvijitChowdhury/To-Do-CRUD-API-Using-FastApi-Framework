from pages.base_page import BasePage


class TaskApiPage(BasePage):
    def open_docs(self) -> None:
        self.goto("/docs")

    def open_root(self) -> None:
        self.goto("/")

    def capture_docs_screenshot(self, file_name: str = "swagger_ui_python.png") -> str:
        self.open_docs()
        return self.capture_screenshot(file_name)

    def capture_root_screenshot(self, file_name: str = "landing_page_python.png") -> str:
        self.open_root()
        return self.capture_screenshot(file_name)
