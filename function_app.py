import azure.functions as func
from flask import Flask, Response, render_template, request, redirect
from validate import is_valid_url, is_valid_custom_url
import random
import os
import urllib.parse
from storage_client import store_url, get_full_url, check_full_url, check_short_url, get_url_count

flask = Flask(__name__)


@flask.get("/")
def return_http():
    return render_template("index.html", ctx={'disable_submit': False})


@flask.post('/validate')
def validate():
    url = request.form['url'].strip()
    custom_url = request.form['custom_url'].strip()

    # valid if url is valid and custom url is empty or not invalid
    url_valid = is_valid_url(url)
    custom_url_valid = not custom_url or is_valid_custom_url(custom_url)

    disable_submit = not url or not url_valid or not custom_url_valid

    ctx = {
        'url': url,
        'custom_url': custom_url,
        'disable_submit': False,
        'errors': {
            'url': "Invalid url" if not url_valid else None,
            'custom_url': 'Length must be 4-12 characters (letters, numbers, - or _)' if not custom_url_valid else None
        },
    }

    return render_template("form.html", ctx=ctx)

@flask.get('/count')
def count_urls():
    count = get_url_count()
    return render_template("count.html", count=count)


@flask.get('/go/<short_url>')
def go(short_url):
    try:
        url, error_code = get_full_url(short_url)
        return redirect(urllib.parse.unquote_plus(url))
    except Exception as e:
        if error_code == 404:
            return Response("Not found", status=404)
        else:
            return Response("Internal server error", status=500)


@flask.post('/shorten')
def shorten_url():
    url = request.form['url'].strip()
    custom_url = request.form['custom_url'].strip()

    # valid if url is valid and custom url is empty or not invalid
    url_valid = is_valid_url(url)
    custom_url_valid = not custom_url or is_valid_custom_url(custom_url)

    ctx = {
        'url': url,
        'custom_url': custom_url,
        'disable_submit': False,
        'errors': {
            'url': "Invalid url" if not url_valid else None,
            'custom_url': 'Length must be 4-12 characters (letters, numbers, - or _)' if not custom_url_valid else None
        },
    }

    has_validation_errors = any(error is not None for error in ctx['errors'].values())

    if has_validation_errors:
        return render_template("form.html", ctx=ctx)

    ### CUSTOM URL FLOW
    if custom_url:
        existing_short_url, error_code = check_short_url(custom_url)
        if existing_short_url:
            ctx["errors"]["custom_url"] = 'Custom URL already exists'
            return render_template("form.html", ctx=ctx)

        # store the url with the custom url
        store_url(url, custom_url, True)
        short_link = request.host_url + 'go/' + custom_url
        return render_template("success.html", short_link=short_link, ctx={'disable_submit': False})

    ### RANDOM URL FLOW   
    
    # check if url is already shortened
    existing_short_url, error_code = check_full_url(url)
    if existing_short_url:
        short_link = request.host_url + 'go/' + existing_short_url
        return render_template("success.html", short_link=short_link, ctx={'disable_submit': False})

    # generate random string of 6 characters
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    short_url = ''.join(random.choice(chars) for i in range(6))
    while True:
        existing_short_url, error_code = check_short_url(short_url)
        if not existing_short_url:
            break
        short_url = ''.join(random.choice(chars) for i in range(6))
    
    # store the url with the random string
    store_url(url, short_url, False)
    short_link = request.host_url + 'go/' + short_url
    return render_template("success.html", short_link=short_link, ctx={'disable_submit': False})


app = func.WsgiFunctionApp(app=flask.wsgi_app,
                           http_auth_level=func.AuthLevel.ANONYMOUS)