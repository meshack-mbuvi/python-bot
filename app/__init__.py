from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
from selenium.webdriver import ActionChains

from selenium.webdriver.common.by import By
from exceptions import Exception


def log_info(message):
    print "[", datetime.datetime.now().strftime(
        "%Y-%b-%d %H:%M:%S"), "]", message


class Bot(object):
    def __init__(self, chrome_driver):
        super(Bot, self).__init__()
        self.password = "password here"
        self.email = "email here"
        extension = './extension_0_6_0_0.crx'

        chrome_options = Options()

        chrome_options.add_argument("--headless")
        chrome_options.add_extension(extension)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")

        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "normal"
        self.driver = webdriver.Chrome(desired_capabilities=caps,
                                       executable_path=chrome_driver,chrome_options=chrome_options)
    
    def handle_recaptcha(self, frame):
        log_info("Solving recaptcha..")
        self.driver.switch_to_frame(frame)
        time.sleep(0.5)

        second_frame = self.driver.find_elements_by_tag_name('iframe')

        # There is a lot of the iframes embedded
        self.driver.switch_to_frame(second_frame[0])

        # print self.driver.page_source
        self.driver.find_element_by_id(
            'recaptcha-anchor').send_keys(Keys.ENTER)

        # Main frame
        self.driver.switch_to.default_content()
        time.sleep(1)
        second_frame = self.driver.find_elements_by_tag_name('iframe')
        self.driver.switch_to_frame(second_frame[0])

        time.sleep(1)

        # Inner frames
        frames = self.driver.find_elements_by_tag_name('iframe')
        self.driver.switch_to_frame(frames[1])

        time.sleep(1)
        log_info('Selecting an audio challenge...')
        self.driver.find_element_by_id(
            'recaptcha-audio-button').send_keys(Keys.ENTER)
        
        # click the button to play
        time.sleep(1)
        self.driver.find_element_by_id(
            'rc-audiochallenge-play-button').send_keys(Keys.ENTER)
        # remember to switch back
        self.driver.switch_to.default_content()

    def buy_product(self, url):
        self.driver.get(url)

        # check whether recaptcha has been enabled
        try:
            first_frame = self.driver.find_element_by_tag_name('iframe')

            # Handle recaptcha here
            if first_frame is not None:
                log_info('Captcha activated')
                self.handle_recaptcha(first_frame)
        except Exception as error:
            log_info(error)
            log_info('Captcha not activated, continuing with shopping')
        

        # Get details
        log_info("Looking for product...")
        time.sleep(1)
        self.driver.find_element_by_id('select-size').send_keys(Keys.ENTER)

        self.sizes = self.driver.find_elements_by_class_name('selectable')

        self.available_sizes = [str(size.text) for size in self.sizes]

        self.product_name = self.driver.find_element_by_class_name(
            'product-name').text

        self.details = 'Found ' + self.product_name + \
            ' - Sizes in stock ' + str(self.available_sizes)
        log_info(self.details)

        # select the first size
        log_info("selecting size " + self.available_sizes[0])
        self.driver.find_element_by_link_text(
            self.available_sizes[0]).send_keys(Keys.ENTER)

        log_info('Adding item to shopping cart')
        time.sleep(1)

        self.driver.find_element_by_id('add-to-cart').send_keys(Keys.ENTER)
        log_info('Product added to cart')
        time.sleep(1)

        log_info('Finalizing order')
        self.driver.find_element_by_class_name(
            'mini-cart-link-checkout').send_keys(Keys.ENTER)

    def login(self):
        try:
            log_info("Attempting login...")

            self.driver.find_element_by_class_name(
                'input-text').send_keys(self.email)
            self.driver.find_element_by_css_selector(
                "input[type='password']").send_keys(self.password)
            self.driver.find_element_by_css_selector(
                "button[type='submit']").send_keys(Keys.RETURN)

            log_info("Successfully logged in!")
        except:
            log_info("A problem occured during login")
