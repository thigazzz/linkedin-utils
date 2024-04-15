import logging
from linkedinutils.core.page import Page, Post

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def test_get_a_post():
    """
    >>> get_a_post()
    >>> (text: str, author: str, attachments: list[str])
    """
    page = Page()

    page.auth()
    post = page.get_post()

    assert post
    assert type(post) == Post

    page.close()

import time
from lxml import etree
from bs4 import BeautifulSoup
def test_click_in_like_button_of_post():
    page = Page()

    page.auth()
    post = page.get_post()
    is_liked_post = page.like_post(post=post.element)

    assert is_liked_post == True

    page.close()

def test_not_click_in_like_button_of_already_liked_post():
    page = Page()

    page.auth()
    post = page.get_post()

    # Tentei alterar o HTML interno do botão, de forma
    # a deixa-lo propicio para o teste.
    
    # post_html = post.element.get_attribute('innerHTML')
    # soup = BeautifulSoup(post_html, 'html.parser')
    # button_html = soup.select_one("span.reactions-react-button > button")
    # print(button_html["aria-pressed"])
    # button_html["aria-pressed"] = "true"
    # post.element.index

    time.sleep(30) # time to modify button
    is_liked_post = page.like_post(post=post.element)

    assert is_liked_post == False

    page.close()
