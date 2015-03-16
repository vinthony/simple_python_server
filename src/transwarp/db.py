#!/usr/bin/env python
# -*- coding:utf-8 -*-
# db.py 连接数据库相关操作

__author__ = 'vinthony@gmail.com'

import time,uuid,functools,threading,colorlog

# Dict object: 
class Dict(dict):
	"""实现一个键值对映射 (k1,k2,k3),(v1,v2,v3) {k1:v1,k2:v2,k3:v3}"""
	def __init__(self, names=(),values=(),**kw):
		super(Dict, self).__init__(**kw)
		for k,v in zip(names,values):
			self[k] = v

	def __getattr__(self,key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'DICT' object has no attribute '%s'" % key)

	def __setattr__(self,key,value):
		self[key] = value		

# 生成一个随time变化的id		
def next_id(t=None):
	if t is None:
		t = time.time()
	return '%015d%s000' % (int(t*1000),uuid.uuid4().hex)	
#输出日志
def _profiling(start,sql=''): 
	t = time.time() - start
	if t > 0.1:
		colorlog.warning('[PROFILING] [DB] %s %s' % (t,sql))
	else:
		colorlog.info('[PROFILING] [DB] %s %s' % (t,sql))
# 处理错误
class DBError(Exception):
	pass
# 处理错误
class MultiColumnsError(DBError):
	pass

class _LazyConnection(object):

	def __init__(self):
		self.connection = None

	def cursor(self):
		if self.connection is None : #如果没有 connection 才开一个enginer
			connection = engine.connect()
			#colorlog.info('open connection <%s>....' % hex(id(connection)))
			self.connection = connection
		return self.connection.cursor()		

	def commit(self):#提交
		self.connection.commit()

	def rollback(self):#撤销
		self.connection.rollback()

	def cleanup(self):
		if self.connection: #断开连接
			connection = self.connection
			self.connection = None
			#colorlog.info('close connection <%s>...'% hex(id(connection)))

# 数据库引擎
class _Engine(object):
	"""docstring for _Engine"""
	def __init__(self, connect):
		self._connect = connect
	def connect(self):
		return self._connect()

engine = None

def create_engine(user,password,database,host='127.0.0.1',port=3306,**kw):
	import mysql.connector
	global engine
	if engine is not None:
		raise DBError('engine is already inited')
	params = dict(user=user,password=password,database=database,host=host,port=port)
	defaults = dict(use_unicode=True,charset='utf8',collation='utf8_general_ci',autocommit=False)
	for k,v in defaults.iteritems(): #kw为一个key，value对
	 	params[k] = kw.pop(k,v) # dict.pop(key[,default]) 如果dict中已经有key就returnkey 否则 return default 值
	params.update(kw) #update([other]) 用kw覆盖params中存在的键值对
	params['buffered'] = True
	engine = _Engine(lambda: mysql.connector.connect(**params)) #将所有的参数传递给engine
	colorlog.info('Init mysql engine <%s> ok' % hex(id(engine)))

# 数据库上下文
class _DbCtx(threading.local):
	def __init__(self):
		self.connection = None
		self.transactions = 0

	def isinit(self):# 如果初始化过 则connection不为None
		return not self.connection is None	

	def init(self):
		self.connection = _LazyConnection()
		self.transactions = 0

	def cleanup(self):#清除
		self.connection.cleanup()
		self.connection = None	

	def cursor(self):#定义游标
		return self.connection.cursor()

_db_ctx = _DbCtx()

# 连接上下文
class _ConnectionCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_cleanup = False
		if not _db_ctx.isinit():
			_db_ctx.init()
			self.should_cleanup = True
		return self
	
	def __exit__(self,exctype,excvalue,trackback):
		global _db_ctx
		if self.should_cleanup:
			_db_ctx.cleanup()

def connection():
	return _ConnectionCtx()

def with_connection(func): #functools.wraps 用来定义一个装饰器 这个装饰器的功能是连接数据库
	@functools.wraps(func)
	def _wrapper(*args,**kw):
		with _ConnectionCtx(): #在_ConnectionCtx()之后执行函数
			return func(*args,**kw)
	return _wrapper	


# 事务
class _TransationCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_close_conn = False
		if not _db_ctx.is_init():
			_db_ctx.init()
			self.should_close_conn = True
		_db_ctx.transactions += 1 #事务++
		return self

	def __exit__(self, exctype, excvalue, traceback):
		global _db_ctx
		_db_ctx.transactions -= 1 #事务--
		try:
		 	if _db_ctx.transactions == 0: #如果事务为0 
		 		if exctype is None: #如果 exctype 为空 则 执行
		 			self.commit() 
		 		else:
					self.rollback() #数据库事务的一致性 不一致则回滚
		finally:
			if self.should_close_conn:
				_db_ctx.cleanup()

	def commit(self):
		global _db_ctx
		try:
			_db_ctx.connection.commit()
		except:
			_db_ctx.connection.rollback()
			raise

	def rollback(self):
		global _db_ctx
		_db_ctx.connection.rollback() 				

def transaction():
	return _TransationCtx()

def with_transaction():
	@functools.wraps(func)
	def _wrapper(*args,**kw):
		_start = time.time()
		with _TransationCtx():
			return func(*args,**kw)
		_profiling(_start)
	return _wrapper

def _select(sql,first,*args):
	global _db_ctx 
	cursor = None
	sql = sql.replace('?','%s')
	colorlog.info('SQL:%s,ARGS:%s'%(sql,args))
	try:
		cursor = _db_ctx.connection.cursor()
		cursor.execute(sql,args)
		if cursor.description: #返回每一列的名称
			names = [ x[0] for x in cursor.description ]
		if first: #如果为true 则抓取一行
			values = cursor.fetchone()
			if not values:
				return None
			return Dict(names,values) #确定对应关系
		return [Dict(names,x) for x in cursor.fetchall()] #第二个参数为false时返回整个数据		   		
	finally:
		if cursor:
			cursor.close()

@with_connection
def select_one(sql,*args): #返回一列数据
	return _select(sql,True,*args)

@with_connection
def select_int(sql,*args):
	d = _select(sql,True,*args)
	if len(d) != 1: #返回一个数据
		raise MultiColumnsError('except only one column.')
	return d.values()[0]

@with_connection
def select(sql,*args): #select函数
	return _select(sql,False,*args)

@with_connection	
def _update(sql,*args): #update函数 包括update/delete
	global _db_ctx
	cursor = None
	sql = sql.replace('?','%s')
	colorlog.warning('SQL:%s,ARGS:%s' % (sql,args))
	try:
		cursor = _db_ctx.connection.cursor()
		cursor.execute(sql,args)
		r = cursor.rowcount
		if _db_ctx.transactions == 0 :
			colorlog.info('auto commit');
			_db_ctx.connection.commit()
		return r
	finally:
		if cursor:
			cursor.close()

def insert(table,**kw):#insert table 数据
	cols,args = zip(*kw.iteritems())
	sql = 'insert into `%s` (%s) values (%s)' % (table,','.join(['`%s`' % col for col in cols]),','.join(['?' for i in range(len(cols))]))
	return _update(sql,*args)

def update(sql,*args):
	return _update(sql,*args)

if __name__ == '__main__': #
	#colorlog.basicConfig(level=colorlog.INFO)
	u1 = dict(id=2000, name='Bob', email='bob@test.org', password='bobobob', last_modified=time.time())
	create_engine('root','123456','test')
	update('drop table if exists user')
	update('create table user (id int primary key,name text,email text,password text,last_modified real)')
	insert('user',**u1)
	u2 = select_one('select * from user where id=?', 2000)
	print u2.name




