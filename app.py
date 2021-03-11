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

def get_session_user():
    session = get_session()
    return session and session.user

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
    suser = get_session_user()
    return dict(suser=suser, labs=Lab.select())

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

@route('/users')
@view('users')
def show_users():
    suser = get_session_user()
    if not suser or not suser.isadmin:
        redirect('/')
    return dict(users=User.select(), suser=suser)

@route('/user/pass/<name>')
@view('user_pass')
def user_pass(name):
    user = User.get_or_none(User.username == name)
    suser = get_session_user()
    if None in (suser, user):
        redirect('/users')
    if user != suser and not suser.isadmin:
        redirect('/users')
    return dict(user=user, suser=suser)

@route('/user_pass/<_id:int>', method='POST')
def post_user_padd(_id):
    user = User.get_by_id(_id)
    suser = get_session_user()
    if None in (suser, user):
        redirect('/users')
    if user != suser and not suser.isadmin:
        redirect('/users')
    oldpass = request.forms.oldpass
    newpass = request.forms.newpass
    if request.forms.newpassconfirm != newpass:
        redirect('/user/pass/{}'.format(user.username))
    if not user.test_password(oldpass):
        redirect('/user/pass/{}'.format(user.username))
    pw_hash, pw_salt = hash_password(newpass)
    user.pw_hash = pw_hash
    user.pw_salt = pw_salt
    user.save()
    redirect('/users')

@route('/user/new')
@view('user_edit')
def user_new():
    suser = get_session_user()
    if not suser or not suser.isadmin:
        redirect('/')
    return dict(user=None, suser=suser)

@route('/user/edit/<name>')
@view('user_edit')
def user_edit(name):
    suser = get_session_user()
    if not suser or not suser.isadmin:
        redirect('/')
    user = User.get_or_none(User.username == name)
    if user is None:
        redirect('/')
    return dict(user=user, suser=suser)

@route('/user_new', method='POST')
def post_user_new():
    suser = get_session_user()
    if not suser or not suser.isadmin:
        redirect('/')
    uname = request.forms.uname
    rname = request.forms.rname
    isadmin = request.forms.admin == "yes"
    new_user(uname, rname, "", isadmin)
    redirect('/users')

@route('/user_upd/<_id:int>', method='POST')
def post_user_upd(_id):
    suser = get_session_user()
    if not suser or not suser.isadmin:
        redirect('/')
    user = User.get_by_id(_id)
    user.username = request.forms.uname
    user.realname = request.forms.rname
    user.isadmin = request.forms.admin == "yes"
    user.save()
    redirect('/users')

@route('/labs//new')
@view('lab_edit')
def lab_new():
    suser = get_session_user()
    if not suser:
        redirect('/')
    return dict(lab=None, suser=suser)

@route('/lab/<name>/edit')
@view('lab_edit')
def lab_edit(name):
    suser = get_session_user()
    lab = Lab.get_or_none(Lab.name == name)
    if lab.membership(suser) != 'C':
        redirect('/')
    return dict(lab=lab, suser=suser)

@route('/labs//new', method='POST')
def post_lab_new():
    suser = get_session_user()
    if not suser:
        redirect('/')
    name = request.forms.name
    desc = request.forms.desc
    color = request.forms.color
    suser.new_lab(name, desc, color)
    redirect('/')

@route('/labs/<_id:int>/edit', method='POST')
def post_lab_upd(_id):
    suser = get_session_user()
    lab = Lab.get_by_id(_id)
    if lab.membership(suser) != 'C':
        redirect('/')
    lab.name = request.forms.name
    lab.desc = request.forms.desc
    lab.color = request.forms.color
    lab.save()
    redirect('/')

run(host='localhost', port=8080)
