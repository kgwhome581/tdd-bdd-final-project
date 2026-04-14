from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Переход на страницу
@when('I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)

# Проверка заголовка
@then('I should see "{text}" in the title')
def step_impl(context, text):
    assert text in context.driver.title

@then('I should not see "{text}"')
def step_impl(context, text):
    assert text not in context.driver.page_source

# Ввод текста в поля (с учетом префикса 'product_')
@when('I set the "{field}" to "{value}"')
def step_impl(context, field, value):
    element_id = 'product_' + field.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(value)

# Работа с выпадающими списками
@when('I select "{value}" in the "{field}" dropdown')
@then('I should see "{value}" in the "{field}" dropdown')
def step_impl(context, value, field):
    element_id = 'product_' + field.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    for option in element.find_elements(By.TAG_NAME, 'option'):
        if option.text == value:
            option.click()
            assert option.is_selected()
            break

# Нажатие на кнопки
@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element(By.ID, button_id).click()

# Проверка сообщений (Flash messages)
@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, 'flash_message'), message)
    )
    assert found

# Проверка значений в полях
@then('I should see "{value}" in the "{field}" field')
def step_impl(context, value, field):
    element_id = 'product_' + field.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute('value') == value

@then('the "{field}" field should be empty')
def step_impl(context, field):
    element_id = 'product_' + field.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute('value') == ""

# Копирование и вставка ID (для Retrieve)
@when('I copy the "{field}" field')
def step_impl(context, field):
    element_id = 'product_' + field.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    context.clipboard = element.get_attribute('value')

@when('I paste the "{field}" field')
def step_impl(context, field):
    element_id = 'product_' + field.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(context.clipboard)
