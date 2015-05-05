#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
A WSGI application entry.
'''

from transwarp import colorlog

import os
import datetime,time
from transwarp import db
from transwarp.web import WSGIApplication, Jinja2TemplateEngine
from models import College,User
from config import configs

def college_filter(id):
    college = College.find_by('where college_id=?',id)
    return college[0].college_name
def user_filter(sno):
    user = User.find_first('where sno=?',sno)
    return user.name
def type_filter(x):
    arr = [u"校二等奖",u"校三等奖",u"校一等奖",u"省三等奖",u"省二等奖",u"省一等奖",u"国家三等奖",u"国家二等奖",u"国家一等奖"]
    return arr[int(x)]    
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
# init db:Template
db.create_engine(**configs.db)

# init wsgi app:
wsgi = WSGIApplication(os.path.dirname(os.path.abspath(__file__)))

template_engine = Jinja2TemplateEngine(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
template_engine.add_filter('datetime', datetime_filter)
template_engine.add_filter('getcollegename',college_filter)
template_engine.add_filter('getuser',user_filter)
template_engine.add_filter('awardtype',type_filter)
wsgi.template_engine = template_engine

import urls

wsgi.add_module(urls)
wsgi.add_interceptor(urls.user_interceptor)

if __name__ == '__main__':
    wsgi.run(9000, host='0.0.0.0')
else:
    import sae
    application = sae.create_wsgi_app(app.wsgifunc())