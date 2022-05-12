"""foo"""
import logging
import random
import string

try:
    from modules.temp_mail_api.TempMailAPI import TempMail
except (ImportError, ModuleNotFoundError) as ex:
    logging.error("Module TempMailAPI not found")
    raise ex("Module TempMailAPI not found") from ex
try:
    from modules.validators import url as url_validator
except (ImportError, ModuleNotFoundError) as ex:
    logging.error("Module validators not found")
    raise ex("Module validators not found") from ex
# try:
#     import requests
# except (ImportError, ModuleNotFoundError) as ex:
#     logging.error("ImportError: requests")
#     raise ex("ImportError: requests")
try:
    from selenium import webdriver
    from selenium.common import exceptions as selenium_exceptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except (ImportError, ModuleNotFoundError) as ex:
    logging.error("Module selenium not found")
    raise ex("Module selenium not found") from ex


class _testData(object):
    """holds the test data that will be used"""
    SEO_CHECKER = "https://www.semrush.com/"
    SEO_CHECKER_WEBSITE = "https://www.semrush.com/website/"
    url = ""
    temp_email = ""
    temp_password = ""
    URL_TEXT_FILED_LOCATOR = (By.CLASS_NAME, "\
            input__control\
            input__control--size_xl\
            index-search__input\
            ")
    START_NOW_BUTTON_LOCATOR = (By.CLASS_NAME, "index-search-start index-button index-button--xl")
    SINUP_EMAIL_TEXT_FILED_LOCATOR = (By.ID, "email")
    SINUP_PASSWORD_TEXT_FILED_LOCATOR = (By.ID, "password")
    SINUP_BUTTON_LOCATOR = (By.CLASS_NAME, "___SButton_rkzvx_gg_ ___SButton_1spyt_gg_ \
        _size_xl_rkzvx_gg_ _theme_primary-success_rkzvx_gg_ \
            __theme_primary-success_1spyt_gg_ __theme_1spyt_gg_")


