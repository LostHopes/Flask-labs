from app import app
from flask import render_template

@app.errorhandler(404)
def page_not_found(request):
    return render_template("not_found.html"), 404
