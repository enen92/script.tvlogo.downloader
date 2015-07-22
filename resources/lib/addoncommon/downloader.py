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

import xbmc,xbmcgui
import os
import urllib
import time
import thelogodb
from common_variables import *


class Downloader:

	def __init__(self,dictionary,replace):
		self.dictionary = dictionary
		self.logo_folder = settings.getSetting('logo-folder')
		self.log = '[B]DOWNLOADED LOGOS:[/B]\n\n'
		if replace:
			for channel in self.dictionary:
				channel_url = channel['channel_logo']
				channel_name = channel['channel_name']
				channel_selected = channel['selected_channel']
				localfile = os.path.join(self.logo_folder,channel_selected+'.png')
				self.download(localfile,channel_url,channel_name,self.log)
		else:
			for channel in self.dictionary:
				channel_url = channel['channel_logo']
				channel_name = channel['channel_name']
				localfile = os.path.join(self.logo_folder,channel_name+'.png')
				self.download(localfile,channel_url,channel_name,self.log)
				
		print self.log
		

	def download(self,path,url,name,log):
		if os.path.isfile(path) is True:
			while os.path.exists(path): 
				try: os.remove(path); break 
				except: pass
				  
		dp = xbmcgui.DialogProgress()
		dp.create('TVLogo Downloader')
		dp.update(0,name)
		xbmc.sleep(500)
		start_time = time.time()
		try: 
			urllib.urlretrieve(url, path, lambda nb, bs, fs: self.dialogdown(name,nb, bs, fs, dp, start_time))
			dp.close()
			log=log+name+':'+path+'\n'
			return True
		except:
			while os.path.exists(path): 
				try: os.remove(path); break 
				except: pass
			dp.close()
			return False
			
	def dialogdown(self,name,numblocks, blocksize, filesize, dp, start_time):
		try:
			percent = min(numblocks * blocksize * 100 / filesize, 100)
			currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
			kbps_speed = numblocks * blocksize / (time.time() - start_time) 
			if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
			else: eta = 0 
			kbps_speed = kbps_speed / 1024 
			total = float(filesize) / (1024 * 1024) 
			mbs = '%.02f MB %s %.02f MB' % (currently_downloaded,'downloaded', total) 
			e = ' (%.0f Kb/s) ' % kbps_speed 
			tempo = 'Tempo:' + ' %02d:%02d' % divmod(eta, 60) 
			dp.update(percent,name +' - '+ mbs + e,tempo)
		except: 
			percent = 100 
			dp.update(percent) 
		if dp.iscanceled(): 
			dp.close()
			raise StopDownloading('Stopped Downloading')
            
class StopDownloading(Exception):
	def __init__(self, value): self.value = value 
	def __str__(self): return repr(self.value)
	

def download_entire_package(packageid):
	channels = thelogodb.Channels().by_package(packageid)
	print channels
