#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'vinthony@gmail.com'


import time,uuid

from transwarp.db import next_id
from transwarp.orm import Model,StringField,BooleanField,FloatField,TextField,IntegerField

class User(Model):
	__table__ = 'users'
	
	id = StringField(primary_key=True,default=next_id,ddl='varchar(50)')
	email = StringField(updatable=False,ddl='varchar(50)')
	password = StringField(ddl='varchar(50)')
	college = IntegerField()
	year = IntegerField()
	identify = BooleanField()
	name = StringField(ddl='varchar(50)')
	created_at = FloatField(updatable=False,default = time.time)

class Award(Model):
	__table__ = 'award'
	id = StringField(primary_key=True,default=next_id,ddl='varchar(50)')	
	award_name = StringField(ddl='varchar(50)')
	award_user_id = StringField(ddl='varchar(50)')
	award_is_show = BooleanField()
	award_content = TextField()
	created_at = FloatField(updatable = False,default=time.time)

class College(Model):
	__table__ = 'college'

	id = StringField(primary_key=True,default=next_id,ddl='varchar(50)')
	college_id = StringField(updatable=False,ddl='varchar(50)')
	college_name = StringField(ddl='varchar(50)')
	created_at = FloatField(updatable=False,default = time.time)	
		