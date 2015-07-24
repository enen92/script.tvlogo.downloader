# -*- coding: utf-8 -*-
# Copyright (C) 2015 enen92
#
# This program is free software; you can redistribute it and/or modify it under the terms 
# of the GNU General Public License as published by the Free Software Foundation; 
# either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; 
# if not, see <http://www.gnu.org/licenses/>.

import json,urllib,urllib2
from addoncommon.tvldutils import *

API_BASE_URL = 'http://www.thelogodb.com/api/json/v1'
API_KEY = '7361'

class Channels:
	
	def __init__(self,):
		self.API_KEY = API_KEY
	
	def by_keyword(self,channel):
		url = '%s/%s/tvchannel.php?s=%s' % (API_BASE_URL,self.API_KEY,str(channel))
		data = json.load(get_page_source(url))
		return data["channels"]
		
	def by_country(self,country):
		url = '%s/%s/tvchannel.php?c=%s' % (API_BASE_URL,self.API_KEY,str(country))
		data = json.load(get_page_source(url))
		return data["channels"]
		
	def by_id(self,_id):
		url = '%s/%s/tvchannel.php?id=%s' % (API_BASE_URL,self.API_KEY,str(_id))
		data = json.load(get_page_source(url))
		return data["channels"]
		
	def by_package(self,package_id):
		url = '%s/%s/tvchannel.php?p=%s' % (API_BASE_URL,self.API_KEY,str(package_id))
		data = json.load(get_page_source(url))
		return data["channels"]
		
	def get_countries(self,):
		url = '%s/%s/tvchannelcountries.php' % (API_BASE_URL,self.API_KEY)
		data = json.load(get_page_source(url))
		return data["channels"]
		
		
class Packages:
	
	def __init__(self,):
		self.API_KEY = API_KEY
		
	def by_keyword(self,package):
		url = '%s/%s/tvpackage.php?s=%s' % (API_BASE_URL,self.API_KEY,str(package))
		data = json.load(get_page_source(url))
		return data["packages"]
		
	def by_country(self,country):
		url = '%s/%s/tvpackage.php?c=%s' % (API_BASE_URL,self.API_KEY,str(country))
		data = json.load(get_page_source(url))
		return data["packages"]
		
	def by_id(self,package_id):
		url = '%s/%s/tvpackage.php?id=%s' % (API_BASE_URL,self.API_KEY,str(package_id))
		data = json.load(get_page_source(url))
		return data["packages"]
		
	def get_all(self,):
		url = '%s/%s/tvpackage.php?c=%s' % (API_BASE_URL,self.API_KEY,'all')
		data = json.load(get_page_source(url))
		return data["packages"]
	


