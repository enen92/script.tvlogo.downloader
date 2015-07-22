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



import xbmcplugin
import xbmcgui
import xbmc 
import xbmcaddon
import os
import sys
from resources.lib.addoncommon.common_variables import *
from resources.lib import tvlogodownloader



def get_params():
	try:
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
				params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
				splitparams={}
				splitparams=pairsofparams[i].split('=')
				if (len(splitparams))==2:
					param[splitparams[0]]=splitparams[1]
	except: pass                     
	return param

      
params=get_params()
url=None
name=None
mode=None
iconimage=None
regexs=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass

try:
    regexs=params["regexs"]
except:
    pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)


if mode==None or url==None or len(url)<1:
	if settings.getSetting('logo-folder') == "":
		mensagemok('TVLogo Downloader','Please configure the download folder!')
		xbmc.executebuiltin('XBMC.Addon.OpenSettings('+addon_id+')')
		mensagemok('TVLogo Downloader','Re-enter the addon to proceed')
		sys.exit(0)
	else:
		tvlogodownloader.main_menu()

elif mode==1:
	calendar()
	
	
try:		
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
except: sys.exit(0)
