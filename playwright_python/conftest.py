from pathlib import Path
import os
from playwright.sync_api import sync_playwright
import pytest


@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def api_client():
    from requests import Session

    session = Session()
    yield session
    session.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        screenshot_dir = Path(__file__).resolve().parents[1] / "assests" / "playwright_python"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / f"failure_{item.name}.png"
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
