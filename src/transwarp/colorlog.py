#!/usr/bin/env python 
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

INFO = 1;
WARNING = 2;
level = INFO

def logConfig(l=INFO):
	global level
	level =  l

def info(s,identify='INFO'):
	if level == INFO:
		print '[%s %s %s][%s %s %s] %s' % (bcolors.OKBLUE,identify,bcolors.ENDC,bcolors.HEADER,time.strftime('%H:%M'),bcolors.ENDC,s)

def warning(s,identify='WARNING'):		
	if level == WARNING:
		print '[%s %s %s][%s %s %s] %s' % (bcolors.OKGREEN,identify,bcolors.ENDC,bcolors.HEADER,time.strftime('%H:%M'),bcolors.ENDC,s)

if __name__ == '__main__':
	logConfig(l=INFO)
	info('it is info')
	logConfig(WARNING)
	warning('it is warning')