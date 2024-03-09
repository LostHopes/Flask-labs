from flask_login import current_user
from flask import url_for

class BaseHelper:

    def __init__(self):
        pass

    def get_menu() -> list:
        menu = [
            {"text": "Albums", "link": url_for("base.albums")},
            {"text": "Contact", "link": url_for("base.contact")},
            {"text": "Skills", "link": url_for("skills.show")},
            {"text": "Todo", "link": url_for("todo.todo_list")},
            {"text": "Posts", "link": url_for("posts.show")},
            {"text": "About", "link": url_for("base.about")},
            {"text": "Feedback", "link": url_for("feedback.feedbacks")},
        ]

        if current_user.is_anonymous:
            menu.extend([
                {"text": "Login", "link": url_for("user.login")},
                {"text": "Register", "link": url_for("user.register")}
            ])
        else:
            menu.append(
                {"text": "Account", "link": url_for("user.account")},
            )

        return menu

    def get_albums() -> dict:
        albums = [
            {
                "title": "The Night Shift",
                "artist": "Larry June",
                "url": "60hrxgJN3QfheGpVzEcUFR"
            },
            {
                "title": "Sunnasritual",
                "artist": "Kveld",
                "url": "49BaLxo4HMWHyGOHpEzuHD"
            },
            {
                "title": "And Then You Pray For Me",
                "artist": "Westside Gunn",
                "url": "3CXoPCQuBb7kP9vEFcfXKU"
            }
        ]
        
        return albums
    
