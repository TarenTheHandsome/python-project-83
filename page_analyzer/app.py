
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.database import (
    find_checks_by_url_id,
    find_url_by_id,
    get_all_urls,
    get_status_code_db,
    get_url,
    save_check,
    save_url,
)
from page_analyzer.html_parser import HtmlParser
from page_analyzer.url_validator import name_validator, normalize_url, validator

load_dotenv()

app = Flask(__name__)
app.secret_key = "super secret key"


# opens start page
@app.route('/')
def hello():
    return render_template('start_page.html')


# receives the URL and sends it to the database('urls' table)
@app.post('/urls')
def post_url():
    form_data = request.form.to_dict()
    url = form_data.get('url')
    error = [validator(url), name_validator(url)]
    if True in error:
        return render_template('errors/error.html'), 422
    id = save_url(normalize_url(url))
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_id', id=id))


# shows all URLs
@app.get('/urls')
def get_url_list():
    # добавить сюда статус код
    all_urls = get_all_urls()
    return render_template('urls.html', all_urls=all_urls)


# shows URL info without checking
@app.get('/urls/<id>')
def get_id(id):
    status = get_status_code_db(id)
    all_urls = find_url_by_id(id)
    return render_template('url.html', all_urls=all_urls, status=status)


# shows URL info with checking
@app.get('/urls/<id>/checks')
def get_check(id):
    status = get_status_code_db(id)
    all_checks = find_checks_by_url_id(id)
    all_urls = find_url_by_id(id)
    return render_template('check_button.html', all_checks=all_checks,
                           all_urls=all_urls, id=id, status=status)


# receives the URL info and sends it to the database('url_check' table)
@app.post('/urls/<id>/checks')
def post_check(id):
    url_name = get_url(id)
    if not url_name:
        flash('URL не найден', 'danger')
        return render_template('errors/error.html'), 422
    parser = HtmlParser(url_name)
    save_check(id, parser.status_code, parser.get_h1(),
               parser.get_title(), parser.get_description())
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_check', id=id))
