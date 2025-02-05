import data
from UrbanRoutesPage import UrbanRoutesPage
from selenium import webdriver

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
        self.driver.get(data.urban_routes_url) # new chrome session
        routes_page = UrbanRoutesPage(self.driver) # open page

        # variable assignation
        address_from = data.address_from
        address_to = data.address_to
        rate = data.rate # comfort rate
        phone_number = data.phone_number
        card_number = data.card_number
        card_code = data.card_code
        ice_creams = data.ice_creams # Edit 1: ´cambio de nombres de variables
        blanket_napkins = data.blanket_napkins
        acoustic_curtain = data.acoustic_curtain
        # end of variable assignation

        routes_page.wait_for_page_load()    # wait for page to open

        routes_page.set_route(address_from, address_to) # create the route
        routes_page.catch_a_ride_click() # click the button to open travel configuration
        routes_page.select_rate(rate) # assign the trip's rate
        routes_page.set_phone(phone_number) # assign phone number, get code and use it

        routes_page.set_card(card_number, card_code) # assign both card number and card code

        routes_page.set_extras(blanket_napkins, acoustic_curtain) # add blanket/napkins

        for flavor in ice_creams: # adding icecream buckets
            for i in range(ice_creams[flavor]):
                routes_page.icecream_plus(flavor)

        routes_page.order_a_taxi_button_click() # ordering the taxi (duda: no se ve el diálogo de espera, ¿cambio algo?)

        # Edit 1: asserts fueron movidos a sus métodos 
        #assert routes_page.get_from() == address_from
        #assert routes_page.get_to() == address_to
        #assert routes_page.get_phone_number() == phone_number

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
