import re
import allure
from playwright.sync_api import Page, expect


class DashboardPage:
    URL = "https://ips.alexgallax-edu.ru/dashboard"

    def __init__(self, page: Page):
        self.page = page
        self.pump_name_input = page.get_by_role("textbox", name="например, student_ivanov")
        self.apply_button = page.get_by_role("button", name="Применить")
        self.glucose_input = page.get_by_role("textbox", name="Значение глюкозы")
        self.send_button = page.get_by_role("button", name="Отправить")
        self.alarms_link = page.get_by_role("link", name=re.compile("Тревоги"))

    @allure.step("Открыть страницу Dashboard")
    def open(self) -> None:
        self.page.goto(self.URL)

    @allure.step("Выбрать помпу с id '{pump_id}'")
    def set_pump_id(self, pump_id: str) -> None:
        self.pump_name_input.fill(pump_id)
        self.apply_button.click()

    @allure.step("Отправить значение глюкозы '{value}' через Devpanel")
    def send_glucose(self, value: str) -> None:
        self.glucose_input.fill(str(value))
        self.send_button.click()

    @allure.step("Проверить, что текущая глюкоза равна '{expected_value}'")
    def should_have_glucose_value(self, expected_value: str) -> None:
        locator = self.page.get_by_text(expected_value, exact=True)
        expect(locator).to_be_visible(timeout=5000)

    @allure.step("Проверить, что статус глюкозы равен '{expected_status}'")
    def should_have_glucose_status(self, expected_status: str) -> None:
        locator = self.page.get_by_text(expected_status, exact=True)
        expect(locator).to_be_visible(timeout=5000)

    @allure.step("Получить текущее значение счётчика тревог")
    def get_alarms_count(self) -> int:
        text = self.alarms_link.inner_text()
        match = re.search(r"\d+", text)
        return int(match.group()) if match else 0

    @allure.step("Проверить, что счётчик тревог стал равен {expected_count}")
    def should_have_alarms_count(self, expected_count: int) -> None:
        expect(self.alarms_link).to_contain_text(str(expected_count), timeout=5000)