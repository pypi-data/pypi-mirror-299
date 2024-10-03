from milea_notify.decorators import milea_notify
from milea_notify.utils import Notify


@milea_notify(label="New Demo Object created for me")
def new_demo_object_created_for_manager(user, url):
    notify = Notify(
        user=user,
        title="Neues Demo Object",
        content="Das ist eine Demo Benachrichtigung, da kannst sie ignorieren :)",
        url=url,
    )
    notify.to_browser()

@milea_notify(label="Test Notification")
def test_notification(user, url):
    pass
