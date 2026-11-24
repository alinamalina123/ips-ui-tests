import allure
import pytest
from src.dashboard_page import DashboardPage


@allure.feature("Панель управления (Dashboard)")
@allure.story("Отображение текущей глюкозы и статуса")
@pytest.mark.parametrize(
    "glucose_value, expected_display, expected_status",
    [
        ("2.0", "2.0", "Низкий"),
        ("4.5", "4.5", "Низкий"),
        ("4.6", "4.6", "Норма"),
        ("5.5", "5.5", "Норма"),
        ("9.9", "9.9", "Норма"),
        ("10.0", "10.0", "Высокий"),
        ("15.0", "15.0", "Высокий"),
    ],
    ids=[
        "low_2.0",
        "low_upper_boundary_4.5",
        "normal_lower_boundary_4.6",
        "normal_5.5",
        "normal_upper_boundary_9.9",
        "high_lower_boundary_10.0",
        "high_15.0",
    ],
)
def test_glucose_value_and_status(
    dashboard_page: DashboardPage,
    pump_id: str,
    glucose_value: str,
    expected_display: str,
    expected_status: str,
):
    allure.dynamic.title(f"Глюкоза {glucose_value} -> статус '{expected_status}'")

    dashboard_page.set_pump_id(pump_id)
    dashboard_page.send_glucose(glucose_value)

    dashboard_page.should_have_glucose_value(expected_display)
    dashboard_page.should_have_glucose_status(expected_status)


@allure.feature("Панель управления (Dashboard)")
@allure.story("Негативные сценарии ввода глюкозы")
@pytest.mark.parametrize(
    "invalid_value",
    ["-1", "abc", ""],
    ids=["negative_value", "non_numeric_string", "empty_string"],
)
def test_invalid_glucose_value_not_applied(
    dashboard_page: DashboardPage,
    pump_id: str,
    invalid_value: str,
):
    allure.dynamic.title(f"Невалидное значение глюкозы: '{invalid_value}'")

    dashboard_page.set_pump_id(pump_id)
    dashboard_page.send_glucose("5.5")
    dashboard_page.should_have_glucose_value("5.5")

    dashboard_page.send_glucose(invalid_value)

    dashboard_page.should_have_glucose_value("5.5")