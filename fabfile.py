import os, re
from datetime import datetime

from fabric.api import *

env.user = 'root'
env.sudo_user ='root'
env.hosts = ['192.241.212.122']
db_user = 'root'
db_password = '123456'

_TAR_FILE = 'dist-awesome.tar.gz'

def build():
	includes = ['static','templates','transwarp','favicon.ico','*.py']
	excludes = ['test','.*','*.pyc','*.pyo']
	local('rm -f dist/%s' % _TAR_FILE)
	with lcd(os.path.join(os.path.abspath('.'),'src')):
		local('pwd')
		cmd = ['tar','--dereference','-czvf', '"../dist/%s"' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))