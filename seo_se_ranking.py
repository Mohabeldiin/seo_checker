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
        self.__logger = self.__setup_loger()
        self.url = self.__validate_url(url)
        self.api = f"https://online.seranking.com/research.competitor.html/organic/keywords?input=\
            {self.url}&mode=base_domain&source=eg"

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
            self.__logger.info("Valid url: %s", url)
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
            self.__logger.debug("Returning url: %s", url)
        else:
            self.__logger.critical("Invalid url: %s", url)
            raise Exception("Invalid url")
        return url

    def __setup_selenium(self):
        """foo"""
        self.__logger.debug("Setting up selenium")
        options = webdriver.ChromeOptions()
        options.headless = True

if __name__ == '__main__':
    seo = SEORanking("https://www.google.com")
