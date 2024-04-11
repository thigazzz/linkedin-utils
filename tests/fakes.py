import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from linkedinutils.core.page import PageInterface

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

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