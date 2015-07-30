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
from resources.lib import context

def get_params():
	param=[]
	try: paramstring=sys.argv[1]
	except: paramstring = ''
	if len(paramstring)>=2:
		params=sys.argv[1]
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=params.split('/')
		for parm in pairsofparams:
			if parm == '':
				pairsofparams.remove(parm)      
	return pairsofparams

try: params=get_params()
except: params = []

if not params:
	if settings.getSetting('logo-folder') == "":
		mensagemok('TVLogo Downloader','Please configure the download folder!')
		xbmc.executebuiltin('XBMC.Addon.OpenSettings('+addon_id+')')
		mensagemok('TVLogo Downloader','Re-enter the addon to proceed')
		sys.exit(0)
	else:
		tvlogodownloader.main_menu()

else:
	if params[0] == 'context':
		context.run('/'.join(params[1:]))

try: xbmcplugin.endOfDirectory(int(sys.argv[1]))
except: sys.exit(0)
