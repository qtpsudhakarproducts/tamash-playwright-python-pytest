from pages.add_employee_page import AddEmployeePage
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.personal_details_page import PersonalDetailsPage
from pages.pim_page import PIMPage

# Page Object Model example: page objects wrap the self-healing `page` fixture.


def test_create_employee_using_page_object_model(page):
    base_page = BasePage(page)
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    pim_page = PIMPage(page)
    add_emp_page = AddEmployeePage(page)
    personal_details_page = PersonalDetailsPage(page)

    base_page.navigate_to_url("/")
    login_page.enter_username("testadmin")
    login_page.enter_password("Vibetestq@123#")
    login_page.click_login()

    dashboard_page.verify_dashboard_page()
    dashboard_page.click_pim()

    pim_page.verify_pim_page()
    pim_page.click_add()

    add_emp_page.enter_first_name("John")
    add_emp_page.enter_last_name("Smith")
    add_emp_page.click_save()

    personal_details_page.verify_personal_details_page()
