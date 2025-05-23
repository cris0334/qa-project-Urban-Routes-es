from helpers import Helpers
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    selected_rate = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-title"]')

    phone_number_field = (By.ID, 'phone')
    add_payment_button = (By.CSS_SELECTOR, "div.pp-button.filled")  # Edit1: Se cambió por CSS_Selector
    card_form_open_button = (By.CLASS_NAME, "pp-plus-container")
    card_form_close_button = (By.XPATH,
                              '//div[@class="payment-picker open"]//div[@class="section active"]//button[@class="close-button section-close"]')
    card_number = (By.ID, 'number')
    card_code = (By.XPATH, "//input[@id='code'][@class='card-input']")
    phone_code_field = (By.XPATH, '//div[@class="input-container"]//input[@id="code"]')
    comment_for_driver_field = (By.ID, 'comment')

    extras_sliders = (By.XPATH, "//span[@class='slider round']")
    extras_values = (By.XPATH, '//input[@class="switch-input"]')

    card_add_button = (By.XPATH, '//div[@class="pp-buttons"]//button[@type="submit"]')
    icecream_plus_buttons = (By.XPATH, '//div[@class="counter-plus"]')
    icecream_values = (By.XPATH, '//div[@class="counter-value"]')
    catch_a_ride_button = (By.XPATH, '//div[@class="results-container"]//button')
    comfort_button = (By.XPATH, '//div[@class="tcard-icon"]//img[@alt="Comfort"]')
    add_phone_button = (By.CSS_SELECTOR, 'div.np-button')  # Edit1: Se cambió por CSS_Selector
    add_phone_confirm_button = (By.XPATH, '//button[text()="Confirmar"]')
    add_phone_send_button = (By.XPATH, '//button[text()="Siguiente"]')
    order_a_taxi_button = (By.CSS_SELECTOR, "button.smart-button")  # Edit1: Se cambió por CSS_Selector

    modal_title = (By.XPATH, '//div[@class="order-header-title"]')
    modal_time_to_assign = (By.XPATH, '//div[@class="order-header-time"]')
    modal_driver_detail_shown = (By.XPATH, '//div[@class="order-details shown"]')
    display_taxi_info_button = (By.XPATH, '//button[@class="order-button"]//img[@alt="burger"]')
    modal_driver_order_button = (By.XPATH, "//div[@class='order-button']")

    def __init__(self, driver):
        self.driver = driver

    def wait_for_page_load(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.from_field))

    def wait_for_payment_page_load(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.card_form_open_button))

    def wait_for_modal_time(self):
        WebDriverWait(self.driver, 60).until(expected_conditions.text_to_be_present_in_element(self.modal_time_to_assign, "01"))
        time_to_assign = self.get_modal_time_to_assign()
        minutes_str, seconds_str = time_to_assign.split(":")

        seconds = int(minutes_str) * 60 + int(seconds_str) + 1

        WebDriverWait(self.driver, seconds).until(expected_conditions.visibility_of_element_located(self.modal_driver_order_button))

    def wait_form_card_page_load(self):  # Edit 1: corrección de nombre
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.card_number))

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)
        assert self.get_from() == from_address  # Edit 1: assert

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)
        assert self.get_to() == to_address  # Edit 1: assert

    def set_phone_number(self, phone_number):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.phone_number_field))
        self.driver.find_element(*self.phone_number_field).send_keys(phone_number)
        assert self.get_phone_number() == phone_number  # Edit 1: assert

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_selected_rate(self):
        return self.driver.find_element(*self.selected_rate).get_property('outerText')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_field).get_property('value')

    def get_card_number(self):  # Edit 1: agregar métodos
        return self.driver.find_element(*self.card_number).get_property('value')

    def get_card_code(self):  # Edit 1: agregar métodos
        return self.driver.find_element(*self.card_code).get_property('value')

    def get_phone_code(self):  # Edit 1: agregar métodos
        return self.driver.find_element(*self.phone_code_field).get_property('value')

    def get_comment_for_driver(self):  # Edit 1: agregar métodos
        return self.driver.find_element(*self.comment_for_driver_field).get_property('value')

    def get_icecream_by_flavor(self, flavor):
        icecream_values = self.driver.find_elements(*self.icecream_values)

        return_value = 0

        if flavor == "chocolate":
            return_value = icecream_values[1].text
        elif flavor == "strawberry":
            return_value = icecream_values[2].text
        else:
            return_value = icecream_values[0].text

        return int(return_value)

    def get_extras(self):
        blanket_napkins_and_acoustic_curtain  = self.driver.find_elements(*self.extras_values)
        blanket_napkins = blanket_napkins_and_acoustic_curtain[0].get_property('checked')
        acoustic_curtain = blanket_napkins_and_acoustic_curtain[1].get_property('checked')

        return blanket_napkins, acoustic_curtain

    def get_modal_title(self):
        modal_title_element = self.driver.find_element(*self.modal_title)

        return modal_title_element.text

    def get_modal_time_to_assign(self):
        modal_time_element = self.driver.find_element(*self.modal_time_to_assign)

        return modal_time_element.text

    def get_modal_driver_detail(self):
        modal_driver_detail = self.driver.find_element(*self.modal_driver_detail_shown)

        return modal_driver_detail.get_property('innerText')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def set_phone(self, phone_number):  # Edit 1: agregar métodos para simplificar pasos
        self.add_phone_click()
        self.set_phone_number(phone_number)  # assign the phone number
        self.send_phone_click()
        phone_code = Helpers.retrieve_phone_code(self.driver)
        self.set_phone_code(phone_code)
        self.confirm_phone_click()

    def select_rate(self, rate):
        if rate == "comfort":
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.comfort_button))
            self.driver.find_element(*self.comfort_button).click()

    def set_card_number(self, card_number):  # Edit 1: agregar métodos, simplifición y assert
        self.driver.find_element(*self.card_number).send_keys(card_number)

    def set_card_code(self, card_code):  # Edit 1: agregar métodos, simplifición y assert
        self.driver.find_element(*self.card_code).send_keys(card_code + Keys.TAB)

    def set_phone_code(self, phone_code):  # Edit 1: assert
        self.driver.find_element(*self.phone_code_field).send_keys(phone_code)

        assert self.get_phone_code() == phone_code

    def set_comment_for_driver(self, comment):
        self.driver.find_element(*self.comment_for_driver_field).send_keys(comment)

    def set_card(self, card_number, card_code):
        self.add_payment_button_click()  # Edit 1: cambio por métodos
        self.wait_for_payment_page_load()
        self.card_form_open_button_click()  # Edit 1: cambio por métodos
        self.wait_form_card_page_load()  # Edit 1: cambio por métodos
        self.set_card_number(card_number)
        self.set_card_code(card_code)

    def icecream_plus(self, flavor):
        buttons = self.driver.find_elements(*self.icecream_plus_buttons)

        if flavor == "chocolate":
            buttons[1].click()
        elif flavor == "strawberry":
            buttons[2].click()
        else:
            buttons[0].click()

    def set_extras(self, blanket_napkins, acoustic_curtain):
        extras_sliders = self.driver.find_elements(*self.extras_sliders)
        if blanket_napkins:
            extras_sliders[0].click()  # corrección de valor

        if acoustic_curtain:
            extras_sliders[1].click()  # corrección de valor

    def add_payment_button_click(self):  # Edit 1: agregar métodos para simplificar pasos
        self.driver.find_element(*self.add_payment_button).click()

    def card_form_open_button_click(self):  # Edit 1: agregar métodos para simplificar pasos
        self.driver.find_element(*self.card_form_open_button).click()

    def card_add_button_click(self):  # Edit 1: agregar métodos para simplificar pasos
        self.driver.find_element(*self.card_add_button).click()

    def card_form_close_button_click(self):  # Edit 1: agregar métodos para simplificar pasos
        self.driver.find_element(*self.card_form_close_button).click()

    def catch_a_ride_click(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.catch_a_ride_button))
        self.driver.find_element(*self.catch_a_ride_button).click()

    def add_phone_click(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.add_phone_button))
        self.driver.find_element(*self.add_phone_button).click()

    def send_phone_click(self):
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.add_phone_send_button))
        self.driver.find_element(*self.add_phone_send_button).click()

    def confirm_phone_click(self):
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.add_phone_confirm_button))
        self.driver.find_element(*self.add_phone_confirm_button).click()

    def order_a_taxi_button_click(self):
        self.driver.find_element(*self.order_a_taxi_button).click()

    def display_driver_info_click(self):
        self.driver.find_element(*self.display_taxi_info_button).click()