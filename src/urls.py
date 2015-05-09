#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, datetime,time, base64, hashlib
from transwarp import colorlog
from transwarp.db import next_id
from transwarp.web import get,view,post,ctx,interceptor,seeother,notfound,found,Dict
from apis import api, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError
from config import configs
import sae.storage
import md5,uuid
SAE_BUCKET = configs.storage['bucket']
from models import User,Award,College

CHUNKSIZE = 8192
_COOKIE_NAME = 'awesession'
UPLOAD_PATH='upload'
_COOKIE_KEY = configs.session.secret
def datetime_filter(t):
    delta = int(time.time() - t)
    # if delta < 60:
    #     return u'1分钟前'
    # if delta < 3600:
    #     return u'%s分钟前' % (delta // 60)
    # if delta < 86400:
    #     return u'%s小时前' % (delta // 3600)
    # if delta < 604800:
    #     return u'%s天前' % (delta // 86400)
    dt = datetime.date.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)
def returndict(**kw):
    user = None
    try:
        user = ctx.request.user
    except Exception, e:
        user = None
    x = dict(user=user)
    x.update(dict(**kw))
    return x
def user_filter(sno):
    user = User.find_first('where sno=?',sno)
    return user.name
def type_filter(x):
    if x == 1:
        return u"奖励"
    else:
        return u"惩罚"  
@view('index.html')
@get('/')
def index():
    return returndict() 

_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')

@interceptor('/')
def user_interceptor(next):
   # colorlog.info('try to bind user from session cookie.')
    user = None 
    try:
        cookie = ctx.request.cookies[_COOKIE_NAME]
        user = parse_signed_cookie(cookie)
       # colorlog.info(user,identify='USER')
        if user:
            pass
         #   colorlog.info('bind user <%s> to session...'% user.name)
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
    sno = i.sno
    password = hashlib.md5(i.password).hexdigest()
    admin = i.identify
    user = User.find_first('where sno=?',sno)
    error = None
    if sno is None:
        error='Invalid sno.'
    elif user.password != password:
        error='Invalid password.'
    elif str(user.identify) != admin:
        error='Invalid identify'
    max_age = 604800
    cookie = make_signed_cookie(user.id,user.password,max_age)
    ctx.response.set_cookie(_COOKIE_NAME, cookie, max_age=max_age)
    if error:
        colorlog.info(error,identify='ERROR')
    else:    
        raise seeother('/')
@api
@post('/api/checkuser')
def checkuser():
    i = ctx.request.input()
    sno = i.sno
    password = hashlib.md5(i.password).hexdigest()
    admin = i['identify']
    user = User.find_first('where sno=?',sno)
    error = None
    if sno is None:
        error='Invalid sno.'
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
    i = ctx.request
    name = i['name'].strip().lower()    
    year = str(i['year'])
    sno = str(i['sno'])
    college = str(i['college'])
    temp = Dict(identify='0');
    if name:
        temp['name'] = name
    if year:
        temp['year'] = year
    if college:
        temp['college'] = college
    if sno:
        temp['sno'] = sno
    temp_str = ' and '.join([ k+'="'+v+'"' for k,v in temp.iteritems()])
    #colorlog.info(temp_str,identify='SQL');
    data = User.find_by('where '+temp_str) 
    for x in data:
        x.college = college_filter(x.college)
    if not name and not sno and not year and not college:
        return dict(code=500,message='没有筛选条件')     
    return dict(code=0,data=data,message='ok')    

def college_filter(id):
    college = College.find_by('where college_id=?',id)
    return college[0].college_name


@view('awardlist.html')
@get('/awardlist')
def awardlist():
    # 获奖情况列表
    page = ctx.request.get('p');
    awards = Award.find_by('where award_is_show=1');
    return returndict(awards=awards)
