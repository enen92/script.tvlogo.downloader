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
import json
import sys
from addoncommon.common_variables import *

def run():
	yes = xbmcgui.Dialog().yesno('TVLogo Downloader', 'Do you want to update the logos on your system?')
	if yes:
		if settings.getSetting('display_warning') == 'true':
			warning = xbmcgui.Dialog().yesno('TVLogo Downloader','Warning: This will change the logo folder in system->settings->TV->Menu/OSD','Do you want to proceed?')
			if warning:
				yes = xbmcgui.Dialog().yesno('TVLogo Downloader','Do you want to hide the warning on the next run?')
				if yes: settings.setSetting('display_warning','false')
		#proceed...
		addon_logo_folder = settings.getSetting('logo-folder')
		#get kodi logo folder
		json_response = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettingValue","params":{"setting":"pvrmenu.iconpath"},"id":9}')
		decoded_data = json.loads(json_response)
		kodi_logo_folder = decoded_data['result']['value']
		if addon_logo_folder.replace('\\','\\\\') != kodi_logo_folder:
			json_response = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"pvrmenu.iconpath","value":"'+addon_logo_folder.replace('\\','\\\\')+'"},"id":19}')
			decoded_data = json.loads(json_response)
			if decoded_data["result"] != True:
				mensagemok('TVLogo Downloader','Could not set the folder! Aborting')
				sys.exit(0)
	#check kodi version and trigger missing logos update
	refresh(yes,False)
	return

def refresh(yes,condition):
	if yes:
		versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
		#TODO drop older methods after Jarvis is stable
		if versionNumber >= 16:
			xbmc.executebuiltin('PVR.SearchMissingChannelIcons')
		else:
			xbmc.executebuiltin('StartPVRManager')
		if condition:
			xbmc.sleep(1000)
			xbmc.executebuiltin('Container.Refresh')
	return
	
