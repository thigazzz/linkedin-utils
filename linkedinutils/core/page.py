import logging
from abc import ABC, abstractmethod
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


Post = namedtuple("Post", "text, author")  # TODO: way to get the attachments of post


class PageInterface(ABC):
    # TODO: set driver and wait as property
    @abstractmethod
    def close(self) -> None: ...
    @abstractmethod
    def auth(self) -> None: ...
    @abstractmethod
    def get_post(self) -> Post: ...


class Page(PageInterface):
    def close(self) -> None:
        self.__driver.close()

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

    def get_post(self) -> Post:
        post_element = self.__driver.find_element(
            By.CSS_SELECTOR, "div.feed-shared-update-v2"
        )
        text = post_element.find_element(
            By.CSS_SELECTOR,
            "div.feed-shared-update-v2 div.feed-shared-update-v2__description-wrapper span.text-view-model",
        ).text.strip()
        title = post_element.find_element(
            By.CSS_SELECTOR, "span.text-view-model"
        ).text.strip()

        return Post(text=text, author=title)