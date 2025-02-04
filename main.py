import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    phone_number_field = (By.ID, 'phone')
    add_payment_button = (By.XPATH, "//div[@class='pp-button filled']")
    card_form_open_button = (By.CLASS_NAME, "pp-plus-container")
    card_form_close_button = (By.XPATH, '//div[@class="payment-picker open"]//div[@class="section active"]//button[@class="close-button section-close"]')
    card_number = (By.ID, 'number')
    card_code = (By.XPATH, "//input[@id='code'][@class='card-input']")
    phone_code_field = (By.XPATH, '//div[@class="input-container"]//input[@id="code"]')

    # extras_sliders = (By.XPATH, '//input[@class="switch-input"]')
    extras_sliders = (By.XPATH, "//span[@class='slider round']")

    card_add_button = (By.XPATH, '//div[@class="pp-buttons"]//button[@type="submit"]')
    icecream_plus_buttons = (By.XPATH, '//div[@class="counter-plus"]')
    catch_a_ride_button = (By.XPATH, '//div[@class="results-container"]//button')
    comfort_button = (By.XPATH, '//div[@class="tcard-icon"]//img[@alt="Comfort"]')
    add_phone_button = (By.CLASS_NAME, 'np-button')
    add_phone_confirm_button = (By.XPATH, '//button[text()="Confirmar"]')
    add_phone_send_button = (By.XPATH, '//button[text()="Siguiente"]')
    order_a_taxi_button = (By.CLASS_NAME, "smart-button")

    def __init__(self, driver):
        self.driver = driver

    def wait_for_page_load(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.from_field))

    def wait_for_payment_page_load(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.card_form_open_button))

    def wait_for_card_page_load(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.card_number))

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_phone_number(self, phone_number):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.phone_number_field))
        self.driver.find_element(*self.phone_number_field).send_keys(phone_number)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def select_rate(self, rate):
        #selected_button = None

        if rate == "comfort":
            WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.comfort_button))
            self.driver.find_element(*self.comfort_button).click()
            #selected_button = self.driver.find_element(*self.comfort_button)

        #if ~(selected_button is None):
        #    selected_button.click()

    def set_card_number(self, number):
        card_number = self.driver.find_element(*self.card_number)
        card_number.send_keys(number)

    def set_card_code(self, code):
        card_code = self.driver.find_element(*self.card_code)
        card_code.send_keys(code + Keys.TAB)

    def set_phone_code(self, phone_code):
        self.driver.find_element(*self.phone_code_field).send_keys(phone_code)

    def set_card(self, card_number, card_code):
        self.driver.find_element(*self.add_payment_button).click()
        self.wait_for_payment_page_load()
        self.driver.find_element(*self.card_form_open_button).click()
        self.wait_for_card_page_load()
        self.set_card_number(card_number)
        self.set_card_code(card_code)
        self.driver.find_element(*self.card_add_button).click()
        self.driver.find_element(*self.card_form_close_button).click()

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
            extras_sliders[1].click()

        if acoustic_curtain:
            extras_sliders[2].click()

    def catch_a_ride_click(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.catch_a_ride_button))
        self.driver.find_element(*self.catch_a_ride_button).click()

    def add_phone_click(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.add_phone_button))
        self.driver.find_element(*self.add_phone_button).click()

    def send_phone_click(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.add_phone_send_button))
        self.driver.find_element(*self.add_phone_send_button).click()

    def confirm_phone_click(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.add_phone_confirm_button))
        self.driver.find_element(*self.add_phone_confirm_button).click()

    def order_a_taxi_button_click(self):
        self.driver.find_element(*self.order_a_taxi_button).click()

    def retrieve_phone_code(self):
        return retrieve_phone_code(self.driver)


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        #cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        temp_driver = webdriver.Chrome()
        temp_driver.start_session(capabilities)
        cls.driver = temp_driver

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        rate = data.rate
        phone_number = data.phone_number
        card_number = data.card_number
        card_code = data.card_code
        icecreams = data.icecreams
        blanket_napkins = data.blanket_napkins
        acoustic_curtain = data.acoustic_curtain

        routes_page.wait_for_page_load()

        routes_page.set_route(address_from, address_to) # create the route
        routes_page.catch_a_ride_click() # click the button to call a taxi
        routes_page.select_rate(rate) # assign the trip's rate

        routes_page.add_phone_click()
        routes_page.set_phone_number(phone_number) # assign the phone number
        routes_page.send_phone_click()
        phone_code = routes_page.retrieve_phone_code()
        routes_page.set_phone_code(phone_code)
        routes_page.confirm_phone_click()

        routes_page.set_card(card_number, card_code) # assign both card number and card code

        routes_page.set_extras(blanket_napkins, acoustic_curtain) # add blanket/napkins

        for flavor in icecreams:
            for i in range(icecreams[flavor]): # adding icecream buckets
                routes_page.icecream_plus(flavor)

        routes_page.order_a_taxi_button_click() # ordering the taxi (duda: no se ve el diálogo de espera, ¿cambio algo?)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        assert routes_page.get_phone_number() == phone_number

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
