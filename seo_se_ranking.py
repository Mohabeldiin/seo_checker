""""SEO Using SE Ranking: seranking.com"""

import logging
# import random
# import string

# try:
#     from modules.temp_mail_api.TempMailAPI import TempMail
# except (ImportError, ModuleNotFoundError) as ex:
#     logging.error("Module TempMailAPI not found")
#     raise ex("Module TempMailAPI not found") from ex
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


class SEORanking():
    """foo"""

    def __init__(self, url: str):
        """foo"""
        logger = self.__setup_loger()
        url = self.__validate_url(logger, url)
        driver = self.__setup_selenium_driver(logger)
        api = f"https://online.seranking.com/research.competitor.html/organic/keywords?input={url}&mode=base_domain&source=eg" # pylint: disable=line-too-long
        self.__open_seranking(logger, driver, api)

    @staticmethod
    def __setup_loger():
        """setup the logger
            Log Example:
                2022-05-24 00:45:56,230 - Seo - INFO: Message
            Returns:
                logging.Logger: logger"""
        logging.basicConfig(

            format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.DEBUG,
            filename='logs/seo_se_ranking.log',
            filemode="a")
        return logging.getLogger("Seo")

    @staticmethod
    def __validate_url(logger, url: str) -> str:
        """validate the url
            by removing the http:// or https:// or www.
            Args:
            url (str): url to validate
            Returns:
                str: url without http:// or https:// or www.
            Raises:
                Exception: if url is not string"""
        if url_validator(url):
            logger.info("Valid url: %s", url)
            if url.startswith("http://www."):
                url = url[11:]
            elif url.startswith("http://"):
                url = url[7:]
            elif url.startswith("https://www."):
                url = url[12:]
            elif url.startswith("https://"):
                url = url[8:]
            elif url.startswith("www."):
                url = url[4:]
            if url.endswith("/"):
                url = url[:-1]
            logger.debug("Returning url: %s", url)
        else:
            logger.critical("Invalid url: %s", url)
            raise Exception("Invalid url")
        return url

    @staticmethod
    def __setup_selenium_driver(logger) -> webdriver.Chrome:
        """foo"""
        logger.debug("Setting up selenium")
        options = webdriver.ChromeOptions()
        options.headless = False
        try:
            driver = webdriver.Chrome(
                executable_path="C:\\Program Files (x86)\\chromedriver.exe", options=options)
        except selenium_exceptions.WebDriverException:
            try:
                driver = webdriver.Chrome(
                    executable_path="C:\\chromedriver.exe", options=options)
            except selenium_exceptions.WebDriverException:
                logger.critical("Chrome driver not found")
                raise selenium_exceptions.WebDriverException(
                    selenium_exceptions.WebDriverException.__str__
                    )from selenium_exceptions.WebDriverException
            except Exception:
                logger.critical("Exception: %s", Exception)
                raise Exception(f"Exception: {Exception}") from Exception
            else:
                driver.implicitly_wait(5)
                logger.debug("Returning driver: %s", driver)
        return driver

    @staticmethod
    def __open_seranking(logger, driver, url):
        """foo"""
        try:
            driver.get(url)
        except selenium_exceptions.TimeoutException:
            logger.critical("TimeoutException")
            raise selenium_exceptions.TimeoutException(
                "TimeoutException") from selenium_exceptions.TimeoutException
        except selenium_exceptions.WebDriverException:
            logger.critical("Unable to open SE Ranking")
            raise selenium_exceptions.WebDriverException(
                "Unable to open SE Ranking") from selenium_exceptions.WebDriverException
        except Exception:
            logger.critical("Unable to open SE Ranking")
            raise Exception("Unable to open SE Ranking") from Exception
        else:
            driver.maximize_window()
            driver.implicitly_wait(5)


if __name__ == '__main__':
    seo = SEORanking("https://www.google.com")
