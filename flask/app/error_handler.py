from app import app
from flask import render_template

@app.errorhandler(404)
def page_not_found(request):
    title = "Not found"
    error = "Page not found"
    return render_template(
        "error.html", 
        title=title, 
        error=error), 404


@app.errorhandler(403)
def access_denied(request):
    title = "Access denied"
    error = "You have no permissions to do this"
    return render_template("error.html", title=title, error=error), 403
    
