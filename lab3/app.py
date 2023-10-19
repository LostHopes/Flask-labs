from flask import Flask, request, render_template, abort
from jinja2.exceptions import TemplateNotFound
import platform
from datetime import datetime


app = Flask(__name__)


@app.context_processor
def base():
    now = datetime.now()
    time = now.strftime("%d/%m/%y %H:%M:%S")
    return dict(
        platform=platform,
        agent=request.user_agent,
        time=time)


@app.route("/")
def index():
    title = "Home"
    return render_template("index.html", title=title)


@app.route("/about")
def about():
    title = "About"
    return render_template("about.html", title=title)


@app.route("/contact")
def contact():
    title = "Contact"
    return render_template("contact.html", title=title)


@app.route("/albums")
def albums():
    title="Albums"
    return render_template("albums.html", title=title)


@app.route("/skills/")
@app.route("/skills/<int:s_id>/")
def skills(s_id=None):
    title = "My skills"
    my_skills = {
        1: "Programming",
        2: "Running",
        3: "Linguistics",
        4: "Soft skills",
        5: "Fast reading and comprehension",
        6: "Tinkering",
    }

    return render_template("skills.html", title=title, my_skills=my_skills, s_id=s_id)


if __name__ == '__main__':
    app.run(debug=True)