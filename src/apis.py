#!/usr/local/env python
# -*- coding:utf-8 -*-

import re, json, functools
from transwarp.web import ctx
def dumps(obj):
	return json.dumps(obj)
class APIError(StandardError):
    '''
    the base APIError which contains error(required), data(optional) and message(optional).
    '''
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message

class APIValueError(APIError):
    '''
    Indicate the input value has error or invalid. The data specifies the error field of input form.
    '''
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value:invalid', field, message)

class APIResourceNotFoundError(APIError):
    '''
    Indicate the resource was not found. The data specifies the resource name.
    '''
    def __init__(self, field, message=''):
        super(APIResourceNotFoundError, self).__init__('value:notfound', field, message)

class APIPermissionError(APIError):
    '''
    Indicate the api has no permission.
    '''
    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission:forbidden', 'permission', message)



def api(func):
	@functools.wraps(func)
	def _wrapper(*args,**kw):
		try:
			r = json.dumps(func(*args,**kw))
		except APIError,e:
			r = json.dumps(dict(error=e.error,data=e.data,message=e.message))
		except Exception,e:
			r = json.dumps(dict(error='internalerror',data=e.__class__.__name__,message=e.message))
		ctx.response.contetn_type = 'application/json'			
		return r
	return _wrapper	