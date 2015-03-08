#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging,re

from transwarp.web import get,view,post,ctx
from apis import api, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError

from models import User,Blog,Comment

#@api
@view('blogs.html')
@get('/')
def test_users():
	blogs = Blog.find_all()
	user = User.find_first('where email=?','vinthony@gmail.com')
	return dict(blogs=blogs,user=user)

_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')

@api
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
    return user				

@view('register.html')
@get('/register')
def register():
    return dict()

@view('signin.html')
@get('/signin')
def signin():
	return dict()

@post('/api/authenticate')
def signin_user():
	pass