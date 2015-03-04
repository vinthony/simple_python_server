# db.py 连接数据库相关操作

# 数据库引擎
class _Engine(object):
	"""docstring for _Engine"""
	def __init__(self, connect):
		self._connect = connect
	def connect(self):
		return self._connect()

engine = None

# 数据库上下文
class _DbCtx(threading.local):
	def __init__(self):
		self.connection = None
		self.transactions = 0

	def isinit(self):# 如果初始化过 则connection不为None
		return not self.connection is None	

	def init(self):
		self.connection = _LazyConnection()
		slef.transactions = 0

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

# 事务
class _TransationCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_close_conn = False
		if not _db_ctx.is_init():
			_db_ctx.init()
			self.should_close_conn = True
		_db_ctx.transactions += 1
		return self

	def __exit__(self, exctype, excvalue, traceback):
		global _db_ctx
		_db_ctx.transactions -= 1
		try:
		 	if _db_ctx.transactions = 0:
		 		if exctype is None:
		 			self.commit()
		 		else:
		 			self.rollback()
		 			
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

def insert():
	pass
def delete():
	pass	
def update():
	pass







