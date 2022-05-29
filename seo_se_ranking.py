""""SEO Using SE Ranking: seranking.com"""

import logging

try:
    from modules.validators import url as url_validator
except (ImportError, ModuleNotFoundError) as e:
    logging.error("Module validators not found: %s", e.__doc__)
    raise (f"Module validators not found: {e.__doc__}") from e

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
    """SEO Using SE Ranking: seranking.com"""

    def __init__(self, url: str):
        """Initializes the class"""
        self.__logger = self.__setup_loger()
        url = self.__validate_url(self.__logger, url)
        self.__driver = self.__setup_selenium_driver(self.__logger)
        api = f"https://online.seranking.com/research.competitor.html/organic/keywords?input={url}&mode=base_domain&source=eg"  # pylint: disable=line-too-long
        self.__open_seranking(self.__logger, self.__driver, api)
        self.__robot_handeler(url)

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
            filemode="w")
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
        """Sets up the selenium driver
            Returns:
                webdriver.Chrome: selenium driver
            Raises:
                WebDriverException: if unable to open selenium driver
                Exception: if unable to open selenium driver"""
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
        """Opens the seranking page

        Args:
            logger (logging.Logger): logger
            driver (webdriver.Chrome): driver
            url (str): url to open

        Raises:
            TimeoutException: if timeout
            WebDriverException: if chrome driver not found
            Exception: if any other exception"""
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

    def get_organic_traffic(self) -> dict:
        """Extract the organic traffic from the SE Ranking

        Returns:
            dict: {
                "Total traffic": int,
                    "Keywords": int,
                    "Total traffic cost": int,
                    "Backlinks": int
            }

            Raises:
                NoSuchElementException: if element is not found
                WebDriverException: if unable to open SE Ranking
                TimeoutException: if can't find element in time
                Exception: if no organic traffic is found
                """
        try:
            self.__logger.info("Extracting Organic traffic from SE Ranking")
            total_traffic, keyworks, total_traffic_cost, backlinks = self.__get_organic_traffic(
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
            organic_traffic = {
                "Organic traffic": {
                    "Total traffic": total_traffic,
                    "Keywords": keyworks,
                    "Total traffic cost": total_traffic_cost,
                    "Backlinks": backlinks
                }
            }
            self.__logger.debug(
                "Returning Organic traffic: %s", organic_traffic)
        return organic_traffic

    @staticmethod
    def __get_organic_traffic(logger, driver) -> dict:
        """Extracts Organic Traffic

        Returns:
            "Total traffic": int,
            "Keywords": int,
            "Total traffic cost": int,
            "Backlinks": int

        Raises:
            NoSuchElementException: if element is not found
            WebDriverException: if unable to open SE Ranking
            Exception: if no organic traffic is found"""
        try:
            elements = WebDriverWait(
                driver, timeout=5).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "keywords-traffic-chart-tab__value")))
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
            total_traffic = elements.pop(0).text
            keyworks = elements.pop(0).text
            total_traffic_cost = elements.pop(0).text
            backlinks = elements.pop(0).text
            logger.debug("Returning Organic traffic values")
        return total_traffic, keyworks, total_traffic_cost, backlinks

    def get_keywords(self):
        """foo"""
        self.__logger.info("Attempting to Extract keywords from SE Ranking")
        keywords = self.__get_keywords(self.__logger, self.__driver)
        self.__logger.debug("Returning keywords: %s", keywords)
        result = {
            "1": keywords[0],
            "2": keywords[1],
            "3": keywords[2],
            "4": keywords[3],
            "5": keywords[4],
            "6": keywords[5],
            "7": keywords[6],
            "8": keywords[7],
            "9": keywords[8],
            "10": keywords[9]
        }
        self.__logger.debug("Returning result: %s", result)
        return result

    @staticmethod
    def __get_keywords(logger, driver):
        """Extracts keywords

        Returns:
            list: list of keywords

        Raises:
            NoSuchElementException: if element is not found
            WebDriverException: if unable to open SE Ranking
            Exception: if no keywords are found"""
        keywords = []
        for index in range(1, 11):
            try:
                element = WebDriverWait(
                    driver, timeout=100).until(
                        EC.presence_of_element_located(
                            (By.XPATH, f'//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[3]/div/section[2]/div/div/div/div[1]/div[2]/div/div[1]/div[1]/div/table/tbody/tr[{str(index)}]/td[1]/div/div/div[2]/a')))  # pylint: disable=line-too-long
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
                keywords.append(element.text)
                logger.debug("Keyword: %s", element.text)
        return keywords

    def __robot_handeler(self, url: str):
        """Handles Google reCaptcha

        Args:
            url (str): url to be opened

        Raises:
            Exception: if unable to Handel reCaptcha"""
        try:
            if WebDriverWait(self.__driver, timeout=5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "recaptcha-popup__body"))):
                self.__logger.info("Robot handeler found")
                self.__driver.refresh()
                self.__robot_handeler(url)
        except selenium_exceptions.TimeoutException:
            self.__logger.info("Robot handeler not found")
            return
        except Exception as ex:
            self.__logger.critical(
                "Unable to to handle Google Robotes: %s", ex.__doc__)
            raise (f"Unable to to handle Google Robotes: {ex.__doc__}") from ex

    def get_result(self):
        """foo"""
        self.__logger.info("Attempting to Extract result from SE Ranking")
        organic_traffic = self.get_organic_traffic()
        keywords = self.get_keywords()
        result = {
            "Organic traffic": organic_traffic,
            "Keywords": keywords
        }
        self.__logger.debug("Returning result: %s", result)
        return result

    def __del__(self):
        """Tears down the driver"""
        self.__logger.debug("Tearing down driver")
        try:
            self.__driver.quit()
        except selenium_exceptions.WebDriverException as ex:
            self.__logger.critical("Unable to quit driver: %s", ex.__doc__)
            raise (f"Unable to quit driver: {ex.__doc__}") from ex
        except Exception as ex:
            self.__logger.critical("Unable to quit driver: %s", ex.__doc__)
            raise (f"Unable to quit driver: {ex.__doc__}") from ex
        else:
            del self.__driver
            self.__logger.debug("Tear Down Successfully.")
            del self.__logger


if __name__ == '__main__':
    seo = SEORanking("https://www.google.com")
    print(seo.get_result())
    del seo
