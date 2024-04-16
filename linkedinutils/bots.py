import logging
from .core import Page, Post

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def like_post_bot():
    def get_post(page: Page) -> Post:
        try:
            post_element = page.find_element(
                selector="div.feed-shared-update-v2", type_of_selector="CSS_SELECTOR"
            )
            author_el = page.find_element(
                selector="span.text-view-model",
                type_of_selector="CSS_SELECTOR",
                by_element=post_element,
            )
            content_el = page.find_element(
                selector="div.feed-shared-update-v2 div.feed-shared-update-v2__description-wrapper span.text-view-model",
                type_of_selector="CSS_SELECTOR",
                by_element=post_element,
            )

            logging.info("Scrap post")

            return Post(
                element=post_element,
                metadata=(author_el.text.strip(), content_el.text.strip()),
            )
        except:
            logging.info("Fail to scrap post")

    def like_post(page: Page, post) -> None:
        button = page.find_element(
            selector="span.reactions-react-button > button",
            type_of_selector="CSS_SELECTOR",
            by_element=post,
        )
        button_press_state = page.get_attribute(
            element=button, attribute="aria-pressed"
        )
        is_post_already_liked = True if button_press_state == "true" else False
        if is_post_already_liked == True:
            logging.info("Post already liked")
            return False

        page.click_element(element=button)
        logging.info("Liked post")
        return True

    page = Page()
    page.auth()
    post = get_post(page)
    return like_post(page, post.element)
