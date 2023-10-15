#!/usr/bin/env python
import cgi
import html
import http.cookies
import os

form = cgi.FieldStorage()

def form_handler():
    counter = 0

    song = form.getvalue("song")
    author = form.getvalue("author")
    genre = form.getvalue("genre")
    country = form.getvalue("country")

    if song != None:
        counter += 1
    if author != None:
        counter += 1
    if genre != None:
        counter += 1
    if country != None:
        counter += 1
    


    selected = {
        "song": song,
        "author": author,
        "genre": genre,
        "country": country,
        "counter": counter
    }
    return selected


def page():
    cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    cookie.setdefault("author", "Chihei Hitakeyama")
    cookie.setdefault("song", "Wave from the North")
    fields_counter = f"{form_handler()['counter']}/{len(form_handler()) - 1}"
    page = f"""Content-type: text/html\n
    <html>
    <body>
        <nav>
            <ul>
                <li>Song name: {form_handler()["song"]}</li>
                <li>Song author: {form_handler()["author"]}</li>
                <li>Song genre: {form_handler()["genre"]}</li>
                <li>Song country: {form_handler()["country"]}</li>
                <li>Non-Empty fields: {fields_counter}</li>
            </ul>
        </nav>
        <p>Author cookie: {cookie.get("song")}</p>
        <p>Song cookie: {cookie.get("author")}</p>
    </body>
    </html>"""
    print(page)


def main():
    page()


if __name__ == "__main__":
    main()