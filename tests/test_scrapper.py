import logging
from abc import ABC, abstractmethod
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

Post = namedtuple("Post", "text, author, attachments")


class PageInterface(ABC):
    # TODO: set driver and wait as property
    @abstractmethod
    def auth(self) -> None: ...
    @abstractmethod
    def get_post(self) -> Post: ...


class Page(PageInterface):
    def auth(self):
        self.__driver = webdriver.Firefox()
        self.__driver.get("https://www.linkedin.com")
        self.__driver.find_element(By.ID, "session_key").send_keys(
            "thiago.p.dasilva2005@gmail.com"
        )
        self.__driver.find_element(By.ID, "session_password").send_keys("Chavv1712$")
        self.__driver.find_element(
            By.CSS_SELECTOR, 'button[data-id="sign-in-form__submit-btn"]'
        ).click()

        logging.info("Login passed!")

        self.__wait_for_load_feed()

    def __wait_for_load_feed(self, timeout=10):
        wait = WebDriverWait(self.__driver, timeout=timeout)
        try:
            # wait the profile title in feed
            wait.until(
                lambda d: self.__driver.find_element(
                    By.CSS_SELECTOR,
                    "div.feed-identity-module [href='/in/thiagopdasilva/'] > div:last-child",
                ).is_displayed()
            )
            # wait the chat
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

    def get_post(self) -> list[Post]: ...


class TestPage(PageInterface):
    def open_linkeidin(self) -> None:
        self.__driver = webdriver.Firefox()
        self.__driver.get("https://www.linkedin.com")

    def auth(self):
        self.__driver = webdriver.Firefox()
        self.__driver.get("https://www.linkedin.com")
        self.__driver.find_element(By.ID, "session_key").send_keys(
            "thiago.p.dasilva2005@gmail.com"
        )
        self.__driver.find_element(By.ID, "session_password").send_keys("Chavv1712$")
        self.__driver.find_element(
            By.CSS_SELECTOR, 'button[data-id="sign-in-form__submit-btn"]'
        ).click()

        logging.info("Login passed!")

        wait = WebDriverWait(self.__driver, timeout=10)

        try:
            wait.until(
                lambda d: self.__driver.find_element(
                    By.CSS_SELECTOR,
                    "div.feed-identity-module [href='/in/thiagopdasilva/'] > div:last-child",
                )
            )

            wait.until(
                lambda d: self.__driver.find_element(
                    By.CSS_SELECTOR, "aside#msg-overlay > div"
                ).is_displayed()
            )

            logging.info("Feed loaded!")
        except:
            logging.warning("Feed not loaded!")
            return

    def get_post(self) -> Post: ...


def test_get_a_post():
    """
    >>> get_a_post()
    >>> (text: str, author: str, attachments: list[str])
    """
    assert_post = [Post(text="any", author="any", attachments=["any"])]
    page = Page()

    page.auth()
    post = page.get_post()

    assert post == assert_post
