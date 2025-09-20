import re
from datetime import datetime

from playwright.sync_api import expect
import time


def test_demo_qa_selectors(page):
    page.goto('https://demoqa.com/webtables')

    page.locator('button:has-text("Add")').click()

    #page.locator('.modal-content').is_visible()
    page.locator('.modal-content .modal-header .modal-title:has-text("Registration Form")').is_visible()
    page.fill('input[placeholder="First Name"]', 'Roman')
    page.get_by_placeholder('Last Name').fill('Bychkov')
    page.get_by_placeholder('name@example.com').fill('mail@ex.com')
    page.get_by_placeholder('Age').fill('26')
    page.get_by_placeholder('Salary').fill('165')
    page.get_by_placeholder('Department').fill('QA')

    time.sleep(2)

    page.get_by_role('button', name='Submit').click()

    time.sleep(2)

def test_demo_qa_actions(page, get_data_for_student_registration_form):
    data_for_student_registration_form = get_data_for_student_registration_form
    today_date = datetime.today()
    today_date_formatted = today_date.strftime('%d %b %Y')

    page.goto('https://demoqa.com/automation-practice-form', wait_until='domcontentloaded')

    expect(page.locator('#userForm')).to_be_visible()
    #assert page.locator('#userForm').is_visible() == True

    page.fill('#firstName', data_for_student_registration_form.firstName)
    page.fill('#lastName', data_for_student_registration_form.lastName)
    page.type('#userEmail', data_for_student_registration_form.email)
    #page.get_by_label('Female').check()
    #page.check(page.get_by_label('Female'))
    page.check(f'label:has-text("{data_for_student_registration_form.gender}")')
    page.fill('#userNumber', data_for_student_registration_form.phoneNumber)

    expect(page.locator('#dateOfBirthInput')).to_have_value(today_date_formatted)
    #expect(page.locator('#dateOfBirthInput')).to_have_attribute('value', today_date_formatted)
    page.click('#dateOfBirthInput')
    page.get_by_role("option", name="Choose Wednesday, September 24th,").click()

    page.type('#subjectsInput', 'c')
    for subject in data_for_student_registration_form.subjects:
        page.get_by_text(subject).click()

    for hobbie in data_for_student_registration_form.hobbies:
        page.check(f'label:has-text("{hobbie}")')

    page.locator('#uploadPicture').set_input_files(f'C:/Users/RBychkov/PycharmProjects/CinescopeOld/files/playwright_trace/{data_for_student_registration_form.pictureFileName}')
    page.type('#currentAddress', data_for_student_registration_form.currentAddress)
    page.click('#state')
    page.get_by_text(data_for_student_registration_form.state).click()
    page.click('#city')
    page.get_by_text(data_for_student_registration_form.city).click()

    page.click('#submit')

    expect(page.get_by_text('© 2013-2020 TOOLSQA.COM | ALL')).to_have_text('© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED.')

    time.sleep(5)


def test_demo_qa_check_enabled_status(page):
    page.goto('https://demoqa.com/radio-button', wait_until='domcontentloaded')
    #page.pause()
    #expect(page.locator('#yesRadio')).to_be_enabled()
    #expect(page.locator('#impressiveRadio')).to_be_enabled()
    #expect(page.locator('#noRadio')).to_be_disabled()

    expect(page.get_by_role("radio", name="Yes")).to_be_enabled()
    expect(page.get_by_role("radio", name="Impressive")).to_be_enabled()
    expect(page.get_by_role("radio", name="No")).to_be_disabled()


def test_demo_qa_check_visibility(page):
    page.goto('https://demoqa.com/checkbox', wait_until='domcontentloaded')

    expect(page.get_by_text('Home')).to_be_visible()
    expect(page.get_by_text('Desktop')).to_be_hidden()

    page.get_by_role("button", name="Toggle").click()

    expect(page.get_by_text('Desktop')).to_be_visible()

    page.get_by_role("listitem").filter(has_text=re.compile(r"^Documents$")).get_by_label("Toggle").click()

def test_demo_qa_check_visibility_2(page):
    page.goto('https://demoqa.com/dynamic-properties', wait_until='domcontentloaded')

    expect(page.get_by_role('button', name='Visible After 5 Seconds')).to_be_hidden()

    #page.wait_for_selector('button:has-text("Visible After 5 Seconds")', state='visible', timeout=6000)
    expect(page.get_by_text('Visible After 5 Seconds')).to_be_visible()





















'''
def test_text_box(page):
    user_data_for_registration = UserData.get_user_data_for_registration()

    page.goto('https://dev-cinescope.coconutqa.ru/register')

    #page.pause()

    page.fill('[placeholder="Имя Фамилия Отчество"]', user_data_for_registration['fullName'])
    page.fill('[placeholder="Email"]', user_data_for_registration['email'])
    page.fill('[placeholder="Пароль"]', user_data_for_registration['password'])
    page.fill('[placeholder="Повторите пароль"]', user_data_for_registration['passwordRepeat'])

    # page.locator(text='Зарегистрироваться').click()
    page.get_by_role('button', name='Зарегистрироваться').click()

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)

    time.sleep(2)
'''




