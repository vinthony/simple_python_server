#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from transwarp.web import get,view

from models import User,Blog,Comment

@view('blogs.html')
@get('/')
def test_users():
	blogs = Blog.find_all()
	user = User.find_first('where email=?','vinthony@gmail.com')
	return dict(blogs=blogs,user=user)