from bottle import view, static_file, hook, route, run, request, response, redirect, template
import markdown2

from model import *

md_extras = ("break-on-newline code-friendly fenced-code-blocks "
             "header-ids strike tables task_list").split()

def render(md):
    return markdown2.markdown(md, extras=md_extras)

def get_session():
    key = request.cookies.get('key', "")
    return Session.get_or_none(Session.key == key)

@hook('before_request')
def _connect_db():
    db.connect()

@hook('after_request')
def _close_db():
    if not db.is_closed():
        db.close()

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/')

@route('/')
@view('home')
def home():
    session = get_session()
    suser = getattr(session, "user", None)
    return dict(suser=suser, labs=[])

@route('/login')
@view('login')
def show_login():
    session = get_session()
    if session is not None:
        redirect('/')
    else:
        return {}

@route('/login', method='POST')
def try_to_login():
    username = request.forms.username
    password = request.forms.password
    session = login(username, password)
    if session is not None:
        ts = datetime.datetime.now() + SESSION_MAX_AGE
        response.set_cookie('key', session.key, expires=ts)
    redirect('/login')

@route('/logout')
def logout():
    session = get_session()
    if session is not None:
        response.delete_cookie('key')
        session.delete_instance()
    redirect('/')

run(host='localhost', port=8080)
