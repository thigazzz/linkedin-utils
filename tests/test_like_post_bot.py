import time
from linkedinutils.bots import like_post_bot

# TODO: close window
# TODO: add a verificaation if post already like
# to not fail the tests
def test_like_post():
    assert like_post_bot() == True

def test_do_not_like_already_liked_post():
    time.sleep(40)
    assert like_post_bot() == False