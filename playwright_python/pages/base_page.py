from pathlib import Path
from typing import Optional
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page, base_url: str = "http://127.0.0.1:8001"):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def goto(self, path: str = "/") -> None:
        self.page.goto(f"{self.base_url}{path}")
        self.page.wait_for_load_state("networkidle")

    def capture_screenshot(self, file_name: str, full_page: bool = True) -> str:
        screenshot_dir = Path(__file__).resolve().parents[1].parent / "assests" / "playwright_python"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / file_name
        self.page.screenshot(path=str(screenshot_path), full_page=full_page)
        return str(screenshot_path)
