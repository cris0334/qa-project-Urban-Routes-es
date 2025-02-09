import data
from UrbanRoutesPage import UrbanRoutesPage
from selenium import webdriver

class TestUrbanRoutes:

    driver = None
    routes_page = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        temp_driver = webdriver.Chrome()
        temp_driver.start_session(capabilities)
        cls.driver = temp_driver
        cls.driver.get(data.urban_routes_url)  # new chrome session
        cls.routes_page = UrbanRoutesPage(cls.driver)  # open page

    def test_set_route(self):
        # variable assignation
        address_from = data.address_from
        address_to = data.address_to
        # end of variable assignation

        self.routes_page.wait_for_page_load()    # wait for page to open
        self.routes_page.set_route(address_from, address_to) # create the route

        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    def test_select_plan(self):
        # variable assignation
        rate = data.rate  # comfort rate
        # end of variable assignation

        self.routes_page.catch_a_ride_click() # click the button to open travel configuration
        self.routes_page.select_rate(rate) # assign the trip's rate

        assert self.routes_page.get_selected_rate().lower() == rate

    def test_fill_phone_number(self):
        # variable assignation
        phone_number = data.phone_number
        # end of variable assignation

        self.routes_page.set_phone(phone_number) # assign phone number, get code and use it

        assert self.routes_page.get_phone_number() == phone_number

    def test_fill_card(self):
        # variable assignation
        card_number = data.card_number
        card_code = data.card_code
        # end of variable assignation

        self.routes_page.set_card(card_number, card_code) # assign both card number and card code

        assert self.routes_page.get_card_code() == card_code
        assert self.routes_page.get_card_number() == card_number

        self.routes_page.card_add_button_click()  # Edit 1: cambio por métodos
        self.routes_page.card_form_close_button_click()  # Edit 1: cambio por métodos

    def test_comment_for_driver(self):
        # variable assignation
        message_for_driver = data.message_for_driver
        # end of variable assignation

        self.routes_page.set_comment_for_driver(message_for_driver)

        assert self.routes_page.get_comment_for_driver() == message_for_driver

    def test_order_extras(self):
        blanket_napkins = data.blanket_napkins
        acoustic_curtain = data.acoustic_curtain

        self.routes_page.set_extras(blanket_napkins, acoustic_curtain)  # add blanket/napkins

        assert self.routes_page.get_extras() == (blanket_napkins, acoustic_curtain)

    def test_order_ice_creams(self):
        ice_creams = data.ice_creams  # Edit 1: cambio de nombres de variables

        for flavor in ice_creams: # adding icecream buckets
            for i in range(ice_creams[flavor]):
                self.routes_page.icecream_plus(flavor)

            assert self.routes_page.get_icecream_by_flavor(flavor) == ice_creams[flavor]

    def test_car_search_model_appears(self):
        self.routes_page.order_a_taxi_button_click() # ordering the taxi

        # No puedo hacer el assert porque no se mantiene el

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
