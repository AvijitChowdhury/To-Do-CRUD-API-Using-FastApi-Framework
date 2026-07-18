from pathlib import Path
import sys

from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pages.task_api_page import TaskApiPage

BASE_URL = "http://127.0.0.1:8001"


def test_api_end_to_end_flow_with_pom():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        task_page = TaskApiPage(page, base_url=BASE_URL)
        task_page.capture_docs_screenshot("swagger_ui_python.png")
        task_page.capture_root_screenshot("landing_page_python.png")

        request_context = playwright.request.new_context(base_url=BASE_URL)
        try:
            health_response = request_context.get("/health")
            assert health_response.ok
            assert health_response.json()["status"] == "ok"

            create_response = request_context.post(
                "/tasks",
                data={"title": "Playwright Python task"},
            )
            assert create_response.status == 201
            created_task = create_response.json()
            assert created_task["title"] == "Playwright Python task"
            assert created_task["done"] is False

            get_response = request_context.get(f"/tasks/{created_task['id']}")
            assert get_response.status == 200
            fetched_task = get_response.json()
            assert fetched_task["id"] == created_task["id"]

            update_response = request_context.put(
                f"/tasks/{created_task['id']}",
                data={"done": True},
            )
            assert update_response.status == 200
            updated_task = update_response.json()
            assert updated_task["done"] is True

            stats_response = request_context.get("/stats")
            assert stats_response.status == 200
            stats_data = stats_response.json()
            assert stats_data["total"] >= 1

            delete_response = request_context.delete(f"/tasks/{created_task['id']}")
            assert delete_response.status == 204

            missing_response = request_context.get(f"/tasks/{created_task['id']}")
            assert missing_response.status == 404
        finally:
            request_context.dispose()
            context.close()
            browser.close()
