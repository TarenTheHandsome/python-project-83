import os
# from url_validator import validator
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

def validator(url):
    errors = {}
    if len(url) == 0:
        errors['url'] = 'Url не должен быть пустым'
    if len(url) > 255:
        errors['url'] = 'Url не должен быть длиннее 255 символов'

    return errors

app = Flask(__name__)
app.secret_key = "super secret key"

DATA = []

@app.route('/')
def hello():
    return render_template('start_page.html')

@app.get('/url_list')
def get_url_list():
    return DATA

@app.post('/')
def post_url():
    url = request.form.to_dict()
    errors = validator(url['url'])
    if errors:
        return 'Error'
    print(url)
    DATA.append(url)
    flash('S', 'success')
    resp = make_response(redirect(url_for('get_url_list')))
    return resp