class Seo(object):
    """foo"""

    def __init__(self, url: str):
        """foo"""
        super().__init__()
        self.test_data = _testData()
        self.temp_email = TempMail()
        self.__set_up(url)
        self._logger.info("Initializing Seo")
        self.__check_seo()
        self.__tear_down()

    def __check_seo(self):
        """check seo"""
        self._logger.info("Checking seo")
        self.__pass_url()
        self.driver.implicitly_wait(5)
        self.__create_account()
        self.driver.implicitly_wait(5)

    def __set_up(self, url: str):
        """set up selenium and logger
            for seo checker"""
        logging.basicConfig(
            format='%(name)s - %(levelname)s: %(message)s', level=logging.DEBUG)
        self._logger = logging.getLogger("Seo")
        options = webdriver.ChromeOptions()
        options.headless = True
        self.test_data.url = self.__validate_url(url)
        self.__set_up_temp_mail()
        self.__set_up_temp_password()
        try:
            self.driver = webdriver.Chrome(
                executable_path="C:\\Program Files (x86)\\chromedriver.exe", options=options)
        except selenium_exceptions.WebDriverException:
            try:
                self.driver = webdriver.Chrome(
                    executable_path="C:\\chromedriver.exe", options=options)
            except selenium_exceptions.WebDriverException:
                self._logger.critical("Chrome driver not found")
                raise selenium_exceptions.WebDriverException(
                    "Chrome driver not found") from selenium_exceptions.WebDriverException
            except Exception:
                self._logger.critical("Exception: %s", Exception)
                raise Exception(f"Exception: {Exception}") from Exception
            else:
                self.driver.implicitly_wait(5)
        try:
            self.driver.get(self.test_data.SEO_CHECKER)
        except selenium_exceptions.TimeoutException:
            self._logger.critical("TimeoutException")
            raise selenium_exceptions.TimeoutException(
                "TimeoutException") from selenium_exceptions.TimeoutException
        except selenium_exceptions.WebDriverException:
            self._logger.critical("Unable to open seo checker")
            raise selenium_exceptions.WebDriverException(
                "Unable to open seo checker") from selenium_exceptions.WebDriverException
        except Exception:
            self._logger.critical("Unable to open seo checker")
            raise Exception("Unable to open seo checker") from Exception
        else:
            self.driver.maximize_window()
            self.driver.implicitly_wait(5)

    def __set_up_temp_mail(self):
        """set up temp mail"""
        self._logger.info("Setting up temp mail")
        self.test_data.temp_email = self.temp_email.get_email()

    def __set_up_temp_password(self):
        """set up temp password"""
        self._logger.info("Setting up temp password")
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        size = 10
        self.test_data.temp_password = ''.join(random.choice(chars) for x in range(size, 20))

    def __validate_url(self, url: str) -> str:
        """validate the url
            by removing the http:// or https:// or www.
            Args:
            url (str): url to validate
            Returns:
                str: url without http:// or https:// or www.
            Raises:
                Exception: if url is not string"""
        if url_validator(url):
            self._logger.info("Valid url: %s", url)
            if url.startswith("http://"):
                url = url[7:]
            elif url.startswith("http://www."):
                url = url[11:]
            elif url.startswith("https://"):
                url = url[8:]
            elif url.startswith("https://www."):
                url = url[12:]
            elif url.startswith("www."):
                url = url[4:]
            if url.endswith("/"):
                url = url[:-1]
            self._logger.debug("Returning url: %s", url)
        else:
            self._logger.critical("Invalid url: %s", url)
            raise Exception("Invalid url")
        return url

    def __pass_url(self):
        """pass the url to seo checker"""
        self._logger.info("Passing url: %s", self.test_data.url)
        url_text_field = self.__handle_text_filed_element(
            self.test_data.URL_TEXT_FILED_LOCATOR)
        url_text_field.clear()
        url_text_field.send_keys(self.test_data.url)
        start_now_button = self.__handle_button_element(
            self.test_data.START_NOW_BUTTON_LOCATOR
            )
        start_now_button.click()

    def __create_account(self):
        """create account"""
        self._logger.info("Creating account")
        email_text_field = self.__handle_text_filed_element(
            self.test_data.SINUP_EMAIL_TEXT_FILED_LOCATOR)
        email_text_field.clear()
        email_text_field.send_keys(self.test_data.temp_email)
        password_text_field = self.__handle_text_filed_element(
            self.test_data.SINUP_PASSWORD_TEXT_FILED_LOCATOR)
        password_text_field.clear()
        password_text_field.send_keys(self.test_data.temp_password)
        sign_up_button = self.__handle_button_element(
            self.test_data.SINUP_BUTTON_LOCATOR)
        sign_up_button.click()

    def __handle_text_filed_element(self, locator: tuple):
        """handle the element
            Args:
            locator (tuple): locator of the element
            Returns:
            raises:"""
        self._logger.info("Handling text filed element")
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(locator)
                )
        except selenium_exceptions.TimeoutException:
            self._logger.critical("TimeoutException")
            raise selenium_exceptions.TimeoutException("TimeoutException") from \
                selenium_exceptions.TimeoutException
        except selenium_exceptions.InvalidSelectorException:
            self._logger.critical("InvalidSelectorException")
            raise selenium_exceptions.InvalidSelectorException(
                "InvalidSelectorException") from selenium_exceptions.InvalidSelectorException
        except EC.NoSuchElementException:
            self._logger.critical("NoSuchElementException")
            raise EC.NoSuchElementException("NoSuchElementException") from EC.NoSuchElementException
        except selenium_exceptions.WebDriverException:
            self._logger.critical("WebDriverException")
            raise selenium_exceptions.WebDriverException("WebDriverException") from \
                selenium_exceptions.WebDriverException
        except Exception:
            self._logger.critical("Exception")
            raise Exception("Exception") from Exception

        self._logger.debug("returning text filed element")
        return element

    def __handle_button_element(self, locator: tuple):
        """handle the element
            Args:
            locator (tuple): locator of the element
            Returns:
            raises:"""
        self._logger.info("Handling button element")
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator)
                )
        except selenium_exceptions.TimeoutException:
            self._logger.critical("TimeoutException")
            raise selenium_exceptions.TimeoutException("TimeoutException") from \
                selenium_exceptions.TimeoutException
        except selenium_exceptions.InvalidSelectorException:
            self._logger.critical("InvalidSelectorException")
            raise selenium_exceptions.InvalidSelectorException(
                "InvalidSelectorException") from selenium_exceptions.InvalidSelectorException
        except EC.NoSuchElementException:
            self._logger.critical("NoSuchElementException")
            raise EC.NoSuchElementException("NoSuchElementException") from EC.NoSuchElementException
        except selenium_exceptions.WebDriverException:
            self._logger.critical("WebDriverException")
            raise selenium_exceptions.WebDriverException("WebDriverException") from \
                selenium_exceptions.WebDriverException
        except Exception:
            self._logger.critical("Exception")
            raise Exception("Exception") from Exception

        self._logger.debug("returning button element")
        return element

    def __tear_down(self):
        """tear down"""
        self._logger.info("Tearing down")
        self.driver.quit()

if __name__ == '__main__':
    seo = Seo("https://play.anghami.com/")
