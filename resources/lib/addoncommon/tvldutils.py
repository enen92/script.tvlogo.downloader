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

import urllib2
import os
import re
from PIL import Image
from common_variables import *

def channel_to_downloaddict(channel,rename_to=None):
	if not rename_to: channel_dict = {'channel_name': channel["strChannel"] ,'channel_logo': channel["strLogoWide"]}
	else: channel_dict = {'channel_name': channel["strChannel"] ,'channel_logo': channel["strLogoWide"],'selected_channel':rename_to}
	return channel_dict
	
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def return_only_valid(match):
	match2 = []
	if match:
		for ch in match:
			if ch['strLogoWide']: match2.append(ch)
		match = match2
		del match2
		return match
	else: return []
	
def get_replaced_names(channel):
	keywords = settings.getSetting("ignore_words").split(',')
	if keywords:
		for keyword in keywords:
			channel=channel.replace(keyword,'')
			resub = keyword.replace('[','\[').replace(']','\]')
			channel = re.sub(resub,'',channel)
	return channel
	

def get_page_source(url):
	try: source = urllib2.urlopen(url)
	except: source = '{ channels = {},packages= {} }'
	return source
	
def resize(localfile):
	if settings.getSetting('resize_logos') == 'true' and int(settings.getSetting('resize_ratio')):
		#resize
		if os.path.exists(localfile):
			img = Image.open(localfile)
			percent = int(settings.getSetting('resize_ratio'))
			w,h = img.size
			img.thumbnail(((percent*w)/100,(percent*h)/100))
			img.save(localfile)
			print "Image " + localfile + " resized!"
			return True	
		else:
			print "File " + localfile +" does not exist. It will not be resized"
			return False
	else:
		return False