@api
@get('/api/search_award')
def search_award():
    i= ctx.request
    year = i['year']
    sno = i['sno']
    award_title=i['award_title']
    award_type =i['award_type']
    temp = Dict(award_is_show='1');    
    if year:
        temp['award_year'] = year
    if award_title:
        temp['award_title'] = award_title
    if sno:
        temp['sno'] = sno
    if award_type:
        temp['award_type'] = award_type
    temp_str = ' and '.join([ k+'="'+v+'"' for k,v in temp.iteritems()])
    data = Award.find_by('where '+temp_str)  
    colorlog.info(data,identify='SEARCH_AWARD')      
    for x in data:
        x.username = user_filter(x.award_user_id)
        x.award_type = type_filter(x.award_type)
        x.created_at = datetime_filter(x.created_at)
    if not sno and not year and not award_title and not award_title:
        return dict(code=500,message='没有筛选条件')     
    return dict(code=0,data=data,message='ok')    

@view('addstudent.html')
@get('/addstudent')
def addstudent():
    colleges = College.find_all()
    return returndict(college=colleges)

@view('myaward.html')
@get('/myaward/:sno')
def function(sno):
    awardlist = Award.find_by('where award_is_show = 1 and award_user_id=?',sno)
    colorlog.info(awardlist,identify='AWARDLIST')
    return returndict(awardlist=awardlist)

@api
@post('/api/addstudent')
def add_student():
    i = ctx.request
    name = i['name']
    year = i['year']
    college = i['college']
    message = 'error happened'
    if name and year and college:
        sid = len(User.find_by('where year='+year+' and college='+college+' and identify=0'))+1
        sno = getlast2(college)+getlast2(year)+getlast2(str(sid))
        #colorlog.info(sno,identify='SNO')
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

@api
@post('/api/addaward')
def add_award():
    i = ctx.request
    # print i.image
    sno = i['sno']
    year = i['year']
    award_type = i['award_type']
    award_title = i['award_title'].strip()
    image = i['image']
    content = i['content'].strip()
    if sno and year and award_title and content and award_type and image:
        image_path = upload(image)
        print image_path
        award = Award(award_user_id=sno,award_year=year,award_title=award_title,award_content=content,award_type=award_type,image=image_path)
        award.insert()
        message = "successful insert %s" % award_title
    else:
        return dict(message=message,code='500')    
    return dict(message=message,code='0')        

@view('myinfomation.html')
@get('/u/:sno')
def myinfomation(sno):
    user = User.find_first('where sno=?',sno)
    return returndict(student=user)    

def upload(image):
    filename = os.path.join(UPLOAD_PATH,hashlib.md5(image.filename.encode('utf-8')).hexdigest()+uuid.uuid4().hex)
    if 'SERVER_SOFTWARE' in os.environ:
       conn = sae.storage.Connection() 
       bucket = conn.get_bucket(SAE_BUCKET)
       bucket.put_object(filename,image.file)
       filename = bucket.generate_url(filename)
    else:
        with open(filename,'w') as f:
            chunk = image.file.read(CHUNKSIZE)
            while chunk:
                f.write(chunk)
                chunk = image.file.read(CHUNKSIZE)
    return filename

@view('award.html')
@get('/awards/:id')
def award_id(id):
    award = Award.find_first('where id=?',id)
    return returndict(award=award)

@view('forgetpassword.html')
@get('/forgetpassword')
def forgetpassword():
    pass
@api
@post('/modifypassowrd')
def modifypassowrd():
    i = ctx.request
    u = ctx.request.user
    if u.password != hashlib.md5(i['old_pass']).hexdigest():
        return dict(message="密码错误！")    
    u.password = hashlib.md5(i['new_pass']).hexdigest()
    u.update()
    return dict(message="修改密码成功！")

@view('summary.html')
@get('/summary')
def summary():
    # last ten year
    dt = datetime.date.fromtimestamp(time.time())
    current = dt.year
    last = current - 10
    re = {}
    for x in xrange(last,current):
        re[x] = len(Award.find_by('where award_year=?',year))

    return dict(data_x=re.keys(),data_y=re.values())
