""""SEO Using SE Ranking: seranking.com"""

import logging
# import random
# import string

# try:
#     from modules.temp_mail_api.TempMailAPI import TempMail
# except (ImportError, ModuleNotFoundError) as e:
#     logging.error("Module TempMailAPI not found: %s", e.__doc__)
#     raise (f"Module TempMailAPI not found: {e.__doc__}") from e
try:
    from modules.validators import url as url_validator
except (ImportError, ModuleNotFoundError) as e:
    logging.error("Module validators not found: %s", e.__doc__)
    raise (f"Module validators not found: {e.__doc__}") from e
# try:
#     import requests
# except (ImportError, ModuleNotFoundError) as e:
#     logging.error("ImportError: requests: %s", e.__doc__)
#     raise (f"ImportError: requests: " {e.__doc__}) from e
try:
    from selenium import webdriver
    from selenium.common import exceptions as selenium_exceptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except (ImportError, ModuleNotFoundError) as e:
    logging.error("Module selenium not found: %s", e.__doc__)
    raise (f"Module selenium not found: {e.__doc__}") from e


class SEORanking():
    """foo"""

    def __init__(self, url: str):
        """foo"""
        self.__logger = self.__setup_loger()
        url = self.__validate_url(self.__logger, url)
        self.__driver = self.__setup_selenium_driver(self.__logger)
        api = f"https://online.seranking.com/research.competitor.html/organic/keywords?input={url}&mode=base_domain&source=eg" # pylint: disable=line-too-long
        self.__open_seranking(self.__logger, self.__driver, api)

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
        options.headless = True
        try:
            driver = webdriver.Chrome(
                executable_path="C:\\Program Files (x86)\\chromedriver.exe", options=options)
        except selenium_exceptions.WebDriverException:
            try:
                driver = webdriver.Chrome(
                    executable_path="C:\\chromedriver.exe", options=options)
            except selenium_exceptions.WebDriverException as ex:
                logger.critical("Chrome driver not found: %s", ex.__doc__)
                raise (f"Chrome driver not found: {ex.__doc__}") from ex
            except Exception as ex:
                logger.critical("Exception: %s", ex.__doc__)
                raise (f"Exception: {ex.__doc__}") from ex
            else:
                driver.implicitly_wait(5)
                logger.debug("Returning driver: %s", driver)
        return driver

    @staticmethod
    def __open_seranking(logger, driver, url):
        """foo"""
        try:
            driver.get(url)
        except selenium_exceptions.TimeoutException as ex:
            logger.critical("TimeoutException: %s", ex.__doc__)
            raise (f"TimeoutException: {ex.__doc__}") from ex
        except selenium_exceptions.WebDriverException as ex:
            logger.critical("Unable to open SE Ranking: %s", ex.__doc__)
            raise (f"Unable to open SE Ranking: {ex.__doc__}") from ex
        except Exception as ex:
            logger.critical("Unable to open SE Ranking: %s", ex.__doc__)
            raise (f"Unable to open SE Ranking: {ex.__doc__}") from ex
        else:
            driver.maximize_window()
            driver.implicitly_wait(5)

    def get_seranking_data(self) -> dict:
        """foo"""
        data = {}
        try:
            data["seranking_data"] = self.__get_seranking_data(
                self.__logger, self.__driver)
        except selenium_exceptions.TimeoutException as ex:
            self.__logger.critical("TimeoutException: %s", ex.__doc__)
            raise (f"TimeoutException: {ex.__doc__}") from ex
        except selenium_exceptions.WebDriverException as ex:
            self.__logger.critical("Unable to open SE Ranking: %s", ex.__doc__)
            raise (f"Unable to open SE Ranking: {ex.__doc__}") from ex
        except Exception as ex:
            self.__logger.critical("Unable to open SE Ranking: %s", ex.__doc__)
            raise (f"Unable to open SE Ranking: {ex.__doc__}") from ex
        else:
            self.__logger.debug("Returning data: %s", data)
        return data

    @staticmethod
    def __get_seranking_data(logger, driver) -> dict:
        """foo"""
        data = {}
        try:
            data["seranking_data"] = driver.find_element(By.ID,
                "organic-keywords-table").text
        except selenium_exceptions.NoSuchElementException as ex:
            logger.critical("NoSuchElementException: %s", ex.__doc__)
            raise (f"NoSuchElementException: {ex.__doc__}") from ex
        except selenium_exceptions.WebDriverException as ex:
            logger.critical("Unable to open SE Ranking: %s", ex.__doc__)
            raise (f"Unable to open SE Ranking{ex.__doc__}") from ex
        except Exception as ex:
            logger.critical("Unable to open SE Ranking: %s", ex.__doc__)
            raise (f"Unable to open SE Ranking{ex.__doc__}") from ex
        else:
            logger.debug("Returning data: %s", data)
        return data


if __name__ == '__main__':
    seo = SEORanking("https://www.google.com")
    print(seo.get_seranking_data())
