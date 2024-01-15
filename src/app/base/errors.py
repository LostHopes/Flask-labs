from app.base import base
from flask import render_template


_ERROR_FILE = "error.html"

@base.errorhandler(405)
def access_denied(request):
    title = "Access denied"
    error = "You have no permissions to do this"
    return render_template(_ERROR_FILE, title=title, error=error)
    

@base.errorhandler(404)
def page_not_found(request):
    title = "Not found"
    error = "Page not found"
    return render_template(_ERROR_FILE, title=title, error=error)


@base.errorhandler(401)
def unauthorized(request):
    title = "Unauthorized access"
    error = "You must be authorized"
    return render_template(_ERROR_FILE, title=title, error=error)


@base.errorhandler(400)
def client_error(request):
    title = "Bad Request"
    error = "Server can't respond due to a bad request"
    return render_template(_ERROR_FILE, title=title, error=error)