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
