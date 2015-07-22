# -*- coding: utf-8 -*-

""" 
File manipulation
"""
    
import os

def readfile(filename):
	f = open(filename, "r")
	string = f.read()
	return string
 
def save(filename,contents):
	fh = open(filename, 'w')
	fh.write(contents)
	fh.close()
	return
