import os
import logging
from dataclasses import dataclass
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@dataclass
class Post:  # TODO: way to get the attachments of post
    element: str
    metadata: tuple[str, str]


class PageInterface(ABC):
    # TODO: set driver and wait as property
    # TODO: Add a type for Elements parameters and return
    @abstractmethod
    def close(self) -> None: ...
    @abstractmethod
    def auth(self) -> None: ...
    @abstractmethod
    def find_element(
        self, selector: str, type_of_selector: str, by_element=None
    ) -> None: ...
    @abstractmethod
    def get_attribute(self, element, attribute: str) -> None: ...
    @abstractmethod
    def click_element(self, element) -> None: ...


class Page(PageInterface):
    def close(self) -> None:
        self.__driver.close()

    def auth(self):
        self.__driver = webdriver.Firefox()
        self.__driver.get("https://www.linkedin.com")
        self.__driver.find_element(By.ID, "session_key").send_keys(
            os.environ.get("EMAIL_AUTH")
        )
        self.__driver.find_element(By.ID, "session_password").send_keys(
            os.environ.get("PASSWORD_AUTH")
        )
        self.__driver.find_element(
            By.CSS_SELECTOR, 'button[data-id="sign-in-form__submit-btn"]'
        ).click()

        logging.info("Login passed!")

        self.__wait_for_load_feed()

    def __wait_for_load_feed(self, timeout=10):
        wait = WebDriverWait(self.__driver, timeout=timeout)
        try:
            # wait the profile title element in feed
            wait.until(
                lambda d: self.__driver.find_element(
                    By.CSS_SELECTOR,
                    "div.feed-identity-module [href='/in/thiagopdasilva/'] > div:last-child",
                ).is_displayed()
            )
            # wait the chat element
            wait.until(
                lambda d: self.__driver.find_element(
                    By.CSS_SELECTOR, "aside#msg-overlay > div"
                ).is_displayed()
            )

            logging.info("Feed loaded!")
        except Exception as error:
            print(type(error))
            logging.warning("Feed not loaded!, because: %s", error)
            return

    def find_element(self, selector: str, type_of_selector: str, by_element=None):
        by = None
        match type_of_selector:
            case "ID":
                by = By.ID
            case "CSS_SELECTOR":
                by = By.CSS_SELECTOR
            case "CLASS_NAME":
                by = By.CLASS_NAME

        if by_element:
            return by_element.find_element(by, selector)
        return self.__driver.find_element(by, selector)

    def get_attribute(self, element, attribute: str):
        return element.get_attribute(attribute)

    def click_element(self, element):
        element.click()
