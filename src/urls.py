#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, time, base64, hashlib
from transwarp import colorlog
from transwarp.db import next_id
from transwarp.web import get,view,post,ctx,interceptor,seeother,notfound,found,Dict
from apis import api, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError
from config import configs
import md5
from models import User,Award,College

_COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret
def returndict(**kw):
    user = None
    try:
        user = ctx.request.user
    except Exception, e:
        user = None
    x = dict(user=user)
    x.update(dict(**kw))
    return x

@view('index.html')
@get('/')
def index():
    return returndict() 

_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')

@interceptor('/')
def user_interceptor(next):
    colorlog.info('try to bind user from session cookie.')
    user = None 
    try:
        cookie = ctx.request.cookies[_COOKIE_NAME]
        user = parse_signed_cookie(cookie)
        colorlog.info(user,identify='USER')
        if user:
            colorlog.info('bind user <%s> to session...'% user.name)
        ctx.request.user = user             
    except Exception,e:
        print e;           
    return next()
#@api
@post('/api/users')
def register_user():
    i = ctx.request.input(name='',email='',password='')
    name = i.name.strip()
    email = i.email.strip().lower()
    password = hashlib.md5(i.password).hexdigest() 
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

@get('/signout')
def signout():
    ctx.response.delete_cookie(_COOKIE_NAME)
    raise seeother('/')

#@api
@post('/login')
def authenticate():
    i = ctx.request.input()
    name = i.name.strip().lower()
    password = hashlib.md5(i.password).hexdigest()
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
    if error:
        colorlog.info(error)
    else:    
        raise seeother('/')
@api
@post('/api/checkuser')
def checkuser():
    i = ctx.request.input()
    name = i.name.strip().lower()
    password = hashlib.md5(i.password).hexdigest()
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

@view('search.html')
@get('/search')
def search():
    # 查询学生
    page = ctx.request.get('p');
    student =User.find_by('where identify=0')
    colleges=College.find_all()
    return returndict(college=colleges,students=student)

@api
@get('/api/search_student')
def search_student():
    i = ctx.request.input()
    name = i['name'].strip().lower()    
    year = i['year']
    college = i['college']
    temp = Dict(identify=0);
    if name:
        temp['name'] = name
    if year:
        temp['year'] = year
    if college:
        temp['college'] = college
    temp_str = ' and '.join([ k+'="'+v+'"' for k,v in temp.iteritems()])
    colorlog.info(temp_str,identify='SQL');
    data = User.find_by('where '+temp_str)        
    if not name and not sno and not grade and not college:
        return dict(code=500,message='没有筛选条件')     
    return dict(code=0,data=data,message='ok')    


@view('awardlist.html')
@get('/awardlist')
def awardlist():
    # 获奖情况列表
    page = ctx.request.get('p');
    return returndict()
@api
@get('/api/search_award')
def search_award():
    pass

@view('addstudent.html')
@get('/addstudent')
def addstudent():
    colleges = College.find_all()
    return returndict(college=colleges)

@api
@post('/api/addstudent')
def add_student():
    i = ctx.request
    colorlog.info(i,identify='REQUEST')
    name = i['name']
    year = i['year']
    college = i['college']
    message = 'error happened'
    if name and year and college:
        sid = len(User.find_by('where year='+year+' and college='+college+' and identify=0'))+1
        sno = getlast2(college)+getlast2(year)+getlast2(str(sid))
        colorlog.info(sno,identify='SNO')
        email = sno+'@student.edu.cn'
        user_dict = dict(name=name,year=year,college=college,sno=sno,email=email)
        colorlog.info(user_dict,'USER_DICT')
        user=User(name=name,year=year,college=college,sno=sno,email=email)
        user.insert()
        message = "successful insert %s" % name
    else:
        return dict(message=message,code='500')    
    return dict(message=message,code='0')    

def getlast2(s):
    if len(s) < 2:
        return s.zfill(2)
    if len(s) == 4:
        return s[2:]    
    
@view('addaward.html')
@get('/addaward')
def addaward():
    return returndict()    

@view('myaward.html')
@get('/myaward')
def myaward():
    return returndict()

@view('myinfomation.html')
@get('/myinfomation')
def myinfomation():
    return returndict()    


