import uuid
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from src.dashboard_page import DashboardPage


@pytest.fixture(scope="session")
def browser() -> Browser:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def pump_id() -> str:
    return f"pump-{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="function")
def dashboard_page(page: Page) -> DashboardPage:
    dashboard = DashboardPage(page)
    dashboard.open()
    return dashboard