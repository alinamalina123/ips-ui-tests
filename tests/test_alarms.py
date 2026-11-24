import allure
import pytest
from src.dashboard_page import DashboardPage


@allure.feature("Панель управления (Dashboard)")
@allure.story("Счётчик тревог при отклонении глюкозы")
@pytest.mark.parametrize(
    "glucose_value",
    ["2.0", "4.5", "10.0", "15.0"],
    ids=[
        "low_2.0",
        "low_upper_boundary_4.5",
        "high_lower_boundary_10.0",
        "high_15.0",
    ],
)
def test_alarm_counter_increases_on_abnormal_glucose(
    dashboard_page: DashboardPage,
    pump_id: str,
    glucose_value: str,
):
    allure.dynamic.title(f"Счётчик тревог +1 при глюкозе {glucose_value}")

    dashboard_page.set_pump_id(pump_id)
    initial_alarms = dashboard_page.get_alarms_count()

    dashboard_page.send_glucose(glucose_value)

    expected_alarms = initial_alarms + 1
    dashboard_page.should_have_alarms_count(expected_alarms)


@allure.feature("Панель управления (Dashboard)")
@allure.story("Счётчик тревог при нормальной глюкозе")
@pytest.mark.parametrize(
    "normal_value",
    ["4.6", "5.5", "9.9"],
    ids=["normal_lower_boundary_4.6", "normal_5.5", "normal_upper_boundary_9.9"],
)
def test_alarm_counter_does_not_increase_on_normal_glucose(
    dashboard_page: DashboardPage,
    pump_id: str,
    normal_value: str,
):
    allure.dynamic.title(f"Счётчик тревог не растёт при норме ({normal_value})")

    dashboard_page.set_pump_id(pump_id)
    initial_alarms = dashboard_page.get_alarms_count()

    dashboard_page.send_glucose(normal_value)
    dashboard_page.should_have_glucose_value(normal_value)

    actual_alarms = dashboard_page.get_alarms_count()
    assert actual_alarms == initial_alarms, (
        f"Ожидалось, что счётчик тревог останется {initial_alarms}, "
        f"но получено {actual_alarms} при нормальной глюкозе {normal_value}"
    )