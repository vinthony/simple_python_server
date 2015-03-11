#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, time, base64, hashlib
from transwarp import colorlog

from transwarp.web import get,view,post,ctx,interceptor,seeother,notfound,found
from apis import api, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError
from config import configs

from models import User,Blog,Comment

_COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

@interceptor('/')
def user_interceptor(next):
    colorlog.info('try to bind user from session cookie.')
    user = None 
    cookie = ctx.request.cookies.get(_COOKIE_NAME)
    if cookie:
        colorlog.info('parse session cookie ...')
        user = parse_signed_cookie(cookie)
        if user:
            colorlog.info('bind user <%s> to session...')
    ctx.request.user = user             
    return next()

@view('index.html')
@get('/')
def index():
    try:
        if ctx.request.get('error'):
            return dict();
        user = parse_signed_cookie(ctx.request.cookies[_COOKIE_NAME])
    except KeyError, e:
        user = None
    return dict(user=user)    

_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')

#@api
@post('/api/users')
def register_user():
    i = ctx.request.input(name='',email='',password='')
    name = i.name.strip()
    email = i.email.strip().lower()
    password = i.password
    if not name :
    	raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
    	raise APIValueError('email')
    if not password:
    	raise APIValueError('password')
    user = User.find_first('where email=?',email)
    if user:
    	raise APIError('register:failed','email','email is already used')
    user = User(name=name,email=email,password=password,image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email).hexdigest())
    user.insert()
    cookie = make_signed_cookie(user.id,user.password,None)
    ctx.response.set_cookie(_COOKIE_NAME,cookie)
    return user		

@view('register.html')
@get('/register')
def register():
    return dict()

@view('signin.html')
@get('/login')
def signin():
	return dict()

def make_signed_cookie(id,password,max_age):
    expires = str(int(time.time()+(max_age or 86400)))
    L = [id,expires,hashlib.md5('%s-%s-%s-%s' % (id,password,expires,_COOKIE_KEY)).hexdigest()]    
    return '-'.join(L)
def parse_signed_cookie(cookie_str):
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        id,expires,md5 = L
        if int(expires) < time.time():
            return None
        user = User.get(id)
        if user is None:
            return None
        colorlog.info(user)
        if md5 != hashlib.md5('%s-%s-%s-%s' % (id,user.password,expires,_COOKIE_KEY)).hexdigest():
           return None
        return user                    
    except Exception,e:
        return None

def check_admin():
    user = ctx.request.user
    if user and user.admin:
        return 
    raise APIPermissionError('No permission.')


@interceptor('/manage/')
def manage_incerceptor(next):
    user = ctx.request.user
    if user and user.admin:
        return next()
    raise seeother('/signin')

@get('/signout')
def signout():
    ctx.response.delete_cookie(_COOKIE_NAME)
    raise seeother('/')

#@api
@post('/login')
def authenticate():
    i = ctx.request.input()
    name = i.name.strip().lower()
    password = i.password
    admin = i.identify
    user = User.find_first('where name=?',name)
    error = None
    if user is None:
        error='Invalid name.'
    elif user.password != password:
        error='Invalid password.'
    elif str(user.identify) != admin:
        error='Invalid identify'
    max_age = 604800
    cookie = make_signed_cookie(user.id,user.password,max_age)
    ctx.response.set_cookie(_COOKIE_NAME, cookie, max_age=max_age)
    user.password = '******'
    if error:
        colorlog.info(error)
    else:    
        raise seeother('/')
@api
@post('/api/checkuser')
def checkuser():
    i = ctx.request.input()
    name = i.name.strip().lower()
    password = i.password
    admin = i['identify']
    user = User.find_first('where name=?',name)
    error = None
    if user is None:
        error='Invalid name.'
    elif user.password != password:
        error='Invalid password.'
    elif str(user.identify) != admin:
        error='Invalid identify'
    if error:
        return dict(code='500',message=error)
    else:
        return dict(code='0',message='ok') 
@api
@get('/api/authenticate')
def getloginName():
    try:
        user = parse_signed_cookie(ctx.request.cookies[_COOKIE_NAME]) 
    except KeyError, e:
        user = None
    if user:
        return dict(user=user)    
    else:
        return dict(message='not login name')