"""foo"""
import logging

try:
    from validators import url as url_validator
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
    from selenium.common.exceptions import WebDriverException, TimeoutException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except (ImportError, ModuleNotFoundError) as ex:
    logging.error("Module selenium not found")
    raise ex("Module selenium not found") from ex


class Seo():
    """foo"""

    def __init__(self, url):
        """foo"""
        super().__init__()
        self.url = self.__validate_url(url)
        self._seo_checker = "https://www.semrush.com/website/"
        self.set_up()
        self._logger.info("Initializing Seo")

    def set_up(self):
        """set up selenium and logger
            for seo checker"""
        logging.basicConfig(
            format='%(name)s - %(levelname)s: %(message)s', level=logging.WARNING)
        self._logger = logging.getLogger("Seo")
        options = webdriver.ChromeOptions()
        options.headless = True
        try:
            self.driver = webdriver.Chrome(
                executable_path="C:\\Program Files (x86)\\chromedriver.exe", options=options)
        except WebDriverException:
            try:
                self.driver = webdriver.Chrome(
                    executable_path="C:\\chromedriver.exe", options=options)
            except WebDriverException:
                self._logger.critical("Chrome driver not found")
                raise WebDriverException(
                    "Chrome driver not found") from WebDriverException
            except Exception:
                self._logger.critical("Exception: %s", Exception)
                raise Exception(f"Exception: {Exception}") from Exception
            else:
                self.driver.implicitly_wait(5)
        try:
            self.driver.get(self._seo_checker)
        except TimeoutException:
            self._logger.critical("TimeoutException")
            raise TimeoutException("TimeoutException") from TimeoutException
        except WebDriverException:
            self._logger.critical("Unable to open seo checker")
            raise WebDriverException(
                "Unable to open seo checker") from WebDriverException
        except Exception:
            self._logger.critical("Unable to open seo checker")
            raise Exception("Unable to open seo checker") from Exception
        else:
            self.driver.maximize_window()
            self.driver.implicitly_wait(5)

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
            elif url.startswith("https://"):
                url = url[8:]
            elif url.startswith("www."):
                url = url[4:]
            if url.endswith("/"):
                url = url[:-1]
            self._logger.debug("Returning url: %s", url)
        else:
            self._logger.critical("Invalid url: %s", url)
            raise Exception("Invalid url")
        return url


if __name__ == '__main__':
    pass
