from app import app
from flask import render_template


_ERROR_FILE = "error.html"

@app.errorhandler(405)
def access_denied(request):
    title = "Access denied"
    error = "You have no permissions to do this"
    return render_template(_ERROR_FILE, title=title, error=error)
    

@app.errorhandler(404)
def page_not_found(request):
    title = "Not found"
    error = "Page not found"
    return render_template(_ERROR_FILE, title=title, error=error)


@app.errorhandler(401)
def unauthorized(request):
    title = "Unauthorized access"
    error = "You must be authorized"
    return render_template(_ERROR_FILE, title=title, error=error)


@app.errorhandler(400)
def client_error(request):
    title = "Bad Request"
    error = "Server can't respond due to a bad request"
    return render_template(_ERROR_FILE, title=title, error=error)