import os
import uuid
import getpass
import hashlib
import base64
import datetime

from peewee import *

D = datetime.date
DT = datetime.datetime

DB_PATH = "nister.db"
db = SqliteDatabase(DB_PATH)

SESSION_MAX_AGE = datetime.timedelta(hours=10)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(max_length=32, unique=True)
    realname = CharField(max_length=128)
    pw_hash = CharField(max_length=64)
    pw_salt = CharField(max_length=64)
    isadmin = BooleanField()

    def test_password(self, password):
        b_password = password.encode()
        b_pw_salt = base64.b64decode(self.pw_salt)
        dk = hashlib.pbkdf2_hmac('sha256', b_password, b_pw_salt, 100000)
        pw_hash = dk.hex()
        return pw_hash == self.pw_hash

    def new_lab(self, name, desc, color):
        lab = Lab.create(name=name, desc=desc, color=color)
        Access.create(lab=lab, user=self, role='C')
        return lab

    def new_project(self, lab, name, goal):
        return Project.create(
            lab=lab, name=name, goal=goal, creator=self, start=DT.now()
        )

    def new_issue(self, proj, title, desc):
        num = proj.last_issue().num + 1
        return Issue.create(
            proj=proj, num=num, creator=self,
            start=DT.now(), title=title, desc=desc
        )

    def new_comment(self, issue, desc):
        num = issue.last_comment().num + 1
        return Comment.create(
            issue=issue, num=num, user=self, time=DT.now(), desc=desc
        )

    # all events visible to self (not just self's actions)
    def last_events(self, limit=-1):
        labs = [acc.lab for acc in Access.select().where(Access.user == self)]
        events = []
        for lab in labs:
            events += lab.last_events(limit)
        events.sort(key=lambda ev: ev[0], reverse=True)
        if limit > 0:
            events = events[:limit]
        return events

class Session(BaseModel):
    key = UUIDField(unique=True)
    user = ForeignKeyField(User, backref="sessions")
    start = DateTimeField()

class Lab(BaseModel):
    name = CharField(max_length=32, unique=True)
    desc = CharField(max_length=128)
    color = CharField(max_length=7) # "#RRGGBB"

    def membership(self, user):
        access = Access.get_or_none((Access.lab == self) & (Access.user == user))
        if access is None:
            return 'N'
        return access.role

    def last_events(self, limit=-1):
        events = []
        for proj in self.projects:
            events += proj.last_events(limit)
        events.sort(key=lambda ev: ev[0], reverse=True)
        if limit > 0:
            events = events[:limit]
        return events

class Access(BaseModel):
    lab = ForeignKeyField(Lab, backref="permissions")
    user = ForeignKeyField(User, backref="permissions")
    role = CharField(max_length=1) # [G]uest/[M]ember/[C]ore

class Project(BaseModel):
    lab = ForeignKeyField(Lab, backref="projects")
    name = CharField(max_length=32, unique=True)
    goal = CharField(max_length=128)
    creator = ForeignKeyField(User, backref="created_projects")
    start = DateTimeField()

    def last_issue(self):
        return self.issues.order_by(Issue.num.desc()).first()

    def last_events(self, limit=-1):
        events = [(self.start, self)]
        for issue in self.issues:
            events += issue.last_events(limit)
        events.sort(key=lambda ev: ev[0], reverse=True)
        if limit > 0:
            events = events[:limit]
        return events

class Issue(BaseModel):
    proj = ForeignKeyField(Project, backref="issues")
    num = IntegerField()
    creator = ForeignKeyField(User, backref="created_issues")
    closer = ForeignKeyField(User, backref="closed_issues")
    start = DateTimeField()
    end = DateTimeField()
    title = CharField(max_length=128)
    desc = TextField()

    def is_open(self):
        return self.end is None

    def last_comment(self):
        return self.comments.order_by(Comment.num.desc()).first()

    def last_events(self, limit=-1):
        comms = self.comments.order_by(Comment.time.desc())
        if limit > 0:
            comms = comms.limit(limit)
        events = [(self.start, self), (self.end, self)]
        events += [(comm.time, comm) for comm in comms]
        events.sort(key=lambda ev: ev[0], reverse=True)
        if limit > 0:
            events = events[:limit]
        return events

class Comment(BaseModel):
    issue = ForeignKeyField(Issue, backref="comments")
    num = IntegerField()
    user = ForeignKeyField(User, backref="comments")
    time = DateTimeField()
    desc = TextField()

def is_foreign_key(field):
    return isinstance(field, ForeignKeyField)

def hash_password(password):
    b_password = password.encode()
    b_pw_salt = os.urandom(32)
    dk = hashlib.pbkdf2_hmac('sha256', b_password, b_pw_salt, 100000)
    pw_hash = dk.hex()
    pw_salt = base64.b64encode(b_pw_salt).decode()  # convert binary to str()
    return pw_hash, pw_salt

def new_user(username, realname, password, isadmin):
    pw_hash, pw_salt = hash_password(password)
    return User.create(
        username=username,
        realname=realname,
        pw_hash=pw_hash,
        pw_salt=pw_salt,
        isadmin=isadmin
    )

def clean_old_sessions():
    now = datetime.datetime.now()
    for session in Session.select():
        if (now - session.start) > SESSION_MAX_AGE:
            session.delete_instance()

def login(username, password):
    user = User.get_or_none(User.username == username)
    if user is None:
        return None
    if not user.test_password(password):
        return None
    clean_old_sessions()
    key = str(uuid.uuid4())
    return Session.create(key=key, user=user, start=datetime.datetime.now())

def get_last_events(limit=-1):
    projs = Project.select().order_by(Project.start.desc())
    iopens = Issue.select().order_by(Issue.start.desc())
    closes = Issue.select().order_by(Issue.end.desc())
    comms = Comment.select().order_by(Comment.time.desc())
    if limit > 0:
        projs = projs.limit(limit)
        iopens = iopens.limit(limit)
        closes = closes.limit(limit)
        comms = comms.limit(limit)
    events = []
    events += [(proj.start, proj) for proj in projs]
    events += [(iopen.start, iopen) for iopen in iopens]
    events += [(close.end, close) for close in closes]
    events += [(comm.time, comm) for comm in comms]
    events.sort(key=lambda ev: ev[0], reverse=True)
    if limit > 0:
        events = events[:limit]
    return events

all_tables = [User, Session, Lab, Access, Project, Issue, Comment]

def create_tables():
    db.create_tables(all_tables)

def init_users():
    password = getpass.getpass("Admin Password: ")
    root = new_user("admin", "Administrator", password, True)

if __name__ == "__main__":
    try:
        os.remove(DB_PATH)
    except FileNotFoundError:
        pass
    create_tables()
    init_users()
